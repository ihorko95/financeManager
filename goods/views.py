from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView

from goods.forms import *
from goods.models import Goods, Category
from goods.utils import *


def indexPage(request):
    return render(request,'goods/index_base.html',context={'menu_items':menu_items})
# Create your views here.

class GoodsList(ListView):
    model = Goods
    template_name = 'goods/goods_list.html'
    context_object_name = 'content'

    def get_context_data(self, *, object_list=None, **kwargs):
        summ = self.model.objects.values('price', 'quantity')
        m = 0
        for s in summ:
            m += s['price'] * s['quantity']
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['menu_items'] = menu_items
        context['goods'] = self.model.objects.all()

        paginator = Paginator(context['goods'], 3)
        pageNumber = self.request.GET.get('page')
        page_obj = paginator.get_page(pageNumber)
        context['goods'] = page_obj

        context['summ'] = m
        context['cat_selected'] = 0
        return context


# class ShowGoods(ListView):
#     model = Goods
#     template_name = 'goods_list1'
#     context_object_name = 'content'
#
#     def get_queryset(self):
#         cat = get_object_or_404(Category, slug__iexact=self.kwargs['slug'])
#         return self.model.objects.filter(cat_id=cat.pk)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cat = get_object_or_404(Category, slug__iexact=self.kwargs['slug'])
#         # summ = self.model.objects.filter(cat_id=cat.pk).aggregate(Sum('total'))
#         context['menu_items'] = menu_items
#         context['category'] = Category.objects.all()
#         context['cat_selected'] = self.model.cat_id
#         summ = self.model.objects.get(pk=cat.pk).goods_set.values('price', 'quantity')
#         m=0
#         for s in summ:
#             m+=s['price']*s['quantity']
#         context['summ'] = m
#         # context['summ'] =summ['total__sum']
#         #context['cat_selected'] = cat.pk
#         return context

class GoodsDetails(DetailView):
    model = Goods
    template_name = 'goods/googs_detail.html'
    context_object_name = 'content'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] =menu_items
        context['category'] = Category.objects.all()
        return context

class TransactionAdd(CreateView):
    form_class = GoodsForm
    template_name = 'goods/goods_add.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = menu_items

        return context

class CategoryAdd(CreateView):
    form_class = CategoryForm
    template_name = 'goods/category_add.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = menu_items
        return context


# class ShowCategory(ListView):
#     model = Goods
#     template_name = 'goods/goods_list1.html'
#     context_object_name = 'content'
#     def get_queryset(self):
#         cat = get_object_or_404(Category, slug__iexact=self.kwargs['slug'])
#         return  self.model.objects.filter(cat_id=cat.pk)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         cat = get_object_or_404(Category, slug__iexact=self.kwargs['slug'])
#         summ = self.model.objects.filter(cat_id=cat.pk).aggregate(Sum('price'))
#
#         context = super().get_context_data(**kwargs)
#         context['menu_items'] = menu_items
#         context['category'] = Category.objects.all()
#         context['summ'] =summ['price__sum']
#         context['cat_selected'] = cat.pk
#         return context

class ShowGoodsFromCat(ListMixin, ListView):
    model = Category
    template_name = 'goods/goods_list.html'
    context_object_name = 'content'

    def get_queryset(self):
        cat = get_object_or_404(self.model, slug__iexact=self.kwargs['slug'])
        return self.model.objects.filter(id=cat.pk)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     cat = get_object_or_404(self.model, slug__iexact=self.kwargs['slug'])
    #     summ = self.model.objects.get(pk=cat.pk).goods_set.values('price', 'quantity')
    #     m=0
    #     for s in summ:
    #         m+=s['price']*s['quantity']
    #     context = super().get_context_data(**kwargs)
    #     # context['category'] = self.model.objects.all()
    #     context['category'] = self.model.objects.filter(goods__isnull=False).distinct()
    #     context['menu_items'] = menu_items
    #     context['goods']=self.model.objects.get(pk=cat.pk).goods_set.all()
    #
    #     paginator = Paginator(context['goods'], 2)
    #     pageNumber = self.request.GET.get('page')
    #     page_obj = paginator.get_page(pageNumber)
    #     context['goods'] = page_obj
    #
    #     context['summ'] = m
    #     context['cat_selected'] = cat.pk
    #     return context

