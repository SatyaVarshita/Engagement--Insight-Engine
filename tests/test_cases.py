import json
import requests
import copy

def test_health_endpoint():
    """Test the health endpoint."""
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    print("Health endpoint test passed!")

def test_version_endpoint():
    """Test the version endpoint."""
    response = requests.get("http://localhost:8000/version")
    assert response.status_code == 200
    assert response.json() == {"version": "1.0.0"}
    print("Version endpoint test passed!")

def test_analyze_engagement_endpoint():
    """Test the analyze-engagement endpoint with various scenarios."""
    # Load test profiles
    with open("data/test_profiles.json", "r") as f:
        test_profiles = json.load(f)
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Resume not uploaded, high batch resume %",
            "profile_index": 0,
            "expected_nudge_types": ["profile"],
            "expected_nudge_actions": ["Upload resume"]
        },
        {
            "name": "Buddies joining event",
            "profile_index": 1,
            "expected_nudge_types": ["event"],
            "expected_nudge_actions": ["Join the event"]
        },
        {
            "name": "User up-to-date profile + no FOMO",
            "profile_index": 2,
            "expected_nudge_count": 0
        },
        {
            "name": "No projects added, high batch average",
            "profile_index": 3,
            "expected_nudge_types": ["profile"],
            "expected_nudge_actions": ["Add a project", "Add your first project"]
        },
        {
            "name": "Multiple nudges needed",
            "profile_index": 4,
            "expected_nudge_count_min": 2
        }
    ]
    
    # Run tests
    for i, scenario in enumerate(test_scenarios):
        print(f"\nRunning test scenario {i+1}: {scenario['name']}")
        
        # Create a deep copy to avoid modifying the original
        test_profile = copy.deepcopy(test_profiles[scenario["profile_index"]])
        
        # Modify test profile based on scenario
        if scenario["name"] == "Resume not uploaded, high batch resume %":
            test_profile["profile"]["resume_uploaded"] = False
            test_profile["peer_snapshot"]["batch_resume_uploaded_pct"] = 90
            # Ensure other conditions don't trigger nudges
            test_profile["profile"]["projects_added"] = 3
            test_profile["peer_snapshot"]["batch_avg_projects"] = 2
            test_profile["peer_snapshot"]["buddies_attending_events"] = []
            test_profile["peer_snapshot"]["batch_event_attendance"] = {"workshop": 5}  # Below trigger threshold
        
        elif scenario["name"] == "Buddies joining event":
            test_profile["peer_snapshot"]["buddies_attending_events"] = ["coding-contest", "hackathon"]
            # Ensure other conditions don't trigger nudges
            test_profile["profile"]["resume_uploaded"] = True
            test_profile["profile"]["projects_added"] = 3
            test_profile["peer_snapshot"]["batch_resume_uploaded_pct"] = 60  # Below threshold
            test_profile["peer_snapshot"]["batch_avg_projects"] = 2
        
        elif scenario["name"] == "User up-to-date profile + no FOMO":
            # Make sure ALL conditions are satisfied to avoid any nudges
            test_profile["profile"]["resume_uploaded"] = True
            test_profile["profile"]["projects_added"] = 3
            test_profile["profile"]["quiz_history"] = []  # No quiz history to avoid quiz nudges
            test_profile["peer_snapshot"]["buddies_attending_events"] = []
            test_profile["peer_snapshot"]["batch_resume_uploaded_pct"] = 60  # Below threshold
            test_profile["peer_snapshot"]["batch_avg_projects"] = 2  # Equal to user's projects
            test_profile["peer_snapshot"]["batch_event_attendance"] = {"workshop": 5}  # Below trigger threshold
        
        elif scenario["name"] == "No projects added, high batch average":
            test_profile["profile"]["projects_added"] = 0
            test_profile["peer_snapshot"]["batch_avg_projects"] = 4
            # Ensure other conditions don't trigger nudges
            test_profile["profile"]["resume_uploaded"] = True
            test_profile["peer_snapshot"]["batch_resume_uploaded_pct"] = 60  # Below threshold
            test_profile["peer_snapshot"]["buddies_attending_events"] = []
            test_profile["peer_snapshot"]["batch_event_attendance"] = {"workshop": 5}  # Below trigger threshold
        
        elif scenario["name"] == "Multiple nudges needed":
            test_profile["profile"]["resume_uploaded"] = False
            test_profile["profile"]["projects_added"] = 0
            test_profile["peer_snapshot"]["batch_resume_uploaded_pct"] = 85
            test_profile["peer_snapshot"]["batch_avg_projects"] = 3
            test_profile["peer_snapshot"]["buddies_attending_events"] = ["hackathon"]
        
        # Send request
        response = requests.post("http://localhost:8000/analyze-engagement", json=test_profile)
        
        # Check response
        assert response.status_code == 200, f"Failed with status code {response.status_code}"
        
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        # Validate response based on scenario
        if "expected_nudge_count" in scenario:
            actual_count = len(result["nudges"])
            expected_count = scenario["expected_nudge_count"]
            assert actual_count == expected_count, \
                f"Expected {expected_count} nudges, got {actual_count}. Nudges: {[n['title'] for n in result['nudges']]}"
            print(f"✓ Nudge count matches expected ({expected_count})")
        
        if "expected_nudge_count_min" in scenario:
            actual_count = len(result["nudges"])
            expected_min = scenario["expected_nudge_count_min"]
            assert actual_count >= expected_min, \
                f"Expected at least {expected_min} nudges, got {actual_count}"
            print(f"✓ Nudge count is at least {expected_min}")
        
        if "expected_nudge_types" in scenario:
            nudge_types = [nudge["type"] for nudge in result["nudges"]]
            for expected_type in scenario["expected_nudge_types"]:
                assert expected_type in nudge_types, f"Expected nudge type '{expected_type}' not found"
            print(f"✓ Nudge types match expected ({scenario['expected_nudge_types']})")
        
        if "expected_nudge_actions" in scenario:
            nudge_actions = [nudge["action"] for nudge in result["nudges"]]
            found_match = False
            for expected_action in scenario["expected_nudge_actions"]:
                for action in nudge_actions:
                    if expected_action in action:
                        found_match = True
                        break
            assert found_match, f"Expected action containing one of {scenario['expected_nudge_actions']} not found in {nudge_actions}"
            print(f"✓ Nudge actions match expected")
        
        print(f"Test scenario {i+1} passed!")

if __name__ == "__main__":
    # Make sure the server is running before running tests
    print("Make sure the FastAPI server is running on http://localhost:8000")
    print("Running tests...")
    
    test_health_endpoint()
    test_version_endpoint()
    test_analyze_engagement_endpoint()
    
    print("\nAll tests passed!")
    
    