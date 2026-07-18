from google import genai
from google.genai import types

from constants import SYSTEM_PROMPT
from tools import tool_handlers

# Initialize client using environment variables
client = genai.Client()

commands = {("quit", "q"): {"description": "exit the loop", "handler": lambda: exit()}}

# build alias -> command lookup once
command_lookup = {
    alias: cmd_info for aliases, cmd_info in commands.items() for alias in aliases
}


def main_loop():
    # Initialize the chat session with model, system instruction, and tools.
    chat = client.chats.create(
        model="gemini-3.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=[f for _a, f in tool_handlers.items()],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )

    tool_called = False
    next_message = None

    while True:
        user_input = ""
        # get input from user
        if not tool_called:
            user_input = input("You: ")
            if user_input.startswith("/"):
                # handle commands
                command = user_input.strip().split(" ")[0][1:]
                args = user_input.strip().split(" ")[1:]
                if command == "quit" or command == "q":
                    break
                if command in command_lookup:
                    cmd = command_lookup.get(command)
                    if cmd:
                        if args:
                            cmd["handler"](*args)
                        else:
                            cmd["handler"]()
                else:
                    print(f'Error: Command "{command}" not found.')
                continue

            response = chat.send_message(user_input)
        else:
            # Send the tool responses accumulated from the last turn
            response = chat.send_message(next_message)
            tool_called = False
            next_message = None

        # Check for tool/function calls in response
        if response.function_calls:
            tool_responses = []
            for call in response.function_calls:
                print("Debug:", call.name, call.args)
                function_name = call.name
                args = call.args
                handler = tool_handlers.get(function_name)
                if handler:
                    tool_result = handler(**(args or {}))
                    # print("Debug: ", tool_result)

                    # Construct a Part with the function response
                    part = types.Part.from_function_response(
                        name=function_name, response={"result": tool_result}
                    )
                    tool_responses.append(part)

            if tool_responses:
                next_message = tool_responses
                tool_called = True
        else:
            # No function calls, print the assistant content
            print("agent: " + (response.text or ""))
