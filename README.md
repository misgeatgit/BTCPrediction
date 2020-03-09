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

### TODO
Experiment with multiple parameter tuning experiments.
