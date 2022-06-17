from django.db import models
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    meta_description = models.TextField(blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/{self.slug}/'
        # return reverse('shop:product_in_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, blank=True)
    stock = models.PositiveIntegerField()
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)


    review = models.TextField(blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created', '-updated']
        index_together = [['id', 'slug']]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/shop/{self.pk}/{self.slug}/'
        # return reverse('shop:product_detail', args=[self.id, self.slug])

    # def get_absolute_url2(self):
    #     return f'/review.html/'
    #     # return reverse('shop:product_detail', args=[self.id, self.slug])

    # def show_review(request):
    #     return render(request, 'shop/../review/templates/review.html')



# class Product_Review(models.Model):
#     review = models.TextField()
#
#     def __str__(self):
#         return self.review
#
#     def get_absolute_url(self):
#         return f'/shop/{self.pk}/{self.slug}/'
#         # return f'/shop/{self.pk}/{self.slug}/review/'
#         # return f'/shop/{self.pk}/'
#         # return render('shop:product_review', args=[self.id, self.slug])

# class Review(models.Model):
#     name = models.CharField(max_length=200, db_index=True)
#     review = models.TextField(blank=True)
#     description = models.TextField(blank=True)
#
#     def get_absolute_url(self):
#         return f'/shop/'