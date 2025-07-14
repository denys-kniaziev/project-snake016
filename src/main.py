import pickle
from pathlib import Path
from commands import (
    parse_input, show_help, add_contact, change_contact, 
    show_phone, show_all, add_birthday, show_birthday, birthdays, delete_contact
)
from address_book import AddressBook


def save_data(book: AddressBook, filename: str = "addressbook.pkl") -> None:
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


def load_data(filename: str = "addressbook.pkl") -> AddressBook:
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


def main():
    """Main function that runs the assistant bot."""
    book = load_data()
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
                    print(add_contact(args, book))
                    save_data(book)

                case "change":
                    print(change_contact(args, book))
                    save_data(book)

                case "phone":
                    print(show_phone(args, book))

                case "all":
                    print(show_all(args, book))

                case "delete":
                    print(delete_contact(args, book))
                    save_data(book)

                case "add-birthday":
                    print(add_birthday(args, book))
                    save_data(book)

                case "show-birthday":
                    print(show_birthday(args, book))

                case "birthdays":
                    print(birthdays(args, book))

                case "":
                    continue  # Skip empty inputs

                case _:
                    print("Invalid command. Type 'help' for available commands.")
    
    except KeyboardInterrupt:
        print("\nReceived Ctrl+C, exiting...")
    
    finally:
        save_data(book)
        print("Good bye!")


if __name__ == "__main__":
    main()