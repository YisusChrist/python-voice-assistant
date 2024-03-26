import sys

from dotenv import load_dotenv  # pip install python-dotenv
from openai import OpenAI  # pip install openai
from openai.types.chat.chat_completion import ChatCompletion

from .commands import *


def load_environment_variables():
    """
    Load environment variables from .env file.
    """
    print("Loading environment variables...")

    env_vars_loaded = load_dotenv()
    if env_vars_loaded:
        print("Environment variables loaded successfully")
    else:
        print("Environment variables could not be loaded")
        sys.exit(1)


def read_command(command_handler: CommandHandler, query: str):
    """
    Read the command from the user.
    """
    query_parts = query.lower()
    for command, function in command_handler.commands.items():
        if command in query_parts or query_parts in command:
            try:
                function()
                return True
            except Exception as e:
                print(e)
                pass

    print("Command not recognized. Please try again.")
    return False


def openai_call(transcript: str):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    # Create a list of messages with the user's input
    messages: list[dict[str, str]] = [
        {"role": "user", "content": transcript},
    ]
    print("Transcript:", transcript)

    # Make the API call for gpt AI
    completion: ChatCompletion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    response = completion.choices[0].message["content"]
    # Print the assistant's response
    print("Assistant:", response)

    return response


def main():
    load_environment_variables()
    command_handler = CommandHandler()

    command_handler.greeting(gender="Male", name="Michael Scott")

    while True:
        query = command_handler.engine.mic_to_text()
        if query is None:
            print("Empty query")
            continue

        result = read_command(command_handler, query)
        if not result:
            openai_response = openai_call(query)
            command_handler.engine.speak(openai_response)


if __name__ == "__main__":
    main()
