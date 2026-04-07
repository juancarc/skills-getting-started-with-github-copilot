"""Tests for signup endpoint using AAA (Arrange-Act-Assert) pattern"""


def test_signup_success(client):
    """
    Arrange: Set up test data for signup to available activity
    Act: POST signup for Basketball Team
    Assert: Verify 200 status and participant added to activity
    """
    # Arrange
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]

    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]


def test_signup_duplicate_email(client):
    """
    Arrange: Use an email already signed up for Chess Club
    Act: POST signup for Chess Club with duplicate email
    Assert: Verify 400 error with descriptive message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found(client):
    """
    Arrange: Set up invalid activity name
    Act: POST signup for non-existent activity
    Assert: Verify 404 error with activity not found message
    """
    # Arrange
    activity_name = "NonExistentClub"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_signup_response_format(client):
    """
    Arrange: Set up valid signup request
    Act: POST signup and inspect response
    Assert: Verify response contains required message field with proper formatting
    """
    # Arrange
    activity_name = "Soccer Club"
    email = "player@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    data = response.json()

    # Assert
    assert "message" in data
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0
