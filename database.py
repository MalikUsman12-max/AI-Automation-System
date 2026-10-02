import sqlite3
import os
from typing import Dict, List, Optional, Any

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "outreach.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Settings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        full_name TEXT DEFAULT 'Hafiz Usman Iftikhar',
        current_degree TEXT DEFAULT 'B.Sc. (Hons.) Agriculture-Agronomy',
        target_degree TEXT DEFAULT "Master's Degree",
        major TEXT DEFAULT 'Agriculture - Agronomy (Crop Science & Plant Physiology)',
        research_interest TEXT DEFAULT 'Crop Abiotic Stress Physiology (Heavy Metals/Salinity/Drought), Nutrient Use Efficiency, Potassium and Silicon Nutrition, Plant Antioxidant Defense, Sustainable Agronomy',
        gpa TEXT DEFAULT '3.52 / 4.00 (73.58%)',
        skills TEXT DEFAULT 'Field experiment layout (RCBD, CRD factorial), plant-soil biochemical analysis, antioxidant enzyme assays, heavy metal stress mitigation, crop physiology measurements, scientific writing',
        previous_university TEXT DEFAULT 'University of Sargodha, Pakistan',
        target_scholarships TEXT DEFAULT 'Chinese Government Scholarship (CSC Type B), ANSO Scholarship (UCAS/CAS), Provincial Government & University Full Fellowships',
        cv_path TEXT DEFAULT '',
        transcript_path TEXT DEFAULT '',
        article1_path TEXT DEFAULT '',
        article2_path TEXT DEFAULT '',
        gmail_address TEXT DEFAULT '',
        gmail_app_password TEXT DEFAULT '',
        gemini_api_key TEXT DEFAULT '',
        min_delay_sec INTEGER DEFAULT 60,
        max_delay_sec INTEGER DEFAULT 180,
        daily_limit INTEGER DEFAULT 25
    )
    """)
    
    # Check if article1_path and article2_path columns exist, add if missing
    cursor.execute("PRAGMA table_info(settings)")
    existing_cols = [row[1] for row in cursor.fetchall()]
    if "article1_path" not in existing_cols:
        cursor.execute("ALTER TABLE settings ADD COLUMN article1_path TEXT DEFAULT ''")
    if "article2_path" not in existing_cols:
        cursor.execute("ALTER TABLE settings ADD COLUMN article2_path TEXT DEFAULT ''")
        
    # Check if province exists in professors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        university TEXT NOT NULL,
        province TEXT DEFAULT '',
        department TEXT DEFAULT '',
        email TEXT NOT NULL,
        research_areas TEXT DEFAULT '',
        recent_papers TEXT DEFAULT '',
        scholarship_type TEXT DEFAULT 'CSC / ANSO / Provincial',
        source_url TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(email)
    )
    """)
    
    cursor.execute("PRAGMA table_info(professors)")
    p_cols = [row[1] for row in cursor.fetchall()]
    if "province" not in p_cols:
        cursor.execute("ALTER TABLE professors ADD COLUMN province TEXT DEFAULT ''")
    if "scholarship_type" not in p_cols:
        cursor.execute("ALTER TABLE professors ADD COLUMN scholarship_type TEXT DEFAULT 'CSC / ANSO / Provincial'")

    # 3. Outreach Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS outreach_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        professor_id INTEGER NOT NULL,
        email_subject TEXT DEFAULT '',
        email_body TEXT DEFAULT '',
        status TEXT DEFAULT 'draft',
        sent_at TIMESTAMP,
        error_message TEXT DEFAULT '',
        FOREIGN KEY (professor_id) REFERENCES professors (id) ON DELETE CASCADE
    )
    """)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    t_path = os.path.join(base_dir, "uploads", "transcript.pdf")
    a1_path = os.path.join(base_dir, "uploads", "article1.pdf")
    a2_path = os.path.join(base_dir, "uploads", "article2.pdf")
    cv_path = os.path.join(base_dir, "uploads", "CV.pdf")
    
    cursor.execute("SELECT COUNT(*) FROM settings WHERE id = 1")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO settings (
            id, full_name, current_degree, target_degree, major, 
            previous_university, gpa, research_interest, skills, 
            transcript_path, article1_path, article2_path, cv_path
        ) VALUES (
            1, 'Hafiz Usman Iftikhar', 'B.Sc. (Hons.) Agriculture-Agronomy', "Master's Degree", 
            'Agriculture - Agronomy (Crop Science & Plant Physiology)',
            'University of Sargodha, Pakistan', '3.52 / 4.00 (73.58%)',
            'Crop Abiotic Stress Physiology (Heavy Metals/Salinity/Drought), Nutrient Use Efficiency, Potassium and Silicon Nutrition, Plant Antioxidant Defense',
            'Field experiment layout (RCBD, CRD factorial), plant-soil biochemical analysis, antioxidant enzyme assays, heavy metal stress mitigation, crop physiology measurements, scientific writing',
            ?, ?, ?, ?
        )
        """, (t_path, a1_path, a2_path, cv_path if os.path.exists(cv_path) else ''))
    else:
        cursor.execute("""
        UPDATE settings SET 
        transcript_path = ?, article1_path = ?, article2_path = ?
        WHERE id = 1
        """, (t_path, a1_path, a2_path))
        
    conn.commit()
    conn.close()

def get_settings() -> Dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {}

def update_settings(data: Dict[str, Any]):
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    for k, v in data.items():
        if k != "id":
            fields.append(f"{k} = ?")
            values.append(v)
    query = f"UPDATE settings SET {', '.join(fields)} WHERE id = 1"
    cursor.execute(query, values)
    conn.commit()
    conn.close()

def add_professor(name: str, university: str, email: str, province: str = "",
                  department: str = "", research_areas: str = "", recent_papers: str = "",
                  scholarship_type: str = "CSC / ANSO / Provincial", source_url: str = "") -> Optional[int]:
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO professors (name, university, province, email, department, research_areas, recent_papers, scholarship_type, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name.strip(), university.strip(), province.strip(), email.strip().lower(), department.strip(),
              research_areas.strip(), recent_papers.strip(), scholarship_type.strip(), source_url.strip()))
        prof_id = cursor.lastrowid
        conn.commit()
        return prof_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_all_professors(status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    query = """
    SELECT p.*, o.id as draft_id, o.email_subject, o.email_body, 
           COALESCE(o.status, 'approved') as status, o.sent_at, o.error_message
    FROM professors p
    LEFT JOIN outreach_logs o ON p.id = o.professor_id
    """
    params = []
    if status_filter:
        query += " WHERE o.status = ?"
        params.append(status_filter)
    query += " ORDER BY p.university ASC, p.name ASC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_universities_summary() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT university, province, scholarship_type, COUNT(p.id) as prof_count
    FROM professors p
    GROUP BY university
    ORDER BY prof_count DESC, university ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_professors_by_university(uni_name: str) -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT p.*, o.id as draft_id, o.email_subject, o.email_body, 
           COALESCE(o.status, 'approved') as status, o.sent_at
    FROM professors p
    LEFT JOIN outreach_logs o ON p.id = o.professor_id
    WHERE p.university = ?
    ORDER BY p.name ASC
    """, (uni_name,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_draft(professor_id: int, subject: str, body: str, status: str = 'draft') -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM outreach_logs WHERE professor_id = ?", (professor_id,))
    existing = cursor.fetchone()
    
    if existing:
        log_id = existing[0]
        cursor.execute("""
        UPDATE outreach_logs 
        SET email_subject = ?, email_body = ?, status = ?
        WHERE id = ?
        """, (subject, body, status, log_id))
    else:
        cursor.execute("""
        INSERT INTO outreach_logs (professor_id, email_subject, email_body, status)
        VALUES (?, ?, ?, ?)
        """, (professor_id, subject, body, status))
        log_id = cursor.lastrowid
        
    conn.commit()
    conn.close()
    return log_id

def set_professor_status(prof_id: int, status: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM outreach_logs WHERE professor_id = ?", (prof_id,))
    row = cursor.fetchone()
    if row:
        cursor.execute("UPDATE outreach_logs SET status = ? WHERE id = ?", (status, row[0]))
    conn.commit()
    conn.close()

def batch_set_all_status(target_status: str = 'approved'):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE outreach_logs SET status = ? WHERE status != 'sent'", (target_status,))
    conn.commit()
    conn.close()

def update_log_status(log_id: int, status: str, error_message: str = ""):
    conn = get_connection()
    cursor = conn.cursor()
    if status == 'sent':
        cursor.execute("""
        UPDATE outreach_logs 
        SET status = 'sent', sent_at = CURRENT_TIMESTAMP, error_message = ''
        WHERE id = ?
        """, (log_id,))
    else:
        cursor.execute("""
        UPDATE outreach_logs 
        SET status = ?, error_message = ?
        WHERE id = ?
        """, (status, error_message, log_id))
    conn.commit()
    conn.close()

def get_stats() -> Dict[str, int]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM professors")
    total_professors = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT university) FROM professors")
    total_unis = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM outreach_logs WHERE status = 'draft'")
    drafts = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM outreach_logs WHERE status = 'approved'")
    approved = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM outreach_logs WHERE status = 'sent'")
    sent = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM outreach_logs WHERE status = 'rejected'")
    rejected = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total": total_professors,
        "unis": total_unis,
        "drafts": drafts,
        "approved": approved,
        "sent": sent,
        "rejected": rejected
    }
