import asyncio
import redis.asyncio as redis

async def main():
    try:
        r = redis.from_url('redis://localhost:6379/0', decode_response=True)
        await r.ping()
        await r.aclose()
        print("Success")
    except Exception as e:
        print(f"Error: type={type(e).__name__}, msg={e}")

asyncio.run(main())
