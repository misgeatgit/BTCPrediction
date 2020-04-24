
for exp in `ls sliding-window-data`; do
	file="sliding-window-data"/$exp 
	if ! [[ -d $file ]]; then
		continue
	fi
	python3 rank_results.py --root-dir $file --rank-size 10
done

