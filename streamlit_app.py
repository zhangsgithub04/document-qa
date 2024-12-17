import streamlit as st
from openai import OpenAI
import os

# Show title and description.
st.title("📄 Question Generator")
st.write(
    "Ques "
    "Your feedback will be helpful. "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
#openai_api_key = st.text_input("OpenAI API Key", type="password")
openai_api_key = st.secrets["openai_api_key"]
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)


    os.write(1,b'Something was executed.\n')

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Display uploaded file name and content
    if uploaded_file:
        st.write(f"**Uploaded File:** {uploaded_file.name}")
        with st.expander("View File Content"):
            st.write(uploaded_file.read().decode())

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "How many questions do you want to generate",
        placeholder="10",
        disabled=not uploaded_file,
    )

    # Button to trigger question generation
    if uploaded_file:
        if question:
            generate_button = st.button("Generate Questions")
        else:
            st.warning("Please enter the number of questions to generate.")
            generate_button = False
    else:
        st.info("Please upload a file first.")
        generate_button = False

    if generate_button:
        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n Please generate {question} short answer questions with reference answers",
            }
        ]

        # Generate an answer using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)