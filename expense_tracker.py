import argparse
import json
import os
from datetime import datetime

FILE_NAME = "expenses.json"


def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []

    with open(FILE_NAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_expenses(expenses):
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f, indent=4)


def add_expense(description, amount):
    expenses = load_expenses()

    new_id = 1
    if expenses:
        new_id = max(expense["id"] for expense in expenses) + 1

    expense = {
        "id": new_id,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount
    }

    expenses.append(expense)
    save_expenses(expenses)

    print(f"Expense added successfully (ID: {new_id})")


def list_expenses():
    expenses = load_expenses()

    if not expenses:
        print("No expenses found.")
        return

    print(f"{'ID':<5}{'Date':<15}{'Description':<25}{'Amount'}")

    for expense in expenses:
        print(
            f"{expense['id']:<5}"
            f"{expense['date']:<15}"
            f"{expense['description']:<25}"
            f"${expense['amount']}"
        )


def delete_expense(expense_id):
    expenses = load_expenses()

    updated = [e for e in expenses if e["id"] != expense_id]

    if len(updated) == len(expenses):
        print("Expense ID not found.")
        return

    save_expenses(updated)
    print("Expense deleted successfully")


def update_expense(expense_id, description=None, amount=None):
    expenses = load_expenses()

    for expense in expenses:
        if expense["id"] == expense_id:

            if description:
                expense["description"] = description

            if amount is not None:
                expense["amount"] = amount

            save_expenses(expenses)
            print("Expense updated successfully")
            return

    print("Expense ID not found.")


def show_summary(month=None):
    expenses = load_expenses()

    if month:
        total = 0

        for expense in expenses:
            expense_month = datetime.strptime(
                expense["date"],
                "%Y-%m-%d"
            ).month

            if expense_month == month:
                total += expense["amount"]

        print(f"Total expenses for month {month}: ${total}")

    else:
        total = sum(expense["amount"] for expense in expenses)
        print(f"Total expenses: ${total}")


parser = argparse.ArgumentParser(
    description="Expense Tracker"
)

subparsers = parser.add_subparsers(dest="command")

# ADD
add_parser = subparsers.add_parser("add")
add_parser.add_argument(
    "--description",
    required=True
)
add_parser.add_argument(
    "--amount",
    required=True,
    type=float
)

# LIST
subparsers.add_parser("list")

# DELETE
delete_parser = subparsers.add_parser("delete")
delete_parser.add_argument(
    "--id",
    required=True,
    type=int
)

# UPDATE
update_parser = subparsers.add_parser("update")
update_parser.add_argument(
    "--id",
    required=True,
    type=int
)
update_parser.add_argument(
    "--description"
)
update_parser.add_argument(
    "--amount",
    type=float
)

# SUMMARY
summary_parser = subparsers.add_parser("summary")
summary_parser.add_argument(
    "--month",
    type=int
)

args = parser.parse_args()

if args.command == "add":
    add_expense(args.description, args.amount)

elif args.command == "list":
    list_expenses()

elif args.command == "delete":
    delete_expense(args.id)

elif args.command == "update":
    update_expense(
        args.id,
        args.description,
        args.amount
    )

elif args.command == "summary":
    show_summary(args.month)

else:
    parser.print_help()