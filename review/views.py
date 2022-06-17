from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.db import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *
# Create your views here.

class ReviewList(ListView):
    model = Review

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ReviewList, self).get_context_data()
    #     context['categories'] = Review.objects.all()
    #     context['count_posts_without_category'] = Review.objects.filter(category=None).count()
    #
    #     return context

class ReviewDetail(DetailView):
    model = Review


class ReviewCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Review
    fields = ['name', 'description', 'review', 'tags']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(ReviewCreate, self).form_valid(form)
        else:
            return redirect('/review/')

class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['name', 'description', 'review', 'tags']

    template_name = 'review/review_form_update.html'

    def dispatch(self, request, *args, **kwargs):
        current_user = request.user
        if current_user.is_authenticated and current_user == self.get_object().author:
            return super(ReviewUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def show_tag_reviews(request, slug):
    tag = Tag.objects.get(slug=slug)
    review_list = tag.review_set.all()

    context = {
        'tag':tag,
        'review_list':review_list
    }
    return render(request, 'review/review_list.html', context)
