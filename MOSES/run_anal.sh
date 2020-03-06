
# Create test(~20%) and train(~80%) data from the original
GET_TRAIN_TEST_SIZE_PY=$(cat <<END
# python code starts here
import sys
import pandas as pds

file = sys.argv[1]
#LA_years = int(file.split('LookAhead')[1].split('_Top')[0])
df = pds.read_csv(file)
size = df.shape[0]
train_size = 839 # i.e [2016,2019)
test_size = size - train_size
print('{},{}'.format(train_size,test_size))
#python code Ends here
END
)

exp_dir="experiment"
OUT="Price"

for exp_on_lookahead in `ls $exp_dir`; do
	for exp_on_target in `ls $exp_dir/$exp_on_lookahead`; do
		DIR=$exp_dir/$exp_on_lookahead/$exp_on_target
		for csv in `ls $DIR/*.csv`; do
			echo 'Working with:'$csv
			res="$(python -c "$GET_TRAIN_TEST_SIZE_PY" $csv)"
			IFS=', ' read -r -a array <<< "$res"
			echo "train_test size: ${array[0]},${array[1]}"
			train_file=$DIR/exp_train.csv
			test_file=$DIR/exp_test.csv
			head -n${array[0]} $csv > $train_file
			head -n1 $csv > $test_file #add header
			tail -n${array[1]} $csv >> $test_file #
			# Run MOSES on the training data
			combof=$exp_dir/$exp_on_lookahead/$exp_on_target/combo.txt
			echo 'Running MOSESE on '$csv
			elapsed_time="$(time (moses -H pre -q 0.3 -w 0.8  -u $OUT -W1  -i \
				$train_file \
				-m 30000 \
				--fs-score pre \
				--enable-fs=1 --fs-target-size=12 --fs-algo simple \
				--complexity-ratio=50 \
				> $combof) 2>&1 1>/dev/null )"
			echo "MOSES TOOK $elapsed_time"
			echo 'Done running MOSES now Running anal.py'
			# Run performance measurement tool script.
			python anal_exp.py -t exp_test.csv -T exp_train.csv \
			--trtstdir $DIR --combof $combof
			echo 'Done analyzing.'
		done
	done
done

