# https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv/43111221
# Arduino https://qna.habr.com/q/537925

import cv2, numpy as np
from sklearn.cluster import KMeans
import  time
from _testbuffer import ndarray
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # choose BCM numbering scheme.

GPIO.setup(17, GPIO.OUT)# set GPIO 17 as output for white led
GPIO.setup(27, GPIO.OUT)# set GPIO 27 as output for red led
GPIO.setup(22, GPIO.OUT)# set GPIO 22 as output for red led

hz = 75 # the frequency in Herz (recommended:75)


def visualize_colors(cluster, centroids):
    # Get the number of different clusters, create histogram, and normalize
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins=labels)
    hist = hist.astype("float")
    hist /= hist.sum()
    # Create frequency rect and iterate through each cluster's color and percentage
    rect = np.zeros((50, 300, 3), dtype=np.uint8)
    colors = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])

    line = list(max(colors))
    rgb = []
    print(line)
    for k in line:
        print(type(k))
        if type(k) == np.ndarray:
            rgb = np.ndarray.tolist(k)
    start = 0

    for (percent, color) in colors:
        print(color, "{:0.2f}%".format(percent * 100))
        """
        end = start + (percent * 300)
        cv2.rectangle(rect, (int(start), 0), (int(end), 50), \
                      color.astype("uint8").tolist(), -1)
        start = end
        """
    return tuple(rgb)


# Load image and convert to a list of pixels
cap = cv2.VideoCapture(0)
ret, image = cap.read()
# cv2.imshow('image', image)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# cv2.waitKey()
reshape = image.reshape((image.shape[0] * image.shape[1], 3))
# Find and display most dominant colors
cluster = KMeans(n_clusters=5).fit(reshape)
visualize = visualize_colors(cluster, cluster.cluster_centers_)
for k in visualize:
    print(str(k).encode())

# visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
# cv2.imshow('visualize', visualize)

reddc =int(visualize[0]) # define the red LED Duty Cycle
greendc = int(visualize[1]) # define the green LED Duty Cycle
bluedc = int(visualize[2]) # define the blue LED Duty Cycle

print(reddc, greendc, bluedc)

red = GPIO.PWM(17, hz)    # create object red for PWM on port 17
green = GPIO.PWM(27, hz)      # create object green for PWM on port 27
blue = GPIO.PWM(22, hz)      # create object blue for PWM on port 22

red.start((reddc/2.55))   #start red led
green.start((greendc/2.55)) #start green led
blue.start((bluedc/2.55))  #start blue led

time.sleep(10)

red.stop()   #stop red led
green.stop() #stop green led
blue.stop()  #stop blue led
GPIO.cleanup()


