from commands import ( 
    parse_input, show_help, add_contact, change_contact, 
    show_phone, show_all, search_contacts, add_birthday, show_birthday, birthdays, delete_contact, add_address, add_email, 
    edit_fields, 
    add_note, remove_note, show_all_notes, search_notes, edit_note, search_notes_by_tag, sort_notes_by_tag, add_tag_to_note, remove_tag_from_note)

from data_persistence import save_addressbook, load_addressbook, save_notebook, load_notebook


def main():
    """Main function that runs the assistant bot."""
    addressbook = load_addressbook()
    notebook = load_notebook()
    print("Welcome to the assistant bot!")

    try:
        while True:
            user_input = input("Enter a command: ")
            command, args = parse_input(user_input)
            
            match command:
                case "close" | "exit":
                    break

                case "hello":
                    print("How can I help you?")

                case "help":
                    print(show_help())

                case "add":
                    print(add_contact(args, addressbook))
                    save_addressbook(addressbook)

                case "change":
                    print(change_contact(args, addressbook))
                    save_addressbook(addressbook)

                case "phone":
                    print(show_phone(args, addressbook))

                case "all":
                    print(show_all(args, addressbook))

                case "search":
                    print(search_contacts(args, addressbook))

                case "delete":
                    print(delete_contact(args, addressbook))
                    save_addressbook(addressbook)

                case "add-birthday":
                    print(add_birthday(args, addressbook))
                    save_addressbook(addressbook)

                case "add-address":
                    print(add_address(args, addressbook))
                    save_addressbook(addressbook)

                case "add-email":
                    print(add_email(args, addressbook))
                    save_addressbook(addressbook)

                case "edit-fields":
                    print(edit_fields(args, addressbook))
                    save_addressbook(addressbook)

                case "show-birthday":
                    print(show_birthday(args, addressbook))

                case "birthdays":
                    print(birthdays(args, addressbook))

                case "add-note":
                    print(add_note(args, notebook))
                    save_notebook(notebook, silentmode=True)

                case "remove-note":
                    print(remove_note(args, notebook))
                    save_notebook(notebook, silentmode=True)

                case "show-all-notes":
                    print(show_all_notes(args, notebook))

                case "search-notes":
                    print(search_notes(args, notebook))

                case "edit-note":
                    print(edit_note(args, notebook))
                    save_notebook(notebook, silentmode=True)

                case "search-notes-by-tag":
                    print(search_notes_by_tag(args, notebook))

                case "sort-notes-by-tag":
                    print(sort_notes_by_tag(args, notebook))

                case "add-tag-to-note":
                    print(add_tag_to_note(args, notebook))
                    save_notebook(notebook, silentmode=True)

                case "remove-tag-from-note":
                    print(remove_tag_from_note(args, notebook))
                    save_notebook(notebook, silentmode=True)

                case "":
                    continue  # Skip empty inputs

                case _:
                    print("Invalid command. Type 'help' for available commands.")
    
    except KeyboardInterrupt:
        print("\nReceived Ctrl+C, exiting...")
    
    finally:
        save_addressbook(addressbook)
        save_notebook(notebook)
        print("Good bye!")


if __name__ == "__main__":
    main()