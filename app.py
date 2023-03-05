import openai
from mixpanel import Mixpanel
import uuid
import mixpanel
from openai import OpenAIError
import streamlit as st
import base64

#mixpanel
mp = Mixpanel(st.secrets["mixpanel"])
random_uuid = str(uuid.uuid4())
distinct_id = random_uuid

#FUNCTIONS
#auto play audio
def autoplay_audio(file_path: str):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay=false">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(
                md,
                unsafe_allow_html=True,
            )

#download data as CSV
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

#OpenAI prompt completion API
def catalyst_ai_question(human_response,max_tokens):
    try:
        conversation = openai.Completion.create(
            model="text-davinci-003",
            prompt="The following is a conversation with an AI assistant Catalyst who is helpful, creative, clever, and very friendly. Catalyst AI provides advice on learning and education with simple, clear language. Please think in steps and list resources when appropriate. Here's the question: "+human_response,
            temperature=0.5,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            )
        response = conversation["choices"][0]["text"]
    except OpenAIError as e:
        response = st.warning("Oops! Looks like we weren't able to process your request right now.")
    return response

def catalyst_ai_summarize(human_response,max_tokens):
    try:
        conversation = openai.Completion.create(
            model="text-davinci-003",
            prompt="The following is a conversation with an AI assistant Catalyst who is helpful, creative, clever, and very friendly. Catalyst AI provides advice on learning and education with simple, clear language. Please summarize the following topic or resource: "+human_response,
            temperature=0.5,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            )
        response = conversation["choices"][0]["text"]
    except OpenAIError as e:
        response = st.warning("Oops! Looks like we weren't able to process your request right now.")
    return response

def catalyst_ai_question_for_personal_growth(response):
    try:
        conversation = openai.Completion.create(
            model="text-davinci-003",
            prompt="Please provide one question that someone could ask to help them grow as a person based on this response to a question: "+response,
            temperature=0.5,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
            )
        growth_response = conversation["choices"][0]["text"]
    except OpenAIError as e:
        growth_response = st.warning("Oops! Looks like we weren't able to process your request right now.")
    return growth_response

def single_prompt_submitted(human_response,response,growth_response):
    try:
        mp.track(distinct_id=distinct_id,event_name="Single Prompt Submitted",properties={"Original Prompt":human_response,"Response":response,"Recommended Question":growth_response})
    except mixpanel.MixpanelException:
        pass

def bulk_prompt_submitted():
    try:
        mp.track(distinct_id=distinct_id,event_name="Bulk Prompt Submitted")
    except mixpanel.MixpanelException:
        pass

def resources_repo_viewed():
    try:
        mp.track(distinct_id=distinct_id,event_name="Resources Repo Viewed")
    except mixpanel.MixpanelException:
        pass

def share_page_viewed():
    try:
        mp.track(distinct_id=distinct_id,event_name="Share Page Viewed")
    except mixpanel.MixpanelException:
        pass
