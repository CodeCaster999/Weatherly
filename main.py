import sys, requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout)

"""
Widget	        Purpose
---------------------------------------------------
QApplication	Controls the entire app (required)
QWidget	        Base window class
QLabel	        Displays text
QLineEdit	    Input box
QPushButton	    Button
QVBoxLayout	    Vertical layout (organizes widgets)
"""

from PyQt5.QtCore import Qt

# Main application window (inherits from QWidget)
class WeatherApp(QWidget):
    def __init__(self):
        # Initialize the base QWidget
        super().__init__()
        # Label prompting the user to enter a city name
        self.city_label = QLabel("Enter city name:", self)

        # Text input for the user to enter a city name
        self.city_input = QLineEdit(self)

        # Button to trigger weather data retrieval
        self.display_weather_button = QPushButton("Display Weather", self)
        
        # Weather display elements
        self.temperature_label = QLabel("70*F", self)
        self.emoji_label = QLabel(": )", self)
        self.description_label = QLabel("Sunny", self)
        
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Weatherly")
        
        vbox = QVBoxLayout()
        
        # Orgianizing the widgets into columns
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.display_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        # Arranging some of the widgets horizontally
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        # Object names for widgets
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.display_weather_button.setObjectName("display_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        
        # Applying CSS style sheet
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 40px;
            }
            QPushButton#get_weatehr_button {
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label {
                font-size: 75px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label {
                font-size: 50px;
            }
            
        """)
        
if __name__ == "__main__":
    # Create the application (handles GUI events)
    app = QApplication(sys.argv)
    
    # Create and display the main window
    weather_app = WeatherApp()
    weather_app.show()
    
    # Start the event loop (runs until the window is closed)
    sys.exit(app.exec_())
