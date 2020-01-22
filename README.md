# Spicy Stores

## Installation

Set up your virtual environment. The easiest way to do this is with the following command:

    python -m venv .venv

This will establish a virtual environment in the .venv folder. In order to do this you will need `python3` and `python3-venv` installed.

Activate the virtual environment:

(On Linux):

    source .venv/bin/activate

(On Windows):

    .venv\Scripts\activate.bat

Install the requirements:

    pip install -r requirements.txt

On Linux, in order to do this you will need `python3-pip` installed.

## Building the customer site

Node.JS is required to build the customer site. 

Run `build-customer` in a terminal in order to build.

## Running the application

    python manage.py runserver
