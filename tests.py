import unittest
from datetime import datetime
from pprint import pprint

import os
from flask_testing import TestCase

from halal import app, api, data, database, db, models


class DatabaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///halal_test.db"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///halal_test.db"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        # Clean Up by deleting database file
        db.session.remove()
        db.drop_all()
        os.remove("halal/halal_test.db")

    def test_db_create(self):
        # Tests if the database was created successfully
        self.assertTrue(os.path.exists("halal/halal_test.db"))

    def test_db_structure(self):
        # Tests if all the tables have been created successfully
        tables = ["course", "hall", "meal", "menu", "menu_item"]
        actual_tables = db.engine.table_names()
        self.assertEqual(tables, actual_tables)

    def test_build_halls_menus(self):
        # Tests if the creating halls and menus method works correctly
        database.create_all_halls()
        halls = models.Hall.query.filter(
            models.Hall.name == "Bursley Dining " "Hall"
        ).all()

        self.assertTrue(len(halls) > 0)

        # Tests if the creating menus method works correctly
        database.create_all_menus()
        menus = models.Menu.query.all()
        self.assertTrue(len(menus) > 0)


class APITest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///halal_test.db"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///halal_test.db"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove("halal/halal_test.db")

    def format_date_today(self):
        # Creates a DateTime object for today with the time set to 00:00
        month = datetime.now().month
        year = datetime.now().year
        day = datetime.now().day
        return datetime(year=year, month=month, day=day)

    def add_objects(self):
        # Create some sample halls, menus, meals and menutiems for the API

        hall = models.Hall("Test Dining")
        db.session.add(hall)

        menu = models.Menu(self.format_date_today())
        menu.hall_id = hall.hall_id
        menu.hours = """{"event_day_start": "Monday", "event_time_start": 
               "2017-11-20T07:00:00-05:00", "event_day_end": "Monday", 
               "event_time_end": "2017-11-20T21:00:00-05:00", "event_title": 
               "Continuous Service", "event_description": {}, "event_maplink": 
               "https://maps.google.ch/maps?q="} """
        hall.menus.append(menu)
        db.session.add(menu)

        meal = models.Meal("Test Meal")
        meal.menu_id = menu.menu_id
        menu.meals.append(meal)
        db.session.add(meal)

        course = models.Course("Test Course")
        course.meal_id = meal.meal_id
        meal.courses.append(course)
        db.session.add(course)

        menuitem = models.MenuItem("Test MenuItem")
        menuitem.course_id = course.course_id
        menuitem.halal = 1
        course.menuitems.append(menuitem)
        db.session.add(menuitem)

        db.session.commit()

    def check_response(self, response):
        # Checks the given response against what we expect
        date = self.format_date_today()
        self.assertEqual(response["date"], date)

        halal_dishes = response["halal_dishes"][0]
        self.assertEqual(halal_dishes["course_name"], "Test Course")
        self.assertEqual(halal_dishes["date"], date)
        self.assertEqual(halal_dishes["dining_hall"], "Test Dining")
        self.assertEqual(halal_dishes["dish_name"], "Test MenuItem")
        self.assertEqual(halal_dishes["meal_name"], "Test Meal")

        hours = halal_dishes["hours"][0]
        self.assertEqual(hours["desc"], "07:00:00 to 21:00:00")
        self.assertEqual(hours["name"], "Continuous Service")

    def test_add_objects(self):
        self.add_objects()
        response = data.fetch_menu(self.format_date_today())
        self.check_response(response)


class AppResponseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///halal_test.db"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///halal_test.db"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        os.remove("halal/halal_test.db")

    def test_index_response(self):
        response = self.client.get("/")
        self.assert200(response)


if __name__ == "__main__":
    unittest.main()
