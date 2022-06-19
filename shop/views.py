from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, CreateView, UpdateView
from .forms import CommentForm, UserForm

from review.models import Review

# from cart.forms import AddProductForm

# Create your views here.

def product_in_category(request, category_slug=None):
    current_category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available_display=True)

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
    return render(request,
                  'shop/list.html',
                  {
                      'current_category':current_category,
                      'categories':categories,
                      'products':products,

                  })

def product_detail(request, id, product_slug=None):
    product = get_object_or_404(Product, id=id, slug=product_slug)

    comment_form = CommentForm
    return render(request,
                  'shop/detail.html',
                  {
                      'product':product,
                      'comment_form':comment_form,
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


class ProductCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'stock', 'available_display', 'available_order', 'author']
    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_superuser):
            form.instance.author = current_user
            return super(ProductCreate, self).form_valid(form)
        else:
            return redirect('/shop')

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['category', 'name', 'slug', 'image', 'description', 'price', 'stock', 'available_display', 'available_order', 'author']

    template_name = 'shop/product_form_update.html'

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user.is_superuser:
            return super(ProductUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied