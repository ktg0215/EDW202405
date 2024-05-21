import datetime
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from .forms import BS4ScheduleForm, ScheduleForm
from .models import Schedule
from . import mixins
from .models import User
from user.models import CustomUser
from django.urls import reverse
from django.http import HttpResponse
import csv
#from openpyxl.writer.excel import save_virtual_workbook
import openpyxl as px
from openpyxl import worksheet
from openpyxl.utils import range_boundaries


User = get_user_model()

class Shift_top(generic.TemplateView):
      template_name = 'shift/shift_top.html'
        
class Shift_OutputView(mixins.Shift_OutputMixin, generic.TemplateView):
    
    model = Schedule
    template_name = 'shift/shift_list.html'
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        # shop = get_object_or_404(Shops, pk=self.kwargs['shops_pk'])
        # shop =self.kwargs['shops_pk']
        # context['shops']= User.objects.filter(shops__shop=shop)
        #bb=Shops.objects.all().order_by('shop')
        # c=[]
        # h=[]
        # b= 0
        # for a in bb:
        #     if a.shop in h:
        #         pass
        #     else:
        #         c.append(a)
        #         h.append(a.shop)
        # context['bshop']=c
        context['job_pk']=self.kwargs['job_pk']
        # shop=self.kwargs['shops_pk']
        # context['shop']=Shops.objects.filter(shop=shop)
        context.update(calendar_context)


        return context   

class Shift_csv(mixins.CsvMixin, generic.TemplateView):    
    model = Schedule
    template_name = 'shift/shift_csv.html'
    date_field = 'date'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        # shop = get_object_or_404(Shops, pk=self.kwargs['shops_pk'])
        context['job_pk'] =self.kwargs['job_pk']
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        today = datetime.date.today()
        filename= today
        wb=context['wb']
        response = HttpResponse(content_type='application/vnd.ms-excel')
        # response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename={}.xlsx'.format(filename)
        wb.save(response)
        return response


class Shift_ConfirmationView(mixins.Shift_ConfirmationMixin, generic.TemplateView):
    """スケジュール付きの週間カレンダーを表示するビュー"""
    template_name = 'shift/shift_confirmation.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = get_object_or_404(User, pk=self.kwargs['user_pk'])
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context



class SubmissionView(mixins.SubmissionMixin, generic.View):
    """フォーム付きの月間カレンダーを表示するビュー"""
    template_name = 'shift/submission_schedule.html'
    model = Schedule
    date_field = 'date'
    form_class = ScheduleForm

    def get(self, request, **kwargs):

        context = self.get_month_calendar()
        context['user'] = get_object_or_404(User, pk=self.kwargs['user_pk'])

        return render(request, self.template_name, context)
    

    def post(self, request, **kwargs):

        context = self.get_month_calendar()
        user_pk = self.kwargs['user_pk']
        user = get_object_or_404(User, pk=user_pk)
        context['user'] = user
        formset = context['month_formset']
        if formset.is_valid():

            instances = formset.save(commit=False)
            for schedule in instances:
                schedule.user = user
                schedule.end_at=schedule.get_end_time_display()
                schedule.start_at=schedule.get_start_time_display()
                user.schedule = schedule
                schedule.save()
                user.save()
            return redirect('shift:shift_confirmation', user_pk=user_pk)

        return render(request, self.template_name, context)

