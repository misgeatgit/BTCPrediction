
'''
Generates training-test data by sliding a window of size K
over the data with each K size being train and K+1th the test.
'''

import pandas as pds
import click
from os import mkdir, path
from shutil import rmtree

@click.command()
@click.option('--train-winsize', type=int, default=6, help='The window size in months.',
        prompt='Window size')
@click.option('--test-size', type=int, default=1, help='The test size in months.',
        prompt='Test size')
@click.option('--data', help='Input data.', prompt='Path to input data')
@click.option('--saving-dir', help='Where to save output.', 
        prompt='Root dir for saving output.')
def main(train_winsize, test_size, data, saving_dir):
    K = train_winsize*30
    Kt = test_size*30
    data = data
    root_saving_dir = path.abspath(saving_dir)
    data_df = pds.read_csv(path.abspath(data))
    # Create all train-test data pairs by sliding window and save.
    for i in range(0,data_df.shape[0] - (K+Kt),30):
        train_df = data_df[i:i+K]
        test_df = data_df[i+K: (i+K+Kt)]
        # save train-test pairs
        tr_tst_dir = 'month_{}_to_{}'.format(int(i/30), int((i+K+Kt)/30))
        abs_path = root_saving_dir + '/' + tr_tst_dir
        if path.exists(abs_path):
            rmtree(abs_path)
        mkdir(abs_path)
        train_df.to_csv(abs_path+'/exp_train.csv', sep=',')
        test_df.to_csv(abs_path+'/exp_test.csv', sep=',')

if __name__ == '__main__':
    main()
