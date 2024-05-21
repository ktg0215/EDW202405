from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import FormView
from django import forms
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from ohb.models import Ohb_items,Items_Counts
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.urls import reverse
from .forms import items_CountsForm,NoForm
from . import mixins
import datetime
from django.utils import timezone
import pandas as pd
from django_pandas.io import read_frame
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np


class ItemsCreateView(CreateView):
    model = Ohb_items
    template_name= 'ohb/create.html'
    fields = "__all__"
    success_url = reverse_lazy('ohb:create')

class ItemsListView(ListView):
    model = Ohb_items
    template_name= 'ohb/items_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Ohb_items.objects.all().order_by('item_type')

        db=read_frame(items)
        
        df_context = pd.DataFrame(columns=['item_name', 'item_price', 'item_type'])
        df_context['item_name']=db['item_name']
        df_context['item_price']=db['item_price']
        df_context['item_type']=db['item_type']
        context['df_context'] = df_context
        #context['i']=items
        return context
    
class Create_los_ListView(ListView,mixins.Item_create_losMixin):
    model = Items_Counts
    template_name= 'ohb/week_list.html'
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date']=self.get_date()
        date=self.get_date()
        for a,n in date:
            month_ago=a.month-1
            month_next=a.month+1
            year_ago=a.year-1
            year_next=a.year+1
            year=a.year
            month=a.month
            day=a.day
        #12月と1月の年が変わるタイミングの処理
        if month_ago ==0:
            month_ago=12
        else:
            year_ago=year
        if month_next==13:
            month_next=1
            pass
        else:
            year_next=year
        context['day']=day
        context['year']=year
        context['month']=month
        context['month_ago']=month_ago
        context['month_next']=month_next
        context['year_ago']=year_ago
        context['year_next']=year_next
        df_context=self.create_list()
        context['df_context']=df_context
        return context

class Buy_View(Create_los_ListView,mixins.Item_create_losMixin):
    model = Items_Counts
    template_name= 'ohb/buy.html'
    date_field = 'date'
        
    def get_context(self, **kwargs):
        context = self.get_context_data()
        df_context=self.get_buy_date()
        context.update(df_context)
        #context['df_context']=df_context


        return context
        



# class Top(generic.TemplateView):
#     template_name = 'ohb/top.html'

class Items_View(generic.View,mixins.Items_Mixin):
    model=Items_Counts
    form_class=items_CountsForm
    template_name='ohb/form.html'
    date_field = 'date'

    def get(self, request, **kwargs):
        #contextはフォームセットが入っている、day_contextは日付関連が入っている、これを纏める為のupdate
        context = self.get_count()
        day_context=self.get_count_day()
        context.update(day_context)

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        context = self.get_count()
        formset = context['formset']
        if formset.is_valid():
            instances = formset.save(commit=False)
            print(7878787878)
            for aa in instances:
                item = aa.item
                item_create=aa.item_create
                item_los=aa.item_los
                date=aa.date

                aa.save()
                item.save()
            return redirect('list')
        if not formset.is_valid():
            print(formset.errors)
        day_context=self.get_count_day()
        context.update(day_context)
        return render(request, self.template_name, context)

class Graph_View(generic.View,mixins.Graph_Item_Mixin):
    model=Items_Counts
    template_name='ohb/graph.html'
    date_field = 'date'

    def get(self, request, **kwargs):
        #graph_image = self.get_item_id()
        context=self.get_item_id()
        # context = {
        #     'graph_image': graph_image
        # }
        #context['graph_image']=graph_image
        #context['today']=datetime.datetime.now().day
        return  render(request, self.template_name, context)
    
class item_No_Views(generic.View,mixins.NoMixin):
    model=Ohb_items
    form_class=NoForm
    template_name='ohb/item_no.html'

    def get(self, request, **kwargs):
        context = self.get_item_no()

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        context = self.get_item_no()
        formset = context['formset']
        if formset.is_valid():
            instances = formset.save(commit=False)
            for a in instances:
                a.save()
                
            return redirect('item_no')
        if not formset.is_valid():
            print(formset.errors)
            
        return render(request, self.template_name, context)
