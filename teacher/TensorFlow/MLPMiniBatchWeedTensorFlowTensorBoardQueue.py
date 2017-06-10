# MLP
#
# This example:
# - Trains a neural network. The Adam optimizer is employed. Its parameters may need tuning.
# - Monitors the learning using a validation data set.
# - Stores the network with the lowest validation error in a file. At the end, this network is loaded and evaluated.
# - Uses a queue for thetraining data (not for test and validation).

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

# Flags
flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_string('summary_dir', '/tmp/MLPMiniLog', 'directory to put the summary data')
flags.DEFINE_string('data_dir', '../data', 'directory with data')
flags.DEFINE_integer('maxIter', 10000, 'number of iterations')
flags.DEFINE_integer('batchSize', 64, 'batch size')
flags.DEFINE_integer('noHidden1', 64, 'size of first hidden layer')
flags.DEFINE_integer('noHidden2', 32, 'size of second hidden layer')
flags.DEFINE_float('lr', 0.0001, 'initial learning rate')

# Read data test and validation data
dataTest = tf.contrib.learn.datasets.base.load_csv_without_header(filename=FLAGS.data_dir + '/LSDA2017WeedCropTest.csv', target_dtype=np.int, features_dtype=np.float32, target_column=-1)
dataValidate = tf.contrib.learn.datasets.base.load_csv_without_header(filename=FLAGS.data_dir + '/LSDA2017WeedCropValidation.csv', target_dtype=np.int, features_dtype=np.float32, target_column=-1)

# Set up queue for training data
with tf.name_scope('input_queue') as scope:
    filename_queue = tf.train.string_input_producer([FLAGS.data_dir + '/LSDA2017WeedCropTrain.csv'])
    reader = tf.TextLineReader(skip_header_lines = 0)
    _, value = reader.read(filename_queue)

    inDim = 13 # input dimension
    record_defaults = [[1.0] for _ in range(inDim)] # define all input features to be floats
    record_defaults.append([1]) # add the label as an integer
    content = tf.decode_csv(value, record_defaults)
    features = tf.stack(content[:inDim]) # pack all inDIm features into a tensor
    label = content[-1] # assign the last column to label

    # Minimum number elements in the queue after a dequeue, used to ensure that the samples are sufficiently mixed
    min_after_dequeue = 10 * FLAGS.batchSize
    # Maximum number of elements in the queue
    capacity = 20 * FLAGS.batchSize
    # Shuffle the data to generate BatchSize sample pairs
    data_batch = tf.train.shuffle_batch([features,label], batch_size = FLAGS.batchSize, capacity = capacity,
                                        min_after_dequeue = min_after_dequeue)

# Create session
sess = tf.Session()

# Initialize placeholders
x_data = tf.placeholder(shape=[None, inDim], dtype=tf.float32, name='input')
y_target = tf.placeholder(shape=[None, 1], dtype=tf.float32, name='target')

# Define variables
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1) # restrict to +/- 2*stddev
    return tf.Variable(initial, name='weights')

def bias_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial, name='bias')


# Define model
with tf.name_scope('layer1') as scope:
    W_1 = weight_variable([inDim, FLAGS.noHidden1])
    b_1 = bias_variable([FLAGS.noHidden1])
    y_1 = tf.nn.sigmoid(tf.matmul(x_data, W_1) + b_1)
    
with tf.name_scope('layer2') as scope:
    W_2 = weight_variable([FLAGS.noHidden1, FLAGS.noHidden2])
    b_2 = bias_variable([FLAGS.noHidden2])
    y_2 = tf.nn.sigmoid(tf.matmul(y_1, W_2) + b_2)

with tf.name_scope('layer3') as scope:
    W_3 = weight_variable([FLAGS.noHidden2, 1])
    b_3 = bias_variable([1])
    model_output = tf.matmul(y_2, W_3) + b_3


# Declare loss function
loss = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=model_output, labels=y_target), name='mean_cross-entropy')
tf.summary.scalar('cross-entropy', loss)

# Declare optimizer
my_opt = tf.train.AdamOptimizer(FLAGS.lr)
train_step = my_opt.minimize(loss)

# Map model output to binary predictions
with tf.name_scope('binary_predictions') as scope:
    prediction = tf.round(tf.sigmoid(model_output))
    predictions_correct = tf.cast(tf.equal(prediction, y_target), tf.float32)
accuracy = tf.reduce_mean(predictions_correct, name='mean_accuracy')
tf.summary.scalar('accuracy', accuracy)

# Logging
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter(FLAGS.summary_dir + '/train')
test_writer = tf.summary.FileWriter(FLAGS.summary_dir + '/test')
validate_writer = tf.summary.FileWriter(FLAGS.summary_dir + '/validate')
writer = tf.summary.FileWriter(FLAGS.summary_dir, sess.graph)
saver = tf.train.Saver() # for storing the best network

# Initialize variables
init = tf.global_variables_initializer()
sess.run(init)

# Best validation accuracy seen so far
bestValidation = 0.0

# Training loop
coord = tf.train.Coordinator() # coordinator for threads
threads = tf.train.start_queue_runners(coord = coord, sess=sess) # start queue thread

for i in range(FLAGS.maxIter):
    xTrain, yTrain = sess.run(data_batch)
    sess.run(train_step, feed_dict={x_data: xTrain, y_target: np.transpose([yTrain])})
    summary = sess.run(merged, feed_dict={x_data: xTrain, y_target: np.transpose([yTrain])})
    train_writer.add_summary(summary, i)
    if((i+1)%100==0):
        print("Iteration:",i+1,"/",FLAGS.maxIter)
        summary = sess.run(merged, feed_dict={x_data: dataTest.data, y_target: np.transpose([dataTest.target])})
        test_writer.add_summary(summary, i)
        currentValidation, summary = sess.run([accuracy, merged], feed_dict={x_data: dataValidate.data, y_target: np.transpose([dataValidate.target])})
        validate_writer.add_summary(summary, i)
        if(currentValidation > bestValidation):
            bestValidation = currentValidation
            saver.save(sess=sess, save_path=FLAGS.summary_dir + '/bestNetwork')
            print("\tbetter network stored,",currentValidation,">",bestValidation)

coord.request_stop() # ask threads to stop
coord.join(threads)  # wait for threads to stop

# Print values after last training step
print("final test accuracy: ", sess.run(accuracy, feed_dict={x_data: dataTest.data, y_target: np.transpose([dataTest.target])}),
      "final validation accuracy: ", sess.run(accuracy, feed_dict={x_data: dataValidate.data, y_target: np.transpose([dataValidate.target])}))

# Load the network with the lowest validation error
saver.restore(sess=sess, save_path=FLAGS.summary_dir + '/bestNetwork')
print("best test accuracy: ", sess.run(accuracy, feed_dict={x_data: dataTest.data, y_target: np.transpose([dataTest.target])}),
      "best validation accuracy: ", sess.run(accuracy, feed_dict={x_data: dataValidate.data, y_target: np.transpose([dataValidate.target])}))



