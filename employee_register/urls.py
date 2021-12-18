# from django.contrib import admin
# from django.contrib import admin
from django.contrib import admin
from django.urls import path, include

from employee_register import views
# from django import views
    
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage , name="HomePage"),
    path('inseart/', views.InsertStudent , name="InseartStudent"),
    path('update/', views.update_all , name="update_all"),
    path('delete/', views.delete_data , name="delete_data"),
    # path('getData/', views.get_data , name="getData")
    path('getStudent/', views.get_student_for_datatable , name="getStudnet"),
    path('deparment/', views.departmentlist , name="departmentlist"),
]