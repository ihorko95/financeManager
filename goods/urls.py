from django.urls import path, include


from goods.views import *

urlpatterns = [
    #path('', indexPage, name='home_url'),
    path('', GoodsList.as_view(), name='home_url'),

    path('transactions/all/', GoodsList.as_view(), name='home_url'),
    path('transactions/<slug:slug>/', ShowGoodsFromCat.as_view(), name='show_category_url'),

    path('transaction/add/', TransactionAdd.as_view(), name='goods_add_url'),
    path('transaction/update/<slug:slug>/', TransactionUpdate.as_view(), name='goods_update_url'),
    path('transaction/delete/<slug:slug>/', TransactionDelete.as_view(), name='goods_delete_url'),
    path('transaction/<slug:slug>/', GoodsDetails.as_view(), name='goods_details_url'),

    path('categories/', CategoryList.as_view(), name='category_list_url'),
    path('category/add/', CategoryAdd.as_view(), name='category_add_url'),
    path('category/update/<slug:slug>/', CategoryUpdate.as_view(), name='category_update_url'),
    path('category/delete/<slug:slug>/', CategoryDelete.as_view(), name='category_delete_url'),

    path('sign-up/', Registration.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logOutUser, name='logout'),

    path('reports/', generateReport, name='generate_report_url'),
    path('data/', get_report_data, name='get_report_data_url'),



]