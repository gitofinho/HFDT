import streamlit as st
import random
import time
import requests
import json

# interact with FastAPI endpoint
backend = "http://localhost:8000/ask"

def process(prompt):
    with requests.post(backend, json={"question": prompt}, stream=True) as res:
        for line in res.iter_lines():
            if line:
                json_response = json.loads(line.decode('utf-8'))
                yield json_response["part"]
                
st.set_page_config(page_title='HFDT-Platform' ,layout="wide",page_icon='🚀')

"## 🛸 HFGPT"
st.write("")

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # CASE 1, Langchain
        # assistant_response = llm(prompt)

        # CASE 2, RANDOM
        # assistant_response = random.choice(
        #     [
        #         "Hello there! How can I assist you today?",
        #         "Hi, human! Is there anything I can help you with?",
        #         "Do you need help?",
        #     ]
        # )
        
        # CASE 3, Hugging Face
        for part_response in process(prompt):
            st.markdown(part_response)
        # assistant_response = process(prompt)
        # # # Simulate stream of response with milliseconds delay
        # # for chunk in assistant_response.split():
        # #     full_response += chunk + " "
        # #     time.sleep(0.05)
        # #     # Add a blinking cursor to simulate typing
        # #     message_placeholder.markdown(full_response + "▌")
        # message_placeholder.write(part_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": part_response})
    # st.session_state.messages.append({"role": "assistant", "content": full_response})

    # GOOD OR BAD with response
    columns = st.columns((1,1,5,1))
    with columns[3]:
        semi_col = st.columns(2)
        with semi_col[0]:
            st.button("👍", use_container_width=True) #<- Button on the right
        with semi_col[1]:
            st.button("👎", use_container_width=True) #<- Button on the right