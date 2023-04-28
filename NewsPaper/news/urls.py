from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, CategoryView, upgrade_me, subscribe_category

from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(60)(NewsList.as_view())),
    path('<int:pk>/', cache_page(60*5)(NewsDetail.as_view()), name='post_detail'),
    path('create/', NewsCreate.as_view(), name='post_create'),
    path('update/<int:pk>/', NewsUpdate.as_view(), name='post_update'),
    path('delete/<int:pk>/', NewsDelete.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('category/', CategoryView.as_view(), name='category'),
    path('category/<int:pk>/subscribe/', subscribe_category, name='subscribe_category'),
]