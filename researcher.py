import requests
import re
from typing import List, Dict, Any, Optional

OPENALEX_API_URL = "https://api.openalex.org/authors"

# Comprehensive index of Chinese universities and institutes offering Agronomy & Agricultural Scholarships
# (CSC Type B, ANSO, CAAS, and Provincial Scholarships)
ALL_CHINESE_AGRI_INSTITUTIONS = [
    # Top National Agricultural Universities (CSC Type B)
    {"name": "China Agricultural University (CAU)", "province": "Beijing", "type": "CSC Type B"},
    {"name": "Nanjing Agricultural University (NJAU)", "province": "Jiangsu", "type": "CSC Type B / Jiangsu Gov"},
    {"name": "Huazhong Agricultural University (HZAU)", "province": "Hubei", "type": "CSC Type B / Hubei Gov"},
    {"name": "Northwest A&F University (NWAFU)", "province": "Shaanxi", "type": "CSC Type B"},
    {"name": "South China Agricultural University (SCAU)", "province": "Guangdong", "type": "CSC Type B / Guangdong Gov"},
    
    # ANSO & CAS National Institutes (ANSO Scholarship / UCAS)
    {"name": "University of Chinese Academy of Sciences (UCAS)", "province": "Beijing", "type": "ANSO / CSC Type B"},
    {"name": "CAS Institute of Genetics and Developmental Biology", "province": "Beijing", "type": "ANSO Scholarship"},
    {"name": "CAS Institute of Subtropical Agriculture", "province": "Hunan", "type": "ANSO Scholarship"},
    {"name": "CAS Northeast Institute of Geography and Agroecology", "province": "Jilin", "type": "ANSO Scholarship"},
    {"name": "CAS Institute of Soil Science", "province": "Jiangsu", "type": "ANSO Scholarship"},
    
    # CAAS National Academy
    {"name": "Graduate School of Chinese Academy of Agricultural Sciences (GSCAAS)", "province": "Beijing", "type": "CSC Type B / CAAS Fellowship"},
    {"name": "CAAS Institute of Crop Sciences", "province": "Beijing", "type": "CSC / CAAS Fellowship"},
    
    # High-Quota Provincial Agricultural Universities (CSC Type B & Provincial Scholarships)
    {"name": "Shandong Agricultural University (SDAU)", "province": "Shandong", "type": "CSC / Shandong Gov"},
    {"name": "Sichuan Agricultural University (SICAU)", "province": "Sichuan", "type": "CSC / Sichuan Gov"},
    {"name": "Henan Agricultural University", "province": "Henan", "type": "CSC / Henan Gov"},
    {"name": "Hunan Agricultural University", "province": "Hunan", "type": "CSC / Hunan Gov"},
    {"name": "Shenyang Agricultural University", "province": "Liaoning", "type": "CSC / Liaoning Gov"},
    {"name": "Jilin Agricultural University", "province": "Jilin", "type": "CSC / Jilin Gov"},
    {"name": "Hebei Agricultural University", "province": "Hebei", "type": "CSC / Hebei Gov"},
    {"name": "Anhui Agricultural University", "province": "Anhui", "type": "CSC / Anhui Gov"},
    {"name": "Jiangxi Agricultural University", "province": "Jiangxi", "type": "CSC / Jiangxi Gov"},
    {"name": "Fujian Agriculture and Forestry University (FAFU)", "province": "Fujian", "type": "CSC / Fujian Gov"},
    {"name": "Gansu Agricultural University", "province": "Gansu", "type": "CSC / Gansu Gov"},
    {"name": "Xinjiang Agricultural University", "province": "Xinjiang", "type": "CSC / Xinjiang Gov"},
    {"name": "Yunnan Agricultural University", "province": "Yunnan", "type": "CSC / Yunnan Gov"},
    {"name": "Inner Mongolia Agricultural University", "province": "Inner Mongolia", "type": "CSC / Regional Gov"},
    {"name": "Shanxi Agricultural University", "province": "Shanxi", "type": "CSC / Shanxi Gov"},
    {"name": "Heilongjiang Bayi Agricultural University", "province": "Heilongjiang", "type": "CSC / Provincial Gov"},
    
    # Comprehensive Universities with Major Agronomy Faculties
    {"name": "Zhejiang University (College of Agriculture & Biotech)", "province": "Zhejiang", "type": "CSC Type B / Zhejiang Gov"},
    {"name": "Yangzhou University (College of Agriculture)", "province": "Jiangsu", "type": "CSC / Jiangsu Gov"},
    {"name": "Hainan University (School of Tropical Agriculture)", "province": "Hainan", "type": "CSC / Hainan Gov"},
    {"name": "Southwest University (College of Agronomy & Biotech)", "province": "Chongqing", "type": "CSC Type B"},
    {"name": "Guizhou University (College of Agriculture)", "province": "Guizhou", "type": "CSC / Guizhou Gov"},
    {"name": "Guangxi University (College of Agriculture)", "province": "Guangxi", "type": "CSC / Guangxi Gov"}
]

def search_scholars_openalex(topic: str = "Agronomy", institution_name: str = "", limit: int = 15) -> List[Dict[str, Any]]:
    """
    Search academic researchers based in China specializing in Agronomy or related subfields
    across all Chinese universities using OpenAlex API.
    """
    params = {
        "search": topic,
        "filter": "last_known_institutions.country_code:CN",
        "per_page": min(limit, 30),
        "sort": "cited_by_count:desc"
    }
    
    if institution_name:
        params["filter"] += f",last_known_institutions.display_name.search:{institution_name}"
        
    headers = {
        "User-Agent": "Agronomy-Scholarship-Agent/1.0 (mailto:scholarships@academic-outreach.org)"
    }
    
    results = []
    try:
        response = requests.get(OPENALEX_API_URL, params=params, headers=headers, timeout=12)
        if response.status_code == 200:
            data = response.json()
            for author in data.get("results", []):
                name = author.get("display_name", "")
                
                institutions = author.get("last_known_institutions", [])
                university = institutions[0].get("display_name", "Chinese Agricultural Institution") if institutions else "Chinese Agricultural Institution"
                
                x_concepts = author.get("x_concepts", [])
                concepts = [c.get("display_name") for c in x_concepts[:6] if c.get("display_name")]
                research_areas = ", ".join(concepts) if concepts else topic
                
                # Fetch recent works by this author
                works_api = author.get("works_api_url", "")
                recent_papers = []
                if works_api:
                    try:
                        w_resp = requests.get(f"{works_api}?per_page=3&sort=publication_year:desc", headers=headers, timeout=6)
                        if w_resp.status_code == 200:
                            w_data = w_resp.json()
                            for w in w_data.get("results", []):
                                title = w.get("title")
                                year = w.get("publication_year")
                                if title:
                                    recent_papers.append(f"({year}) {title}")
                    except Exception:
                        pass
                
                papers_str = " | ".join(recent_papers) if recent_papers else "Recent papers in " + research_areas
                source_url = author.get("id", "")
                
                results.append({
                    "name": name,
                    "university": university,
                    "province": "China",
                    "email": "",
                    "department": "Department of Agronomy / Crop Science",
                    "research_areas": research_areas,
                    "recent_papers": papers_str,
                    "scholarship_type": "CSC / ANSO / Provincial",
                    "source_url": source_url
                })
    except Exception as e:
        print(f"Error querying OpenAlex: {e}")
        
    return results

def extract_emails_from_text(text: str) -> List[str]:
    """Extract email addresses from scraped or pasted text."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    return list(set(emails))
