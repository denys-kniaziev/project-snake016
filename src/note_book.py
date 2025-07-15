class Note:
    def __init__(self, title, content, tags=None):
        self.title = title
        self.content = content
        self.tags = tags if tags is not None else []

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\nTags: {', '.join(self.tags)}"
    
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
    

if __name__ == "__main__":
    notebook = NoteBook()
    note1 = Note("Shopping List", "Buy milk, eggs, and bread", ["shopping", "groceries"])
    note2 = Note("Meeting Notes", "Discuss project updates", ["work", "meeting"])

    notebook.add(note1)
    notebook.add(note2)

    print(notebook.show_all())

    print(notebook.find("Shopping List"))
    
    print(notebook.remove("Meeting Notes"))
    print(notebook.show_all())
    
    print(notebook.remove("Nonexistent Note"))