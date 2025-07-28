import streamlit as st
from pdf_utils import prepare_pdf_content
from api_client import get_gemini_response
from prompts import RESUME_ANALYSIS_PROMPT, PERCENTAGE_MATCH_PROMPT
from PIL import Image


GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# Page configuration
## for windowes st.set_page_config(page_title="ATS Resume Expert", page_icon=Image.open("..\\assets\\icon.png"), layout="wide")
## to lunix and stramlit cloud deploy 
st.set_page_config(page_title="ATS Resume Expert", page_icon=Image.open("../assets/icon.png"), layout="wide")

# st.markdown(...): Allows raw HTML/CSS to be rendered in the app.
# button[kind="primary"]: Targets Streamlit’s primary buttons (used for “Analyze Resume”).
# background-color: #2E7D32: Sets a forest green background.
# border-radius: 8px: Rounds button corners for a modern look.
# padding: 10px 20px: Adds internal spacing for better button size.
# button[kind="primary"]:hover: Changes the background to a darker green (#1B5E20) on hover for visual feedback.
# div.st-emotion-cache-1r4qj8v: Targets Streamlit containers (e.g., for the response section).
# border: 1px solid #E0E0E0: Adds a light gray border.
# border-radius: 8px: Rounds container corners.
# padding: 15px: Adds internal spacing for content.
# unsafe_allow_html=True: Enables rendering of raw HTML/CSS, as Streamlit sanitizes HTML by default.
st.markdown(
    """
    <style>
    /* Style primary buttons */
    button[kind="primary"] {
        background-color: #2E7D32;
        border-radius: 8px;
        padding: 10px 20px;
    }
    button[kind="primary"]:hover {
        background-color: #1B5E20;
    }
    /* Add border to containers */
    div.st-emotion-cache-1r4qj8v {
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header with logo
st.image("..\\assets\\resume_logo.png", caption="ATS Resume Expert Logo", width=100)
st.header("ATS Resume Expert", anchor=False)

# Initialize session state
if "response" not in st.session_state:
    st.session_state.response = None

# Layout with columns
col1, col2 = st.columns([2, 1])
with col1:
    job_description = st.text_area(
        "Job Description",
        height=200,
        placeholder="Paste the job description here...",
        key="job_description"
    )
with col2:
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        help="Upload a PDF file of your resume"
    )
    if uploaded_file:
        st.success("PDF uploaded successfully!")

# Form for submissions
with st.form(key="resume_form"):
    submit_resume_analysis = st.form_submit_button(
        "Analyze Resume",
        type="primary",
        help="Get a detailed analysis of the resume against the job description"
    )
    submit_percentage_match = st.form_submit_button(
        "Percentage Match",
        type="secondary",
        help="Calculate how well the resume matches the job description"
    )

# Handle submissions
if submit_resume_analysis or submit_percentage_match:
    if not uploaded_file or not job_description:
        st.error("Please upload a resume and provide a job description")
    else:
        with st.spinner("Processing your resume..."):
            try:
                pdf_content = prepare_pdf_content(uploaded_file)
                prompt = (
                    RESUME_ANALYSIS_PROMPT if submit_resume_analysis
                    else PERCENTAGE_MATCH_PROMPT
                )
                st.session_state.response = get_gemini_response(job_description, pdf_content, prompt)
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Display response
if st.session_state.response:
    # st.container: Creates a container with borders and padding (styled via CSS above).
    # Context: Organizes the output visually, improving readability.
    with st.container():
        st.subheader("Analysis Result", anchor=False)
        with st.expander("View Details", expanded=True):
            st.markdown(st.session_state.response)
