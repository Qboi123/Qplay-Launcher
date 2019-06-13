import numpy as np
import json

with open("input.json", "r") as file:
    json_str = file.read()
    json_inputs = json.decoder.JSONDecoder().decode(json_str)

with open("output.json", "r") as file:
    json_str = file.read()
    json_outputs = json.decoder.JSONDecoder().decode(json_str)


class NeuralNetwork(object):
    def __init__(self):
        np.random.seed(1)

        self.synaptic_weights = 2 * np.random.random((6, 1)) - 1

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def train(self, inputs, outputs, iterations):
        for iteration in range(iterations):
            output = self.think(inputs)
            error = outputs - output
            adjustments = np.dot(inputs.T, error * self.sigmoid_derivative(output))
            self.synaptic_weights += adjustments

    def think(self, inputs):
        inputs = inputs.astype(float)
        output = self.sigmoid(np.dot(inputs, self.synaptic_weights))

        return output


if __name__ == '__main__':
    neural_network = NeuralNetwork()
    print("Random synaptic weights: \n%s" % neural_network.synaptic_weights)

    training_inputs = np.array(json_inputs)

    training_outputs = np.array(json_outputs).T

    neural_network.train(training_inputs, training_outputs, 100000)

    print("Synaptic weights after training: \n%s" % neural_network.synaptic_weights)

    while True:
        print()
        Z = str(input("Input: "))
        if len(Z) != 6:
            continue
        LIST = list(Z)

        OUT = neural_network.think(np.array(LIST))

        print("New situation: input data =", *LIST)
        print('Output data: %s' % int(round(OUT[0], 0)))
