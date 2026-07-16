from .handlers import (
    list_files,
    get_file_content,
    create_file,
    modify_file,
    delete_file,
    make_directory,
    search_grep,
)

tool_handlers = {
    'list_files': list_files,
    'get_file_content': get_file_content,
    'create_file': create_file,
    'modify_file': modify_file,
    'delete_file': delete_file,
    'make_directory': make_directory,
    'search_grep': search_grep,
}
