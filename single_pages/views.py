from django.shortcuts import render

# Create your views here.
from shop.models import Product
from review.models import Review


def landing(request):
    recent_product = Product.objects.order_by('-pk')[:5]
    recent_review = Review.objects.order_by('-pk')[:3]
    return render(request,
                  'single_pages/landing.html',
                  {
                        'recent_product':recent_product,
                        'recent_review':recent_review,
                  })