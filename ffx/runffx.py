import pandas as pds
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import ffx
from textwrap import wrap
from datetime import datetime

def plot_prediction_vs_actual(yhat, y, starting_year, file_name, title=''):
        years = [datetime(year=starting_year + i,month=1,day=1) for i in range(0,yhat.shape[0])]
        assert(len(years) == yhat.shape[0] == y.shape[0])
        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(years, yhat, label='Predicted')
        ax.plot(years, y, label='Actual')
        # round to nearest years.
        ax.format_xdata = mdates.DateFormatter('%Y')
        ax.set_ylabel('BTC Daily Price (USD)')
        ax.set_xlabel('Days')
        ax.legend()
        plt.rcParams['axes.titlepad'] = 20
        plt.rcParams["axes.titlesize"] = 8
        plt.title(title)
        #plt.grid(which='both')
        #plt.title("\n".join(wrap(title,80)))
        #plt.text(0.5, 0.5, "\n".join(wrap(title,80)), fontsize=9)
        fig.savefig(file_name, dpi=fig.dpi)
        plt.close()
# Silence SKlearn warning on python3
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

ffx_dir = 'data/'
test_X = pds.read_csv('{}/test/test_input.csv'.format(ffx_dir)).values
test_Y = pds.read_csv('{}/test/test_output.csv'.format(ffx_dir)).values
train_X = pds.read_csv('{}/train/training_input.csv'.format(ffx_dir)).values
train_Y = pds.read_csv('{}/train/training_output.csv'.format(ffx_dir)).values

data_X = np.append(train_X, test_X, axis=0)
data_Y = np.append(train_Y, test_Y, axis=0)

predictors = ['MarketCap','BlockSize','GoldPrice','GTrends','HashRate',
              'MempoolCount', 'MempoolSize','MinningDifficulty',
              'TransactionPerDay','TransactionFee','TransactionVolume_USD']

# Predict K years ahead
#Ks = [0,1,2,3,4,5,6,7,8,10,9]
Ks = range(1,8)#[15,16,17,18,19,20]
results = {'years_predicted': [], 'test_data_size': [], 'SquaredSumError': [],\
        'MeanAbsError':[], 'RMSError':[], 'Model': []}
data_starting_year = 0
for K in Ks:
    print('\nModels Predicting {} years ahead:'.format(K))
    # Remove the last K year data from as the Y value is unknown
    cur_data_X = data_X[:len(data_X) - K]
    # Shift Y values K steps up and remove the last K points.
    cur_data_Y = np.roll(data_Y, -K, axis=0)[:len(data_Y) - K]
    train_size = int(cur_data_X.shape[0]*0.8) #80%
    test_starting_year = data_starting_year + (train_size-1) + 1
    print('Data size: {}'.format(cur_data_X.shape[0]))
    print('Test data starting year: {}'.format(test_starting_year))
    # Prepare FFX inputs
    cur_train_X = cur_data_X[:train_size]
    cur_train_Y = cur_data_Y[:train_size]
    cur_test_X = cur_data_X[train_size: ]
    cur_test_Y = cur_data_Y[train_size: ]

    assert(cur_test_X.shape[0] == cur_test_Y.shape[0])
    assert(cur_train_X.shape[0] == cur_train_Y.shape[0])

    print('cur_train_X dim: {}'.format(cur_train_X.shape))
    print('cur_test_X dim: {}'.format(cur_test_X.shape))

    #models = xgp.XGPRegressor()
    #models.fit(train_X, train_Y)
    models = ffx.run(cur_train_X, cur_train_Y, cur_test_X, \
                 cur_test_Y, predictors)
    best_performing_model={'sq_err':float('inf'), 'model':None}
    for model in models:
        #yhat = model.predict(test_X)
        #y = np.reshape(test_Y, test_Y.shape[0])
        yhat = model.simulate(cur_test_X)
        y = np.reshape(cur_test_Y, cur_test_Y.shape[0])
        print(' * {}'.format(model))
        sq_err = np.sum(np.square(y - yhat))
        print('   squared error= {}'.format(sq_err))
        if sq_err < best_performing_model['sq_err']:
            best_performing_model['model'] = model
            best_performing_model['sq_err'] = sq_err
            best_performing_model['y'] = y
            best_performing_model['yhat'] = yhat
            best_performing_model['rms_err'] = np.sqrt(sq_err/len(yhat))
            best_performing_model['mabs_err'] = np.sum(np.absolute(y - yhat))/len(yhat)

    print('y= {}'.format(best_performing_model['y']))
    print('yhat= {}'.format(best_performing_model['yhat']))
    model = best_performing_model['model']
    results['SquaredSumError'].append(best_performing_model['sq_err'])
    results['RMSError'].append(best_performing_model['rms_err'])
    results['MeanAbsError'].append(best_performing_model['mabs_err'])
    results['test_data_size'].append(len(cur_test_Y))
    results['years_predicted'].append(K)
    results['Model'].append('{}'.format(model))

    #yhat = model.predict(test_X)
    #y = np.reshape(test_Y, test_Y.shape[0])
    yhat = model.simulate(cur_test_X)
    y = np.reshape(cur_test_Y, cur_test_Y.shape[0])
    plot_prediction_vs_actual(yhat, y, test_starting_year, 'predict_{}_days.png'.format(K),\
            'Look ahead days={}'.format(K))
    '''
    FFX = ffx.FFXRegressor()
    FFX.fit(cur_train_X, cur_train_Y)
    #print("Prediction:", FFX.predict(cur_test_X))
    print(" Score(of best performing model):", FFX.score(cur_test_X, cur_test_Y))
    '''
pds.DataFrame(results).to_csv('ffx_results.csv',sep=',', index=False)
print('Done FFX experiment. Check ffx_results.csv for summary and the plots.')
