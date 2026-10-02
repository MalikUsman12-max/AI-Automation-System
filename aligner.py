from typing import Dict, Any, Optional
import json

def generate_alignment_email(
    candidate: Dict[str, Any],
    professor: Dict[str, Any],
    api_key: Optional[str] = None
) -> Dict[str, str]:
    """
    Generates a personalized cold email tailored to a specific professor in China.
    Highlights Hafiz Usman Iftikhar's published research (including his paper on Chinese Agricultural Sciences,
    and his experimental study on potassium silicate and oxidative stress mitigation in sunflowers),
    along with his 3.52 GPA and strong foundation in crop physiology and field trial design.
    """
    
    cand_name = candidate.get("full_name") or "Hafiz Usman Iftikhar"
    cand_degree_target = candidate.get("target_degree") or "Master's Degree"
    cand_current_degree = candidate.get("current_degree") or "B.Sc. (Hons.) Agriculture-Agronomy"
    cand_major = candidate.get("major") or "Agriculture - Agronomy"
    cand_interests = candidate.get("research_interest") or "Crop Abiotic Stress Physiology, Nutrient Management, Plant Antioxidant Defense"
    cand_skills = candidate.get("skills") or "Field experiment layout (RCBD/CRD factorial), plant-soil biochemical analysis, antioxidant enzyme assays"
    cand_gpa = candidate.get("gpa") or "3.52 / 4.00"
    cand_prev_uni = candidate.get("previous_university") or "University of Sargodha, Pakistan"
    cand_scholarships = candidate.get("target_scholarships") or "CSC Type B, ANSO Scholarship, or Provincial Government Scholarships"
    
    prof_name = professor.get("name", "Professor")
    prof_uni = professor.get("university", "your esteemed university")
    prof_dept = professor.get("department", "Department of Agronomy")
    prof_areas = professor.get("research_areas") or "Agronomy and Crop Science"
    prof_papers = professor.get("recent_papers") or ""
    
    # 1. Gemini LLM Alignment Engine (if API key available)
    if api_key and api_key.strip():
        try:
            from google import genai
            client = genai.Client(api_key=api_key.strip())
            
            prompt = f"""
You are an expert academic advisor writing an elite cold outreach email for Hafiz Usman Iftikhar, an exceptional Agronomy graduate applying for graduate supervision in China under fully-funded international scholarships (CSC Type B, ANSO, or Provincial Government Scholarships).

CANDIDATE STRENGTHS & RESEARCH BACKGROUND:
- Name: Hafiz Usman Iftikhar
- Degree: B.Sc. (Hons.) Agriculture-Agronomy from University of Sargodha, Pakistan (CGPA: 3.52 / 4.00, Grade A in Crop Physiology, Conservation Agronomy, Organic Farming, and Scientific Writing).
- Proven Research & Publications:
  1. Co-authored paper on 'Historical Overview of the Chinese Agricultural Sciences and Technological Development' (CRAF, 2023) — demonstrates longstanding commitment and study of China's agricultural advances!
  2. Research article on 'Potassium Silicate Decreases Nickel Induced Oxidative Stress by Improving Nutrients Uptake and Antioxidant Defense System in Sunflower' (IJBR, 2025) — demonstrates experimental expertise in heavy metal/abiotic stress, plant nutrition (K & Si), ROS scavenging, and factorial field/pot trial layouts.
- Target Degree: Master's in Agronomy / Crop Science commencing Fall 2026.

TARGET PROFESSOR:
- Name: {prof_name}
- Institution: {prof_uni} ({prof_dept})
- Research Focus: {prof_areas}
- Recent Works/Papers: {prof_papers}

TASK:
Write a high-converting, professional cold outreach email.
KEY RULES:
- Connect the candidate's experimental research in abiotic stress mitigation (potassium/silicon fertilization, antioxidant enzyme defense, nutrient uptake) and knowledge of Chinese agricultural development with the professor's research topics.
- Even if the professor works on a different crop or agronomic area, establish a strong intellectual bridge showing how Hafiz's hands-on lab and field methodologies will add immediate value to the professor's team.
- State clearly that the candidate is seeking supervision under fully-funded scholarships ({cand_scholarships}) and requires no laboratory funding.
- Request a Provisional Acceptance Letter / Supervisor Agreement Form to support the scholarship application.
- Tone: Respectful, scholarly, under 250 words.

OUTPUT FORMAT:
Return ONLY valid JSON with two fields: "subject" and "body".
Do not include markdown tags.
"""
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            text = response.text.strip()
            
            if text.startswith("```"):
                text = text.strip("`")
                if text.startswith("json"):
                    text = text[4:].strip()
            
            data = json.loads(text)
            return {
                "subject": data.get("subject", f"Prospective Master's Applicant: Supervision Request in Agronomy – Hafiz Usman Iftikhar"),
                "body": data.get("body", "")
            }
        except Exception as e:
            print(f"Gemini API generation note: {e}")
            pass

    # 2. Dynamic Rule-Based Template with Publications Highlighted
    subject = f"Prospective Master's Applicant: Supervision Request in Agronomy – Hafiz Usman Iftikhar"
    
    paper_ref = ""
    if prof_papers and prof_papers.strip():
        first_paper = prof_papers.split("|")[0].strip()
        paper_ref = f"I have been closely following your research group's recent publications, especially your impactful work on '{first_paper}'."
    else:
        paper_ref = f"I have been closely studying your scientific contributions in {prof_areas}."

    alignment_bridge = (
        f"Having earned a CGPA of 3.52 in B.Sc. (Hons.) Agriculture-Agronomy (with Grade A in Crop Physiology and Research Writing), "
        f"I have developed strong research capabilities. My published work includes investigating potassium silicate-mediated mitigation "
        f"of nickel-induced oxidative stress in sunflowers, as well as an analytical review on Chinese Agricultural Sciences and "
        f"Technological Development. My hands-on experience in layout of field experiments, antioxidant enzyme assays, and plant nutrition "
        f"equips me to quickly integrate into your ongoing projects on {prof_areas}."
    )

    body = f"""Dear Professor {prof_name},

I hope this email finds you in good health and high spirits.

My name is Hafiz Usman Iftikhar, and I recently completed my B.Sc. (Hons.) in Agriculture-Agronomy from the University of Sargodha, Pakistan, graduating with a CGPA of 3.52 / 4.00. I am writing to express my earnest desire to pursue my Master's degree under your supervision at {prof_uni} starting in Fall 2026.

{paper_ref}

{alignment_bridge}

I am preparing to apply for fully-funded international scholarships, including the Chinese Government Scholarship (CSC Type B - University Program), the ANSO Scholarship, and Provincial Government Fellowships. These cover full tuition waiver, campus accommodation, medical insurance, and a monthly stipend; thus, no financial burden will be placed on your laboratory.

I have attached my Curriculum Vitae, official transcript of records, and my research publications for your kind evaluation. If my profile aligns with your group's standards, I would be deeply honored if you would consider providing me with a Provisional Acceptance Letter to support my formal scholarship submission.

Thank you very much for your time, consideration, and leadership in agricultural sciences.

With highest regards,

Hafiz Usman Iftikhar
B.Sc. (Hons.) Agriculture-Agronomy | University of Sargodha
Email: {candidate.get('gmail_address', '')}
"""

    return {
        "subject": subject,
        "body": body.strip()
    }
