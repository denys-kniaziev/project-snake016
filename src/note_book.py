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