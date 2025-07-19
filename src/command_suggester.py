from typing import List
import difflib
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document


class CommandCompleter(Completer):
    """
    Custom completer that only suggests commands for the first word,
    and stops suggesting once arguments are being typed.
    """
    
    def __init__(self, commands: List[str]):
        self.commands = commands
    
    def get_completions(self, document: Document, complete_event):
        """
        Get completions for the current document.
        Only provide suggestions for the first word (command).
        """
        text = document.text
        
        # If there's already a space, don't suggest anything (user is typing arguments)
        if ' ' in text:
            return
        
        # Get the current word being typed, including hyphens
        # Use the full text before cursor since we know there are no spaces
        word = text.lower()
        
        # Find matching commands
        for command in self.commands:
            if command.lower().startswith(word):
                yield Completion(command, start_position=-len(word))


class CommandSuggester:
    """
    Intelligent command suggester that analyzes user input and provides
    the closest matching commands with autocomplete functionality.
    """
    
    def __init__(self):
        # Define all available commands
        self.commands = [
            # General commands
            "help", "exit", "close",
            
            # Address book commands
            "add-contact", "show-all-contacts", "search-contacts",
            "delete-contact", "add-birthday", "add-address", "add-email",
            "edit-fields", "show-birthday", "birthdays",
            
            # Note book commands
            "add-note", "remove-note", "show-all-notes", "search-notes",
            "edit-note", "search-notes-by-tag", "sort-notes-by-tag",
            "add-tag-to-note", "remove-tag-from-note"
        ]
        
        # Create custom command completer that only suggests for the first word
        self.completer = CommandCompleter(self.commands)
        
        # Create prompt session with autocomplete
        self.session = PromptSession(completer=self.completer)
    
    def get_user_input(self, prompt_text: str = "Enter a command: ") -> str:
        """
        Get user input with autocomplete functionality.
        
        Args:
            prompt_text (str): The prompt message to display
            
        Returns:
            str: User input with autocomplete support
        """
        try:
            return self.session.prompt(prompt_text)
        except (KeyboardInterrupt, EOFError):
            return "exit"
    

    def suggest_closest_commands(self, user_input: str, max_suggestions: int = 3) -> List[str]:
        """
        Suggest the closest matching commands based on user input using SequenceMatcher.
        
        Args:
            user_input (str): The user's input text
            max_suggestions (int): Maximum number of suggestions to return
            
        Returns:
            List[str]: List of suggested commands
        """
        if not user_input.strip():
            return []
        
        # Get the first word as the potential command
        potential_command = user_input.strip().split()[0].lower()
        
        # Calculate similarity scores for all commands using just SequenceMatcher
        similarities = []
        for command in self.commands:
            similarity = difflib.SequenceMatcher(None, potential_command, command).ratio()
            similarities.append((command, similarity))
        
        # Sort by similarity score (descending) and take top suggestions
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Filter out very low similarity scores and return just command names
        suggestions = []
        for command, score in similarities[:max_suggestions]:
            if score > 0.3:  # Include any similarity > 0.4
                suggestions.append(command)
        
        return suggestions
    
    
    def analyze_and_suggest(self, user_input: str) -> str:
        """
        Analyze user input and provide command suggestions if the command is not recognized.
        
        Args:
            user_input (str): The user's input text
            
        Returns:
            str: Suggestion message or empty string if no suggestions needed
        """
        if not user_input.strip():
            return ""
        
        command = user_input.strip().split()[0].lower()
        
        # If it's a valid command, no suggestion needed
        if command in self.commands:
            return ""
        
        # Get suggestions for invalid commands
        suggestions = self.suggest_closest_commands(user_input)
        
        if not suggestions:
            return "Command not recognized. Type 'help' for available commands."
        
        # Format suggestions - just show the command names
        suggestion_text = f"Command '{command}' not recognized. Did you mean:\n"
        for i, suggested_command in enumerate(suggestions, 1):
            suggestion_text += f"  {i}. {suggested_command}\n"
        
        suggestion_text += "Type 'help' for detailed command descriptions."
        return suggestion_text
    
    def get_all_commands(self) -> List[str]:
        """
        Get all available commands.
        
        Returns:
            List[str]: List of all available commands
        """
        return self.commands.copy()


# Global instance for easy access
command_suggester = CommandSuggester()
