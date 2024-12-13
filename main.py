

import discord
import os
from dotenv import load_dotenv
import google.generativeai as genai
from openai import OpenAI
load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')
gemini_token = os.getenv('GEMINI_TOKEN')
# client = OpenAI(
#     api_key=os.getenv("OPENAI_TOKEN"),  # This is the default and can be omitted
# )

genai.configure(api_key=gemini_token)
# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
        if self.user != message.author:
            if self.user in message.mentions:
                channel = message.channel
                chat_session = model.start_chat()
                response = chat_session.send_message(message.content)
                if len(response.text) >= 2000:
                    for i in range(0, len(response.text), 2000):
                        await channel.send(response.text[i:i+2000])
                else:
                  messageToSend = response.text
                  await channel.send(messageToSend)
        

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_token)

