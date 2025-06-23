from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class ProfileData(BaseModel):
    resume_uploaded: bool
    goal_tags: List[str]
    karma: int
    projects_added: int
    quiz_history: List[str]
    clubs_joined: List[str]
    buddy_count: int

class ActivityData(BaseModel):
    login_streak: int
    posts_created: int
    buddies_interacted: int
    last_event_attended: str

class PeerSnapshotData(BaseModel):
    batch_avg_projects: int
    batch_resume_uploaded_pct: int
    batch_event_attendance: Dict[str, int]
    buddies_attending_events: List[str]

class EngagementAnalysisRequest(BaseModel):
    user_id: str
    profile: ProfileData
    activity: ActivityData
    peer_snapshot: PeerSnapshotData

class NudgeResponse(BaseModel):
    type: str
    title: str
    action: str
    priority: str

class EngagementAnalysisResponse(BaseModel):
    user_id: str
    nudges: List[NudgeResponse]
    status: str