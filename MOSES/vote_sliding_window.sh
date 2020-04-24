
for exp in `ls sliding-window-data`; do
	file="sliding-window-data/"$exp
	if ! [[ -d $file ]]; then
		continue
	fi
	for LAs in `ls $file`; do
		la_dir=$file"/"$LAs
		if ! [[ -d $la_dir ]]; then
			continue
		fi
		#echo "Voting based on acc in "$la_dir
		#python3 vote.py --metrics-dir $la_dir --vote-size 10 --threshold 0.7 --ranked-on acc
		echo "Voting based on prec in "$la_dir
		python3 vote.py --metrics-dir $la_dir --vote-size 10 --threshold 0.7 --ranked-on prec
	done
done
