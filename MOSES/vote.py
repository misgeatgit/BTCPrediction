import pandas as pds
import os
import sys
import subprocess
from anal_exp import eval_output, calc_performance, values_of_col
import click
from shutil import rmtree

'''
A script for applying voting algorithm over the top_N_pre*.csv file
found in this directory.
'''
@click.command()
@click.option('--metrics-dir',  help='Directory where the rank result csv files are stored.',
        prompt='Dir where top_*metrics.csv file are located.')
@click.option('--vote-size', type=int, default=10, help='How many models to vote on.',
        prompt='Rank size.')
@click.option('--threshold', type=float, default=0.7, 
             help='Threshold value for voting.', prompt='Threshold for voting.')
@click.option('--ranked-on', type=click.Choice(['acc', 'prec'], case_sensitive=False),
             help='Vote based on <acc|prec>.', prompt='Vote based on [acc|prec]', default='prec')
def main(metrics_dir, vote_size, threshold, ranked_on):
    metrics_dir = metrics_dir
    N = vote_size
    THRESHOLD = threshold
    rank_type = ranked_on
    top_N_metrics_file = '{}/top_{}_{}_metrics.csv'.format(metrics_dir, N, rank_type)

    top_N_metrics_df = pds.read_csv(top_N_metrics_file)
    # Each group of 10 models belong to one MOSES run. So pick M 10*i for i in moses_runs
    top_N_moses_models= []
    for i in range(N):
        df = top_N_metrics_df['program'][10*i]
        path = top_N_metrics_df['experiment_dir'][10*i]
        print('INFO: Selected:\n{} \n{}'.format(df, path))
        top_N_moses_models.append((df, path))

    tmpdir = '/tmp/models-to-vote-on'
    if os.path.exists(tmpdir):
        rmtree(tmpdir)
    os.mkdir(tmpdir)

    i = 1
    actual_train = []
    actual_test = []
    for model_expdir in top_N_moses_models:
        cfile = tmpdir+'/'+str(i)+'.combo'
        train_file = model_expdir[1] + '/exp_train.csv'
        print('TrainFile: '+train_file)
        test_file = model_expdir[1] + '/exp_test.csv'
        print('TestFile: '+test_file)
        # store once
        if not actual_train and not actual_test:
            try:
                actual_train = pds.read_csv(train_file, sep=' ')['Price'].to_list()
                actual_test = pds.read_csv(test_file, sep=' ')['Price'].to_list()
            except:
                with open('erraneous_exps.txt', 'a+') as log:
                    log.write(train_file)
                    log.write(test_file)

        with open(cfile, 'w') as f:
            f.write(model_expdir[0])

        ofile = tmpdir+'/'+str(i)+'_train.out'
        eval_output(train_file, cfile, ofile)

        ofile2 = tmpdir+'/'+str(i)+'_test.out'
        eval_output(test_file, cfile, ofile2)

        i += 1

    # create a DF as a concatination of the outputs from each model
    dfs_train = []
    for j in range(1,i):
        outf = tmpdir+'/'+str(j)+'_train.out'
        df = pds.read_csv(outf)
        df.rename(columns={"Price": 'Model_'+str(j)})
        dfs_train.append(df)

    print('Actual train size: {}'.format(len(actual_train)))
    df_train = pds.concat(dfs_train, axis=1, ignore_index=True)

    vote_train = df_train.sum(axis=1).to_list()
    df_train['vote_count'] = vote_train
    print('Vote size: {}'.format(len(vote_train)))
    df_train['vote'] = [ 1 if v >=int(THRESHOLD * N) else 0 for  v in vote_train]
    df_train['actual'] = actual_train
    df_train.to_csv('vote_train.csv', sep=',', index=False)
    print('Measures on train:')
    train_perf = calc_performance(df_train['vote'], actual_train)

    dfs_test = []
    for j in range(1,i):
        outf = tmpdir+'/'+str(j)+'_test.out'
        df = pds.read_csv(outf)
        df.rename(columns={"Price": 'Model_'+str(j)})
        dfs_test.append(df)

    print('Actual test size: {}'.format(len(actual_test)))
    df_test = pds.concat(dfs_test, axis=1, ignore_index=True)
    vote_test = df_test.sum(axis=1).to_list()
    df_test['vote_count'] = vote_test
    print('Vote size: {}'.format(len(vote_test)))
    df_test['vote'] = [ 1 if v >= int(THRESHOLD * N) else 0 for  v in vote_test]
    df_test['actual'] = actual_test
    df_test.to_csv('vote_test.csv', sep=',', index=False)
    print('Measures on test:')
    test_perf = calc_performance(df_test['vote'], actual_test)

    result = {'training_accuracy':[round(train_perf['accuracy'],2)], 'training_precision':[round(train_perf['precision'],2)],
               'test_accuracy':[round(test_perf['accuracy'],2)], 'test_precision':[round(test_perf['precision'],2)]}

    pds.DataFrame(result).to_csv(metrics_dir+'/voting_result_based_on_'+rank_type+'.csv', sep=',', index=False)
    rmtree(tmpdir)

if __name__ == '__main__':
    main()




