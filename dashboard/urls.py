from django.urls import path, include
from django.conf.urls.static import static
from djangoProject import settings
from dashboard import views

urlpatterns = [

    path('dashboard', views.dash, name='dash'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('add_product', views.add_product, name='add_product'),
    path('products', views.products, name='products'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit_product/<int:id>', views.edit_product, name='edit_product'),
    path('home', views.show_products, name='show_products'),
    path('', views.show_products, name='show_products'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


##attached media folder
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)