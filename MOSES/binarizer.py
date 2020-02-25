import abc
import numpy as np
import pandas as pds

class Binarizer:
    def __init__(self):
        pass

    @abc.abstractmethod
    def binarize(self, input_vec, bins):
        '''
         Given a feature vector of N x 1 and bins size B
         returns a matrix of N x B binary matrix.
        '''
        pass


class QuantileBinarizer(Binarizer):
    def __init__(self):
        pass

    def binarize(self, input_vec, bins):
       '''
         Given a feature vector of N x 1 numeric values and bins size B
         Returns matrix of N x B binary matrix using quantiles
         for creating the bins.
       '''
       #TODO check input_vec is a real number vector and numpy array
       quantiles = []
       for i in range(1, bins-1):
           quantiles.append(np.quantile(input_vec, float(i)/(bins-1)))

       binary_matrix = []
       for x in input_vec:
           bit_array = [0] * bins
           # TODO use binary search instead.
           for i in range(quantiles):
               if x <= quantiles[i]:
                   bit_array[i] = 1
                   break
               if i == len(quantiles) - 1 and x > quantiles[i]:
                   bit_array[i] = 1
           if 1 not in bit_array:
               raise Exception('There should be a 1 in the bit array.')
           binary_matrix.append(bit_array)

       return binary_matrix
# Add more binarization classes here.

class BinarizationFactory:
    def __init__(self):
        pass

    def get_binarizer(self, name):
        if name == 'QuantileBinarizer':
            return QuantileBinarizer()
        else:
            raise Exception('Unable to instantiate an Binarizer Object for {}'.format(name))
