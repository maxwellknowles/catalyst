import streamlit as st
import pandas as pd
import time
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from app import convert_df, catalyst_ai_question, catalyst_ai_summarize, catalyst_ai_question_for_personal_growth, single_prompt_submitted, bulk_prompt_submitted, resources_repo_viewed, share_page_viewed, get_video

#pull in some data
resources = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/catalyst/main/resources.csv")
questions = pd.read_csv("https://raw.githubusercontent.com/maxwellknowles/catalyst/main/Catalyst%20Data%20-%20great%20questions.csv")

resources_list = []
for i in range(len(resources)):
    name = resources["resource"][i]
    description = resources["description"][i]
    link = resources["link"][i]
    string = name + ": " + description + " Link: " + link
    resources_list.append(string)

#code for buttons linking off-site
button_html = '''
<a href="{}" target="_blank">
    <button style="font-size: 16px; padding: 10px; background-color: #C96985; color: white;">
        Open
    </button>
</a>
'''

#page setup
st.set_page_config(page_title="GuidedAI: Free, rapid learning for everyone, everywhere", page_icon=":brain:", layout="wide")

#START PAGE
#menu
choose = option_menu("GuidedAI: Free, rapid learning for everyone, everywhere", ["Home","About","Resources", "Ask AI", "Batch Learning", "Feedback", "Share"],
                            icons=['house-door-fill','journal','collection-fill', 'chat-text-fill', 'table', 'envelope', "share-fill"],
                            menu_icon="stars", default_index=0, orientation="horizontal",
                            styles={
        "container": {"padding": "5!important", "background-color": "white"},
        "icon": {"black": "white", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#BBBBBD"},
        "nav-link-selected": {"background-color": "#C96985"},
    }
    )

st.title("GuidedAI")
#home
if choose=="Home":
    steps = 3
    steps_completed = 0

    #prompt session states
    if "user" not in st.session_state:
        st.session_state.user = ""
    if "direction" not in st.session_state:
        st.session_state.direction = ""
    if "problem" not in st.session_state:
        st.session_state.problem = ""

    #first question session states
    if "prompt" not in st.session_state:
        st.session_state.prompt = False
    if "response" not in st.session_state:
        st.session_state.response = ""
    
    #second question session states
    if "secondary_response" not in st.session_state:
        st.session_state.secondary_response = ""
    if "second_prompt" not in st.session_state:
        st.session_state.second_prompt = ""

    #rec resources
    if "rec_resources" not in st.session_state:
        st.session_state.rec_resources = ""

    col1, col2 = st.columns([1,2], gap="large")
    with col1:
        st.session_state.user = st.text_input("I am a(n)...", placeholder="lifelong learner", value=st.session_state.user)
        if st.session_state.user:
            steps_completed += 1

        st.session_state.direction = st.selectbox("who wants to...", ("","learn", "solve a problem", "get advice"))
        if st.session_state.direction:
            steps_completed += 1
        
        st.session_state.problem = st.text_area("about...", placeholder="having more productive conversations", value=st.session_state.problem)
        if st.session_state.problem:
            steps_completed += 1

        st.progress(steps_completed/steps)
        first_prompt = "I am a "+st.session_state.user+" who wants to "+st.session_state.direction+" about "+st.session_state.problem+". Please provide advice or a solution."
        second_prompt = "I am a "+st.session_state.user+" who wants to "+st.session_state.direction+" about "+st.session_state.problem+". What might be the best few resources from the following? Please explain why and include the link \n"+str(resources_list)

        submit = st.button("Submit", key=0, use_container_width=True, type="primary")

        if submit:
            st.session_state.prompt = True
            with st.spinner('GuidedAI is pondering...'):
                time.sleep(3)
            st.session_state.response = catalyst_ai_question(first_prompt,500)

    with col2:
        
        if st.session_state.response == "":
            st.write("Describe your goal, get answers and resources. That's it!")
            get_video()
        else:
            st.write("**Guided's Response**")
            st.write(st.session_state.response)

            with st.expander("Ask GuidedAI A Question"):

                st.write("**Let's continue...**")

                if st.session_state.response != "":
                    rec_question = catalyst_ai_question_for_personal_growth(st.session_state.response)
                else:
                    rec_question = ""

                new_prompt = st.text_input("What would you like to ask?", value=rec_question, key=1)

                if st.button("Submit"):
                    with st.spinner('GuidedAI is pondering...'):
                        time.sleep(3)
                    st.session_state.secondary_response = catalyst_ai_question(new_prompt,500)

                    st.write(st.session_state.secondary_response)

                    with st.spinner('Preparing a recommended question...'):
                        time.sleep(2)
                    rec = catalyst_ai_question_for_personal_growth(st.session_state.secondary_response)
                    st.write("**Here's a good question you may want to ask now:** "+rec)

            with st.expander("Explore Recommended Resources") or st.session_state.rec_resources:

                #free learning resources
                st.subheader("Free Learning Resources")

                if st.session_state.response != "":
                    rec_resources = catalyst_ai_question(second_prompt,250)

                    st.write(str(rec_resources))

                st.write("\nYou can also filter through our list of digitally-based, accessible resources for yourself...")

                categories = ["Books", "Platform", "Online Courses", "Online Degree", "Blog", "Newsletter", "Community"]
                category = st.selectbox("Select a type of resource", categories)

                filtered_resources = resources.loc[(resources["form"]==category)]
                filtered_resources = filtered_resources.reset_index()

                for i in range(len(filtered_resources)):
                    st.subheader(filtered_resources["resource"][i])
                    st.write("Type: **"+filtered_resources["form"][i]+"**")
                    st.write(filtered_resources["description"][i])
                    st.markdown(button_html.format(filtered_resources["link"][i]), unsafe_allow_html=True)
    
if choose=="About":
    st.header("About")

    html = """
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets7.lottiefiles.com/packages/lf20_n8y71jlq.json"  background="transparent"  speed="1"  style="width: 200px; height: 200px;"  loop autoplay></lottie-player>
    """
    components.html(html,height=200)
   
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

    email_html = """
            <!-- Begin Mailchimp Signup Form -->
        <link href="//cdn-images.mailchimp.com/embedcode/classic-071822.css" rel="stylesheet" type="text/css">
        <style type="text/css">
            #mc_embed_signup{background:#fff; clear:left; font:14px Helvetica,Arial,sans-serif;  width:600px;}
            /* Add your own Mailchimp form style overrides in your site stylesheet or in this style block.
            We recommend moving this block and the preceding CSS link to the HEAD of your HTML file. */
        </style>
        <div id="mc_embed_signup">
            <form action="https://gmail.us3.list-manage.com/subscribe/post?u=334d52076753891f71b9f4240&amp;id=24f3985bec&amp;f_id=00a241e2f0" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
                <div id="mc_embed_signup_scroll">
                <h2>Join Guided</h2>
                <div class="indicates-required"><span class="asterisk">*</span> indicates required</div>
        <div class="mc-field-group">
            <label for="mce-EMAIL">Email Address  <span class="asterisk">*</span>
        </label>
            <input type="email" value="" name="EMAIL" class="required email" id="mce-EMAIL" required>
            <span id="mce-EMAIL-HELPERTEXT" class="helper_text"></span>
        </div>
            <div id="mce-responses" class="clear foot">
                <div class="response" id="mce-error-response" style="display:none"></div>
                <div class="response" id="mce-success-response" style="display:none"></div>
            </div>    <!-- real people should not fill this in and expect good things - do not remove this or risk form bot signups-->
            <div style="position: absolute; left: -5000px;" aria-hidden="true"><input type="text" name="b_334d52076753891f71b9f4240_24f3985bec" tabindex="-1" value=""></div>
                <div class="optionalParent">
                    <div class="clear foot">
                        <input type="submit" value="Subscribe" name="subscribe" id="mc-embedded-subscribe" class="button">
                        <p class="brandingLogo"><a href="http://eepurl.com/img2to" title="Mailchimp - email marketing made easy and fun"><img src="https://eep.io/mc-cdn-images/template_images/branding_logo_text_dark_dtp.svg"></a></p>
                    </div>
                </div>
            </div>
        </form>
        </div>
        <script type='text/javascript' src='//s3.amazonaws.com/downloads.mailchimp.com/js/mc-validate.js'></script><script type='text/javascript'>(function($) {window.fnames = new Array(); window.ftypes = new Array();fnames[0]='EMAIL';ftypes[0]='email';fnames[1]='FNAME';ftypes[1]='text';fnames[2]='LNAME';ftypes[2]='text';fnames[3]='ADDRESS';ftypes[3]='address';fnames[4]='PHONE';ftypes[4]='phone';fnames[5]='BIRTHDAY';ftypes[5]='birthday';fnames[6]='MMERGE6';ftypes[6]='text';}(jQuery));var $mcj = jQuery.noConflict(true);</script>
        <!--End mc_embed_signup-->
    """
    components.html(email_html,height=300)
    
#free resources
if choose=="Resources":
    resources_repo_viewed()
    st.header("Repository Repo")
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
        categories = resources.drop_duplicates("form")
        category = st.selectbox("Select a category!", categories['form'])
        resources = resources[(resources["form"]==category)]
        resources = resources.reset_index()
        col1, col2 = st.columns(2)
        for i in range(len(resources)):
            if i % 2 > 0:
                with col1:
                    st.subheader(resources["resource"][i])
                    st.write("Type: **"+resources["form"][i]+"**")
                    st.write(resources["description"][i])
                    st.markdown(button_html.format(resources["link"][i]), unsafe_allow_html=True)
            if i % 2 == 0:
                with col2:
                    st.subheader(resources["resource"][i])
                    st.write("Type: **"+resources["form"][i]+"**")
                    st.write(resources["description"][i])
                    st.markdown(button_html.format(resources["link"][i]), unsafe_allow_html=True)

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
    st.header("An On-Demand Advisor & Tutor")
    html = """
       <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
        <lottie-player src="https://assets5.lottiefiles.com/packages/lf20_wcjgoacf.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px;" autoplay></lottie-player>
        """
    components.html(html,height=250)

    st.write("**Submit a prompt**")

    st.write("Each question may only have one answer, but one answer can inspire many questions. Guided focuses on asking good questions to focus your path towards better understanding.")

    st.write("When we ask a question, it's important to know what we're trying to accomplish. Why are you asking GuidedAI a question?")

    questions_narrowed = questions
    search_list = []

    st.write("**Next, choose a question**")
    if 'human_prompt_example' not in st.session_state:
        st.session_state.human_prompt_example = ""

    st.session_state.human_prompt_example = st.text_area("Ask a question", key=1)
    
    #prompts and responses
    prompts = []
    responses = []

    col1, col2 = st.columns([1,2])
    response = ""
    l=[]
    if st.button("Submit"):
        with st.spinner('GuidedAI is pondering...'):
            time.sleep(3)
        response = catalyst_ai_question(st.session_state.human_prompt_example,300)
        tup=(st.session_state.human_prompt_example,response)
        l.append(tup)
        st.write(response)
        with st.spinner('Preparing a recommended question...'):
            time.sleep(2)
        growth_question = catalyst_ai_question_for_personal_growth(response)
        st.write("**Here's a good question you may want to ask now:** "+growth_question)
        single_prompt_submitted(st.session_state.human_prompt_example, response, growth_question)
    conversation = pd.DataFrame(l,columns=["Prompt","Response"])
    
    if len(conversation) > 0:
        
        conversation_csv = convert_df(conversation)

        st.write("**Download your question and response from GuidedAI...**")
        st.download_button(
            label="Download",
            data=conversation_csv,
            file_name='guided.csv',
            mime='text/csv',
            )

#uploading groups of prompts        
if choose=="Batch Learning":  
    st.header("Batch Learning")  
    col1, col2 = st.columns([1.5,1])
    with col1:
        st.subheader("Summarize or answer prompts in bulk")
        st.write("GuidedAI leverages the latest developments in artificial intelligence to comb through a list of prompts — math problems, book titles, a set of spiritual disciplines, etc — and provide summaries or answers for each one. This is a tool for rapidly downloading information to help you in your research and learning.\nIf you need help getting started, consider asking Guided's AI advisor for a list of resources or questions on a topic.")

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
            with st.spinner('GuidedAI is working through your problems...'):
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
    st.header("Submit Feedback")
    st.write("Share recommended resources, feature requests, or bug reports...")
    jotform = """<script type="text/javascript" src="https://form.jotform.com/jsform/230567840430049"></script>"""
    components.html(jotform, height=1500)

#email, text, and twitter share options
if choose=="Share":
    share_page_viewed()
    st.header("Share Guided")
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
