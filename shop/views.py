from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, CreateView
from .forms import CommentForm, UserForm

from review.models import Review

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
    review = Review.objects.all()
    comment_form = CommentForm
    # add_to_cart = AddProductForm(initial={'quantity':1})
    return render(request,
                  'shop/detail.html',
                  {
                      'product':product,
                      'review':review,
                      'comment_form':comment_form
                      # 'add_to_cart':add_to_cart
                  })

def new_comment(request, pk, slug):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk, slug=slug)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.product = product
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(product.get_absolute_url())
    else:
        raise PermissionDenied

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

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'shop/signup.html', {'form': form})


class ProductCreate(CreateView):
    model = Product
    fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'stock', 'available_display', 'available_order', 'author']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser):
            form.instance.author = current_user
            return super(ProductCreate, self).form_valid(form)
        else:
            return redirect('/shop')