num=0;
i=0;
file=$1
to_dir=$2
column=$3

starting_date='1/1/2016'
for word in $(cat -n $file | grep $starting_date -m1 | cut -d' ' -f3)
do
	echo $word
	i=$((i + 1))
       	if [ $i -eq 1 ]
	then 
		num=$word
	fi
done


tail -n +$num $file | csvcut -c $column > $to_dir/$file
