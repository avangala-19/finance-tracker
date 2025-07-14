# CloudCash
This finance tracker, named CloudCash, is a web application designed to help users manage their personal finances. **Still in development

It allows users to:
Add income and expense transactions.
Filter transactions by date and category.
Track their balance, income, & expenses over last week, month, etc. along with dynamically updating visual bar graph
Generate a downloadable summary report in Excel format.
Use simple question & answer code to analyze spending patterns and answer questions based on them personalized to the user.
Input validation for income & expense entry, checks both syntactical and semantic errors.

**Installation (Github)**
Clone the repository:
git clone <repository-url>
Navigate to the project folder:
cd workspaces/finance-tracker

## Setup Instructions

1. Create a virtual environment named `venv`:

   python3 -m venv venv

Activate the virtual environment:

macOS/Linux:
source venv/bin/activate

Windows (PowerShell):
.\venv\Scripts\Activate.ps1

Windows (Command Prompt):
.\venv\Scripts\activate.bat

**Install the required dependencies:**
pip install flask openpyxl datetime

Run the program
python main.py

Option 2 (using Flask CLI):
macOS/Linux:
export FLASK_APP=app.py
export FLASK_ENV=development
flask run

Windows (PowerShell):
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run

Windows (Command Prompt):
set FLASK_APP=app.py
set FLASK_ENV=development
flask run




**Usage**
Run the application: python main.py
Open your browser and visit http://localhost:8080

**Libraries Used**
Flask: Web framework for handling routes and requests.
openpyxl: For generating Excel reports.
datetime: For date handling and filtering logic.
Chart.js: Creating a bar graph visual using JavaScript
