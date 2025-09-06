from locust import HttpUser, task, between
import random


class LotteryUser(HttpUser):
    wait_time = between(1, 2) # Users wait between 1 and 2 seconds between tasks
    host = "http://localhost:8000" # Assuming Django backend runs on port 8000

    def on_start(self):
        self.client.headers = {"Content-Type": "application/json"}
        self.username = "a@t.com"
        self.email = f"test@example.com"
        self.password = "@Quadrat1"
        self.access_token = None
        self.refresh_token = None
        self.register_and_login()

    def register_and_login(self):
        # # Register
        # register_data = {"username": self.username, "email": self.email, "password": self.password}
        # self.client.post("/api/v1/register/", json=register_data)

        # Login
        login_data = {"username": self.username, "password": self.password}
        response = self.client.post("/api/token/", json=login_data)
        if response.status_code == 200:
            self.access_token = response.json()["access"]
            self.refresh_token = response.json()["refresh"]
            self.client.headers = {"Authorization": f"Bearer {self.access_token}", "Content-Type": "application/json"}
        else:
            print(f"Login failed for {self.username}: {response.text}")

    @task(3)
    def get_wallet_balance(self):
        if self.access_token:
            self.client.get("/api/v1/wallet/balance/")

    @task(5)
    def place_bet(self):
        if self.access_token:
            # Assuming a game_id and draw_id exist
            # In a real scenario, you would fetch these dynamically
            bet_data = {
                "game_id": 73, # Placeholder
                "draw_id": 1, # Placeholder
                "selection": random.randint(1, 99),
                "stake": random.randint(100, 1000)
            }
            self.client.post("/api/v1/tickets/place/", json=bet_data, headers=self.client.headers)

    @task(1)
    def get_draws(self):
        if self.access_token:
            self.client.get("/api/v1/draws/draws/")

    @task(1)
    def get_tickets(self):
        if self.access_token:
            self.client.get("/api/v1/tickets/history/")

    @task(1)
    def get_payouts(self):
        if self.access_token:
            self.client.get("/api/v1/payouts/history/")
