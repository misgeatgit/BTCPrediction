
'''
For each month_x_to_y:
    For each LA_i:
        df.add_row('month':month_x_to_y, 'LA':LA_i, type:'prec' + df(voting_on_prec)
        df.add_row('month':month_x_to_y, 'LA':LA_i, type:'acc' + df(voting_on_acc)

'''

import os
from os import path
import pandas as pds
import re

root_dir = path.abspath('./sliding-window-data')
sliding_window_exps = [path.join(root_dir,d) for d in os.listdir(root_dir)
                                if path.isdir(path.join(root_dir, d))]

aggregate_report_df = pds.DataFrame({'month':[],'look_ahead_days':[],
    'vote_based_on':[], 'training_accuracy':[], 'training_precision':[],
    'test_accuracy':[], 'test_precision':[] })
for exp_dir in sliding_window_exps:
    la_exps = [path.join(exp_dir, la_exp) for la_exp in os.listdir(exp_dir)
                                if path.isdir(path.join(exp_dir, la_exp))]
    dir_name = path.basename(path.normpath(exp_dir))
    begin = re.compile('month_([0-9]*)').findall(dir_name)[0]
    end = re.compile('to_([0-9]*)').findall(dir_name)[0]
    for la_exp in la_exps:
        dir_name = path.basename(path.normpath(la_exp))
        la_days = int(dir_name[len(dir_name)-1]) # because dear is named like LA_5 or LA_*INT in general
        #print('Month:{}-{} LookAheadDays:{}'.format(begin, end, la_days))

        # Append precision based voting results
        prec_voting_df = pds.read_csv(la_exp+'/voting_result_based_on_prec.csv')
        aggregate_report_df=aggregate_report_df.append({'month':'{}-{}'.format(begin,end),
            'look_ahead_days':la_days, 'vote_based_on':'precision', 
            'training_accuracy': prec_voting_df['training_accuracy'][0],
            'training_precision': prec_voting_df['training_precision'][0],
            'test_accuracy': prec_voting_df['test_accuracy'][0],
            'test_precision': prec_voting_df['test_precision'][0]},
            ignore_index=True)

        # Append accuracy based voting results
        acc_voting_df = pds.read_csv(la_exp+'/voting_result_based_on_acc.csv')
        print(acc_voting_df['training_accuracy'][0])
        aggregate_report_df=aggregate_report_df.append({'month':'{}-{}'.format(begin,end),
            'look_ahead_days':la_days, 'vote_based_on':'accuracy', 
            'training_accuracy': acc_voting_df['training_accuracy'][0],
            'training_precision': acc_voting_df['training_precision'][0],
            'test_accuracy': acc_voting_df['test_accuracy'][0],
            'test_precision': acc_voting_df['test_precision'][0]},
            ignore_index=True)

aggregate_report_df.sort_values(by=['month', 'look_ahead_days'])
aggregate_report_df.to_csv('voting_results_summary.csv', sep=',', index=False)



