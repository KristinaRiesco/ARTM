# ARTM – Augmented Reality Triggered Macros

ARTM (Augmented Reality Triggered Macros) is a local desktop application designed to provide accessible interaction through real-time hand gesture recognition. Developed in Python, ARTM uses a PyQt5 frontend, a Python backend, and a local SQLite database to help users trigger predefined system actions without the need for a keyboard or mouse.

## Features

- Real-time gesture recognition using OpenCV and MediaPipe  
- Predefined gestures trigger system actions such as notifications and URL opening  
- Secure local user authentication with password hashing  
- PyQt5-based graphical interface  
- SQLite database managed with SQLAlchemy ORM  
- Completely offline architecture with no network dependency  

## Architecture

- Frontend: PyQt5  
- Backend: Local Python services  
- Database: SQLite with SQLAlchemy ORM  
- Gesture Processing: MediaPipe and OpenCV  

## Project Structure

ARTM/  
├── main.py                      – Application entry point  
├── ARTM.py                      – Main GUI class and page controller  
├── style.qss                    – Custom Qt stylesheet  
│  
├── backend/  
│   ├── core/  
│   │   ├── config.py            – Global config settings (e.g., DB URI)  
│   │   ├── database.py          – Initializes the SQLite database  
│   │   └── extensions.py        – SQLAlchemy and Bcrypt instances  
│   │  
│   ├── models/  
│   │   ├── gestures.py          – Gesture table model  
│   │   └── user.py              – User table model  
│   │  
│   └── services/  
│       ├── gesture_service.py   – Gesture logic and mappings  
│       └── user_service.py      – Registration, login, and profile logic  
│  
├── pages/  
│   ├── Gesture_Capture_Page.py  
│   ├── Gesture_Creation_Page.py  
│   ├── Gesture_Recognition.py  
│   ├── gesture_utils.py  
│   ├── Home_Page.py  
│   ├── Login_Page.py  
│   ├── Register_Page.py  
│   ├── Profile_Page.py  
│   └── Settings_Page.py  
│  
├── migrations/  
│   ├── env.py  
│   ├── script.py.mako  
│   └── versions/  
│  
├── Not Code/  
│   ├── ARTM Flowchart-Whiteboard.jpg  
│   └── ARTM Updated Flowchart-Whiteboard.jpg  
│  
├── site.db                      – SQLite database file  
├── requirements.txt             – Python dependencies  
├── README.md                    – Project documentation  
├── .gitignore                   – Ignored files and folders  

## Setup Instructions

1. Clone the repository:

git clone https://github.com/your-username/ARTM.git  
cd ARTM

2. Create a virtual environment:

python -m venv env  
source env/bin/activate   (On Windows: env\Scripts\activate)

3. Install dependencies:

pip install -r requirements.txt

If no requirements.txt exists, install manually:

pip install PyQt5 opencv-python mediapipe flask flask_sqlalchemy flask_bcrypt

4. Run the application:

python main.py

This will launch the application, initialize the SQLite database, and open the login interface.

## How It Works

- At startup, the app creates a Flask application context to enable SQLAlchemy and Bcrypt functionality.  
- Users can register and log in locally. Passwords are hashed and stored in the SQLite database.  
- Once logged in, users are directed to functional pages where gestures are captured and interpreted.  
- Predefined gestures are recognized using MediaPipe and matched with system-level responses.

## Security

- All user passwords are hashed using Bcrypt before being stored  
- Data is stored locally in a SQLite database  
- No user data is sent or stored remotely  

## Contributors

Kristina Riesco – Backend Developer
- Designed and implemented the local Python backend architecture
- Built and integrated the SQLite database using SQLAlchemy ORM
- Developed backend services for user authentication and gesture-to-action mapping
- Integrated gesture recognition with system-level responses
- Contributed to frontend development and predefined gesture creation

Kyle McGuinness – Frontend Developer + Project Manager
- Designed the PyQt5 user interface and layout
- Implemented page navigation and user interaction flow
- Developed login, registration, and settings pages
- Contributed to predefined gesture creation and overall app design
  
Cole Talarek – Gesture Developer
- Defined and tested the predefined gesture set used in the application
- Worked on custom gesture creation (later deprecated) and MediaPipe integration
- Supported frontend development and camera interaction logic


Sacred Heart University – Senior Capstone Program  
Built with: PyQt5, OpenCV, MediaPipe, Flask-SQLAlchemy  

## License

This project is licensed under the MIT License. See LICENSE for details.
