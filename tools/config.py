
tools = [
  {
    'type': 'function',
    'function': {
      'name': 'list_files',
      'description': 'Lists all the files inside current directory if no parameters passed else in the provided directory.',
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
]
