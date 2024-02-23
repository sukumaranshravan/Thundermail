from django.urls import path
from user_app import views
from django.conf.urls.static import static
urlpatterns = [
    path('',views.start_up,name='start_up'),
    path('sign_up/',views.sign_up,name='sign_up'),
    path('register/',views.register,name='register'),
    path('sign_in/',views.sign_in,name='sign_in'),
    path('sign_out/',views.sign_out,name='sign_out'),
]
