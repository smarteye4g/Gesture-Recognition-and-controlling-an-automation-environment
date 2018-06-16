import os
import time
import operator
alist={}
now = time.time()
directory=os.path.join("/home","/home/ubuntu/Documents/Gesture_Recognition/Gestures/Training/Right")
os.chdir(directory)
for file in os.listdir("."):
    if os.path.isdir(file):
        timestamp = os.path.getmtime( file )
        # get timestamp and directory name and store to dictionary
        alist[os.path.join(os.getcwd(),file)]=timestamp

# sort the timestamp
for i in sorted(alist.iteritems(), key=operator.itemgetter(1)):
    latest="%s" % ( i[0])
# latest=sorted(alist.iteritems(), key=operator.itemgetter(1))[-1]
print "newest directory is ", latest
os.chdir(latest)