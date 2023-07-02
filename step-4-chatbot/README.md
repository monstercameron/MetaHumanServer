Building this out into a bigger project...

To set up the environment and run the chatbot, follow these steps:

```bash
conda create --name <your_env_name> python=3.8
conda activate <your_env_name>
pip install -r requirements.txt
echo "OPENAI_API_KEY=<your_api_key_here>" >> .env
python main.py
```




Commands:
* /reset - reset the chat history
* /exit - exit program




Example return object from openAI chatbot
```python
{
    "choices": [
      {
        "finish_reason": "stop",
        "index": 0,
        "message": {
          "content": "The 2020 World Series was played at Globe Life Field in Arlington, Texas.",
          "role": "assistant"
        }
      }
    ],
    "created": 1677811207,
    "id": "chatcmpl-6ppd1iJeZa5qSNUO5cAzCKMYErdHC",
    "model": "gpt-3.5-turbo-0301",
    "object": "chat.completion",
    "usage": {
      "completion_tokens": 19,
      "prompt_tokens": 56,
      "total_tokens": 75
    }
  }
```