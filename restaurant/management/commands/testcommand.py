from typing import Any
from django.core.management.base import BaseCommand
from ...models import Restaurant, Category
import csv

class Command(BaseCommand):
    help = "テストコマンド"
    
    def handle(self, *args, **options):
        print('test')
        filename = './restaurant/management/commands/dummy_restaurant.csv'
        with open(filename) as f:
            csvreader = csv.reader(f)
            i = 0
            for row in csvreader:
                if i >= 2:
                    id = row[1]
                    name = row[2]
                    postal_code = ''
                    address = row[4]
                    tel_number = row[5]
                    price_max = int(row[9])
                    price_min = int(row[8])
                    category_name = row[3]
                    
                    print('⭐️⭐️⭐️')
                    print(f'id:{id}')
                    print(f'name:{name}')
                    print(f'postal_code:{postal_code}')
                    print(f'address:{address}')
                    print(f'tel_number:{tel_number}')
                    print(f'price_max:{price_max}')
                    print(f'price_min:{price_min}')
                    print(f'category_name:{category_name}')
            
        
                    if Category.objects.filter(name=category_name).exists() == False:
                        tmp_category = Category()
                        tmp_category.name = category_name
                        tmp_category.save()
                    else:
                        tmp_category = Category.objects.get(name=category_name)
                    if Restaurant.objects.filter(name=name,postal_code=postal_code).exists() == False:
                        tmp_restaurant = Restaurant()
                        tmp_restaurant.name = name
                        tmp_restaurant.postal_code = postal_code
                        tmp_restaurant.address = address
                        tmp_restaurant.tel_number = tel_number
                        tmp_restaurant.price_max = price_max
                        tmp_restaurant.price_min = price_min
                        tmp_restaurant.category = tmp_category
                        
                        tmp_restaurant.save()
                    else:
                        Restaurant.objects.filter(name=name,postal_code=postal_code).delete()   
                    
                i += 1      
        