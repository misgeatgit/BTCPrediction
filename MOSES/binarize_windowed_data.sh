data_dir=$1
for exp_dir in `ls $data_dir`; do
	echo 'EXP_DIR:'$exp_dir
	for config in `ls LA*.json`; do
		echo 'CONFIG_FILE:'$config
		input=$data_dir/$exp_dir/ExpData.csv 
		dump_to=$data_dir/$exp_dir 
		echo "python transformer.py -i $input -d $dump_to -c $config"
		`python3 transformer.py -i $input -d $dump_to -c $config &`
	done
done
