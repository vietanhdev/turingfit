import logging
from workers import task
from django.contrib.auth.models import User

from .strava import sync_user_weekly_distance


@task(schedule=10 * 60)
def sync_strava():
    file_rotation_handler = logging.handlers.RotatingFileHandler(
        "sync_strava.log", maxBytes=100000, backupCount=5
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(file_rotation_handler)
    logger.setLevel(logging.INFO)
    logger.info("Starting sync_strava task")
    all_users = User.objects.all()
    for user in all_users:
        distance = sync_user_weekly_distance(user)
        if distance is not None:
            logger.info(f"Synced {user.username}: {distance}km")
