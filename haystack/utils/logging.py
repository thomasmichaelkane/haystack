from rich import print as rprint
from rich.console import Console

def update(message):
    
    rprint(message)
    
def line():
    
    console = Console()
    console.print("---------------", style="magenta")

def warning(message):
    
    rprint("[bold red]Warning[/bold red] {}".format(message))