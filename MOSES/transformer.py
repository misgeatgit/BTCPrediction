from binarizer import BinarizationFactory
import argparse
import numpy as np
import pandas as pds

def binarize(data, config):
    '''
      Binarizes given DataFrame according to the config params.
      Returns a set of binarized DataFrames for each inputFeatures.
    '''
    input_feat_config = config['inputFeatures']
    feat_binarized_DFs = {}
    for  dct in input_feat_config:
        feat_name = dct['name']
        bins_to_try = dct['bins']
        binarizer = BinarizationFactory(dct['binarizer']).get_binarizer()

        binarizations = []
        for bins in bin_to_try:
            bin_matrix = binarizer.binarize(data[feat_name].to_numpy(), bins)
            # build dataFrame
            df_columns = {}
            for i in range(bins):
                df_columns[feat_name+'_bin'+str(i)] = np.array(bin_matrix)[:,i]
            binarizations.append(pds.DataFrame(df_columns))

        feat_binarized_DFs[feat_name] = binarizations

    return feat_binarizations

def binarize_target(target_vec, config):
    la_years = config['LA_years']
    bin_vecs = []
    for la_year in la_years:
        bin_vec = []
        for i in range(len(target_vec) - la_year):
            if target_vec[i] < target_vec[i+la_year]:
                bin_vec.append(1) # UP
            else:
                bin_vec.append(0) # DOWN
        bin_vecs.append({la_year: bin_vec})

    return bin_vecs

def _cartesian(elements_set):
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
       dump_dir = args.dump_dir[0]
       data = pds.read_csv(args.input[0])
       # Load config file
       config = None
       with open(args.config[0], 'r') as jsonf:
           config = json.load(jsonf)

       list_of_feat_bin_matrix = binarize(data, config)
       list_of_bin_matrix = combine_all(list_of_feat_bin_matrix)
       predictions = binarize_target(data[config['target']].to_numpy(), config[predict])

       for layears in predictions.keys():
           look_ahead = layears
           vec = prediction[layears]
           for i in range(list_of_bin_matrix):
               bin_vec = list_of_bin_matrix[i]
               list_of_bin_matrix[i] = bin_vec.drop(bin_vec.tail(look_ahead).index,inplace=True)
               target_feat_bin_vec = pds.DataFrame({config['target']:vec})
               assert(list_of_bin_matrix[i].shape[0] == target_feat_bin_vec[0])
               list_of_bin_matrix[i] = pds.merge(list_of_bin_matrix[i],\
                       target_feat_bin_matrix, left_index = True,\
                       right_index = True)
       # dump TODO
       # for bin_matrix in list_of_bin_matrix:
            # dir = MAKE_UP_SOME_DIR
            # bin_matrix.to_csv(dum_dir+'/'+dir, sep=' ', index=False)
    else:
        parser.print_help()


# configuration
# {FeatureName: [{bins:Bins, binarizer: Binarizer, names:[..]}], target:FeatureName, predict:[1...]}
if __name__ == '__main__':
    main()
