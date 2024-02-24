from django.urls import path
from user_app import views
from django.conf.urls.static import static
urlpatterns = [
    path('',views.start_up,name='start_up'),
    path('sign_up/',views.sign_up,name='sign_up'),
    path('register/',views.register,name='register'),
    path('sign_in/',views.sign_in,name='sign_in'),
    path('home/',views.home,name='home'),
    path('sign_out/',views.sign_out,name='sign_out'),
    path('compose/',views.compose,name='compose'),
    path('compose_action/',views.compose_action,name='compose_action'),
    path('sent_items/',views.sent_items,name='sent_items'),
    path('read_message<int:id>/',views.read_message,name='read_message'),
]
