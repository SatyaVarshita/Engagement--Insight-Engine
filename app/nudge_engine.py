import json
import pickle
import datetime
import numpy as np
from typing import List, Dict, Any
from app.schemas import NudgeResponse, EngagementAnalysisRequest

class NudgeEngine:
    def __init__(self, config_path="config.json", model_path="models/nudge_models.pkl"):
        """Initialize the nudge engine with configuration and models."""
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        # Load models
        with open(model_path, 'rb') as f:
            self.models = pickle.load(f)
    
    def _extract_features(self, request: EngagementAnalysisRequest) -> np.ndarray:
        """Extract features from the request for model prediction."""
        # Extract relevant features
        resume_uploaded = request.profile.resume_uploaded
        karma = request.profile.karma
        projects_added = request.profile.projects_added
        batch_avg_projects = request.peer_snapshot.batch_avg_projects
        batch_resume_uploaded_pct = request.peer_snapshot.batch_resume_uploaded_pct
        
        # Calculate event FOMO score
        event_fomo_score = len(request.peer_snapshot.buddies_attending_events)
        
        # Create feature vector
        features = np.array([
            1 if resume_uploaded else 0,
            karma,
            projects_added,
            batch_avg_projects,
            batch_resume_uploaded_pct,
            event_fomo_score
        ]).reshape(1, -1)
        
        return features
    
    def _apply_rule_based_logic(self, request: EngagementAnalysisRequest) -> List[Dict[str, Any]]:
        """Apply rule-based logic to generate nudges."""
        nudges = []
        
        # Resume nudge rule
        if not request.profile.resume_uploaded and request.peer_snapshot.batch_resume_uploaded_pct >= self.config["profile_rules"]["resume_threshold"] * 100:
            nudges.append({
                "type": "profile",
                "title": f"{request.peer_snapshot.batch_resume_uploaded_pct}% of your peers have uploaded resumes. You haven't yet!",
                "action": "Upload resume now",
                "priority": self.config["priority_labels"]["resume"]
            })
        
        # Project nudge rule
        if request.profile.projects_added == 0 and request.peer_snapshot.batch_avg_projects >= self.config["profile_rules"]["projects_avg_threshold"]:
            nudges.append({
                "type": "profile",
                "title": f"Your peers have {request.peer_snapshot.batch_avg_projects} projects on average. Add your first project!",
                "action": "Add a project",
                "priority": self.config["priority_labels"]["project"]
            })
        
        # Quiz nudge rule
        if request.profile.quiz_history:
            last_quiz_date = datetime.datetime.now() - datetime.timedelta(days=10)  # Simulated
            days_since_last_quiz = (datetime.datetime.now() - last_quiz_date).days
            if days_since_last_quiz >= self.config["profile_rules"]["quiz_idle_days"]:
                nudges.append({
                    "type": "profile",
                    "title": f"It's been {days_since_last_quiz} days since your last quiz. Keep learning!",
                    "action": "Take a 2-question quiz today",
                    "priority": self.config["priority_labels"]["quiz"]
                })
        
        # Event FOMO nudge rule
        buddies_attending = request.peer_snapshot.buddies_attending_events
        if buddies_attending and len(buddies_attending) >= self.config["event_rules"]["buddy_attendance_trigger"]:
            event = buddies_attending[0]  # Just take the first event
            nudges.append({
                "type": "event",
                "title": f"{len(buddies_attending)} of your buddies are joining '{event}'",
                "action": "Join the event",
                "priority": self.config["priority_labels"]["event_fomo"]
            })
        
        # Batch attendance nudge rule
        for event, attendance in request.peer_snapshot.batch_event_attendance.items():
            if attendance >= self.config["event_rules"]["batch_attendance_trigger"]:
                nudges.append({
                    "type": "event",
                    "title": f"{attendance} peers from your batch are attending '{event}'",
                    "action": "Check out this popular event",
                    "priority": self.config["priority_labels"]["event_fomo"]
                })
                break  # Just show one batch attendance nudge
        
        return nudges
    
    def _apply_ml_logic(self, request: EngagementAnalysisRequest) -> List[Dict[str, Any]]:
        """Apply ML-based logic to generate nudges."""
        features = self._extract_features(request)
        nudges = []
        
        # Predict resume nudge
        resume_prediction = self.models["resume_model"].predict(features)[0]
        if resume_prediction == 1 and not request.profile.resume_uploaded:
            nudges.append({
                "type": "profile",
                "title": "Your profile would be stronger with a resume. Upload now!",
                "action": "Upload resume",
                "priority": self.config["priority_labels"]["resume"]
            })
        
        # Predict project nudge
        project_prediction = self.models["project_model"].predict(features)[0]
        if project_prediction == 1 and request.profile.projects_added == 0:
            nudges.append({
                "type": "profile",
                "title": "Adding projects can boost your profile visibility by 70%",
                "action": "Add your first project",
                "priority": self.config["priority_labels"]["project"]
            })
        
        # Predict event nudge
        event_prediction = self.models["event_model"].predict(features)[0]
        if event_prediction == 1 and request.peer_snapshot.buddies_attending_events:
            event = request.peer_snapshot.buddies_attending_events[0]
            nudges.append({
                "type": "event",
                "title": f"Our AI thinks you'd enjoy the '{event}' event",
                "action": "View event details",
                "priority": self.config["priority_labels"]["event_fomo"]
            })
        
        return nudges
    
    def _prioritize_nudges(self, rule_nudges: List[Dict[str, Any]], ml_nudges: List[Dict[str, Any]]) -> List[NudgeResponse]:
        """Prioritize and combine nudges from rule-based and ML-based logic."""
        # Combine all nudges
        all_nudges = rule_nudges + ml_nudges
        
        # Remove duplicates (prefer rule-based nudges)
        unique_nudges = {}
        for nudge in all_nudges:
            nudge_key = f"{nudge['type']}_{nudge['action']}"
            if nudge_key not in unique_nudges:
                unique_nudges[nudge_key] = nudge
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        sorted_nudges = sorted(unique_nudges.values(), key=lambda x: priority_order[x["priority"]])
        
        # Limit to max nudges per day
        max_nudges = self.config["max_nudges_per_day"]
        limited_nudges = sorted_nudges[:max_nudges]
        
        # Convert to NudgeResponse objects
        return [NudgeResponse(**nudge) for nudge in limited_nudges]
    
    def generate_nudges(self, request: EngagementAnalysisRequest) -> List[NudgeResponse]:
        """Generate nudges based on user profile, activity, and peer data."""
        # Apply rule-based logic
        rule_nudges = self._apply_rule_based_logic(request)
        
        # Apply ML-based logic
        ml_nudges = self._apply_ml_logic(request)
        
        # Prioritize and combine nudges
        return self._prioritize_nudges(rule_nudges, ml_nudges)