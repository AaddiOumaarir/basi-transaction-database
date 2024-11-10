from datetime import datetime



CATEGORIES = {"I": "income", "E": "Expense"}

def get_date(prompt, allowed_default=False):
    date_input = input(prompt)
    if allowed_default and not date_input:
        return datetime.today().strftime("%d-%m-%Y")
    try:
        valide_date = datetime.strptime(date_input, "%d-%m-%Y")
        return valide_date.strftime("%d-%m-%Y")
    except ValueError:
        print("invalid date format. Please enter the date in dd-mm-yyyy format")
        return get_date(prompt, allowed_default)



def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("invalid amount. The amount must be greater than 0.")
        return amount
    except ValueError as e:
        return get_amount()

def get_category():
    category = input("Enter the category('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Invalid category. Enter 'I' for Income or 'E' for Expense.")
    return get_category()


def get_description():
    description = input("Enter description: ")
    return description