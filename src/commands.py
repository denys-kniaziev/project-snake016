from textwrap import dedent
from address_book import AddressBook, Record


def input_error(func):
    """
    Decorator to handle input errors for bot command functions.
    
    Handles the following exceptions:
    - ValueError: When invalid values are provided
    - KeyError: When trying to access an item that doesn't exist
    - IndexError: When not enough arguments are provided
    
    Args:
        func: The function to decorate
        
    Returns:
        The decorated function with error handling
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {str(e)}"
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Not enough arguments provided."
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    return inner


def parse_input(user_input: str) -> tuple[str, list[str]]:
    """
    Parse user input into command and arguments.
    
    Args:
        user_input (str): The raw input string from the user.
        
    Returns:
        tuple[str, list[str]]: A tuple containing the command and a list of arguments.
    """
    # Handle empty input
    if not user_input.strip():
        return "", []
        
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """
    Add a new contact to the address book or add phone to existing contact.
    
    Args:
        args (list[str]): List containing name and phone number.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide both name and phone number. Usage: add <name> <phone>")
    
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """
    Change the phone number of an existing contact.
    
    Args:
        args (list[str]): List containing name, old phone, and new phone.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 3:
        raise ValueError("Please provide name, old phone, and new phone. Usage: change <name> <old_phone> <new_phone>")
    
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def edit_fields(args: list[str], book: AddressBook):
    """
    Change the named fields of an existing contact.
    
    Args:
        args (list[str]): List containing name, old phone, and new phone.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 3:
        raise ValueError("Please provide name, old phone, and new phone. Usage: change <name> <old_phone> <new_phone>")
    
    name, field_name, new_value = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    record.edit_field(field_name, new_value)
    return "Contact updated."

@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """
    Show the phone numbers of a specific contact.
    
    Args:
        args (list[str]): List containing the name of the contact.
        book (AddressBook): The address book instance.
        
    Returns:
        str: The phone numbers or an error message.
    """
    if len(args) < 1:
        raise ValueError("Please provide a contact name. Usage: phone <name>")
    
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    if not record.phones:
        return f"No phone numbers found for {name}"
    
    phones = ", ".join(phone.value for phone in record.phones)
    return f"{name}: {phones}"


@input_error
def show_all(args: list[str], book: AddressBook) -> str:
    """
    Show all contacts and their information.
    
    Args:
        args (list[str]): Should be empty.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Formatted string of all contacts or message if no contacts.
    """
    if not book.data:
        return "No contacts saved."
    
    result = []
    for record in book.data.values():
        result.append(str(record))
    
    return "\n".join(result)


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """
    Add birthday to a contact.
    
    Args:
        args (list[str]): List containing name and birthday in DD.MM.YYYY format.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide both name and birthday. Usage: add-birthday <name> <DD.MM.YYYY>")
    
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    record.add_birthday(birthday)
    return f"Birthday added for {name}."

@input_error
def add_address(args: list[str], book: AddressBook) -> str:
    """
    Add address to a contact.
    
    Args:
        args (list[str]): List containing name and address.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide both name and address.")
    
    name, address = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    record.add_address(address)
    return f"Address added for {name}."

@input_error
def add_email(args: list[str], book: AddressBook) -> str:
    """
    Add email to a contact.
    
    Args:
        args (list[str]): List containing name and email.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide both name and email.")
    
    name, email = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    record.add_email(email)
    return f"Email added for {email}."

@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """
    Show birthday of a specific contact.
    
    Args:
        args (list[str]): List containing the name of the contact.
        book (AddressBook): The address book instance.
        
    Returns:
        str: The birthday or an error message.
    """
    if len(args) < 1:
        raise ValueError("Please provide a contact name. Usage: show-birthday <name>")
    
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    if record.birthday is None:
        return f"No birthday found for {name}"
    
    return f"{name}'s birthday: {record.birthday}"


@input_error
def birthdays(number_days:int, book: AddressBook) -> str:
    """
    Show upcoming birthdays for the next number_days days
    
    Args:
        number_days: Number days
        book (AddressBook): The address book instance.
        
    Returns:
        str: Formatted string of upcoming birthdays.
    """
    upcoming = book.get_upcoming_birthdays(number_days)
    
    if not upcoming:
        return "No upcoming birthdays in the {number_days} days."
    
    result = ["Upcoming birthdays:"]
    for birthday_info in upcoming:
        result.append(f"{birthday_info['name']}: {birthday_info['congratulation_date']}")
    
    return "\n".join(result)


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """
    Delete a contact from the address book.
    
    Args:
        args (list[str]): List containing the name of the contact to delete.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 1:
        raise ValueError("Please provide a contact name. Usage: delete <name>")
    
    name = args[0]
    try:
        book.delete(name)
        return f"Contact '{name}' deleted."
    except KeyError:
        raise KeyError(f"Contact '{name}' not found")


def show_help() -> str:
    """
    Show help information with all available commands and their usage.
    
    Returns:
        str: Formatted help text with all commands
    """
    help_text = dedent("""
        Available commands:
        hello                                   - Greet the bot
        add <name> <phone>                      - Add a new contact or phone to existing contact
        change <name> <old_phone> <new_phone>   - Change existing contact's phone number
        phone <name>                            - Show contact's phone numbers
        all                                     - Show all contacts
        add-birthday <name> <DD.MM.YYYY>        - Add birthday to contact
        add-address <name> <address>            - Add address to contact
        add-email <name> <email>              - Add email to contact
        show-birthday <name>                    - Show contact's birthday
        birthdays <number of days>              - Show contacts whose birthday is a specified number of days away from the current date
        edit-fields <name> <name field> <new_value> - Edit named field
        delete <name>                           - Delete a contact
        help                                    - Show this help message
        exit/close                              - Exit the program

        Examples:
        add John 1234567890
        change John 1234567890 0987654321
        phone John
        add-birthday John 15.03.1990
        add-address John USA
        add-email John 124@gmail.com
        show-birthday John
        birthdays 5
        edit-fields John birthday 01.05.1997
        delete John 
        all""")
    return help_text.strip()