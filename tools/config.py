
tools = [
  {
    'type': 'function',
    'function': {
      'name': 'list_files',
      'description': 'Lists all files and directories inside the current directory (workspace root) if no parameters passed, else in the provided directory, returning their paths relative to the workspace root as a JSON array.',
      'parameters': {
        'type': 'object',
        'properties': {
          'dir_name': {
            'type': 'string',
            'description': 'optional name of the directory where the list_files tools will be called'
          }
        }
      }
    }
  },
  {
    'type': 'function',
    'function': {
      'name': 'get_file_content',
      'description': 'Retrieves the content of a specified file. Optionally, can retrieve a range of lines.',
      'parameters': {
        'type': 'object',
        'properties': {
          'file_path': {
            'type': 'string',
            'description': 'The path of the file to read.'
          },
          'start_line': {
            'type': 'integer',
            'description': 'Optional line number to start reading from (1-indexed).'
          },
          'end_line': {
            'type': 'integer',
            'description': 'Optional line number to stop reading at (1-indexed, inclusive).'
          }
        },
        'required': ['file_path']
      }
    }
  },
  {
    'type': 'function',
    'function': {
      'name': 'create_file',
      'description': 'Creates a new file with the specified content.',
      'parameters': {
        'type': 'object',
        'properties': {
          'file_path': {
            'type': 'string',
            'description': 'The path of the file to create.'
          },
          'content': {
            'type': 'string',
            'description': 'The initial content to write into the file.'
          }
        },
        'required': ['file_path', 'content']
      }
    }
  },
  {
    'type': 'function',
    'function': {
      'name': 'modify_file',
      'description': 'Modifies a block of content in an existing file by replacing a target string with a new string.',
      'parameters': {
        'type': 'object',
        'properties': {
          'file_path': {
            'type': 'string',
            'description': 'The path of the file to modify.'
          },
          'target_content': {
            'type': 'string',
            'description': 'The exact block of code/content in the file to be replaced.'
          },
          'replacement_content': {
            'type': 'string',
            'description': 'The new content to replace the target block with.'
          }
        },
        'required': ['file_path', 'target_content', 'replacement_content']
      }
    }
  },
  {
    'type': 'function',
    'function': {
      'name': 'delete_file',
      'description': 'Deletes a specified file.',
      'parameters': {
        'type': 'object',
        'properties': {
          'file_path': {
            'type': 'string',
            'description': 'The path of the file to delete.'
          }
        },
        'required': ['file_path']
      }
    }
  },
  {
    'type': 'function',
    'function': {
      'name': 'make_directory',
      'description': 'Creates a new directory if it does not already exist.',
      'parameters': {
        'type': 'object',
        'properties': {
          'dir_name': {
            'type': 'string',
            'description': 'The path of the directory to create.'
          }
        },
        'required': ['dir_name']
      }
    }
  },
  {
    'type': 'function',
    'function': {
      'name': 'search_grep',
      'description': 'Searches for a query string pattern in files within a directory.',
      'parameters': {
        'type': 'object',
        'properties': {
          'query': {
            'type': 'string',
            'description': 'The string or pattern to search for.'
          },
          'dir_name': {
            'type': 'string',
            'description': 'Optional directory path to search within. Defaults to the current directory.'
          }
        },
        'required': ['query']
      }
    }
  }
]
