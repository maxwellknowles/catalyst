import streamlit as st
import pandas as pd
import time
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from app import convert_df, catalyst_ai_question, catalyst_ai_summarize, catalyst_ai_question_for_personal_growth, single_prompt_submitted, bulk_prompt_submitted, resources_repo_viewed, share_page_viewed

#pull in some data
free_resources = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/catalyst/main/Catalyst%20Data%20-%20free%20resources.csv")
questions = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/catalyst/main/Catalyst%20Data%20-%20great%20questions.csv")

#code for buttons linking off-site
button_html = '''
<a href="{}" target="_blank">
    <button style="font-size: 16px; padding: 10px; background-color: #C96985; color: white;">
        Open
    </button>
</a>
'''

#page setup
st.set_page_config(page_title="Guided: Lifelong Learning Everywhere", page_icon=":stars:", layout="centered")

#START PAGE
#menu
with st.sidebar:
    choose = option_menu("Guided", ["Home","Resources Repo", "Ask AI", "Rapid Learning", "Feedback", "Share"],
                            icons=['house-door-fill','collection-fill', 'chat-text-fill', 'table', 'envelope', "share-fill"],
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
    st.title("Guided")
    st.subheader("**Free, rapid learning for everyone, everywhere.**")
    html = """
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets7.lottiefiles.com/packages/lf20_n8y71jlq.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;"  loop autoplay></lottie-player>
    """
    components.html(html,height=250)

    st.subheader("Knowledge doesn't belong to an age or zip code.")
    st.write("• Today, a person's outcomes are largely determined by where they are born and, by extension, the public education they receive.")
    st.write("• Structured learning for professional, civic, and personal growth during our academic years is often weak, and after school, near non-existent.")
    st.write("• People don't choose where they are born or how the world will evolve, but everyone should be able to flourish throughout their lives.")

    st.subheader("**That's where Guided comes in.**")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Guided provides...**")
        st.write(">**Collected free resources:** A repository of online courses, book repositories, language learning, and code programs")
        st.write(">**Rapid learning:** Guided can answer or summarize sets of prompts **in bulk** for accelerated information download")
        st.write(">**An AI advisor:** ChatGPT meets Socrates in this directed prompt/response interface that not only answers but _*facilitates*_ **focused, goal-oriented questions**")
    with col2:
        html = """
       <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets3.lottiefiles.com/packages/lf20_bvleoupy.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;"  loop  autoplay></lottie-player>
        """
        components.html(html,height=500)
    st.write("If you're a **student**, **young professional**, or simply enjoy **learning new things faster**, then you have found a tool to use and share. If you aren't open to exploring online resources, embracing AI responsibly, or changing the way you think, you should probably close this tab.")
    st.write("**Happy learning!**")
    
#free resources
if choose=="Resources Repo":
    resources_repo_viewed()
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
        st.write("**Resources for high school, college, career, and personal growth! You can find more resources and even specific course recommendations by chatting with Guided AI.**")
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

#submitting one prompt at a time based on goal (similar to Chat-GPT)
if choose=="Ask AI":
    
    st.title("Guided AI: An On-Demand Advisor & Tutor")
    html = """
       <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets5.lottiefiles.com/packages/lf20_wcjgoacf.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;" autoplay></lottie-player>
        """
    components.html(html,height=250)

    st.write("Each question may only have one answer, but one answer can inspire many questions. Guided focuses on asking good questions to focus your path towards better understanding.")
    
    st.subheader("Submit a prompt")

    st.write("**First, establish your goal**")

    st.write("When we ask a question, it's important to know what we're trying to accomplish. Why are you asking Guided a question?")

    col1, col2, col3 = st.columns(3)

    questions_narrowed = questions
    search_list = []
    with col1:
        if st.checkbox("I need help on an assignment"):
            goal = "I need help on an assignment"
            questions_narrowed = questions[(questions["goal"]==goal)]
            search_list = list(questions_narrowed["question"])
    with col2:
        if st.checkbox("I want to improve my day-to-day living"):
            goal = "I want to improve my day-to-day living"
            questions_narrowed = questions[(questions["goal"]==goal)]
            search_list = list(questions_narrowed["question"])
    with col3:
        if st.checkbox("I want to grow my life direction"):
            goal = "I want to grow my life direction"
            questions_narrowed = questions[(questions["goal"]==goal)]
            search_list = list(questions_narrowed["question"])

    st.write("**Next, choose a question**")
    if 'human_prompt_example' not in st.session_state:
        st.session_state.human_prompt_example = ""
    st.session_state.human_prompt_example = st.selectbox(
        "Select an example question based on your goal or write your own below",
        search_list)

    human_prompt = st.text_area("Ask a question", value=st.session_state.human_prompt_example)

    #prompts and responses
    prompts = []
    responses = []

    col1, col2 = st.columns([1,2])
    response = ""
    l=[]
    if st.button("Submit"):
        with st.spinner('AI is pondering...'):
            time.sleep(3)
        response = catalyst_ai_question(human_prompt,300)
        tup=(human_prompt,response)
        l.append(tup)
        st.write(response)
        with st.spinner('Preparing a recommended question...'):
            time.sleep(2)
        growth_question = catalyst_ai_question_for_personal_growth(response)
        st.write("**Here's a good question you may want to ask now:** "+growth_question)
        single_prompt_submitted(human_prompt, response, growth_question)
    conversation = pd.DataFrame(l,columns=["Prompt","Response"])
    
    if len(conversation) > 0:
        
        conversation_csv = convert_df(conversation)

        st.write("**Download your question and response from Guided AI...**")
        st.download_button(
            label="Download",
            data=conversation_csv,
            file_name='guided.csv',
            mime='text/csv',
            )

#uploading groups of prompts        
if choose=="Rapid Learning":  
    st.title("Rapid Learning")  
    col1, col2 = st.columns([1.5,1])
    with col1:
        st.subheader("Summarize or answer prompts in bulk")
        st.write("Guided leverages the latest developments in AI to comb through a list of prompts — math problems, book titles, a set of spiritual disciplines, etc — and provide summaries or answers for each one. This is a tool for rapidly downloading information to help you in your research and learning.\nIf you need help getting started, consider asking Guided's AI advisor for a list of resources or questions on a topic.")

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
        file_name='guided_prompts_and_responses.csv',
        mime='text/csv',
        )
    
    st.write("**Step 2**")
    uploaded_file = st.file_uploader("Choose a CSV file (must have one 'prompt' column and one blank 'answer' column)", accept_multiple_files=False)
    if uploaded_file is not None:
        problems = pd.read_csv(uploaded_file)

    st.write("**Step 3**")
    max_tokens = st.select_slider("Select max length of each response (in words)",options=range(200,1001))

    if uploaded_file is not None:
        if st.button("Answer Questions"):
            bulk_prompt_submitted()
            with st.spinner('Guided AI is working through your problems...'):
                time.sleep(2)
                l=[]
                for i in range(len(problems)):
                    problems["answer"][i] = catalyst_ai_question(problems['prompt'][i],max_tokens)
                    with st.spinner("Answered question "+str(i+1)):
                        time.sleep(1)
            st.table(problems)
        
        if st.button("Summarize Topics or Resources"):
            bulk_prompt_submitted()
            with st.spinner('Guided AI is working through your problems...'):
                time.sleep(2)
                l=[]
                for i in range(len(problems)):
                    problems["answer"][i] = catalyst_ai_summarize(problems['prompt'][i],max_tokens)
                    st.write("Answered question "+str(i+1))
            st.table(problems)

        problems_and_answers_csv = convert_df(problems)
        st.write("**Download your prompts and responses from Guided AI...**")
        st.download_button(
            label="Download",
            data=problems_and_answers_csv,
            file_name='guided_prompts_and_responses.csv',
            mime='text/csv',
            )

#jotform feedback form        
if choose=="Feedback":
    st.title("Submit Feedback")
    st.write("Share recommended resources, feature requests, or bug reports...")
    jotform = """<script type="text/javascript" src="https://form.jotform.com/jsform/230567840430049"></script>"""
    components.html(jotform, height=1500)

#email, text, and twitter share options
if choose=="Share":
    share_page_viewed()
    st.title("Share Guided")
    #email
    subject = "Check out Guided, a platform for learning"
    body = "Take a look at Guided, an AI-powered project that's democratizing and expediting lifelong learning: https://guided-ai.streamlit.app/"
    st.markdown(f'<a href="mailto:?subject={subject}&body={body}">Share via Email</a>', unsafe_allow_html=True)

    #text
    text_message = "Take a look at Guided, an AI-powered project democratizing and expediting lifelong learning: https://guided-ai.streamlit.app/"
    st.markdown(f'<a href="sms:?body={text_message}">Share via Text</a>', unsafe_allow_html=True)

    #twitter
    html_twitter = """
        <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" 
        data-text="Check out Guided, an AI-powered project that's democratizing and expediting lifelong learning..."
        data-url="https://guided-ai.streamlit.app/"
        data-show-count="false">
        data-size="Large" 
        data-hashtags="streamlit,python"
        Tweet
        </a>
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    """

    components.html(html_twitter)
