from datetime import datetime, timedelta
import sys

file = sys.argv[1]

fixed_csv = ''
date_format = '%Y-%m-%d'

with open(file, 'r') as csvf:
    prev_date = None
    lines = csvf.readlines()
    for i in range(1, len(lines)-1): # start from 1 to escape header.
        date_str = lines[i].split(',')[0]
        date = datetime.strptime(date_str, date_format)
        # Append missing
        #print('% Date:{} PrevDate:{}'.format(date, prev_date))
        while prev_date and (date - prev_date).days > 1:
            prev_date = prev_date + timedelta(days=1)
            fixed_csv += prev_date.strftime(date_format) + ',Nan\n'
        # Continue copying
        prev_date = date
        fixed_csv += lines[i]

print(fixed_csv)
