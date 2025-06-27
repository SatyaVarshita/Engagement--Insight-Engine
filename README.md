
# 🚀 Engagement Insight Engine

An **AI-powered microservice** that analyzes user profiles, activity, and peer behavior to generate personalized engagement nudges. Built using FastAPI, scikit-learn, and Docker — designed to run fully offline.

---

## ✅ Features

- Analyze user profile completeness and activity
- Compare user metrics with peers
- Generate nudges (Glow-up Advisor, Event FOMO Radar)
- Fully deterministic, rule + ML hybrid logic
- Offline, portable, and configurable

---

## 🧠 Architecture

The system uses a two-layer scoring engine:
- **Rule Layer**: Applies hard-coded conditions (defined in `config.json`)
- **AI Layer**: Uses `RandomForestClassifier` to score nudging likelihood

Nudges are filtered and prioritized based on rules.

---

## 📋 Tech Stack

- **FastAPI** – Backend microservice
- **scikit-learn** – Lightweight ML classifier
- **Pydantic** – Data validation
- **Docker** – Container deployment
- **Python 3.9+**

---

## ⚙️ Setup Instructions

'''bash
1.## clone repository##
git clone https://github.com/your-username/engagement-insight-engine.git
cd engagement-insight-engine
2. Create and activate a virtual environment
🔹 On Windows:
`bash`
 python -m venv venv
venv\Scripts\activate

### 3. Install Requirements
pip install -r requirements.txt
4. Run the App
bash
uvicorn main:app --reload --port 8000
5. Open Docs
http://localhost:8000/docs

🐳 Docker (Optional)
bash
docker build -t engagement-insight-engine .
docker run -p 8000:8000 engagement-insight-engine
Again once seeing docker run in browser the command http://localhost:8000/docs

##API END POINTS##
| Method | Endpoint              | Description                    |
| ------ | --------------------- | ------------------------------ |
| POST   | `/analyze-engagement` | Analyze user and return nudges |
| GET    | `/health`             | Health check                   |
| GET    | `/version`            | Version info                   |




# API Key or Secrets (if calling external services)
OPENAI_API_KEY=your_openai_api_key_here

# ML Model Path (optional)
MODEL_PATH=models/nudge_model.pkl

# App Environment
APP_ENV=development

# Log Level
LOG_LEVEL=info




🧪 Sample Test Case

{
  "user_id": "stu_7023",
  "profile": {
    "resume_uploaded": false,
    "karma": 190,
    "projects_added": 0
  },
  "activity": {
    "login_streak": 2,
    "buddies_interacted": 0
  },
  "peer_snapshot": {
    "batch_resume_uploaded_pct": 84,
    "buddies_attending_events": ["coding-contest"]
  }
}
 
 🔄 Response
 {
  "nudges": [
    {
      "type": "profile",
      "title": "84% of your peers have uploaded resumes. You haven’t yet!",
      "action": "Upload resume now",
        "priority": "high"
        }
       ]
       "status": "generated"
       }

📁 Project Structure
├── main.py               # FastAPI app entry
├── nudge_engine.py       # Core nudge generation logic
├── config.json           # Rule thresholds
├── model.pkl             # Trained ML model
├── peer_snapshot.json    # Peer group data
├── test_cases/           # Sample test inputs
├── Dockerfile            # For containerization
├── README.md             # You're reading it






🙏 Acknowledgements:
## 🧠 AI Assistance Notice:
This project was developed with the help of modern AI tools and manual customization:

ChatGPT by OpenAI – Used to generate the base logic, test cases, and documentation structure.

V0.dev by Vercel – Used to prototype any required frontend UI (if applicable).

🧉 Visual Studio Code (VS Code) – Primary IDE for development, testing, and debugging

🛠️ All AI-generated content was reviewed and modified to meet exact project needs and functionality


