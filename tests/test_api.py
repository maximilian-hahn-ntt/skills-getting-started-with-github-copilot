"""
Tests for the Mergington High School Activities API endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_root_redirect(client: TestClient):
    """Test that root path redirects to static/index.html"""
    response = client.get("/")
    assert response.status_code == 200
    # The redirect should be followed automatically by TestClient


def test_get_activities(client: TestClient):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    
    # Test structure of an activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_for_activity_success(client: TestClient):
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess Club/signup?email=newstudent@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    
    # Verify the participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_for_nonexistent_activity(client: TestClient):
    """Test signup for an activity that doesn't exist"""
    response = client.post(
        "/activities/Nonexistent Club/signup?email=student@mergington.edu"
    )
    assert response.status_code == 404
    
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_already_registered(client: TestClient):
    """Test signup when student is already registered"""
    response = client.post(
        "/activities/Chess Club/signup?email=michael@mergington.edu"
    )
    assert response.status_code == 400
    
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_signup_special_characters_in_activity_name(client: TestClient):
    """Test signup with special characters in activity name (URL encoding)"""
    # First add an activity with special characters for testing
    from src.app import activities
    activities["Art & Crafts Club"] = {
        "description": "Arts and crafts activities",
        "schedule": "Fridays, 2:00 PM - 4:00 PM",
        "max_participants": 15,
        "participants": []
    }
    
    response = client.post(
        "/activities/Art & Crafts Club/signup?email=artist@mergington.edu"
    )
    assert response.status_code == 200


def test_unregister_from_activity_success(client: TestClient):
    """Test successful unregistration from an activity"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "michael@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]
    
    # Verify the participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_from_nonexistent_activity(client: TestClient):
    """Test unregister from an activity that doesn't exist"""
    response = client.delete(
        "/activities/Nonexistent Club/unregister?email=student@mergington.edu"
    )
    assert response.status_code == 404
    
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_not_registered(client: TestClient):
    """Test unregister when student is not registered"""
    response = client.delete(
        "/activities/Chess Club/unregister?email=notregistered@mergington.edu"
    )
    assert response.status_code == 400
    
    data = response.json()
    assert data["detail"] == "Student is not signed up for this activity"


def test_signup_and_unregister_workflow(client: TestClient):
    """Test complete workflow of signup and then unregister"""
    email = "testworkflow@mergington.edu"
    activity = "Programming Class"
    
    # First signup
    signup_response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert signup_response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity]["participants"]
    
    # Then unregister
    unregister_response = client.delete(
        f"/activities/{activity}/unregister?email={email}"
    )
    assert unregister_response.status_code == 200
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity]["participants"]


def test_multiple_signups_different_activities(client: TestClient):
    """Test that a student can sign up for multiple different activities"""
    email = "multisport@mergington.edu"
    
    # Sign up for multiple activities
    activities = ["Chess Club", "Programming Class", "Art Club"]
    
    for activity in activities:
        response = client.post(
            f"/activities/{activity}/signup?email={email}"
        )
        assert response.status_code == 200
    
    # Verify student is in all activities
    activities_response = client.get("/activities")
    all_activities = activities_response.json()
    
    for activity in activities:
        assert email in all_activities[activity]["participants"]


def test_participant_count_limits(client: TestClient):
    """Test that participant limits are respected (though not enforced in current implementation)"""
    # Get initial participant count for Chess Club (max 12)
    activities_response = client.get("/activities")
    activities = activities_response.json()
    initial_count = len(activities["Chess Club"]["participants"])
    max_participants = activities["Chess Club"]["max_participants"]
    
    # This test documents current behavior - the API doesn't enforce limits
    # In a production system, you might want to add this validation
    assert initial_count <= max_participants


def test_email_validation_format(client: TestClient):
    """Test various email formats (basic validation via query parameter)"""
    # Valid email
    response = client.post(
        "/activities/Chess Club/signup?email=valid@mergington.edu"
    )
    assert response.status_code == 200
    
    # The FastAPI framework handles basic query parameter parsing
    # Additional email validation could be added to the endpoint if needed


def test_activity_data_structure_consistency(client: TestClient):
    """Test that all activities have consistent data structure"""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"
        
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)
        assert activity_data["max_participants"] > 0