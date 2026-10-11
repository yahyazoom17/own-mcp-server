from mcp.server.mcpserver import MCPServer
import os

mcp = MCPServer("AI Sticky Notes", "1.0.0")

NOTES_FILE = os.path.join(os.path.dirname(__file__), "notes.txt")

def ensure_notes_file_exists():
    """Ensure the notes file exists."""
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as f:
            f.write("")

@mcp.tool()
def add_note(note: str) -> str:
    """
    Append a new note to the notes file.

    Args:
        note (str): The note to be added.

    Returns:
        str: A confirmation message indicating the note was saved successfully.
    """
    ensure_notes_file_exists()
    with open(NOTES_FILE, "a") as f:
        f.write(note + "\n")
    return "Note saved successfully."

@mcp.tool()
def read_notes() -> str:
    """
    Read all notes from the notes file.

    Returns:
        str: A string containing all notes, each separated by a newline.
    """
    ensure_notes_file_exists()
    with open(NOTES_FILE, "r") as f: 
        notes = f.read().strip()
    return notes or "No notes yet."

@mcp.resource("notes://latest")
def get_latest_note() -> str:
    """
    Get the latest note from the notes file.

    Returns:
        str: The latest note, or a message indicating there are no notes.
    """
    ensure_notes_file_exists()
    with open(NOTES_FILE, "r") as f:
        lines = f.readlines()
    if lines:
        return lines[-1].strip()
    else:
        return "No notes yet."

@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt for summarizing the current notes.

    Returns:
        str: The summary prompt.
    """
    ensure_notes_file_exists()
    with open(NOTES_FILE, "r") as f:
        notes = f.read().strip()
    if not notes:
        return "You have no notes yet."
    
    return f"Summarize the current notes: {notes}"