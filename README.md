# Perth Regional Weather Map 
This website aims to help people make travel plans by providing visualization of weather in reginal areas. Users could import weather data and easily find places with appealing weathers.


## Contributor:
- 24576325 Canaan Guo github:bilibilistack
- 24176913 Changjiang Zhang  github:chanale
- 24257061 Marcus Zhou github:MarcusZhou-2024
- 24563207 Wendy Song github:WendySong1

## Project Structure

```
CITS5505Group3/
├── app/                            # Main application folder
│   ├── __init__.py                 # Initializes the Flask app, database, and CSRF protection
│   ├── routes.py                   # Defines the main routes for the application
│   ├── models.py                   # Contains database models (e.g., User model)
│   ├── auth_routes.py              # Handles authentication-related routes (e.g., login, logout)
│   ├── templates/                  # HTML templates for rendering views
│   │   ├── base.html               # Base template with shared layout (header, sidebar, footer)
│   │   ├── homechart.html          # Template for the weather visualization page
│   │   ├── upload.html             # Template for the file upload page
│   │   ├── intro.html              # Template for the introduction page before login
│   │   ├── share.html              # Template for the sharing page
│   │   ├── login.html              # Template for the login page
│   │   ├── register.html           # Template for the register page
│   │   ├── redirect.html           # Template for the redirect page
│   ├── static/                     # Static files (CSS, JavaScript, images)
│   │   ├── chart/                  # Static files for the weather visualization page
│   │   │   ├── resources/          # icon library
│   │   │   ├── homechart.css       # Styles for the weather visualization page
│   │   │   ├── homechart.js        # JavaScript for the weather visualization page
│   │   │   ├── leaflet.css         # Leaflet library styles for maps
│   │   │   ├── leaflet.js          # Leaflet library JavaScript for maps
│   │   │   ├── base.css            # Shared styles for the entire application
│   │   ├── login/                  # Static files for the login page
│   │   │   ├── login.css           # Styles for the login page
│   │   │   ├── home.js             # JavaScript for login and registration
│   │   │   ├── intro.css           # Styles for the intro page
│   │   │   ├── register.css        # Styles for the registration page
│   │   │   ├── main.css            # Styles for the login and registration page
│   │   ├── share/                  # Static files for the share page
│   │   │   ├── share.css           # Styles for the share page
│   │   │   ├── share.js            # JavaScript for handling share
│   │   ├── upload/                 # Static files for the file upload page
│   │   │   ├── upload.css          # Styles for the file upload page
│   │   │   ├── upload.js           # JavaScript for handling file uploads
│   ├── config.py                   # Configuration file for the Flask app (e.g., database settings)
│   ├── instance/                   # Folder for SQLite database and instance-specific files
│       ├── application.db          # SQLite database file, will be generated but excluded from git
├── demo/                           # Demo folder for testing or showcasing the app
│   ├── app.py                      # Entry point for running the demo application
│   ├── README.md                   # Instructions for running the demo
├── README.md                       # Project overview and instructions for running the application
├── load_demo_data.py               # Clean database and load demo user, city and weather data
├── start_server.py                 # Start server using python start_server.py
├── .gitignore                      # Specifies files and folders to ignore in version control
```


## instructions for how to launch the application



1. Install python 3.13.
2. Create your python environment and activate (optional)：
```
python -m venv application-env
cd application-env/Scripts
activate.bat(cmd) or activate.ps1(powershell) or activate(bash)
```
3. Install required modules:
```
pip install flask flask-Migrate Flask-SQLAlchemy WTForms

```

4. In your project root directory, run:

```
python start_server.py
```

Once the server is running, open your browser and visit:

http://127.0.0.1:5000


Press CTRL+C to quit

![Homepage](introduction_images/Homepage.png)





##TODO:
instructions for how to run the tests for the application.

