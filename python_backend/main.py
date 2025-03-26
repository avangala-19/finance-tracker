from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import openpyxl

# Initialize the Flask application
app = Flask(__name__, template_folder="template", static_folder="static")
  # Change this to a secure secret key

# Temporary in-memory storage for transactions
transactions = []  # List to store transaction data
balance = 0.00  # Variable to track the total balance (with 2 decimal places)
transaction_id_counter = 1  # Counter to ensure unique transaction IDs

@app.route("/")
def index():
    """Render the homepage with the current transactions and balance."""
    return render_template("index.html", transactions=transactions, balance=balance)

@app.route("/add", methods=["POST"])
def add_transaction():
    """Handle adding a new transaction."""
    global balance, transaction_id_counter
    # Retrieve form data from the submitted request
    date = request.form["date"]
    try:
        amount = float(request.form["amount"])  # Allow decimals directly
        if amount <= 0 or round(amount, 2) != amount:
            raise ValueError("Amount must be positive and have up to two decimal places.")
    except ValueError:
        return "Error: Please enter a valid positive amount with up to two decimal places."

    category = request.form["category"]

    # Define income categories to determine if it's an income or expense
    income_categories = {"salary", "investments", "gifts", "other_income"}

    # Update the balance: Add for income, subtract for expenses
    balance = round(balance + (amount if category in income_categories else -amount), 2)

    # Store the new transaction in the list
    transactions.append({
        "id": transaction_id_counter,  # Assign a unique ID
        "date": date,
        "amount": amount,
        "category": category,
        "type": "income" if category in income_categories else "expense"
    })
    transaction_id_counter += 1  # Increment ID for the next transaction

    return redirect(url_for("index"))  # Redirect back to homepage

@app.route("/delete", methods=["POST"])
def delete_transaction():
    """Handle deleting a transaction and adjusting the balance."""
    global balance
    transaction_id = int(request.form["transaction_id"])  # Get the transaction ID from form data

    # Find the transaction by ID and remove it
    for i, transaction in enumerate(transactions):
        if transaction["id"] == transaction_id:
            income_categories = {"salary", "investments", "gifts", "other_income"}

            # Reverse the balance adjustment for the deleted transaction
            balance -= transaction["amount"] if transaction["category"] in income_categories else -transaction["amount"]

            transactions.pop(i)  # Remove the transaction from the list
            break  # Exit loop after finding and deleting the transaction

    return redirect(url_for("index"))  # Redirect back to homepage

@app.route("/filter", methods=["GET"])
def filter():
    global balance
    # Get filter values from the form
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    category = request.args.get('category')

    # Filter logic
    filtered_transactions = transactions

    if start_date:
        filtered_transactions = [
            t for t in filtered_transactions if t['date'] >= start_date
        ]

    if end_date:
        filtered_transactions = [
            t for t in filtered_transactions if t['date'] <= end_date
        ]

    if category and category != '':
        filtered_transactions = [
            t for t in filtered_transactions if t['category'] == category
        ]

    return render_template("index.html", transactions=filtered_transactions, balance=balance, active_tab="history")

@app.route('/get-summary')
def get_summary():
    """Return a summary of income, expenses, and net balance as JSON."""
    from datetime import datetime, timedelta

    period = request.args.get('period', 'all')
    income_categories = {"salary", "investments", "gifts", "other_income"}

    # Filter transactions based on time period
    filtered_transactions = transactions
    if period != 'all':
        today = datetime.now()
        if period == 'month':
            start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        elif period == '2weeks':
            start_date = (today - timedelta(days=14)).strftime('%Y-%m-%d')
        elif period == 'week':
            start_date = (today - timedelta(days=7)).strftime('%Y-%m-%d')

        filtered_transactions = [t for t in transactions if t['date'] >= start_date]

    # Calculate total income and total expenses
    total_income = sum(t['amount'] for t in filtered_transactions if t['category'] in income_categories)
    total_expense = sum(t['amount'] for t in filtered_transactions if t['category'] not in income_categories)
    net_balance = total_income - total_expense  # Calculate net balance

    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": net_balance
    })

@app.route('/download-summary')
def download_summary():
    """Generate and download the Excel summary report."""
    income_categories = {"salary", "investments", "gifts", "other_income"}

    # Create a new Excel workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Summary Report"

    # Write header row
    ws.append(["Category", "Amount"])

    # Calculate and write income and expense totals
    total_income = sum(t['amount'] for t in transactions if t['category'] in income_categories)
    total_expense = sum(t['amount'] for t in transactions if t['category'] not in income_categories)
    net_balance = total_income - total_expense

    # Write totals to the Excel sheet
    ws.append(["Total Income", total_income])
    ws.append(["Total Expense", total_expense])
    ws.append(["Net Balance", net_balance])

    # Save the file temporarily
    temp_file = "temp_summary.xlsx"
    wb.save(temp_file)
    
    # Send the file and then remove it
    from flask import send_file
    import os
    response = send_file(
        temp_file,
        as_attachment=True,
        download_name="finance_summary.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # Delete the temporary file after sending
    os.remove(temp_file)
    return response

@app.route("/chatbot", methods=["POST"])
def chatbot():
    prompt = request.form.get("prompt").strip().lower()

    if not prompt:
        return jsonify({"response": "Invalid prompt."})

    if "spending the most money on" in prompt:
        expense_totals = {}
        for t in transactions:
            if t["category"] not in {"salary", "investments", "gifts", "other_income"}:
                expense_totals[t["category"]] = expense_totals.get(t["category"], 0) + t["amount"]
        category = max(expense_totals, key=expense_totals.get, default="No data")
        return jsonify({"response": f"You're spending the most on {category}."})

    elif "biggest source of " in prompt:
        income_totals = {cat: 0 for cat in ["salary", "investments", "gifts", "other_income"]}
        for t in transactions:
            if t["category"] in income_totals:
                income_totals[t["category"]] += t["amount"]
        biggest_income = max(income_totals, key=income_totals.get, default="No data")
        return jsonify({"response": f"Your biggest income source is {biggest_income}."})

    elif "highest expense in a single transaction" in prompt:
        highest_expense = max((t for t in transactions if t["category"] not in {"salary", "investments", "gifts", "other_income"}),
                              key=lambda x: x["amount"],
                              default=None)
        if highest_expense:
            return jsonify({"response": f"Your highest expense was ${highest_expense['amount']} on {highest_expense['category']}."})
        else:
            return jsonify({"response": "No expense data available."})

    elif "category has the most transactions" in prompt:
        category_counts = {}
        for t in transactions:
            category_counts[t["category"]] = category_counts.get(t["category"], 0) + 1
        most_common_category = max(category_counts, key=category_counts.get, default="No data")
        return jsonify({"response": f"The category with the most transactions is {most_common_category}."})

    else:
        return jsonify({"response": "I'm not sure how to answer that. Try asking about spending patterns, income sources, or transaction details."})

# Run the application on port 8080 with debugging enabled
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)