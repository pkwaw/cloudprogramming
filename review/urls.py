from django.urls import path
from . import views

urlpatterns = [
    path('review', views.ReviewList.as_view()),
    path('review/<int:pk>/', views.ReviewDetail.as_view()),
    path('tag/<str:slug>/', views.show_tag_reviews),
    path('create_review/', views.ReviewCreate.as_view()),
    path('update_review/<int:pk>', views.ReviewUpdate.as_view()),
]