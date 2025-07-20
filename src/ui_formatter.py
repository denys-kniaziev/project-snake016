from typing import List, Dict
from colorama import init, Fore, Back, Style
from prettytable import PrettyTable
from .address_book import Record
from .note_book import Note

# Initialize colorama for cross-platform colored output
init(autoreset=True)


class Colors:
    """Color constants for consistent styling throughout the application."""
    
    # Text colors
    SUCCESS = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.CYAN
    PROMPT = Fore.BLUE
    HIGHLIGHT = Fore.MAGENTA
    
    # Styles
    BOLD = Style.BRIGHT
    DIM = Style.DIM
    RESET = Style.RESET_ALL
    
    # Background colors
    BG_SUCCESS = Back.GREEN
    BG_ERROR = Back.RED
    BG_WARNING = Back.YELLOW


class UIFormatter:
    """Handles all UI formatting and display logic."""
    
    @staticmethod
    def print_header(title: str, width: int = 60) -> None:
        """Print a styled header with title."""
        border = "=" * width
        print(f"\n{Colors.BOLD}{Colors.INFO}{border}")
        print(f"{title:^{width}}")
        print(f"{border}{Colors.RESET}")
    
    @staticmethod
    def print_success(message: str) -> None:
        """Print a success message in green."""
        print(f"{Colors.SUCCESS}✅ {message}{Colors.RESET}")
    
    @staticmethod
    def print_error(message: str) -> None:
        """Print an error message in red."""
        print(f"{Colors.ERROR}❌ {message}{Colors.RESET}")
    
    @staticmethod
    def print_warning(message: str) -> None:
        """Print a warning message in yellow."""
        print(f"{Colors.WARNING}⚠️  {message}{Colors.RESET}")
    
    @staticmethod
    def print_info(message: str) -> None:
        """Print an info message in cyan."""
        print(f"{Colors.INFO}ℹ️  {message}{Colors.RESET}")
    
    @staticmethod
    def print_separator(char: str = "-", width: int = 50) -> None:
        """Print a separator line."""
        print(f"{Colors.DIM}{char * width}{Colors.RESET}")
    
    @staticmethod
    def format_contacts_table(records: List[Record]) -> str:
        """Format contacts as a pretty table."""
        if not records:
            return f"{Colors.WARNING}No contacts found.{Colors.RESET}"
        
        table = PrettyTable()
        table.field_names = ["Name", "Phones", "Email", "Birthday", "Address"]
        table.align = "l"  # Left align all columns
        table.max_width = 20  # Max width per column
        
        for record in records:
            phones = "; ".join(p.value for p in record.phones) if record.phones else "No phones"
            email = str(record.email) if record.email else "No email"
            birthday = str(record.birthday) if record.birthday else "No birthday"
            address = str(record.address) if record.address else "No address"
            
            table.add_row([
                record.name.value,
                phones,
                email,
                birthday,
                address
            ])
        
        return f"{Colors.INFO}{table}{Colors.RESET}"
    
    @staticmethod
    def format_single_contact(record: Record) -> str:
        """Format a single contact with colored fields."""
        output = []
        output.append(f"{Colors.BOLD}{Colors.HIGHLIGHT}📞 Contact Details{Colors.RESET}")
        output.append(f"{Colors.INFO}Name:{Colors.RESET} {Colors.BOLD}{record.name.value}{Colors.RESET}")
        
        if record.phones:
            phones_str = ", ".join(p.value for p in record.phones)
            output.append(f"{Colors.INFO}Phones:{Colors.RESET} {phones_str}")
        else:
            output.append(f"{Colors.INFO}Phones:{Colors.RESET} {Colors.DIM}No phones{Colors.RESET}")
        
        if record.email:
            output.append(f"{Colors.INFO}Email:{Colors.RESET} {record.email}")
        else:
            output.append(f"{Colors.INFO}Email:{Colors.RESET} {Colors.DIM}No email{Colors.RESET}")
        
        if record.birthday:
            output.append(f"{Colors.INFO}Birthday:{Colors.RESET} {record.birthday}")
        else:
            output.append(f"{Colors.INFO}Birthday:{Colors.RESET} {Colors.DIM}No birthday{Colors.RESET}")
        
        if record.address:
            output.append(f"{Colors.INFO}Address:{Colors.RESET} {record.address}")
        else:
            output.append(f"{Colors.INFO}Address:{Colors.RESET} {Colors.DIM}No address{Colors.RESET}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_notes_table(notes: List[Note]) -> str:
        """Format notes as a pretty table."""
        if not notes:
            return f"{Colors.WARNING}No notes found.{Colors.RESET}"
        
        table = PrettyTable()
        table.field_names = ["Title", "Content", "Tags"]
        table.align = "l"
        table.max_width = 30
        
        for note in notes:
            content = note.content[:50] + "..." if len(note.content) > 50 else note.content
            tags = ", ".join(note.tags) if note.tags else "No tags"
            
            table.add_row([
                note.title,
                content,
                tags
            ])
        
        return f"{Colors.INFO}{table}{Colors.RESET}"
    
    @staticmethod
    def format_single_note(note: Note) -> str:
        """Format a single note with colored fields."""
        output = []
        output.append(f"{Colors.BOLD}{Colors.HIGHLIGHT}📝 Note Details{Colors.RESET}")
        output.append(f"{Colors.INFO}Title:{Colors.RESET} {Colors.BOLD}{note.title}{Colors.RESET}")
        
        # Handle multi-line content with proper formatting
        content_lines = note.content.split('\n')
        if len(content_lines) == 1:
            output.append(f"{Colors.INFO}Content:{Colors.RESET} {note.content}")
        else:
            output.append(f"{Colors.INFO}Content:{Colors.RESET}")
            for line in content_lines:
                output.append(f"  {line}")
        
        if note.tags:
            tags_str = ", ".join(f"{Colors.HIGHLIGHT}{tag}{Colors.RESET}" for tag in note.tags)
            output.append(f"{Colors.INFO}Tags:{Colors.RESET} {tags_str}")
        else:
            output.append(f"{Colors.INFO}Tags:{Colors.RESET} {Colors.DIM}No tags{Colors.RESET}")
        
        return "\n".join(output)
    
    @staticmethod
    def format_birthdays_table(birthdays: List[Dict[str, str]]) -> str:
        """Format upcoming birthdays as a pretty table."""
        if not birthdays:
            return f"{Colors.WARNING}No upcoming birthdays.{Colors.RESET}"
        
        table = PrettyTable()
        table.field_names = ["Name", "Birthday Date"]
        table.align = "l"
        
        for birthday in birthdays:
            table.add_row([
                birthday["name"],
                birthday["congratulation_date"]
            ])
        
        return f"{Colors.SUCCESS}🎂 Upcoming Birthdays:\n{Colors.INFO}{table}{Colors.RESET}"
    
    @staticmethod
    def format_help_table(commands_by_category: Dict[str, List]) -> str:
        """Format help commands as organized tables by category."""
        output = []
        output.append(f"{Colors.BOLD}{Colors.INFO}📚 Available Commands{Colors.RESET}")
        
        for category, commands in commands_by_category.items():
            if not commands:
                continue
                
            output.append(f"\n{Colors.BOLD}{Colors.HIGHLIGHT}{category} Commands:{Colors.RESET}")
            
            table = PrettyTable()
            table.field_names = ["Command", "Description"]
            table.align["Command"] = "l"
            table.align["Description"] = "l"
            table.max_width["Command"] = 100
            table.max_width["Description"] = 100

            for cmd in commands:
                table.add_row([cmd.usage, cmd.description])
            
            output.append(f"{Colors.INFO}{str(table)}{Colors.RESET}")
        
        return "\n".join(output)
    
    @staticmethod
    def print_welcome() -> None:
        """Print a styled welcome message."""
        print(f"""
{Colors.BOLD}{Colors.INFO}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       🏠 Welcome to the Address Book Assistant Bot! 📚       ║
║                                                              ║
║       Your personal contact and note management system       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.SUCCESS}✨ Features:{Colors.RESET}
  • {Colors.INFO}📞 Contact Management{Colors.RESET} - Add, edit, search contacts
  • {Colors.INFO}📝 Note Taking{Colors.RESET} - Create and organize notes with tags  
  • {Colors.INFO}🎂 Birthday Tracking{Colors.RESET} - Never miss important dates
  • {Colors.INFO}🔍 Smart Search{Colors.RESET} - Find contacts and notes quickly
  • {Colors.INFO}💾 Auto-Save{Colors.RESET} - Your data is always preserved

{Colors.PROMPT}💡 Tips:{Colors.RESET}
  • Use {Colors.BOLD}Tab{Colors.RESET} for command autocomplete
  • Use {Colors.BOLD}arrow keys{Colors.RESET} for command history
  • Type {Colors.BOLD}'help'{Colors.RESET} to see all available commands
  • Type {Colors.BOLD}'exit'{Colors.RESET} or press {Colors.BOLD}Ctrl+C{Colors.RESET} to quit
""")
    
    @staticmethod
    def print_goodbye() -> None:
        """Print a styled goodbye message."""
        print(f"""
{Colors.SUCCESS}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   👋 Thank you for using Address Book Assistant Bot!         ║
║                                                              ║
║                   Your data has been saved.                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}

{Colors.INFO}See you next time! 🌟{Colors.RESET}
""")


def format_command_result(result: str, command_type: str = "info") -> str:
    """
    Format command results with appropriate styling.
    
    Args:
        result: The result message from a command
        command_type: Type of result (success, error, info, warning)
    
    Returns:
        Formatted result string with colors
    """
    if not result or result.strip() == "":
        return ""
    
    # Detect result type from content if not specified
    if command_type == "auto":
        result_lower = result.lower()
        if any(word in result_lower for word in ["error", "failed", "not found", "invalid"]):
            command_type = "error"
        elif any(word in result_lower for word in ["added", "updated", "deleted", "success"]):
            command_type = "success"
        elif any(word in result_lower for word in ["warning", "already exists"]):
            command_type = "warning"
        else:
            command_type = "info"
    
    # Apply appropriate styling
    if command_type == "error":
        return f"{Colors.ERROR}{result}{Colors.RESET}"
    elif command_type == "success":
        return f"{Colors.SUCCESS}{result}{Colors.RESET}"
    elif command_type == "warning":
        return f"{Colors.WARNING}{result}{Colors.RESET}"
    else:
        return f"{Colors.INFO}{result}{Colors.RESET}"
