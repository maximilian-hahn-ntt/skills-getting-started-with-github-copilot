"""
Test configuration and fixtures for FastAPI tests
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities database before each test"""
    global activities
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team with practices and games",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu", "sarah@mergington.edu"]
        },
        "Track and Field": {
            "description": "Running, jumping, and throwing events training",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["ryan@mergington.edu", "lisa@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater performances and acting workshops",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["grace@mergington.edu", "ethan@mergington.edu"]
        },
        "Art Club": {
            "description": "Painting, drawing, and creative arts projects",
            "schedule": "Fridays, 3:00 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu", "jacob@mergington.edu"]
        },
        "Science Club": {
            "description": "Science experiments, research projects, and competitions",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ava@mergington.edu", "noah@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debating and public speaking skills",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["isabella@mergington.edu", "liam@mergington.edu"]
        }
    })