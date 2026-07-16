import re
import pdfplumber

# ----------------------------------
# Skills Database
# ----------------------------------

SKILLS = [
    "python","java","c","c++","sql","mysql","mongodb",
    "html","css","javascript","react","nodejs","django",
    "flask","machine learning","deep learning","nlp",
    "tensorflow","keras","pytorch","opencv","pandas",
    "numpy","scikit-learn","git","linux","aws","azure",
    "docker","kubernetes","power bi","tableau","excel","rest api","fastapi",
    "postgresql","postgres"


]

EDUCATION = [
    "b.tech","btech","b.e","be",
    "m.tech","mtech",
    "bca","mca",
    "bsc","msc",
    "mba","phd"
]

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

    match = re.search(r'(\d+)\+?\s*(?:years|year)', text.lower())

    if match:
        return match.group(1) + " Years"

    return "Not Mentioned"

# ----------------------------------
# Education
# ----------------------------------
def extract_education(text):

    text = text.lower()

    found = []

    if "b.tech" in text or "btech" in text:
        found.append("B.Tech")

    if "b.e" in text or "be" in text:
        found.append("B.E")

    if "m.tech" in text or "mtech" in text:
        found.append("M.Tech")

    if "bca" in text:
        found.append("BCA")

    if "mca" in text:
        found.append("MCA")

    if "bsc" in text:
        found.append("BSc")

    if "msc" in text:
        found.append("MSc")

    if "mba" in text:
        found.append("MBA")

    if "phd" in text:
        found.append("PhD")

    return found

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