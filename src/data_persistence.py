import pickle
from pathlib import Path
from address_book import AddressBook
from note_book import NoteBook


def save_addressbook(book: AddressBook, filename: str = "addressbook.pkl", silentmode: bool = False) -> None:
    """
    Save the address book to a file using pickle serialization.
    
    Args:
        book (AddressBook): The address book to save
        filename (str): The filename to save to (default: "addressbook.pkl")
    """
    try:
        with open(filename, "wb") as f:
            pickle.dump(book, f)
        if not silentmode:
            print(f"Address book saved to {filename}")
    except Exception as e:
        print(f"Error saving address book: {e}")


def load_addressbook(filename: str = "addressbook.pkl", silentmode: bool = False) -> AddressBook:
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
            if not silentmode:
                print(f"Address book loaded from {filename}")
            return book
        else:
            print("No saved address book found. Starting with empty address book.")
            return AddressBook()
    except Exception as e:
        print(f"Error loading address book: {e}. Starting with empty address book.")
        return AddressBook()


def save_notebook(notebook: NoteBook, filename: str = "notebook.pkl", silentmode: bool = False) -> None:
    """
    Save the notebook to a file using pickle serialization.

    Args:
        notebook (NoteBook): The notebook to save
        filename (str): The filename to save to (default: "notebook.pkl")
        silentmode (bool): If True, suppress success messages
    """
    try:
        with open(filename, "wb") as f:
            pickle.dump(notebook, f)
        if not silentmode:
            print(f"Notebook saved to {filename}")
    except Exception as e:
        print(f"Error saving notebook: {e}")


def load_notebook(filename: str = "notebook.pkl", silentmode: bool = False) -> NoteBook:
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
            if not silentmode:
                print(f"Notebook loaded from {filename}")
            return notebook
        else:
            print("No saved notebook found. Starting with empty notebook.")
            return NoteBook()
    except Exception as e:
        print(f"Error loading notebook: {e}. Starting with empty notebook.")
        return NoteBook()
