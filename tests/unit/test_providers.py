# pyrefly: ignore [missing-import]
import pytest
# pyrefly: ignore [missing-import]
import httpx
from app.services.providers.groq import GroqProvider
# pyrefly: ignore [missing-import]
from app.core.exceptions import ProviderServerError

@pytest.mark.asyncio
async def test_groq_provider_complete_success(mock_groq_api):

    # Setting up mock route and fake response
    mock_groq_api.post("/openai/v1/chat/completions").respond(
        status_code=200,
        json={
            "id":"chatcmpl-test1234",
            "choices": [{"message":{"role":"assistant","content":"Mocked Hello"}}],
            "usage":{"prompt_tokens":10,"completion_tokens":5, "total_tokens":15}
        }
    )

    # Respx intercepts this http call and sends the fake response
    async with httpx.AsyncClient() as client:
        provider = GroqProvider(
            http_client=client,
            api_key="test_key",
            base_url="https://api.groq.com",
            model="llama-3.1-8b-instant"
        )

        messages = [{"role":"user", "content":" Say Hello"}]
        # getting response from our groq provider with the interfernce of respx
        response = await provider.complete(messages=messages)

        assert response["choices"][0]["message"]["content"] == "Mocked Hello"
        assert response["usage"]["total_tokens"] == 15

@pytest.mark.asyncio
async def test_groq_provider_complete_server_error(mock_groq_api):

    mock_groq_api.post("/openai/v1/chat/completions").respond(
        status_code=500,
        json={
            "error":{
                "message":"Groq server error"
            }
        }
    )

    async with httpx.AsyncClient() as client:
        provider = GroqProvider(
            http_client=client,
            api_key="test_key",
            base_url="https://api.groq.com",
            model="llama-3.1-8b-instant"
        )

    messages = [{"role":"user","content":"Say Hello"}]

    # getting response from groq provider for error
    with pytest.raises(ProviderServerError) as e:
        await provider.complete(messages=messages)

    assert "500" in str(e.value)
