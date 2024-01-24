import streamlit as st
import random
import time
import requests
import json

# interact with FastAPI endpoint
backend = "http://localhost:8000/ask"

def process(prompt):
    url = f"http://127.0.0.1:8000/ask/?query={prompt}"
    with requests.get(url, stream=True) as res:
        for chunk in res.iter_content(1024):
            yield chunk

# def process(prompt):
#     with requests.post(backend, json={"question": prompt}, stream=True) as res:
#         for line in res.iter_lines():
#             if line:
#                 json_response = json.loads(line.decode('utf-8'))
#                 yield json_response["part"]
                
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
        buffer = ""
        for chunk in process(prompt):
            decoded_chunk = chunk.decode('utf-8')
            buffer += decoded_chunk
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                parsed_chunk = line
                try:
                    full_response += parsed_chunk
                    message_placeholder.markdown(full_response + "▌")
                except KeyError:
                    pass
        message_placeholder.markdown(full_response)

    # # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     message_placeholder = st.empty()
    #     full_response = ""
    #     for part_response in process(prompt):
    #         st.markdown(part_response.decode('utf-8'))
        # assistant_response = process(prompt)
        # # # Simulate stream of response with milliseconds delay
        # # for chunk in assistant_response.split():
        # #     full_response += chunk + " "
        # #     time.sleep(0.05)
        # #     # Add a blinking cursor to simulate typing
        # #     message_placeholder.markdown(full_response + "▌")
        # message_placeholder.write(part_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    # st.session_state.messages.append({"role": "assistant", "content": full_response})

    # GOOD OR BAD with response
    columns = st.columns((1,1,5,1))
    with columns[3]:
        semi_col = st.columns(2)
        with semi_col[0]:
            st.button("👍", use_container_width=True) #<- Button on the right
        with semi_col[1]:
            st.button("👎", use_container_width=True) #<- Button on the right