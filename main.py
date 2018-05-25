from PyQt5.QtWidgets import QApplication
import sys

# Local Module Imports
import app_framework as af

# Create GUI application
app = QApplication(sys.argv)
form = af.MyApp()
form.show()
app.exec_()
