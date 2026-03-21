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
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        
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
            QPushButton#display_weather_button {
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
        
        # Shows the weather when the "Display Weather" button is clicked
        self.display_weather_button.clicked.connect(self.get_weather)
    
    def get_weather(self):
        
        api_key = "e6a0b10d1a364100c0cd0a82da65567c"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            # Send a GET request to the API
            response = requests.get(url)
            
            # Raise an exception for HTTP error responses (4xx, 5xx)
            response.raise_for_status()
            
            # Parse the response JSON into a Python dictionary
            data = response.json()
            
            # Check if API returned a successful status code in the JSON payload
            if data["cod"] == 200:
                self.display_weather(data)
                
        # Handle HTTP errors triggered by raise_for_status()        
        except requests.exceptions.HTTPError as http_error:
            
            # Match specific HTTP status codes for more user-friendly error messages
            match response.status_code:
                case 400:
                    print("Error Code: 400\nBad request\nPlease check your input")
                case 401:
                    print("Error Code: 401\nUnauthorized\nInvalidate API key")
                case 403:
                    print("Error Code: 403\nForbidden\nAccess is denied")
                case 404:
                    print("Error Code: 404\nNot found\nPlease check your input")
                case 500:
                    print("Error Code: 500\nInternal server error\nPlease try again later")
                case 502:
                    print("Error Code: 502\nBad Gateway\nInvaid response from the server")
                case 503:
                    print("Error Code: 503\nService Unvaliable\nServer is down")
                case 504:
                    print("Error Code: 504\nGateway timeout\nNo response from the server")
                case _:
                    print(f"An HTTP error occured\n{http_error}")
        
        except requests.exceptions.ConnectionError:
            print("Connection Error:\nPlease check your internet connection before proceeding")
        
        except requests.exceptions.Timeout:
            print("Timeout Error:\nThe request timed out")
        
        except requests.exceptions.ToomanyRedirects:
            print("Too many Redirects:\nPlease check the URL before proceeding")
        
        # Catch any other request-related issues (connection errors, timeouts, etc.)        
        except requests.exceptions.RequestException as req_error:
            print(f"Request Error:\n{req_error}")
    
    def display_error(self, message):
        pass
    
    def display_weather(self, data):
        print(data)
            
if __name__ == "__main__":
    # Create the application (handles GUI events)
    app = QApplication(sys.argv)
    
    # Create and display the main window
    weather_app = WeatherApp()
    weather_app.show()
    
    # Start the event loop (runs until the window is closed)
    sys.exit(app.exec_())
