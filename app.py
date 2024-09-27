import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re


# Loading environment variables from .env to Python-Environment
load_dotenv()

# Configuring the Grmini-Pro API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


predefined_skills = [
    # Programming Languages
    "Python", "Java", "JavaScript", "C++", "CPP", "C", "C#", "Ruby", "Go", "Swift", "Kotlin", "PHP", "TypeScript", "R", 
    "Shell Scripting", "Scala", "Perl", "Rust", "Dart", "Elixir", "Haskell", "Lua", "Objective-C", "MATLAB", 
    "VHDL", "Verilog", "Solidity",   
    # Web Development Frameworks and Tools
    "HTML", "CSS", "Tailwind", "Bootstrap", "SASS", "LESS", "React", "Angular", "Vue.js", "Node.js", "Express.js",
    "Django", "Flask", "ASP.NET", "Ruby on Rails", "Next.js", "Gatsby", "Nuxt.js", "jQuery", "Svelte", "WebAssembly",
    # Mobile Development Frameworks
    "Flutter", "React Native", "SwiftUI", "Xamarin", "Ionic", "Cordova", "Kotlin Multiplatform", "NativeScript",
    # Cloud Platforms and Services
    "AWS", "Azure", "Google Cloud Platform (GCP)", "IBM Cloud", "Oracle Cloud", "Heroku", "DigitalOcean", 
    "CloudFormation", "Lambda", "API Gateway", "EC2", "S3", "Route 53", "Azure DevOps", "GCP BigQuery", "Kubernetes",
    # DevOps & CI/CD Tools
    "Docker", "Kubernetes", "Jenkins", "Terraform", "Ansible", "Chef", "Puppet", "Vagrant", "CircleCI", "TravisCI",
    "GitLab CI", "Bitbucket Pipelines", "SonarQube", "Artifactory", "Nagios", "Prometheus", "Grafana", "ELK Stack (Elasticsearch, Logstash, Kibana)", 
    "New Relic", "Splunk", "PagerDuty", "Istio", "OpenShift", "ArgoCD", "Nomad",
    # Version Control & Collaboration Tools
    "Git", "GitHub", "GitLab", "Bitbucket", "Perforce", "Subversion (SVN)", "Mercurial",
    # Databases
    "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Oracle", "SQL Server", "MariaDB", "Cassandra", "Redis", "DynamoDB",
    "CouchDB", "Memcached", "Firestore", "Couchbase", "Neo4j", "Elasticsearch", "ClickHouse", "InfluxDB", "TimescaleDB", 
    "CockroachDB", "HBase", "Hive", "PrestoDB",
    # Machine Learning & Data Science Libraries/Tools
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "Scikit-learn", "TensorFlow", "Keras", "PyTorch", "OpenCV", "XGBoost", 
    "LightGBM", "CatBoost", "NLTK", "SpaCy", "Hugging Face Transformers", "SciPy", "Statsmodels", "Dask", "PySpark", 
    "Airflow", "Hadoop", "Kafka", "MLflow", "Kubeflow", "Tidyverse", "Jupyter Notebooks", 
    # Natural Language Processing (NLP) and AI Tools
    "Speech Recognition", "TextBlob", "BERT", "GPT", "Transformer Networks", "Word2Vec", "FastText", "GloVe", 
    "OpenAI API", "DeepSpeech", "CoreNLP", "AllenNLP", "Fairseq", "Dialogflow", "Rasa",
    # Software Testing & QA
    "Selenium", "JUnit", "pytest", "TestNG", "Cucumber", "Mocha", "Chai", "Jest", "Postman", "SoapUI", "LoadRunner", 
    "JMeter", "Appium", "Robot Framework", "Cypress", "Protractor", "SpecFlow", "QTest", "TestComplete", "Zephyr",
    # System Administration & Infrastructure
    "Linux", "Bash", "PowerShell", "Windows Server", "Unix", "VMware", "Hyper-V", "OpenStack", "Zabbix", "Nagios", 
    "pfSense", "HAProxy", "Nginx", "Apache HTTP Server", "Tomcat", "IIS", "FreeBSD", "OpenBSD", "AWS Lambda", 
    # Networking & Security
    "TCP/IP", "DNS", "DHCP", "HTTP", "HTTPS", "Load Balancing", "VPN", "SSH", "SSL/TLS", "Firewalls", "Routing Protocols", 
    "OSI Model", "Wireshark", "Nmap", "Snort", "Penetration Testing", "OWASP", "Burp Suite", "Metasploit", 
    "Kali Linux", "Suricata", "SOC", "SIEM", "IDS/IPS", "Endpoint Security", "Zero Trust", "OAuth", "SAML", "IAM", "PKI", 
    "SSL Certificates", "WAF", "Cloud Security", "Encryption", "AES", "RSA", "Two-Factor Authentication", 
    # Big Data & Data Engineering Tools
    "Hadoop", "Spark", "Flink", "Kafka", "Storm", "Hive", "Pig", "Presto", "Airflow", "NiFi", "HDFS", "Cloudera", 
    "Databricks", "EMR", "MapReduce", "Delta Lake", "Snowflake", "Redshift", "BigQuery", "Azure Data Lake",
    # Business Intelligence & Data Visualization Tools
    "Tableau", "Power BI", "Looker", "Qlik", "Google Data Studio", "D3.js", "Plotly", "ggplot2", "Metabase", "Grafana",
    # Software Design & Architecture
    "Microservices", "RESTful API", "GraphQL", "gRPC", "Service-Oriented Architecture (SOA)", "Event-Driven Architecture",
    "CQRS", "Domain-Driven Design (DDD)", "Test-Driven Development (TDD)", "Behavior-Driven Development (BDD)",
    "Clean Architecture", "Serverless Architecture", "Event Sourcing", "Pub/Sub Architecture", 
    # Miscellaneous Tools & Technologies
    "VS Code", "IntelliJ IDEA", "Eclipse", "PyCharm", "Xcode", "NetBeans", "Android Studio", "Atom", "Sublime Text",
    "Maven", "Gradle", "npm", "Yarn", "Webpack", "Parcel", "Babel", "ESLint", "Prettier", "SonarLint", "Figma", 
    "Adobe XD", "Sketch", "InVision", "Zeplin", "Lucidchart", "Microsoft Visio", "PlantUML", "Draw.io", 
    # Soft Skills
    "Collaboration", "Communication", "Teamwork", "Problem Solving", "Time Management", "Leadership", 
    "Creativity", "Critical Thinking", "Adaptability", "Emotional Intelligence", "Public Speaking", "Negotiation",
    "Conflict Resolution", "Empathy", "Decision Making", "Strategic Thinking", "Interpersonal Skills", 
    "Organizational Skills", "Customer Service", "Networking",
    # Emerging Technologies
    "Blockchain", "NFTs", "Smart Contracts", "IoT", "AR/VR", "Metaverse", "Quantum Computing", "5G", "Edge Computing", 
    "3D Printing", "Wearable Technology", "Autonomous Systems", "Robotic Process Automation (RPA)", "Biotechnology", 
    "Synthetic Biology", "Nanotechnology", "Cognitive Computing", "Augmented Reality", "Virtual Reality",
    # Additional Skills
    "SQL", "Git", "Linux", "AWS", "Docker", "Kubernetes", "MySQL Workbench", "OpenShift", "CyberSecurity", 
    "Tkinter", "SMTP", "Object-Oriented Programming (OOP)", "Data Structures and Algorithms", "Cloudinary", 
    "Slack", "React.js", "Azure", "GitHub", "Selenium", "TensorFlow"
]

# Pre-Defining the standard Certification Courses
standard_certifications = [
    "AWS Certified Solutions Architect – Associate",
    "Certified Kubernetes Administrator (CKA)",
    "Google Professional Cloud Architect",
    "Microsoft Certified: Azure Solutions Architect Expert",
    "Certified Information Systems Security Professional (CISSP)",
    "AWS Certified Developer – Associate",
    "Certified Ethical Hacker (CEH)",
    "Cisco Certified Network Associate (CCNA)",
    "CompTIA Security+",
    "Microsoft Certified: Azure Fundamentals",
    "Google Professional Data Engineer",
    "AWS Certified Cloud Practitioner",
    "Certified ScrumMaster (CSM)",
    "AWS Certified DevOps Engineer – Professional",
    "Microsoft Certified: Azure DevOps Engineer Expert",
    "CompTIA Network+",
    "Certified Information Security Manager (CISM)",
    "Cisco Certified Network Professional (CCNP)",
    "Google Associate Cloud Engineer",
    "PMP: Project Management Professional",
    "Certified Software Development Professional (CSDP)",
    "Microsoft Certified: Azure Administrator Associate",
    "Oracle Certified Java Programmer",
    "VMware Certified Professional (VCP)",
    "AWS Certified Security – Specialty",
    "Certified Cloud Security Professional (CCSP)",
    "Microsoft Certified: Power Platform Fundamentals",
    "Red Hat Certified Engineer (RHCE)",
    "TOGAF 9 Certification",
    "AWS Certified Big Data – Specialty",
    "ITIL 4 Foundation Certification",
    "Microsoft Certified: Power BI Data Analyst Associate",
    "Certified Information Systems Auditor (CISA)",
    "Google Professional Cloud Developer",
    "Salesforce Certified Platform Developer I",
    "Certified in Risk and Information Systems Control (CRISC)",
    "Microsoft Certified: Dynamics 365 Fundamentals",
    "Adobe Certified Expert (ACE)",
    "Cloudera Certified Data Analyst",
    "Certified Data Privacy Solutions Engineer (CDPSE)",
    "HashiCorp Certified: Terraform Associate",
    "Certified Agile Leadership (CAL)",
    "Google Professional Machine Learning Engineer",
    "AWS Certified Machine Learning – Specialty",
    "Scrum.org Professional Scrum Master (PSM I)",
    "Microsoft Certified: Security, Compliance, and Identity Fundamentals",
    "Cisco Certified DevNet Professional",
    "Oracle Database SQL Certified Associate",
    "Certified Blockchain Developer",
    "Certified JavaScript Developer (CIW)"
]


def extract_skills(text):
    # Convert text to lowercase for case-insensitive matching

    # If text is a list, converting it to a single string (Like if JD comes in the form of String)
    if isinstance(text, list):
        text = ' '.join(text).lower()  # Join the list into a single string and convert to lowercase
    else:
        text = text.lower()  # If text is a string, converting it to lowercase
    
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

    # Putting non-matching skills into missing_skills list
    for job_skill in job_description_skills:
        if not any(resume_skill.lower() in job_skill.lower() for resume_skill in resume_skills):
            missing_skills.append(job_skill)

    # Remove duplicates
    missing_skills = list(set(missing_skills))

    return matching_skills, missing_skills


def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error with API call: {e}")
        return None


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text


# Resume Parser
st.title("Resume Parser")
st.text("Determine your Resume Score")

Primary_Skills = st.text_area("Enter the Primary Skills")
Secondary_Skills = st.text_area("Enter the Secondary Skills")
Other_Skills = st.text_area("Enter the Other Skills")


uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None and Primary_Skills and Secondary_Skills and Other_Skills:
        res = input_pdf_text(uploaded_file)
        
        skills_etraction = f""" From the following resume text, extract all skills mentioned under any 
                                section labeled 'Technical Skills,' 'Skills,' or similar. If the resume 
                                contains skills mentioned in other sections, extract them as well. Return 
                                only the skills as a comma-separated list, with no additional information or 
                                formatting. Ensure the output is in a single line and consistent across 
                                multiple runs. **Resume**: {res} """

        text = get_gemini_response(skills_etraction)
        # Display the extracted text for debugging
        # st.text_area("Extracted Resume Text", text, height=300, disabled=True)
        st.markdown("###### Etracted Resume")


        st.code(text, language='text')
        
        # Extract skills from resume and job description
        resume_skills = extract_skills(text)
        jd_Primary_Skills = extract_skills(Primary_Skills)
        jd_Secondary_Skills = extract_skills(Secondary_Skills)
        jd_Other_Skills = extract_skills(Other_Skills)
        
        # Match skills
        Pri_matching_skills, Pri_missing_skills = match_skills(resume_skills, jd_Primary_Skills)
        Sec_matching_skills, Sec_missing_skills = match_skills(resume_skills, jd_Secondary_Skills)
        Oth_matching_skills, Oth_missing_skills = match_skills(resume_skills, jd_Other_Skills)
        
        # Percentage Primary, Secondary and Other Skill match
        per_primary_skill_match = round((len(Pri_matching_skills)/(len(Pri_matching_skills) + len(Pri_missing_skills)))*100, 2)
        per_secondary_skill_match = round((len(Sec_matching_skills)/(len(Sec_matching_skills) + len(Sec_missing_skills)))*100, 2)
        per_other_skill_match = round((len(Oth_matching_skills)/(len(Oth_matching_skills) + len(Oth_missing_skills)))*100, 2)


        input_prompt = f"""
        As an advanced Application Tracking System (ATS) with expertise in the tech field, analyze the following resume and provide a response in a single string with the following structure:

        {{
            "all_skills": [], 
            "work_skills": [], 
            "project_skills": [], 
            "total_publications": 0, 
            "copyrights": 0, 
            "patents": 0, 
            "certifications": [], 
            "hackathon_participation": 0
        }}

        1. **all_skills**: A list of all skills mentioned in the resume.
        2. **work_skills**: A list of skills specifically mentioned or inferred from the work experience section of the resume.
        3. **project_skills**: A list of skills used or learned from the project section of the resume.
        4. **total_publications**: The total count of publications mentioned in the resume.
        5. **copyrights**: The total count of copyrights mentioned in the resume.
        6. **patents**: The total count of patents mentioned in the resume.
        7. **certifications**: A list of certifications mentioned in the resume.
        8. **hackathon_participation**: A Flag value indicating if hackathon participation is mentioned (If yes, return 1, else return 0).

        **Resume**: {text}
        """

        # Extracting the prompt Response and Multiple Resume Details
        gem_response = get_gemini_response(input_prompt)

        if gem_response:
                    try:
                        # Try to parse the response as JSON
                        gem_response_data = json.loads(gem_response)

                        # Store the Workeperience, Project, Publications, Patent, Copyright, Certifications and Hackathons
                        # in the form of List's
                        work_skills = gem_response_data["work_skills"]
                        project_skills = gem_response_data["project_skills"]
                        total_publications = gem_response_data["total_publications"]
                        copyrights = gem_response_data["copyrights"]
                        patents = gem_response_data["patents"]
                        certifications = gem_response_data["certifications"]
                        hackathon_participation = gem_response_data["hackathon_participation"]


                        # Refining Skills once again with the predefined skills
                        ref_work_skills = extract_skills(' '.join(work_skills))  # Convert list to string
                        ref_project_skills = extract_skills(' '.join(project_skills))  # Convert list to string

                                                
                        # Matching the work and project skills with primary and secondary skills
                        Pri_work_matching_skills, Pri_work_missing_skills = match_skills(ref_work_skills, jd_Primary_Skills)
                        Sec_work_matching_skills, Sec_work_missing_skills = match_skills(ref_work_skills, jd_Secondary_Skills)
                        
                        Pri_project_matching_skills, Pri_project_missing_skills = match_skills(ref_project_skills, jd_Primary_Skills)
                        Sec_project_matching_skills, Sec_project_missing_skills = match_skills(ref_project_skills, jd_Secondary_Skills)


                        # Percentage match of the primary and secondary skills of  work and project respectively.
                        per_pri_work_matching_skills = round(((len(Pri_work_matching_skills))/(len(jd_Primary_Skills))) * 100, 2)
                        per_sec_work_matching_skills = round(((len(Sec_work_matching_skills))/(len(jd_Secondary_Skills))) * 100, 2)

                        per_pri_project_matching_skills = round(((len(Pri_project_matching_skills))/(len(jd_Primary_Skills))) * 100, 2)
                        per_sec_project_matching_skills = round(((len(Sec_project_matching_skills))/(len(jd_Secondary_Skills))) * 100, 2)

                        # Sum of Publications, Copyrights and Patents and the final percentage score calculation
                        filing_total = total_publications + copyrights + patents
                        per_filing_score = 0
                        if filing_total >= 1:
                            per_filing_score = 5
                        else:
                            per_filing_score = 0

                        # Certifications Score Calculation
                        matching_certifications = set(certifications).intersection(standard_certifications)
                        count_matching_std_certifications = len(matching_certifications)
                        
                        per_certi_Score = 0
                        if count_matching_std_certifications >= 1:
                            per_certi_Score = 5
                        else:
                            per_certi_Score = 3

                     
                        # Hackathon Score Calculation
                        per_hackathon_score = 0
                        if hackathon_participation == 1:
                            per_hackathon_score = 4
                        else:
                            per_hackathon_score = 0

                        # Final Rubrick Formula
                        Final_score = (0.4 * per_primary_skill_match) + (0.2 * per_secondary_skill_match) + (0.1 * per_other_skill_match) + (0.056 * per_pri_work_matching_skills) + (0.024 * per_sec_work_matching_skills) + (0.056 * per_pri_project_matching_skills) + (0.024 * per_sec_project_matching_skills) + (per_filing_score) + (per_certi_Score) + (per_hackathon_score) 

                        # Constructing the response JSON manually
                        response_data = {
                             
                            "Primary Matching Skills": Pri_matching_skills,
                            "Primary Missing Skills": Pri_missing_skills,
                            "Number of Matching Primary Skills": len(Pri_matching_skills),
                            "Number of Missing Primary Skills": len(Pri_missing_skills),
                            "Total Required Primary Skills": len(Pri_matching_skills) + len(Pri_missing_skills),
                            "Percentage Primary Skill Match": per_primary_skill_match,

                            "Secondary Matching Skills": Sec_matching_skills,
                            "Secondary Missing Skills": Sec_missing_skills,
                            "Number of Matching Secondary Skills": len(Sec_matching_skills),
                            "Number of Missing Secondary Skills": len(Sec_missing_skills),
                            "Total Required Secondary Skills": len(Sec_matching_skills) + len(Sec_missing_skills),
                            "Percentage Secondary Skill Match": per_secondary_skill_match,

                            "Other Matching Skills": Oth_matching_skills,
                            "Other Missing Skills": Oth_missing_skills,
                            "Number of Matching Other Skills": len(Oth_matching_skills),
                            "Number of Missing Other Skills": len(Oth_missing_skills),
                            "Total Required Other Skills": len(Oth_matching_skills) + len(Oth_missing_skills),
                            "Percentage Other Skill Match": per_other_skill_match,

                            "Work Skills": work_skills,
                            "Project Skills": project_skills,
                            "Total Publications": total_publications,
                            "Copyrights": copyrights,
                            "Patents": patents,
                            "Certifications": certifications,
                            "Hackathon Participation": hackathon_participation, 

                            "Primary Skills From Work-Eperience": Pri_work_matching_skills,
                            "Secondary Skills From Work-Eperience": Sec_work_matching_skills,
                            "Number of Pri_Work_Skills": len(Pri_work_matching_skills),
                            "Number of Sec_Work_Skills": len(Sec_work_matching_skills),
                            "Percentage Pri_work_Skill_Match": per_pri_work_matching_skills,
                            "Percentage Sec_work_Skill_Match": per_sec_work_matching_skills,

                            "Primary Skills From Projects": Pri_project_matching_skills,
                            "Secondary Skills From Projects": Sec_project_matching_skills,
                            "Number of Pri_Projects_Skills": len(Pri_project_matching_skills),
                            "Number of Sec_Projects_Skills": len(Sec_project_matching_skills),
                            "Percentage Pri_Projects_Skill_Match": per_pri_project_matching_skills,
                            "Jd_Sec_Skills": jd_Secondary_Skills,
                            "Percentage Sec_Projects_Skill_Match": per_sec_project_matching_skills,

                            "Total Filings": filing_total,

                            "Final Resume Score": Final_score
                        }

                        # Displaying  the updated response
                        st.text_area("Analysis Result", json.dumps(response_data, indent=4), height=300)

                        st.markdown("###### Final Score")
                        st.code(Final_score, language='text')
                        

                    except json.JSONDecodeError as e:
                        st.error(f"Failed to parse JSON response: {e}")
                        st.text_area("Gemini API Response", gem_response, height=300)
        else:
            st.warning("Gemini API call failed or returned an empty response.")

    else:
        st.warning("Please upload a resume and enter a job description.")