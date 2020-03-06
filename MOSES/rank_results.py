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
    print('Ranking in {}'.format(LA_exp))
    max_prec_df = None
    max_acc_df = None
    top_5_max_prec = []
    top_5_max_acc = []
    path_info = {'top_prec_file':[], 'top_acc_file':[]}
    for exp_dir in os.listdir(LA_exp_path):
        path = LA_exp_path + '/' + exp_dir
        if not os.path.isdir(path):
            continue
        csvf = path + '/metrics.csv'
        csvf_rel_path =  exp_dir + '/metrics.csv'
        # start ranking by precision here.
        # TODO use heap instead of sorting. 5x faster.
        df_prec = pds.read_csv(csvf).sort_values(by='test_precision', ascending=False)
        if len(top_5_max_prec) < 5:
            top_5_max_prec.append([df_prec, csvf_rel_path])
        else:
            top_5_max_prec.sort(key=lambda s: s[0].sort_values\
                    (by='training_precision',
                     ascending=False)['training_precision'][0], reverse=True)
            least = top_5_max_prec.pop()
            if df_prec['training_precision'][0] > least[0]['training_precision'][0]:
                top_5_max_prec.append([df_prec, csvf_rel_path])
            else:
                top_5_max_prec.append(least)

        df_acc = pds.read_csv(csvf).sort_values(by='test_accuracy', ascending=False)
        if len(top_5_max_acc) < 5:
            top_5_max_acc.append([df_acc, csvf_rel_path])
        else:
            top_5_max_acc.sort(key=lambda s: s[0].sort_values\
                    (by='training_accuracy',
                     ascending=False)['training_accuracy'][0], reverse=True)
            least = top_5_max_acc.pop()
            if df_acc['training_accuracy'][0] > least[0]['training_accuracy'][0]:
                top_5_max_acc.append([df_acc, csvf_rel_path])
            else:
                top_5_max_acc.append(least)

    #TODO merge those top5 DataFrames
    print('Top accurate on training count: {}'.format(len(top_5_max_acc)))
    print('Top precise on training count: {}'.format(len(top_5_max_prec)))

    for i in range(5):
        path_info['top_prec_file'].append(top_5_max_prec[i][1])
        path_info['top_acc_file'].append(top_5_max_acc[i][1])
    pds.DataFrame(path_info).to_csv(LA_exp_path+'/top_5_metrics_file_paths.csv', sep=',', index=False)

    max_prec_df = pds.concat([s[0] for s in top_5_max_prec], ignore_index=True)
    max_acc_df = pds.concat([s[0] for s in top_5_max_acc], ignore_index=True)

    max_prec_df.to_csv(LA_exp_path+'/top_5_prec_metrics.csv',sep=',', index=False)
    max_acc_df.to_csv(LA_exp_path+'/top_5_acc_metrics.csv',sep=',', index=False)










