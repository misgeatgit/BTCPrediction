from binarizer import BinarizationFactory
from target_binarizer import binarize_target 
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
        binarizations = []
        for bins in bins_to_try:
            logging.info('Feat: {} Bins: {}'.format(feat_name, bins))
            bin_matrix = binarizer.binarize(data[feat_name].to_numpy(), bins)
            # build dataFrame
            df_columns = {}
            for i in range(bins):
                df_columns[feat_name+'_bin'+str(i)] = np.array(bin_matrix)[:,i]
            binarizations.append(('{}Bins{}'.format(feat_name,bins), pds.DataFrame(df_columns))) #name_binarization tuple
        logging.info('Result:\n{}'.format(binarizations))
        feat_binarized_DFs[feat_name] = binarizations

    return feat_binarized_DFs

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
    input: A map of feature name and list of tuple of names and binary panda DataFram objects
    output: A list of all combination of binary matrix from concatenating each feat binarization
    '''
    combinations = _cartesian(list(feat_bin_matrix.values()))
    dfs = []
    for combination in combinations:
        df_merged = combination[0][1] #df
        name = combination[0][0] #name(featNameBins)
        for name_df in combination[1:]:
            assert(df_merged.shape[0] == name_df[1].shape[0])
            name += name_df[0]
            df_merged = pds.merge(df_merged, name_df[1], left_index=True, right_index=True)

        dfs.append((name, df_merged))

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

       logging.basicConfig(filename='transformer.log', level=logging.INFO)

       list_of_feat_bin_matrix = binarize(data, config)
       list_of_bin_matrix = combine_all(list_of_feat_bin_matrix)

       for matrix in list_of_bin_matrix:
           logging.info('BinarizatinName: {}:\n{}\n'.format(matrix[0],matrix[1]))

       target = config['targetFeature']
       predictions = binarize_target(data[target].to_numpy(), config['LA_days'])
       # Resize Input to Length(Input) - K for K look-ahead years prediction and merge.
       moses_data = {}
       for la_days in predictions.keys():
           for i in range(len(list_of_bin_matrix)):
               logging.info('LA_years: {}\n'.format(la_days))
               logging.info('inputFeature bin_matrix initial size: {}'.format(list_of_bin_matrix[i][1].shape))
               df = list_of_bin_matrix[i][1].drop(list_of_bin_matrix[i][1].tail(la_days).index,inplace=False)
               target_feat_bin_vec = pds.DataFrame({target:predictions[la_days]})
               logging.info('inputFeature bin_matrix size after resize: {}'.format(df.shape))
               logging.info('targetFeature bin_matrix initial size: {} \n'.format(target_feat_bin_vec.shape))
               assert(df.shape[0] == target_feat_bin_vec.shape[0])
               # merge Input MAtrix and Output Vec
               moses_df = pds.merge(df,\
                       target_feat_bin_vec, left_index = True,\
                       right_index = True)
               if la_days in moses_data.keys():
                   moses_data[la_days].append((list_of_bin_matrix[i][0], moses_df))
               else:
                   moses_data[la_days] = [(list_of_bin_matrix[i][0], moses_df)]

       #TODO use informative naming
       for la_days in moses_data.keys():
           cnt = 0
           saving_dir = '{}/LA_{}'.format(dump_dir,la_days)
           if not os.path.exists(saving_dir):
               os.mkdir(saving_dir)
           for name_moses_df in moses_data[la_days]:
                saving_child_dir = '{}/{}'.format(saving_dir, name_moses_df[0])
                cnt += 1
                os.mkdir(saving_child_dir)
                file_name = saving_child_dir + '/data.csv'
                name_moses_df[1].to_csv(file_name, sep=' ', index=False)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
