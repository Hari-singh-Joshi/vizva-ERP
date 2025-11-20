from django.urls import path
from . import views
urlpatterns = [
    path('', views.case_list, name='case-list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('case/<int:pk>/edit/', views.case_edit, name='case-edit'),
    path('po-entries/', views.po_entry_list, name='ph_list'),
    path('candidates/', views.candidate_list, name='candidate_list'),
     path('timer/', views.timer, name="timer"),
]
