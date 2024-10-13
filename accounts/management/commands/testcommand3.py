from typing import Any
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from ...models import CustomUser, Job
import csv
import datetime
from datetime import timedelta
import random
import math

class Command(BaseCommand):
    help = "テストコマンド"
    
    def handle(self, *args, **options):
        print('test')
        filename = './accounts/management/commands/dummy_user3.csv'
        with open(filename) as f:
            csvreader = csv.reader(f)
            i = 0
            for row in csvreader:
                random.seed(i)
                
                # id = row[0]
                user_name_kanji = row[1]
                user_name_kana = row[2]
                birthday = str(row[3])
                gender = row[4]
                
                job_name = row[5]
                
                if row[6]==1:
                    is_subscribed = True
                else:
                    is_subscribed = False
                
                email = row[7]
                
                basedate = datetime.datetime(2024,10,12,0,0,0,tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))
                n = math.floor(random.random()*365*5)
                
                created_day = basedate - datetime.timedelta(days=n)
                
                n2 = math.floor(random.random()*n)
                
                updated_day = created_day + datetime.timedelta(days=n2)
                
                print('⭐️⭐️⭐️')
                # print(f'id:{id}')
                print(f'user_name_kanji:{user_name_kanji}')
                print(f'user_name_kana:{user_name_kana}')
                print(f'birthday:{birthday}')
                print(f'gender:{gender}')
                print(f'job_name:{job_name}')
                print(f'email:{email}')
                print(f'created_at:{created_day}')
                print(f'updated_at:{updated_day}')
                
                if Job.objects.filter(name=job_name).count() == 1:
                    tmp_job = Job.objects.get(name=job_name)
                    if CustomUser.objects.filter(user_name_kanji=user_name_kanji, birthday=birthday).exists() == False:
                        tmp_user = CustomUser()
                        tmp_user.username = user_name_kanji
                        tmp_user.user_name_kanji = user_name_kanji
                        tmp_user.user_name_kana = user_name_kana
                        tmp_user.birthday = birthday
                        tmp_user.gender = gender
                        tmp_user.job = tmp_job
                        tmp_user.created_day = created_day
                        tmp_user.updated_day = updated_day
                        
                        tmp_user.save()
                    else:
                        CustomUser.objects.filter(username=user_name_kanji, birthday=birthday).delete()   
                i += 1    