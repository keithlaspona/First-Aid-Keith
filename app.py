import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.globals import set_verbose
import os
import re
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Set the Streamlit page configuration (must be first Streamlit command)
st.set_page_config(
    page_title="First Aid Keith", 
    page_icon="https://i.ibb.co/PcHHP7c/First-Aid-Keith-Logo.png",  
    layout="wide"
)

# Set your Google API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set verbosity if needed
set_verbose(True)  # Enable verbose mode for debugging; set to False for normal operation

# Check if the API key is set
if not GOOGLE_API_KEY:
    st.error("Google API Key is not set. Please set the GOOGLE_API_KEY environment variable.")
else:
    # Create a ChatGoogleGenerativeAI instance
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

    # Function to format prompt with conversation history
    def format_prompt(question, conversation_history):
        prompt_template = (
            "You are a helpful and precise first-aid assistant. "
            "Provide concise and relevant answers based on your knowledge and the following history: {conversation_history} "
            "User: {question} Assistant:"
        )
        return prompt_template.format(conversation_history=conversation_history, question=question)

    # Function to generate a response based on user input
    def load_answer(question, conversation_history):
        prompt = format_prompt(question, conversation_history)
        response = llm.invoke(prompt)
        content = getattr(response, 'content', "No content available.")
        
        # Automatically convert words/phrases enclosed in ** to bold
        content = convert_to_bold(content)

        # Remove any HTML tags (e.g., </div>) in the content
        content = re.sub(r'</?div.*?>', '', content)

        # Strip leading and trailing whitespace
        content = content.strip()  

        return content

    def convert_to_bold(text):
        import re
        # Use regex to find all occurrences of **word/phrase**
        bold_pattern = re.compile(r'\*\*(.*?)\*\*')
        # Replace with HTML bold tags
        formatted_text = re.sub(bold_pattern, r'<b>\1</b>', text)
        # Remove any HTML tags (e.g., </div>)
        formatted_text = re.sub(r'</?div.*?>', '', formatted_text)
        return formatted_text

    # Initialize session state for chat history
    if 'sessionMessages' not in st.session_state:
        st.session_state.sessionMessages = []

# Custom CSS for styling and chat bubbles
st.markdown(
"""
<style>
.stApp {
    background-color: #ffffff;
    padding: 0;
    position: relative;
    min-height: 100vh; 
}
.chat-container {
    max-width: 600px;
    margin: auto;
    padding: 20px;
}
.stSidebar {
    background-color: #006666;
    color: #333; 
    padding: 20px; 
}
[data-testid="stBaseButton-secondary"] {
    color: black;
    background-color: #ffffff; /* Initial button color */
    border: none;
    border-radius: 5px;
    padding: 10px;
    text-align: center;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s, color 0.3s;
}

[data-testid="stBaseButton-secondary"]:hover {
    background-color: #19b659; /* Darker green on hover */
    color: #ffffff;
}

[data-testid="stBaseButton-secondary"]:active,
[data-testid="stBaseButton-secondary"]:focus {
    color: #ffffff !important; /* White text when clicked */
    background-color: #87d2a7 !important; /* Different color on click */
}
.centered-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 100vh; /* Full viewport height */
    text-align: center;
}
.centered-content img {
    width: 150px; /* Set the desired width for the logo */
    margin-bottom: 20px; /* Add space between the logo and text */
}
.centered-content h1 {
    font-size: 24px;
    color: white; /* Set the text color to white */
    margin: 0;
}
.user-message {
    text-align: right;
    background-color: #53d769;
    color: white;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    max-width: 70%;
    float: right;
    clear: both;
}
.bot-message {
    text-align: left;
    background-color: #f2faf4;
    color: black;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    max-width: 70%;
    display: inline-block;
    float: left;
    clear: both;
}
</style>
""",
unsafe_allow_html=True
)

# Sidebar content
sidebar_logo_url = "https://i.ibb.co/PcHHP7c/First-Aid-Keith-Logo.png"
st.sidebar.markdown(
    f"""
    <div class="sidebar-header" style="text-align: center; display: flex; flex-direction: column; align-items: center;">
        <img src="{sidebar_logo_url}" alt="Logo" width="192" style="margin-bottom: 10px;">
        <h1 style="font-family: 'Gill Sans', Tahoma, Geneva, Verdana, sans-serif; font-size: 24px; margin: 0; color: white;">First Aid Keith</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Create buttons for navigation
if st.sidebar.button('New Chat', use_container_width=True):
    st.session_state.page = "New Chat"
if st.sidebar.button('Chat History', use_container_width=True):
    st.session_state.page = "Chat History"
if st.sidebar.button('About First Aid Keith', use_container_width=True):
    st.session_state.page = "About First Aid Keith"

# Set default page
if 'page' not in st.session_state:
    st.session_state.page = "New Chat"

# Page routing based on session state
if st.session_state.page == "New Chat":
    # Display centered logo and header
    st.markdown(
        f"""
        <div class="centered-content">
            <img src="{sidebar_logo_url}" alt="First Aid Keith Logo">
            <h1>First Aid Keith</h1>
            <h2 style="font-family: 'Gill Sans', Tahoma, Geneva, Verdana, sans-serif; font-size: 40px; font-weight: bold;">First Aid Keith</h2>
            <p class="description" style="font-size: 18px; color: #333;">Here to Answer All Your First Aid Questions!</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Chat interface container
    st.markdown("<div class='chat-container' id='chat-container'>", unsafe_allow_html=True)

    # Display chat history
    if st.session_state.sessionMessages:
        for message in st.session_state.sessionMessages:
            content = convert_to_bold(message['content'])
            if message["role"] == "user":
                st.markdown(f"""
                <div class='message user-message'>
                    {content}
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='message bot-message'>
                    {content}
                </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Chat input box at the bottom
    user_input = st.text_input("Enter your question here:")

    # When user submits a question
    if user_input:
        # Append user message
        st.session_state.sessionMessages.append({"role": "user", "content": user_input})

        # Generate the conversation history for the assistant prompt
        conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.sessionMessages])

        # Get assistant response
        response = load_answer(user_input, conversation_history)
        st.session_state.sessionMessages.append({"role": "assistant", "content": response})

        # Clear the input box after submitting
        st.experimental_rerun()  # Rerun the script to update the UI immediately

        # Scroll to the bottom of the chat container
        st.markdown(
            """
            <script>
            var chatContainer = document.getElementById('chat-container');
            chatContainer.scrollTop = chatContainer.scrollHeight;
            </script>
            """,
            unsafe_allow_html=True
        )

elif st.session_state.page == "Chat History":
    st.write("### Chat History")

    # Display chat history if available
    if st.session_state.sessionMessages:
        for message in st.session_state.sessionMessages:
            content = convert_to_bold(message['content'])
            if message["role"] == "user":
                st.markdown(f"**User:** {content}", unsafe_allow_html=True)
            else:
                st.markdown(f"**Assistant:** {content}", unsafe_allow_html=True)
        
        # Clear chat history button
        if st.button("Clear Chat History"):
            st.session_state.sessionMessages.clear()
                st.experimental_rerun()  # Rerun to immediately reflect cleared history
    else:
        st.write("No chat history available.")

elif st.session_state.page == "About First Aid Keith":
    st.write(
        """
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
            <h2 style="font-family: 'Trebuchet MS', Helvetica, sans-serif; font-size: 32px; font-weight: bold; margin: 0;">About First Aid Keith</h2>
            <p style="font-family: 'Gill Sans', Tahoma, Geneva, Verdana, sans-serif; font-size: 16px; margin-top: 10px;">
                First Aid Keith is here to help you with all your first aid questions. Feel free to ask anything!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
