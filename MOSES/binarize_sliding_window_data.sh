
for exp_dir in `ls sliding-window-data`; do
	echo 'EXP_DIR:'$exp_dir
	for config in `ls LA*.json`; do
		echo 'CONFIG_FILE:'$config
		input=sliding-window-data/$exp_dir/ExpData.csv 
		dump_to=sliding-window-data/$exp_dir 
		echo "python transformer.py -i $input -d $dump_to -c $config"
		`python3 transformer.py -i $input -d $dump_to -c $config &`
	done
done
