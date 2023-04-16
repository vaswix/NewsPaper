from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

from .filters import PostFilter

from .forms import PostForm


class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-date_created')
    paginate_by = 10

    def get_context_data(self,
                         **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,
                                       queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class NewsCreate(CreateView):
    form_class = PostForm
    template_name = 'post_create.html'


class NewsUpdate(UpdateView):
    form_class = PostForm
    template_name = 'post_create.html'

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return Post.objects.get(pk=pk)


class NewsDelete(DeleteView):
    queryset = Post.objects.all()
    template_name = 'post_delete.html'
    success_url = '/news/'
