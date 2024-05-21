from collections import deque
import datetime
import itertools
from django import forms
from django_pandas.io import read_frame
from .models import Items_Counts,Ohb_items
import pandas as pd
import numpy as np
from django.shortcuts import redirect, render, get_object_or_404
from django.shortcuts import render
from bs4 import BeautifulSoup
import urllib.request
import re
from .forms import items_CountsForm,NoForm
import calendar
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import io
import urllib, base64
#import seaborn as sns
from django.db.models import Value, IntegerField
from django.db.models.functions import Cast





def get_item():
    item_list=[]
    queryset=Ohb_items.objects.all().order_by('item_type')
    for a in queryset:
        item_list.append(a.item_name)

    return item_list

    
class Item_create_losMixin():

    def get_date(self,**kwargs):
        #1ｶ月の日付の取得
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month ==None:
            year=datetime.datetime.now().year
            month=datetime.datetime.now().month
            day=datetime.datetime.now().day
        else:
            pass

        dtm = calendar.monthrange(year,month)[1]
        
        date = datetime.date(year = int(year),month=int(month),day=int(1))
        datelist = [date + datetime.timedelta(days =day) for day in range(0,dtm)]
        weekname=[]
        name=['月','火','水','木','金','土','日']
        for aa in datelist:
            a=aa.weekday()
            w=name[a]
            weekname.append(w)

        monthday=zip(datelist,weekname)

        return monthday
    
    def create_list(self):
        datelist=self.get_date()
        db=[]
        #月の最初と最後の日だけを変数に入れる
        for a,b in datelist:
            db.append(a)


        start=db[0]
        end=db[-1]
        #クエリセットの一ヵ月間のデータと取り出すためのキーを作成
        lookup = {'{}__range'.format(self.date_field): (start, end),}
        #クエリセットで上記で作ったキーを使い期間内のデータ取り出し、アイテムタイプで並べ替え
        queryset=Items_Counts.objects.filter(**lookup).order_by('item__item_no')
        days = {day: [] for day in db}   
        df = pd.DataFrame(days)
## 全部の合計
        all=[]
        for a in db:
            o=Items_Counts.objects.filter(date=a).order_by('item__item_no')
            n=len(o)
            ic=[]
            il=[]
            for a,b in zip(o,range(n,0,-1)):
                if b ==1:
                    
                    ic.append(a.item_create)
                    il.append(a.item_los)
                    ic_sum=sum(ic)
                    il_sum=sum(il)
                    item_m=str(ic_sum)+'('+str(il_sum)+')'
                    all.append(item_m)     
                   
                else:
                    ic.append(a.item_create)
                    il.append(a.item_los)
        m=1
        for a,b in zip(all,db):
            date=b
            if m == 1:
                ddf =pd.DataFrame({date:[a]},index =['all'])
                df = pd.concat([df,ddf],axis=0)
                df.fillna(" ", inplace=True)
                m = 2
            else:    
                df[date]= df[date].astype(str)
                df.at['all',date] =a
                df.fillna(" ", inplace=True)
#ここまで

        a=1
        for db in queryset:
            date= db.date
            item=db.item
            item_c=db.item_create
            item_l=db.item_los
            item_m=str(item_c)+'('+str(item_l)+')'
            if a == 1:
                item=db.item
                ddf =pd.DataFrame({date:item_m},index =[item])
                df = pd.concat([df,ddf],axis=0)
                df.fillna(" ", inplace=True)

                a = 2
                
            elif item != db.item: 
                item=db.item
                ddf =pd.DataFrame({date:item_m},index =[item])
                df = pd.concat([df,ddf],axis=0)
                df.fillna(" ", inplace=True)
                
            else:    
                item=db.item
                df[date]= df[date].astype(str)
                df.at[item,date] =item_m
                df.fillna(" ", inplace=True)
                   
        df.fillna(" ", inplace=True)
        
        return df

    # def get_buy_date(self):
    #     detalist=self.get_date()
    #     db=[]
    #     #月の最初と最後の日だけを変数に入れる
    #     for a,b in detalist:
    #         db.append(a)


    #     start=db[0]
    #     end=db[-1]
    #     #クエリセットの一ヵ月間のデータと取り出すためのキーを作成
    #     lookup = {'{}__range'.format(self.date_field): (start, end),}
    #     #クエリセットで上記で作ったキーを使い期間内のデータ取り出し、アイテムタイプで並べ替え
    #     queryset=Items_Counts.objects.filter(**lookup).order_by('item__item_type')
    #     item_list=get_item()
    #     days = {day: [] for day in db}   
    #     df = pd.DataFrame(days)


    #     a=1
    #     for db in queryset:
    #         date= db.date
    #         item=db.item
    #         item_c=db.item_create-db.item_los
    #         print(item_c)
    #         item_l=db.item_los
    #         item_m=str(item_c)+'('+str(item_l)+')'
    #         if a == 1:
    #             item=db.item
    #             item="http://127.0.0.1:8000/form/"
    #             ddf =pd.DataFrame({date:item_m},index =[item])
    #             df = pd.concat([df,ddf],axis=0)
    #             df.fillna(" ", inplace=True)
    #             a = 2
                
    #         elif item != db.item: 
    #             item=db.item
    #             ddf =pd.DataFrame({date:item_m},index =[item])
    #             df = pd.concat([df,ddf],axis=0)
    #             df.fillna(" ", inplace=True)
                
    #         else:    
    #             item=db.item
    #             df[date]= df[date].astype(str)
    #             df.at[item,date] =item_m
    #             df.fillna(" ", inplace=True)
                   
               
    #     df.fillna(" ", inplace=True)
        
    #     return df
class Items_Mixin(Item_create_losMixin):
    
    def get_count(self):
        #get_count＿dayで日付を取得
        days=self.get_count_day()
        year=days['year']
        month=days['month']
        day=days['day']
        days=datetime.date(year, month, day)
        i = Ohb_items.objects.all().order_by('item_no')
        items=[]
        date =datetime.date.today()
        count=(len(i))
        itemname= []
        for q in i:
            o={'item':q,'date':days}
            itemname.append(o)
            items.append(q)
        
        date = datetime.date.today()
        FormClass = forms.modelformset_factory(Items_Counts,form=items_CountsForm, extra=count,max_num=count)
        #co=Items_Counts.objects.filter(date=datetime.date.today()).count()
        co=Items_Counts.objects.filter(date=days).count()
        if self.request.method == 'POST': 
            formset = self.items_formset = FormClass(self.request.POST)
            zip_date=zip(items,formset)
        elif co==0:
            formset= self.items_formset =FormClass(queryset=Items_Counts.objects.none(),initial=itemname)
            zip_date=zip(items,formset)
        else:
            formset = self.items_formset =FormClass(queryset=Items_Counts.objects.filter(date=days).order_by('item__item_no'))
            zip_date=zip(items,formset)


        formset = {
        'formset':formset,
        'zip_date':zip_date,
  
       }
        return formset

    def get_count_day(self,**kwargs):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        #context = self.get_count()
        day_context={}
        if month ==None:
            year=datetime.datetime.now().year
            month=datetime.datetime.now().month
            day=datetime.datetime.now().day
        else:
            pass
        bb=[]
        date=self.get_date()
        for a,n in date:
            month_ago=a.month-1
            year_ago=a.year-1
            year_next=a.year+1
            year=a.year
            month=a.month
            day_ago=a.day-1
            first_day=1
            bb.append(a.day)
            
        last_day=bb[-1]
        #12月と1月の年が変わるタイミングの処理
        if day==last_day:
            day_next=1
            day_ago=day-1
            month_next=month+1
        else:
            day_next=day+1
            month_next=month
        if day==1:
            day_ago=28
            month_ago=month-1
        else:
            month_ago=month
            day_ago=day-1
        if month_ago ==0:
            month_ago=12
        else:
            year_ago=year
        if month_next==13:
            month_next=1
            pass
        else:
            year_next=year
        day_context['today']=datetime.datetime.now().day
        day_context['year']=year
        day_context['month']=month
        day_context['month_ago']=month_ago
        day_context['month_next']=month_next
        day_context['year_ago']=year_ago
        day_context['year_next']=year_next

        day_context['daya']=day_ago
        day_context['year']=year
        day_context['month']=month
        day_context['day']=day
        day_context['dayb']=day_next

        return day_context


class Graph_Item_Mixin(Items_Mixin,Item_create_losMixin):
    

    def get_item_id(self,**kwargs):
        item_id=self.kwargs.get('id')
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        day=self.kwargs.get('day')
        
        if item_id ==100:
            context=self.get_count_day()
            days=self.get_date()
            day=[]
            last=[]
            y=[]
            
            last_month_day = calendar.monthrange(year,month-1)[1] #先月の最終日
            last_start=datetime.date(year,month-1,1)
            last_end=datetime.date(year,month-1,last_month_day)
            last_month=[]
            
            for a in range(1,last_month_day):
                l=datetime.date(year,month-1,a)
                last_month.append(l)

            
            for a,b in days:
                day.append(a)
                y.append(b)

            item_create=[]
            item_los=[]
            days=[]
            
            for a in day:
                o=Items_Counts.objects.filter(date=a).order_by('item__item_no')
                n=len(o)
                ic=[]
                il=[]
                
                for a,b in zip(o,range(n,0,-1)):
                    if b ==1:
                        ic.append(a.item_create)
                        il.append(a.item_los)
                        ic_sum=sum(ic)
                        il_sum=sum(il)
                        item_create.append(ic_sum) 
                        item_los.append(il_sum)  
                        days.append(a.date.day)     
                    else:
                        ic.append(a.item_create)
                        il.append(a.item_los)
                        
            last_item_create=[]
            last_item_los=[]            
            for a in last_month:
                o=Items_Counts.objects.filter(date=a).order_by('item__item_no')
                n=len(o)
                ic=[]
                il=[]
                
                for a,b in zip(o,range(n,0,-1)):
                    if b ==1:
                        ic.append(a.item_create)
                        il.append(a.item_los)
                        ic_sum=sum(ic)
                        il_sum=sum(il)
                        last_item_create.append(ic_sum) 
                        last_item_los.append(il_sum)
                        
                    else:
                        ic.append(a.item_create)
                        il.append(a.item_los)
            item_name='all'
        else:
            context=self.get_count_day()
            days=self.get_date()
            day=[]
            last=[]
            y=[]
            last_month_day = calendar.monthrange(year,month-1)[1] #先月の最終日
            last_start=datetime.date(year,month-1,1)
            last_end=datetime.date(year,month-1,last_month_day)
            for a,b in days:
                day.append(a)
                y.append(b)

            start=day[0]
            end=day[-1]
            lookup = {'{}__range'.format(self.date_field): (start, end),}
            last_lookup= {'{}__range'.format(self.date_field): (last_start, last_end),}#先月のデータ
            #クエリセットで上記で作ったキーを使い期間内のデータ取り出し、アイテムタイプで並べ替え
            item=Items_Counts.objects.filter(item_id=item_id,**lookup).order_by('date')
            last_month_item=Items_Counts.objects.filter(item_id=item_id,**last_lookup).order_by('date')#先月のデータ

            item_create=[]
            item_los=[]
            days=[]
            last_item_create=[]
            
            for u in item :
                item_create.append(u.item_create)
                item_los.append(u.item_los)
                days.append(u.date.day)
                item_name=u.item
            last_item_create=[]
            for a in last_month_item:
                last_item_create.append(a.item_create)  

        #context['item']=item_name
        context['item_create']=item_create
        context['item_los']=item_los
        context['days']=days
        week=[]
        x=len(days)
        week_label=y[:x]
        for a,b in zip(days,week_label):
            c=f"{a}日\n({b})"
            week.append(c)
        plt.rcParams['font.family'] = 'Meiryo'
        categories =  days
        window_size = 7 #平均を出す期間


        # 確認: データが十分あるかどうか
        if len(item_create) < window_size:
            # データが足りないため、エラーメッセージを表示して終了
            return "Insufficient data for calculating moving average."
        
        def calculate_moving_average(data, window_size):
            moving_average = np.zeros(len(data))
            for i in range(window_size - 1, len(data)):
                # 7日間の平均を計算
                moving_average[i] = np.mean(data[i - window_size + 1:i + 1])

            return moving_average
        # 10月のデータ
        date = days
        
        # 9月のデータを取得（最終7日間分）
        last_date = last_item_create[-7:]
        if len(last_date) == 0:
             last_date = np.zeros(window_size)
             print("データがないよ")
        print("データがあるよ")
        # 9月のデータを末尾に追加して移動平均を計算
        combined_data = np.concatenate((last_date,item_create))
        moving_average = calculate_moving_average(combined_data, window_size)
        moving_average = moving_average[len(last_date):]
        index = days
        item_create_filled = [item_create[days.index(date)] if date in days else 0 for date in index]
        item_los_filled = [item_los[days.index(date)] if date in days else 0 for date in index]
        #moving_average_filled = [moving_average[days.index(date)] if date in days else 0 for date in index]
        plt.figure(figsize=(20, 8))
        # グラフの位置
        bar_width = 0.7
        xy=max(item_create)
        y = [5,10,xy]
        # 棒グラフを描画
        plt.bar(index, item_create_filled, bar_width, color='#6495ed', label='販売数')
        plt.bar(index, item_los_filled, bar_width, bottom=item_create_filled, color='#d0af4c', label='ロス')
        plt.plot(index, moving_average, label='移動平均', color='red')
        # グラフのカスタマイズ
        plt.xlabel('日')
        plt.ylabel('Values')
        plt.title(f"{month}月   {item_name}")
        
        plt.xticks(index,labels=week)
        
        if xy>100:
            plt.yticks(range(0, max(y)+10, 30))
        else:
            plt.yticks(range(0, max(y)+10, 5))
        plt.legend()
        
        plt.grid(axis='y')
        # グラフの画像をbase64エンコードして返す
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.3)
        buffer.seek(0)



        plt.show()
        plt.close()
        ave_list = [round(num, 1) for num in moving_average]
        context['ave']=ave_list
        context['graph_image']=base64.b64encode(buffer.read()).decode('utf-8')

        return context


class NoMixin():

    def get_no(self):
        item= Ohb_items.objects.all()
        b=[ a for a in item]
        # queryset = UserData.objects.all()
        queryset = Ohb_items.objects.all().order_by('item_no')
        count=(len(item))
        items=[]
        FormClass = forms.modelformset_factory(Ohb_items,NoForm, extra=count,max_num=count)
        if self.request.method == 'POST':
            formset = self.item_no_formset = FormClass(self.request.POST)
        else:
            formset = self.item_no_formset = FormClass(queryset=queryset)
            # for bound_form in formset.initial_forms:
            #         instance = bound_form.instance
            #         item_name=instance.item_name
            #         u={item_name:bound_form}
            #         items.append(u)
                   
                        
        formset = {
            #'items': items,
            'formset':formset
        }
        return formset
    def get_item_no(self):
        context = self.get_no()
        # context['user_forms'] = self.get_no()
        context['item_no_formset'] = self.item_no_formset
        
        return context


# class Graph_Item_Mixin(Items_Mixin,Item_create_losMixin):
    

#     def get_item_id(self,**kwargs):
#         item_id=self.kwargs.get('id')
#         year=self.kwargs.get('year')
#         month=self.kwargs.get('month')
#         day=self.kwargs.get('day')
#         #
#         context=self.get_count_day()
#         days=self.get_date()
#         day=[]
#         last=[]
#         y=[]
#         last_month_day = calendar.monthrange(year,month-1)[1] #先月の最終日
#         last_start=datetime.date(year,month-1,1)
#         last_end=datetime.date(year,month-1,last_month_day)
#         for a,b in days:
#             day.append(a)
#             y.append(b)

#         start=day[0]
#         end=day[-1]
#         lookup = {'{}__range'.format(self.date_field): (start, end),}
#         last_lookup= {'{}__range'.format(self.date_field): (last_start, last_end),}#先月のデータ
#         #クエリセットで上記で作ったキーを使い期間内のデータ取り出し、アイテムタイプで並べ替え
#         item=Items_Counts.objects.filter(item_id=item_id,**lookup).order_by('date')
#         last_month_item=Items_Counts.objects.filter(item_id=item_id,**last_lookup).order_by('date')#先月のデータ

#         item_create=[]
#         item_los=[]
#         days=[]
#         last_item_create=[]
        
#         for u in item :
#             item_create.append(u.item_create)
#             item_los.append(u.item_los)
#             days.append(u.date.day)
#             item_name=u.item
#         last_item_create=[]
#         for a in last_month_item:
#             last_item_create.append(a.item_create)

#         context['item']=item_name
#         context['item_create']=item_create
#         context['item_los']=item_los
#         context['days']=days
#         week=[]
#         x=len(days)
#         week_label=y[:x]
#         for a,b in zip(days,week_label):
#             c=f"{a}日({b})"
#             week.append(c)
#         print(week)
#         plt.rcParams['font.family'] = 'Meiryo'
#         categories =  days
#         window_size = 7 #平均を出す期間

#         # 確認: データが十分あるかどうか
#         if len(item_create) < window_size:
#             # データが足りないため、エラーメッセージを表示して終了
#             return "Insufficient data for calculating moving average."
        
#         def calculate_moving_average(data, window_size):
#             moving_average = np.zeros(len(data))
#             for i in range(window_size - 1, len(data)):
#                 # 7日間の平均を計算
#                 moving_average[i] = np.mean(data[i - window_size + 1:i + 1])

#             return moving_average
#         # 10月のデータ
#         date = days
        
#         # 9月のデータを取得（最終7日間分）
#         last_date = last_item_create[-7:]
#         if len(last_date) == 0:
#              last_date = np.zeros(window_size)
#              print("データがないよ")
#         print("データがあるよ")
#         # 9月のデータを末尾に追加して移動平均を計算
#         combined_data = np.concatenate((last_date,item_create))
#         moving_average = calculate_moving_average(combined_data, window_size)
#         moving_average = moving_average[len(last_date):]
#         index = days

#         item_create_filled = [item_create[days.index(date)] if date in days else 0 for date in index]
#         item_los_filled = [item_los[days.index(date)] if date in days else 0 for date in index]
#         #moving_average_filled = [moving_average[days.index(date)] if date in days else 0 for date in index]
        
#         # グラフの位置
#         bar_width = 0.7
#         y = [10, 25, 40]
#         # 棒グラフを描画
#         plt.bar(index, item_create_filled, bar_width, color='#6495ed', label='販売数')
#         plt.bar(index, item_los_filled, bar_width, bottom=item_create_filled, color='#d0af4c', label='ロス')
#         plt.plot(index, moving_average, label='移動平均', color='red')
#         # グラフのカスタマイズ
#         plt.xlabel('日')
#         plt.ylabel('Values')
#         plt.title(f"{month}月   {item_name}")
#         plt.xticks(index,labels=week)
#         plt.yticks(range(0, max(y)+1, 5))
#         plt.legend()
#         plt.grid(axis='y')
#         # グラフの画像をbase64エンコードして返す
#         buffer = io.BytesIO()
#         plt.savefig(buffer, format='png')
#         buffer.seek(0)
#         plt.show()
#         plt.close()
#         ave_list = [round(num, 1) for num in moving_average]
#         context['ave']=ave_list
#         context['graph_image']=base64.b64encode(buffer.read()).decode('utf-8')

#         return context















































