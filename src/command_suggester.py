from typing import List
import difflib
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.document import Document
from command_registry import registry


class CommandCompleter(Completer):
    """
    Tab completer for command names only.

    Suggests only the first word (command), ignores arguments.
    Case-insensitive, supports hyphens.
    """

    def __init__(self, commands: List[str]):
        """Initialize with list of command names."""
        self.commands = commands

    def get_completions(self, document: Document, complete_event):
        """
        Provide completions for the first word only.

        Yields matching commands from the list.
        """
        text = document.text
        if ' ' in text:
            return
        current_word = text.lower()
        for command in self.commands:
            if command.lower().startswith(current_word):
                yield Completion(command, start_position=-len(current_word))


class CommandSuggester:
    """
    Suggests commands based on user input.

    Supports tab completion and fuzzy suggestions for typos.
    """

    def __init__(self):
        """
        Set up command list, completer, and interactive session.
        """
        self.commands = registry.get_all_command_names()
        self.completer = CommandCompleter(self.commands)
        self.session = PromptSession(completer=self.completer)

    def get_user_input(self, prompt_text: str = "Enter a command: ") -> str:
        """
        Prompt user for input with autocomplete.

        Returns:
            User input string or 'exit' on interruption.
        """
        try:
            return self.session.prompt(prompt_text)
        except (KeyboardInterrupt, EOFError):
            return "exit"

    def suggest_closest_commands(self, user_input: str, max_suggestions: int = 3) -> List[str]:
        """
        Suggest closest matching commands.

        Uses difflib for fuzzy matching. Returns top N similar commands.
        """
        if not user_input.strip():
            return []
        potential_command = user_input.strip().split()[0].lower()
        similarities = [
            (command, difflib.SequenceMatcher(None, potential_command, command).ratio())
            for command in self.commands
        ]
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [
            command for command, score in similarities[:max_suggestions] if score > 0.3
        ]

    def analyze_and_suggest(self, user_input: str) -> str:
        """
        Suggest alternatives for unrecognized commands.

        Returns a formatted suggestion or help message.
        """
        if not user_input.strip():
            return ""
        command = user_input.strip().split()[0].lower()
        if registry.is_valid_command(command):
            return ""
        suggestions = self.suggest_closest_commands(user_input)
        if not suggestions:
            return "Command not recognized. Type 'help' for available commands."
        suggestion_text = f"Command '{command}' not recognized. Did you mean:\n"
        for i, suggested_command in enumerate(suggestions, 1):
            suggestion_text += f"  {i}. {suggested_command}\n"
        suggestion_text += "Type 'help' for detailed command descriptions."
        return suggestion_text

    def get_all_commands(self) -> List[str]:
        """
        Return all available command names.
        """
        return self.commands.copy()


# Global suggester instance
command_suggester = CommandSuggester()
