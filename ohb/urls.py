from django.urls import path
from . import views

app_name='ohb'

urlpatterns = [
    # path('top/',views.Top.as_view(), name='top'),
    path('create/',views.ItemsCreateView.as_view(), name='create'),
    path('list/', views.ItemsListView.as_view(), name='list'),
    path('form/', views.Items_View.as_view(), name='form'),
    path('form/<int:year>/<int:month>/<int:day>/', views.Items_View.as_view(), name='form'),
    path('week_list/', views.Create_los_ListView.as_view(), name='week_list'),
    path('week_list/<int:year>/<int:month>/', views.Create_los_ListView.as_view(), name='week_list'),
    #path('buy/', views.Buy＿View.as_view(), name='buy'),
    #path('buy/<int:year>/<int:month>/', views.Buy＿View.as_view(), name='buy'),
    path('graph/', views.Graph_View.as_view(), name='graph'),
    path('graph/<int:id>/<int:year>/<int:month>/<int:day>', views.Graph_View.as_view(), name='graph'),
    path('item_no/', views.item_No_Views.as_view(), name='item_no'),
    


    #path('form/', views.make_test_modelformset, name='form'),
    
]