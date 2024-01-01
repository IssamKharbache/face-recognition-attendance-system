from django.urls import path
from . import views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('trysystem/',views.open_cam,name="trysystem"),
    path('statis/',views.statis,name='statis')
]

urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

