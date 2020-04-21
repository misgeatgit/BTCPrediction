import pandas as pds
import json
import os
import re
import sys

root_dir = sys.argv[1]
N = sys.argv[2]

metrics_file = 'top_'+str(N)+'_metrics_file_paths.csv'

config_template_main = {
        "inputFeatures":[
		{"name": "MarketCap", "bins":[],"binarizer":"QuantileBinarizer"},
		{"name": "BlockSize", "bins":[],"binarizer":"QuantileBinarizer"},
		{"name": "GoldPrice", "bins":[],"binarizer":"QuantileBinarizer"},
		{"name": "GTrends", "bins":[],"binarizer":"QuantileBinarizer"},
		{"name": "HashRate", "bins":[],"binarizer":"QuantileBinarizer"},
		{"name": "MempoolCount", "bins":[],"binarizer": "QuantileBinarizer"},
		{"name": "MempoolSize", "bins":[],"binarizer": "QuantileBinarizer"},
		{"name": "MinningDifficulty", "bins":[],"binarizer": "QuantileBinarizer"},
		{"name": "TransactionPerDay", "bins":[],"binarizer": "QuantileBinarizer"},
		{"name": "TransactionFee", "bins":[],"binarizer": "QuantileBinarizer"},
		{"name": "TransactionVolume_USD", "bins":[], "binarizer": "QuantileBinarizer"}
        ],
	"targetFeature": "Price",
	"targetBinarization":"TopNvsOthers",
	"LA_days": [2]
}

LA_exp_dirs = os.listdir(root_dir)

for LA_exp in LA_exp_dirs:
    if not os.path.isdir(root_dir + '/'+ LA_exp):
        continue
    LA_exp_top_metric_file = root_dir+'/'+LA_exp+'/'+ metrics_file
    df = pds.read_csv(LA_exp_top_metric_file)
    binarization = 1
    import copy
    for index, row in df.iterrows():
        config_template = copy.deepcopy(config_template_main)
        file_str = row['top_acc_file']
        MarketCapBins = re.compile('MarketCapBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][0]['bins'].append(MarketCapBins)
        BlockSizeBins = re.compile('BlockSizeBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][1]['bins'].append(BlockSizeBins)
        GoldPriceBins = re.compile('GoldPriceBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][2]['bins'].append(GoldPriceBins)
        GTrendsBins = re.compile('GTrendsBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][3]['bins'].append(GTrendsBins)
        HashRateBins = re.compile('HashRateBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][4]['bins'].append(HashRateBins)
        MempoolCountBins = re.compile('MempoolCountBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][5]['bins'].append(MempoolCountBins)
        MempoolSizeBins = re.compile('MempoolSizeBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][6]['bins'].append(MempoolSizeBins)
        MinningDifficultyBins = re.compile('MinningDifficultyBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][7]['bins'].append(MinningDifficultyBins)
        TransactionPerDayBins = re.compile('TransactionPerDayBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][8]['bins'].append(TransactionPerDayBins)
        TransactionFeeBins = re.compile('TransactionFeeBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][9]['bins'].append(TransactionFeeBins)
        TransactionVolume_USDBins = re.compile('TransactionVolume_USDBins([0-9]*)').findall(file_str)[0]
        config_template['inputFeatures'][10]['bins'].append(TransactionVolume_USDBins)
        #random test
        print('SIZE {}'.format(len(config_template['inputFeatures'][8]['bins'])))
        assert(len(config_template['inputFeatures'][8]['bins']) == 1)
        jsoned = json.dumps(config_template)
        with open('{}_top_{}_models_binarization_{}_exp_config.json'.format(LA_exp,N,binarization), 'w') as f:
          f.write(jsoned)
        binarization += 1
        print(jsoned)




