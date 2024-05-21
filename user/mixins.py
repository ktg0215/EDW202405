from django import forms
from .models import CustomUser

class NoMixin():

    def get_no(self):

        pk=self.kwargs.get('pk')
        user= CustomUser.objects.filter(job=pk)
        b =[]
        for a in user:
            b.append(a)
        # queryset = UserData.objects.all()
        queryset = CustomUser.objects.filter(job=pk).order_by('user_no')
        count=(len(user))
        users=[]
        FormClass = forms.modelformset_factory(self.model, self.form_class, extra=count,max_num=count)
        if self.request.method == 'POST':
            formset = self.no_formset =FormClass(self.request.POST)
        else:
            formset =  self.no_formset =FormClass(queryset=queryset)
            for bound_form in formset.initial_forms:
                instance = bound_form.instance
                user = instance.user_name
                u={user:bound_form}
                users.append(u)
            else:
                pass
        
        formset = {
            'users': users,
        }
        return formset
    def get_member_no(self):
        context = self.get_no()
        # context['user_forms'] = self.get_no()
        context['formset'] = self.no_formset

        return context
 