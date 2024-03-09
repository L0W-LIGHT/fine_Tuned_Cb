import streamlit as st
import google.generativeai as genai

# Configure the model
genai.configure(api_key="AIzaSyBZmyKqMVWxFn6q4SJ3CTa3MJcKZg2cIjA")

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_ONLY_HIGH"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Streamlit app title
st.title("Child Psychology Chatbot")

# Initialize a session to keep track of the conversation
session_state = st.session_state
if "conversation" not in session_state:
    session_state.conversation = []

# Function to generate a response
def generate_response(user_input):
    prompt_parts = [
        f"input: {user_input}",
        "output: "
    ]
    response = model.generate_content(prompt_parts)
    return response.text

# Main area for displaying the conversation
chat_container = st.container()
with chat_container:
    st.image("https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/mobile-phone_1f4f1.png", width=50)
    st.write("Hi there! I'm here to help with any questions you have about your child's mental health.")
    st.write("Feel free to ask me anything.")

# Sidebar for user input
user_input = st.text_input("Your message:")
submit_button = st.button("Send")

if submit_button:
    if user_input.lower() in ["quit", "exit"]:
        session_state.conversation.append("You: " + user_input)
        session_state.conversation.append("Bot: Conversation ended.")
    else:
        # Generate the response
        response = generate_response(user_input)
        # Add the user's question and the bot's response to the conversation
        session_state.conversation.append("You: " + user_input)
        session_state.conversation.append("Bot: " + response)

# Display conversation
with chat_container:
    for message in session_state.conversation:
        if message.startswith("You:"):
            st.text_area("You:", value=message, height=100, max_chars=None, key=None)
        elif message.startswith("Bot:"):
            st.text_area("Bot:", value=message, height=100, max_chars=None, key=None)
