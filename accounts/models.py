import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Job(models.Model):
    
    name = models.CharField(max_length=200)
    
    # class Meta:
    #     verbose_name_plural = "Job"
    #     # constraints = [
    #     #     models.UniqueConstraint(fields=['name'], name='unique_job')
    #     # ]
    
    def __str__(self):
         return self.name   

class CustomUser(AbstractUser):
    GENDER_TYPES = (
        ("男性","男性"),
        ("女性","女性"),
        ("未回答","未回答"),
    )
    # e_mail = models.EmailField("E-Mail",unique=True)
    user_name_kanji = models.CharField("名前" ,max_length=20, blank=False, null=False)
    user_name_kana = models.CharField("ふりがな" ,max_length=50, blank=False, null=False)
    # birthday = models.DateField("生年月日" ,auto_now=True)
    birthday = models.CharField("生年月日" , max_length=20, null=True, blank=True)
    gender = models.CharField("性別", max_length=50, choices=GENDER_TYPES, blank=True)
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, blank=True, null=True)
    # job = models.CharField("職業", max_length=200, blank=True, null=True)
    
    # 有料会員情報
    is_subscribed = models.BooleanField(default=False, verbose_name="有料会員")
    card_name = models.CharField(max_length=128, null=True, blank=True, verbose_name="カード名義")
    card_number = models.CharField(max_length=128, null=True, blank=True, verbose_name="カード番号")
    
    created_day = models.DateTimeField("登録日", default=datetime.datetime.now, null=True, blank=True)
    updated_day = models.DateTimeField("更新日", default=datetime.datetime.now, null=True, blank=True)    
    deleted_day = models.DateTimeField("削除日", null=True, blank=True)
    
    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['e_mail'], name='unique_member')
    #     ]
    class Meta:
        verbose_name_plural = "CustomUser"
        # constraints = [
        #     models.UniqueConstraint(fields=['user_name_kanji'], name='unique_user_name_kanji')
        # ]
    
    def __str__(self):
        return self.user_name_kanji

