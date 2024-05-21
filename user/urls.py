from django.urls import path
from . import views
from .views import login_view

app_name='user'

urlpatterns = [
    # ... other URL patterns
   # path('', views.login_view, name='login'),
    #path('', views.CustomLoginView.as_view(), name='login'),
    path('', views.login_view, name='login'), 
    path('top/',views.Top.as_view(),name='top'),
    path('<int:pk>no/',views.MemberNo.as_view(),name='no'),
   

]