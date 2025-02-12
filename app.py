import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Helper Functions ---
def generate_resume_content(prompt):
    """
    Generates resume content using OpenAI.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or another suitable engine
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,  # Adjust for creativity vs. accuracy
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error generating resume content: {e}"


# --- Streamlit UI ---
def main():
    st.title("Smart Resume Generator")

    # --- User Input Sections ---

    st.header("Personal Information")
    name = st.text_input("Full Name:")
    email = st.text_input("Email Address:")
    phone = st.text_input("Phone Number:")
    linkedin = st.text_input("LinkedIn Profile URL:")
    github = st.text_input("GitHub Profile URL (Optional):")

    st.header("Summary/Objective")
    objective = st.text_area("Write a brief career objective or summary:")

    st.header("Skills")
    skills = st.text_area("List your skills (comma-separated):")

    st.header("Experience")
    experience_count = st.number_input("Number of work experiences to include:", min_value=0, max_value=5, value=2)  # Limit to 5 for UI simplicity

    experiences = []
    for i in range(experience_count):
        st.subheader(f"Experience #{i+1}")
        company = st.text_input(f"Company Name:", key=f"company_{i}")
        job_title = st.text_input(f"Job Title:", key=f"job_title_{i}")
        start_date = st.text_input(f"Start Date (e.g., Jan 2020):", key=f"start_date_{i}")
        end_date = st.text_input(f"End Date (e.g., Present, or Dec 2022):", key=f"end_date_{i}")
        responsibilities = st.text_area(f"Responsibilities and Achievements:", key=f"responsibilities_{i}")

        experiences.append({
            "company": company,
            "job_title": job_title,
            "start_date": start_date,
            "end_date": end_date,
            "responsibilities": responsibilities,
        })

    st.header("Education")
    education_count = st.number_input("Number of educational qualifications to include:", min_value=0, max_value=3, value=1)  # Limit to 3

    educations = []
    for i in range(education_count):
        st.subheader(f"Education #{i+1}")
        institution = st.text_input(f"Institution Name:", key=f"institution_{i}")
        degree = st.text_input(f"Degree:", key=f"degree_{i}")
        graduation_date = st.text_input(f"Graduation Date:", key=f"graduation_date_{i}")
        description = st.text_area(f"Description (e.g., Major, GPA, relevant coursework):", key=f"education_description_{i}")

        educations.append({
            "institution": institution,
            "degree": degree,
            "graduation_date": graduation_date,
            "description": description,
        })

    # --- Resume Generation ---
    if st.button("Generate Resume"):
        # Build the prompt for OpenAI
        prompt = f"""
        Generate a resume for:
        Name: {name}
        Email: {email}
        Phone: {phone}
        LinkedIn: {linkedin}
        GitHub: {github}

        Summary/Objective: {objective}

        Skills: {skills}

        Experience:
        """
        for exp in experiences:
            prompt += f"""
            Company: {exp['company']}
            Job Title: {exp['job_title']}
            Start Date: {exp['start_date']}
            End Date: {exp['end_date']}
            Responsibilities: {exp['responsibilities']}
            """

        prompt += """
        Education:
        """
        for edu in educations:
            prompt += f"""
            Institution: {edu['institution']}
            Degree: {edu['degree']}
            Graduation Date: {edu['graduation_date']}
            Description: {edu['description']}
            """

        prompt += "\n\nGenerate the resume in a clean, professional format." #give instructions for the style of resume
        resume_content = generate_resume_content(prompt)
        st.subheader("Generated Resume:")
        st.write(resume_content)

if __name__ == "__main__":
    main()