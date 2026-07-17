import re
import pdfplumber
from datetime import datetime

# ----------------------------------
# Skills Database
# ----------------------------------

SKILLS = [

    # Programming Languages
    "python","java","c","c++","c#","r","go","php","ruby","swift","kotlin","scala","perl","matlab",

    # Web Technologies
    "html","css","javascript","typescript","bootstrap","tailwind css",
    "jquery","ajax","xml","json",

    # Frontend Frameworks
    "react","angular","vue","nextjs","nuxtjs",

    # Backend Frameworks
    "nodejs","express","django","flask","fastapi","spring","spring boot",
    "laravel","asp.net",

    # Mobile Development
    "android","flutter","react native","ionic",

    # Databases
    "sql","mysql","postgresql","mongodb","sqlite","oracle","redis","firebase",

    # Data Science
    "numpy","pandas","matplotlib","seaborn","plotly","scipy",

    # Machine Learning
    "machine learning","deep learning","artificial intelligence",
    "nlp","computer vision","reinforcement learning",
    "scikit-learn","tensorflow","keras","pytorch",
    "xgboost","lightgbm","catboost","opencv","hugging face",

    # Data Engineering
    "apache spark","hadoop","kafka","airflow","etl",

    # Cloud
    "aws","azure","google cloud","gcp","ec2","lambda","s3",

    # DevOps
    "docker","kubernetes","jenkins","github","gitlab",
    "ci/cd","linux","bash","shell scripting",

    # BI Tools
    "power bi","tableau","excel","google sheets",

    # Testing
    "selenium","pytest","junit","postman",

    # APIs
    "rest api","graphql","soap",

    # Networking
    "tcp/ip","dns","http","https",

    # Cyber Security
    "penetration testing","ethical hacking","wireshark",
    "metasploit","burp suite","nmap",

    # Software Engineering
    "data structures","algorithms","oops","operating system",
    "computer networks","dbms","system design",

    # Version Control
    "git","github","bitbucket",

    # IDEs & Tools
    "visual studio code","pycharm","eclipse","intellij",
    "jupyter notebook","anaconda",

    # Soft Skills
    "communication","leadership","teamwork",
    "problem solving","critical thinking","time management"

]

EDUCATION = {

    "b.tech": "B.Tech",
    "btech": "B.Tech",
    "bachelor of technology": "B.Tech",

    "b.e": "B.E",
    "be": "B.E",
    "bachelor of engineering": "B.E",

    "m.tech": "M.Tech",
    "mtech": "M.Tech",
    "master of technology": "M.Tech",

    "bca": "BCA",
    "bachelor of computer applications": "BCA",

    "mca": "MCA",
    "master of computer applications": "MCA",

    "bsc": "B.Sc",
    "bachelor of science": "B.Sc",

    "msc": "M.Sc",
    "master of science": "M.Sc",

    "mba": "MBA",
    "master of business administration": "MBA",

    "phd": "PhD",
    "doctor of philosophy": "PhD"

}


# ----------------------------------
# Read JD PDF
# ----------------------------------

def extract_text(pdf_path):

    text = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text

# ----------------------------------
# Job Title
# ----------------------------------

def extract_job_title(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if line.lower().startswith("job title"):

            return line.split(":",1)[1].strip()

    return "Not Found"

# ----------------------------------
# Skills
# ----------------------------------

def extract_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text):

            found.append(skill.title())

    return sorted(set(found))

# ----------------------------------
# Experience
# ----------------------------------
def extract_experience(text):

    text = text.lower()

    # Case 1: Direct experience mention (e.g. 2 years, 3+ years)
    match = re.search(r'(\d+)\+?\s*(years?|year|yrs?)', text)

    if match:
        return match.group(1) + " Years"

    # Case 2: Calculate from date range
    months = {
        "jan":1, "january":1,
        "feb":2, "february":2,
        "mar":3, "march":3,
        "apr":4, "april":4,
        "may":5,
        "jun":6, "june":6,
        "jul":7, "july":7,
        "aug":8, "august":8,
        "sep":9, "sept":9, "september":9,
        "oct":10, "october":10,
        "nov":11, "november":11,
        "dec":12, "december":12
    }

    pattern = r'(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t|tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s+(\d{4})\s*[-–]\s*(present|current|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:t|tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)?\s*(\d{4})?'

    matches = re.findall(pattern, text)

    if matches:

        total_months = 0

        for start_month, start_year, end_month, end_year in matches:

            start = datetime(int(start_year), months[start_month], 1)

            if end_month in ["present", "current"]:
                end = datetime.now()
            else:
                end = datetime(int(end_year), months[end_month], 1)

            diff = (end.year - start.year) * 12 + (end.month - start.month)

            if diff > 0:
                total_months += diff

        years = total_months // 12
        rem_months = total_months % 12

        if years > 0:
            return f"{years} Years {rem_months} Months"

        elif rem_months > 0:
            return f"{rem_months} Months"

    return "Not Mentioned"

# ----------------------------------
# Education
# ----------------------------------

def extract_education(text):

    text = text.lower()

    degree = []

    for key, value in EDUCATION.items():

        if key in text:

            degree.append(value)

    degree = sorted(set(degree))

    if degree:
        return degree

# ----------------------------------
# Parse JD
# ----------------------------------

def parse_job_description(pdf_path):

    text = extract_text(pdf_path)

    return {

        "job_title": extract_job_title(text),

        "skills": extract_skills(text),

        "experience": extract_experience(text),

        "education": extract_education(text),

        "text": text

    }

# ----------------------------------
# Testing
# ----------------------------------

if __name__ == "__main__":

    jd_path = input("Enter JD PDF Path : ")

    result = parse_job_description(jd_path)

    print("\n========== JOB DESCRIPTION ==========\n")

    print("Job Title :", result["job_title"])
    print("Skills :", result["skills"])
    print("Experience :", result["experience"])
    print("Education :", result["education"])