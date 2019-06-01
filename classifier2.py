import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from os import listdir
from os.path import isfile, join
import numpy
import cv2
import glob
import os
import dbConnection as db
import shutil, os
import Message

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

import os
import sys

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class AccidentsClassifier(object):
    def __init__(self):
        PATH_TO_MODEL = 'graph/frozen_inference_graph.pb'
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            # Works up to here.
            with tf.gfile.GFile(PATH_TO_MODEL, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            self.d_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            self.d_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.d_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_d = self.detection_graph.get_tensor_by_name('num_detections:0')

        self.sess = tf.Session(graph=self.detection_graph)

    def get_classification(self, img):
        # Bounding Box Detection.
        with self.detection_graph.as_default():
            # Expand dimension since the model expects image to have shape [1, None, None, 3].
            img_expanded = np.expand_dims(img, axis=0)
            (boxes, scores, classes, num) = self.sess.run(
                [self.d_boxes, self.d_scores, self.d_classes, self.num_d],
                feed_dict={self.image_tensor: img_expanded}
            )
        return boxes, scores, classes, num


def classify(path):
    PATH_TO_LABELS = 'accidents.pbtxt'
    NUM_CLASSES = 1

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    data_path = os.path.join(path, '*jpg')
    files = glob.glob(data_path)
    count = 0
    input_image = []
    accident_detected = False;
    threshold = 80;
    for input1 in files :
        input_image = input1
        count = count + 1
        img = plt.imread(input_image)  # [::-1,:,::-1]
        img.setflags(write=1)
        x = AccidentsClassifier()
        boxes, scores, classes, num = x.get_classification(img)
        per = 100* np.squeeze(scores)[0]
        print("----------------")
        print(per)
        if per >= threshold :
            accident_detected = True
        print("--------------------------")	
        print(per)
        # print(type(np.squeeze(scores)))
        # print(np.squeeze(classes).astype(np.int32))
        # print("---------------")
        vis_util.visualize_boxes_and_labels_on_image_array(img, np.squeeze(boxes), np.squeeze(classes).astype(np.int32),
                                                           np.squeeze(scores), category_index,
                                                           use_normalized_coordinates=True, line_thickness=8)
    # Update accident detected variable.
    if (accident_detected):
        # send this video file so that it would visible on dashboard, make an entry into database and move video to folder from which 				its getting served
        newVidPath = path
        ind = newVidPath.rfind("/")
        ind = ind + 1
        newVidPathLength = len(newVidPath)
        newVidName = newVidPath[ind: newVidPathLength]
        # print(newVidName)
        videoPath = '/home/pradnya/Downloads/EARS-master/Python_Demo/videos/' + newVidName
        shutil.copy(videoPath,
                    '/home/pradnya/Downloads/EARS-master/Python_Demo/videos-to-show')
        #print(files)
        db.insertVideoName(newVidName,"wagholi")
        link = "http://127.0.0.1:5000/videos/" + newVidName
        Message.sendMessage(link)

    # send an SMS with link of an video
    # plt.imsave("frame{:d}.jpg".format(count), img)

    print("done")
    print(path)
