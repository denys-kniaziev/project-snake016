from .commands import parse_input
from .data_persistence import save_addressbook, load_addressbook, save_notebook, load_notebook
from .command_suggester import command_suggester
from .command_registry import registry
from .ui_formatter import UIFormatter, format_command_result


def execute_command(command_name: str, args: list, addressbook, notebook) -> tuple[str, bool]:
    """
    Execute a command using the centralized registry.
    
    This function handles all command execution logic, including:
    - Command validation through the registry
    - Proper argument passing based on command category
    - Automatic save logic based on command metadata
    
    Args:
        command_name: The name of the command to execute
        args: List of arguments for the command
        addressbook: The address book instance
        notebook: The notebook instance
        
    Returns:
        tuple: (result_message, should_exit)
    """
    # Get command metadata from registry
    cmd_obj = registry.get_command(command_name)
    
    if not cmd_obj:
        # Command not found - provide intelligent suggestions
        suggestion = command_suggester.analyze_and_suggest(command_name)
        return suggestion, False
    
    # Handle special exit commands
    if command_name in ["exit", "close"]:
        return "", True  # Signal to exit
    
    try:
        # Execute command based on its category
        if cmd_obj.category == "General":
            # General commands (help, etc.)
            result = cmd_obj.handler(args)
        elif cmd_obj.category == "Address Book":
            # Address book commands need the addressbook instance
            result = cmd_obj.handler(args, addressbook)
            # Save addressbook if command requires it
            if cmd_obj.save_addressbook:
                save_addressbook(addressbook, silentmode=True)
        elif cmd_obj.category == "Note Book":
            # Note book commands need the notebook instance
            result = cmd_obj.handler(args, notebook)
            # Save notebook if command requires it
            if cmd_obj.save_notebook:
                save_notebook(notebook, silentmode=True)
        else:
            return f"Unknown command category: {cmd_obj.category}", False
        
        return result, False
        
    except Exception as e:
        # Handle command execution errors gracefully
        return f"Error executing command: {str(e)}", False


def main():
    """
    Main function that runs the assistant bot.
    
    This simplified main loop uses the centralized command registry
    to eliminate all duplication and provide a clean, maintainable
    command execution system.
    """
    # Load data at startup
    addressbook = load_addressbook(silentmode=True)
    notebook = load_notebook(silentmode=True)

    # Show welcome message with beautiful formatting
    UIFormatter.print_welcome()

    try:
        while True:
            # Get user input with autocomplete support
            user_input = command_suggester.get_user_input("🔹 Enter a command: ")
            
            # Parse the input into command and arguments
            command, args = parse_input(user_input)
            
            # Skip empty inputs
            if command == "":
                continue
            
            # Execute the command using the registry
            result, should_exit = execute_command(command, args, addressbook, notebook)
            
            # Print result with appropriate formatting if there is one
            if result:
                formatted_result = format_command_result(result, "auto")
                print(formatted_result)
            
            # Exit if requested
            if should_exit:
                break
    
    except KeyboardInterrupt:
        UIFormatter.print_info("\nReceived Ctrl+C, exiting...")
    
    finally:
        # Save data before exiting
        UIFormatter.print_info("Saving data...")
        save_addressbook(addressbook, silentmode=True)
        save_notebook(notebook, silentmode=True)
        UIFormatter.print_goodbye()


if __name__ == "__main__":
    main()