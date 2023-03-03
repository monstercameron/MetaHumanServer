# Import the required modules
import os
import time
import openai
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Set the OpenAI API key using the value of the OPENAI_API_KEY environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the initial chat history as an empty list
history = []

# Define the roles for the AI and the user
model = "gpt-3.5-turbo"
aiRole = "assistant"
userRole = "user"
alive = True


# Define a Message class that stores the role and content of a chat message
class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    # Define a to_dict() method that returns the message as a dictionary
    def to_dict(self):
        return {"role": self.role, "content": self.content}


# Define a function called promptAI() that sends a request to the OpenAI API to generate a chat response
def promptAI():
    return openai.ChatCompletion.create(
        model=model,
        messages=history
    )


# Define a function called resetHistory() that resets the chat history to the initial message
def resetHistory():
    global history
    if (len(history) > 0):
        print("Resetting Chat History...\n")
    else:
        print("Setting The AI personality...\n")
    history = [{"role": "system", "content": "You are a helpful assistant."}]


# Define a function called exit() that ends the program
def exit():
    print("Exiting Program...")
    global alive
    alive = False


# Define a function called checkCommands() that checks if the user's input is a command and executes the command if it is
def checkCommands(prompt):
    if (prompt == "/reset"):
        resetHistory()
        return True
    elif (prompt == "/exit"):
        exit()
        return True
    elif (prompt == ""):
        # this case covers empty prompts
        return True
    else:
        return False


# Define a function called promptOpenAI() that sends a request to the OpenAI API to generate a chat response and handles rate limit errors
def promptOpenAI():
    try:
        # Send the request to the OpenAI API
        return openai.ChatCompletion.create(
            model=model,
            messages=history
        )
    except openai.error.RateLimitError as e:
        if e.status_code == 429:
            # Rate limit exceeded, wait and try again
            print("Rate limit exceeded, waiting for 60 seconds...")
            time.sleep(60)
            return openai.ChatCompletion.create(
                model=model,
                messages=history
            )
        else:
            # Other error, re-raise the exception
            raise e


# Define a function called getPromptText() that extracts the generated response text from the OpenAI response object
def getPromptText(response):
    return response["choices"].pop(0)["message"]["content"]


# Define a function called addToChatHistory() that adds a message to the chat history
def addToChatHistory(previous):
    history.append(previous)


# Check if the script is being run as the main program
if __name__ == "__main__":
    # Reset the chat history and print a welcome message
    resetHistory()
    print("Welcome to ChatGPT in the terminal!\n")

   # Start an infinite loop that prompts the user for input and generates AI responses
    while alive:
        # Prompt the user for input and store it in the variable 'prompt'
        prompt = input(f"\n{userRole}: ")

        # Check if the user's input is a command using the 'checkCommands' function
        isCommand = checkCommands(prompt)

        if (isCommand):
            # If the user's input is a command, skip the rest of the loop and start a new iteration
            continue

        # Create a Message object for the user's input and add it to the chat history using the 'addToChatHistory' function
        promptMessage = Message(userRole, prompt)
        addToChatHistory(promptMessage.to_dict())

        # Generate an AI response using the 'promptOpenAI' function
        responseRaw = promptOpenAI()

        # Extract the response text from the OpenAI response object using the 'getPromptText' function
        reponse = getPromptText(responseRaw)

        # Create a Message object for the AI's response and add it to the chat history using the 'addToChatHistory' function
        responseMessage = Message(aiRole, reponse)
        addToChatHistory(responseMessage.to_dict())

        # Print the AI's response to the console
        print(f'\n{aiRole}: {reponse}')

    print("\nGood Bye.")
