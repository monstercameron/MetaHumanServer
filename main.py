import os
import time
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

history = []
model = "gpt-3.5-turbo"
aiRole = "assistant"
userRole = "user"


class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def to_dict(self):
        return {"role": self.role, "content": self.content}


def promptAI():
    return openai.ChatCompletion.create(
        model=model,
        messages=history
    )


def resetHistory():
    history = [{"role": "system", "content": "You are a helpful assistant."}]


def checkResetHistory(prompt):
    if (prompt == "/reset"):
        resetHistory()


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


def getPromptText(response):
    return response["choices"].pop(0)["message"]["content"]


def addToChatHistory(previous):
    history.append(previous)


if __name__ == "__main__":
    resetHistory()
    print("Welcome to ChatGPT in the terminal! \n\n")

    while True:
        prompt = input(f"{userRole}: ")
        checkResetHistory(prompt)

        promptMessage = Message(userRole, prompt)
        addToChatHistory(promptMessage.to_dict())

        responseRaw = promptOpenAI()
        reponse = getPromptText(responseRaw)

        newResponse = Message(aiRole, reponse)
        addToChatHistory(newResponse.to_dict())

        print(f'{aiRole}: {reponse}')
