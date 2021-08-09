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
                if data['operation'] == None:
                    goods_obj = Goods.objects.filter(
                        Q(time_add__gte=data['time_from']) and Q(time_add__lte=data['time_to']))
                else:
                    goods_obj = Goods.objects.filter(
                        (Q(time_add__gte=data['time_from']) and Q(time_add__lte=data['time_to'])),
                        cat__name=data['operation'])

                #make json
                # obj_dict={}
                # i = 0
                # obj_dict[i] = ['', 0, []]
                #
                # for obj in goods_obj.order_by('time_add'):
                #     if str(obj.time_add.date()) !=  obj_dict[i][0] and obj_dict[i][0] != '':
                #         i += 1
                #         obj_dict[i]= ['',0,[]]
                #
                #     obj_dict[i][0]= str(obj.time_add.date())
                #     obj_dict[i][1]+= float(obj.get_total_price())
                #     obj_dict[i][2].append(obj.title)
                obj_dict=[]
                i = 0
                temp = { 'x':'', 'y': 0,'z': []}

                for obj in goods_obj.order_by('time_add'):
                    if str(obj.time_add.date()) !=  temp['x'] and temp['x'] != '':
                        i += 1
                        temp = {'x': '', 'y': 0, 'z': []}
                    temp['x'] = str(obj.time_add.date())
                    temp['y'] += float(obj.get_total_price())
                    temp['z'].append(obj.title)

                    obj_dict.append(temp)

                # print('Data: ')
                # print(goods_obj)
                # print('To JSON: ')
                # print(obj_dict)


                #Category JSON
                # print('Data: ')
                # print(goods_obj)
                cat_dict=[]
                # i = 0
                # temp = {'category': '', 'value':[{ 'x': '', 'y': 0, 'z': []}]}
                data_labels = ['Date']
                # print('Here: ')
                cats_labels=set(goods_obj.values_list('cat__name'))

                # print(cats_labels)
                for label in cats_labels:
                    data_labels.append(str(label).replace("'",'').replace("(",'').replace(")",'').replace(",",'')) #WTF???
                data_res=[]
                data_res.append(data_labels)
                data_template = [0] * len(data_labels)
                for obj in goods_obj.order_by('time_add'):
                    if str(obj.time_add.date()) != data_template[0]:
                        data_template = [0] * len(data_labels)
                        data_template[0]= str(obj.time_add.date())
                    cat_index=data_labels.index(str(obj.cat))
                    data_template[cat_index]+=float(obj.get_total_price())
                    data_res.append(data_template)
                print(data_res)

                # if temp1['category']['value']['x'] == 'hi':
                #     print('That is true')
                # for obj in goods_obj.order_by('time_add'):
                #     if str(obj.time_add.date()) != temp['value']['x'] and temp['value']['x'] != '' :
                #         print('hello')
                chart_json = json.dumps(data_res, indent=4)
                qs_json = json.dumps(obj_dict, indent=4)

                context = {
                    'menu_items': menu_items,
                    'chart_data': chart_json,
                    'dataw':goods_obj,
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



