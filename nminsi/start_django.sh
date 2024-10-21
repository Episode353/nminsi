#!/bin/bash
# Open a new terminal window and run the Django server

# Change to the directory where your manage.py file is located
cd /home/mike/Documents/GitHub/nminsi/nminsi

# Open a new terminal and run the Django server
lxterminal -e "python manage.py runserver 0.0.0.0:8000"
