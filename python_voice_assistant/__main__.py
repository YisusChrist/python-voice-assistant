import sys

from dotenv import load_dotenv  # pip install python-dotenv

from .commands import *


# def ListenInBg():
#     r = sr.Recognizer()
#     r.listen_in_background(sr.Microphone(),callback,phrase_time_limit=2)

#     try:
#         print("You said " + recognizer.recognize_google(audio,language='en-in'))  # received audio data, now need to recognize it
#     except LookupError:
#         print("Oops! Didn't catch that")


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
    query_parts = " ".join([p.lower() for p in query.split()])
    for command, function in command_handler.commands.items():
        if command in query_parts or query_parts in command:
            try:
                function()
                return
            except Exception as e:
                print(e)
                pass

    else:
        print("Command not recognized. Please try again.")


def main():
    load_environment_variables()
    command_handler = CommandHandler()

    command_handler.greeting(gender="Male", name="Michael Scott")

    while True:
        query = command_handler.engine.mic_to_text()
        if query is None:
            print("Empty query")
            continue

        read_command(command_handler, query)


if __name__ == "__main__":
    main()
