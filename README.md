# BTCPrediction
BTCPrediction contains scripts and data for BTC price prediction. Currently, we are experimenting with [FFX](https://github.com/natekupp/ffx)
and [MOSES](https://github.com/opencog/moses).

## FFX
The FFX director contains a python script called ruffx.py and FFX style formatted training and test data. The 
script runs FFX and saves best models in a csv file called ffx_results.csv and the plots for each predictions vs actual
in png format.

## MOSES
The MOSES directory contains MOSES style training data generation script and analysis script which runs MOSES with a certain parameter
setup and evaluation and scoring script for evaluating the MOSES generated Model. The MOSES data generator script is called transformer.py
which requires a certain arguments including a config file. The default one is called experiment-config.json. It is not adviced to run this script
multiple times with the configuration depicted in experiment-config.json as it may require lots of CPU time to generate all sorts of combination
of bins. Instead you may run it only once and manually invoke run_anal.sh. 


After manually tuning important parameter, I fixated on using the following settings for the entire experiment.
```sh
moses -H pre -q 0.3 -w 0.8  -u $OUT -W1  -i $train_file 
				-m 30000 \
				--fs-score pre \
				--enable-fs=1 --fs-target-size=12 --fs-algo simple \
				--complexity-ratio=50 \
```


- For the binarization I used the following configuration to generate 243 different binarizations.
```js
{
        "inputFeatures":[
		{"name": "MarketCap", "bins":[2,3,5],"binarizer":"QuantileBinarizer"},
		{"name": "BlockSize", "bins":[10],"binarizer":"QuantileBinarizer"},
		{"name": "GoldPrice", "bins":[2,5,7],"binarizer":"QuantileBinarizer"},
		{"name": "GTrends", "bins":[2,5,7],"binarizer":"QuantileBinarizer"},
		{"name": "HashRate", "bins":[10],"binarizer":"QuantileBinarizer"},
		{"name": "MempoolCount", "bins":[10],"binarizer": "QuantileBinarizer"},
		{"name": "MempoolSize", "bins":[10],"binarizer": "QuantileBinarizer"},
		{"name": "MinningDifficulty", "bins":[10],"binarizer": "QuantileBinarizer"},
		{"name": "TransactionPerDay", "bins":[10],"binarizer": "QuantileBinarizer"},
		{"name": "TransactionFee", "bins":[2,5,7],"binarizer": "QuantileBinarizer"},
		{"name": "TransactionVolume_USD", "bins":[2,5,7], "binarizer": "QuantileBinarizer"}
        ],
	"targetFeature": "Price",
	"targetBinarization":"TopNvsOthers",
	"LA_days": [2]
}
```
the bins key refer to the list of bins experimented with.

- Using the MOSES data and parameter settings from the above two steps, I used ```run_anal.sh``` to run moses. The training and test size is fixed to 839,91 respectively. This data corresponds to 2016-2018 inclusively. The remaining data which accounts for 2019-2020 is kept as a virgin data for evaluating performance of the best models later.

- Following the above MOSES runs, the top N MOSES models based on training precision and accuracy are picked and stored in files which are found directly under ```LargeExperiment/LA_*/``` directories (LA referes to the number of look ahead days). ```rank_results.py``` does exactly this job; taking root directory of the experiment and N value as arguments and saves ```top_N_prec_metrics.csv``` and ```top_N_acc_metrics.csv``` files under each ```LargeExperiment/LA_*/``` directories.  

- ```vote.py``` does simple voting by ensembling the top N models. It takes the root directory where ```top_N_acc_metrics.csv``` and ```top_N_prec_metrics.csv``` are found, N, and the thhreshold value for voting ((0,1]) as arguments to perform voting. It also valuates performance and accuracy on training and test inputs with the ensemble model and saves the result in ```voting_results.csv``` file.   





