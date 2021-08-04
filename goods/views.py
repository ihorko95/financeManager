from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['menu_items'] = menu_items

        search_query = self.request.GET.get('search', '')
        if search_query:
            search_obj=self.model.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
            context['goods']=search_obj
        else: context['goods'] = self.model.objects.all()

        paginator = Paginator(context['goods'], 3)
        pageNumber = self.request.GET.get('page')
        page_obj = paginator.get_page(pageNumber)
        context['goods'] = page_obj
        m = 0
        if search_query:
            for s in search_obj.values('price','quantity'):
                m += s['price'] * s['quantity']
        else:
            summ = self.model.objects.values('price', 'quantity')
            for s in summ:
                m += s['price'] * s['quantity']

        context['summ'] = m
        context['cat_selected'] = 0
        return context

class GoodsDetails(DetailView):
    model = Goods
    template_name = 'goods/goods_detail.html'
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
class TransactionUpdate(LoginRequiredMixin,UpdateView):
    model = Goods
    form_class = GoodsForm
    #fields = ['title','slug','body','cat','quantity','price','is_required']
    template_name_suffix = '_update_form'
class TransactionDelete(LoginRequiredMixin,DeleteView):
    model = Goods
    success_url = reverse_lazy('home_url')

class CategoryAdd(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = 'goods/category_add.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = menu_items
        return context

class CategoryUpdate(LoginRequiredMixin,UpdateView):
    model = Category
    form_class = CategoryForm
    #fields = ['name', 'slug', 'body']
    template_name_suffix = '_update_form'
class CategoryDelete(LoginRequiredMixin,DeleteView):
    model = Category
    success_url = reverse_lazy('category_list_url')
class CategoryList(ListView):
    model = Category
    template_name = 'goods/category_list.html'
    context_object_name = 'content'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_items'] = menu_items
        return context

class ShowGoodsFromCat(ListMixin, ListView):
    model = Category
    template_name = 'goods/goods_list.html'
    context_object_name = 'content'

    def get_queryset(self):
        cat = get_object_or_404(self.model, slug__iexact=self.kwargs['slug'])
        return self.model.objects.filter(id=cat.pk)

class Registration(CreateView):
    form_class = RegisterUserForm
    template_name = 'goods/register.html'
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('home_url')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'goods/login.html'
    # success_url = reverse_lazy('home_url')
    def get_success_url(self):
        return reverse_lazy('home_url')

def logOutUser(request):
    logout(request)
    return redirect('login')
