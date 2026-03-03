from collections import defaultdict
import csv
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
FILENAME = SCRIPT_DIR / 'expenses.csv'


def collect_expenses() -> list[dict]:
    """
    Interactively collects expense data from the user via the terminal.
    Returns a list of dictionaries containing 'Category' and 'Amount'.
    """
    expenses = []

    while True:
        print("\n--- Add New Expense (type 'stop' to finish) ---")
        # Normalize input to lowercase and remove extra whitespace
        category = input("Category: ").strip().lower()

        if category == "stop":
            break

        try:
            amount = float(input("Amount: "))
            # Basic validation to ensure financial data makes sense
            if amount < 0:
                print("Amount cannot be negative.")
                continue

            expenses.append({"Category": category, "Amount": amount})
        except ValueError:
            # Catches non-numeric strings to prevent program crash
            print("Invalid input. Please enter a numeric value.")

    return expenses


def save_expenses_data(expense_list: list[dict]) -> None:
    """
    Saves expense data to a CSV file.
    Creates the file with headers if it doesn't exist.
    """
    if not expense_list:
        print("No expenses to save.")
        return

    fieldnames = ['Category', 'Amount']
    try:
        file_exists = FILENAME.exists()
        with open(FILENAME, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerows(expense_list)
        print(f"Saved {len(expense_list)} expense(s) to {FILENAME}")
    except IOError as e:
        print(f"Error saving expenses: {e}")


def get_expenses_data() -> list[dict]:
    """
    Reads expense data from the CSV file.
    Returns an empty list if the file doesn't exist or is empty.
    """
    if not FILENAME.exists():
        return []

    try:
        with open(FILENAME, 'r') as file:
            reader = csv.DictReader(file)
            data = list(reader)

        for expense in data:
            # Clean the category name for this session
            if 'Category' in expense:
                expense['Category'] = expense['Category'].strip().lower()

            # Convert Amount strings to floats
            if 'Amount' in expense:
                expense['Amount'] = float(expense['Amount'])

        return data
    except (IOError, ValueError) as e:
        print(f"Error reading expenses file: {e}")
        return []


def analyze_expenses(expenses: list[dict]) -> dict:
    """
    Processes the raw list of expenses to calculate totals and averages.
    Returns a summary dictionary or an empty dict if no data exists.
    """
    if not expenses:
        return {}

    # defaultdict handles missing keys automatically by initializing them to 0.0
    total_per_category = defaultdict(float)
    for e in expenses:
        total_per_category[e["Category"]] += e["Amount"]

    total = sum(total_per_category.values())

    # Find the category with the highest sum.
    # lambda ensures we compare the values, not the keys.
    highest_category = max(total_per_category,
                           key=lambda k: total_per_category.get(k, 0))

    # Average is based on the number of individual entries, not number of categories
    average_expense = total / len(expenses)

    return {
        "Total spent": total,
        "Highest category": highest_category,
        "Total per category": dict(total_per_category),
        "Average expense": average_expense
    }


def print_summary(analized_expenses: dict):
    """
    Formats and prints the analysis to the console.
    Includes a warning if one category exceeds 40% of total spend.
    """
    if not analized_expenses:
        print("No data to summarize.")
        return

    print("\n=== Financial Summary ===")
    # Iterate through the analysis metrics
    for key, value in analized_expenses.items():
        if isinstance(value, (int, float)):
            print(f"{key}: ${value:,.2f}")
        else:
            print(f"{key}: {value}")

    # Financial health check: Identify "heavy" spending categories
    total_spent = analized_expenses["Total spent"]
    for c, v in analized_expenses["Total per category"].items():
        # 0.4 represents 40% of the total budget
        if v > (total_spent * 0.4):
            print(f"WARNING: High dependency on '{c}' category (${v})")
    print("=========================")


# --- Main Execution Flow ---
if __name__ == "__main__":
    raw_data = collect_expenses()
    save_expenses_data(raw_data)
    expenses_data = get_expenses_data()
    analized = analyze_expenses(expenses_data)
    print_summary(analized)
