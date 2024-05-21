from django.db import models
from django.utils import timezone
from django.urls import reverse_lazy,reverse

class Ohb_items(models.Model):

    types= (
        ('1','食パン'),      
        ('2','クロワッサン'),
        ('3','リュスティック'),
        ('4','パイ'),
        ('5','タルティーヌ'),
        ('6','その他'),
    )
    item_name = models.CharField('商品名',max_length=50,blank=False,)
    item_price = models.IntegerField('価格',default=0)
    item_type = models.CharField("タイプ", max_length=15,choices=types, blank=True,default=1)
    item_no= models.CharField(max_length=3,blank=True)

    def __str__(self):
        return self.item_name
    #def get_absolute_url(self):
    #    return reverse('ohb:item', args=[str(self.pk),])
    

class Items_Counts(models.Model):
    item = models.ForeignKey(Ohb_items,on_delete=models.CASCADE)
    item_create = models.IntegerField('作成数',default=0)
    item_los = models.IntegerField('ロス',default=0)
    date = models.DateField('日付')

    def __str__(self):
        return f"{self.item}{self.date}"
    
    def save(self, *args, **kwargs):
        # デフォルトの値をセット
        if self.item_create is None:
            self.item_create = 0
        if self.item_los is None:
            self.item_los = 0

        # 親クラスの save() メソッドを呼び出す
        super().save(*args, **kwargs)
 




