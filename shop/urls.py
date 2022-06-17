from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'shop'
urlpatterns = [
    path('', product_in_category, name='product_all'),
    path('<slug:category_slug>/', product_in_category, name='product_in_category'),
    # path('<int:id>/<product_slug>/review/', product_review, name='product_review'),
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'),
    # path('<int:id>/<product_slug>/review/', product_review, name='product_detail'),
    # path('review/', include('review.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)