#
# Author: Philipp Jaehrling philipp.jaehrling@gmail.com)
#
import tensorflow as tf
import numpy as np

from models.model import Model

class VGG(Model):
    """
    VGG16 model definition for Tensorflow
    """
    # TODO might use a param to init the net as VGG 19 (adds conv3_4, conv4_4, conv5_4)

    input_width = 224
    input_height = 224
    subtract_imagenet_mean = True
    use_bgr = True

    def __init__(self, tensor, keep_prob, num_classes, retrain_layer, weights_path='./weights/vgg16.npy'):
        # Call the parent class, which will create the graph
        Model.__init__(self, tensor, keep_prob, num_classes, retrain_layer, weights_path)

    def create(self):
        # 1st Layer: Conv -> Conv -> Pool
        # conv(tensor, filter_height, filter_width, num_filters, stride_y, stride_x, name, padding)
        conv1_1 = Model.conv(self.tensor, 3, 3, 64, 1, 1, padding='SAME', name='conv1_1')
        conv1_2 = Model.conv(conv1_1    , 3, 3, 64, 1, 1, padding='SAME', name='conv1_2')
        pool1   = tf.nn.max_pool(conv1_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool1')
        
        # 2nd Layer: Conv -> Conv -> Pool
        conv2_1 = Model.conv(pool1  , 3, 3, 128, 1, 1, padding='SAME', name='conv2_1')
        conv2_2 = Model.conv(conv2_1, 3, 3, 128, 1, 1, padding='SAME', name='conv2_2')
        pool2   = tf.nn.max_pool(conv2_2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool2')

        # 3rd Layer: Conv -> Conv -> Conv -> Pool
        conv3_1 = Model.conv(pool2  , 3, 3, 256, 1, 1, padding='SAME', name='conv3_1')
        conv3_2 = Model.conv(conv3_1, 3, 3, 256, 1, 1, padding='SAME', name='conv3_2')
        conv3_3 = Model.conv(conv3_2, 3, 3, 256, 1, 1, padding='SAME', name='conv3_3')
        pool3   = tf.nn.max_pool(conv3_3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool3')

        # 4th Layer: Conv -> Conv -> Conv -> Pool
        conv4_1 = Model.conv(pool3  , 3, 3, 512, 1, 1, padding='SAME', name='conv4_1')
        conv4_2 = Model.conv(conv4_1, 3, 3, 512, 1, 1, padding='SAME', name='conv4_2')
        conv4_3 = Model.conv(conv4_2, 3, 3, 512, 1, 1, padding='SAME', name='conv4_3')
        pool4   = tf.nn.max_pool(conv4_3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool4')

        # 5th Layer: Conv -> Conv -> Conv -> Pool
        conv5_1 = Model.conv(pool4  , 3, 3, 512, 1, 1, padding='SAME', name='conv5_1')
        conv5_2 = Model.conv(conv5_1, 3, 3, 512, 1, 1, padding='SAME', name='conv5_2')
        conv5_3 = Model.conv(conv5_2, 3, 3, 512, 1, 1, padding='SAME', name='conv5_3')
        pool5   = tf.nn.max_pool(conv5_3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME', name='pool5')

        # 6th Layer: FC -> DropOut
        # [1:] cuts away the first element
        pool5_out  = int(np.prod(pool5.get_shape()[1:])) # 7 * 7 * 512 = 25088
        pool5_flat = tf.reshape(pool5, [-1, pool5_out]) # shape=(image count, 7, 7, 512) -> shape=(image count, 25088)
        fc6        = Model.fc(pool5_flat, num_in=pool5_out, num_out=4096, name='fc6', relu=True)
        dropout1   = tf.nn.dropout(fc6, self.keep_prob)

        # 7th Layer: FC
        fc7      = Model.fc(dropout1, num_in=4096, num_out=4096, name='fc7', relu=True)
        dropout2 = tf.nn.dropout(fc7, self.keep_prob)

        # 8th Layer: FC
        fc8 = Model.fc(dropout2, num_in=4096, num_out=self.num_classes, name='fc8', relu=False)
        self.final = fc8
