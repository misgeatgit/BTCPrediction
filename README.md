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
 
