from address_book import AddressBook, Record
from note_book import NoteBook, Note
from ui_formatter import UIFormatter
import shlex


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
            return "Item not found."
        except IndexError:
            return "Not enough arguments provided."
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    return inner

def parse_input(user_input: str) -> tuple[str, list[str]]:
    """
    Parse user input into command and arguments.
    Supports quoted strings for multi-word arguments.
    
    Args:
        user_input (str): The raw input string from the user.
        
    Returns:
        tuple[str, list[str]]: A tuple containing the command and a list of arguments.
    """
    # Handle empty input
    if not user_input.strip():
        return "", []
    
    try:
        # Use shlex to properly handle quoted strings
        parts = shlex.split(user_input)
        if not parts:
            return "", []
        
        cmd = parts[0].strip().lower()
        args = parts[1:] if len(parts) > 1 else []
        return cmd, args
    except ValueError:
        # Fallback to simple split if shlex fails (e.g., unmatched quotes)
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, args

@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """
    Universal add command for contacts with optional email and birthday.
    Can add phone, email, birthday all at once or just name + phone (minimum required).
    
    Args:
        args (list[str]): List containing name, phone, [email], [birthday].
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide both name and phone number. Usage: add-contact <name> <phone> [email] [birthday]")
    
    name = args[0]
    phone = args[1]
    email = args[2] if len(args) > 2 else None
    birthday = args[3] if len(args) > 3 else None
    
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    
    # Add phone (required)
    if phone:
        record.add_phone(phone)
    
    # Add email if provided
    if email:
        try:
            record.add_email(email)
            message += f" Email added."
        except ValueError as e:
            message += f" Email error: {e}"
    
    # Add birthday if provided
    if birthday:
        try:
            record.add_birthday(birthday)
            message += f" Birthday added."
        except ValueError as e:
            message += f" Birthday error: {e}"
    
    return message

@input_error
def edit_phone(args: list[str], book: AddressBook) -> str:
    """
    Edit existing phone number for a contact.
    
    Args:
        args (list[str]): List containing name, old phone, and new phone.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 3:
        raise ValueError("Please provide name, old phone, and new phone. Usage: edit-phone <name> <old_phone> <new_phone>")
    
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    record.edit_phone(old_phone, new_phone)
    return f"Phone number updated for {name}."

@input_error
def add_phone(args: list[str], book: AddressBook) -> str:
    """
    Add an additional phone number to an existing contact.
    
    Args:
        args (list[str]): List containing name and new phone number.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide name and phone number. Usage: add-phone <name> <phone>")
    
    name, phone = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    # Check if phone already exists
    if record.find_phone(phone):
        return f"Phone number {phone} already exists for {name}."
    
    record.add_phone(phone)
    return f"Phone number {phone} added to {name}."

@input_error
def remove_phone(args: list[str], book: AddressBook) -> str:
    """
    Remove a specific phone number from a contact.
    
    Args:
        args (list[str]): List containing name and phone number to remove.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide name and phone number. Usage: remove-phone <name> <phone>")
    
    name, phone = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    # Check if contact has this phone
    if not record.find_phone(phone):
        return f"Phone number {phone} not found for {name}."
    
    # Prevent removing the last phone if it's the only one
    if len(record.phones) == 1:
        return f"Cannot remove {phone} - it's the only phone number for {name}. Use delete-contact to remove the entire contact."
    
    record.remove_phone(phone)
    return f"Phone number {phone} removed from {name}."

@input_error  
def edit_email(args: list[str], book: AddressBook) -> str:
    """
    Add or update email for a contact (upsert logic).
    
    Args:
        args (list[str]): List containing name and new email.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide name and email. Usage: edit-email <name> <new_email>")
    
    name, new_email = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    action = "updated" if record.email else "added"
    record.add_email(new_email)
    return f"Email {action} for {name}."

@input_error
def edit_birthday(args: list[str], book: AddressBook) -> str:
    """
    Add or update birthday for a contact (upsert logic).
    
    Args:
        args (list[str]): List containing name and birthday in DD.MM.YYYY format.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide name and birthday. Usage: edit-birthday <name> <DD.MM.YYYY>")
    
    name, birthday = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    action = "updated" if record.birthday else "added"
    record.add_birthday(birthday)
    return f"Birthday {action} for {name}."

@input_error
def edit_address(args: list[str], book: AddressBook) -> str:
    """
    Add or update address for a contact (upsert logic).
    
    Args:
        args (list[str]): List containing name and address.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide name and address. Usage: edit-address <name> <new_address>")
    
    name = args[0]
    address = " ".join(args[1:])  # Join all remaining args as address can contain spaces
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    action = "updated" if record.address else "added"
    record.add_address(address)
    return f"Address {action} for {name}."

@input_error
def edit_name(args: list[str], book: AddressBook) -> str:
    """
    Rename a contact.
    
    Args:
        args (list[str]): List containing old name and new name.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Status message.
    """
    if len(args) < 2:
        raise ValueError("Please provide old name and new name. Usage: edit-name <old_name> <new_name>")
    
    old_name, new_name = args
    
    # Use the AddressBook's rename_contact method (proper OOP approach)
    book.rename_contact(old_name, new_name)
    return f"Contact renamed from '{old_name}' to '{new_name}'."

@input_error
def show_contact(args: list[str], book: AddressBook) -> str:
    """
    Show a specific contact with formatted display.
    
    Args:
        args (list[str]): List containing the contact name.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Formatted contact information or error message.
    """
    if len(args) < 1:
        raise ValueError("Please provide a contact name. Usage: show-contact <name>")
    
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    return UIFormatter.format_single_contact(record)

@input_error
def show_contacts(args: list[str], book: AddressBook) -> str:
    """
    Show all contacts and their information in a formatted table.
    
    Args:
        args (list[str]): Should be empty.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Formatted table of all contacts or message if no contacts.
    """
    if not book.data:
        return "No contacts saved."
    
    records = list(book.data.values())
    return UIFormatter.format_contacts_table(records)

@input_error
def search_contacts(args: list[str], book: AddressBook) -> str:
    """
    Search for contacts by name, phone, email, or address.
    
    Args:
        args (list[str]): List containing the search query.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Formatted string of matching contacts.
    """
    if len(args) < 1:
        raise ValueError("Please provide a search query.")
    
    query = " ".join(args).lower()
    results = []
    
    for record in book.data.values():
        # Search in name
        if query in record.name.value.lower():
            results.append(record)
            continue
            
        # Search in phones
        for phone in record.phones:
            if query in phone.value:
                results.append(record)
                break
        else:
            # Search in email
            if record.email and query in record.email.value.lower():
                results.append(record)
            # Search in address
            elif record.address and query in record.address.value.lower():
                results.append(record)
    
    if results:
        return f"Found {len(results)} contact(s):\n" + UIFormatter.format_contacts_table(results)
    else:
        return f"No contacts found matching '{' '.join(args)}'."

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
        raise ValueError("Please provide a contact name. Usage: delete-contact <name>")
    
    name = args[0]
    try:
        book.delete(name)
        return f"Contact '{name}' deleted."
    except KeyError:
        raise KeyError(f"Contact '{name}' not found")

@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """
    Show upcoming birthdays for the next number_days days
    
    Args:
        args (list[str]): List containing the number of days.
        book (AddressBook): The address book instance.
        
    Returns:
        str: Formatted string of upcoming birthdays.
    """
    if len(args) < 1:
        raise ValueError("Please provide the number of days.")
    
    try:
        number_days = int(args[0])
    except ValueError:
        raise ValueError("Number of days must be a valid integer.")
    
    if number_days < 0:
        raise ValueError("Number of days must be positive.")
    
    upcoming = book.get_upcoming_birthdays(args)
    
    if not upcoming:
        return f"No upcoming birthdays in the next {number_days} days."
    
    return UIFormatter.format_birthdays_table(upcoming)


@input_error
def add_note(args: list[str], notebook: NoteBook) -> str:
    """
        Add a new note to the note book.
        
        Args:
            args (list[str]): List containing title, content, and optional tags.
            notebook (NoteBook): The note book instance.

        Returns:
            str: Status message.
        """    
    if len(args) < 2:
        raise ValueError("Please provide a title and content for the note.")
    
    title = args[0]
    content = args[1]
    
    # Handle tags if provided
    tags = []
    if len(args) > 2:
        # Tags are in the third argument, split by comma
        tags = [tag.strip() for tag in args[2].split(',') if tag.strip()]
    
    note = Note(title, content, tags)
    return notebook.add(note)

@input_error
def remove_note(args: list[str], notebook: NoteBook) -> str:
    """
        Remove a note from the note book by title.
        
        Args:
            args (list[str]): List containing the title of the note to remove.
            notebook (NoteBook): The note book instance.

        Returns:
            str: Status message.
        """
    if len(args) < 1:
        raise ValueError("Please provide a title of the note to remove.")
    title = args[0]
    return notebook.remove(title)

@input_error
def show_all_notes(args: list[str], notebook: NoteBook) -> str:
    """
    Show all notes in the note book with table formatting.
    
    Args:
        args (list[str]): Should be empty.
        notebook (NoteBook): The note book instance.

    Returns:
        str: Formatted table of all notes or message if no notes.
    """
    if args:
        return "No arguments expected for this command."
    
    if not notebook.notes:
        return "No notes found."
    
    return UIFormatter.format_notes_table(notebook.notes)

@input_error
def show_note(args: list[str], notebook: NoteBook) -> str:
    """
    Show a specific note with detailed formatting.
    
    Args:
        args (list[str]): List containing the note title.
        notebook (NoteBook): The note book instance.

    Returns:
        str: Formatted note details or error message.
    """
    if len(args) < 1:
        raise ValueError("Please provide a note title. Usage: show-note <title>")
    
    title = args[0]
    note = notebook.find(title)
    if note is None:
        raise KeyError(f"Note '{title}' not found")
    
    return UIFormatter.format_single_note(note)

@input_error
def search_notes(args: list[str], notebook: NoteBook) -> str:
    """
    Search for notes containing a specific query in their title or content.
    
    Args:
        args (list[str]): List containing the search query.
        notebook (NoteBook): The note book instance.

    Returns:
        str: Formatted table of matching notes.
    """
    if len(args) < 1:
        raise ValueError("Please provide a search query.")
    query = " ".join(args)
    result = notebook.search(query)

    if result:
        return f"Found {len(result)} note(s) matching '{query}':\n" + UIFormatter.format_notes_table(result)
    else:
        return f"No notes found matching '{query}'."

@input_error
def edit_note(args: list[str], notebook: NoteBook) -> str:
    """
        Edit an existing note in the note book.
        
        Args:
            args (list[str]): List containing title, new title, new content, and new tags.
            notebook (NoteBook): The note book instance.

        Returns:
            str: Status message.
        """
    if len(args) < 1:
        raise ValueError("Please provide the title of the note to edit.")
    
    title = args[0]
    new_title = args[1] if len(args) > 1 else None
    new_content = " ".join(args[2:]) if len(args) > 2 else None
    new_tags = args[3:] if len(args) > 3 else None

    return notebook.edit(title, new_title, new_content, new_tags)

@input_error
def search_notes_by_tag(args: list[str], notebook: NoteBook) -> str:
    """
    Search for notes by a specific tag.
    
    Args:
        args (list[str]): List containing the tag to search for.
        notebook (NoteBook): The note book instance.

    Returns:
        str: Formatted table of notes matching the tag.
    """
    if len(args) < 1:
        raise ValueError("Please provide a tag to search for.")
    tag = args[0]
    result = notebook.search_by_tag(tag)

    if result:
        return f"Found {len(result)} note(s) with tag '{tag}':\n" + UIFormatter.format_notes_table(result)
    else:
        return f"No notes found with tag '{tag}'."

@input_error
def sort_notes_by_tag(args: list[str], notebook: NoteBook) -> list[Note]:
    """
        Sort notes by their tags.
        
        Args:
            args (list[str]): Should be empty.
            notebook (NoteBook): The note book instance.

        Returns:
            list[Note]: Sorted list of notes by tags.
        """
    if args:
        raise ValueError("No arguments expected for this command.")
    return notebook.sort_by_tag()

@input_error
def add_tag_to_note(args: list[str], notebook: NoteBook) -> str:
    """
        Add a tag to an existing note.
        
        Args:
            args (list[str]): List containing title and tag.
            notebook (NoteBook): The note book instance.

        Returns:
            str: Status message.
        """
    if len(args) < 2:
        raise ValueError("Please provide a title and a tag to add.")
    
    title, tag = args[0], args[1]
    note = notebook.find(title)
    if note is None:
        raise KeyError(f"Note '{title}' not found")
        
    return note.add_tag(tag)

@input_error
def remove_tag_from_note(args: list[str], notebook: NoteBook) -> str:
    """
        Remove a tag from an existing note.
        
        Args:
            args (list[str]): List containing title and tag.
            notebook (NoteBook): The note book instance.

        Returns:
            str: Status message.
        """
    if len(args) < 2:
        raise ValueError("Please provide a title and a tag to remove.")
    
    title, tag = args[0], args[1]
    note = notebook.find(title)
    if note is None:
        raise KeyError(f"Note '{title}' not found")
    
    return note.remove_tag(tag)
