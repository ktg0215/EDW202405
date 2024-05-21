from django.urls import path
from . import views

app_name = 'shift'

urlpatterns = [
    path('shift_top/',views.Shift_top.as_view(),name='shift_top'),
    path('shift_list/<int:job_pk>/', views.Shift_OutputView.as_view(), name='shift_list'),
    path('shift_list/<int:job_pk>/<int:year>/<int:month>/<int:day>/', views.Shift_OutputView.as_view(), name='shift_list'),
    path('user/<int:user_pk>/shift_confirmation/', views.Shift_ConfirmationView.as_view(), name='shift_confirmation'),
    path('user/<int:user_pk>/shift_confirmation/<int:year>/<int:month>/<int:day>/',views.Shift_ConfirmationView.as_view(),name='shift_confirmation'),

    path('shift_csv/<int:job_pk>/<int:year>/<int:month>/<int:day>/', views.Shift_csv.as_view(), name='shift_csv'),
    path('shift_csv/<int:job_pk>/', views.Shift_csv.as_view(), name='shift_csv'),
    path(
        'user/<int:user_pk>/submission_schedule/',
        views.SubmissionView.as_view(), name='submission_schedule'
    ),
    path(
        'user/<int:user_pk>/submission_schedule/<int:year>/<int:month>/<int:day>/',
        views.SubmissionView.as_view(), name='submission_schedule'
    ),
]