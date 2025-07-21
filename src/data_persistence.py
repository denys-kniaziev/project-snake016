import pickle
from pathlib import Path
from typing import TypeVar, Type, Any
from address_book import AddressBook
from note_book import NoteBook

T = TypeVar('T')


def _save_object(obj: Any, filename: str, object_type: str, silentmode: bool = False) -> None:
    """
    Serialize and save object to file using pickle.

    Args:
        obj: Object to save
        filename: Target file name
        object_type: Label for messages
        silentmode: Suppress success message if True
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
    Load object from pickle file or return default instance.

    Args:
        filename: File to load from
        default_factory: Type to create if loading fails
        object_type: Label for messages
        silentmode: Suppress success message if True

    Returns:
        Loaded object or new instance
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
    Save address book to file.

    Args:
        book: Address book instance
        filename: File to save to
        silentmode: Suppress success message if True
    """
    _save_object(book, filename, "Address book", silentmode)


def load_addressbook(filename: str = "addressbook.pkl", silentmode: bool = False) -> AddressBook:
    """
    Load address book from file.

    Args:
        filename: File to load from
        silentmode: Suppress success message if True

    Returns:
        Loaded AddressBook or new instance
    """
    return _load_object(filename, AddressBook, "Address book", silentmode)


def save_notebook(notebook: NoteBook, filename: str = "notebook.pkl", silentmode: bool = False) -> None:
    """
    Save notebook to file.

    Args:
        notebook: NoteBook instance
        filename: File to save to
        silentmode: Suppress success message if True
    """
    _save_object(notebook, filename, "Notebook", silentmode)


def load_notebook(filename: str = "notebook.pkl", silentmode: bool = False) -> NoteBook:
    """
    Load notebook from file.

    Args:
        filename: File to load from
        silentmode: Suppress success message if True

    Returns:
        Loaded NoteBook or new instance
    """
    return _load_object(filename, NoteBook, "Notebook", silentmode)
