from binarizer import BinarizationFactory
import argparse
import json
import logging
import os
import numpy as np
import pandas as pds

def binarize(data, config):
    '''
      Binarizes given DataFrame according to the config params.
      Returns a set of binarized DataFrames for each inputFeatures.
    '''
    input_feat_config = config['inputFeatures']
    logging.info('Config:\n{}'.format(input_feat_config))
    feat_binarized_DFs = {}
    logging.info('Binarizing')
    for  dct in input_feat_config:
        feat_name = dct['name']
        bins_to_try = dct['bins']
        binarizer = BinarizationFactory().get_binarizer(dct['binarizer'])
        logging.info('Feat: {} Bins: {}'.format(feat_name, bins_to_try))
        binarizations = []
        for bins in bins_to_try:
            bin_matrix = binarizer.binarize(data[feat_name].to_numpy(), bins)
            # build dataFrame
            df_columns = {}
            for i in range(bins):
                df_columns[feat_name+'_bin'+str(i)] = np.array(bin_matrix)[:,i]
            binarizations.append(pds.DataFrame(df_columns))
        logging.info('Result:\n{}'.format(binarizations))
        feat_binarized_DFs[feat_name] = binarizations

    return feat_binarized_DFs

def binarize_target(target_vec, la_years):
    '''
     UP vs DOWN/NEURTRAL binarizer.
    '''
    feat_bin_vec_dict = {}
    for la_year in la_years:
        bin_vec = []
        for i in range(len(target_vec) - la_year):
            if target_vec[i] < target_vec[i+la_year]:
                bin_vec.append(1) # UP
            else:
                bin_vec.append(0) # DOWN OR NEUTRAL
        feat_bin_vec_dict[la_year] = bin_vec

    return feat_bin_vec_dict

def _cartesian(elements_set):
    '''
    Returns a list of the cartesian product given a list
    of sets of objects. eg. input: [[a,b], [c]] output: [[a,c], [b,c]]
    '''
    result = []
    if len(elements_set) == 0:
        return result
    if len(elements_set) == 1:
        return [[e] for e in elements_set[0]]
    for i in range(0, 1):
        products = _cartesian(elements_set[i+1: ])
        for j in range(0, len(elements_set[i])):
            for prdct in products:
                result.append([elements_set[i][j]] + prdct)

    return result

def combine_all(feat_bin_matrix):
    '''
    input: A map of feature name and list of binary panda DataFram objects
    output: A list of all combination of binary matrix from concatenating each feat binarization
    '''
    combinations = _cartesian(list(feat_bin_matrix.values()))
    dfs = []
    for combination in combinations:
        df_merged = combination[0]
        for df in combination[1:]:
            assert(df_merged.shape[0] == df.shape[0])
            df_merged = pds.merge(df_merged, df, left_index=True, right_index=True)

        dfs.append(df_merged)

    return dfs

def main():
    usage = "usage: %prog [options]\n"
    parser = argparse.ArgumentParser(usage)
    parser = argparse.ArgumentParser(usage)
    parser.add_argument("-i", "--input", nargs=1, help = "Input data.")
    parser.add_argument("-d", "--dump_dir", nargs=1, help = "Binarized data dumping dir.")
    parser.add_argument("-c", "--config", nargs=1, help = "Config file.")
    args = parser.parse_args()

    if args.input and args.dump_dir and args.config:
       dump_dir =  os.path.abspath(os.path.expanduser(args.dump_dir[0])) #expanduser for tilde expansion
       data = pds.read_csv(args.input[0])
       # Load config file
       config = None
       with open(args.config[0], 'r') as jsonf:
           config = json.load(jsonf)

       logging.basicConfig(filename='transformer.log', level=logging.WARNING)

       list_of_feat_bin_matrix = binarize(data, config)
       list_of_bin_matrix = combine_all(list_of_feat_bin_matrix)

       for matrix in list_of_bin_matrix:
           logging.info('{}\n'.format(matrix))

       target = config['targetFeature']
       predictions = binarize_target(data[target].to_numpy(), config['LA_years'])
       # Resize Input to Length(Input) - K for K look-ahead years prediction and merge.
       for la_years in predictions.keys():
           vec = predictions[la_years]
           for i in range(len(list_of_bin_matrix)):
               list_of_bin_matrix[i].drop(list_of_bin_matrix[i].tail(la_years).index,inplace=True)
               target_feat_bin_vec = pds.DataFrame({target:vec})
               assert(list_of_bin_matrix[i].shape[0] == target_feat_bin_vec.shape[0])
               # merge Input MAtrix and Output Vec
               list_of_bin_matrix[i] = pds.merge(list_of_bin_matrix[i],\
                       target_feat_bin_vec, left_index = True,\
                       right_index = True)
       #TODO use informative naming
       cnt = 0
       for bin_matrix in list_of_bin_matrix:
            saving_dir = '{}/exp_{}'.format(dump_dir,cnt)
            os.mkdir(saving_dir)
            file_name = saving_dir + '/data.moses'
            bin_matrix.to_csv(file_name, sep=' ', index=False)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
