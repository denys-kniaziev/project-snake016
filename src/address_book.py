import re
from collections import UserDict
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict


class Field:
    """
    Base class for all contact record fields.
    
    Provides common functionality for storing and displaying field values.
    All specific field types inherit from this class.
    
    Attributes:
        value (str): The actual value stored in the field
    """
    
    def __init__(self, value: str) -> None:
        """
        Initialize the field with a value.
        
        Args:
            value (str): The value to store in this field
        """
        self.value = value

    def __str__(self) -> str:
        """
        Return string representation of the field value.
        
        Returns:
            str: String representation of the field value
        """
        return str(self.value)


class Name(Field):
    """
    Contact name field.
    
    Stores the full name of a contact. No special validation is required
    for names as they can contain various characters and formats.
    
    Inherits from Field class for basic value storage functionality.
    """
    pass


class Phone(Field):
    """
    Phone number field with validation.
    
    Validates that phone numbers contain exactly 10 digits.
    Stores phone numbers in a standardized format for consistency.
    
    Validation Rules:
        - Must contain exactly 10 digits
        - Only numeric characters allowed
        - No formatting characters (dashes, spaces, parentheses)
    
    Raises:
        ValueError: If phone number doesn't meet validation criteria
    """
    
    def __init__(self, value: str) -> None:
        """
        Initialize phone number with validation.
        
        Args:
            value (str): Phone number string to validate and store
            
        Raises:
            ValueError: If phone number format is invalid
        """
        if not self.validate_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    def validate_phone(self, phone: str) -> bool:
        """
        Validate phone number format.
        
        Checks that the phone number contains exactly 10 digits
        with no other characters.
        
        Args:
            phone (str): Phone number to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        return phone.isdigit() and len(phone) == 10


class Birthday(Field):
    """
    Birthday field with date validation and parsing.
    
    Stores birthday dates in DD.MM.YYYY format and provides
    date object access for calculations and comparisons.
    
    Format: DD.MM.YYYY (e.g., "15.03.1985")
    
    Attributes:
        date (datetime.date): Parsed date object for calculations
        value (str): Original string representation
    
    Raises:
        ValueError: If date format is invalid or date doesn't exist
    """
    
    def __init__(self, value: str) -> None:
        """
        Initialize birthday with date validation.
        
        Args:
            value (str): Birthday string in DD.MM.YYYY format
            
        Raises:
            ValueError: If date format is invalid
        """
        try:
            # Parse the date and store both string and date object
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        """
        Return formatted date string.
        
        Returns:
            str: Date in DD.MM.YYYY format
        """
        return self.date.strftime("%d.%m.%Y")


class Email(Field):
    """
    Email field with format validation.
    
    Validates email addresses using regex pattern matching
    to ensure they follow basic email format rules.
    
    Validation Rules:
        - Must contain @ symbol
        - Must have text before and after @
        - Must have domain with at least one dot
        - Example: user@domain.com
    
    Raises:
        ValueError: If email format is invalid
    """
    
    def __init__(self, value: str) -> None:
        """
        Initialize email with format validation.
        
        Args:
            value (str): Email address to validate and store
            
        Raises:
            ValueError: If email format is invalid
        """
        if not self.validate_email(value):
            raise ValueError("Invalid email format")
        super().__init__(value)

    def validate_email(self, email: str) -> bool:
        """
        Validate email format using regex.
        
        Checks for basic email structure: text@domain.extension
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if valid email format, False otherwise
        """
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


class Address(Field):
    """
    Address field for storing contact location information.
    
    Stores physical address information without specific validation.
    Can contain street address, city, state, postal code, etc.
    
    No format restrictions as addresses vary greatly by region.
    """
    pass


class Record:
    """
    Complete contact record containing all contact information.
    
    Manages all aspects of a single contact including name, multiple phone numbers,
    email, birthday, and address. Provides methods for adding, editing, and
    removing contact information.
    
    Attributes:
        name (Name): Contact's full name (required)
        phones (List[Phone]): List of phone numbers (can have multiple)
        birthday (Optional[Birthday]): Contact's birthday
        email (Optional[Email]): Contact's email address
        address (Optional[Address]): Contact's physical address
    """
    
    def __init__(self, name: str) -> None:
        """
        Initialize a new contact record.
        
        Args:
            name (str): Full name of the contact (required field)
        """
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None

    def add_phone(self, phone: str) -> None:
        """
        Add a new phone number to the contact.
        
        Contacts can have multiple phone numbers (home, work, mobile, etc.).
        Each phone number is validated before being added.
        
        Args:
            phone (str): Phone number to add (must be 10 digits)
            
        Raises:
            ValueError: If phone number format is invalid
        """
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """
        Remove a specific phone number from the contact.
        
        Args:
            phone (str): Phone number to remove
            
        Raises:
            ValueError: If phone number is not found in contact
        """
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone {phone} not found")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """
        Replace an existing phone number with a new one.
        
        Args:
            old_phone (str): Current phone number to replace
            new_phone (str): New phone number (must be valid format)
            
        Raises:
            ValueError: If old phone is not found or new phone is invalid
        """
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            # Validate new phone by creating Phone object, then use its value
            phone_to_edit.value = Phone(new_phone).value
        else:
            raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone: str) -> Optional[Phone]:
        """
        Find a specific phone number in the contact's phone list.
        
        Args:
            phone (str): Phone number to search for
            
        Returns:
            Optional[Phone]: Phone object if found, None otherwise
        """
        return next((p for p in self.phones if p.value == phone), None)

    def add_birthday(self, birthday: str) -> None:
        """
        Add or update the contact's birthday.
        
        Args:
            birthday (str): Birthday in DD.MM.YYYY format
            
        Raises:
            ValueError: If date format is invalid
        """
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        """
        Add or update the contact's email address.
        
        Args:
            email (str): Email address in valid format
            
        Raises:
            ValueError: If email format is invalid
        """
        self.email = Email(email)

    def add_address(self, address: str) -> None:
        """
        Add or update the contact's physical address.
        
        Args:
            address (str): Physical address (no format restrictions)
        """
        self.address = Address(address)

    def edit_field(self, field_name: str, new_value: str) -> None:
        """
        Edit any contact field by name.
        
        Provides a generic interface for updating contact information.
        Validates the new value according to field-specific rules.
        
        Args:
            field_name (str): Name of field to edit ('name', 'email', 'address', 'birthday')
            new_value (str): New value for the field
            
        Raises:
            ValueError: If field name is not supported or value is invalid
        """
        if field_name == "name":
            self.name = Name(new_value)
        elif field_name == "email":
            self.email = Email(new_value)
        elif field_name == "address":
            self.address = Address(new_value)
        elif field_name == "birthday":
            self.birthday = Birthday(new_value)
        else:
            raise ValueError(f"Field '{field_name}' is not supported for editing.")

    def __str__(self) -> str:
        """
        Return a string representation of the complete contact record.
        
        Returns:
            str: Formatted string containing all contact information
        """
        phones_str = '; '.join(p.value for p in self.phones)
        bday = f", birthday: {self.birthday}" if self.birthday else ""
        email = f", email: {self.email}" if self.email else ""
        addr = f", address: {self.address}" if self.address else ""
        return f"Name: {self.name.value}, phones: {phones_str}{bday}{email}{addr}"


class AddressBook(UserDict):
    """
    Address book collection for managing multiple contact records.
    
    Extends UserDict to provide dictionary-like interface for storing
    and retrieving contacts by name. Includes advanced features like
    birthday tracking and contact management operations.
    
    The address book uses contact names as keys and Record objects as values.
    Provides methods for adding, finding, deleting, and renaming contacts,
    as well as birthday reminder functionality.
    
    Attributes:
        data (Dict[str, Record]): Dictionary storing contact records by name
    """
    
    def add_record(self, record: Record) -> None:
        """
        Add a new contact record to the address book.
        
        Uses the contact's name as the key for storage and retrieval.
        If a contact with the same name already exists, it will be replaced.
        
        Args:
            record (Record): Contact record to add to the address book
        """
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """
        Find a contact by name.
        
        Performs exact name matching to locate contacts.
        
        Args:
            name (str): Name of the contact to find
            
        Returns:
            Optional[Record]: Contact record if found, None otherwise
        """
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """
        Delete a contact from the address book.
        
        Args:
            name (str): Name of the contact to delete
            
        Raises:
            KeyError: If no contact with the specified name exists
        """
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"No record with name '{name}'")

    def rename_contact(self, old_name: str, new_name: str) -> None:
        """
        Rename a contact in the address book.
        
        Args:
            old_name (str): Current name of the contact
            new_name (str): New name for the contact
            
        Raises:
            KeyError: If contact with old_name doesn't exist
            ValueError: If contact with new_name already exists
        """
        # Check if old contact exists
        if old_name not in self.data:
            raise KeyError(f"Contact '{old_name}' not found")
        
        # Check if new name already exists
        if new_name in self.data:
            raise ValueError(f"Contact '{new_name}' already exists")
        
        # Get the record and update its name
        record = self.data[old_name]
        record.name = Name(new_name)
        
        # Move the record to the new key and remove the old one
        self.data[new_name] = record
        del self.data[old_name]

    def get_upcoming_birthdays(self, days_ahead: int = 7) -> List[Dict[str, str]]:
        """
        Get list of contacts with upcoming birthdays within specified days.
        
        Identifies contacts whose birthdays fall within the next N days,
        including handling of year transitions and weekend adjustments.
        
        Args:
            days_ahead (int or list): Number of days to look ahead for birthdays (default: 7).
            
        Returns:
            List[Dict[str, str]]: List of birthday reminders with name and date
        """
        from datetime import datetime, timedelta
        
        today = date.today()
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            # Calculate this year's birthday
            bday = record.birthday.date.replace(year=today.year)
            
            # If birthday already passed this year, use next year
            if bday < today:
                bday = bday.replace(year=today.year + 1)

            # Check if birthday is within the specified days
            delta = (bday - today).days
            if 0 <= delta <= days_ahead:
                # Adjust for weekends (move to Monday if weekend)
                celebration_date = bday
                if celebration_date.weekday() >= 5:  # Saturday (5) or Sunday (6)
                    days_until_monday = 7 - celebration_date.weekday()
                    celebration_date = celebration_date + timedelta(days=days_until_monday)
                
                result.append({
                    "name": record.name.value,
                    "congratulation_date": celebration_date.strftime("%d.%m.%Y")
                })

        return result


