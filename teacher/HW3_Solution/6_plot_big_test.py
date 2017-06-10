import numpy
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

data = numpy.genfromtxt("big_predictions_test.csv", delimiter=",", dtype=int) 
plt.imshow(data.reshape(3000,3000), cmap='hot', interpolation='nearest')
plt.show()
