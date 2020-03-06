import os
import sys
import pandas as pds

'''
This script extracts the top performing quantization/binarizations
interms of test set accuracy and test set precission for each Look Ahead
experiment. saves these best experiment results directly under LA_* directory
for each Look Ahead experiment.
'''
root_dir = os.path.abspath(sys.argv[1])
LA_exp_dirs = os.listdir(root_dir)

for LA_exp in LA_exp_dirs:
    LA_exp_path = root_dir + '/'+ LA_exp 
    if not os.path.isdir(LA_exp_path):
        continue
    max_prec = float('-inf')
    max_prec_file = None
    max_prec_df = None
    max_acc = float('-inf')
    max_acc_file = None
    max_acc_df = None
    path_info = {'top_prec_file':[], 'top_acc_file':[]}
    for exp_dir in os.listdir(LA_exp_path):
        path = LA_exp_path + '/' + exp_dir
        if not os.path.isdir(path):
            continue
        csvf = path + '/metrics.csv'
        csvf_rel_path =  exp_dir + '/metrics.csv'
        # start ranking by precision here.
        df = pds.read_csv(csvf).sort_values(by='test_precision', ascending=False)
        if df['test_precision'][0] > max_prec:
            max_prec = df['test_precision'][0]
            max_prec_file = csvf
            max_prec_df = df
            if path_info['top_prec_file']:
                path_info['top_prec_file'][0] = csvf_rel_path
            else:
                path_info['top_prec_file'].append(csvf_rel_path)
        df = pds.read_csv(csvf).sort_values(by='test_accuracy', ascending=False)
        if df['test_accuracy'][0] > max_acc:
            max_acc = df['test_accuracy'][0]
            max_acc_file = csvf
            max_acc_df = df
            if path_info['top_acc_file']:
                path_info['top_acc_file'][0] = csvf_rel_path
            else:
                path_info['top_acc_file'].append(csvf_rel_path)

    max_prec_df.to_csv(LA_exp_path+'/top_prec_metrics.csv',sep=',', index=False)
    max_acc_df.to_csv(LA_exp_path+'/top_acc_metrics.csv',sep=',', index=False)
    pds.DataFrame(path_info).to_csv(LA_exp_path+'/top_metrics_file_paths.csv', sep=',', index=False)










