import os
import glob
 


img_dir='/home/mutex/BE_Project_2019/EARS-master/accidentFrames'
data_path=os.path.join(img_dir,'*jpg')
files=glob.glob(data_path)

f = []
for input1 in files:
	f=input1
	print(f)
'''
f1 = []
for f1 in files:
	c=classifier2.AccidentsClassifier(f1)

#print('done')
'''

'''
mylist = os.listdir('/home/mutex/BE_Project_2019/EARS-master/accidentFrames')

for filename in mylist:
	print(filename)

data = []

'''	

