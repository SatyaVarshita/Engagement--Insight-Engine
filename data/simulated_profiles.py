import json
import random
import datetime
from typing import List, Dict, Any

def generate_user_profile(user_id: str) -> Dict[str, Any]:
    """Generate a simulated user profile."""
    resume_uploaded = random.choice([True, False])
    goal_tags = random.sample(["GRE", "data science", "web development", 
                              "machine learning", "cloud computing", "DevOps"], 
                              k=random.randint(1, 3))
    karma = random.randint(50, 500)
    projects_added = random.randint(0, 5)
    quiz_history = random.sample(["aptitude", "python", "java", "javascript", 
                                 "data structures", "algorithms"], 
                                 k=random.randint(0, 4))
    clubs_joined = random.sample(["coding club", "data science club", "AI club", 
                                 "cloud computing club"], 
                                 k=random.randint(0, 3))
    buddy_count = random.randint(0, 10)
    
    return {
        "user_id": user_id,
        "profile": {
            "resume_uploaded": resume_uploaded,
            "goal_tags": goal_tags,
            "karma": karma,
            "projects_added": projects_added,
            "quiz_history": quiz_history,
            "clubs_joined": clubs_joined,
            "buddy_count": buddy_count
        }
    }

def generate_user_activity(days_back: int = 30) -> Dict[str, Any]:
    """Generate simulated user activity data."""
    login_streak = random.randint(0, 7)
    posts_created = random.randint(0, 10)
    buddies_interacted = random.randint(0, 5)
    
    # Generate a random date within the last 'days_back' days
    today = datetime.datetime.now()
    random_days = random.randint(0, days_back)
    last_event_date = today - datetime.timedelta(days=random_days)
    last_event_attended = last_event_date.strftime("%Y-%m-%d")
    
    return {
        "activity": {
            "login_streak": login_streak,
            "posts_created": posts_created,
            "buddies_interacted": buddies_interacted,
            "last_event_attended": last_event_attended
        }
    }

def generate_peer_snapshot() -> Dict[str, Any]:
    """Generate simulated peer snapshot data."""
    batch_avg_projects = random.randint(1, 5)
    batch_resume_uploaded_pct = random.randint(50, 95)
    
    events = ["startup-meetup", "coding-contest", "hackathon", "career-fair", "workshop"]
    batch_event_attendance = {event: random.randint(3, 20) for event in random.sample(events, k=random.randint(2, 5))}
    
    buddies_attending = []
    if random.random() > 0.3:  # 70% chance of having buddies attending events
        buddies_attending = random.sample(list(batch_event_attendance.keys()), 
                                         k=min(random.randint(1, 3), len(batch_event_attendance)))
    
    return {
        "peer_snapshot": {
            "batch_avg_projects": batch_avg_projects,
            "batch_resume_uploaded_pct": batch_resume_uploaded_pct,
            "batch_event_attendance": batch_event_attendance,
            "buddies_attending_events": buddies_attending
        }
    }

def generate_complete_profile(user_id: str) -> Dict[str, Any]:
    """Generate a complete user profile with activity and peer data."""
    profile = generate_user_profile(user_id)
    activity = generate_user_activity()
    peer_snapshot = generate_peer_snapshot()
    
    # Merge all dictionaries
    complete_profile = {**profile}
    complete_profile.update(activity)
    complete_profile.update(peer_snapshot)
    
    return complete_profile

def generate_training_data(num_samples: int = 500) -> List[Dict[str, Any]]:
    """Generate training data for the ML model."""
    training_data = []
    
    for i in range(num_samples):
        user_id = f"stu_{1000 + i}"
        profile = generate_complete_profile(user_id)
        
        # Extract features for training
        resume_uploaded = profile["profile"]["resume_uploaded"]
        karma = profile["profile"]["karma"]
        projects_added = profile["profile"]["projects_added"]
        batch_avg_projects = profile["peer_snapshot"]["batch_avg_projects"]
        batch_resume_uploaded_pct = profile["peer_snapshot"]["batch_resume_uploaded_pct"]
        
        # Calculate event FOMO score
        event_fomo_score = 0
        if profile["peer_snapshot"]["buddies_attending_events"]:
            event_fomo_score = len(profile["peer_snapshot"]["buddies_attending_events"])
        
        # Generate labels based on rules
        should_nudge_resume = 1 if (not resume_uploaded and batch_resume_uploaded_pct >= 80) else 0
        should_nudge_project = 1 if (projects_added == 0 and batch_avg_projects >= 2) else 0
        should_nudge_event = 1 if event_fomo_score >= 2 else 0
        
        # Create training sample
        training_sample = {
            "features": {
                "resume_uploaded": resume_uploaded,
                "karma": karma,
                "projects_added": projects_added,
                "batch_avg_projects": batch_avg_projects,
                "batch_resume_uploaded_pct": batch_resume_uploaded_pct,
                "event_fomo_score": event_fomo_score
            },
            "label": {
                "should_nudge_resume": should_nudge_resume,
                "should_nudge_project": should_nudge_project,
                "should_nudge_event": should_nudge_event
            }
        }
        
        training_data.append(training_sample)
    
    return training_data

def generate_test_profiles(num_profiles: int = 10, num_peer_sets: int = 3) -> List[Dict[str, Any]]:
    """Generate test profiles with different peer sets."""
    test_profiles = []
    
    for peer_set in range(num_peer_sets):
        # Generate a peer snapshot for this set
        peer_snapshot = generate_peer_snapshot()["peer_snapshot"]
        
        for i in range(num_profiles):
            user_id = f"test_stu_{peer_set}_{i}"
            profile = generate_user_profile(user_id)["profile"]
            activity = generate_user_activity()["activity"]
            
            test_profile = {
                "user_id": user_id,
                "profile": profile,
                "activity": activity,
                "peer_snapshot": peer_snapshot
            }
            
            test_profiles.append(test_profile)
    
    return test_profiles

if __name__ == "__main__":
    # Generate training data
    training_data = generate_training_data(500)
    with open("data/training_data.json", "w") as f:
        json.dump(training_data, f, indent=2)
    
    # Generate test profiles
    test_profiles = generate_test_profiles(10, 3)
    with open("data/test_profiles.json", "w") as f:
        json.dump(test_profiles, f, indent=2)
    
    print(f"Generated {len(training_data)} training samples")
    print(f"Generated {len(test_profiles)} test profiles")