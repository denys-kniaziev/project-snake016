from address_book import AddressBook, Record
from note_book import NoteBook, Note
from ui_formatter import UIFormatter
import shlex


def input_error(func):
    """
    Handle common input errors with user-friendly messages.
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
    Split user input into command and arguments.

    Supports quoted strings using shlex.
    """
    if not user_input.strip():
        return "", []
    try:
        parts = shlex.split(user_input)
        if not parts:
            return "", []
        cmd = parts[0].strip().lower()
        args = parts[1:] if len(parts) > 1 else []
        return cmd, args
    except ValueError:
        cmd, *args = user_input.split()
        return cmd.strip().lower(), args


@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    """Add new contact with phone, email, birthday."""
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

    if phone:
        record.add_phone(phone)
    if email:
        try:
            record.add_email(email)
            message += f" Email added."
        except ValueError as e:
            message += f" Email error: {e}"
    if birthday:
        try:
            record.add_birthday(birthday)
            message += f" Birthday added."
        except ValueError as e:
            message += f" Birthday error: {e}"

    return message


@input_error
def edit_phone(args: list[str], book: AddressBook) -> str:
    """Edit a contact's phone number."""
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
    """Add another phone number to a contact."""
    if len(args) < 2:
        raise ValueError("Please provide name and phone number. Usage: add-phone <name> <phone>")

    name, phone = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")

    if record.find_phone(phone):
        return f"Phone number {phone} already exists for {name}."

    record.add_phone(phone)
    return f"Phone number {phone} added to {name}."


@input_error
def remove_phone(args: list[str], book: AddressBook) -> str:
    """Remove a phone number from a contact."""
    if len(args) < 2:
        raise ValueError("Please provide name and phone number. Usage: remove-phone <name> <phone>")

    name, phone = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")

    if not record.find_phone(phone):
        return f"Phone number {phone} not found for {name}."

    if len(record.phones) == 1:
        return f"Cannot remove {phone} - it's the only phone number for {name}. Use delete-contact to remove the entire contact."

    record.remove_phone(phone)
    return f"Phone number {phone} removed from {name}."


@input_error
def edit_email(args: list[str], book: AddressBook) -> str:
    """Add or update a contact's email."""
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
    """Add or update a contact's birthday."""
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
    """Add or update a contact's address."""
    if len(args) < 2:
        raise ValueError("Please provide name and address. Usage: edit-address <name> <new_address>")

    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")

    action = "updated" if record.address else "added"
    record.add_address(address)
    return f"Address {action} for {name}."


@input_error
def edit_name(args: list[str], book: AddressBook) -> str:
    """Rename a contact."""
    if len(args) < 2:
        raise ValueError("Please provide old name and new name. Usage: edit-name <old_name> <new_name>")

    old_name, new_name = args
    book.rename_contact(old_name, new_name)
    return f"Contact renamed from '{old_name}' to '{new_name}'."


@input_error
def show_contact(args: list[str], book: AddressBook) -> str:
    """Show contact details."""
    if len(args) < 1:
        raise ValueError("Please provide a contact name. Usage: show-contact <name>")

    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")

    return UIFormatter.format_single_contact(record)


@input_error
def show_contacts(args: list[str], book: AddressBook) -> str:
    """Show all contacts."""
    if not book.data:
        return "No contacts saved."
    return UIFormatter.format_contacts_table(list(book.data.values()))


@input_error
def search_contacts(args: list[str], book: AddressBook) -> str:
    """Search contacts by name, phone, email, or address."""
    if len(args) < 1:
        raise ValueError("Please provide a search query.")

    query = " ".join(args).lower()
    results = []

    for record in book.data.values():
        if query in record.name.value.lower():
            results.append(record)
            continue
        if any(query in phone.value for phone in record.phones):
            results.append(record)
            continue
        if record.email and query in record.email.value.lower():
            results.append(record)
        elif record.address and query in record.address.value.lower():
            results.append(record)

    if results:
        return f"Found {len(results)} contact(s):\n" + UIFormatter.format_contacts_table(results)
    else:
        return f"No contacts found matching '{' '.join(args)}'."


@input_error
def delete_contact(args: list[str], book: AddressBook) -> str:
    """Delete a contact."""
    if len(args) < 1:
        raise ValueError("Please provide a contact name. Usage: delete-contact <name>")

    name = args[0]
    book.delete(name)
    return f"Contact '{name}' deleted."


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    """Show upcoming birthdays."""
    if len(args) < 1:
        raise ValueError("Please provide the number of days.")
    try:
        number_days = int(args[0])
    except ValueError:
        raise ValueError("Number of days must be a valid integer.")
    if number_days < 0:
        raise ValueError("Number of days must be positive.")

    upcoming = book.get_upcoming_birthdays(number_days)
    if not upcoming:
        return f"No upcoming birthdays in the next {number_days} days."
    return UIFormatter.format_birthdays_table(upcoming)


@input_error
def add_note(args: list[str], notebook: NoteBook) -> str:
    """Add a new note with optional tags."""
    if len(args) < 2:
        raise ValueError("Please provide a title and content for the note.")

    title = args[0]
    content = args[1]
    tags = [tag.strip() for tag in args[2].split(',')] if len(args) > 2 else []

    note = Note(title, content, tags)
    return notebook.add(note)


@input_error
def remove_note(args: list[str], notebook: NoteBook) -> str:
    """Remove a note by title."""
    if len(args) < 1:
        raise ValueError("Please provide a title of the note to remove.")
    return notebook.remove(args[0])


@input_error
def show_all_notes(args: list[str], notebook: NoteBook) -> str:
    """Show all notes as a table."""
    if args:
        return "No arguments expected for this command."
    if not notebook.notes:
        return "No notes found."
    return UIFormatter.format_notes_table(notebook.notes)


@input_error
def show_note(args: list[str], notebook: NoteBook) -> str:
    """Show details of a specific note."""
    if len(args) < 1:
        raise ValueError("Please provide a note title. Usage: show-note <title>")
    note = notebook.find(args[0])
    if note is None:
        raise KeyError(f"Note '{args[0]}' not found")
    return UIFormatter.format_single_note(note)


@input_error
def search_notes(args: list[str], notebook: NoteBook) -> str:
    """Search notes by title or content."""
    if len(args) < 1:
        raise ValueError("Please provide a search query.")
    query = " ".join(args)
    result = notebook.search(query)
    if result:
        return f"Found {len(result)} note(s) matching '{query}':\n" + UIFormatter.format_notes_table(result)
    return f"No notes found matching '{query}'."


@input_error
def edit_note(args: list[str], notebook: NoteBook) -> str:
    """Edit note title, content, or tags."""
    if len(args) < 1:
        raise ValueError("Please provide the title of the note to edit.")
    title = args[0]
    new_title = args[1] if len(args) > 1 else None
    new_content = " ".join(args[2:]) if len(args) > 2 else None
    new_tags = args[3:] if len(args) > 3 else None
    return notebook.edit(title, new_title, new_content, new_tags)


@input_error
def search_notes_by_tag(args: list[str], notebook: NoteBook) -> str:
    """Search notes by tag."""
    if len(args) < 1:
        raise ValueError("Please provide a tag to search for.")
    tag = args[0]
    result = notebook.search_by_tag(tag)
    if result:
        return f"Found {len(result)} note(s) with tag '{tag}':\n" + UIFormatter.format_notes_table(result)
    return f"No notes found with tag '{tag}'."


@input_error
def sort_notes_by_tag(args: list[str], notebook: NoteBook) -> str:
    """Return notes sorted alphabetically by tag."""
    if args:
        raise ValueError("No arguments expected for this command.")
    return UIFormatter.format_notes_table(notebook.sort_by_tag())


@input_error
def add_tag_to_note(args: list[str], notebook: NoteBook) -> str:
    """Add a tag to a note."""
    if len(args) < 2:
        raise ValueError("Please provide a title and a tag to add.")
    note = notebook.find(args[0])
    if note is None:
        raise KeyError(f"Note '{args[0]}' not found")
    return note.add_tag(args[1])


@input_error
def remove_tag_from_note(args: list[str], notebook: NoteBook) -> str:
    """Remove a tag from a note."""
    if len(args) < 2:
        raise ValueError("Please provide a title and a tag to remove.")
    note = notebook.find(args[0])
    if note is None:
        raise KeyError(f"Note '{args[0]}' not found")
    return note.remove_tag(args[1])
