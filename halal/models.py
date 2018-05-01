"""
Defines schema for all the tables in our database. All tables are related

Hall => Menu (One to Many)
Menu => Meal (One to Many)
Meal => Course (One to Many)
Course => MenuItem (One to Many)

Hassaan Ali Wattoo - <hawattoo@umich.edu>
"""

import json
import os
from halal import db
import datetime


class Hall(db.Model):
    hall_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(250))
    menus = db.relationship('Menu', backref='hall')

    def __init__(self, name):
        self.name = name

    def get_folder_name_format(self):
        # Returns the name formatted as the folder path name
        # Bursley Dining Hall => bursley_dining_hall
        return self.name.lower().replace(" ", "_")

    def get_id(self):
        return str(self.id)

    def add(self):
        db.session.add(self)

    def add_menu(self, menu):
        self.menus.append(menu)

    def delete(self):
        db.session.delete(self)


class Menu(db.Model):
    menu_id = db.Column(db.Integer, primary_key=True, index=True)
    date = db.Column(db.DateTime)
    hall_id = db.Column(db.Integer, db.ForeignKey('hall.hall_id'))
    meals = db.relationship('Meal', backref='menu')

    def __init__(self, date):
        self.date = date

    def get_id(self):
        return str(self.id)

    def load_json(self):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + "/dining_halls_json_data/"
        dir_path = os.path.join(dir_path, self.hall.get_folder_name_format())
        date = datetime.datetime.strftime(self.date, "%Y-%m-%d")
        file_name = os.path.join(dir_path, date + ".json")
        with open(file_name, "r") as file:
            return json.load(file)

    def add_meal(self, meal):
        self.meals.append(meal)

    def add(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)


class Meal(db.Model):
    meal_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(250))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.menu_id'))
    courses = db.relationship('Course', backref='meal')

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return str(self.id)

    def add(self):
        db.session.add(self)

    def add_course(self, course):
        self.courses.append(course)

    def delete(self):
        db.session.delete(self)


class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(250))
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.meal_id'))
    menuitems = db.relationship('MenuItem', backref='course')

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return str(self.id)

    def add(self):
        db.session.add(self)

    def add_menu_item(self, menuitem):
        self.menuitems.append(menuitem)

    def delete(self):
        db.session.delete(self)


class MenuItem(db.Model):
    menuitem_id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(250))
    course_id = db.Column(db.Integer, db.ForeignKey('course.course_id'))
    halal = db.Column(db.Boolean, default=False)

    def __init__(self, name):
        self.name = name

    def get_id(self):
        return str(self.id)

    def add(self):
        db.session.add(self)

    def delete(self):
        db.session.delete(self)

    def __repr__(self):
        """
        Returns a nicely formatted string for printing out a menuitem to the console
        Useful for debugging
        Also demonstrates how we can move upwards through objects to relate a MenuItem
        all the way back to a Dining Hall
        :return: string
        """
        return ('<MenuItem %s for %s at %s>' % (self.name,
                                                self.course.name,
                                                self.course.meal.menu.hall.name))
