import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re
import spacy

# Load environment variables
load_dotenv()

# Configure the API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Example predefined list of skills (expand this list based on domain)
predefined_skills = [
    "Python", "Java", "JavaScript", "C++", "CPP", "Machine Learning", "Data Analysis", "SQL", "Project Management", "Communication",
    "Ruby", "Go", "Swift", "Kotlin", "PHP", "TypeScript", "R", "Tailwind", "Openshift",
    "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Express.js",
    "Flutter", "React Native",
    "Object-Oriented Design", "Design Patterns", "System Architecture", "UML",
    "Git", "GitHub", "GitLab", "Bitbucket",
    "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "Oracle",
    "Unit Testing", "Integration Testing", "Test-Driven Development (TDD)", "Selenium", "JUnit", "pytest",
    "Docker", "Kubernetes", "CI/CD", "Jenkins", "Terraform", "Ansible",
    "AWS", "Azure", "Google Cloud Platform (GCP)",
    "Trees", "Graphs", "Hash Tables", "Sorting Algorithms", "Search Algorithms",
    "Encryption", "Authentication", "Authorization", "OWASP", "Penetration Testing",
    "Visual Studio Code", "IntelliJ IDEA", "Eclipse", "PyCharm", "Xcode",
    "Jira", "Trello", "Asana", "Basecamp",
    "Slack", "Microsoft Teams", "Zoom",
    "pgAdmin", "MySQL Workbench", "MongoDB Compass",
    "Maven", "Gradle", "npm",
    "Introduction to Computer Science", "Data Structures and Algorithms", "Software Engineering Principles", 
    "Operating Systems", "Database Systems", "Computer Networks", "Web Development", "Mobile App Development", 
    "Machine Learning and Data Science", "Cybersecurity", "Software Testing and Quality Assurance", 
    "Human-Computer Interaction", "Software Design and Architecture",
    "Discrete Mathematics", "Linear Algebra", "Calculus", "Probability and Statistics", "Algorithms and Complexity",
    "Computer Architecture", "Compiler Design", "Operating System Design", "Computer Graphics", "Artificial Intelligence",
    "Software Engineering Ethics", "Database Design", "Network Security", "Cloud Computing", "Big Data Technologies",
    # Java Libraries
    "Spring Framework", "Hibernate", "Apache Commons", "Guava", "Log4j", "Jackson", "JUnit", "Maven", "Gradle",
    # C++ Libraries
    "Boost", "STL (Standard Template Library)", "Eigen", "Qt", "Poco", "OpenCV", "Cereal", "TBB (Threading Building Blocks)",
    # Python Libraries
    "NumPy", "Pandas", "Matplotlib", "Scikit-learn", "TensorFlow", "Keras", "PyTorch", "Django", "Flask", "Requests", 
    "BeautifulSoup", "SQLAlchemy", "Celery", "OpenCV", "NLTK", "SciPy"
]

def extract_skills(text):
    # Convert text to lowercase for case-insensitive matching
    text = text.lower()
    
    # Extract exact keyword matches from the predefined skills list
    skills = [skill for skill in predefined_skills if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text)]

    # Remove duplicates by converting the list to a set and back to a list
    print(list(set(skills)))
    return list(set(skills))




def match_skills(resume_skills, job_description_skills):
    resume_skill_set = set(resume_skills)
    job_skill_set = set(job_description_skills)

    matching_skills = [skill for skill in job_skill_set if skill in resume_skill_set]
    missing_skills = [skill for skill in job_skill_set if skill not in matching_skills]

    # Handle partial matches or variations
    for job_skill in job_description_skills:
        if not any(resume_skill.lower() in job_skill.lower() for resume_skill in resume_skills):
            missing_skills.append(job_skill)

    # Remove duplicates
    missing_skills = list(set(missing_skills))

    return matching_skills, missing_skills

def get_gemini_response(prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

# Streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")

Primary_Skills = st.text_area("Enter the Primary Skills")
Secondary_Skills = st.text_area("Enter the Secondary Skills")
Other_Skills = st.text_area("Enter the Other Skills")


uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and Primary_Skills and Secondary_Skills and Other_Skills:
        text = input_pdf_text(uploaded_file)
        
        # Display the extracted text for debugging
        st.text_area("Extracted Resume Text", text, height=300)
        
        # Extract skills from resume and job description
        resume_skills = extract_skills(text)
        jd_Primary_Skills = extract_skills(Primary_Skills)
        jd_Secondary_Skills = extract_skills(Secondary_Skills)
        jd_Other_Skills = extract_skills(Other_Skills)
        
        # Match skills
        Pri_matching_skills, Pri_missing_skills = match_skills(resume_skills, jd_Primary_Skills)
        Sec_matching_skills, Sec_missing_skills = match_skills(resume_skills, jd_Secondary_Skills)
        Oth_matching_skills, Oth_missing_skills = match_skills(resume_skills, jd_Other_Skills)
        
        # Construct the response JSON manually
        response_data = {
            "Primary Matching Skills": Pri_matching_skills,
            "Primary Missing Skills": Pri_missing_skills,
            "Number of Matching Primary Skills": len(Pri_matching_skills),
            "Number of Missing Primary Skills": len(Pri_missing_skills),
            "Total Required Primary Skills": len(Pri_matching_skills) + len(Pri_missing_skills),
            "Percentage Primary Skill Match": round((len(Pri_matching_skills)/(len(Pri_matching_skills) + len(Pri_missing_skills)))*100, 2),

            "Secondary Matching Skills": Sec_matching_skills,
            "Secondary Missing Skills": Sec_missing_skills,
            "Number of Matching Secondary Skills": len(Sec_matching_skills),
            "Number of Missing Secondary Skills": len(Sec_missing_skills),
            "Total Required Secondary Skills": len(Sec_matching_skills) + len(Sec_missing_skills),
            "Percentage Secondary Skill Match": round((len(Sec_matching_skills)/(len(Sec_matching_skills) + len(Sec_missing_skills)))*100, 2),


            "Other Matching Skills": Oth_matching_skills,
            "Other Missing Skills": Oth_missing_skills,
            "Number of Matching Other Skills": len(Oth_matching_skills),
            "Number of Missing Other Skills": len(Oth_missing_skills),
            "Total Required Other Skills": len(Oth_matching_skills) + len(Oth_missing_skills),
            "Percentage Other Skill Match": round((len(Oth_matching_skills)/(len(Oth_matching_skills) + len(Oth_missing_skills)))*100, 2)

        }

        # Display the updated response
        st.text_area("Analysis Result", json.dumps(response_data, indent=4), height=300)

    else:
        st.warning("Please upload a resume and enter a job description.")