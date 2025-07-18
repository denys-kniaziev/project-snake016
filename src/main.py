import pickle
from pathlib import Path
from commands import ( 
    parse_input, show_help, add_contact, change_contact, 
    show_phone, show_all, add_birthday, show_birthday, birthdays, delete_contact, add_address, add_email, 
    edit_fields, 
    add_note, remove_note, show_all_notes, search_notes, edit_note, search_notes_by_tag, sort_notes_by_tag, add_tag_to_note, remove_tag_from_note)

from address_book import AddressBook
from note_book import NoteBook


def save_addressbook(book: AddressBook, filename: str = "addressbook.pkl") -> None:
    """
    Save the address book to a file using pickle serialization.
    
    Args:
        book (AddressBook): The address book to save
        filename (str): The filename to save to (default: "addressbook.pkl")
    """
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
        print(f"Address book saved to {filename}")
    except Exception as e:
        print(f"Error saving address book: {e}")

def load_addressbook(filename: str = "addressbook.pkl") -> AddressBook:
    """
    Load the address book from a file using pickle deserialization.
    
    Args:
        filename (str): The filename to load from (default: "addressbook.pkl")
        
    Returns:
        AddressBook: The loaded address book or a new one if file doesn't exist
    """
    try:
        if Path(filename).exists():
            with open(filename, "rb") as f:
                book = pickle.load(f)
            print(f"Address book loaded from {filename}")
            return book
        else:
            print("No saved address book found. Starting with empty address book.")
            return AddressBook()
    except Exception as e:
        print(f"Error loading address book: {e}. Starting with empty address book.")
        return AddressBook()

def save_notebook(notebook: NoteBook, filename: str = "notebook.pkl", silentmode:bool=False) -> None:
    """
    Save the notebook to a file using pickle serialization.

    Args:
        notebook (NoteBook): The notebook to save
        filename (str): The filename to save to (default: "notebook.pkl")
    """
    try:
        with open(filename, "wb") as f:
            pickle.dump(notebook, f)
        if not silentmode:
            print(f"Notebook saved to {filename}")
    except Exception as e:
        print(f"Error saving notebook: {e}")

def load_notebook(filename: str = "notebook.pkl") -> NoteBook:
    """
    Load the notebook from a file using pickle deserialization.

    Args:
        filename (str): The filename to load from (default: "notebook.pkl")

    Returns:
        NoteBook: The loaded notebook or a new one if file doesn't exist
    """
    try:
        if Path(filename).exists():
            with open(filename, "rb") as f:
                notebook = pickle.load(f)
            print(f"Notebook loaded from {filename}")
            return notebook
        else:
            print("No saved notebook found. Starting with empty notebook.")
            return NoteBook()
    except Exception as e:
        print(f"Error loading notebook: {e}. Starting with empty notebook.")
        return NoteBook()


def main():
    """Main function that runs the assistant bot."""
    addressbook = load_addressbook()
    notebook = load_notebook()
    print("Welcome to the assistant bot!")

    try:
        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)
            
            match command:
                case "close" | "exit":
                    break

                case "hello":
                    print("How can I help you?")

                case "help":
                    print(show_help())

                case "add":
                    print(add_contact(args, addressbook))
                    save_addressbook(addressbook)

                case "change":
                    print(change_contact(args, addressbook))
                    save_addressbook(addressbook)

                case "phone":
                    print(show_phone(args, addressbook))

                case "all":
                    print(show_all(args, addressbook))

                case "delete":
                    print(delete_contact(args, addressbook))
                    save_addressbook(addressbook)

                case "add-birthday":
                    print(add_birthday(args, addressbook))
                    save_addressbook(addressbook)

                case "add-address":
                    print(add_address(args, addressbook))
                    save_addressbook(addressbook)

                case "add-email":
                    print(add_email(args, addressbook))
                    save_addressbook(addressbook)

                case "edit-fields":
                    print(edit_fields(args, addressbook))
                    save_addressbook(addressbook)

                case "show-birthday":
                    print(show_birthday(args, addressbook))

                case "add-note":
                    print(add_note(args, notebook))
                    save_notebook(notebook, silentmode=True)

                case "remove-note":
                    print(remove_note(args, notebook))
                    save_notebook(notebook, silentmode=True)

                case "show-all-notes":
                    print(show_all_notes(args, notebook))

                case "search-notes":
                    print(search_notes(args, notebook))

                case "edit-note":
                    print(edit_note(args, notebook))
                    save_notebook(notebook, silentmode=True)

                case "search-notes-by-tag":
                    print(search_notes_by_tag(args, notebook))

                case "sort-notes-by-tag":
                    print(sort_notes_by_tag(args, notebook))

                case "add-tag-to-note":
                    print(add_tag_to_note(args, notebook))
                    save_notebook(notebook, silentmode=True)

                case "remove-tag-from-note":
                    print(remove_tag_from_note(args, notebook))
                    save_notebook(notebook, silentmode=True)

                case "":
                    continue  # Skip empty inputs

                case _:
                    print("Invalid command. Type 'help' for available commands.")
    
    except KeyboardInterrupt:
        print("\nReceived Ctrl+C, exiting...")
    
    finally:
        save_addressbook(addressbook)
        save_notebook(notebook)
        print("Good bye!")


if __name__ == "__main__":
    main()