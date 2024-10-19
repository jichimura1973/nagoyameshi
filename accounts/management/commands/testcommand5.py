import calendar
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

from typing import Any
from django.core.management.base import BaseCommand
from accounts.models import CustomUser, MonthlySales

class Command(BaseCommand):
    help = "テストコマンド"
    
    def handle(self, *args, **options):

        PRICE = 300

        date_list = []
        sales_list = []
        # ユーザー登録を5年前からにしたので売り上げ計算も5年前からとする。
        st_date = datetime.datetime(2024,10,12,23,59,59,tzinfo=datetime.timezone(datetime.timedelta(seconds=32400))) - datetime.timedelta(days=365*5)
        last_day = calendar.monthrange(st_date.year,st_date.month)[1]
        tmp_date = datetime.datetime(st_date.year, st_date.month, last_day,23,59,59,tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))
        # 今月までの売り上げを計算
        today = datetime.datetime.today()
        today = datetime.datetime(today.year, today.month, today.day, 23, 59, 59, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))
        
        while tmp_date < today:
            # 月末の日付を作る
            last_day = calendar.monthrange(tmp_date.year, tmp_date.month)[1]
            tmp_date = datetime.datetime(tmp_date.year, tmp_date.month, last_day, 23, 59, 59, tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))
            # 更新日の時点で有料会員になったと仮定して計算
            user_num = CustomUser.objects.filter(is_subscribed=True, updated_day__lte=tmp_date ).count()
            
            if MonthlySales.objects.filter(date=tmp_date).exists() == False:
                tmp_monthly_sales = MonthlySales()
                tmp_monthly_sales.date = tmp_date
                tmp_monthly_sales.sales = user_num * PRICE
                tmp_monthly_sales.save()
            
                print(f'{tmp_date.strftime("%Y-%m-%d")}, {user_num}')
            else:
                MonthlySales.objects.filter(date=tmp_date).delete()  
            
            tmp_date = tmp_date + relativedelta(months=1)
    
    