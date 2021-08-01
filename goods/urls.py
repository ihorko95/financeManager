from django.urls import path, include


from goods.views import *

urlpatterns = [
    #path('', indexPage, name='home_url'),
    path('', GoodsList.as_view(), name='home_url'),
    path('transactions/all/', GoodsList.as_view(), name='home_url'),
    path('transactions/<slug:slug>/', ShowGoodsFromCat.as_view(), name='show_category_url'),
    #path('transactions/<slug:slug>/', ShowGoods.as_view(), name='show_goods_url'),
   # path('transactions/<slug:slug>/', ShowGoods.as_view(), name='category_details_url'),
    path('transaction/add/', TransactionAdd.as_view(), name='goods_add_url'),
    path('transaction/<slug:slug>/', GoodsDetails.as_view(), name='goods_details_url'),
    path('category/add/', CategoryAdd.as_view(), name='category_add_url'),
    # path('category/<slug:slug>/', ShowCategory.as_view(), name='show_category_url'),




]