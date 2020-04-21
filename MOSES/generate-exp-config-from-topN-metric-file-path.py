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
	"LA_days": []
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
        features=['MarketCapBins', 'BlockSizeBins', 'GoldPriceBins', \
                'GTrendsBins', 'HashRateBins', 'MempoolCountBins',\
                'MempoolSizeBins', 'MinningDifficultyBins',\
                'TransactionPerDayBins','TransactionFeeBins',\
                'TransactionVolume_USDBins']
        LA = re.compile('LA_([0-9]*)').findall(LA_exp)[0]
        config_template['LA_days'].append(int(LA))
        for i, feat in enumerate(features, start=0):
            bins = re.compile('{}([0-9]*)'.format(feat)).findall(file_str)[0]
            config_template['inputFeatures'][i]['bins'].append(int(bins))
        #random test
        print('SIZE {}'.format(len(config_template['inputFeatures'][8]['bins'])))
        assert(len(config_template['inputFeatures'][8]['bins']) == 1)
        jsoned = json.dumps(config_template)
        with open('{}_top_{}_models_binarization_{}_exp_config.json'.format(LA_exp,N,binarization), 'w') as f:
          f.write(jsoned)
        binarization += 1
        print(jsoned)




