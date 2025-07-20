from typing import List
import difflib
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from .command_registry import registry


class CommandCompleter(Completer):
    """
    Custom completer that provides Tab completion for commands only.
    
    Key behaviors:
    - Only suggests commands when typing the first word
    - Stops suggesting once a space is typed (prevents argument completion)
    - Supports hyphenated commands like 'add-contact', 'show-all-notes'
    - Case-insensitive matching
    """
    
    def __init__(self, commands: List[str]):
        """
        Initialize the completer with a list of available commands.
        
        Args:
            commands: List of command names for completion
        """
        self.commands = commands
    
    def get_completions(self, document: Document, complete_event):
        """
        Generate completions for the current document position.
        
        This method is called by prompt_toolkit when the user presses Tab.
        It only provides suggestions for the command part (before any spaces).
        
        Args:
            document: Current document state from prompt_toolkit
            complete_event: Completion event details
            
        Yields:
            Completion objects for matching commands
        """
        text = document.text
        
        # Don't suggest anything if user is typing arguments (after space)
        if ' ' in text:
            return
        
        # Get the current word being typed (handles hyphens properly)
        # Since we know there are no spaces, the entire text is the command
        current_word = text.lower()
        
        # Find and yield matching commands
        for command in self.commands:
            if command.lower().startswith(current_word):
                # Create completion that replaces the current word
                yield Completion(command, start_position=-len(current_word))


class CommandSuggester:
    """
    Intelligent command suggester that analyzes user input and provides
    the closest matching commands with autocomplete functionality.
    
    This class integrates with the centralized command registry to provide:
    - Tab completion for all registered commands
    - Fuzzy matching suggestions for typos
    - Interactive prompt with autocomplete support
    """
    
    def __init__(self):
        """
        Initialize the command suggester using the centralized registry.
        
        Gets the list of available commands from the registry and sets up
        the autocomplete system with prompt_toolkit.
        """
        # Get all command names from the centralized registry
        # This eliminates duplication - commands are defined once in registry
        self.commands = registry.get_all_command_names()
        
        # Create custom command completer that only suggests for the first word
        self.completer = CommandCompleter(self.commands)
        
        # Create prompt session with autocomplete support
        # This provides the interactive command line with Tab completion
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
        
        This method uses difflib.SequenceMatcher to find commands that are similar
        to what the user typed, helping with typos and partial command names.
        SequenceMatcher naturally handles prefix matches, contains matches, and typos
        without needing manual boost logic.
        
        Args:
            user_input (str): The user's input text
            max_suggestions (int): Maximum number of suggestions to return
            
        Returns:
            List[str]: List of suggested commands sorted by similarity
        """
        if not user_input.strip():
            return []
        
        # Get the first word as the potential command (ignore arguments)
        potential_command = user_input.strip().split()[0].lower()
        
        # Calculate similarity scores for all commands using SequenceMatcher
        # SequenceMatcher.ratio() returns a float between 0.0 and 1.0
        # where 1.0 means identical and 0.0 means completely different
        similarities = []
        for command in self.commands:
            similarity = difflib.SequenceMatcher(None, potential_command, command).ratio()
            similarities.append((command, similarity))
        
        # Sort by similarity score (highest first) and take top suggestions
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Return command names with reasonable similarity (> 0.3 threshold)
        # This filters out completely unrelated commands
        suggestions = []
        for command, score in similarities[:max_suggestions]:
            if score > 0.3:  # Only suggest if similarity is reasonable
                suggestions.append(command)
        
        return suggestions
    
    
    def analyze_and_suggest(self, user_input: str) -> str:
        """
        Analyze user input and provide command suggestions if the command is not recognized.
        
        This method is called when the user types an invalid command. It uses fuzzy
        matching to find similar commands and presents them in a user-friendly format.
        
        Args:
            user_input (str): The user's input text
            
        Returns:
            str: Suggestion message or empty string if no suggestions needed
        """
        if not user_input.strip():
            return ""
        
        # Extract just the command part (first word)
        command = user_input.strip().split()[0].lower()
        
        # If it's a valid command, no suggestion needed
        # This check uses the registry to validate commands
        if registry.is_valid_command(command):
            return ""
        
        # Get fuzzy matching suggestions for invalid commands
        suggestions = self.suggest_closest_commands(user_input)
        
        if not suggestions:
            # No similar commands found - show generic help message
            return "Command not recognized. Type 'help' for available commands."
        
        # Format suggestions in a user-friendly way
        suggestion_text = f"Command '{command}' not recognized. Did you mean:\n"
        for i, suggested_command in enumerate(suggestions, 1):
            suggestion_text += f"  {i}. {suggested_command}\n"
        
        suggestion_text += "Type 'help' for detailed command descriptions."
        return suggestion_text
    
    def get_all_commands(self) -> List[str]:
        """
        Get all available commands from the registry.
        
        This method provides access to the complete list of commands,
        primarily used for testing or debugging purposes.
        
        Returns:
            List[str]: Copy of all available command names
        """
        return self.commands.copy()


# Global instance for easy access throughout the application
# This provides a single point of access to command suggestion functionality
command_suggester = CommandSuggester()
