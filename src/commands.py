from address_book import AddressBook, Record
from note_book import NoteBook, Note


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
        raise ValueError("Please provide both name and phone number. Usage: add-contact <name> <phone>")
    
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
        raise ValueError("Please provide name, old phone, and new phone. Usage: change-contact <name> <old_phone> <new_phone>")
    
    name, field_name, new_value = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    
    record.edit_field(field_name, new_value)
    return "Contact updated."

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
        result_strings = [str(record) for record in results]
        return f"Found {len(results)} contact(s):\n" + "\n".join(result_strings)
    else:
        return f"No contacts found matching '{' '.join(args)}'."

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
        raise ValueError("Please provide a contact name. Usage: delete-contact <name>")
    
    name = args[0]
    try:
        book.delete(name)
        return f"Contact '{name}' deleted."
    except KeyError:
        raise KeyError(f"Contact '{name}' not found")

@input_error
def add_note(args: list[str], notebook: NoteBook) -> str:
    """
        Add a new note to the note book.
        
        Args:
            args (list[str]): List containing title and content.
            notebook (NoteBook): The note book instance.

        Returns:
            str: Status message.
        """    
    if len(args) < 2:
        raise ValueError("Please provide a title and content for the note.")
    title, content = args[0], " ".join(args[1:])
    tags = [tag.strip() for tag in args[2:]] if len(args) > 2 else []
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
        Show all notes in the note book.
        
        Args:
            args (list[str]): Should be empty.
            notebook (NoteBook): The note book instance.

        Returns:
            str: Formatted string of all notes or message if no notes.
        """
    return notebook.show_all() if not args else "No arguments expected for this command."

@input_error
def search_notes(args: list[str], notebook: NoteBook) -> str:
    """
        Search for notes containing a specific query in their title or content.
        
        Args:
            args (list[str]): List containing the search query.
            notebook (NoteBook): The note book instance.

        Returns:
            list[Note]: List of notes matching the search query.
        """
    if len(args) < 1:
        raise ValueError("Please provide a search query.")
    query = " ".join(args)
    result = notebook.search(query)

    if result:
        message_parts = [f"Found {len(result)} note(s) for note '{query}':"]
        for i, note in enumerate(result):
            message_parts.append(
                f"  {i+1}. Title: {note.title}, Content: {note.content}, Tags: {', '.join(note.tags)}"
            )
        return "\n".join(message_parts)
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
            list[Note]: List of notes matching the tag.
        """
    if len(args) < 1:
        raise ValueError("Please provide a tag to search for.")
    tag = args[0]
    result = notebook.search_by_tag(tag)

    if result:
        message_parts = [f"Found {len(result)} note(s) for tag '{tag}':"]
        for i, note in enumerate(result):
            message_parts.append(
                f"  {i+1}. Title: {note.title}, Content: {note.content}, Tags: {', '.join(note.tags)}"
            )
        return "\n".join(message_parts)
    else:
        return f"No notes found matching for tag '{tag}'."

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
