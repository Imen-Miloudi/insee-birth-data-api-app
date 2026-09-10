import requests


class AppHandler:

    def __init__(self):
        self.url = "http://127.0.0.1:8000"

    def get_departments(self):
        response = requests.get(
            f"{self.url}/departments"
        )

        response.raise_for_status()

        return response.json()

    def get_births_by_department(self, dep):
        response = requests.get(
            f"{self.url}/births/{dep}"
        )

        response.raise_for_status()

        return response.json()

    def get_births_by_department_and_period(self, dep, period):
        response = requests.get(
            f"{self.url}/births/{dep}/{period}"
        )

        response.raise_for_status()

        return response.json()