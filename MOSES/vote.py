import pandas as pds
import os
import sys
from anal_exp import eval_output, calc_performance, values_of_col
'''
A script for applying voting algorithm over the top_5_pre*.csv file
found in this directory.
'''

metrics_dir = sys.argv[1]

if not metrics_dir:
    print('You need to provide the LA* directory path')
    exit()

top_5_metrics_df = pds.read_csv(metrics_dir +'/top_5_prec_metrics.csv')

# Each group of 10 models belong to one MOSES run. So pick M 10*i for i in moses_runs

top_5_moses_models= []
for i in range(5):
    df = top_5_metrics_df['program'][10*i]
    path = top_5_metrics_df['experiment_dir'][10*i]
    top_5_moses_models.append((df, path))

tmpdir = 'models-to-vote-on'
os.mkdir(tmpdir)

i = 1
actual_train = []
actual_test = []
for model_expdir in top_5_moses_models:
    cfile = tmpdir+'/'+str(i)+'.combo'
    train_file = model_expdir[1] + '/exp_train.csv'
    test_file = model_expdir[1] + '/exp_test.csv'
    # store once
    if not actual_train and not actual_test:
        actual_train = values_of_col(train_file, 'Price', ' ')
        actual_test = values_of_col(test_file, 'Price', ' ')

    with open(cfile, 'w') as f:
        f.write(model_expdir[0])

        ofile = tmpdir+'/'+stri(i)+'_train.out'
        print('evaluating output with COMBO: {},\n TRAIN: {}\n OUT:{}'.\
          format(cfile, train_file, ofile))
        eval_output(train_file, cfile, ofile)

        ofile2 = tmpdir+'/'+stri(i)+'_test.out'
        print('evaluating output with COMBO: {},\n TRAIN: {}\n OUT:{}'.\
          format(cfile, test_file, ofile2))
        eval_output(train_file, cfile, ofile2)

        i += 1


# create a DF as a concatination of the outputs from each model
dfs_train = []
for j in range(i):
    df = pds.read_csv(tmpdir+'/'+str(i)+'_train.out')
    df.rename(columns={"Price": 'Model_'+str(j)})
    dfs.append(df)

df_train = pds.concat(dfs_train, ignore_index=True)
vote= df_train.sum(axis=1).to_list()

df_train['vote'] = [ 1 if v >=4 else 0 for  v in vote]

df_train['actual'] = actual

df_train.to_csv('vote.csv', sep=',', index=False)








