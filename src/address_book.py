import re
from collections import UserDict
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict


class Field:
    """Base class for all contact fields. Stores and displays a value."""

    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Field for contact name."""
    pass


class Phone(Field):
    """
    Phone number with validation.

    Formats:
    - 10-digit local
    - +[country][number], 7–15 digits
    - Without +, 11–16 digits
    """

    def __init__(self, value: str) -> None:
        if not self.validate_phone(value):
            raise ValueError(
                "Phone number must be either:\n"
                "- 10 digits for local numbers (e.g., 1234567890)\n"
                "- +[country code][number] for international (e.g., +1234567890)\n"
                "- 11-16 digits for country code without + (e.g., 1234567890123)"
            )
        super().__init__(value)

    def validate_phone(self, phone: str) -> bool:
        """
        Validate supported phone formats:
        - Local: 10 digits
        - International: + and 7–15 digits
        - Alternative: 11–16 digits (no +)
        """
        phone = phone.strip()
        if not phone:
            return False
        if phone.isdigit() and len(phone) == 10:
            return True
        if phone.startswith('+'):
            digits_part = phone[1:]
            if digits_part.isdigit() and 7 <= len(digits_part) <= 15:
                return True
        if phone.isdigit() and 11 <= len(phone) <= 16:
            return True
        return False


class Birthday(Field):
    """
    Birthday in DD.MM.YYYY format.

    Parses and stores as both string and date.
    """

    def __init__(self, value: str) -> None:
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self.date.strftime("%d.%m.%Y")


class Email(Field):
    """Email field with basic format validation."""

    def __init__(self, value: str) -> None:
        if not self.validate_email(value):
            raise ValueError("Invalid email format")
        super().__init__(value)

    def validate_email(self, email: str) -> bool:
        """Validates basic structure: text@domain.ext"""
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


class Address(Field):
    """Free-form address field without validation."""
    pass


class Record:
    """
    Full contact record with name, phones, birthday, email, and address.
    Supports editing and searching.
    """

    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None

    def add_phone(self, phone: str) -> None:
        """Add validated phone number."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Remove phone number if found."""
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone {phone} not found")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Replace existing phone number with a new one."""
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = Phone(new_phone).value
        else:
            raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone: str) -> Optional[Phone]:
        """Search for phone number in list."""
        return next((p for p in self.phones if p.value == phone), None)

    def add_birthday(self, birthday: str) -> None:
        """Set or update birthday."""
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        """Set or update email."""
        self.email = Email(email)

    def add_address(self, address: str) -> None:
        """Set or update address."""
        self.address = Address(address)

    def edit_field(self, field_name: str, new_value: str) -> None:
        """Edit supported fields by name."""
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
        """Return string summary of the contact."""
        phones_str = '; '.join(p.value for p in self.phones)
        bday = f", birthday: {self.birthday}" if self.birthday else ""
        email = f", email: {self.email}" if self.email else ""
        addr = f", address: {self.address}" if self.address else ""
        return f"Name: {self.name.value}, phones: {phones_str}{bday}{email}{addr}"


class AddressBook(UserDict):
    """
    Collection of contact records.

    Provides dictionary-like access and birthday reminders.
    """

    def add_record(self, record: Record) -> None:
        """Add or replace contact by name."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        """Find contact by name."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Delete contact by name."""
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"No record with name '{name}'")

    def rename_contact(self, old_name: str, new_name: str) -> None:
        """Rename a contact, updating key and internal name."""
        if old_name not in self.data:
            raise KeyError(f"Contact '{old_name}' not found")
        if new_name in self.data:
            raise ValueError(f"Contact '{new_name}' already exists")
        record = self.data[old_name]
        record.name = Name(new_name)
        self.data[new_name] = record
        del self.data[old_name]

    def get_upcoming_birthdays(self, days_ahead: int = 7) -> List[Dict[str, str]]:
        """
        Return list of upcoming birthdays within N days.

        Adjusts for weekends by shifting to Monday.
        """
        today = date.today()
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.date.replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)

            delta = (bday - today).days
            if 0 <= delta <= days_ahead:
                celebration_date = bday
                if celebration_date.weekday() >= 5:
                    days_until_monday = 7 - celebration_date.weekday()
                    celebration_date += timedelta(days=days_until_monday)

                result.append({
                    "name": record.name.value,
                    "congratulation_date": celebration_date.strftime("%d.%m.%Y")
                })

        return result
