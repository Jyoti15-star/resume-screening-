import re

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

        match = re.search(r"\d+", text)

        if match:
            return int(match.group())

        return 0

    resume_years = get_years(resume_exp)
    jd_years = get_years(jd_exp)

    return resume_years >= jd_years


# ----------------------------------
# Education Matching
# ----------------------------------

def match_education(resume_edu, jd_edu):

    resume_set = set(item.lower() for item in resume_edu)
    jd_set = set(item.lower() for item in jd_edu)

    return len(resume_set & jd_set) > 0


# ----------------------------------
# ATS Score
# ----------------------------------

def calculate_ats_score(skill_score,
                        experience_match,
                        education_match):

    ats = 0

    # Skills = 70 Marks
    ats += skill_score * 0.70

    # Experience = 20 Marks
    if experience_match:
        ats += 20

    # Education = 10 Marks
    if education_match:
        ats += 10

    return round(ats, 2)


# ----------------------------------
# Main Matching Function
# ----------------------------------
def match_resume_with_jd(resume_text, jd_pdf_path):

    resume_skills = extract_skills(resume_text)
    resume_exp = extract_experience(resume_text)
    resume_edu = extract_education(resume_text)

    jd = parse_job_description(jd_pdf_path)

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
        edu_match
    )

    return {

        "matched_skills": matched,
        "missing_skills": missing,
        "skill_score": round(skill_score, 2),
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

    print("Matched Skills :", result["matched_skills"])
    print("Missing Skills :", result["missing_skills"])
    print("Skill Score :", result["skill_score"])
    print("Experience Match :", result["experience_match"])
    print("Education Match :", result["education_match"])
    print("ATS Score :", result["ats_score"])


   