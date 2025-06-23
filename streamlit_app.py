import streamlit as st
import aiohttp
import asyncio


async def fetch(url: str):
    """Fetch JSON from a URL with graceful fallback when parsing fails."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            try:
                return await response.json()
            except Exception:
                text = await response.text()
                message = text or "No response body"
                raise RuntimeError(message)


st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

url = st.text_input("URL", "https://example.com/api")
if st.button("Fetch data"):
    try:
        data = asyncio.run(fetch(url))
        st.toast(str(data))
    except Exception as e:
        st.toast(str(e) or "Unknown error")
