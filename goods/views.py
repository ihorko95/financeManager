from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from goods.forms import *
from goods.models import Goods, Category
from goods.utils import *
import json
from django.http import JsonResponse, HttpResponse


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
        context['orders']=['title', 'time_add', 'cat']
        # self.model.
        order_query = self.request.GET.get('order', 'time_add')


        search_query = self.request.GET.get('search', '')
        if search_query:
            search_obj=self.model.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
            context['goods']=search_obj.order_by(order_query)
        else: context['goods'] = self.model.objects.all().order_by(order_query)
        context['order_query'] =order_query

        paginator = Paginator(context['goods'], 20)
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
    success_url = reverse_lazy('home_url')

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

def indexPage(request):
    return render(request,'goods/index_base.html',context={'menu_items':menu_items})

# def get_json(request,data):
#     return JsonResponse(data)

def get_report_data(request,data={'seles': 100,'costomers': 10}):
    print(data)
    # return JsonResponse(data,safe=False)
    return JsonResponse({"models_to_return": list(data)})


def generateReport(request):
    form = ReportForm
    if request.method == 'POST':
        form = ReportForm(request.POST)
        #print(form.errors)
        if form.is_valid():
            # print('DATA: ')
            data = form.cleaned_data
            if data['time_to'] < data['time_from']:
                form.add_error(None,"Date is not correct. 'Date From' must be before 'Date To'.")
            else:
                #print('Operation: ')
                #print(data['operation'])
                if data['operation'] == None:
                    goods_obj = Goods.objects.filter(
                        Q(time_add__gte=data['time_from']) and Q(time_add__lte=data['time_to']))
                else:
                    goods_obj = Goods.objects.filter(
                        (Q(time_add__gte=data['time_from']) and Q(time_add__lte=data['time_to'])),
                        cat__name=data['operation'])

                #make json
                obj_dict={}
                for obj in goods_obj:
                    if str(obj.time_add.date()) not in obj_dict.keys():
                        obj_dict[str(obj.time_add.date())]= [0,[]]
                    obj_dict[str(obj.time_add.date())][0]+= float(obj.get_total_price())
                    obj_dict[str(obj.time_add.date())][1].append(obj.title)
                # print(goods_obj)
                # print(obj_dict)

               # qs_json = serializers.serialize('json', obj_dict)
                qs_json = json.dumps(obj_dict, indent=4)
                #qs_json.replace(/&quot;/g,'"')
                # print (qs_json)
                # test =JsonResponse({'Python': 52.9, 'Jython': 1.6, 'Iron Python': 27.7})
                #get_json(obj_dict)
                #get_report_data(request, data=goods_obj)
                context = {
                    'menu_items': menu_items,
                    'data':goods_obj,
                    'test':qs_json
                    # 'test': get_report_data(request,data=goods_obj)
                }
                return render(request, 'goods/report.html',context=context)
                # print(data['time_from'], data['time_to'], data['operation'])

        #else:
        #    form = ReportForm()
    context={
        'menu_items':menu_items,
        'form':form
    }

    return render(request, 'goods/generate_report.html',context=context)



