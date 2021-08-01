from django.db import models

# Create your models here.
from django.urls import reverse


class Goods(models.Model):
    title = models.CharField(max_length=32, db_index=True)
    slug = models.SlugField(max_length=32, unique=True, verbose_name='URL')
    body = models.CharField(max_length=255, db_index=True, blank=True, verbose_name='Description')
    quantity = models.DecimalField(max_digits=4, decimal_places=0, default=1) #1000
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0) #100 000.00
    is_required = models.BooleanField(default=True)
    time_add = models.DateTimeField(auto_now_add=True, verbose_name='Time (add)')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Time (update)')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Category',blank=True, default=1)
    class Meta:
        ordering=['-time_add','title']
# from goods.models import Category
# Category.objects.create(name='food',slug='food',body='food for home')

#from goods.models import Goods
#Goods.objects.create(title='water',slug='water',body='water Morshynska 1l.',quantity=2,price=11)
# DROP TABLE goods_goods        goods_category
    #drop table goods_goods, goods_category;
    def get_absolute_url(self):
        return reverse('goods_details_url', kwargs={'slug':self.slug})
        #return reverse_lazy()
    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(max_length=32, unique=True, verbose_name='URL')
    body = models.CharField(max_length=255, blank=True, verbose_name='Description')
    time_add = models.DateTimeField(auto_now_add=True, verbose_name='Time (add)', blank=True)

    class Meta:
        verbose_name='Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('show_category_url', kwargs={'slug':self.slug})

    def __str__(self):
        return self.name
