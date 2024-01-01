from django.urls import path
from . import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users.views import ChangePasswordView


urlpatterns = [
    path('',user_views.LoginPage,name="login"),
    path('logout/',user_views.logoutPage,name="logout"),
    path('home/',user_views.home,name="home"),
    path('adduser/',user_views.adduser,name="adduser"),
    path('addemploye/',user_views.addEmploye,name="addemploye"),
    path('profile/',user_views.profile,name='profile'),
    path('editemploye/<str:pk>/',user_views.editEmploye,name='edit'),
    path('allemploye/',user_views.allemploye,name="allemploye"),
    path('delete/<str:pk>/',user_views.delete,name="delete"),
    path('about/',user_views.aboutPage,name='about'),
    path('editemployetry/<str:pk>/',user_views.editemployetry,name='edittry'),
    path('deletetry/<str:pk>/',user_views.deletetry,name='deletetry'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    
]

urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)