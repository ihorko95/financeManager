from django import forms

from goods.models import *


class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods
        fields = ['title','slug','body','cat','quantity','price','is_required']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','slug','body']