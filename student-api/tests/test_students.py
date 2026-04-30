# Test suite for Student API endpoints


def test_create_student(client):
    # Test successful student creation
    payload = {"name": "John Doe", "age": 21}

    response = client.post("/api/v1/students", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "John Doe"
    assert data["age"] == 21
    assert "id" in data


def test_get_students(client):
    # Test retrieving all students
    response = client.get("/api/v1/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_student_by_id(client):
    # Test retrieving a specific student by ID
    # First create
    create = client.post("/api/v1/students", json={"name": "A", "age": 20})
    student_id = create.json()["id"]

    # Then fetch
    response = client.get(f"/api/v1/students/{student_id}")

    assert response.status_code == 200
    assert response.json()["id"] == student_id


def test_get_student_not_found(client):
    # Test retrieving a non-existent student
    response = client.get("/api/v1/students/9999")

    assert response.status_code == 404


def test_update_student(client):
    # Test successful student update
    create = client.post("/api/v1/students", json={"name": "Old", "age": 20})
    student_id = create.json()["id"]

    response = client.put(
        f"/api/v1/students/{student_id}",
        json={"name": "New", "age": 25},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "New"
    assert data["age"] == 25


def test_update_student_not_found(client):
    # Test updating a non-existent student
    response = client.put(
        "/api/v1/students/9999",
        json={"name": "X", "age": 30},
    )

    assert response.status_code == 404


def test_delete_student(client):
    # Test successful student deletion
    create = client.post("/api/v1/students", json={"name": "Temp", "age": 22})
    student_id = create.json()["id"]

    response = client.delete(f"/api/v1/students/{student_id}")

    assert response.status_code == 204


def test_delete_student_not_found(client):
    # Test deleting a non-existent student
    response = client.delete("/api/v1/students/9999")

    assert response.status_code == 404
