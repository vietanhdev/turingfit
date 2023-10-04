from django.utils.timezone import datetime, timedelta
from core import models
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from stravalib.client import Client

from .strava import get_access_token_with_verification


@login_required
def home(request):
    activities = None
    from_date = None
    to_date = None
    if settings.SHOW_PERSONAL_ACTIVITIES:
        activities = []
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        view_this_week = (request.GET.get("submit") == "this_week") or (
            not from_date and not to_date and not request.GET.get("submit")
        )
        if view_this_week:
            need_redirect = False
            from_datetime = datetime.today()
            from_datetime -= timedelta(days=from_datetime.weekday())
            week_from_date = from_datetime.strftime("%d/%m/%Y")
            if not from_date or from_date != week_from_date:
                from_date = week_from_date
                need_redirect = True
            to_datetime = datetime.today()
            to_datetime += timedelta(days=6 - to_datetime.weekday())
            week_to_date = to_datetime.strftime("%d/%m/%Y")
            if not to_date or to_date != week_to_date:
                to_date = week_to_date
                need_redirect = True
            if need_redirect:
                return redirect(
                    "/?from_date={}&to_date={}&submit=this_week".format(
                        from_date, to_date
                    )
                )

        view_last_week = request.GET.get("submit") == "last_week"
        if view_last_week:
            need_redirect = False
            if not from_date:
                from_datetime = datetime.today()
                from_datetime -= timedelta(days=from_datetime.weekday() + 7)
                from_date = from_datetime.strftime("%d/%m/%Y")
                need_redirect = True
            if not to_date:
                to_datetime = datetime.today()
                to_datetime += timedelta(days=6 - to_datetime.weekday() + 7)
                to_date = to_datetime.strftime("%d/%m/%Y")
                need_redirect = True
            if need_redirect:
                return redirect(
                    "/?from_date={}&to_date={}".format(from_date, to_date)
                )

        if from_date:
            from_datetime = datetime.strptime(
                from_date + " 00:00:00", "%d/%m/%Y %H:%M:%S"
            )
        if to_date:
            to_datetime = datetime.strptime(
                to_date + " 23:59:59", "%d/%m/%Y %H:%M:%S"
            )

        page = request.GET.get("page")

        # Get activities
        access_token = get_access_token_with_verification(request.user)
        client = Client(access_token=access_token)

        if from_date and to_date:
            query = client.get_activities(before=to_datetime, after=from_datetime)
        elif from_date:
            query = client.get_activities(after=from_datetime)
        else:  # to_date
            query = client.get_activities(before=to_datetime)

        for activity in query:
            if from_date and not to_date:
                index = 0
            else:
                index = len(activities)

            activities.insert(
                index,
                {
                    "id": activity.id,
                    "name": activity.name,
                    "distance": activity.distance.num / 1000,
                    "type": activity.type,
                    "link": "https://www.strava.com/activities/{}".format(
                        activity.id
                    ),
                    "date": activity.start_date_local,
                },
            )

        paginator = Paginator(activities, 20)  # Show n results per page
        try:
            activities = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            activities = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            activities = paginator.page(paginator.num_pages)

    # Leaderboard
    leaderboard = models.WeekDistance.objects.filter(
        week__gte=datetime.today() - timedelta(days=7)
    ).order_by("-distance")

    return render(
        request,
        "core/home.html",
        context={
            "activities": activities,
            "from_date": from_date,
            "to_date": to_date,
            "leaderboard": leaderboard,
        },
    )
