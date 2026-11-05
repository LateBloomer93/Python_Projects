import json
import os
from datetime import datetime

script_dir=os.path.dirname(os.path.abspath(__file__))
DB_FILE=os.path.join(script_dir, 'my_data.json')

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {'amount':[], 'category':[], 'description':[], 'date':[]}

def save_data(expenses):
    with open(DB_FILE, 'w') as f:
        json.dump(expenses, f, indent=2)

expenses=load_data()

if not expenses:
    expenses={
    'amount':[],
    'category': [],
    'description': [],
    'date': []
    }

def add_expense(amount, category, description, date):
    blank=[]

    fields=[
        ('amount', amount),
        ('category', category),
        ('description', description),
        ('date', date)
    ]

    for field_name, value in fields:
        if value==None or (isinstance(value, str) and value.strip()==""):
            blank.append(field_name)

    if blank:
        return f"The following fields are empty: {", ".join(blank)}"
    
    try:
        num=float(amount)
    except ValueError:
        return "Error: the amount has to be a number"

    if num<=0:
        return "Error: the amount has to be a positive number"
    
    cat1=category.strip().replace(" ","")
    if cat1.isdigit():
        return "The category must contain letters, not just numbers."

    des1=description.strip().replace(" ","")
    if des1.isdigit():
        return "The description must contain letters, not just numbers."
    
    try:
        datetime.strptime(date, "%d/%m/%Y")
    except ValueError:
        return "Error: date must be in DD/MM/YY format"
    
    expenses.setdefault('amount', []).append(amount)
    expenses.setdefault('category', []).append(category)
    expenses.setdefault('description', []).append(description)
    expenses.setdefault('date', []).append(date)
    save_data(expenses)

    return "The expense has been added"

def total_expenses():
    total=0
    if not expenses['amount']:
        return "Expenses are empty"
    
    for item in expenses['amount']:
        total+=float(item)
    
    return f"{total:,.2f}"

def monthly_spending(date):
    if date==None or (isinstance(date, str) and date.strip()==""):
        return "The date field is empty."
    
    try:
        parsed_dates=datetime.strptime(date, '%d/%m/%Y')
        month_q=parsed_dates.month
        year_q=parsed_dates.year
        print(f"This is the total spending in the month {month_q}, year {year_q}.")
    except ValueError:
        return "Error: Invalid date format."

    indices_in_q=[]
    total=0
    for i in range(len(expenses['date'])):
        try:
            questioned_dates=datetime.strptime(expenses['date'][i], '%d/%m/%Y')
            month_a=questioned_dates.month
            year_a=questioned_dates.year

            try:
                if month_a==month_q and year_a==year_q:
                    indices_in_q.append(i)
            except UnboundLocalError:
                return "Error: Invalid date format."
        except ValueError:
            return "Error: Invalid date format."
            
    try:
        for i in indices_in_q:
            total+=float(expenses['amount'][i])
    except ValueError as e:
        print("Error:", e)

    return f"{total:,.2f}"
    
def delete_expense(amount, date):
    blank=[]

    field=[
        ('amount', amount),
        ('date', date)
    ]

    for names, values in field:
        if values==None or (isinstance(values, str) and values.strip()==""):
            blank.append(names)

    if blank:
        return f"The following fields are empty: {", ".join(blank)}.\n"

    try:
        datetime.strptime(date, '%d/%M/%Y')
    except ValueError:
        return "Error: Invalid date format"
    
    matching_indices=[]

    for i in range(len(expenses['amount'])):
        if expenses['amount'][i]==amount and expenses['date'][i]==date:
            matching_indices.append(i)

    if len(matching_indices)==0:
        return "No expense with that amount and date was found."
    
    for i in matching_indices:
        expenses['amount'].pop(i)
        expenses['category'].pop(i)
        expenses['description'].pop(i)
        expenses['date'].pop(i)

    save_data(expenses)

    return "The expense has been deleted, as well as it's corresponding category, description and date."

def get_expense(amount, date):
    blank=[]

    field = [
        ('amount', amount),
        ('date', date)
    ]

    for names, values in field:
        if values==None or (isinstance(values, str) and values.strip()==""):
            blank.append(names)

    if blank:
        return f"The following fields are empty: {", ".join(blank)}.\n"

    try:
        datetime.strptime(date, '%d/%M/%Y')
    except ValueError:
        return "Error: Invalid date format"

    matching_indices=[]

    for i in range(len(expenses['amount'])):
        if expenses['amount'][i]==amount and expenses['date'][i]==date:
            matching_indices.append(i)

    if len(matching_indices)==0:
        return "No expense found with that exact same amount and date."
    
    for index, i in enumerate(matching_indices, 1):
        print(f"{index}.  {expenses['amount'][i]}, {expenses['category'][i]}, {expenses['description'][i]}, {expenses['date'][i]}")

    return f"The expenses result according to Amount: {amount} and Date: {date}."

def search_by_description(description):
    if description==None or (isinstance(description, str) and description==""):
        return "The description field is empty."
    
    matching_descriptions=[]

    for i in range(len(expenses['description'])):
        if expenses['description'][i]==description:
            matching_descriptions.append(i)

    if len(matching_descriptions)==0:
        return "No descriptions were found by that name."

    for index, i in enumerate(matching_descriptions, 1):
        print(f"{index}. {expenses['amount'][i]}, {expenses['category'][i]}, {expenses['description'][i]}, {expenses['date'][i]}")
    
    return f"Your search result by Description: {description}"

def monthly_budget(date, budget=8000):
    if budget=="":
        budget=8000
        
    if date==None or (isinstance(date, str) and date.strip()==""):
        return "The date field is empty."
    
    total=0

    if float(budget)<=0:
        return "The budget has to be a positive number bigger than 0."

    try:
        num=float(budget)
    except ValueError:
        print("Error: The budget has to be a number.")

    try:
        parsed_dates=datetime.strptime(date, '%d/%M/%Y')
        month=parsed_dates.month
        year=parsed_dates.year
    except ValueError:
        print("Error: Invalid date format")

    indices_in_q=[]
    for i in range(len(expenses['date'])):
        try:
            parsed_check_dates=datetime.strptime(expenses['date'][i], '%d/%M/%Y')
            month_q=parsed_check_dates.month
            year_q=parsed_check_dates.year
        except ValueError:
            print("Error: Invalid date format")
        if month==month_q and year==year_q:
            indices_in_q.append(i)

    for i in indices_in_q:
        total+=float(expenses['amount'][i])

    if total<= float(budget):
        return f"Total amount spent is below budget allocation. Balance: {num-total:,.2f}"
    elif total==num:
        return f"Amount used is exactly in the budget. Amount: {num:,.2f}"
    else:
        return f"Total amount exceeds the budget: Balance: -{total-num:,.2f}"

def clear_expense_tracker():

    expenses['amount'].clear()
    expenses['category'].clear()
    expenses['description'].clear()
    expenses['date'].clear()

    save_data(expenses)

    return f"The expenses have all been cleared, {expenses}"


def main():

    while True:
        print("\n---Welcome to your expense tracker---")
        print("1. Add an expense.")
        print("2. Display expenses.")
        print("3. Calculate total expenses.")
        print("4. Calculate total monthly expenses.")
        print("5. Delete an expense.")
        print("6. Search for a specific expense.")
        print("7. Search by description.")
        print("8. Check for monthly budget and limits.")
        print("9. Clear the all expenses in the tracker.")
        print("10. Exit the expense tracker.")

        try:
            choice=int(input("Enter a number between 1 and 10 to choose what to do next: "))
        except ValueError:
            print("Please input valid numbers only")
            choice=None

        if choice == 1:
            amount=input("Enter the amount of the expense: ")
            category=input("Enter the category of the expense: ")
            description=input("Enter a short description of the expense: ")
            date=input("Enter the date of the expense in the format DD/MM/YYYY: ")
            result=add_expense(amount, category, description, date)
            print(result)

        elif choice == 2:
            print("\nCurrent Expenses:")
            if not expenses:
                print("(Empty)")
            else:
                for key, value in expenses.items():
                    print(f"{key}: {value}")

        elif choice == 3:
            result=total_expenses()
            print(result)

        elif choice == 4:
            date=input("Enter the date of the month in question in DD/MM/YYYY format: ")
            result = monthly_spending(date)
            print(result)

        elif choice == 5:
            amount=input("Enter the amount of the expense to be deleted: ")
            date=input("Enter the date of the expense to be deleted: ")
            result=delete_expense(amount, date)
            print(result)

        elif choice == 6:
            amount=input("Enter the amount you are searching for: ")
            date=input("Enter the date of the expense in DD/MM/YYYY format: ")
            result=get_expense(amount, date)
            print(result)

        elif choice == 7:
            description=input("Enter the description you want to search for: ")
            result=search_by_description(description)
            print(result)

        elif choice==8:
            date=input("Enter the date of the month you want to check in DD/MM/YYYY format: ")
            budget=input("Enter the budget you want it compared against(default budget=8000): ")
            result=monthly_budget(date, budget)
            print(result)

        elif choice == 9:
            result=clear_expense_tracker()
            print(result)

        elif choice == 10:
            print("Exiting the Expense Tracker, goodbye!!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 10.")

if __name__ == '__main__':
    main()