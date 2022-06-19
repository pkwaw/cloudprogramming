from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

app_name = 'shop'
urlpatterns = [
    path('', product_in_category, name='product_all'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('<int:pk>/<str:slug>/new_comment/', views.new_comment),
    path('create_product/', views.ProductCreate.as_view()),
    path('<slug:category_slug>/', product_in_category, name='product_in_category'),
    # path('<int:id>/<product_slug>/review/', product_review, name='product_review'),
    path('<int:id>/<product_slug>/', product_detail, name='product_detail'),

    # path('<int:id>/<product_slug>/review/', product_review, name='product_detail'),
    # path('review/', include('review.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)