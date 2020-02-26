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
       for i in range(1, bins):
           quantiles.append(np.quantile(input_vec, float(i)/(bins)))
       #print('InputVec: {}'.format(input_vec))
       #print('Bins: {}'.format(bins))
       #print('Quantiles: {}'.format(quantiles))
       binary_matrix = []
       for x in input_vec:
           bit_array = [0] * bins
           # TODO use binary search instead.
           for i in range(len(quantiles)):
               if x <= quantiles[i]:
                   bit_array[i] = 1
                   break
               if i == len(quantiles) - 1 and x > quantiles[i]:
                   bit_array[i+1] = 1
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


def test_binarize():
    xdf = pds.DataFrame({'nums': [i for i in range(0,11)]})
    binarizer = QuantileBinarizer()
    result = binarizer.binarize(xdf['nums'].to_numpy(), 2)
    assert( result[0] == [1,0])
    assert( result[6] == [0,1])
    assert( result[7] == [0,1])
    result = binarizer.binarize(xdf['nums'].to_numpy(), 5)
    assert( result[0] == [1,0,0,0,0])
    assert( result[4] == [0,1,0,0,0])
    assert( result[9] == [0,0,0,0,1])


if __name__ == '__main__':
    test_binarize()
