import pickle
from pathlib import Path
from typing import TypeVar, Type, Any
from address_book import AddressBook
from note_book import NoteBook

T = TypeVar('T')


def _save_object(obj: Any, filename: str, object_type: str, silentmode: bool = False) -> None:
    """
    Generic function to save any object to a file using pickle serialization.
    
    Args:
        obj: The object to save
        filename (str): The filename to save to
        object_type (str): Type description for messages
        silentmode (bool): If True, suppress success messages
    """
    try:
        with open(filename, "wb") as f:
            pickle.dump(obj, f)
        if not silentmode:
            print(f"{object_type} saved to {filename}")
    except Exception as e:
        print(f"Error saving {object_type.lower()}: {e}")


def _load_object(filename: str, default_factory: Type[T], object_type: str, silentmode: bool = False) -> T:
    """
    Generic function to load any object from a file using pickle deserialization.
    
    Args:
        filename (str): The filename to load from
        default_factory (Type[T]): Class to instantiate if file doesn't exist or loading fails
        object_type (str): Type description for messages
        silentmode (bool): If True, suppress success messages
        
    Returns:
        T: The loaded object or a new instance if file doesn't exist
    """
    try:
        if Path(filename).exists():
            with open(filename, "rb") as f:
                obj = pickle.load(f)
            if not silentmode:
                print(f"{object_type} loaded from {filename}")
            return obj
        else:
            print(f"No saved {object_type.lower()} found. Starting with empty {object_type.lower()}.")
            return default_factory()
    except Exception as e:
        print(f"Error loading {object_type.lower()}: {e}. Starting with empty {object_type.lower()}.")
        return default_factory()


def save_addressbook(book: AddressBook, filename: str = "addressbook.pkl", silentmode: bool = False) -> None:
    """
    Save the address book to a file using pickle serialization.
    
    Args:
        book (AddressBook): The address book to save
        filename (str): The filename to save to (default: "addressbook.pkl")
        silentmode (bool): If True, suppress success messages
    """
    _save_object(book, filename, "Address book", silentmode)


def load_addressbook(filename: str = "addressbook.pkl", silentmode: bool = False) -> AddressBook:
    """
    Load the address book from a file using pickle deserialization.
    
    Args:
        filename (str): The filename to load from (default: "addressbook.pkl")
        silentmode (bool): If True, suppress success messages
        
    Returns:
        AddressBook: The loaded address book or a new one if file doesn't exist
    """
    return _load_object(filename, AddressBook, "Address book", silentmode)


def save_notebook(notebook: NoteBook, filename: str = "notebook.pkl", silentmode: bool = False) -> None:
    """
    Save the notebook to a file using pickle serialization.

    Args:
        notebook (NoteBook): The notebook to save
        filename (str): The filename to save to (default: "notebook.pkl")
        silentmode (bool): If True, suppress success messages
    """
    _save_object(notebook, filename, "Notebook", silentmode)


def load_notebook(filename: str = "notebook.pkl", silentmode: bool = False) -> NoteBook:
    """
    Load the notebook from a file using pickle deserialization.

    Args:
        filename (str): The filename to load from (default: "notebook.pkl")
        silentmode (bool): If True, suppress success messages

    Returns:
        NoteBook: The loaded notebook or a new one if file doesn't exist
    """
    return _load_object(filename, NoteBook, "Notebook", silentmode)
