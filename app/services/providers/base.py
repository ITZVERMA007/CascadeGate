from annotated_types import Not
from abc import ABC, abstractmethod
from typing import AsyncGenerator
# pyrefly: ignore [missing-import]
import httpx

class LLMProvider(ABC):
    def __init__(self, http_client: httpx.AsyncClient, api_key: str, base_url: str, model: str):
        self.http_client = http_client
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
    
    # Sends a non streaming response to the provider
    @abstractmethod
    async def complete(self, messages: list[dict], **kwargs) -> dict:
        
        raise NotImplementedError
    
    # Sends a streaming response to the provider in the form of chunks
    @abstractmethod
    async def stream(self, messages: list[dict], **kwargs) -> AsyncGenerator:

        raise NotImplementedError