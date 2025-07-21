from dataclasses import dataclass
from typing import Callable, List, Dict
from ui_formatter import UIFormatter
from commands import (
    # Address book functions
    add_contact, show_contacts, show_contact, search_contacts, delete_contact,
    edit_phone, add_phone, remove_phone, edit_email, edit_birthday, edit_address, edit_name, birthdays,
    # Note book functions
    add_note, remove_note, show_all_notes, show_note, search_notes, edit_note,
    search_notes_by_tag, sort_notes_by_tag, add_tag_to_note, remove_tag_from_note
)


@dataclass
class Command:
    """
    Single command with all metadata.

    Includes name, handler, description, usage, category, and save flags.
    """
    name: str
    handler: Callable
    description: str
    usage: str
    category: str
    save_addressbook: bool = False
    save_notebook: bool = False


class CommandRegistry:
    """
    Registry for all commands.

    Handles registration, lookup, help generation, and metadata access.
    """

    def __init__(self):
        """Initialize and register all commands."""
        self.commands: Dict[str, Command] = {}
        self._register_all_commands()

    def _register_all_commands(self):
        """
        Register all available commands.

        Add new ones by importing and calling _register_command.
        """

        # === GENERAL COMMANDS ===

        self._register_command(
            name="help",
            handler=lambda args, *_: self.get_help_text(),
            description="Show this help message",
            usage="help",
            category="General"
        )

        self._register_command(
            name="exit",
            handler=lambda args, *_: "exit",
            description="Exit the program",
            usage="exit",
            category="General"
        )

        self._register_command(
            name="close",
            handler=lambda args, *_: "exit",
            description="Exit the program",
            usage="close",
            category="General"
        )

        # === ADDRESS BOOK COMMANDS ===

        self._register_command(
            name="add-contact",
            handler=add_contact,
            description="Add a new contact with phone, optional email and birthday",
            usage="add-contact <name> <phone> [email] [birthday]",
            category="Address Book",
            save_addressbook=True
        )

        self._register_command(
            name="edit-phone",
            handler=edit_phone,
            description="Edit existing phone number",
            usage="edit-phone <name> <old_phone> <new_phone>",
            category="Address Book",
            save_addressbook=True
        )

        self._register_command(
            name="add-phone",
            handler=add_phone,
            description="Add additional phone number to contact",
            usage="add-phone <name> <phone>",
            category="Address Book",
            save_addressbook=True
        )

        self._register_command(
            name="remove-phone",
            handler=remove_phone,
            description="Remove specific phone number from contact",
            usage="remove-phone <name> <phone>",
            category="Address Book",
            save_addressbook=True
        )

        self._register_command(
            name="edit-email",
            handler=edit_email,
            description="Add or update email",
            usage="edit-email <name> <new_email>",
            category="Address Book",
            save_addressbook=True
        )

        self._register_command(
            name="edit-birthday",
            handler=edit_birthday,
            description="Add or update birthday",
            usage="edit-birthday <name> <DD.MM.YYYY>",
            category="Address Book",
            save_addressbook=True
        )

        self._register_command(
            name="edit-address",
            handler=edit_address,
            description="Add or update address",
            usage="edit-address <name> <new_address>",
            category="Address Book",
            save_addressbook=True
        )

        self._register_command(
            name="edit-name",
            handler=edit_name,
            description="Rename contact",
            usage="edit-name <old_name> <new_name>",
            category="Address Book",
            save_addressbook=True
        )

        self._register_command(
            name="show-contact",
            handler=show_contact,
            description="Show specific contact",
            usage="show-contact <name>",
            category="Address Book"
        )

        self._register_command(
            name="show-contacts",
            handler=show_contacts,
            description="Show all contacts",
            usage="show-contacts",
            category="Address Book"
        )

        self._register_command(
            name="search-contacts",
            handler=search_contacts,
            description="Search contacts by name, phone, email, or address",
            usage="search-contacts <query>",
            category="Address Book"
        )

        self._register_command(
            name="delete-contact",
            handler=delete_contact,
            description="Delete a contact",
            usage="delete-contact <name>",
            category="Address Book",
            save_addressbook=True
        )

        self._register_command(
            name="birthdays",
            handler=birthdays,
            description="Show upcoming birthdays",
            usage="birthdays <days>",
            category="Address Book"
        )

        # === NOTE BOOK COMMANDS ===

        self._register_command(
            name="add-note",
            handler=add_note,
            description="Add a new note",
            usage='add-note "title" "content" "tag1,tag2"',
            category="Note Book",
            save_notebook=True
        )

        self._register_command(
            name="remove-note",
            handler=remove_note,
            description="Remove a note by title",
            usage='remove-note "title"',
            category="Note Book",
            save_notebook=True
        )

        self._register_command(
            name="show-all-notes",
            handler=show_all_notes,
            description="Show all notes",
            usage="show-all-notes",
            category="Note Book"
        )

        self._register_command(
            name="show-note",
            handler=show_note,
            description="Show a specific note by title",
            usage='show-note "title"',
            category="Note Book"
        )

        self._register_command(
            name="search-notes",
            handler=search_notes,
            description="Search notes by title or content",
            usage='search-notes "query"',
            category="Note Book"
        )

        self._register_command(
            name="edit-note",
            handler=edit_note,
            description="Edit an existing note",
            usage='edit-note "title" "new_title" "new_content" "new_tags"',
            category="Note Book",
            save_notebook=True
        )

        self._register_command(
            name="search-notes-by-tag",
            handler=search_notes_by_tag,
            description="Search notes by tag",
            usage='search-notes-by-tag "tag"',
            category="Note Book"
        )

        self._register_command(
            name="sort-notes-by-tag",
            handler=sort_notes_by_tag,
            description="Sort notes by tags",
            usage="sort-notes-by-tag",
            category="Note Book"
        )

        self._register_command(
            name="add-tag-to-note",
            handler=add_tag_to_note,
            description="Add a tag to a note",
            usage='add-tag-to-note "title" "tag"',
            category="Note Book",
            save_notebook=True
        )

        self._register_command(
            name="remove-tag-from-note",
            handler=remove_tag_from_note,
            description="Remove a tag from a note",
            usage='remove-tag-from-note "title" "tag"',
            category="Note Book",
            save_notebook=True
        )

    def _register_command(self, name: str, handler: Callable, description: str,
                          usage: str, category: str, save_addressbook: bool = False,
                          save_notebook: bool = False):
        """
        Register a command with metadata.

        Stores the command in the registry.
        """
        self.commands[name] = Command(
            name=name,
            handler=handler,
            description=description,
            usage=usage,
            category=category,
            save_addressbook=save_addressbook,
            save_notebook=save_notebook
        )

    def get_command(self, name: str) -> Command | None:
        """Return command by name, or None if not found."""
        return self.commands.get(name)

    def get_all_command_names(self) -> List[str]:
        """Return sorted list of command names."""
        return sorted(self.commands.keys())

    def get_help_text(self) -> str:
        """
        Generate help text grouped by category.

        Includes description and usage for each command.
        """
        categories = ["General", "Address Book", "Note Book"]
        commands_by_category = {}

        for category in categories:
            category_commands = [cmd for cmd in self.commands.values()
                                 if cmd.category == category]
            if category_commands:
                category_commands.sort(key=lambda x: x.name)
                commands_by_category[category] = category_commands

        return UIFormatter.format_help_table(commands_by_category)

    def is_valid_command(self, name: str) -> bool:
        """Check if the given command exists."""
        return name in self.commands


# Global command registry instance
registry = CommandRegistry()
