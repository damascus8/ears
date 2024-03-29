import cv2
import os
#import monitoring3
 

def extractFrames(pathIn, pathOut):
	os.mkdir(pathOut)
	 
	cap = cv2.VideoCapture(pathIn)
	count = 0
 
	while (cap.isOpened()):
 
# Capture frame-by-frame
		ret, frame = cap.read()
 
		if ret == True:
            #print('Read %d frame: ' % count, ret)
			if count%2 == 0:
				cv2.imwrite(os.path.join(pathOut, "frame{:d}.jpg".format(count)), frame)  # save frame as JPEG file
			count += 1
		else:
			break

	print("Total Frames - ",count)
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
 
#def main():
#	videoName="accident"
#	folderName = videoName+'Frames'
#	extractFrames(videoName, folderName)
 
#if __name__=="__main__":
#    main()
