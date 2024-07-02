from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path('complaint-success/<str:complaint_id>/', views.complaint_success, name='complaint_success'),
    
    #admin_urls
    
    #dashboard
    path('', views.dashboard, name='dashboard'),
    path('login/',views.loginpage, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    #user 
    path('create_user/',views.create_user, name='create_user'),
    path('success_user',views.success_user,name='success_user'),
    path('all_user',views.view_users, name='view_users'),
    path('edit_user/<str:assign_id>/', views.edit_user, name='edit_user'),
    path('success_user_edit',views.success_user_edit,name='success_user_edit'),
   

    
    #table
    path('accept_reject_complaint/', views.accept_reject_complaint, name='accept_reject_complaint'),
    path('change_status/<str:complaint_id>/', views.change_status, name='change_status'),path('table/',views.table, name='table'),
    path('view-file/<path:file_path>/', views.view_file, name='view_file'),
    path('table/<str:status>/', views.table, name='table_with_status'),
    
    #complaint_assign
    path('assign/<str:complaint_id>/',views.assign,name='assign'),
    path('assigned-success/<str:complaint_id>/<str:username>/', views.assigned_success, name='assigned_success'),
    
    #worker-urls
    path('worker-login/', views.worker_login, name='worker_login'),
    path('worker-dashboard/', views.worker_dashboard, name='worker_dashboard'),
    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)