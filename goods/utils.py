from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
menu_items ={'Add Transaction':'goods_add_url', 'Add category':'category_add_url', 'Pricing':0, 'FAQs':0, 'About':0}

class ListMixin:
    model=None
    def get_context_data(self, *, object_list=None, **kwargs):
        cat = get_object_or_404(self.model, slug__iexact=self.kwargs['slug'])
        summ = self.model.objects.get(pk=cat.pk).goods_set.values('price', 'quantity')
        m=0
        for s in summ:
            m+=s['price']*s['quantity']
        context = super().get_context_data(**kwargs)
        # context['category'] = self.model.objects.all()
        context['category'] = self.model.objects.filter(goods__isnull=False).distinct()
        context['menu_items'] = menu_items
        context['goods']=self.model.objects.get(pk=cat.pk).goods_set.all()

        paginator = Paginator(context['goods'], 3)
        pageNumber = self.request.GET.get('page')
        page_obj = paginator.get_page(pageNumber)
        context['goods'] = page_obj

        context['summ'] = m
        context['cat_selected'] = cat.pk
        return context