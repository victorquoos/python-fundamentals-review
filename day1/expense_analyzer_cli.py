from collections import defaultdict


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
    # Iterate through the main analysis metrics
    for key, value in analized_expenses.items():
        if key != "Total per category":
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
    analized = analyze_expenses(raw_data)
    print_summary(analized)
