"""Tests for participant removal endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_remove_participant_success(client):
    """
    Arrange: Get a current participant from Chess Club
    Act: DELETE participant from activity
    Assert: Verify 200 status and participant removed from list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]

    # Verify participant was removed
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email not in activities[activity_name]["participants"]


def test_remove_participant_not_found(client):
    """
    Arrange: Set up email not in any activity
    Act: DELETE non-existent participant from Chess Club
    Assert: Verify 404 error with participant not found message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_remove_participant_activity_not_found(client):
    """
    Arrange: Set up invalid activity name
    Act: DELETE participant from non-existent activity
    Assert: Verify 404 error with activity not found message
    """
    # Arrange
    activity_name = "NonExistentClub"
    email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_remove_participant_response_format(client):
    """
    Arrange: Set up valid participant removal request
    Act: DELETE participant and inspect response
    Assert: Verify response contains required message field with proper formatting
    """
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already in Programming Class

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "message" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0


def test_remove_then_readd_participant(client):
    """
    Arrange: Start with participant in activity
    Act: Remove participant, then add them back
    Assert: Verify both operations succeed and state is correct
    """
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"

    # Get initial state
    initial_response = client.get(f"/activities")
    initial_participants = initial_response.json()[activity_name]["participants"]
    assert email in initial_participants

    # Act - Remove
    delete_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    assert delete_response.status_code == 200

    # Assert - Verify removed
    check_response = client.get("/activities")
    assert email not in check_response.json()[activity_name]["participants"]

    # Act - Re-add
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    assert signup_response.status_code == 200

    # Assert - Verify re-added
    final_response = client.get("/activities")
    assert email in final_response.json()[activity_name]["participants"]
