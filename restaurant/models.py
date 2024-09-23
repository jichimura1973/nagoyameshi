import datetime

from accounts.models import CustomUser
from django.core.validators import MinLengthValidator, RegexValidator, MaxValueValidator, MinValueValidator

from django.db import models

class Category(models.Model):
    
    name = models.CharField(verbose_name="カテゴリー名", max_length=200)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Category"
        
        # constraints = [
        #     models.UniqueConstraint(fields=['name'], name='unique_category_name')
        # ]
    
    def __str__(self):
         return self.name   


class Restaurant(models.Model):
    
    name = models.CharField("店名",max_length=200, blank=False, null=False)
    description = models.CharField(verbose_name='説明', max_length=200, blank=True, null=True)
    postal_code_regex = RegexValidator(regex=r'^[0-9]+$', message = ("Postal Code must be entered in the format: '1234567'. Up to 7 digits allowed."))
    postal_code = models.CharField(validators=[postal_code_regex], max_length=7, verbose_name='郵便番号', blank=False, null=False) 
    address = models.CharField("住所", max_length=200)
    tel_number_regex = RegexValidator(regex=r'^[0-9]+$', message = ("Tel Number must be entered in the format: '09012345678'. Up to 15 digits allowed."))
    tel_number = models.CharField(validators=[tel_number_regex], max_length=15, verbose_name='電話番号', blank=False, null=False)
    e_mail = models.EmailField("E-Mail", blank=True, null=True)
    url = models.URLField("店舗URL", blank=True, null=True)
    price_max = models.PositiveIntegerField("予算上限", blank=True, null=True)
    price_min = models.PositiveIntegerField("予算下限", blank=True, null=True)
    rate = models.FloatField(verbose_name="レート", default=0.0)
    min_varidator = MinValueValidator(0)
    max_varidator = MaxValueValidator(1000)
    seats_number = models.IntegerField("席数", blank=True, null=True, validators=[min_varidator, max_varidator])
    close_day_of_week = models.CharField("定休日", max_length=50, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField("登録日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now_add=True)    
    deleted_at = models.DateTimeField("削除日", auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Restaurant"
        constraints = [
            models.UniqueConstraint(fields=['name', 'postal_code'], name='unique_restaurant')
        ]
        
    def __str__(self):
        return self.name

class RestaurantCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, blank=True, null=True)
    
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['restaurant_id', 'category_id'], name='unique_category')
    #     ]
        
    def __str__(self):
        return self.restaurant.name
    
class Reservation(models.Model):
    STATUS_TYPES = (
        ("予約受付","予約受付"),
        ("予約完了","予約完了"),
        ("予約取消","予約取消"),
    )
    restaurant = models.ForeignKey(Restaurant, verbose_name="店名", on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, verbose_name="会員氏名", on_delete=models.PROTECT) 
    reservation_date = models.DateTimeField("予約日", auto_now_add=False)
    number_of_people = models.PositiveIntegerField("人数", blank=True, null=True)
    status = models.CharField("予約ステータス", max_length=50, choices=STATUS_TYPES, blank=True)
    created_at = models.DateTimeField("登録日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)    
    deleted_at = models.DateTimeField("削除日", auto_now=True)
    
    class Meta:
        verbose_name_plural = "Reservation"
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'user', 'reservation_date'], name='unique_reservation')
        ]
    
    def __str__(self):
        return self.restaurant.name

class Review(models.Model):
    
    RATES =(
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),    
    )
    
    restaurant = models.ForeignKey(Restaurant, verbose_name="店名", on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, verbose_name="会員氏名", on_delete=models.PROTECT) 
    rate = models.PositiveIntegerField("評価", default=5, choices=RATES)
    comment = models.TextField("コメント", blank=True, null=True)
    visited_at = models.DateField("利用日", auto_now_add=False)
    created_at = models.DateTimeField("登録日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now_add=True)    
    deleted_at = models.DateTimeField("削除日", auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Review"
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'user', 'visited_at'], name='unique_review')
        ]
        

class FavoriteRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT) 

    class Meta:
        verbose_name_plural = "Favorite"
        constraints = [
            models.UniqueConstraint(fields=['restaurant', 'user'], name='unique_favorite')
        ]

    # def __str__(self):
    #     return self.restaurant_id





