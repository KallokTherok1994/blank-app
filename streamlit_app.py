import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"


def saveAndTestApiKey(api_key: str) -> bool:
    """Send the API key to the backend and trigger a connection test."""
    r = requests.post(f"{BACKEND_URL}/api-key", json={"api_key": api_key})
    if not r.ok:
        st.error(r.json().get("error", "Failed to save API key"))
        return False
    r = requests.get(f"{BACKEND_URL}/test")
    if r.ok:
        st.success("API key saved and connection successful")
        return True
    st.error(r.json().get("error", "Connection failed"))
    return False


def testConnection() -> bool:
    r = requests.get(f"{BACKEND_URL}/test")
    return r.ok


def callClaude(prompt: str) -> str:
    r = requests.post(f"{BACKEND_URL}/claude", json={"prompt": prompt})
    if r.ok:
        return r.json().get("completion", "")
    st.error(r.json().get("error", "Request failed"))
    return ""


st.title("🎈 My new app")

if "api_key_saved" not in st.session_state:
    st.session_state["api_key_saved"] = False

st.header("Setup")
api_key_input = st.text_input("API Key", type="password")
if st.button("Save and Test API Key"):
    st.session_state["api_key_saved"] = saveAndTestApiKey(api_key_input)

if st.session_state["api_key_saved"]:
    st.header("Chat with Claude")
    prompt = st.text_area("Prompt")
    if st.button("Call Claude"):
        response = callClaude(prompt)
        st.write(response)
