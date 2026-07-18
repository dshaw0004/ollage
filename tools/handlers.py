import json
import os

# Define the workspace root relative to this file's location: tools/handlers.py -> two levels up
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def list_files(dir_name: str = None) -> str:
    """
    Lists all the files and directories inside the current directory (or workspace root if none passed),
    or the provided directory, returning their paths relative to the workspace root as a JSON array.

    Args:
        dir_name: optional name of the directory where the list_files tools will be called
    """
    if dir_name:
        if os.path.isabs(dir_name):
            target_dir = dir_name
        else:
            target_dir = os.path.abspath(os.path.join(WORKSPACE_ROOT, dir_name))
    else:
        target_dir = WORKSPACE_ROOT

    if not os.path.exists(target_dir):
        return json.dumps({"error": f"Directory '{dir_name}' does not exist."})
    if not os.path.isdir(target_dir):
        return json.dumps({"error": f"'{dir_name}' is not a directory."})

    try:
        items = os.listdir(target_dir)
        result = []
        for item in sorted(items):
            full_path = os.path.join(target_dir, item)
            rel_path = os.path.relpath(full_path, WORKSPACE_ROOT)
            result.append(rel_path)
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": f"Error listing directory contents: {str(e)}"})


def get_file_content(
    file_path: str = None, start_line: int = None, end_line: int = None
) -> str:
    """
    Retrieves the content of a specified file. Optionally, can retrieve a range of lines (1-indexed).

    Args:
        file_path: path to the file to retrieve
        start_line: optional line number to start from (1-indexed)
        end_line: optional line number to end at (1-indexed)
    """
    file_path = file_path.strip()
    if not file_path:
        return "Error: 'file_path' is a required argument."

    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    if not os.path.isfile(file_path):
        return f"Error: '{file_path}' is not a file."

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        total_lines = len(lines)
        start = 1
        if start_line is not None:
            start = max(1, int(start_line))

        end = total_lines
        if end_line is not None:
            end = min(total_lines, int(end_line))

        if start > total_lines or start > end:
            return f"Error: Invalid line range {start}-{end} for a file with {total_lines} lines."

        selected_lines = lines[start - 1 : end]
        formatted_content = "".join(
            f"{idx}: {line}" for idx, line in zip(range(start, end + 1), selected_lines)
        )
        return formatted_content
    except Exception as e:
        return f"Error reading file content: {str(e)}"


def create_file(file_path: str = None, content: str = None) -> str:
    """
    Creates a new file with the specified content. Also creates parent directories if they don't exist.

    Args:
        file_path: path to the file to create
        content: content to write to the file
    """
    file_path = file_path.strip()
    if not file_path:
        return "Error: 'file_path' is a required argument."
    if content is None:
        return "Error: 'content' is a required argument."

    try:
        parent_dir = os.path.dirname(file_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Success: File '{file_path}' created successfully."
    except Exception as e:
        return f"Error creating file: {str(e)}"


def modify_file(
    file_path: str = None, target_content: str = None, replacement_content: str = None
) -> str:
    """
    Modifies a block of content in an existing file by replacing a target string with a new string.

    Args:
        file_path: path to the file to modify
        target_content: the string to replace
        replacement_content: the string to replace with
    """
    file_path = file_path.strip()
    if not file_path:
        return "Error: 'file_path' is a required argument."
    if target_content is None:
        return "Error: 'target_content' is a required argument. If you want to write a new file or overwrite it entirely, please use the 'create_file' tool instead."
    if replacement_content is None:
        return "Error: 'replacement_content' is a required argument."

    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    if not os.path.isfile(file_path):
        return f"Error: '{file_path}' is not a file."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_data = f.read()

        if target_content not in file_data:
            return f"Error: Target content to replace was not found in the file."

        occurrences = file_data.count(target_content)
        if occurrences > 1:
            new_data = file_data.replace(target_content, replacement_content)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_data)
            return f"Success: Replaced {occurrences} occurrences of target content in '{file_path}'."

        new_data = file_data.replace(target_content, replacement_content, 1)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_data)
        return f"Success: File '{file_path}' modified successfully."
    except Exception as e:
        return f"Error modifying file: {str(e)}"


def delete_file(file_path: str = None) -> str:
    """
    Deletes a specified file.

    Args:
        file_path: path to the file to delete
    """
    if not file_path:
        return "Error: 'file_path' is a required argument."

    if not os.path.exists(file_path):
        return f"Error: File '{file_path}' does not exist."
    if not os.path.isfile(file_path):
        return f"Error: '{file_path}' is not a file."

    try:
        os.remove(file_path)
        return f"Success: File '{file_path}' deleted successfully."
    except Exception as e:
        return f"Error deleting file: {str(e)}"


def make_directory(dir_name: str = None) -> str:
    """
    Creates a new directory if it does not already exist.

    Args:
        dir_name: path to the directory to create
    """
    if not dir_name:
        return "Error: 'dir_name' is a required argument."

    try:
        if os.path.exists(dir_name):
            if os.path.isdir(dir_name):
                return f"Info: Directory '{dir_name}' already exists."
            else:
                return f"Error: Path '{dir_name}' exists but is not a directory."

        os.makedirs(dir_name, exist_ok=True)
        return f"Success: Directory '{dir_name}' created successfully."
    except Exception as e:
        return f"Error creating directory: {str(e)}"


def search_grep(query: str = None, dir_name: str = None) -> list[str] | str:
    """
    Searches for a query string pattern in files within a directory.

    Args:
        query: the string pattern to search for
        dir_name: path to the directory to search in (default is current directory)
    """
    if not query:
        return ["Error: 'query' is a required argument."]

    target_dir = dir_name if dir_name else "."
    if not os.path.exists(target_dir):
        return [f"Error: Directory '{target_dir}' does not exist."]

    matches = []
    try:
        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [
                d
                for d in dirs
                if d not in (".git", "__pycache__", "node_modules", ".venv", "env")
            ]
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, 1):
                            if query in line:
                                matches.append(
                                    f"{file_path}:{line_num}: {line.strip()}"
                                )
                except Exception:
                    continue

        if not matches:
            return [f"No matches found for query: '{query}'"]

        total_matches = len(matches)
        if total_matches > 100:
            matches = matches[:100]
            suffix = f"\n... (truncated {total_matches - 100} more matches)"
        else:
            suffix = ""

        return [*matches, suffix]
    except Exception as e:
        return f"Error performing search: {str(e)}"
