for i in {1..7}; do echo "LookAhead $i days"; cat  LargeExperiment/LA_$i/top_5_acc_metrics.csv ; done > top_5_acc_on_train_results.csv
for i in {1..7}; do echo "LookAhead $i days"; cat  LargeExperiment/LA_$i/top_5_prec_metrics.csv ; done > top_5_prec_on_train_results.csv
