from commands import parse_input
from data_persistence import save_addressbook, load_addressbook, save_notebook, load_notebook
from command_suggester import command_suggester
from command_registry import registry
from ui_formatter import UIFormatter, format_command_result


def execute_command(command_name: str, args: list, addressbook, notebook) -> tuple[str, bool]:
    """
    Execute a command via the registry.

    Handles validation, dispatch, and autosave logic.
    """
    cmd_obj = registry.get_command(command_name)

    if not cmd_obj:
        return command_suggester.analyze_and_suggest(command_name), False

    if command_name in ["exit", "close"]:
        return "", True

    try:
        if cmd_obj.category == "General":
            result = cmd_obj.handler(args)
        elif cmd_obj.category == "Address Book":
            result = cmd_obj.handler(args, addressbook)
            if cmd_obj.save_addressbook:
                save_addressbook(addressbook, silentmode=True)
        elif cmd_obj.category == "Note Book":
            result = cmd_obj.handler(args, notebook)
            if cmd_obj.save_notebook:
                save_notebook(notebook, silentmode=True)
        else:
            return f"Unknown command category: {cmd_obj.category}", False

        return result, False

    except Exception as e:
        return f"Error executing command: {str(e)}", False


def main():
    """
    Main application loop.

    Loads data, handles input, executes commands, saves on exit.
    """
    addressbook = load_addressbook(silentmode=True)
    notebook = load_notebook(silentmode=True)

    UIFormatter.print_welcome()

    try:
        while True:
            user_input = command_suggester.get_user_input("🔹 Enter a command: ")
            command, args = parse_input(user_input)

            if command == "":
                continue

            result, should_exit = execute_command(command, args, addressbook, notebook)

            if result:
                print(format_command_result(result, "auto"))

            if should_exit:
                break

    except KeyboardInterrupt:
        UIFormatter.print_info("\nReceived Ctrl+C, exiting...")

    finally:
        UIFormatter.print_info("Saving data...")
        save_addressbook(addressbook, silentmode=True)
        save_notebook(notebook, silentmode=True)
        UIFormatter.print_goodbye()


if __name__ == "__main__":
    main()
