import json


class TestProject:
    def test_home(self, client):
        response = client.get("/api")
        assert response.status == "200 OK"

    def test_user_creation_full(self, client):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-secret": "password",
        }
        data = {"username": "someusername", "email": "someuser@email.com", "password": "pass"}

        response = client.post("api/users", data=json.dumps(data), headers=headers)
        assert response.status == "200 OK"

    def test_same_user_creation(self, client):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-secret": "password",
        }
        data = {"username": "someusername", "email": "someuser@email.com", "password": "pass"}

        response = client.post("api/users", data=json.dumps(data), headers=headers)
        assert response.status == "400 BAD REQUEST"

    def test_user_creation_without_x_sec(self, client):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        data = {"username": "someusername1", "email": "someuser@email.com", "password": "pass"}

        response = client.post("api/users", data=json.dumps(data), headers=headers)
        assert response.status == "400 BAD REQUEST"

    def test_user_without_username(self, client):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-secret": "password",
        }
        data = {"email": "someuser@email.com", "password": "pass"}

        response = client.post("api/users", data=json.dumps(data), headers=headers)
        assert response.status == "400 BAD REQUEST"

    def test_user_without_email(self, client):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-secret": "password",
        }
        data = {"username": "someusername2", "password": "pass"}

        response = client.post("api/users", data=json.dumps(data), headers=headers)
        assert response.status == "400 BAD REQUEST"

    def test_user_without_password(self, client):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-secret": "password",
        }
        data = {"username": "someusername2", "email": "someuser@email.com"}

        response = client.post("api/users", data=json.dumps(data), headers=headers)
        assert response.status == "400 BAD REQUEST"

    def test_users(self, client):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = client.get("api/users", headers=headers)
        assert "users" in response.json.keys()

    def retrieve_user(self, client):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        user_id = 5

        response = client.get(f"api/users/{user_id}", headers=headers)
        assert "username" in response.json.keys()

    def update_user(self, client):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        update_user_data = {"username": "someusername2", "email": "someuser@email.com", "password": "1213213"}
        user_id = 5

        response = client.put(f"api/users/{user_id}", data=json.dumps(update_user_data), headers=headers)
        assert "someusername2" in response.json.get("username")

    def delete_user(self, client):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-secret": "password",
        }
        user_id = 5

        response = client.delete(f"api/users/{user_id}", headers=headers)
        assert "user were deleted" in response.json.get("data")
