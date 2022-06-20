from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import *
from shop.models import *
from django.db.models import Q


# Create your views here.

class ReviewList(ListView):
    model = Review

class ReviewDetail(DetailView):
    model = Review

class ReviewCreate(CreateView):
    model = Review
    fields = ['title', 'description', 'review', 'tags']

    def test_func(self):
        pass

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(ReviewCreate, self).form_valid(form)
        else:
            return redirect('/review')

class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    fields = ['title', 'description', 'review', 'tags']

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

def show_login(request):
    return render(request, 'review/login.html')

class ReviewSearch(ReviewList):
    paginate_by = None
    def get_queryset(self):
        q = self.kwargs['q']
        review_list = Review.objects.filter(Q(title__contains=q) | Q(tags__name__contains=q)
        ).distinct()
        return review_list

    def get_context_date(self, **kwargs):
        context = super(ReviewSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context
