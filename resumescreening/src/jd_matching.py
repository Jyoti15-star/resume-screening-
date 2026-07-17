import re
from predict import predict_role

from resume_parser import (
    extract_text as extract_resume_text,
    extract_skills,
    extract_experience,
    extract_education
   
)

from jd_parser import (
    parse_job_description
)


# ----------------------------------
# Skill Matching
# ----------------------------------

def match_skills(resume_skills, jd_skills):

    resume_set = set(skill.lower() for skill in resume_skills)
    jd_set = set(skill.lower() for skill in jd_skills)

    matched = sorted(resume_set & jd_set)
    missing = sorted(jd_set - resume_set)

    if len(jd_set) == 0:
        score = 0
    else:
        score = (len(matched) / len(jd_set)) * 100

    return matched, missing, score


# ----------------------------------
# Experience Matching
# ----------------------------------

def match_experience(resume_exp, jd_exp):

    def get_years(text):
        text = text.lower()
        years = 0
        year_match = re.search(r'(\d+)\s*year', text)
        month_match = re.search(r'(\d+)\s*month', text)
        if year_match:
            years += int(year_match.group(1))
        if month_match:
            years += int(month_match.group(1)) / 12
        return years
    resume_years = get_years(resume_exp)
    jd_years = get_years(jd_exp)

    return resume_years >= jd_years

# ----------------------------------
# Education Matching
# ----------------------------------
def match_education(resume_edu, jd_edu):

    if not resume_edu or not jd_edu:
        return False

    resume_set = set(item.lower() for item in resume_edu)
    jd_set = set(item.lower() for item in jd_edu)

    return len(resume_set & jd_set) > 0


# ----------------------------------
# ATS Score
# ----------------------------------

def calculate_ats_score(skill_score,
                        experience_match,
                        education_match,
                        role_match):

    ats = 0

    # Skills = 60
    ats += skill_score * 0.60

    # Experience = 15
    if experience_match:
        ats += 15

    # Education = 10
    if education_match:
        ats += 10

    # Role Match = 15
    if role_match:
        ats += 15

    return round(ats,2)

# ----------------------------------
# Main Matching Function
# ----------------------------------
def match_resume_with_jd(resume_text, jd_pdf_path):
    resume_role = predict_role(resume_text)

    resume_skills = extract_skills(resume_text)
    resume_exp = extract_experience(resume_text)
    resume_edu = extract_education(resume_text)

    jd = parse_job_description(jd_pdf_path)
    jd_role = jd["job_title"]
    if jd_role != "Not Found":
        role_match = (
        resume_role.lower() in jd_role.lower()
        or jd_role.lower() in resume_role.lower()
        )
    else:
        role_match = False

    matched, missing, skill_score = match_skills(
        resume_skills,
        jd["skills"]
    )

    exp_match = match_experience(
        resume_exp,
        jd["experience"]
    )

    edu_match = match_education(
        resume_edu,
        jd["education"]
    )

    ats = calculate_ats_score(
        skill_score,
        exp_match,
        edu_match,
        role_match
    )
    return {
        "resume_role": resume_role,
        "jd_role": jd_role,
        "role_match": role_match,
        "matched_skills": matched,
        "missing_skills": missing,
        "skill_score": round(skill_score,2),
        "experience_match": exp_match,
        "education_match": edu_match,
        "ats_score": ats
        }


# ----------------------------------
# Testing
# ----------------------------------

if __name__ == "__main__":

        # Resume PDF
    resume_path = input("Enter Resume PDF Path: ")

    # JD PDF
    jd_path = input("Enter JD PDF Path: ")

    # Resume Text
    resume = extract_resume_text(resume_path)

    # Matching
    result = match_resume_with_jd(
        resume,
        jd_path
)
    

    print("\n========== ATS REPORT ==========\n")
    print("Resume Role :", result["resume_role"])
    print("JD Role :", result["jd_role"])
    print("Role Match :", result["role_match"])

    print("Matched Skills :", result["matched_skills"])
    print("Missing Skills :", result["missing_skills"])
    print("Skill Score :", result["skill_score"])
    print("Experience Match :", result["experience_match"])
    print("Education Match :", result["education_match"])
    print("ATS Score :", result["ats_score"])


   