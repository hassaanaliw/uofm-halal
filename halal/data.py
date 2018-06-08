"""
Query data from the database and format it into a JSON format suitable for the main
Flask API

Hassaan Ali Wattoo <hawattoo@umich.edu>
"""
import json
from pprint import pprint

from halal import models
from datetime import datetime, timedelta
from collections import OrderedDict


def fetch_menus(start_date):
    """
    Returns Data for menus for 7 days for all the dining halls starting at
    :param start_date

    :param start_date: DateTime Object for first date
    :return: JSON object
    """
    end_date = start_date + timedelta(days=6)
    resp = {"start_date": start_date, "data": []}
    while start_date < end_date:
        resp["data"].append(fetch_menu(start_date))
        start_date += timedelta(days=1)

    return resp


def fetch_menu(date):
    """
    Returns a properly formatted JSON response of all menus for a given day
    :param date: DateTime object for given day
    :return: JSON object
    """
    response = {"date": date, "halal_dishes": []}

    data = []

    halal_courses = (
        models.MenuItem.query.with_entities(
            models.MenuItem.name,
            models.Course.name,
            models.Meal.name,
            models.Menu.date,
            models.Menu.hours,
            models.Hall.name,
        )
        .join(models.Course)
        .join(models.Meal)
        .join(models.Menu)
        .join(models.Hall)
        .filter(models.Menu.date == date)
        .filter(models.MenuItem.halal == True)
    )

    for course in halal_courses.all():
        json_times = json.loads(course[4])

        if isinstance(json_times, dict):
            times = [{"name": json_times["event_title"], "desc": ""}]
            start = datetime.strptime(
                json_times["event_time_start"][:-6], "%Y-%m-%dT%H:%M:%S"
            )
            end = datetime.strptime(
                json_times["event_time_end"][:-6], "%Y-%m-%dT%H:%M:%S"
            )
            times[0]["desc"] = "%s to %s" % (start.time(), end.time())

        else:
            times = []
            for time in json_times:
                start = datetime.strptime(
                    time["event_time_start"][:-6], "%Y-%m-%dT%H:%M:%S"
                )
                end = datetime.strptime(
                    time["event_time_end"][:-6], "%Y-%m-%dT%H:%M:%S"
                )
                desc = "%s to %s" % (start.time(), end.time())
                times.append({"name": time["event_title"], "desc": desc})

        resp = {
            "dining_hall": course[5],
            "date": course[3],
            "dish_name": course[0],
            "course_name": course[1],
            "meal_name": course[2],
            "hours": times,
        }

        response["halal_dishes"].append(resp)

    return response


if __name__ == "__main__":
    fetch_menus(datetime(2017, 11, 20, 0, 0))
