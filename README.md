# 🌾 CSC & ANSO Scholarship Outreach Agent

An autonomous research, intelligent alignment, and safe email dispatch system tailored for international candidates in **Agriculture – Agronomy** (pre-configured for GPA: 3.52).

This system covers **all Chinese institutions** with international scholarship quotas:
* **CSC (Chinese Government Scholarship - Type B / University Program)**
* **ANSO Scholarship** (University of Chinese Academy of Sciences & CAS Institutes)
* **CAAS Fellowship** (Chinese Academy of Agricultural Sciences)
* **Provincial Government Scholarships** (Jiangsu, Shandong, Sichuan, Hubei, Guangdong, etc.)
* **University Presidential & Full-Tuition Scholarships** across all provincial agricultural universities.

---

## 📁 Project Structure

```
csc_outreach_bot/
│
├── run_app.bat            # 1-Click launcher for Windows (double-click to run!)
├── app.py                 # Streamlit web dashboard & CRM interface
├── database.py            # SQLite database manager (stores history across machines)
├── researcher.py          # Academic researcher discovering professors in China
├── aligner.py             # AI Alignment Engine (bridges student background to professor research)
├── mailer.py              # Gmail SMTP dispatcher with anti-spam delays & attachments
├── sample_professors.csv  # 16 pre-selected Agronomy professors across China
├── requirements.txt       # Python libraries
├── outreach.db            # SQLite database file (created automatically)
└── uploads/               # Folder storing your CV, Transcripts, and Articles
```

---

## 🚀 How to Run on this Computer

1. Simply **double-click** `run_app.bat`.
   * It will verify required packages and open the dashboard in your web browser (`http://localhost:8501`).
2. Or open Command Prompt in this folder and run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

---

## 💻 How to Transfer & Run on Your Other Computer

Because this application is 100% portable and uses a self-contained SQLite database:

1. **Copy the entire `csc_outreach_bot` folder** to a USB flash drive or zip it and upload to Google Drive/OneDrive.
2. Paste the folder onto your other computer.
3. On the other computer, make sure Python is installed, then simply **double-click `run_app.bat`**!
   * All your candidate profiles, saved drafts, and sent history in `outreach.db` will transfer seamlessly.
   * You will **never** accidentally re-email a professor you previously contacted.

---

## 🔐 How to Generate Your Google App Password

To allow the local Python mailer to dispatch emails safely without sharing your master password:

1. Go to your **[Google Account](https://myaccount.google.com/)**.
2. Click **Security** on the left menu.
3. Under "How you sign in to Google", ensure **2-Step Verification** is turned ON.
4. Go to **[App Passwords](https://myaccount.google.com/apppasswords)**.
5. Create a new app name (e.g. `CSC Outreach Bot`) and click **Create**.
6. Google will give you a 16-character code (e.g., `abcd efgh ijkl mnop`).
7. Enter this code inside the bot dashboard under the **Gmail & Safety Settings** tab.
8. Click **Test SMTP Authentication** or **Send Test Email** to verify!

---

## 🛡️ Anti-Spam Safeguards Built-in

* **Randomized Jitter Delay:** Waits 60 to 180 seconds between emails to emulate human typing/sending patterns so Chinese university email filters do not mark your address as spam.
* **Daily Sending Quota:** Capped at 20–25 emails per day to keep your Gmail account in pristine health.
* **Human-in-the-Loop Review:** Only emails marked as **'approved'** are sent. You can inspect and tweak each AI alignment paragraph beforehand.

---

## 🌾 Strategic Agronomy Advice for Chinese Scholarships

1. **Don't just target Beijing:** Top provincial agricultural universities (Shandong Ag, Sichuan Ag, Henan Ag, Hunan Ag, Anhui Ag, Gansu Ag) receive substantial government funding for crop research and have generous international quotas with far less competition than CAU or Tsinghua.
2. **Timing:** Cold email professors between **November and February** for Fall intake. Send during Chinese working hours (**8:30 AM – 11:30 AM or 2:00 PM – 5:00 PM Beijing Time**).
3. **Acceptance Letter:** Once a professor says yes, send them the university's official *Provisional Acceptance Form* or *CSC Supervisor Agreement Form* immediately for signature.
