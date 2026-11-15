import os
from pathlib import Path

from dotenv import load_dotenv

from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

class OpenAiConnect:
    def __init__(self):
        env_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(env_path)
        self.endpoint = os.getenv("FOUNDARY_OPENAI_ENDPOINT")
        self.deployment_name = "gpt-5-mini"
        token_url = os.getenv("TOKEN_PROVIDER_DEFAULT_URL", "https://ai.azure.com/.default")
        self.token_provider = get_bearer_token_provider(DefaultAzureCredential(), token_url)
        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token_provider
        )

    def get_response(self, instructions, input_text, temperature=0.7, max_output_tokens=1500):
        response = self.client.responses.create(
            model=self.deployment_name,
            instructions=instructions,
            input=input_text,
            stream=True,  # Enable streaming for real-time responses
            max_output_tokens=max_output_tokens  # Limit response length
        )
        for event in response:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)  # Print each event as it arrives
        # print(f"answer: {response.output_text}")
        # print(f"Response ID: {response.id}")
        # print(f"Tokens used: {response.usage.total_tokens}")
        # print(f"Status: {response.status}")
        return response
    def chat(self):
        print("Assistant: Ask anything, Type quit to exit.")

        while True:
            user_input = input("You: ")
            if user_input.lower() == "quit":
                print("Assistant: Goodbye!")
                break

            try:
                openai_connect = OpenAiConnect()
                response = openai_connect.get_response(
                    instructions="You are a helpful AI assistant that answers questions clearly and concisely.",
                    input_text=user_input
                    )
                print(f"Assistant: {response.output_text}")
            except Exception as e:
                print(f"An error occurred: {e}")