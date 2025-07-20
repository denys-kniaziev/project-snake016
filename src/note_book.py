from typing import List, Optional


class Note:
    """
    Individual note with title, content, and tags.
    
    Represents a single note entry containing a title, content body,
    and optional tags for categorization and organization.
    
    Notes support tag management operations for adding and removing
    classification labels that help with searching and filtering.
    
    Attributes:
        title (str): The note's title or heading
        content (str): The main content/body of the note
        tags (List[str]): List of tags for categorization
    """
    
    def __init__(self, title: str, content: str, tags: Optional[List[str]] = None) -> None:
        """
        Initialize a new note with title, content, and optional tags.
        
        Args:
            title (str): The note's title or heading
            content (str): The main content/body of the note
            tags (Optional[List[str]]): List of tags for categorization (default: empty list)
        """
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []

    def __str__(self) -> str:
        """
        Return formatted string representation of the note.
        
        Displays the note in a readable format with title, content,
        and comma-separated tags.
        
        Returns:
            str: Formatted note representation
        """
        return f"Title: {self.title}\nContent: {self.content}\nTags: {', '.join(self.tags)}"
    
    def add_tag(self, tag: str) -> str:
        """
        Add a new tag to the note if it doesn't already exist.
        
        Prevents duplicate tags by checking if the tag already exists
        before adding it to the tags list.
        
        Args:
            tag (str): Tag to add to the note
            
        Returns:
            str: Success message confirming tag addition
        """
        if tag not in self.tags:
            self.tags.append(tag)
        return f"Tag '{tag}' added to note '{self.title}'."

    def remove_tag(self, tag: str) -> str:
        """
        Remove a specific tag from the note.
        
        Args:
            tag (str): Tag to remove from the note
            
        Returns:
            str: Success or error message about tag removal
        """
        if tag in self.tags:
            self.tags.remove(tag)
            return f"Tag '{tag}' removed from note '{self.title}'."
        return f"Tag '{tag}' not found in note '{self.title}'."
    
class NoteBook:
    """
    Collection for managing multiple notes with advanced operations.
    
    Provides a comprehensive note management system with capabilities for
    adding, removing, editing, searching, and organizing notes. Supports
    both content-based search and tag-based filtering and organization.
    
    The notebook maintains an internal list of Note objects and provides
    various methods to manipulate and query this collection.
    
    Attributes:
        notes (List[Note]): List storing all notes in the notebook
    """
    
    def __init__(self) -> None:
        """
        Initialize an empty notebook.
        
        Creates a new notebook with an empty list ready to store notes.
        """
        self.notes: List[Note] = []

    def add(self, note: Note) -> str:
        """
        Add a new note to the notebook.
        
        Args:
            note (Note): Note object to add to the notebook
            
        Returns:
            str: Success message confirming note addition
        """
        self.notes.append(note)
        return f"Note added: {note.title}"

    def remove(self, title: str) -> str:
        """
        Remove a note from the notebook by title.
        
        Searches for a note with the specified title and removes it
        from the notebook if found.
        
        Args:
            title (str): Title of the note to remove
            
        Returns:
            str: Success or error message about note removal
        """
        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)
                return f"Note '{title}' removed."
        return f"Note '{title}' not found."

    def find(self, title: str) -> Optional[Note]:
        """
        Find a note by title.
        
        Internal utility method used by other methods to locate
        specific notes within the notebook.
        
        Args:
            title (str): Title of the note to find
            
        Returns:
            Optional[Note]: Note object if found, None otherwise
        """
        for note in self.notes:
            if note.title == title:
                return note
        return None

    def show_all(self) -> str:
        """
        Return formatted string representation of all notes.
        
        Creates a comprehensive view of all notes in the notebook,
        with each note separated by newlines.
        
        Returns:
            str: Formatted string of all notes or message if empty
        """
        return "\n".join(str(note) for note in self.notes) if self.notes else "No notes available."
    
    def search(self, query: str) -> List[Note]:
        """
        Search for notes containing the query in title or content.
        
        Performs case-insensitive substring matching across both
        note titles and content to find relevant notes.
        
        Args:
            query (str): Search term to look for in notes
            
        Returns:
            List[Note]: List of notes containing the search query
        """
        return [note for note in self.notes if query.lower() in note.title.lower() or query.lower() in note.content.lower()]

    def edit(self, title: str, new_title: Optional[str] = None, new_content: Optional[str] = None, new_tags: Optional[List[str]] = None) -> str:
        """
        Edit an existing note's title, content, or tags.
        
        Allows selective updating of note properties. Only specified
        parameters will be updated, leaving others unchanged.
        
        Args:
            title (str): Current title of the note to edit
            new_title (Optional[str]): New title for the note
            new_content (Optional[str]): New content for the note
            new_tags (Optional[List[str]]): New tags list for the note
            
        Returns:
            str: Success or error message about note editing
        """
        note = self.find(title)
        if note:
            if new_title is not None:
                note.title = new_title
            if new_content is not None:
                note.content = new_content
            if new_tags is not None:
                note.tags = new_tags
            return f"Note '{title}' updated."
        return f"Note '{title}' not found."

    def search_by_tag(self, tag: str) -> List[Note]:
        """
        Find all notes containing a specific tag.
        
        Filters the notebook to return only notes that have been
        tagged with the specified tag.
        
        Args:
            tag (str): Tag to search for in notes
            
        Returns:
            List[Note]: List of notes containing the specified tag
        """
        return [note for note in self.notes if tag in note.tags]

    def sort_by_tag(self) -> List[Note]:
        """
        Return notes sorted alphabetically by their tags.
        
        Sorts notes based on their tags in alphabetical order.
        For notes with multiple tags, uses comma-separated sorted tags.
        
        Returns:
            List[Note]: New list of notes sorted by tags
        """
        return sorted(self.notes, key=lambda note: ','.join(sorted(note.tags)))
        

if __name__ == "__main__":
    notebook = NoteBook()
    note1 = Note("Shopping List", "Buy milk, eggs, and bread", ["shopping", "groceries"])
    note2 = Note("Meeting Notes 1", "Discuss project updates", ["work", "meeting", "project"])
    note3 = Note("Meeting Notes 2", "Discuss annual bonus", ["work", "meeting", "finance"])
    
    notebook.add(note1)
    notebook.add(note2)
    notebook.add(note3)
    
    print(notebook.show_all())
    
    notebook.edit("Shopping List", new_content="Buy milk, eggs, bread, and butter")
    print(notebook.show_all())
    
    print('   Result of note search:')
    result = notebook.search("project")
    if result:
        for note in result:
            print(note)
    else:
        print("No notes found with that query.")

    print('   Result of tag search:')
    tag = "work"
    notes_with_tag = notebook.search_by_tag(tag)
    if notes_with_tag:
        for note in notes_with_tag:
            print(note)
    else:
        print(f"No notes found with tag '{tag}'")

    print('   Result of sorted notes by tag:')
    sorted_notes = notebook.sort_by_tag()
    for note in sorted_notes:
        print(note)

    print('   Result of added tag: Added tag - bread to Shopping List')
    note1.add_tag("bread")
    print(notebook.show_all())

    print('   Result of removed notes by tag: Removed tag - bread')
    for note in notebook.notes:
        note.remove_tag("bread")
    print(notebook.show_all())

    print('   Result of removed notes: Removed note - Shopping List')
    notebook.remove("Shopping List")
    print(notebook.show_all())

