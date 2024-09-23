import csv
import math
import random
import datetime
from datetime import timedelta

USER_NUM = 5.0
USER_NUM_ADJUST = 1
VISIT_ADJUST = 365 * 3

in_filename = './restaurant/management/commands/review_comment.csv'
out_filename = './restaurant/management/commands/review_comment_2.csv'

with open(out_filename,'w') as fo:
    with open(in_filename) as f:
        csvreader = csv.reader(f)
        i = 0
        
        for row in csvreader:
            random.seed(i)

            if i >= 2:
                id = row[1]
                restaurant_name = row[2]
                if row[3] == "なし":
                    rate = row[3]
                else:
                    rate = math.ceil(float(row[3])-0.5)
                comment = row[4]
                user_id = math.ceil(random.random()*USER_NUM) + USER_NUM_ADJUST
                print(f'🤩🤩{user_id}')
                
                if user_id == 2:
                    user_name = "市村　コタロー"
                elif user_id == 3:
                    user_name = "市村　チャッピー"
                elif user_id == 4:
                    user_name = "市村　タロー"
                elif user_id == 5:
                    user_name = "市村　順一"
                elif user_id == 6:
                    user_name = "市村　とらお"
                else:
                    user_name = "やばお。"
                
                n = math.ceil(random.random()*VISIT_ADJUST) 
                hh = math.floor(random.random()*8) + 12
                mm = math.floor(random.random()*2) * 30
                date = datetime.datetime(2024,9,23,12,0,0) - datetime.timedelta(days=n)
                date = datetime.datetime(date.year, date.month, date.day, hh, mm, 0) 
                datestr = date.strftime("%Y/%m/%d %H:%M:%S")  
                print('⭐️')
                print(id)
                print(user_name)
                print(restaurant_name)
                print(rate)
                print(comment)
                print(datestr)

                out_text = f'{id},{user_name},{restaurant_name},{rate},{comment},{datestr}\n'
                fo.write(out_text)
            i += 1
        f.close()
    fo.close()
        