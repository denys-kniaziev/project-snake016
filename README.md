# Address Book Assistant Bot 📚

A modern, feature-rich command-line interface for managing contacts and notes with an intuitive user experience.

## ✨ Features

### 📞 Contact Management
- **Add contacts** with names, multiple phone numbers, emails, birthdays, and addresses
- **Edit contact information** individually (name, phone, email, birthday, address)
- **Search contacts** by name or phone number
- **Delete contacts** with confirmation
- **Phone management** - add/remove multiple phone numbers per contact

### 📝 Note Taking
- **Create notes** with titles, content, and tags
- **Edit existing notes** (title, content, tags)
- **Search notes** by content or title
- **Tag-based organization** - add/remove tags and search by tags
- **Sort notes** alphabetically by tags

### 🎂 Birthday Tracking
- **Birthday reminders** - view upcoming birthdays within a specified timeframe
- **Weekend adjustment** - automatically moves celebrations to Monday if birthday falls on weekend
- **Smart date handling** - handles year transitions and leap years

### 🔍 Smart Features
- **Multi-word support** - use quotes for multi-word titles and content
- **Auto-complete** - Tab completion for commands
- **Command history** - Use arrow keys to navigate previous commands
- **Smart search** - case-insensitive searching across all fields
- **Data persistence** - automatic saving and loading of data

### 🎨 Modern UI/UX
- **Colorized output** - consistent color scheme throughout the application
- **Pretty tables** - organized display of contacts and notes
- **Interactive prompts** - user-friendly command interface
- **Error handling** - helpful error messages and suggestions

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Install

1. **Clone or download** the project to your local machine

2. **Navigate to the project directory**

3. **Install the package:**
   ```bash
   pip install -e .
   ```

### Usage

After installation, start the application from anywhere:

```bash
address-book
```

## 📖 Quick Start Guide

### Basic Commands

**Contact Management:**
```bash
add-contact "John Doe"                    # Add a new contact
add-phone "John Doe" 1234567890          # Add phone number
edit-email "John Doe" john@example.com   # Add/edit email
edit-birthday "John Doe" 15.03.1985      # Add birthday (DD.MM.YYYY)
show-contact "John Doe"                   # View contact details
show-contacts                             # List all contacts
search-contacts john                      # Search contacts
delete-contact "John Doe"                 # Delete contact
```

**Note Management:**
```bash
add-note "Meeting Notes" "Project discussion" tag1 tag2    # Add note with tags
show-note "Meeting Notes"                                  # View specific note
show-all-notes                                            # List all notes
edit-note "Meeting Notes" --content "Updated content"     # Edit note content
search-notes project                                       # Search notes
search-notes-by-tag work                                  # Search by tag
```

**Birthday Tracking:**
```bash
birthdays                                 # Show upcoming birthdays (7 days)
birthdays 14                            # Show birthdays in next 14 days
```

**Other Commands:**
```bash
help                                     # Show all available commands
exit                                     # Exit the application
```

### Multi-word Support

Use quotes for multi-word arguments:
```bash
add-contact "John Smith Doe"
add-note "My Shopping List" "Buy milk, eggs, and bread"
edit-note "Meeting Notes" --title "Project Meeting Notes"
```

## 🛠️ Dependencies

The application automatically installs these dependencies:
- **prompt-toolkit** (≥3.0.36) - Interactive command line interface
- **colorama** (≥0.4.6) - Cross-platform colored terminal text
- **prettytable** (≥3.6.0) - ASCII table formatting

## 📁 Data Storage

- Contact data is saved to `addressbook.pkl`
- Notes data is saved to `notebook.pkl`
- Data is automatically loaded on startup and saved on exit
- Files are created in the current working directory

## 🔧 Uninstallation

To remove the application:
```bash
pip uninstall address-book-assistant
```

## 💡 Tips

- Use **Tab** for command auto-completion
- Use **arrow keys** to navigate command history
- Type `help` to see all available commands with usage examples
- Use quotes around multi-word arguments
- All data is automatically saved when you exit

## 🏷️ Version

**Version:** 1.0.0  
**Python Support:** 3.8+  
**Platform:** Windows, macOS, Linux
