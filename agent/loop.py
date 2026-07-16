from ollama import chat
from ollama import ChatResponse

from tools.config import tools
from tools import tool_handlers


def loop_handler():
    # send chat history to ollama
    print()
    # 

commands = {
    ('quit', 'q'): { 'description': 'exit the loop', 'handler': lambda: exit() }
}

# build alias -> command lookup once
command_lookup = {
    alias: cmd_info
    for aliases, cmd_info in commands.items()
    for alias in aliases
}

def main_loop():
    messages = [{
        'role': 'system',
        'content': 'You are a cli coding agent name ollage.'
    }]
    tool_called = False
    while True:
        user_input = ''
        # get input from user
        if not tool_called:
            user_input = input("You: ")
            messages.append({
                'role': 'user',
                'content': user_input
            })
        if user_input.startswith('/'):
            # handle commands
            command = user_input.strip().split(' ')[0][1:]
            args = user_input.strip().split(' ')[1:]
            if command == 'quit' or command == 'q':
                break
            if command in commands:
                cmd = command_lookup.get(cmd_name)
                if cmd:
                    if args:
                        cmd['handler'](*args)
                    else:
                        cmd['handler']()
                else:
                    print(f'Error: Command "{command}" not found.')
            continue
            

        # send to ollama
        response: ChatResponse = chat(model='granite4:350m', messages=messages,
            tools=tools)

        # handle tool calls
        if 'tool_calls' in response.message:
            for tool_call in response.message.tool_calls:
                print('Debug:', tool_call.function.name , tool_call.function.arguments)
                args = tool_call.function.arguments
                funciton_name = tool_call.function.name
                handler = tool_handlers.get(funciton_name)
                if handler:
                    tool_response = handler(**(args or {}))
                    messages.append({
                        'role': 'tool',
                        'content': tool_response
                    })
                    print('Debug: ', tool_response)
                    tool_called = True
                    continue
                
        else:
            # update messages
            tool_called = False
            messages.append({
                'role': 'assistant',
                'content': response.message.content
            })
            print('agent: ' + response.message.content)
