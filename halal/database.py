"""
Database Builder. Reads in all the JSON menus and adds the courses to
the database accordingly

Hassaan Ali Wattoo <hawattoo@umich.edu>
"""

from halal import db, models
import os
import datetime
from pprint import pprint

# only consider the following meals when parsing the json files
MEALS = ["BREAKFAST", "LUNCH", "DINNER"]


def create_all_halls():
    """
    Traverses through every dining hall folder and prints out all the JSON file names
    Creates an entry for each dining hall in the database
    :return: void
    """
    dir_path = os.path.dirname(os.path.realpath(__file__)) + "/dining_halls_json_data/"
    for folder in os.listdir(dir_path):
        hall_name = " ".join([x.capitalize() for x in folder.split("_")])
        hall = models.Hall(hall_name)
        if not models.Hall.query.filter_by(name=hall_name).first():
            hall.add()


def create_all_menus():
    """
    Traverses through all the Halls in the database and adds
    corresponding menu objects to the database
    :return: void
    """
    halls = models.Hall.query.all()
    for hall in halls:
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/dining_halls_json_data/"
        # Each menu is stored in the format YEAR-MONTH-DAY.json e.g 2018-04-11.json
        for file in os.listdir(os.path.join(dir_path, hall.get_folder_name_format())):
            file_date = file.split(".")[0]
            date = datetime.datetime.strptime(file_date, "%Y-%m-%d")
            menu = models.Menu(date)
            menu.hall_id = hall.hall_id
            hall.add_menu(menu)
            menu.add()


def create_all_meals_and_courses_and_menu_items():
    """
    This is all as one function for now to avoid multiple traversals of each JSON
    file
    :return: void
    """
    halls = models.Hall.query.all()
    for hall in halls:
        print("Building menu for " + hall.name)
        for menu in hall.menus:
            meals = menu.load_json()['menu']['meal']
            for meal in meals:
                # Ignore useless meals
                if meal['name'] in MEALS:
                    # Create meal object and add to database
                    meal_obj = models.Meal(meal['name'])
                    meal_obj.menu_id = menu.menu_id
                    menu.add_meal(meal_obj)
                    meal_obj.add()

                    # Iterate over courses in the JSON structure
                    add_courses_from_meal(meal_obj, meal)


def add_courses_from_meal(meal_obj, meal_json):
    courses = []
    try:
        courses = meal_json['course']
    except KeyError:
        # Michigan sometimes includes meals with warning messages
        # like "Not serving this course"
        # They do not include any course key in this case
        return

    # If the course is a dict, only one course in the meal
    # Why Michigan doesn't return a list of length one is
    # beyond me.
    if isinstance(courses, dict):
        course = models.Course(courses['name'])
        course.meal_id = meal_obj.meal_id
        meal_obj.add_course(course)
        course.add()
        add_menu_items_from_course(course, courses)
    # Multiple courses for this meal
    else:
        for _course in courses:
            course = models.Course(_course['name'])
            course.meal_id = meal_obj.meal_id
            meal_obj.add_course(course)
            course.add()
            add_menu_items_from_course(course, _course)


def add_menu_items_from_course(course_obj, course_json):
    menuitems = []
    try:
        menuitems = course_json['menuitem']
    except KeyError:
        # Michigan sometimes includes meals with warning messages
        # like "Not serving this course"
        # They do not include any course key in this case
        return

    # If the menuitem is a dict, only one item in the course
    # Why Michigan doesn't return a list of length one is
    # beyond me.
    if isinstance(menuitems, dict):
        menuitem = models.MenuItem(menuitems['name'])
        menuitem.course_id = course_obj.course_id
        if 'trait' in menuitems:
            if 'halal' in menuitems['trait']:
                # Weed Out Non Halal Courses
                menuitem.halal = True
        course_obj.add_menu_item(menuitem)
        menuitem.add()
    # Multiple MenuItems
    else:
        for item in menuitems:
            menuitem = models.MenuItem(item['name'])
            if 'trait' in item:
                if 'halal' in item['trait']:
                    # Weed Out Non Halal Courses
                    menuitem.halal = True
            menuitem.course_id = course_obj.course_id
            course_obj.add_menu_item(menuitem)
            menuitem.add()


def print_halal_meals():
    """
    Debugging function, prints out as much info as possible for each dish
    that is halal in our database
    :return: void
    """
    halal_items = models.MenuItem.query.filter_by(halal=True).all()
    pprint(halal_items)


def build_database():
    print("Building Database")
    db.drop_all()
    db.create_all()
    create_all_halls()
    create_all_menus()
    create_all_meals_and_courses_and_menu_items()
    db.session.commit()


if __name__ == "__main__":
    build_database()
    print_halal_meals()
