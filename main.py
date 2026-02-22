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
        self.city_name = QLabel("Enter city name:", self)

        # Text input for the user to enter a city name
        self.city_input = QLineEdit(self)

        # Button to trigger weather data retrieval
        self.display_weather_button = QPushButton("Display Weather", self)
        
        # Weatehr display elements
        self.temperature_label = QLabel("70*F", self)
        self.emoji_label = QLabel(": )", self)
        self.description_label = QLabel("Sunny", self)
        
        
if __name__ == "__main__":
    # Create the application (handles GUI events)
    app = QApplication(sys.argv)
    
    # Create and display the main window
    weather_app = WeatherApp()
    weather_app.show()
    
    # Start the event loop (runs until the window is closed)
    sys.exit(app.exec_())
