import openai
from decouple import config

# Import  custom functions
from functions.database import get_recent_messages

# Retrieve our environment variables
openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")


# Open AI - Whisper
# Convert Audio to Text
def convert_audio_to_text(audio_file):
    try:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
        message_text = transcript["text"]
        return message_text
    except Exception as e:
        print(e)
        return
    
    # Open AI - CharGPT
    # Get response to our message
def get_chat_response(message_input):
    # Get recent chat messages
    recent_messages = get_recent_messages()

    # Create user message and add it to recent messages
    # user_message = {"role": "user", "content": message_input  + " Only say two or 3 words in Spanish if speaking in Spanish. The remaining words should be in English"}
    user_message = {"role": "user", "content": message_input}
    recent_messages.append(user_message)

    # Call OpenAI's ChatCompletion API and get response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=recent_messages
        )
        message_text = response["choices"][0]["message"]["content"]
        return message_text
    except Exception as e:
        return
