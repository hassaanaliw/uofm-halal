import unittest

import os
from flask_testing import TestCase

from halal import app, api, data, database, db, models


class DatabaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///halal_test.db"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///halal_test.db"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_db_create(self):
        # Tests if the database was created successfully
        self.assertTrue(os.path.exists("halal/halal_test.db"))

    def test_db_structure(self):
        # Tests if all the tables have been created successfully
        tables = ['course', 'hall', 'meal', 'menu', 'menu_item']
        actual_tables = db.engine.table_names()
        self.assertEqual(tables, actual_tables)

    def test_build_halls_menus(self):
        # Tests if the creating halls and menus method works correctly
        database.create_all_halls()
        halls = models.Hall.query.filter(models.Hall.name == "Bursley Dining " \
                                                             "Hall").all()

        self.assertTrue(len(halls) > 0)

        # Tests if the creating menus method works correctly
        database.create_all_menus()
        menus = models.Menu.query.all()
        self.assertTrue(len(menus) > 0)


if __name__ == '__main__':
    unittest.main()
