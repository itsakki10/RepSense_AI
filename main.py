import os
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from services.auth.login_wall import render_login_wall
from services.state.session_defaults import initial_session_defaults
from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import (
    load_css,
    inject_local_font,
    inject_webrtc_styles
)

from services.persistence.exercise_repository import (
    init_db,
    get_users_exercises
)

from streamlit_webrtc import (
    webrtc_streamer,
    WebRtcMode
)

from services.vision.exercise_video_processor import VideoProcessorClass
from services.tracking.metrics import sync_metrics_update

from groq import Groq
from services.coaching.llm import LLMCoach
from services.coaching.tts import TextToSpeech
from services.coaching.voice_pipeline import (
    VoicePipeline,
    autoplay_audio
)

load_dotenv()


def main():

    st.set_page_config(
        page_title="RepSense AI",
        page_icon="🏋️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    load_css(
        os.path.join(
            os.getcwd(),
            "static",
            "style.css"
        )
    )

    inject_local_font(
        os.path.join(
            os.getcwd(),
            "static",
            "AdobeClean.otf"
        ),
        "AdobeClean"
    )

    init_db()

    if not render_login_wall():
        return

    initial_session_defaults()

    workout_started = st.session_state.get(
        "workout_started",
        False
    )


    # ================= VOICE =================

    if "voice_pipeline" not in st.session_state:

        try:

            api_key = os.getenv(
                "GROQ_API_KEY"
            )

            if not api_key:
                raise Exception(
                    "GROQ_API_KEY missing"
                )

            groq_client = Groq(
                api_key=api_key
            )

            llm_coach = LLMCoach(
                groq_client
            )

            tts = TextToSpeech()

            st.session_state.voice_pipeline = (
                VoicePipeline(
                    llm_coach,
                    tts
                )
            )

        except Exception as e:

            st.error(
                f"Voice failed: {e}"
            )

            st.session_state.voice_pipeline = None



    # ================= SIDEBAR =================

    with st.sidebar:

        st.markdown(
        """
        <h1 style='text-align:center'>
        🏋️ RepSense AI
        </h1>
        """,
        unsafe_allow_html=True
        )

        st.caption(
        f"👤 {st.session_state.username}"
        )

        st.divider()

        st.subheader(
        "Workout Plan"
        )

        if not workout_started:

            exercise = st.selectbox(
                "Exercise",
                EXERCISE_OPTIONS
            )

            sets = st.number_input(
                "Sets",
                1,
                20,
                value=3
            )

            reps = st.number_input(
                "Reps per Set",
                1,
                50,
                value=10
            )

            if st.button(
                "🔥 Start Workout",
                use_container_width=True,
                key="start_workout_btn"
            ):

                st.session_state.exercise_type = exercise

                st.session_state.target_sets = int(
                    sets
                )

                st.session_state.reps_per_set = int(
                    reps
                )

                st.session_state.reps = 0

                st.session_state.workout_started = True


                if st.session_state.voice_pipeline:

                    result = (
                    st.session_state
                    .voice_pipeline
                    .process_event(
                        event="workout_started",
                        exercise=exercise,
                        metrics={}
                    )
                    )

                    if result:

                        (
                        st.session_state.audio_to_play,
                        st.session_state.coach_feedback
                        ) = result

                st.rerun()


        else:

            st.success(
            st.session_state.exercise_type
            )

            if st.button(
                "⛔ End Workout",
                use_container_width=True,
                key="end_workout_btn"
            ):

                st.session_state.workout_started = False
                st.rerun()



    # ================= DASHBOARD =================

    left,right = st.columns([2.5,1])

    with left:

        selected_exercise = (
            st.session_state.get(
                "exercise_type",
                "No workout selected"
            )
        )

        st.markdown(
        f"""

        <div class='dashboard-banner'>

        <h1>

        Welcome back,
        {st.session_state.username} 💪

        </h1>

        <p>

        RepSense AI systems initialized.
        Your AI coach is ready.

        </p>

        <br>

        <h3>
        🎯 Current Workout
        </h3>

        <p>
        {selected_exercise}
        </p>

        <br>

        <h3>
        🧠 Active Capabilities
        </h3>

        <p>

        • Real-time rep counting<br>
        • Live posture analysis<br>
        • AI voice coaching<br>
        • Form correction system<br>
        • Workout analytics

        </p>

        </div>

        """,

        unsafe_allow_html=True
        )


    with right:

        voice_status = (
            "ONLINE"
            if st.session_state.get(
                "voice_pipeline"
            )
            else
            "OFFLINE"
        )


        st.markdown(
        f"""

        <div class='ai-status'>

        <h1>🤖</h1>

        <h3>
        RepSense Core
        </h3>

        <hr>

        <p>
        Voice: {voice_status}
        </p>

        <p>
        Vision: READY
        </p>

        <p>
        Tracking: ACTIVE
        </p>

        <p>
        Camera: STANDBY
        </p>

        </div>

        """,

        unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)



    c1,c2,c3=st.columns(3)


    with c1:

        st.markdown("""

        <div class='feature-card'>

        <div class='feature-icon'>
        📷
        </div>

        <h2>
        Vision Engine
        </h2>

        <p>
        MediaPipe pose estimation with live tracking
        </p>

        </div>

        """, unsafe_allow_html=True)


    with c2:

        st.markdown("""

        <div class='feature-card'>

        <div class='feature-icon'>
        🎤
        </div>

        <h2>
        Voice Coach
        </h2>

        <p>
        AI-generated coaching and corrections
        </p>

        </div>

        """, unsafe_allow_html=True)


    with c3:

        st.markdown("""

        <div class='feature-card'>

        <div class='feature-icon'>
        🏋️
        </div>

        <h2>
        Supported Exercises
        </h2>

        <p>
        Squats • Pushups • Lunges • Curls
        </p>

        </div>

        """, unsafe_allow_html=True)



    if st.session_state.get(
        "audio_to_play"
    ):

        autoplay_audio(
            st.session_state.audio_to_play
        )


    if st.session_state.get(
        "coach_feedback"
    ):

        st.markdown(
        f"""

        <div class='coach-box'>

        🤖
        {st.session_state.coach_feedback}

        </div>

        """,

        unsafe_allow_html=True
        )



    # ================= CAMERA =================

    if not workout_started:

        st.markdown("""

        <div class='start-card'>

        <h1>
        Ready To Train?
        </h1>

        <p>
        Configure workout from sidebar and begin
        </p>

        </div>

        """,

        unsafe_allow_html=True
        )

    else:

        st.markdown(
        "## 🎥 Live Workout Session"
        )

        context = webrtc_streamer(

            key="exercise-analysis",

            mode=WebRtcMode.SENDRECV,

            video_processor_factory=
            VideoProcessorClass,

            rtc_configuration={
                "iceServers":[
                    {
                        "urls":[
                        "stun:stun.l.google.com:19302"
                        ]
                    }
                ]
            },

            media_stream_constraints={
                "video":True,
                "audio":False
            },

            async_processing=True
        )


        sync_metrics_update(
            context
        )


        if context.state.playing:

            time.sleep(.25)

            st.rerun()


        inject_webrtc_styles()



    st.divider()

    st.markdown(
    "## 📈 Workout History"
    )

    user_id = st.session_state.get(
        "user_id",
        0
    )

    history_rows = get_users_exercises(
        user_id
    )

    arr = [

        {

        "Exercise":
        row["exercise_name"],

        "Reps":
        row["reps"],

        "Sets":
        row["sets"],

        "Time (sec)":
        row["time"],

        "Date":
        row["created_at"]

        }

        for row in history_rows
    ]


    df = pd.DataFrame(arr)


    if not df.empty:

        df["Date"] = pd.to_datetime(
            df["Date"]
        ).dt.date

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info(
        "No workout history found."
        )


if __name__=="__main__":
    main()