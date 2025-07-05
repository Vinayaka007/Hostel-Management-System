from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from project_user_ctr.views import index_page, base_page, login_view, register, success_page, student_page, logout_view, user_index, apply_for_hostel,room_allotment, complaint_box, complaint_success, admin_room_allotment,get_room_details,admin_login,admin_work,applicant,accept_application,delete_application,complaint_list,accept_complaint,delete_complaint,post_notice,notice_list,delete_notice, update_notice, notice_list_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index_page, name='index'),
    path('base/', base_page, name='base'),
    path('register/', register, name='register'),
    
    path('success/', success_page, name='success'),
    
    
    path('logout/', logout_view, name='logout'),

    path('login/', login_view, name='login'),
    path('student/', student_page, name='student_page'),
    path('user_index/', user_index, name='user_index'),
    path('apply/', apply_for_hostel, name='apply_for_hostel'),
    
    path('room_allotment/', room_allotment, name='room_allotment'),
    
    path('complaint/', complaint_box, name='complaint_box'),
    path('complaint/success/', complaint_success, name='complaint_success'),
    path('admin_room_allot/', admin_room_allotment, name='admin_room_allot'),
    path('get-room-details/', get_room_details, name='get_room_details'),
    path('admin_login/', admin_login, name='admin_login'),
    path('admin_work/', admin_work, name='admin_work'),
    path('applicant/', applicant, name='applicant'),
    path('accept/<int:id>/', accept_application, name='accept_application'),
    path('delete/<int:id>/', delete_application, name='delete_application'),
    path('complaints/', complaint_list, name='complaint_list'),
    path('accept_complaint/<int:id>/', accept_complaint, name='accept_complaint'),
    path('delete_complaint/<int:id>/', delete_complaint, name='delete_complaint'),
    path('post_notice/', post_notice, name='post_notice'),
    path('notice_list/', notice_list, name='notice_list'),
    path('notice/delete/<int:notice_id>/', delete_notice, name='delete_notice'),
    path('notice/update/<int:notice_id>/', update_notice, name='update_notice'),
    path('notice_list_user/', notice_list_user, name='notice_list_user'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

