import pandas as pds
import numpy as np

df = pds.read_csv('voting_result_averaged.csv')

averaged_df = pds.DataFrame({'look_ahead_days':[],'vote_based_on':[],
                            'training_accuracy':[],'training_precision':[],
                            'test_accuracy':[],'test_precision':[]})
averaged_df = averaged_df.T # To match with the output of mean() functions 
for i in range(1, 8):
    acc_df = (df[(df['look_ahead_days'] == i)
                                        & (df['vote_based_on'].str.contains('accuracy'))])\
                                        .drop(['month', 'vote_based_on'], axis=1)\
                                        .mean(axis=0)
    prec_df = (df[(df['look_ahead_days'] == i) \
                                        & (df['vote_based_on'].str.contains('precision'))])\
                                        .drop(['month', 'vote_based_on'], axis=1)\
                                        .mean(axis=0).T
    acc_df['vote_based_on'] = 'accuracy'
    prec_df['vote_based_on'] = 'precision'
    averaged_df = pds.concat([acc_df,prec_df,averaged_df], axis=1)

averaged_df = averaged_df.T.sort_values(by=['look_ahead_days'])
averaged_df = averaged_df[['look_ahead_days','vote_based_on', 'training_accuracy',\
               'training_precision', 'test_accuracy', 'test_precision']]
print(averaged_df)
averaged_df.to_csv('averaged_telescopic_window_based_vote_result.csv',index=False)
