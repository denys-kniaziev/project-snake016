import re
from collections import UserDict
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict


class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    """Поле для імені контакту."""
    pass


class Phone(Field):
    """Поле для номера телефону з валідацією (10 цифр)."""
    def __init__(self, value: str) -> None:
        if not self.validate_phone(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    def validate_phone(self, phone: str) -> bool:
        return phone.isdigit() and len(phone) == 10


class Birthday(Field):
    """Поле для дня народження. Формат: DD.MM.YYYY"""
    def __init__(self, value: str) -> None:
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        return self.date.strftime("%d.%m.%Y")


class Email(Field):
    """Поле для зберігання email з валідацією."""
    def __init__(self, value: str) -> None:
        if not self.validate_email(value):
            raise ValueError("Invalid email format")
        super().__init__(value)

    def validate_email(self, email: str) -> bool:
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


class Address(Field):
    """Поле для адреси."""
    pass


class Record:
    """Клас для зберігання повної інформації про контакт."""
    def __init__(self, name: str) -> None:
        self.name: Name = Name(name)
        self.phones: List[Phone] = []
        self.birthday: Optional[Birthday] = None
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None

    def add_phone(self, phone: str) -> None:
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone {phone} not found")

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            phone_to_edit.value = Phone(new_phone).value
        else:
            raise ValueError(f"Phone {old_phone} not found")

    def find_phone(self, phone: str) -> Optional[Phone]:
        return next((p for p in self.phones if p.value == phone), None)

    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def add_email(self, email: str) -> None:
        self.email = Email(email)

    def add_address(self, address: str) -> None:
        self.address = Address(address)

    def edit_field(self, field_name: str, new_value: str) -> None:
        """Редагування полів: name, email, address, birthday"""
        if field_name == "name":
            self.name = Name(new_value)
        elif field_name == "email":
            self.email = Email(new_value)
        elif field_name == "address":
            self.address = Address(new_value)
        elif field_name == "birthday":
            self.birthday = Birthday(new_value)
        else:
            raise ValueError(f"Поле '{field_name}' не підтримується для редагування.")

    def __str__(self) -> str:
        phones_str = '; '.join(p.value for p in self.phones)
        bday = f", birthday: {self.birthday}" if self.birthday else ""
        email = f", email: {self.email}" if self.email else ""
        addr = f", address: {self.address}" if self.address else ""
        return f"Name: {self.name.value}, phones: {phones_str}{bday}{email}{addr}"


class AddressBook(UserDict):
    """Клас адресної книги для зберігання кількох записів."""
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
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

    def get_upcoming_birthdays(self, days_ahead_) -> List[Dict[str, str]]:
        """Отримати список контактів, у яких день народження через вказану кількість днів."""
        today = date.today()
        days_ahead=int(days_ahead_[0])
        target_date = today + timedelta(days=days_ahead)
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.date.replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)

            delta = (bday - today).days
            if 0 <= delta <= days_ahead:
                result.append({
                    "name": record.name.value,
                    "congratulation_date": bday.strftime("%d.%m.%Y")
                })

        return result


