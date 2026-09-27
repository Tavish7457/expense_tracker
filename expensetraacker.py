
import csv
import os

FILE_NAME = "expenses.csv"
FIELDS = ["id", "amount", "category", "description", "date"]


# =====================================================================
# FILE HANDLING  (reads/writes expenses.csv)
# =====================================================================

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    expenses = []
    with open(FILE_NAME, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["amount"] = float(row["amount"])
            expenses.append(row)
    return expenses


def save_expenses(expenses):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


# =====================================================================
# MODULE 1: EXPENSE MANAGEMENT (add / view / delete)
# =====================================================================

def add_expense(amount, category, description, date):
    amount = float(amount)  # raises ValueError if not a number
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if not category.strip():
        raise ValueError("Category cannot be empty.")
    if not description.strip():
        raise ValueError("Description cannot be empty.")

    expenses = load_expenses()
    new_id = (max((e["id"] for e in expenses), default=0)) + 1
    record = {
        "id": new_id,
        "amount": amount,
        "category": category.strip().lower(),
        "description": description.strip(),
        "date": date.strip(),
    }
    expenses.append(record)
    save_expenses(expenses)
    return record


def view_expenses():
    return load_expenses()


def delete_expense(expense_id):
    expenses = load_expenses()
    remaining = [e for e in expenses if e["id"] != expense_id]
    deleted = len(remaining) < len(expenses)
    if deleted:
        save_expenses(remaining)
    return deleted


# =====================================================================
# MODULE 2: SEARCH & FILTER
# =====================================================================

def search_by_category(category):
    category = category.strip().lower()
    return [e for e in load_expenses() if e["category"] == category]


def search_by_date_range(start_date, end_date):
    return [e for e in load_expenses() if start_date <= e["date"] <= end_date]


def search_by_keyword(keyword):
    keyword = keyword.strip().lower()
    return [e for e in load_expenses() if keyword in e["description"].lower()]


# =====================================================================
# MODULE 3: REPORTING
# =====================================================================

def total_spent():
    return round(sum(e["amount"] for e in load_expenses()), 2)


def spending_by_category():
    totals = {}
    for e in load_expenses():
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return {k: round(v, 2) for k, v in totals.items()}


def highest_expense():
    expenses = load_expenses()
    return max(expenses, key=lambda e: e["amount"]) if expenses else None


# =====================================================================
# CLI MENU
# =====================================================================

MENU = """
=== Simple Expense Tracker ===
1. Add expense
2. View all expenses
3. Delete an expense
4. Search by category
5. Search by date range
6. Search by keyword
7. View report
8. Exit
Choose an option (1-8): """


def print_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return
    for e in expenses:
        print(f"  #{e['id']}  {e['date']}  {e['category']:<12} "
              f"{e['amount']:>8.2f}  {e['description']}")


def main():
    while True:
        choice = input(MENU).strip()

        if choice == "1":
            try:
                amount = input("Amount: ")
                category = input("Category: ")
                description = input("Description: ")
                date = input("Date (YYYY-MM-DD): ")
                record = add_expense(amount, category, description, date)
                print(f"Added expense #{record['id']}.")
            except ValueError as e:
                print(f"Input error: {e}")

        elif choice == "2":
            print_expenses(view_expenses())

        elif choice == "3":
            try:
                expense_id = int(input("Expense id to delete: "))
                print("Deleted." if delete_expense(expense_id) else "No expense with that id.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            print_expenses(search_by_category(input("Category: ")))

        elif choice == "5":
            start = input("Start date (YYYY-MM-DD): ")
            end = input("End date (YYYY-MM-DD): ")
            print_expenses(search_by_date_range(start, end))

        elif choice == "6":
            print_expenses(search_by_keyword(input("Keyword: ")))

        elif choice == "7":
            print(f"Total spent: {total_spent():.2f}")
            print("By category:")
            for category, total in spending_by_category().items():
                print(f"  {category:<12} {total:.2f}")
            top = highest_expense()
            if top:
                print(f"Highest expense: #{top['id']} {top['amount']:.2f} ({top['description']})")

        elif choice == "8":
            print("Goodbye!")
            break

        else:
            print("Please choose a number from 1 to 8.")


if __name__ == "__main__":
      main()