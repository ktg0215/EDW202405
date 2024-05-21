from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views import generic
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login
from . import mixins
from .models import CustomUser
from .forms import MemberNoForm

User = get_user_model()

logger = logging.getLogger(__name__)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # フォームからユーザー名を取得
        password = request.POST.get('password')  # フォームからパスワードを取得

        # ユーザーの認証を試行
        logger.debug(f"Received username: {username}, password: {password}")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 認証に成功した場合
            login(request, user)  # ユーザーをログインさせる
            user_authenticated_successfully = True
            return redirect('top/')  # ログイン後のページにリダイレクト
        else:
    # 認証に失敗した場合
            messages.error(request, 'ユーザー認証に失敗しました。正しいユーザー名とパスワードを入力してください。')
            user_authenticated_successfully = False
            return render(request, 'login.html', {'authentication_failed': True})

        # GETリクエストを処理する場合
    else:
        user_authenticated_successfully = False  # 初期状態では認証は成功していない
        return render(request, 'login.html', {'authentication_failed': False})

class Top(generic.TemplateView):
    template_name = 'top.html'

class MemberNo(generic.View,mixins.NoMixin):
    model=CustomUser
    form_class=MemberNoForm
    template_name='no.html'

    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        context = self.get_member_no()

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        context = self.get_member_no()
        formset = context['formset']

        if formset.is_valid():
            instances = formset.save(commit=False)
            for customuser in instances:
                customuser.save()
                pk=1
            return redirect('user:top')

        return render(request, self.template_name, context)



# User = get_user_model()

# def login_view(request):
#     if request.method == 'POST':
#         user_id = request.POST['user_id']
#         password = request.POST['password']

#         user = authenticate(user_id=user_id, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('ohb/top.html')  # ログイン成功後のリダイレクト先を適宜設定
#         else:
#             messages.error(request, 'Invalid user_id or password.')

#     return render(request, 'user/login.html')

# @login_required
# def home_view(request):
#     return render(request, 'ohb/top.html')


# views.py