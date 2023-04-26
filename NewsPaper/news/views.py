from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, User


class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date_created')
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])
        context['category'] = post.category.values()[0]['category_title']
        return context


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = PostForm
    template_name = 'post_create.html'
    permission_required = ('news.add_post',)

    def post(self, request, *args, **kwargs):
        post = Post(
            author_id=self.request.user.id,
            type_news=request.POST['type_news'],
            title=request.POST['title'],
            text=request.POST['text'],
        )
        post.save()
        post.category.add(int(request.POST['category']))
        post.save()

        pk_category = self.request.POST['category']
        users = Category.objects.all().filter(pk=pk_category).values('subscribers')

        email_list = []
        for user in users:
            email = User.objects.all().filter(pk=user['subscribers']).values('email')[0]['email']
            if email:
                email_list.append(email)

        html_content = render_to_string(
            'news_created.html',
            {
                'post': post,
            }
        )

        msg = EmailMultiAlternatives(
            subject=post.title,
            body=post.text[0:49],
            from_email='Lack10000@yandex.ru',
            to=email_list
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        return redirect('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.filter(author__username=self.request.user.pk).filter(
            date_created__day=datetime.today().day
        )

        if len(posts) >= 3:
            context.pop('form')
            context['info'] = 'Нельзя создать больше 3 постов в день'
        return context


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    form_class = PostForm
    template_name = 'post_create.html'
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)


class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    queryset = Post.objects.all()
    template_name = 'post_delete.html'
    success_url = '/news/'
    permission_required = ('news.delete_post',)


class CategoryView(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_category = [x['pk'] for x in self.request.user.category_set.values('category_title').values('pk')]
        context['user_categories'] = user_category
        return context


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')


def subscribe_category(request, **kwargs):
    user = request.user
    pk = kwargs.get('pk')
    Category.objects.get(pk=pk).subscribers.add(user)
    return redirect('category')
