class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\nTags: {', '.join(self.tags)}"
    
    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)
    
class NoteBook:
    def __init__(self):
        self.notes = []

    def add(self, note: Note):
        self.notes.append(note)

    def remove(self, title: str):
        for note in self.notes:
            if note.title == title:
                self.notes.remove(note)
                return f"Note '{title}' removed."
        return f"Note '{title}' not found."

    def find(self, title: str):
        for note in self.notes:
            if note.title == title:
                return note
        return None

    def show_all(self):
        return "\n".join(str(note) for note in self.notes) if self.notes else "No notes available."
    
    def search(self, query: str):
        return [note for note in self.notes if query.lower() in note.title.lower() or query.lower() in note.content.lower()]

    def edit(self, title: str, new_title=None, new_content=None, new_tags=None):
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

    def search_by_tag(self, tag: str):
        return [note for note in self.notes if tag in note.tags]

    def sort_by_tag(self):
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
    print(notebook.search("project")[0] if notebook.search("project") else "No notes found with that query")

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

