"""Tests for activity endpoints using AAA (Arrange-Act-Assert) pattern"""


def test_get_activities_success(client):
    """
    Arrange: Set up test client
    Act: Call GET /activities
    Assert: Verify status 200 and response structure
    """
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for activity_name in expected_activities:
        assert activity_name in data
        assert "description" in data[activity_name]
        assert "schedule" in data[activity_name]
        assert "max_participants" in data[activity_name]
        assert "participants" in data[activity_name]


def test_get_activities_contains_all_expected_fields(client):
    """
    Arrange: Set up test client
    Act: Call GET /activities and inspect first activity
    Assert: Verify all required fields are present
    """
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    data = response.json()
    first_activity = next(iter(data.values()))

    # Assert
    assert all(field in first_activity for field in required_fields)
    assert isinstance(first_activity["max_participants"], int)
    assert isinstance(first_activity["participants"], list)


def test_root_redirect(client):
    """
    Arrange: Set up test client
    Act: Call GET /
    Assert: Verify redirect to /static/index.html
    """
    # Arrange
    # (no setup needed)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]
