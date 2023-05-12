from django.core.management.base import BaseCommand, CommandError
from news.models import Category, Post


class Command(BaseCommand):
    help = 'Удаляет посты указанной категории'

    def add_arguments(self, parser):
        parser.add_argument('argument', nargs='?', type=str)

    def handle(self, *args, **options):
        posts = Post.objects.filter(category__category_title=options['argument'])

        self.stdout.write('Вы действительно хотите удалить все посты из этой категории? Напишите, "Да", если хотите')

        answer = input()

        if answer == 'Да':
            posts.delete()
            self.stdout.write('Посты удалены!')
            return

        self.stdout.write(self.style.ERROR('Access denied'))
