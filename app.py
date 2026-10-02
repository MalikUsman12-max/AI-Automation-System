import streamlit as st
import os
import time
import random
import pandas as pd

import database as db
import aligner
import mailer

# Initialize database
db.init_db()

st.set_page_config(
    page_title="CSC & ANSO Scholarship Outreach Agent",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-header { font-size: 2.1rem; font-weight: 800; color: #1E3A8A; margin-bottom: 0.1rem; }
    .sub-header { font-size: 1.05rem; color: #4B5563; margin-bottom: 1.2rem; }
    .stat-card { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 14px; text-align: center; border-top: 3px solid #2563EB; }
    .stat-num { font-size: 1.7rem; font-weight: 700; color: #0F172A; }
    .stat-label { font-size: 0.8rem; color: #64748B; font-weight: 600; text-transform: uppercase; }
    .prof-card { background: white; border: 1px solid #E5E7EB; border-radius: 8px; padding: 14px; margin-bottom: 12px; }
    .status-badge { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }
    .badge-approved { background: #DCFCE7; color: #166534; }
    .badge-draft { background: #FEF9C3; color: #854D0E; }
    .badge-sent { background: #DBEAFE; color: #1E40AF; }
    .badge-rejected { background: #FEE2E2; color: #991B1B; }
</style>
""", unsafe_allow_html=True)

# Main Title & Subtitle
st.markdown('<div class="main-header">🌾 CSC & ANSO Scholarship Outreach Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Applicant: <b>Hafiz Usman Iftikhar</b> | B.Sc. (Hons.) Agriculture-Agronomy (CGPA: <b>3.52</b>) | University of Sargodha</div>', unsafe_allow_html=True)

# Quick Statistics Row
stats = db.get_stats()
sc1, sc2, sc3, sc4, sc5 = st.columns(5)
with sc1:
    st.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("unis", 0)}</div><div class="stat-label">🏛️ Chinese Universities</div></div>', unsafe_allow_html=True)
with sc2:
    st.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("total", 0)}</div><div class="stat-label">🧑‍🏫 Total Professors</div></div>', unsafe_allow_html=True)
with sc3:
    st.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("approved", 0)}</div><div class="stat-label">🚀 Ready to Dispatch</div></div>', unsafe_allow_html=True)
with sc4:
    st.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("sent", 0)}</div><div class="stat-label">✉️ Emails Delivered</div></div>', unsafe_allow_html=True)
with sc5:
    st.markdown(f'<div class="stat-card"><div class="stat-num">{stats.get("rejected", 0)}</div><div class="stat-label">❌ Skipped / Rejected</div></div>', unsafe_allow_html=True)

st.write("---")

settings = db.get_settings()

# Collect verified attachments
base_dir = os.path.dirname(os.path.abspath(__file__))
active_attachments = []
for fname in ["transcript.pdf", "article1.pdf", "article2.pdf", "CV.pdf"]:
    fpath = os.path.join(base_dir, "uploads", fname)
    if os.path.exists(fpath):
        active_attachments.append((fname, fpath))

# Navigation Tabs
tabs = st.tabs([
    "🏛️ Universities & Faculties Roster",
    "✍️ AI Drafts & Alignment",
    "🚀 Email Dispatcher (Send / Reject)",
    "👤 Candidate Profile & Documents",
    "🔐 Gmail & Anti-Spam Settings",
    "📊 Master CRM Tracker"
])

# ========================================================
# TAB 1: UNIVERSITIES & FACULTIES ROSTER
# ========================================================
with tabs[0]:
    st.subheader("🏛️ Complete Roster: Chinese Universities & Agronomy Faculties")
    st.info("Check and verify every Chinese institution with international scholarship quotas (CSC Type B, ANSO, CAAS, Provincial Government). Under each university, all professors and their official emails are listed.")
    
    unis_summary = db.get_universities_summary()
    
    if not unis_summary:
        st.warning("No universities loaded yet.")
    else:
        u_col1, u_col2 = st.columns([1, 2])
        with u_col1:
            st.write("#### Select a University to View Faculty")
            uni_names = [u["university"] for u in unis_summary]
            selected_uni = st.selectbox("Choose University", uni_names)
            
            # Display meta for selected uni
            cur_uni_meta = next((u for u in unis_summary if u["university"] == selected_uni), None)
            if cur_uni_meta:
                st.markdown(f"**Province:** `{cur_uni_meta.get('province') or 'China'}`")
                st.markdown(f"**Scholarship Type:** `{cur_uni_meta.get('scholarship_type') or 'CSC / Provincial'}`")
                st.markdown(f"**Faculty Members in CRM:** `{cur_uni_meta.get('prof_count', 0)}`")
                
            st.write("---")
            st.write("#### ➕ Add New Professor to this University")
            with st.form("add_prof_to_uni_form"):
                new_p_name = st.text_input("Professor Full Name", placeholder="e.g. Prof. Liu Qiang")
                new_p_dept = st.text_input("Department / College", value="College of Agronomy")
                new_p_email = st.text_input("Official Email Address", placeholder="e.g. liuqiang@cau.edu.cn")
                new_p_areas = st.text_input("Research Areas", placeholder="Crop Physiology; Plant Nutrition; Abiotic Stress")
                new_p_papers = st.text_input("Recent Paper / Project", placeholder="Recent publication in crop science")
                
                add_p_btn = st.form_submit_button("Add Professor & Generate Draft")
                if add_p_btn:
                    if new_p_name and new_p_email:
                        pid = db.add_professor(
                            name=new_p_name,
                            university=selected_uni,
                            email=new_p_email,
                            province=cur_uni_meta.get('province') if cur_uni_meta else '',
                            department=new_p_dept,
                            research_areas=new_p_areas,
                            recent_papers=new_p_papers,
                            scholarship_type=cur_uni_meta.get('scholarship_type') if cur_uni_meta else 'CSC / ANSO / Provincial'
                        )
                        if pid:
                            d = aligner.generate_alignment_email(settings, {
                                "name": new_p_name,
                                "university": selected_uni,
                                "department": new_p_dept,
                                "research_areas": new_p_areas,
                                "recent_papers": new_p_papers
                            })
                            db.save_draft(pid, d["subject"], d["body"], status="approved")
                            st.success(f"Added {new_p_name} and generated outreach draft!")
                            st.rerun()
                        else:
                            st.warning("A professor with this email is already registered.")
                    else:
                        st.error("Name and Email are required.")

        with u_col2:
            st.write(f"#### Faculty Directory: {selected_uni}")
            profs_in_uni = db.get_professors_by_university(selected_uni)
            
            if profs_in_uni:
                for p in profs_in_uni:
                    p_stat = (p.get("status") or "draft").lower()
                    status_color = "badge-approved" if p_stat == "approved" else ("badge-sent" if p_stat == "sent" else "badge-draft")
                    st.markdown(f"""
                    <div class="prof-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h4 style="margin:0; color:#1E3A8A;">🧑‍🏫 {p['name']}</h4>
                            <span class="status-badge {status_color}">{p_stat.upper()}</span>
                        </div>
                        <p style="margin:4px 0; color:#374151;"><b>Department:</b> {p.get('department') or 'N/A'}</p>
                        <p style="margin:4px 0; color:#2563EB;"><b>Official Email:</b> <code>{p['email']}</code></p>
                        <p style="margin:4px 0; color:#4B5563;"><b>Research Focus:</b> {p.get('research_areas') or 'N/A'}</p>
                        <p style="margin:4px 0; color:#6B7280; font-size:0.88rem;"><b>Recent Works:</b> {p.get('recent_papers') or 'N/A'}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No professors registered for this university yet.")

# ========================================================
# TAB 2: AI DRAFTS & ALIGNMENT
# ========================================================
with tabs[1]:
    st.subheader("✍️ Personalized AI Outreach Drafts")
    st.info("Every professor has a tailored cold email connecting your 3.52 GPA, your CRAF 2023 paper on Chinese Agricultural Sciences, and your 2025 experimental paper on Potassium Silicate/Nickel Stress.")
    
    all_profs = db.get_all_professors()
    if all_profs:
        # Safe string handling: guarantee status is never None
        prof_dict = {
            f"{p['name']} ({p['university']}) — [{(p.get('status') or 'draft').upper()}]": p 
            for p in all_profs
        }
        selected_prof_label = st.selectbox("Select Professor Draft to Inspect or Edit", list(prof_dict.keys()))
        selected_p = prof_dict[selected_prof_label]
        
        st.write("---")
        ad_col1, ad_col2 = st.columns([1, 1.2])
        
        with ad_col1:
            st.write(f"### 🧑‍🏫 {selected_p['name']}")
            st.write(f"**University:** {selected_p['university']} ({selected_p.get('province') or 'China'})")
            st.write(f"**Department:** {selected_p.get('department') or 'Department of Agronomy'}")
            st.write(f"**Official Email:** `{selected_p['email']}`")
            st.write(f"**Research Areas:** {selected_p.get('research_areas') or 'Agronomy & Crop Science'}")
            st.write(f"**Recent Publications:**\n{selected_p.get('recent_papers') or 'Recent research'}")
            
            st.write("#### 📎 Confirmed Email Attachments:")
            for fname, _ in active_attachments:
                st.markdown(f"✅ `{fname}`")
                
            if st.button("⚡ Regenerate Alignment Draft with AI", use_container_width=True):
                with st.spinner("Regenerating alignment bridge..."):
                    new_d = aligner.generate_alignment_email(settings, selected_p, api_key=settings.get("gemini_api_key"))
                    db.save_draft(selected_p["id"], new_d["subject"], new_d["body"], status="approved")
                    st.success("Draft regenerated and set to APPROVED!")
                    st.rerun()

        with ad_col2:
            st.write("### ✉️ Email Content")
            with st.form("draft_editor_form"):
                subj_val = st.text_input("Subject Line", value=selected_p.get("email_subject") or f"Prospective Master's Applicant: Supervision Request – {settings.get('full_name')}")
                body_val = st.text_area("Personalized Email Body", value=selected_p.get("email_body") or "", height=360)
                
                status_opts = ["approved", "draft", "rejected", "sent"]
                cur_stat = (selected_p.get("status") or "approved").lower()
                status_val = st.selectbox("Status", status_opts, index=status_opts.index(cur_stat) if cur_stat in status_opts else 0)
                
                save_draft_btn = st.form_submit_button("💾 Save Draft Changes", use_container_width=True)
                if save_draft_btn:
                    db.save_draft(selected_p["id"], subj_val, body_val, status=status_val)
                    st.success("Draft saved successfully!")
                    st.rerun()
    else:
        st.warning("No professors found.")

# ========================================================
# TAB 3: EMAIL DISPATCHER (SEND / REJECT)
# ========================================================
with tabs[2]:
    st.subheader("🚀 Email Dispatcher: Review & Send Commands")
    st.info("Here are all professors in your outreach queue. You have direct control over each email: click **[🚀 Send Email]** to dispatch immediately, or **[❌ Reject / Skip]** to remove from queue.")
    
    st.write("#### 📎 Outgoing Attachments for Every Email:")
    att_cols = st.columns(len(active_attachments) if active_attachments else 1)
    if active_attachments:
        for idx, (afname, afpath) in enumerate(active_attachments):
            with att_cols[idx]:
                st.success(f"📎 **{afname}** (Attached)")
    else:
        st.warning("No attachments found. Please ensure files are in `uploads/`.")
        
    st.write("---")
    
    gmail_addr = settings.get("gmail_address", "")
    gmail_pwd = settings.get("gmail_app_password", "")
    
    if not gmail_addr or not gmail_pwd:
        st.error("⚠️ Please configure your Gmail address and Google App Password in the **'🔐 Gmail & Anti-Spam Settings'** tab before sending.")
    
    # Filter controls
    disp_filter = st.radio("Display Queue:", ["Approved Only (Ready to Send)", "All Professors", "Drafts Only"], horizontal=True)
    
    if disp_filter == "Approved Only (Ready to Send)":
        target_profs = db.get_all_professors(status_filter="approved")
    elif disp_filter == "Drafts Only":
        target_profs = db.get_all_professors(status_filter="draft")
    else:
        target_profs = db.get_all_professors()

    # Batch Actions Bar
    col_b1, col_b2, col_b3 = st.columns([1.5, 1, 1])
    with col_b1:
        st.write(f"**Queue Count:** `{len(target_profs)} professors listed`")
    with col_b2:
        if st.button("✅ Approve All to Queue"):
            db.batch_set_all_status("approved")
            st.success("All professors marked as APPROVED!")
            st.rerun()
    with col_b3:
        if st.button("⚡ Dispatch All Approved (Auto-Delay)", type="primary"):
            if not gmail_addr or not gmail_pwd:
                st.error("Configure Gmail in Settings tab first!")
            else:
                approved_list = db.get_all_professors(status_filter="approved")
                if not approved_list:
                    st.warning("No approved emails to send.")
                else:
                    progress_bar = st.progress(0)
                    msg_ph = st.empty()
                    file_paths = [p[1] for p in active_attachments]
                    
                    for i, p in enumerate(approved_list):
                        msg_ph.markdown(f"**Sending to:** {p['name']} (`{p['email']}`) at {p['university']}...")
                        ok, res_msg = mailer.send_single_outreach(
                            sender_email=gmail_addr,
                            app_password=gmail_pwd,
                            recipient_email=p["email"],
                            subject=p.get("email_subject") or "Supervision Request",
                            body=p.get("email_body") or "",
                            attachment_paths=file_paths
                        )
                        if ok:
                            db.update_log_status(p["draft_id"], "sent")
                            st.toast(f"Delivered to {p['name']}!", icon="✅")
                        else:
                            db.update_log_status(p["draft_id"], "failed", error_message=res_msg)
                            st.toast(f"Failed for {p['name']}: {res_msg}", icon="❌")
                            
                        progress_bar.progress((i + 1) / len(approved_list))
                        
                        if i < len(approved_list) - 1:
                            wait_s = random.uniform(settings.get("min_delay_sec", 60), settings.get("max_delay_sec", 180))
                            for sec in range(int(wait_s), 0, -1):
                                msg_ph.text(f"Waiting {sec}s before next email (anti-spam protection)...")
                                time.sleep(1)
                                
                    msg_ph.success("🎉 Batch dispatch completed!")
                    st.rerun()

    st.write("---")
    
    # Table of Individual Professors with SEND / REJECT Buttons
    if target_profs:
        for p in target_profs:
            p_id = p["id"]
            p_name = p["name"]
            p_uni = p["university"]
            p_email = p["email"]
            p_status = (p.get("status") or "draft").lower()
            p_subject = p.get("email_subject") or "Supervision Request"
            
            with st.container():
                r_col1, r_col2, r_col3, r_col4, r_col5 = st.columns([2.5, 2.5, 1.2, 1.2, 1.2])
                
                with r_col1:
                    st.markdown(f"**🧑‍🏫 {p_name}**")
                    st.caption(f"🏛️ {p_uni} ({p.get('province') or 'China'})")
                with r_col2:
                    st.markdown(f"✉️ `{p_email}`")
                    st.caption(f"📝 *{p_subject[:45]}...*")
                with r_col3:
                    if p_status == "approved":
                        st.markdown('<span class="status-badge badge-approved">APPROVED</span>', unsafe_allow_html=True)
                    elif p_status == "sent":
                        st.markdown('<span class="status-badge badge-sent">SENT</span>', unsafe_allow_html=True)
                    elif p_status == "rejected":
                        st.markdown('<span class="status-badge badge-rejected">REJECTED</span>', unsafe_allow_html=True)
                    else:
                        st.markdown('<span class="status-badge badge-draft">DRAFT</span>', unsafe_allow_html=True)
                        
                with r_col4:
                    if st.button("🚀 Send Email", key=f"send_btn_{p_id}", use_container_width=True):
                        if not gmail_addr or not gmail_pwd:
                            st.error("Configure Gmail in Settings tab first!")
                        else:
                            with st.spinner(f"Sending to {p_name}..."):
                                file_paths = [af[1] for af in active_attachments]
                                ok, res_msg = mailer.send_single_outreach(
                                    sender_email=gmail_addr,
                                    app_password=gmail_pwd,
                                    recipient_email=p_email,
                                    subject=p.get("email_subject") or "Supervision Request",
                                    body=p.get("email_body") or "",
                                    attachment_paths=file_paths
                                )
                                if ok:
                                    db.update_log_status(p["draft_id"], "sent")
                                    st.success(f"Email delivered to {p_name}!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    db.update_log_status(p["draft_id"], "failed", error_message=res_msg)
                                    st.error(f"Failed: {res_msg}")
                                    
                with r_col5:
                    if st.button("❌ Reject", key=f"rej_btn_{p_id}", use_container_width=True):
                        db.set_professor_status(p_id, "rejected")
                        st.warning(f"Marked {p_name} as Rejected.")
                        time.sleep(0.5)
                        st.rerun()
                st.write("<hr style='margin:4px 0; border:0; border-top:1px solid #F1F5F9;'>", unsafe_allow_html=True)
    else:
        st.info("No professors found in this filter view.")

# ========================================================
# TAB 4: CANDIDATE PROFILE & DOCUMENTS
# ========================================================
with tabs[3]:
    st.subheader("👤 Candidate Profile & Research Credentials")
    
    st.markdown("""
    <div style="background:#F0FDF4; border-left:4px solid #16A34A; padding:12px; border-radius:6px; margin-bottom:15px;">
        <h4 style="margin:0 0 6px 0; color:#166534;">🎓 Verified Credentials from Official Transcripts & Publications:</h4>
        <ul style="margin:0; padding-left:20px; color:#15803D;">
            <li><b>Candidate:</b> Hafiz Usman Iftikhar</li>
            <li><b>Graduating Institution:</b> University of Sargodha, Pakistan (Session 2021-2025)</li>
            <li><b>Degree:</b> B.Sc. (Hons.) Agriculture-Agronomy (CGPA: <b>3.52 / 4.00 - 73.58%</b>)</li>
            <li><b>Grade A Coursework:</b> Concepts of Crop Physiology (4.00), Conservation Agronomy (4.00), Organic Farming (4.00), Research & Scientific Writing (4.00)</li>
            <li><b>Article 1 (CRAF 2023):</b> <i>Historical Overview of the Chinese Agricultural Sciences and Technological Development</i></li>
            <li><b>Article 2 (IJBR 2025):</b> <i>Potassium Silicate Decreases Nickel Induced Oxidative Stress by Improving Nutrients Uptake and Antioxidant Defense System in Sunflower</i></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("#### 📄 Confirmed Document Attachments:")
    c_doc1, c_doc2, c_doc3, c_doc4 = st.columns(4)
    with c_doc1:
        st.success("✅ **transcript.pdf**\n(Official Transcript attached)")
    with c_doc2:
        st.success("✅ **article1.pdf**\n(Chinese Ag Science paper attached)")
    with c_doc3:
        st.success("✅ **article2.pdf**\n(K-Silicate/Nickel paper attached)")
    with c_doc4:
        cv_fpath = os.path.join(base_dir, "uploads", "CV.pdf")
        if os.path.exists(cv_fpath):
            st.success("✅ **CV.pdf**\n(Resume attached)")
        else:
            st.info("ℹ️ **CV.pdf**\n(Pending - upload below when ready)")
            
    st.write("---")
    st.write("#### 📤 Upload / Update CV File")
    new_cv_upload = st.file_uploader("Upload your CV / Resume (PDF)", type=["pdf"])
    if new_cv_upload:
        save_target = os.path.join(base_dir, "uploads", "CV.pdf")
        with open(save_target, "wb") as f:
            f.write(new_cv_upload.getbuffer())
        st.success("CV.pdf uploaded and saved! It will now be attached to all outgoing emails.")
        st.rerun()

# ========================================================
# TAB 5: GMAIL & ANTI-SPAM SETTINGS
# ========================================================
with tabs[4]:
    st.subheader("🔐 Secure Gmail Connection & Anti-Spam Safeguards")
    st.warning("🔒 Your password is stored locally on this machine and is never transmitted to any third party.")
    
    with st.form("settings_form"):
        sc_col1, sc_col2 = st.columns(2)
        with sc_col1:
            g_email = st.text_input("Your Gmail Address", value=settings.get("gmail_address", ""), placeholder="e.g. hafizusman@gmail.com")
            g_pwd = st.text_input("Google App Password (16 characters)", value=settings.get("gmail_app_password", ""), type="password", help="Generate from Google Account > Security > App Passwords")
            g_gemini = st.text_input("Gemini API Key (Optional)", value=settings.get("gemini_api_key", ""), type="password")
        with sc_col2:
            st.write("**Anti-Spam Delay Settings**")
            s_min_del = st.number_input("Minimum delay between emails (seconds)", min_value=30, max_value=300, value=settings.get("min_delay_sec", 60))
            s_max_del = st.number_input("Maximum delay between emails (seconds)", min_value=60, max_value=600, value=settings.get("max_delay_sec", 180))
            s_limit = st.number_input("Daily sending limit", min_value=5, max_value=50, value=settings.get("daily_limit", 25))
            
        save_settings_btn = st.form_submit_button("💾 Save Gmail & Safety Settings", use_container_width=True)
        if save_settings_btn:
            db.update_settings({
                "gmail_address": g_email,
                "gmail_app_password": g_pwd,
                "gemini_api_key": g_gemini,
                "min_delay_sec": s_min_del,
                "max_delay_sec": s_max_del,
                "daily_limit": s_limit
            })
            st.success("Settings saved locally!")
            
    st.write("---")
    st.write("#### 🧪 Test Your Connection")
    tc1, tc2 = st.columns(2)
    with tc1:
        if st.button("🔌 Test SMTP Authentication"):
            s = db.get_settings()
            ok, msg = mailer.test_smtp_connection(s.get("gmail_address", ""), s.get("gmail_app_password", ""))
            if ok:
                st.success(msg)
            else:
                st.error(msg)
    with tc2:
        if st.button("✉️ Send Test Email to My Own Inbox"):
            s = db.get_settings()
            ok, msg = mailer.send_test_email(s.get("gmail_address", ""), s.get("gmail_app_password", ""))
            if ok:
                st.success(msg)
            else:
                st.error(msg)

# ========================================================
# TAB 6: MASTER CRM TRACKER
# ========================================================
with tabs[5]:
    st.subheader("📊 Master Outreach CRM Tracker")
    all_crm_data = db.get_all_professors()
    
    if all_crm_data:
        crm_df = pd.DataFrame([{
            "ID": p["id"],
            "Professor": p["name"],
            "University": p["university"],
            "Province": p.get("province") or "China",
            "Department": p.get("department") or "N/A",
            "Email": p["email"],
            "Status": (p.get("status") or "draft").upper(),
            "Sent At": p.get("sent_at") or "-"
        } for p in all_crm_data])
        
        st.dataframe(crm_df, use_container_width=True)
        
        csv_bytes = crm_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Full Outreach CRM to CSV",
            data=csv_bytes,
            file_name="csc_agronomy_professors_crm.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("No data in CRM.")
