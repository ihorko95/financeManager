from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
menu_items ={'Add Transaction':'goods_add_url', 'Categories':'category_list_url', 'Reports':'generate_report_url'}


class ListMixin:
    model=None
    def get_context_data(self, *, object_list=None, **kwargs):
        cat = get_object_or_404(self.model, slug__iexact=self.kwargs['slug'])
        #c = self.model.objects.get(pk=cat.pk)
        #summ = c.goods_set.values('price', 'quantity')


        summ = self.model.objects.get(pk=cat.pk).goods_set.values('price', 'quantity')
        m=0
        for s in summ:
            m+=s['price']*s['quantity']
        context = super().get_context_data(**kwargs)
        # context['category'] = self.model.objects.all()
        context['orders'] = ['title', 'time_add', 'cat']
        # self.model.
        order_query = self.request.GET.get('order', 'time_add')
        context['menu_items'] = menu_items
        #context['goods'] = c.goods_set.all()
        context['goods']=self.model.objects.get(pk=cat.pk).goods_set.all().order_by(order_query)
        context['order_query'] =order_query
        context['category'] = self.model.objects.filter(goods__isnull=False).distinct()



        paginator = Paginator(context['goods'], 20)
        pageNumber = self.request.GET.get('page')
        page_obj = paginator.get_page(pageNumber)
        context['goods'] = page_obj

        context['summ'] = m
        context['cat_selected'] = cat.pk
        return context