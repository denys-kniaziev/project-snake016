from collections import UserDict
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict


class Field:
    """Base class for record fields."""
    
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Class for storing contact name. Required field."""
    pass


class Phone(Field):
    """Class for storing phone number. Must contain exactly 10 digits."""
    
    def __init__(self, value: str) -> None:
        if not self.validate_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)
    
    def validate_phone(self, phone: str) -> bool:
        """Validate that phone number contains exactly 10 digits."""
        return phone.isdigit() and len(phone) == 10


class Birthday(Field):
    """Class for storing birthday date. Date format: DD.MM.YYYY"""
    
    def __init__(self, value: str) -> None:
        try:
            # Convert string to datetime object to validate format
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
    
    def __str__(self) -> str:
        return self.value


class Record:
    """Class for storing contact information including name, phone numbers and birthday."""
    
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone: str) -> None:
        """Add a phone number to the record."""
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)
    
    def remove_phone(self, phone: str) -> None:
        """Remove a phone number from the record."""
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone {phone} not found in record")
    
    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit an existing phone number."""
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            # Validate new phone number by creating temporary Phone object
            temp_phone = Phone(new_phone)
            phone_to_edit.value = new_phone
        else:
            raise ValueError(f"Phone {old_phone} not found in record")
    
    def find_phone(self, phone: str) -> Optional[Phone]:
        """Find a phone number in the record."""
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None
    
    def add_birthday(self, birthday: str) -> None:
        """Add birthday to the record."""
        self.birthday = Birthday(birthday)

    def __str__(self) -> str:
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    """Class for storing and managing contact records."""
    
    def add_record(self, record: Record) -> None:
        """Add a record to the address book."""
        self.data[record.name.value] = record
    
    def find(self, name: str) -> Optional[Record]:
        """Find a record by name."""
        return self.data.get(name)
    
    def delete(self, name: str) -> None:
        """Delete a record by name."""
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record with name '{name}' not found")
    
    def get_upcoming_birthdays(self) -> List[Dict[str, str]]:
        """
        Get list of contacts with birthdays in the next 7 days.
        
        Returns:
            List of dictionaries containing 'name' and 'congratulation_date'
        """
        upcoming_birthdays = []
        today = date.today()
        next_week = today + timedelta(days=7)
        
        for record in self.data.values():
            if record.birthday is None:
                continue
                
            # Get the birthday date for this year
            birthday_this_year = record.birthday.date.replace(year=today.year)
            
            # If birthday already passed this year, check next year
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)
            
            # Check if birthday is within next 7 days
            if today <= birthday_this_year <= next_week:
                # Adjust for weekends (move to Monday)
                congratulation_date = birthday_this_year
                if congratulation_date.weekday() == 5:  # Saturday
                    congratulation_date = congratulation_date + timedelta(days=2)
                elif congratulation_date.weekday() == 6:  # Sunday
                    congratulation_date = congratulation_date + timedelta(days=1)
                
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })
        
        return upcoming_birthdays


# Example usage and testing
if __name__ == "__main__":
    # Create new address book
    book = AddressBook()

    # Create record for John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("15.03.1990")

    # Add John's record to address book
    book.add_record(john_record)

    # Create and add new record for Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("20.07.1985")
    book.add_record(jane_record)

    # Print all records in the book
    for name, record in book.data.items():
        print(record)

    # Test upcoming birthdays
    upcoming = book.get_upcoming_birthdays()
    print("\nUpcoming birthdays:")
    for birthday in upcoming:
        print(f"{birthday['name']}: {birthday['congratulation_date']}")