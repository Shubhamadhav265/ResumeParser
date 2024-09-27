import spacy
import re

# Load a pre-trained NLP model
nlp = spacy.load("en_core_web_sm")

def extract_skills(resume_text):
    # Define a list of known skills, including multi-word skills
    known_skills = [
        "Python", "Java", "Machine Learning", "Data Analysis", 
        "JavaScript", "SQL", "HTML", "CSS", "Deep Learning", 
        "Natural Language Processing", "Cloud Computing"
    ]

    # Process the resume text
    doc = nlp(resume_text)

    # Extract skills
    extracted_skills = []
    
    # Check for multi-word skills
    for skill in known_skills:
        # Use regex to match whole phrases in the resume text
        if re.search(r'\b' + re.escape(skill) + r'\b', resume_text):
            extracted_skills.append(skill)

    # Remove duplicates
    return list(set(extracted_skills))

# Example usage
resume = "I have experience with Python, Java, and Machine Learning."
skills = extract_skills(resume)
print(skills)  # Output: ['Python', 'Machine Learning', 'Java']
