from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # login / logout uchun

    # asosiy sahifalar
    path('', views.index, name='index'),
    path('days/', views.days, name='days'),
    path('work_times/', views.work_times, name='work_times'),
    path('add_worktime/', views.add_worktime, name='add_worktime'),
    path('worktime/<int:pk>/delete/', views.delete_worktime, name='delete_worktime'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('staffs/<int:pk>/delete/', views.delete_staff, name='delete_staff'),
    path('stuffs/', views.staffs, name='stuffs'),
    # path('staffs/<int:pk>/', views.staff_detail, name='staff_detail'),
    path('staffs/<int:staff_id>/', views.staff_detail, name='staff_detail'),

    path('days/', views.days, name='days'),
    path('days/<int:year>/<int:month>/<int:day>/', views.day_detail, name='day_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
