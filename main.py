import initialize

from pprint import pprint

from ollama import chat
from ollama import ChatResponse

from tools.config import tools


def main():
    response: ChatResponse = chat(model='granite4:350m', messages=[
        {
            'role': 'user',
            'content': 'list out all the files in the tools folder'
        }
    ],
        tools=tools)
    # print(response['message']['content'])
    print(response.message.content)
    # print(response.message)
    if 'tool_calls' in response.message:
        for tool_call in response.message.tool_calls:
            args = tool_call.function.arguments
            funciton_name = tool_call.function.name
            pprint({
                "function name": funciton_name,
                "arguments": args
            })


if __name__ == "__main__":
    main()
