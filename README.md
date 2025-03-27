# CloudCash
This finance tracker, named CloudCash, is a web application designed to help users manage their personal finances.

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
cd finance-tracker

**Install the required dependencies:**
pip install flask openpyxl datetime io

**Usage**
Run the application: python main.py
Open your browser and visit http://localhost:8080

**Libraries Used**
Flask: Web framework for handling routes and requests.
openpyxl: For generating Excel reports.
datetime: For date handling and filtering logic.
Chart.js: Creating bar graph visual using JavaScript
