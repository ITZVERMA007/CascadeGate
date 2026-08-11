# pyrefly: ignore [missing-import]
import httpx
# pyrefly: ignore [missing-import]
import structlog
from typing import AsyncGenerator

from app.services.providers.base import LLMProvider
from app.services.exceptions import (
    ProviderClientError,
    ProviderServerError,
    ProviderTimeoutError,
)

logger = structlog.get_logger()

class GroqProvider(LLMProvider):
    async def complete(self, messages: list[dict], **kwargs) -> dict:

        url = f"{self.base_url.rstrip('/')}/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": kwargs.get("temperature",0.7),
            "max_tokens": kwargs.get("max_tokens",1024),
            "logprobs": True,
        }

        try:
            # Creating http request using the http pool
            response = await self.http_client.post(url, headers=headers, json=payload)

            if 400 <= response.status_code < 500:
                logger.error("groq_client_error",status=response.status_code, body=response.text)
                raise ProviderClientError(f"Groq Client Error: {response.text}",status_code=response.status_code)
            
            elif response.status_code >= 500:
                logger.error("groq_server_error",status=response.status_code,body=response.text)
                raise ProviderServerError(f"Groq Server Error: {response.text}", status_code=response.status_code)
            
            return response.json()
        
        except httpx.TimeoutException as e:
            logger.error("groq_timeout_error",error=str(e))
            raise ProviderTimeoutError(f"Request to Groq timed out: {str(e)}")
        
        except httpx.RequestError as e:
            logger.erro("groq_network_error",error=str(e))
            raise ProviderServerError(f"Network error connecting to Groq: {str(e)}")
        
    async def stream(self,messages: list[dict],**kwargs) -> AsyncGenerator:
        
        raise NotImplementedError("Streaming data to be soon...!")