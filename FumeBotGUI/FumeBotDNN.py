import os
import cv2
import numpy as np
import tensorflow as tf
from PyQt4 import QtCore

from keras.models import model_from_json


class FumeBotDNN(QtCore.QObject):

    dnnOutputKeyPress=QtCore.pyqtSignal(list)

    def __init__(self):
        super(FumeBotDNN, self).__init__()

        self.frame_width=80
        self.frame_height=60
        self.frame_channels=1

        # Model name and path should be changed here
        self.model_file='Fumebot-0.0001-AlexNet-12-model-95AP.json'
        self.model_file_path=os.path.expanduser('~\\Documents\\FumeBot - DNN Model\\Project Models')
        self.model_path_to_file=os.path.join(self.model_file_path,self.model_file)

        # Weight file name and path should be changed here
        self.weight_file='Fumebot-0.0001-AlexNet-12-weight-95AP.h5'
        self.weight_file_path=os.path.expanduser('~\\Documents\\FumeBot - DNN Model\\Project Models')
        self.weight_path_to_file=os.path.join(self.weight_file_path,self.weight_file)

        # Loading the model from JSON file
        model_json_file = open(self.model_path_to_file, 'r')
        self.loaded_model_json = model_json_file.read()
        model_json_file.close()

        self.loaded_model = model_from_json(self.loaded_model_json)  # Model loaded

        # Load weights into the loaded model
        self.loaded_model.load_weights(self.weight_path_to_file)

        self.graph = tf.get_default_graph()

    def dnn_model_prediction(self, dnn_input):

        input_frame=cv2.resize(dnn_input, (self.frame_width, self.frame_height), interpolation=cv2.INTER_LINEAR)
        input_frame=cv2.cvtColor(input_frame,cv2.COLOR_BGR2GRAY)  # Convert grayscale
        input_frame=input_frame.reshape(-1,self.frame_width,self.frame_height,self.frame_channels)

        # Neural Network prediction goes here
        with self.graph.as_default():
            output=self.loaded_model.predict(x=input_frame, batch_size=None, verbose=0, steps=None)
            output=np.around(output[0])
            move_list=list(output.astype(int))  # Convert the numpy array to a list

            self.dnnOutputKeyPress.emit(move_list)
