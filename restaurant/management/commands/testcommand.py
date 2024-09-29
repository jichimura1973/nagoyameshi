from typing import Any
from django.core.management.base import BaseCommand
from django.core.files import File
from PIL import Image
from ...models import Restaurant, Category
import csv

class Command(BaseCommand):
    help = "テストコマンド"
    
    def handle(self, *args, **options):
        print('test')
        filename = './restaurant/management/commands/dummy_restaurant2.csv'
        # imagefile = './restaurant/management/commands/images/restaurant_001.jpg'
        imagefile = 'restaurant_001.jpg'
                     
        with open(filename) as f:
            csvreader = csv.reader(f)
            i = 0
            for row in csvreader:
                if i >= 2:
                    id = row[1]
                    name = row[2]
                    postal_code = row[12].replace("-","")
                    address = row[4]
                    tel_number = row[5]
                    price_max = int(row[9])
                    price_min = int(row[8])
                    category_name = row[3]
                    close_day_of_week = row[7]
                    seats_number = row[10]
                    rate = row[11]
                    description = row[13]
                    print('⭐️⭐️⭐️')
                    print(f'id:{id}')
                    print(f'name:{name}')
                    print(f'description:{description}')
                    print(f'postal_code:{postal_code}')
                    print(f'address:{address}')
                    print(f'tel_number:{tel_number}')
                    print(f'price_max:{price_max}')
                    print(f'price_min:{price_min}')
                    print(f'category_name:{category_name}')
                    print(f'seats_number:{seats_number}')
                    print(f'close_day_of_werk:{close_day_of_week}')
                    print(f'rate:{rate}')

        
                    if Category.objects.filter(name=category_name).exists() == False:
                        tmp_category = Category()
                        tmp_category.name = category_name
                        tmp_category.save()
                    else:
                        tmp_category = Category.objects.get(name=category_name)
                    if Restaurant.objects.filter(name=name,postal_code=postal_code).exists() == False:
                        tmp_restaurant = Restaurant()
                        tmp_restaurant.name = name
                        tmp_restaurant.description = description
                        tmp_restaurant.postal_code = postal_code
                        tmp_restaurant.address = address
                        tmp_restaurant.tel_number = tel_number
                        tmp_restaurant.price_max = price_max
                        tmp_restaurant.price_min = price_min
                        tmp_restaurant.category = tmp_category
                        tmp_restaurant.close_day_of_week = close_day_of_week
                        tmp_restaurant.seats_number = seats_number
                        tmp_restaurant.rate = rate
                        
                        # im = Image.open(imagefile)
                        # # with open(imagefile, 'r') as fi:
                        # #     print('open')
                        #     # tmp_restaurant.photo = File(fi)
                        # tmp_restaurant.photo = im
                        # print(im.format, im.size)
                        s = format(i%20+1,'03')
                        tmp_restaurant.photo.name = f'restaurant_{s}.jpg'
                        tmp_restaurant.save()
                        # tmp_restaurant.photo.save(name='file01',content=im,save=True) 
                    else:
                        Restaurant.objects.filter(name=name,postal_code=postal_code).delete()   
                    
                i += 1      
        