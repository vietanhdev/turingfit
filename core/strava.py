from django.conf import settings
from django.utils.timezone import datetime, timedelta
from stravalib.client import Client
from core.models import WeekDistance


def get_access_token(user, force_refresh=False):
    """Get access token for user, refresh if necessary."""
    client = Client()
    social = user.social_auth.get(provider="strava")
    if not social.extra_data.get("refresh_token", None):
        return None
    refresh_token = social.extra_data["refresh_token"]
    if (
        not force_refresh
        and "expires_at" in social.extra_data
        and social.extra_data["expires_at"] > datetime.now().timestamp()
    ):
        return social.extra_data["access_token"]
    try:
        token_response = client.refresh_access_token(
            client_id=settings.SOCIAL_AUTH_STRAVA_KEY,
            client_secret=settings.SOCIAL_AUTH_STRAVA_SECRET,
            refresh_token=refresh_token,
        )
        social.extra_data["access_token"] = token_response["access_token"]
        social.extra_data["refresh_token"] = token_response["refresh_token"]
        social.extra_data["expires_at"] = token_response["expires_at"]
        social.save()
        return token_response["access_token"]
    except:
        social.extra_data["access_token"] = None
        social.extra_data["refresh_token"] = None
        social.save()
        return None


def get_access_token_with_verification(user):
    """Get access token and call Strava API to verify it."""
    token = get_access_token(user)
    if not token:
        return None
    client = Client()
    client.access_token = token
    try:
        athlete = client.get_athlete()
        if athlete:
            return token
    except:
        pass
    return get_access_token(user, force_refresh=True)


def sync_user_weekly_distance(user):
    """Synchronize user weekly distance from Strava."""
    from_datetime = datetime.today()
    from_datetime -= timedelta(days=from_datetime.weekday())
    week_from_date = from_datetime.strftime("%d/%m/%Y")
    to_datetime = datetime.today()
    to_datetime += timedelta(days=6 - to_datetime.weekday())
    week_to_date = to_datetime.strftime("%d/%m/%Y")
    from_datetime = datetime.strptime(
        week_from_date + " 00:00:00", "%d/%m/%Y %H:%M:%S"
    )
    to_datetime = datetime.strptime(
        week_to_date + " 23:59:59", "%d/%m/%Y %H:%M:%S"
    )

    token = get_access_token_with_verification(user)
    if not token:
        return None
    client = Client()
    client.access_token = token
    activities = client.get_activities(after=from_datetime, before=to_datetime)
    week_distance = 0
    for activity in activities:
        if activity.type not in ("Run", "Walk"):
            continue
        week_distance += activity.distance.num / 1000.0

    WeekDistance.objects.update_or_create(
        user=user,
        week=from_datetime.date(),
        defaults={"distance": week_distance},
    )

    return week_distance
