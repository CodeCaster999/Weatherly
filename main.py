import sys, requests
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QWidget, QLabel, 
                             QLineEdit, QPushButton, QVBoxLayout)
import qdarktheme

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
        
        # A button that returns the user back to the main menu
        self.back_button = QPushButton("↩️ Go Back", self)

        # A button that turns on darkmode
        self.dark_mode = QPushButton("🌓", self)    

        # Makes the button checkable so the feature can turn on
        self.dark_mode.setCheckable(True)  

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
        
        top_bar = QHBoxLayout()
        top_bar.addWidget(self.back_button)
        top_bar.addStretch()
        top_bar.addWidget(self.dark_mode)
        
        vbox.addLayout(top_bar)
        
        # Orgianizing the widgets into columns
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.display_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        
        # Arranging some of the widgets horizontally
        self.city_label.setAlignment(Qt.AlignLeft)
        self.city_input.setAlignment(Qt.AlignLeft)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        # Object names for widgets
        self.back_button.setObjectName("back_button")
        self.dark_mode.setObjectName("dark_mode")    
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.display_weather_button.setObjectName("display_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Toggles between the dark and light themes
        self.dark_mode.toggled.connect(self.toggle_theme)
        
        # Applying CSS style sheet
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: calibri;
            }
            QPushButton#back_button {
                font-size: 20px
            }
            QPushButton#dark_mode {
                font-size: 20px
            }
            QLabel#city_label {
                font-size: 40px;
                margin-top: 40px;
            }
            QLineEdit#city_input {
                font-size: 40px;
                margin-bottom: 40px;
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
            
            # For dev purposes
            print(data)
            
            # Check if API returned a successful status code in the JSON payload
            if data["cod"] == 200:
                self.display_weather(data)
                self.display_weather_desc(data)
                
        # Handle HTTP errors triggered by raise_for_status()        
        except requests.exceptions.HTTPError as http_error:
            
            # Match specific HTTP status codes for more user-friendly error messages
            match response.status_code:
                case 400:
                    self.display_error("Error Code: 400\nBad request\nPlease check your input")
                case 401:
                    self.display_error("Error Code: 401\nUnauthorized\nInvalidate API key")
                case 403:
                    self.display_error("Error Code: 403\nForbidden\nAccess is denied")
                case 404:
                    self.display_error("Error Code: 404\nNot found\nPlease check your input")
                case 500:
                    self.display_error("Error Code: 500\nInternal server error\nPlease try again later")
                case 502:
                    self.display_error("Error Code: 502\nBad Gateway\nInvaid response from the server")
                case 503:
                    self.display_error("Error Code: 503\nService Unvaliable\nServer is down")
                case 504:
                    self.display_error("Error Code: 504\nGateway timeout\nNo response from the server")
                case _:
                    self.display_error(f"An HTTP error occured\n{http_error}")
        
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        
        # Catch any other request-related issues (connection errors, timeouts, etc.)        
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")
    
    # Display the error on the interface using the temperature_label widget
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        
        # Clears up the interface from these widgets if the city name is not on the input
        self.emoji_label.clear()
        self.description_label.clear()
    
    # Display the weather on the interface using the temperature_label widget
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_f = (temperature_k * 9/5) - 459.67
        
        # Used as an argument for the display_weather_emoji function
        weather_id = data["weather"][0]["id"]
        
        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.display_weather_emoji(weather_id))
    
    # Display the weather description on the interface using the description_label widget
    def display_weather_desc(self, data):
        weather_desc = data["weather"][0]["description"]
        self.description_label.setText(weather_desc)
        
    def toggle_theme(self, checked):
        if checked:
            qdarktheme.setup_theme("dark")
        else:
            qdarktheme.setup_theme("light")
    
    # Displays weather emojis on the interface using the weather the emoji_label widget
    @staticmethod
    def display_weather_emoji(weather_id):
        # Thunderstorm
        if 200 <= weather_id <= 232:
            return "⛈️"

        # Drizzle
        elif 300 <= weather_id <= 321:
            return "🌦️"

        # Rain
        elif 500 <= weather_id <= 504:
            return "🌧️"
        elif weather_id == 511:
            return "🌨️"  # freezing rain
        elif 520 <= weather_id <= 531:
            return "🌧️"

        # Snow
        elif 600 <= weather_id <= 622:
            return "❄️"

        # Atmosphere (mist, fog, etc)
        elif 701 <= weather_id <= 781:
            return "🌫️"

        # Clear
        elif weather_id == 800:
            return "☀️"

        # Clouds
        elif weather_id == 801:
            return "🌤️"
        elif weather_id == 802:
            return "⛅"
        elif weather_id in (803, 804):
            return "☁️"

        # Fallback
        else:    
            return "❓"

    
            
if __name__ == "__main__":

    # Create the application (handles GUI events)
    app = QApplication(sys.argv)

    # Apply dark theme.
    qdarktheme.setup_theme('light')
    
    # Create and display the main window
    weather_app = WeatherApp()
    weather_app.show()
    
    # Start the event loop (runs until the window is closed)
    sys.exit(app.exec_())
