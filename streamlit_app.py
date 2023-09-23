import os 

import openai
import streamlit as st

from streamlit_chat import message


openai.api_key = os.environ.get('AZURE_OPENAI_KEY')
openai.api_base = os.environ.get('AZURE_OPENAI_ENDPOINT')
openai.api_type = 'azure'
openai.api_version = '2023-05-15' # this may change in the future
deployment_name = os.environ.get('DEPLOYMENT_NAME')

# openai.api_key = os.environ.get('API_KEY')
# openai.api_key = os.environ.get('API_KEY')


def generate_response(prompt):
    completion=openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.6,
    )
    message=completion.choices[0].text
    return message


def get_completion(prompt, model=deployment_name):
    messages = [{"role": "system", "content": "Assistant is a large language model trained by OpenAI.",
                 "role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        engine=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == os.environ.get("USER_PASSWORD"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
    st.title("Azure GPT Web App")

    st.experimental_get_query_params()
    #{"show_map": ["True"], "selected": ["asia", "america"]}

    #storing the chat
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []
    if 'past' not in st.session_state:
        st.session_state['past'] = []
    user_input=st.text_input("You:", key='input')
    if user_input:
        output=get_completion(user_input)
        #store the output
        st.session_state['past'].append(user_input)
        st.session_state['generated'].append(output)
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])-1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
