import random
import json
from locust import HttpUser, between, task, TaskSet

from fake_data import NewLogbook, LoadedPilot


class MyTasks(TaskSet):

    @task
    def user_functions(self):
        self.client.get("pilot/id")
        # self.client.get("logbook/pilot/")

    @task
    def post_logbook(self):
        count = 0
        max_items = random.randint(4, 9)
        while count < max_items:
            logbook = NewLogbook().__dict__
            data = json.dumps(logbook, indent=4)
            response = self.client.post("logbook/new", data)
            if response.status_code == 201:
                count += 1


# class ApiUserKnown(HttpUser):
#     wait_time = between(1, 5)
#     host = 'http://127.0.0.1:8000/'
#
#     def on_start(self):
#         token = self.client.post("login",
#                                  {
#                                      "username": "bob@bob.com",
#                                      "password": "12345"
#                                  })
#         data = token.json()
#         self.client.headers = {
#         "Authorization": f"Bearer {data.get('access_token')}"
#         }
#
#     tasks = {MyTasks}


class ApiUserLoaded(HttpUser):
    wait_time = between(1, 5)
    host = 'http://127.0.0.1:8000/'

    def on_start(self):
        new_user = LoadedPilot().__dict__
        self.client.post("pilot/new", json=new_user)

        token = self.client.post('login', {
            "username": str(new_user.get('email')),
            "password": str(new_user.get('password'))
        })

        data = token.json()
        self.client.headers = {
            "Authorization": f"Bearer {data['access_token']}"
        }

    tasks = {MyTasks}
