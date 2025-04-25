import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QScrollArea, QTextEdit, QLineEdit, QComboBox, QFileDialog
)
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt, QUrl

# Global variable example
global_var = "default_value"

class HomePage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        layout = QVBoxLayout(self)

        # Image on top
        self.image_label = QLabel()
        pixmap = QPixmap("example.jpg")  # Use a real path here
        self.image_label.setPixmap(pixmap.scaledToHeight(400, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)

        # Buttons below image
        self.form_button = QPushButton("Go to Form Page")
        self.search_button = QPushButton("Go to Search Page")
        self.form_button.setFixedHeight(50)
        self.search_button.setFixedHeight(50)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.form_button)
        button_layout.addWidget(self.search_button)

        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)

        self.form_button.clicked.connect(lambda: self.open_page("form"))
        self.search_button.clicked.connect(lambda: self.open_page("search"))

    def open_page(self, page):
        if page == "form":
            self.stacked_widget.setCurrentWidget(self.stacked_widget.form_page)
            self.stacked_widget.parent().setWindowTitle("Form Page")
        elif page == "search":
            self.stacked_widget.setCurrentWidget(self.stacked_widget.search_page)
            self.stacked_widget.parent().setWindowTitle("Search Page")

class FormPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        scroll_area = QScrollArea()
        content_widget = QWidget()
        form_layout = QVBoxLayout(content_widget)
        form_layout.setContentsMargins(20, 20, 20, 20)

        self.fields = {}
        field_names = []
        for i in range(0,17):
            field_names.append("Field_"+str(i))

        #field_names = [
            "Script Name", "Author or Owner", "Revision", "Revision Date", "Revision History",
            "Script Summary", "Script Type", "Script Path", "Projects", "Description",
            "Execution shell", "Pre-run procedure", "Run command", "Input variables",
            "Sample command", "Output", "Known limitations"
        #]

        for name in field_names:
            label = QLabel(name)
            if name in ["Field_10", "Field_12"]:
                input_field = QTextEdit()
                input_field.setFixedHeight(80)
            elif name == "Field_5":
                input_field = QComboBox()
                input_field.addItems(["Python", "Shell", "SQL"])
            else:
                input_field = QLineEdit()

            form_layout.addWidget(label)
            field_container = QHBoxLayout()
            field_container.addWidget(input_field)
            if name == "Field_1":
                check_button = QPushButton("Check Availability")
                field_container.addWidget(check_button)
            form_layout.addLayout(field_container)
            self.fields[name] = input_field

        self.submit_button = QPushButton("Submit")
        self.back_button = QPushButton("Back to Home")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.back_button)
        button_layout.setContentsMargins(0, 0, 20, 0)

        form_layout.addLayout(button_layout)

        scroll_area.setWidget(content_widget)
        scroll_area.setWidgetResizable(True)
        layout = QVBoxLayout(self)
        layout.addWidget(scroll_area)

        self.submit_button.clicked.connect(self.handle_submit)
        self.back_button.clicked.connect(self.go_home)

    def handle_submit(self):
        # Handle form data save here
        print("Form submitted")
        for field in self.fields.values():
            if isinstance(field, (QLineEdit, QTextEdit)):
                field.clear()
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(0)

    def go_home(self):
        self.stacked_widget.setCurrentWidget(self.stacked_widget.home_page)
        self.stacked_widget.parent().setWindowTitle("Home")

class SearchPage(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        layout = QVBoxLayout(self)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search query")
        self.search_button = QPushButton("Search")
        self.result_browser = QTextEdit()
        self.result_browser.setReadOnly(True)
        self.result_browser.setAlignment(Qt.AlignTop)

        self.back_button = QPushButton("Back to Home")

        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.result_browser)
        layout.addWidget(self.back_button)

        self.search_button.clicked.connect(self.perform_search)
        self.back_button.clicked.connect(self.go_home)

    def perform_search(self):
        query = self.search_input.text().strip().replace(" ", ".*")
        file_path = "sample.txt"  # Replace with real path
        if not os.path.exists(file_path):
            self.result_browser.setPlainText("No file to search")
            return

        found = False
        with open(file_path, "r") as f:
            for line in f:
                if re.search(query, line, re.IGNORECASE):
                    found = True
                    break

        if found:
            self.result_browser.setPlainText("Match found!")
        else:
            self.result_browser.setPlainText("No match found.")

    def go_home(self):
        self.search_input.clear()
        self.result_browser.clear()
        self.stacked_widget.setCurrentWidget(self.stacked_widget.home_page)
        self.stacked_widget.parent().setWindowTitle("Home")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home")
        self.resize(800, 735)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_page = HomePage(self.stacked_widget)
        self.form_page = FormPage(self.stacked_widget)
        self.search_page = SearchPage(self.stacked_widget)

        self.stacked_widget.home_page = self.home_page
        self.stacked_widget.form_page = self.form_page
        self.stacked_widget.search_page = self.search_page

        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.form_page)
        self.stacked_widget.addWidget(self.search_page)

        self.stacked_widget.setCurrentWidget(self.home_page)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
