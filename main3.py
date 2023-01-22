import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets
import os

# Create SQLite database and table
if os.path.exists("mydatabase.db"):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
else:
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE contacts
                    (Name TEXT, Surname TEXT, Address TEXT, City TEXT, Phone_Number TEXT, Email TEXT)"""
    )
    conn.commit()

# GUI using QT5
class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Add data button
        self.add_button = QtWidgets.QPushButton("Add Data", self)
        self.add_button.clicked.connect(self.addData)

        # Delete data button
        self.delete_button = QtWidgets.QPushButton("Delete Data", self)
        self.delete_button.clicked.connect(self.deleteData)

        # Search data button
        self.search_button = QtWidgets.QPushButton("Search Data", self)
        self.search_button.clicked.connect(self.searchData)

        # View all data button
        self.view_button = QtWidgets.QPushButton("View All Data", self)
        self.view_button.clicked.connect(self.viewData)

        # Add new table button
        self.new_table_button = QtWidgets.QPushButton("Add New Table", self)
        self.new_table_button.clicked.connect(self.addNewTable)

        # Add new table button
        self.show_contact_button = QtWidgets.QPushButton("Show Contacts", self)
        self.show_contact_button.clicked.connect(self.showContactInformation)

        # Add buttons to layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.add_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.view_button)
        layout.addWidget(self.new_table_button)
        layout.addWidget(self.show_contact_button)

        # Create central widget and set layout
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def addData(self):
        # Create input dialogs to get user input for each column
        name, ok = QtWidgets.QInputDialog.getText(self, "Add Data", "Enter Name:")
        if ok:
            surname, ok = QtWidgets.QInputDialog.getText(
                self, "Add Data", "Enter Surname:"
            )
        if ok:
            address, ok = QtWidgets.QInputDialog.getText(
                self, "Add Data", "Enter Address:"
            )
        if ok:
            city, ok = QtWidgets.QInputDialog.getText(self, "Add Data", "Enter City:")
        if ok:
            phone_number, ok = QtWidgets.QInputDialog.getText(
                self, "Add Data", "Enter Phone Number:"
            )
        if ok:
            email, ok = QtWidgets.QInputDialog.getText(self, "Add Data", "Enter Email:")
        if ok:
            # Insert the data into the 'contacts' table
            cursor.execute(
                "INSERT INTO contacts (Name, Surname, Address, City, Phone_Number, Email) VALUES (?,?,?,?,?,?)",
                (name, surname, address, city, phone_number, email),
            )
            conn.commit()

    def deleteData(self):
        # Get the ID of the record to delete
        id, ok = QtWidgets.QInputDialog.getInt(
            self, "Delete Data", "Enter the ID of the record to delete:"
        )
        if ok:
            # Delete the record with the specified ID from the 'contacts' table
            cursor.execute("DELETE FROM contacts WHERE id=?", (id,))
            conn.commit()

    def searchData(self):
        # Get the search term and column name
        search_term, ok = QtWidgets.QInputDialog.getText(
            self, "Search Data", "Enter the search term:"
        )
        if ok:
            column_name, ok = QtWidgets.QInputDialog.getItem(
                self,
                "Search Data",
                "Select the column to search:",
                ["Name", "Surname", "Address", "City", "Phone Number", "Email"],
            )
        if ok:
            # Search the 'contacts' table for records with the specified search term in the specified column
            cursor.execute(
                f"SELECT * FROM contacts WHERE {column_name} LIKE ?",
                (f"%{search_term}%",),
            )
            search_results = cursor.fetchall()

        # Create a new window to display the search results
        search_results_window = QtWidgets.QDialog(self)
        search_results_window.setWindowTitle("Search Results")

        # Create a table widget to display the search results
        table = QtWidgets.QTableWidget(search_results_window)
        table.setRowCount(len(search_results))
        table.setColumnCount(len(search_results[0]))
        table.setHorizontalHeaderLabels(
            ["Name", "Surname", "Address", "City", "Phone Number", "Email"]
        )

        # Populate the table with the search results
        for i, d in enumerate(search_results):
            for j, value in enumerate(d):
                table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

        # Create a layout for the window and add the table to it
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(table)
        search_results_window.setLayout(layout)

        # Show the window
        search_results_window.exec_()

    def viewData(self):
        # Retrieve all data from the 'contacts' table
        cursor.execute("SELECT * FROM contacts")
        data = cursor.fetchall()

        # Create a new window to display the data
        view_data_window = QtWidgets.QDialog(self)
        view_data_window.setWindowTitle("View Data")

        # Create a table widget to display the data
        table = QtWidgets.QTableWidget(view_data_window)
        table.setRowCount(len(data))
        table.setColumnCount(len(data[0]))
        labels = list(map(lambda x: x[0], cursor.description))
        table.setHorizontalHeaderLabels(labels)

        # Populate the table with the data
        for i, d in enumerate(data):
            for j, value in enumerate(d):
                table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

        # Create a layout for the window and add the table to it
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(table)
        view_data_window.setLayout(layout)

        # Show the window
        view_data_window.exec_()

    def addNewTable(self):
        # Get the name of the new table
        table_name, ok = QtWidgets.QInputDialog.getText(
            self, "Add New Table", "Enter the name of the new table:"
        )
        if ok:
            # Create the new table with the specified name
            cursor.execute(f"ALTER TABLE contacts ADD {table_name}")
            conn.commit()

    def showContactInformation(self):
        # Retrieve all data from the 'contacts' table
        cursor.execute("SELECT * FROM contacts")
        data = cursor.fetchall()

        # Create a new window to display the data
        view_contact_information_window = QtWidgets.QDialog(self)
        view_contact_information_window.setWindowTitle("View Data")
        layout = QtWidgets.QVBoxLayout()
        view_contact_information_window.exec_()


app = QtWidgets.QApplication([])
window = MyApp()
window.show()
app.exec_()
