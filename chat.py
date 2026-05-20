from openai import OpenAI
from dotenv import load_dotenv
from sys_msg import sys_message
import os
import tiktoken
import logging
load_dotenv()

# connection to openai api
client = OpenAI(
    api_key=os.getenv("API_KEY"),       #openaikey
    base_url=os.getenv("BASE_URL"),     #endpoint url (since im using a private endpoint)
)

# messages array to preserve history
messages=[
            {"role": "system", "content": sys_message}
        ]

def send_message_to_ai(user_msg):
    """
        Receives the messages sent from the api and creates a dict with the role.
        Appends this dict to the messages history.
        Sends that message to the ai for a stream response.
        Receives the ai answer in chunks and later appends to the message history.
    """
    user_message = {"role": "user", "content": user_msg}
    messages.append(user_message)

    try:
        ai_response_stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            stream=True,
        )
        
        prompt_tokens = sum(count_tokens(m["content"]) for m in messages)       # it uses the messages as context which are part of the prompt

        full_answer = ""
        for chunk in ai_response_stream:
            if chunk.choices and chunk.choices[0].delta.content is not None:    # some chunks can have empty choices
                piece = chunk.choices[0].delta.content
                full_answer += piece
                yield piece

        completion_tokens = count_tokens(full_answer)
        total_tokens = prompt_tokens + completion_tokens

        yield f"__TOKENS__{prompt_tokens},{completion_tokens},{total_tokens}"
        messages.append({"role": "assistant", "content": full_answer})
    except Exception as e:
        logging.error(f"OpenAI call failed: {e}")
        raise
        

def reset_chat():
    global messages 
    messages=[
            {"role": "system", "content": sys_message}
        ]
    return

def count_tokens(text: str) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))