"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import request
from django.urls import path
from .views import main_view,signup_view,login_view,logout_view,adds,withdraw,reset_passs,update_passs
from profiles.views import my_recommendations_view,makedeposit


urlpatterns = [
    path('', main_view,name='main-view'),
    path('admin/', admin.site.urls),
    path('signup/', signup_view,name='signup-view'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('profiles/',my_recommendations_view, name='my-recs-views'),
    path('make-deposit/',makedeposit,name="make-deposit"),
    path('daily-ads/',adds,name="daily-ads"),
    path('withdraw/',withdraw,name="withdraw"),
    path('reset-password/',reset_passs,name='reset-password'),
    path('update/',update_passs,name='update-password'),
    path('<str:ref_code>/',main_view,name='main-view'),
    

]
