import openai
import streamlit as st
#from gtts import gTTS
import base64
import pandas as pd
import time
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

#OpenAI API Key
openai.api_key = st.secrets["openai_key"]

#pull in some data
#state_requirements = pd.read_csv("https://raw.githubusercontent.com/2Maximus7/CGU/main/Homeschool%20Project%20MVP%20-%20State%20High%20School%20Grad%20Requirements.csv")
free_resources = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/catalyst/main/Catalyst%20Data%20-%20free%20resources.csv")

#FUNCTIONS
#auto play audio
def autoplay_audio(file_path: str):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio controls autoplay="true">
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
prompts = []
responses = []
def catalyst_ai_question(human_response,max_tokens):
    conversation = openai.Completion.create(
        model="text-davinci-003",
        #prompt="The following is a conversation with an AI assistant Catalyst who is helpful, creative, clever, and very friendly. Catalyst AI provides advice on learning and education with simple, clear language. Please think in steps and list resources when appropriate. Catalyst should finish its answer in a separate paragraph with 3 good questions to could ask Catalyst next.\n\nHuman:"+human_response,
        prompt="The following is a conversation with an AI assistant Catalyst who is helpful, creative, clever, and very friendly. Catalyst AI provides advice on learning and education with simple, clear language. Please think in steps and list resources when appropriate. Here's the question: "+human_response,
        temperature=0.5,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        #stop=[" Human:", " AI:"]
        )
    response = conversation["choices"][0]["text"]
    #responses.append(response)
    return response

def catalyst_ai_summarize(human_response,max_tokens):
    conversation = openai.Completion.create(
        model="text-davinci-003",
        #prompt="The following is a conversation with an AI assistant Catalyst who is helpful, creative, clever, and very friendly. Catalyst AI provides advice on learning and education with simple, clear language. Please think in steps and list resources when appropriate. Catalyst should finish its answer in a separate paragraph with 3 good questions to could ask Catalyst next.\n\nHuman:"+human_response,
        prompt="The following is a conversation with an AI assistant Catalyst who is helpful, creative, clever, and very friendly. Catalyst AI provides advice on learning and education with simple, clear language. Please summarize the following topic or resource: "+human_response,
        temperature=0.5,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        #stop=[" Human:", " AI:"]
        )
    response = conversation["choices"][0]["text"]
    #responses.append(response)
    return response

def catalyst_ai_question_for_personal_growth(response):
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
    return growth_response

def catalyst_ai_question_for_related(response):
    conversation = openai.Completion.create(
        model="text-davinci-003",
        prompt="Please provide one question that someone could ask to help them learn about related or competing topics based on this response to a question: "+response,
        temperature=0.5,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
        )
    related_response = conversation["choices"][0]["text"]
    return related_response

button_html = '''
<a href="{}" target="_blank">
    <button style="font-size: 16px; padding: 10px; background-color: #C96985; color: white;">
        Open
    </button>
</a>
'''

#START PAGE
#page setup
st.set_page_config(page_title="Catalyst: Lifelong Learning Everywhere", page_icon=":book:", layout="centered")

#st.image("https://github.com/maxwellknowles/catalyst/blob/main/DALL%C2%B7E%202022-12-29%2014.05%201.png?raw=true",width=200)

#menu
with st.sidebar:
    choose = option_menu("Catalyst", ["Home","Resources Repo", "Ask AI", "Bulk: Summarize or Answer", "Feedback", "Share"],
                            icons=['play-circle-fill','journals', 'chat-text-fill', 'table', 'envelope', "share-fill"],
                            menu_icon="app-indicator", default_index=0, orientation="vertical",
                            styles={
        "container": {"padding": "5!important", "background-color": "white"},
        "icon": {"black": "white", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#BBBBBD"},
        "nav-link-selected": {"background-color": "#C96985"},
    }
    )

#home
if choose=="Home":
    st.title("Catalyst")
    st.subheader("**Democratizing and expediting lifelong learning**")
    html = """
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets7.lottiefiles.com/packages/lf20_n8y71jlq.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;"  loop autoplay></lottie-player>
    """
    components.html(html,height=250)

    st.subheader("Knowledge doesn't belond to an age or zip code.")
    st.write("• Today, a person's outcomes are largely determined by where they are born and, by extension, the public education they receive.")
    st.write("• Learning for professional or personal growth both during and beyond our academic years is crucial but often unguided.")
    st.write("• People don't choose where they are born or how the world will evolve, but everyone has a right to learn and flourish.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("**That's where Catalyst comes in.**")
        st.write("Catalyst...")
        st.write("• surfaces **free resources** by type or purpose")
        st.write("• provides powerful **answers** to sets of prompts **en masse** for rapid information download")
        st.write("• features an **AI advisor** that not only answers but recommends **focused, goal-oriented questions** — an AI-infused application of the 2400 year old Socratic method")
        st.write("**Happy learning!**")
    with col2:
        html = """
       <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets3.lottiefiles.com/packages/lf20_bvleoupy.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;"  loop  autoplay></lottie-player>
        """
        components.html(html,height=500)

#free resources
if choose=="Resources Repo":
    st.title("Repository Repo")
    html = """
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <lottie-player src="https://assets2.lottiefiles.com/private_files/lf30_t8f3t4.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;"  loop  autoplay></lottie-player>
    """
    components.html(html,height=300)
    tab1, tab2 = st.tabs(["Free Learning", "Free Planning"])
    with tab1:
        #free learning resources
        st.subheader("Free Learning Resources")
        st.write("**Resources for high school, college, career, and personal growth! You can find more resources and even specific course recommendations by chatting with Catalyst AI.**")
        categories = free_resources.drop_duplicates("type")
        category = st.selectbox("Select a category!", categories['type'])
        free_resources = free_resources[(free_resources["type"]==category)]
        free_resources = free_resources.reset_index()
        col1, col2 = st.columns(2)
        for i in range(len(free_resources)):
            if i % 2 > 0:
                with col1:
                    st.subheader(free_resources["resource"][i])
                    st.write("Type: **"+free_resources["type"][i]+"**")
                    st.write(free_resources["description"][i])
                    st.markdown(button_html.format(free_resources["link"][i]), unsafe_allow_html=True)
            if i % 2 == 0:
                with col2:
                    st.subheader(free_resources["resource"][i])
                    st.write("Type: **"+free_resources["type"][i]+"**")
                    st.write(free_resources["description"][i])
                    st.markdown(button_html.format(free_resources["link"][i]), unsafe_allow_html=True)

    with tab2:
        #free planning resources for personal development or course/semester planning
        st.subheader("Free Planning Resources")
        st.write("**A few resources to help you manage courses, semesters, skill building, reading goals, and more...**")
        notion = "https://www.notion.so/templates/categories/education"
        kiddom = "https://www.kiddom.co/"
        dreammapping = "https://dreammapping.io/"
        st.write("Notion Templates: "+notion)
        st.write("Dream Mapping in Miro: "+dreammapping)
        st.write("Kiddom for Digital Classrooms: "+kiddom)

#start AI
#text to speech 
#myobj = gTTS(text=response, lang="en-uk", slow=False)
#myobj.save("audio.mp3")
#autoplay_audio("audio.mp3")
if choose=="Ask AI":
    st.title("Catalyst AI: An On-Demand Advisor & Tutor")
    html = """
       <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets5.lottiefiles.com/packages/lf20_wcjgoacf.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;" autoplay></lottie-player>
        """
    components.html(html,height=250)
    st.write("Each question may only have one answer, but one answer can inspire many questions. Catalyst focuses on asking good questions to focus your path towards better understanding.")
    st.subheader("Submit a prompt")
    st.write("Feel free to select an example prompt below or write your own :pencil:")
    if 'human_prompt_example' not in st.session_state:
        st.session_state.human_prompt_example = ""
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("What are some good alternatives to a 4-year degree?"):
            st.session_state.human_prompt_example="What are some good alternatives to a 4-year degree?"
    with col2:
        if st.button("Can you please walk me through Jungian philosophy?"):
            st.session_state.human_prompt_example="Can you please walk me through Jungian philosophy?"
    with col3:
        if st.button("What are some steps I can take to be a more well informed voter?"):
            st.session_state.human_prompt_example="What are some steps I can take to be a more well informed voter?"

    human_prompt = st.text_area("Ask a question", value=st.session_state.human_prompt_example)

    col1, col2 = st.columns([1,2])
    response = ""
    l=[]
    if st.button("Submit"):
        response = catalyst_ai_question(human_prompt,300)
        with st.spinner('AI is pondering...'):
            time.sleep(3)
        tup=(human_prompt,response)
        l.append(tup)
        st.write(response)
        growth_question = catalyst_ai_question_for_personal_growth(response)
        st.write("**Here's a good question you may want to ask now:** "+growth_question)
        #related_question = catalyst_ai_question_for_related(response)
        #st.write("Here's a good question you may want to ask to learn about competing or related topics: "+related_question)
    conversation = pd.DataFrame(l,columns=["Prompt","Response"])
    
    if len(conversation) > 0:
        
        conversation_csv = convert_df(conversation)

        st.write("**Download your question and response from Catalyst AI...**")
        st.download_button(
            label="Download",
            data=conversation_csv,
            file_name='catalyst.csv',
            mime='text/csv',
            )
        
if choose=="Bulk: Summarize or Answer":  
    st.title("Bulk: Summarize or Answer")  
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Summarize or answer a set of prompts")
        st.write("Catalyst leverages the latest developments in AI to comb through a list of prompts — Algebra questions, book titles, topics, etc — and provide summaries or answers for each one. This is meant as a tool for rapidly downloading information on a set of topics.\nIf you need help getting started, consider asking Catalyst's AI advisor for a list of resources on a topic.")

    with col2:
        html = """
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets4.lottiefiles.com/packages/lf20_z9gxmvaq.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;"  loop autoplay></lottie-player>
        """
        components.html(html,height=250)

    st.subheader("Upload prompts")

    st.write("**Step 1**")
    example = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/catalyst/main/catalyst_example.csv")
    example_csv = convert_df(example)
    st.download_button(
        label="Download Template",
        data=example_csv,
        file_name='catalyst_problems_and_answers.csv',
        mime='text/csv',
        )
    
    st.write("**Step 2**")
    uploaded_file = st.file_uploader("Choose a CSV file", accept_multiple_files=False)
    if uploaded_file is not None:
        problems = pd.read_csv(uploaded_file)

    st.write("**Step 3**")
    max_tokens = st.select_slider("Select max length of each response (in words)",options=range(200,1001))

    if uploaded_file is not None:
        if st.button("Answer Questions"):
            with st.spinner('Catalyst AI is working through your problems...'):
                time.sleep(2)
                l=[]
                for i in range(len(problems)):
                    problems["answer"][i] = catalyst_ai_question(problems['prompt'][i],max_tokens)
                    st.write("Answered question "+str(i+1))
            st.table(problems)
        
        if st.button("Summarize Topics or Resources"):
            with st.spinner('Catalyst AI is working through your problems...'):
                time.sleep(2)
                l=[]
                for i in range(len(problems)):
                    problems["answer"][i] = catalyst_ai_summarize(problems['prompt'][i],max_tokens)
                    st.write("Answered question "+str(i+1))
            st.table(problems)

        problems_and_answers_csv = convert_df(problems)
        st.write("**Download your prompts and responses from Catalyst AI...**")
        st.download_button(
            label="Download",
            data=problems_and_answers_csv,
            file_name='catalyst_problems_and_answers.csv',
            mime='text/csv',
            )
        

if choose=="Feedback":
    st.title("Submit Feedback")
    st.subheader("We appreciate your feedback!")
    st.write("Share recommended resources, feature requests, or bug reports...")
    jotform = """<script type="text/javascript" src="https://form.jotform.com/jsform/230567840430049"></script>"""
    components.html(jotform, height=1500)

if choose=="Share":
    st.title("Share Catalyst")
    #email
    subject = "Check out Catalyst, a platform for learning"
    body = "Take a look at Catalyst, an AI-powered project that's democratizing and expediting lifelong learning: https://catalyst-ai.streamlit.app/"
    st.markdown(f'<a href="mailto:?subject={subject}&body={body}">Share via Email</a>', unsafe_allow_html=True)

    #text
    text_message = "Take a look at Catalyst, an AI-powered project democratizing and expediting lifelong learning: https://catalyst-ai.streamlit.app/"
    st.markdown(f'<a href="sms:?body={text_message}">Share via Text</a>', unsafe_allow_html=True)

    #twitter
    html_twitter = """
        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" 
        data-text="Check out Catalyst, an AI-powered project that's democratizing and expediting lifelong learning..."
        data-url="https://catalyst-ai.streamlit.app/"
        data-show-count="false">
        data-size="Large" 
        data-hashtags="streamlit,python"
        Tweet
        </a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """

    components.html(html_twitter)
