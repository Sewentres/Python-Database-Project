import sqlite3
from PyQt5 import QtWidgets, QtGui

db_name_sql = "DATABASE"


class ShowData(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 500)
        self.setWindowTitle("Show Data")

        self.table = QtWidgets.QTableWidget(self)
        self.table.setRowCount(10)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            [
                "First Name",
                "Last Name",
                "Email",
                "Phone",
                "Country",
                "City",
                "Street",
                "Zip",
            ]
        )
        self.table.resize(380, 450)
        self.table.move(10, 10)

        self.show_data()

    def show_data(self):
        conn = sqlite3.connect(db_name_sql + ".db")
        c = conn.cursor()

        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(val))
        conn.close()


import os


class CreateDB(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.db_name = db_name_sql
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 500)
        self.setWindowTitle("Create Database")

        self.first_name = QtWidgets.QLineEdit(self)
        self.first_name.move(140, 80)

        first_name_label = QtWidgets.QLabel("First Name:", self)
        first_name_label.move(10, 80)

        self.last_name = QtWidgets.QLineEdit(self)
        self.last_name.move(140, 110)

        last_name_label = QtWidgets.QLabel("Last Name:", self)
        last_name_label.move(10, 110)

        self.email = QtWidgets.QLineEdit(self)
        self.email.move(140, 140)

        email_label = QtWidgets.QLabel("Email:", self)
        email_label.move(10, 140)

        self.phone = QtWidgets.QLineEdit(self)
        self.phone.move(140, 170)

        phone_label = QtWidgets.QLabel("Phone:", self)
        phone_label.move(10, 170)

        self.country = QtWidgets.QLineEdit(self)
        self.country.move(140, 200)

        country_label = QtWidgets.QLabel("Country:", self)
        country_label.move(10, 200)

        self.city = QtWidgets.QLineEdit(self)
        self.city.move(140, 230)

        city_label = QtWidgets.QLabel("City:", self)
        city_label.move(10, 230)

        self.street = QtWidgets.QLineEdit(self)
        self.street.move(140, 260)

        street_label = QtWidgets.QLabel("Street:", self)
        street_label.move(10, 260)

        self.zip = QtWidgets.QLineEdit(self)
        self.zip.move(140, 290)

        zip_label = QtWidgets.QLabel("Zip:", self)
        zip_label.move(10, 290)

        create_btn = QtWidgets.QPushButton("Create", self)
        create_btn.move(150, 330)
        create_btn.clicked.connect(self.create_database)

        show_data_btn = QtWidgets.QPushButton("Show Data", self)
        show_data_btn.move(250, 330)
        show_data_btn.clicked.connect(self.show_data_view)

        self.show()

    def create_database(self):
        if not os.path.isfile(self.db_name + ".db"):
            conn = sqlite3.connect(self.db_name + ".db")
            c = conn.cursor()

            c.execute(
                """CREATE TABLE users
                         (first_name text, last_name text, email text, phone text, country text, city text, street text, zip text)"""
            )
            conn.commit()
            conn.close()

            self.first_name_val = self.first_name.text()
            self.last_name_val = self.last_name.text()
            self.email_val = self.email.text()
            self.phone_val = self.phone.text()
            self.country_val = self.country.text()
            self.city_val = self.city.text()
            self.street_val = self.street.text()
            self.zip_val = self.zip.text()

            self.insert_data()
        else:
            self.insert_data()

    def insert_data(self):
        conn = sqlite3.connect(self.db_name + ".db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO users (first_name, last_name, email, phone, country, city, street, zip) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                self.first_name.text(),
                self.last_name.text(),
                self.email.text(),
                self.phone.text(),
                self.country.text(),
                self.city.text(),
                self.street.text(),
                self.zip.text(),
            ),
        )
        conn.commit()
        conn.close()

    def show_data_view(self):
        self.show_data_window = ShowData()
        self.show_data_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    create_db = CreateDB()
    app.exec_()
