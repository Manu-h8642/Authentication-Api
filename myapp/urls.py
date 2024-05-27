from django.urls import path
from myapp import views

urlpatterns = [
    path('register/',views.reg.as_view()),
    path('login/',views.loginview.as_view()),
    path('user/',views.Userview.as_view()),
    path('logout/',views.LogoutView.as_view()),
]