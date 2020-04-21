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
N = int(sys.argv[2])
for LA_exp in LA_exp_dirs:
    LA_exp_path = root_dir + '/'+ LA_exp 
    if not os.path.isdir(LA_exp_path):
        continue
    print('Ranking in {}'.format(LA_exp))
    max_prec_df = None
    max_acc_df = None
    top_N_max_prec = []
    top_N_max_acc = []
    path_info = {'top_prec_file':[], 'top_acc_file':[]}
    for exp_dir in os.listdir(LA_exp_path):
        path = LA_exp_path + '/' + exp_dir
        if not os.path.isdir(path):
            continue
        csvf = path + '/metrics.csv'
        csvf_rel_path =  exp_dir + '/metrics.csv'
        # start ranking by precision here.
        # TODO use heap instead of sorting. 5x faster.
        #print('Working with {}'.format(csvf))
        df_prec = pds.read_csv(csvf).sort_values(by='test_precision', ascending=False)
        for i in range(df_prec.shape[0]):
            df_prec['experiment_dir'] = path
        if len(top_N_max_prec) < N:
            top_N_max_prec.append([df_prec, csvf_rel_path])
        else:
            for df_path in top_N_max_prec:
                df_path[0].sort_values(by='training_precision', inplace=True,\
                                 ascending=False)
            top_N_max_prec.sort(key=lambda s: s[0]['training_precision'][0],\
                                reverse=True)
            least = top_N_max_prec.pop()
            if df_prec['training_precision'][0] > least[0]['training_precision'][0]:
                top_N_max_prec.append([df_prec, csvf_rel_path])
            else:
                top_N_max_prec.append(least)

        df_acc = pds.read_csv(csvf).sort_values(by='test_accuracy', ascending=False)
        for i in range(df_acc.shape[0]):
            df_acc['experiment_dir'] = path
        if len(top_N_max_acc) < N:
            top_N_max_acc.append([df_acc, csvf_rel_path])
        else:
            for df_path in top_N_max_acc:
                df_path[0].sort_values(by='training_accuracy', inplace=True,\
                                       ascending=False)
            top_N_max_acc.sort(key=lambda s: s[0]['training_accuracy'][0],\
                               reverse=True)
            least = top_N_max_acc.pop()
            if df_acc['training_accuracy'][0] > least[0]['training_accuracy'][0]:
                top_N_max_acc.append([df_acc, csvf_rel_path])
            else:
                top_N_max_acc.append(least)

    #TODO merge those topN DataFrames
    print('Top accurate on training count: {}'.format(len(top_N_max_acc)))
    print('Top precise on training count: {}'.format(len(top_N_max_prec)))

    for i in range(N):
        path_info['top_prec_file'].append(top_N_max_prec[i][1])
        path_info['top_acc_file'].append(top_N_max_acc[i][1])
    pds.DataFrame(path_info).to_csv(LA_exp_path+'/top_'+str(N)+'_metrics_file_paths.csv', sep=',', index=False)

    max_prec_df = pds.concat([s[0] for s in top_N_max_prec], ignore_index=True)
    max_acc_df = pds.concat([s[0] for s in top_N_max_acc], ignore_index=True)

    max_prec_df.to_csv(LA_exp_path+'/top_'+str(N)+'_prec_metrics.csv',sep=',', index=False)
    max_acc_df.to_csv(LA_exp_path+'/top_'+str(N)+'_acc_metrics.csv',sep=',', index=False)










