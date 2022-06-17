from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, CreateView


# from cart.forms import AddProductForm

# Create your views here.

def product_in_category(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)
    count = Category.objects.all().count()

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)



    return render(request,
                  'shop/list.html',
                  {
                      'current_category':current_category,
                      'categories':categories,
                      'products':products,
                      'count':count
                  })


# class CategoryList(ListView):
#     model = Product
#
#     def get_context_data(self, **kwargs):
#         context = super(CategoryList, self).get_context_data()
#         context['categories'] = Category.object.all()
#         context['no_category_post_count'] = Product.objects.filter(category=None).count()
#
#         return context


def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)
    count = Product.objects.all()
    # add_to_cart = AddProductForm(initial={'quantity':1})
    return render(request,
                  'shop/detail.html',
                  {
                      'product':product,
                      # 'add_to_cart':add_to_cart
                  })

# def product_review(request, id, product_slug=None):
#     product = get_object_or_404(Product, id=id, slug=product_slug)
#     review = get_object_or_404(Product, id=id, slug=product_slug)
#     return render(request,
#                   'shop/../review/templates/review.html',
#                   {
#                       'product': product,
#                       'review':review,
#                   })

# class ReviewList(ListView):
#     model = Review
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ReviewList, self).get_context_data()
#         context['categories'] = Category.objects.all()
#         context['count_posts_without_category'] = Review.objects.filter(category=None).count()
#
#         return context
#
#
# class ReviewCreate(CreateView):
#     model = Review
#     fields = ['name', 'description', 'review']
