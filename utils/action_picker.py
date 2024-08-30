# standard library
from pathlib import Path
import sys, subprocess

# third-party imports
from rich.console import Console
from pick import pick


console = Console()


class ActionPicker:
    @staticmethod
    def advanced_picker(choices: list[tuple], prompt: str) -> list:
        """
        Choice picker using the advanced and less compatible Pick module.
        """
        options = [choice[0] for choice in choices]
        selected_index = pick(options, prompt, indicator="->")[1]
        return choices[selected_index]

    def pick_task(self, choices: list[tuple], repeat: bool = True) -> None:
        """
        Allows picking a task using Arrow Keys and Enter.
        """
        if not sys.stdout.isatty():
            # runs if it is not an interactable terminal
            print("\nSkipping Task Picker.\nInput can't be used")
            return
        input("\nPress Enter to Pick Next Action:")
        PROMPT = "What do you want to do? (Use Arrow Keys and Enter):"
        selected = self.advanced_picker(choices, PROMPT)
        if selected:
            name, func = selected[0], selected[1]
            msg = f"\n[b underline]{name}[/] Selected"
            console.print(msg, highlight=False)
            func()
            if "exit" in name.lower():
                return
            if repeat:
                self.pick_task(choices, repeat)

    @staticmethod
    def open_folder(folder: Path) -> None:
        print(f"\nOpening Directory | {folder}")
        subprocess.Popen(f'explorer "{folder}"')
