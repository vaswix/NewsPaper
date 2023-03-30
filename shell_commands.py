from NewsPaper.news.models import *

user01 = User.objects.create(username='User01')
user02 = User.objects.create(username='User02')

user01 = User.objects.get(pk=1)
user02 = User.objects.get(pk=2)

author01 = Author.objects.create(username=user01)
author02 = Author.objects.create(username=user02)

author01 = Author.objects.get(pk=1)
author02 = Author.objects.get(pk=2)

category01 = Category.objects.create(category_title='Today News')
category02 = Category.objects.create(category_title='Yesterday News')
category03 = Category.objects.create(category_title='Breaking News')
category04 = Category.objects.create(category_title='Weekly News')

category01 = Category.objects.get(pk=1)
category02 = Category.objects.get(pk=2)
category03 = Category.objects.get(pk=3)
category04 = Category.objects.get(pk=4)

article01 = Post.objects.create(author=author01, type_news='PA', title='Заголовок_статьи_1',
                                text='Текст_статьиt_1')
article02 = Post.objects.create(author=author01, type_news='PA', title='Заголовок_статьи_2',
                                text='Текст_статьиt_2')

news01 = Post.objects.create(author=author02, type_news='PN', title='Заголовок_новости_1',
                             text='Текст_новости_1')

article01 = Post.objects.get(pk=1)
article02 = Post.objects.get(pk=2)

news01 = Post.objects.get(pk=3)

article01.category.add(category01)
article01.category.add(category02)
article02.category.add(category03)

news01.category.add(category03)

# Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
comment01 = Comment.objects.create(post=article01, user=user01, text='Текст_статьи_комментария_1')
comment02 = Comment.objects.create(post=article02, user=user02, text='Текст_статьи_комментария_2')
comment03 = Comment.objects.create(post=article01, user=user01, text='Текст_статьи_комментария_3')
comment04 = Comment.objects.create(post=news01, user=user02, text='Текст_новости_комментария_1')

comment01 = Comment.objects.get(pk=1)
comment02 = Comment.objects.get(pk=2)
comment03 = Comment.objects.get(pk=3)
comment04 = Comment.objects.get(pk=4)

# Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
comment01.like()
comment02.like()
comment03.like()
comment04.like()
comment01.like()
comment02.like()
comment03.like()
comment01.like()
comment02.like()
comment01.like()
comment01.dislike()
comment04.dislike()
comment03.dislike()
comment01.dislike()
article01.like()
article01.like()
article01.like()
article01.like()
article01.like()
article02.like()
article02.like()
article02.like()
news01.dislike()

author01.update_rating()
author02.update_rating()

author01.authorRating
author02.authorRating

best = Author.objects.all().order_by('-author_rating').values('username', 'author_rating')[0]

print(best)

Post.objects.all().order_by('-post_rating').values('date_created', 'author__username__username', 'post_rating',
                                                   'preview_name', 'text')[0]

Comment.objects.all().order_by().values('date_created', 'user__username', 'post', 'comment_rating',
                                        'text')[0]

Post.objects.all().values('author', 'preview_name')
Post.objects.filter(postAuthor=author02)
Post.objects.filter(preview_name='Заголовок_статьи_1').values('postAuthor')

Comment.objects.all().values('post', 'author')
Comment.objects.filter(commentPost=article01).values('text')
Comment.objects.filter(commentText='Текст_статьи_комментария_2').values('comment_rating')

Author.objects.filter(pk=1)
Author.objects.all().values('username', 'pk')
