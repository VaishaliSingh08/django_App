from django.urls import path, include
from django.conf.urls.static import static
from djangoProject import settings
from dummy import views
from.views import VerificationView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('confirmatiom', views.confirmation, name='confirmation'),
    path('confirmation', views.imapppp, name='imapppp'),
    # path('dashboard', views.dashboard, name='dashboard'),
    # path('', views.show_products, name='show_products'),
    # path('home', views.home, name='home'),

    # path('verification/', include('verify_email.urls')),
    path('activate/<user_id>', VerificationView.as_view(), name='activate'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)