from django.urls import path
from .views import NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, CategoryView, upgrade_me, subscribe_category


urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>/', NewsDetail.as_view(), name='post_detail'),
    path('create/', NewsCreate.as_view(), name='post_create'),
    path('update/<int:pk>/', NewsUpdate.as_view(), name='post_update'),
    path('delete/<int:pk>/', NewsDelete.as_view(), name='post_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('category/', CategoryView.as_view(), name='category'),
    path('category/<int:pk>/subscribe/', subscribe_category, name='subscribe_category'),
]