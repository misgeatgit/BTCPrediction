rm experiment/* -rf
python3 transformer.py -i ../preprocessed-data/ExpData.csv -d experiment -c experiment-config.json
./run_anal.sh
