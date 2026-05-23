import streamlit as st
import base64
import os

from services.persistence.exercise_repository import (
    get_or_create_user
)

from services.ui.style_loader import (
    load_css
)


# ---------------------------------
# BACKGROUND ONLY
# ---------------------------------

def add_bg():

    current_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    project_root = os.path.dirname(
        os.path.dirname(current_dir)
    )

    image_path = os.path.join(
        project_root,
        "assets",
        "gym_bg.jpg"
    )

    with open(
        image_path,
        "rb"
    ) as img:

        encoded=base64.b64encode(
            img.read()
        ).decode()


    st.markdown(
f"""

<style>

.stApp{{

background:

linear-gradient(
rgba(0,0,0,.82),
rgba(0,0,0,.90)
),

url(
data:image/jpg;base64,{encoded}
);

background-size:cover;

background-position:center;

background-repeat:no-repeat;

background-attachment:fixed;

}}

</style>

""",

unsafe_allow_html=True
)



# ---------------------------------
# LOGIN PAGE
# ---------------------------------

def render_login_wall():

    if st.session_state.get(
        "user_id"
    ):
        return True


    # GLOBAL STYLE

    load_css()

    # PAGE BG

    add_bg()


    # HEADER

    st.markdown("""

    <div class='title'>

    🏋️ RepSense AI

    </div>

    """,

    unsafe_allow_html=True)



    st.markdown("""

    <div class='subtitle'>

    Your Real-Time AI Gym Coach

    </div>

    """,

    unsafe_allow_html=True)



    st.markdown("""

    <div class='small'>

    Track reps • Correct posture • Train smarter

    </div>

    """,

    unsafe_allow_html=True)




    # FEATURES

    c1,c2,c3=st.columns(
        3,
        gap="medium"
    )


    features=[

    (

    "⚡",

    "Live Tracking",

    "Real-time movement detection"

    ),

    (

    "🎯",

    "Form Correction",

    "AI posture analysis"

    ),

    (

    "🤖",

    "AI Coach",

    "Smart voice feedback"

    )

    ]



    for col,data in zip(
        [c1,c2,c3],
        features
    ):

        icon,title,desc=data


        with col:

            st.markdown(
f"""

<div class='feature-card'>

<h1>{icon}</h1>

<h2>{title}</h2>

<p>{desc}</p>

</div>

""",

unsafe_allow_html=True
)



    st.write("")



    # LOGIN

    left,mid,right=st.columns(
        [1,2,1]
    )


    with mid:


        st.markdown("""

        <div class='login-title'>

        👋 Start Your Fitness Session

        </div>

        """,

        unsafe_allow_html=True)



        st.markdown("""

        <div class='login-sub'>

        Enter your unique username

        </div>

        """,

        unsafe_allow_html=True)



        with st.container(
            border=True
        ):

            with st.form(
                "login_form"
            ):

                username=(
                st.text_input(
                    "Username",
                    placeholder=
                    "Enter unique username"
                )
                )


                submitted=(
                st.form_submit_button(
                    "💪 Enter Gym Mode",
                    use_container_width=True
                )
                )




    # LOGIN LOGIC

    if submitted:


        username=username.strip()


        if not username:

            st.toast(
            "Please enter username"
            )

            return False



        with st.spinner(
        "Initializing AI Coach..."
        ):

            user=(
            get_or_create_user(
            username
            )
            )


        st.session_state[
        "user_id"
        ]=user["id"]


        st.session_state[
        "username"
        ]=user["username"]


        st.success(
        f"Welcome {username} 💪"
        )


        st.rerun()



    st.markdown("""

    <div class='footer'>

    Powered by
    MediaPipe + OpenCV + AI

    <br><br>

    ❤️ Train smarter.
    Lift safer.
    Become stronger.

    </div>

    """,

    unsafe_allow_html=True)


    return False