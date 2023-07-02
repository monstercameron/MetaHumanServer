import os
import time
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPT:
    def __init__(self, model, ai_role, user_role):
        self.model = model
        self.ai_role = ai_role
        self.user_role = user_role
        self.history = []
        self.alive = True
        self.reset_history()
        print('Initializing chatGPT')
        print("Setting up AI personality")

    class Message:
        def __init__(self, role, content):
            self.role = role
            self.content = content

        def to_dict(self):
            return {"role": self.role, "content": self.content}

    def reset_history(self):
        self.history = [
            {"role": "system", "content": "You are a helpful assistant."}]

    def exit(self):
        self.alive = False

    def check_commands(self, prompt):
        if prompt == "/reset":
            self.reset_history()
            return True
        elif prompt == "/exit":
            self.exit()
            return True
        elif prompt == "":
            # this case covers empty prompts
            return True
        else:
            return False

    def prompt_openai(self):
        try:
            # Send the request to the OpenAI API
            return openai.ChatCompletion.create(
                model=self.model,
                messages=self.history
            )
        except openai.error.RateLimitError as e:
            if e.status_code == 429:
                # Rate limit exceeded, wait and try again
                print("Rate limit exceeded, waiting for 60 seconds...")
                time.sleep(60)
                return openai.ChatCompletion.create(
                    model=self.model,
                    messages=self.history
                )
            else:
                # Other error, re-raise the exception
                raise e

    def get_prompt_text(self, response):
        return response["choices"].pop(0)["message"]["content"]

    def add_to_chat_history(self, previous):
        self.history.append(previous)

    def run(self):
        # Reset the chat history and print a welcome message
        self.reset_history()
        print("Welcome to ChatGPT in the terminal!\n")

        while self.alive:
            prompt = input(f"\n{self.user_role}: ")
            is_command = self.check_commands(prompt)
            if is_command:
                # If the user's input is a command, skip the rest of the loop and start a new iteration
                continue
            prompt_message = self.Message(self.user_role, prompt)
            self.add_to_chat_history(prompt_message.to_dict())
            response_raw = self.prompt_openai()
            response = self.get_prompt_text(response_raw)
            response_message = self.Message(self.ai_role, response)
            self.add_to_chat_history(response_message.to_dict())
            print(f'\n{self.ai_role}: {response}')

        print("\nGood Bye.")

    def next(self, prompt):
        is_command = self.check_commands(prompt)
        if is_command:
            return "\n"
        prompt_message = self.Message(self.user_role, prompt)
        self.add_to_chat_history(prompt_message.to_dict())
        response_raw = self.prompt_openai()
        response = self.get_prompt_text(response_raw)
        response_message = self.Message(self.ai_role, response)
        self.add_to_chat_history(response_message.to_dict())
        return response
