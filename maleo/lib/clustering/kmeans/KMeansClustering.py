"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Copyright (C) 2020 Henrico Aldy Ferdian & Lennia Savitri Azzahra Loviana
Udayana University, Bali, Indonesia
"""

# Python Library
import multiprocessing
import sys

# Third Party Library
import tensorflow as tf

# Inherit
from maleo.lib.classification.neuralnetwork.neural_network import NeuralNetwork

class KMeansClustering(NeuralNetwork):
    def __init__(self, data, labels, *args):
        super(KMeansClustering, self).__init__(data, labels)
        self.activationFunction = "relu"
        self.name = "K-Means Clustering"

    def get_name(self):
        return self.name

    def get_supported_operations(self):
        return "DataType.Numeric", "DataType.Nominal"

    def get_unsupported_operations(self):
        return None

    def get_available_settings(self):
        return {
                "set_activation_function":{
                    "name":"Fungsi Aktivasi",
                    "params":{
                        "param1":{
                                "type":"DataType.DropDown",
                                "options":["sigmoid","relu"]
                            }
                        }
                    }
                }

    def set_activation_function(self, param1=None):
        self.activationFunction = param1

    def start_operation(self):
        try:
            self.proc = multiprocessing.Process(target=self.train(), args=())
            self.proc.start()
        except Exception as e:
            print(e)

    def stop_operation(self):
        print("KMeans Clustering stopped")
        sys.stdout = self.originalStdOut
        try:
            self.proc.terminate()
        except Exception as e:
            print(e)

    def set_output_widget(self, output):
        self.outputWidget = output

    def train(self):
        self.originalStdOut = sys.stdout
        sys.stdout = self.outputWidget

        print("Convolutional Neural Network with Tensorflow")
        print("Activation Function :",self.activationFunction)
        print("Dataset :",self.data)
        print("Labels :",self.labels)

        out = self.labels.nunique()

        self.preprocess_data()

        self.ltrain = tf.keras.utils.to_categorical(self.ltrain, out)
        self.ltest = tf.keras.utils.to_categorical(self.ltest, out)

        self.model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(out*2, activation='relu'),
            tf.keras.layers.Dense(out)
        ])

        self.model.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
                      optimizer='adam',
                      metrics=['acc'])

        self.history = self.model.fit(x=self.dtrain,y=self.ltrain,epochs=self.numEpochs,batch_size=self.batchSize,validation_data=(self.dtest,self.ltest), verbose=1)


        self.model.summary()
        self.stopOperation()
