import logging
import os
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from dotenv import load_dotenv
from news.models import *

load_dotenv()

logger = logging.getLogger(__name__)


def send_email():
    users = User.objects.all()
    # перебор юзеров
    for user in users:
        if user.category_set.values():
            # получение категорий в которых состоит юзер
            for category in user.category_set.values():
                posts = Post.objects.filter(category__pk=category['id']).filter(
                    date_created__gte=datetime.now(tz=pytz.UTC) - timedelta(days=7)
                )
                # перебор постов полученных через связь категории и поста которые были созданы за последние 7 дней
                for post in posts:
                    send_mail(
                        subject=post.title,
                        message=f'{post.text[0:49]} http://127.0.0.1/{post.pk}',
                        from_email=os.environ.get('USER'),
                        recipient_list=user.email
                    )

        def delete_old_job_executions(max_age=604_800):
            """This job deletes all apscheduler job executions older than `max_age` from the database."""
            DjangoJobExecution.objects.delete_old_job_executions(max_age)

        class Command(BaseCommand):
            help = "Runs apscheduler."

            def handle(self, *args, **options):
                scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
                scheduler.add_jobstore(DjangoJobStore(), "default")

                scheduler.add_job(
                    send_email,
                    trigger=CronTrigger(day="*/7"),
                    id="send_email",
                    max_instances=1,
                    replace_existing=True,
                )
                logger.info("Added job 'send_email'.")

                scheduler.add_job(
                    delete_old_job_executions,
                    trigger=CronTrigger(
                        day_of_week="mon", hour="00", minute="00"
                    ),
                    id="delete_old_job_executions",
                    max_instances=1,
                    replace_existing=True,
                )
                logger.info(
                    "Added weekly job: 'delete_old_job_executions'."
                )

                try:
                    logger.info("Starting scheduler...")
                    scheduler.start()
                except KeyboardInterrupt:
                    logger.info("Stopping scheduler...")
                    scheduler.shutdown()
                    logger.info("Scheduler shut down successfully!")
