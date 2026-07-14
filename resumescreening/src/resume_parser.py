import re
import pdfplumber
import spacy

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# ----------------------------------
# Skills Database
# ----------------------------------

SKILLS = [

    "python","java","c","c++","sql","mysql","mongodb",
    "html","css","javascript","react","nodejs","django",
    "flask","machine learning","deep learning","nlp",
    "tensorflow","keras","pytorch","opencv","pandas",
    "numpy","scikit-learn","git","linux","aws","azure",
    "power bi","tableau","excel"

]

EDUCATION = [

    "b.tech","btech","b.e","be","m.tech","mtech",
    "bca","mca","bsc","msc","mba","phd"

]

# ----------------------------------
# Read PDF
# ----------------------------------

def extract_text(pdf_path):

    text=""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            page_text=page.extract_text()

            if page_text:

                text+=page_text+"\n"

    return text

# ----------------------------------
# Name
# ----------------------------------

def extract_name(text):

    doc=nlp(text)

    for ent in doc.ents:

        if ent.label_=="PERSON":

            return ent.text

    return "Not Found"

# ----------------------------------
# Email
# ----------------------------------

def extract_email(text):

    match=re.findall(r'[\w\.-]+@[\w\.-]+\.\w+',text)

    return match[0] if match else "Not Found"

# ----------------------------------
# Phone
# ----------------------------------

def extract_phone(text):

    match=re.findall(r'(\+91[\-\s]?\d{10}|\d{10})',text)

    return match[0] if match else "Not Found"

# ----------------------------------
# Skills
# ----------------------------------

def extract_skills(text):

    text=text.lower()

    found=[]

    for skill in SKILLS:

        if skill.lower() in text:

            found.append(skill.title())

    return sorted(set(found))

# ----------------------------------
# Education
# ----------------------------------

def extract_education(text):

    text=text.lower()

    degree=[]

    for edu in EDUCATION:

        if edu in text:

            degree.append(edu.upper())

    return sorted(set(degree))

# ----------------------------------
# Experience
# ----------------------------------

def extract_experience(text):

    match=re.findall(r'(\d+)\+?\s*(?:years|year)',text.lower())

    if match:

        return match[0]+" Years"

    return "Not Mentioned"

# ----------------------------------
# Main
# ----------------------------------

if __name__=="__main__":

    path=input("Enter Resume PDF Path : ")

    resume=extract_text(path)

    print("\n========== Resume Details ==========\n")

    print("Name :",extract_name(resume))
    print("Email :",extract_email(resume))
    print("Phone :",extract_phone(resume))
    print("Skills :",extract_skills(resume))
    print("Education :",extract_education(resume))
    print("Experience :",extract_experience(resume))



    