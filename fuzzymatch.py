# from fuzzywuzzy import process

# # List of skills to check
# input_skills = ["Python", "Java", "Javascript", "ReactJS"]

# # Predefined list of skills
# predefined_skills = ["Java", "JavaScript", "React.JS", "Python", "HTML"]

# # Define a function to get the best matches without false matches
# def get_matching_skills(input_skills, predefined_skills, threshold=95):
#     matching_skills = []
#     for skill in input_skills:
#         # Get the best match from the predefined skills
#         best_match, score = process.extractOne(skill, predefined_skills)
#         # Only add to the list if the similarity score is above the threshold
#         if score >= threshold:
#             matching_skills.append(best_match)
#     return list(set(matching_skills))  # Convert to set to ensure uniqueness, then back to list

# # Find the matching skills with a similarity threshold of 80%
# matching_skills = get_matching_skills(input_skills, predefined_skills, threshold=80)

# # Display the matching skills
# print(matching_skills)




import re
from fuzzywuzzy import fuzz

# Predefined list of skills (customizable)
predefined_skills = ["Java", "JavaScript", "React.JS", "Python", "HTML", "C++"]

# Define a function to extract skills from text using both exact and fuzzy matching
def extract_skills(text, threshold=80):
    # Convert text to lowercase for case-insensitive matching
    
    # If the text is a list, join it into a single string (e.g., if JD comes in the form of a list)
    if isinstance(text, list):
        text = ' '.join(text).lower()
    else:
        text = text.lower()  # If it's already a string, just convert to lowercase

    # Step 1: Extract exact keyword matches from the predefined skills list
    exact_skills = [skill for skill in predefined_skills if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text)]

    # Step 2: Use fuzzy matching to find approximate matches from the predefined skills list
    fuzzy_skills = []
    for skill in predefined_skills:
        # Use fuzzy matching on the entire text
        score = fuzz.partial_ratio(skill.lower(), text)  # Compare skill with the whole input text
        if score >= threshold:
            fuzzy_skills.append(skill)  # Add the matched predefined skill

    # Combine exact and fuzzy skills, and remove duplicates
    all_skills = list(set(exact_skills + fuzzy_skills))

    return all_skills

# Example usage
text_input = "I have experience with Python, Java, ExpressJS, ReactJS frameworks, and HTML development."
extracted_skills = extract_skills(text_input, threshold=80)

# Display the extracted skills
print(extracted_skills)
