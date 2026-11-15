from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

class CodeInterpretTool:
    def __init__(self):
        env_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(env_path)
        self.endpoint = os.getenv("FOUNDARY_OPENAI_ENDPOINT")
        self.deployment_name = "gpt-5-mini"
        token_url = os.getenv("TOKEN_PROVIDER_DEFAULT_URL")
        self.token_provider = get_bearer_token_provider(DefaultAzureCredential(),token_url)
        self.client = OpenAI(base_url=self.endpoint, api_key= self.token_provider)
        
        
    def get_response(self):
        response = self.client.responses.create(
            model=self.deployment_name,
            instructions="You are an AI assistant that provides information. Use the python tool to run code for math problems.",
            input="What is the squre root of 16?",
            tools=[{"type": "code_interpreter", "container":{"type":"auto"}}]
        )
        print(response.output_text)
        print(response)
        
    