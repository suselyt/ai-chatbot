from openai import OpenAI
from dotenv import load_dotenv
from sys_msg import sys_message
import os
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

    ai_response_stream = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        stream=True,
    )

    full_answer = ""
    for chunk in ai_response_stream:
        piece = chunk.choices[0].delta.content
        if piece is not None :
            full_answer += piece
            yield piece

    messages.append({"role": "assistant", "content": full_answer})