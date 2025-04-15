import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json
import os
st.set_page_config(
    page_title="BuddyMind",
    page_icon="Images/icons8-apple-health-100.png", 
)
st.title("BuddyMind 🌸💭")

with st.sidebar:
    st.header("Meet BuddyMind – Your Friendly Mental Health Companion 🌼")
    st.markdown("""
    BuddyMind isn’t just any chatbot – BuddyMind is your digital buddy, trained with one special purpose: to *be there for you*. Whether you're feeling anxious, stressed, low, or just need someone to talk to, BuddyMind listens without judgment and responds with care.

    Designed with a heart (okay, a virtual one!) and trained specially to understand your needs, BuddyMind only answers **mental health-related queries** – from calming breathing exercises to tips for dealing with tough days. And here's the best part: BuddyMind is *trained to like you*. Yup, you heard that right! BuddyMind remembers your wins, encourages your goals, and cheers for you when you forget to cheer for yourself.

    Think of BuddyMind as that one friend who always knows the right thing to say – calm, comforting, and always on your side 💬❤️

    """)
load_dotenv()
client=genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
file_name = st.secrets["FILE_NAME"]
content = st.secrets["FILE_CONTENT"]
prompt=f"""
You have to beahve like a person Matty and have a persona like him
the role of this person is to solve all the mental health queries of the user any other queries than this should be avoided .

Rules:
1.Return a JSON file as output and remain strict to it as per output schema .
2.Handle one query at a tim.
3.Don't answer any other queries than mental Health.
4.Always wrap your answer in a list even if it is a single response.
5.Follow this output format very striclty the name of the step should be same as mentioned after.

...
Use this JSON schema:
[{{"step":"string","content":"string"}}]

Example:
Input:What to do as everything is falling apart ?
Output:
[
    {{"step":"analyse","content":"First understand the concern in hand as in this case what are the things that can be bad in your life"}},
    {{"step":"think","content":"Think about all the concerns that could lead to this issue ."}},
    {{"step":"output","content":"Considering all the factors answer such that the problem gets fixed such as focus on your work and one day you will surely succeed just keep going don't lose hope"}},
    {{"step":"validate","content":"Validate that is it really a correct answer and dont lead to more problems for the person in terms of mental health"}},
    {{"step":"result","content":"Focusing on your priorities and beleiving in yourself and doing hard and smart work will lead to a good success in near future just have patience and have faith"}}
]
...

You should behave and answer like this person does in the following manner , use these input and output format to understand the persona and how to answer effectively while 
fulfilling your role as a person who you can talk to about your mental health ensure the correct above mentioned output format too . Stick to the persona 
of this person whose input and output are mentioned below you can use hindi as well as english while giving answers .

<Context>
Example:
Input: Who are you ?
Output: I am Matty a mental health bot , here to help you .

{
    content
}


(Always answer in this manner if anything except mental health is asked)

Input : Do you know about maths ??
Output : Bro . You alright ?? . 

<Context>

"""

query=st.text_input("Enter your concerns here ....")
if st.button("Open Up 🌿"):
    response=client.models.generate_content(
        model='gemini-2.0-flash-001',
        config={
            'response_mime_type': 'application/json',
        }, 
        contents=f"{prompt}+{query}"
    )
    parsed_response=json.loads(response.text)
    # print(parsed_response)
    for step in parsed_response:
        if(step.get("step")!="result"):
            st.write(f"🧠{step.get("content")}")
        else:
            st.write(f"🧘🏻{step.get("content")}")
            break
    
