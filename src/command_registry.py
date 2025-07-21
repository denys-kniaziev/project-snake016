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
    Represents a single command with all its metadata.
    
    Attributes:
        name (str): The command name as typed by user (e.g., "add-contact")
        handler (Callable): The function that handles this command
        description (str): Short description for help text
        usage (str): Usage example with parameters
        category (str): Category for grouping in help (e.g., "Address Book")
        save_addressbook (bool): Whether to save address book after execution
        save_notebook (bool): Whether to save notebook after execution
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
    Centralized registry for all application commands.
    
    This class manages all commands in the application, providing:
    - Command registration and lookup
    - Automatic help text generation
    - Command name listing for autocomplete
    - Metadata management (save flags, categories, etc.)
    """
    
    def __init__(self):
        """Initialize the registry and register all commands."""
        self.commands: Dict[str, Command] = {}
        self._register_all_commands()
    
    def _register_all_commands(self):
        """
        Register all application commands with their metadata.
        
        This method defines every command in the application. To add a new command:
        1. Create the handler function in commands.py
        2. Import it at the top of this file
        3. Add a _register_command() call here
        """
        
        # === GENERAL COMMANDS ===
        # Commands for help and application control
        
        self._register_command(
            name="help",
            handler=lambda args, *_: self.get_help_text(),  # Special handler that returns help
            description="Show this help message",
            usage="help",
            category="General"
        )
        
        self._register_command(
            name="exit",
            handler=lambda args, *_: "exit",  # Special return value to signal exit
            description="Exit the program",
            usage="exit",
            category="General"
        )
        
        self._register_command(
            name="close",
            handler=lambda args, *_: "exit",  # Alias for exit
            description="Exit the program", 
            usage="close",
            category="General"
        )
        
        # === ADDRESS BOOK COMMANDS ===
        # Commands for managing contacts, birthdays, addresses, emails
        
        # Adding contacts
        self._register_command(
            name="add-contact",
            handler=add_contact,
            description="Add a new contact with phone, optional email and birthday",
            usage="add-contact <name> <phone> [email] [birthday]",
            category="Address Book",
            save_addressbook=True
        )
        
        # Editing commands (with upsert logic)
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
        
        # Viewing/Managing commands
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
        # Commands for managing notes, tags, and note operations
        
        self._register_command(
            name="add-note",
            handler=add_note,
            description="Add a new note",
            usage='add-note "title" "content" "tag1,tag2"',
            category="Note Book",
            save_notebook=True  # Save after adding note
        )
        
        self._register_command(
            name="remove-note",
            handler=remove_note,
            description="Remove a note by title",
            usage='remove-note "title"',
            category="Note Book",
            save_notebook=True  # Save after removal
        )
        
        self._register_command(
            name="show-all-notes",
            handler=show_all_notes,
            description="Show all notes",
            usage="show-all-notes",
            category="Note Book"
            # No save needed - read-only operation
        )
        
        self._register_command(
            name="show-note",
            handler=show_note,
            description="Show a specific note by title",
            usage='show-note "title"',
            category="Note Book"
            # No save needed - read-only operation
        )
        
        self._register_command(
            name="search-notes",
            handler=search_notes,
            description="Search notes by title or content",
            usage='search-notes "query"',
            category="Note Book"
            # No save needed - read-only operation
        )
        
        self._register_command(
            name="edit-note",
            handler=edit_note,
            description="Edit an existing note",
            usage='edit-note "title" "new_title" "new_content" "new_tags"',
            category="Note Book",
            save_notebook=True  # Save after editing
        )
        
        self._register_command(
            name="search-notes-by-tag",
            handler=search_notes_by_tag,
            description="Search notes by a specific tag",
            usage='search-notes-by-tag "tag"',
            category="Note Book"
            # No save needed - read-only operation
        )
        
        self._register_command(
            name="sort-notes-by-tag",
            handler=sort_notes_by_tag,
            description="Sort notes by their tags",
            usage="sort-notes-by-tag",
            category="Note Book"
            # No save needed - read-only operation
        )
        
        self._register_command(
            name="add-tag-to-note",
            handler=add_tag_to_note,
            description="Add a tag to an existing note",
            usage='add-tag-to-note "title" "tag"',
            category="Note Book",
            save_notebook=True  # Save after adding tag
        )
        
        self._register_command(
            name="remove-tag-from-note",
            handler=remove_tag_from_note,
            description="Remove a tag from an existing note",
            usage='remove-tag-from-note "title" "tag"',
            category="Note Book",
            save_notebook=True  # Save after removing tag
        )
    
    def _register_command(self, name: str, handler: Callable, description: str, 
                         usage: str, category: str, save_addressbook: bool = False, 
                         save_notebook: bool = False):
        """
        Register a single command in the registry.
        
        Args:
            name: Command name as typed by user
            handler: Function that handles the command
            description: Short description for help
            usage: Usage example with parameters
            category: Category for help grouping
            save_addressbook: Whether to save address book after execution
            save_notebook: Whether to save notebook after execution
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
        """
        Get a command by name.
        
        Args:
            name: The command name to look up
            
        Returns:
            Command object if found, None otherwise
        """
        return self.commands.get(name)
    
    def get_all_command_names(self) -> List[str]:
        """
        Get list of all command names for autocomplete.
        
        Returns:
            List of all command names sorted alphabetically
        """
        return sorted(self.commands.keys())
    
    def get_help_text(self) -> str:
        """
        Generate formatted help text from registered commands.
        
        The help text is organized by category with proper formatting:
        - General commands first
        - Address Book commands second  
        - Note Book commands third
        - Usage examples aligned for readability
        
        Returns:
            Formatted help text string
        """
        # Group commands by category, preserving order
        categories = ["General", "Address Book", "Note Book"]
        commands_by_category = {}
        
        for category in categories:
            # Find commands in this category
            category_commands = [cmd for cmd in self.commands.values() 
                               if cmd.category == category]
            
            if category_commands:
                # Sort commands within category by name
                category_commands.sort(key=lambda x: x.name)
                commands_by_category[category] = category_commands
        
        return UIFormatter.format_help_table(commands_by_category)
    
    def is_valid_command(self, name: str) -> bool:
        """
        Check if a command name is valid.
        
        Args:
            name: Command name to check
            
        Returns:
            True if command exists, False otherwise
        """
        return name in self.commands


# Global registry instance - used throughout the application
# This provides a single point of access to all command metadata
registry = CommandRegistry()
