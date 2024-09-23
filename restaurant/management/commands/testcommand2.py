from typing import Any
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from ...models import Review, Restaurant
import csv
import datetime
from datetime import timedelta
import random
import math

class Command(BaseCommand):
    help = "テストコマンド"
    
    def handle(self, *args, **options):
        print('test')
        filename = './restaurant/management/commands/review_comment_2.csv'
        with open(filename) as f:
            csvreader = csv.reader(f)
            i = 0
            for row in csvreader:
                random.seed(i)
                
                id = row[0]
                user_name = row[1]
                restaurant_name = row[2]
                rate = row[3]
                if rate == 'なし':
                    continue
                rate = int(rate)
                comment = row[4]
                datestr = row[5]
                date_elem = datestr.split(' ')
                year = int(date_elem[0][0:4])
                month = int(date_elem[0][5:7])
                day = int(date_elem[0][8:10])
                hour = int(date_elem[1][0:2])
                min = int(date_elem[1][3:5])
                sec = int(date_elem[1][6:8])
                visited_at = datetime.datetime(year, month, day, hour, min, sec)
                
                # 来店から30日以内のランダムな日数を登録日とする
                n = math.floor(random.random()*30)
                created_at = visited_at + datetime.timedelta(days=n)
                print('⭐️⭐️⭐️')
                print(f'id:{id}')
                print(f'user_name:{user_name}')
                print(f'restaurant_name:{restaurant_name}')
                print(f'rate:{rate}')
                print(f'comment:{comment}')
                print(f'date:{year}/{month}/{day} {hour}:{min}:{sec}')
                 
                if CustomUser.objects.filter(user_name_kanji=user_name).count() == 1  and Restaurant.objects.filter(name=restaurant_name).count() == 1:
                    tmp_user = CustomUser.objects.get(user_name_kanji=user_name)
                    tmp_restaurant = Restaurant.objects.get(name=restaurant_name)
                    if Review.objects.filter(user=tmp_user, restaurant=tmp_restaurant, visited_at=visited_at).exists() == False:
                        tmp_review = Review()
                        tmp_review.restaurant = tmp_restaurant
                        tmp_review.user = tmp_user
                        tmp_review.rate = rate
                        tmp_review.comment = comment
                        tmp_review.visited_at = visited_at
                        tmp_review.created_at = created_at
                        
                        tmp_review.save()
                    else:
                        Review.objects.filter(user=tmp_user, restaurant=tmp_restaurant, visited_at=visited_at).delete()   
                i += 1    