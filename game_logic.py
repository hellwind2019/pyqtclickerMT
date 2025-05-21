import requests
from PyQt5.QtCore import QTimer


class GameLogic:
    def __init__(self):
        self.user_id = None
        self.init_default_values()

        self.save_timer = QTimer()
        self.save_timer.timeout.connect(self.save_state)
        self.save_timer.setInterval(10000)  # 10 seconds

    def init_default_values(self):
        self.clicks = 0
        self.multiplier = 1
        self.multiplier_price = 10
        self.auto_click_enabled = True
        self.boost_active = False
        self.boost_multiplier = 1
        self.boost_price = 50
        self.auto_click_price = 100

    def load_user_state(self, user_id):
        """Load user state from database"""
        self.user_id = user_id
        try:
            response = requests.get(f"http://localhost:8000/user/{user_id}/state")
            if response.status_code == 200:
                state = response.json()
                self.clicks = state['score']
                self.multiplier = state['multiplier']
                self.multiplier_price = state['multiplier_price']
                self.boost_multiplier = state['boost_multiplier']
                self.boost_price = state['boost_price']
                self.boost_active = state['boost_active']
                self.auto_click_enabled = state['auto_click']
                self.auto_click_price = state['auto_click_price']

                # Start auto-saving
                self.save_timer.start()
                return True
        except requests.RequestException:
            print("Failed to load user state")
        return False

    def save_state(self):
        """Save current state to database"""
        if not self.user_id:
            return

        try:
            state = {
                "score": self.clicks,
                "multiplier": self.multiplier,
                "multiplier_price": self.multiplier_price,
                "boost_multiplier": self.boost_multiplier,
                "boost_price": self.boost_price,
                "boost_active": self.boost_active,
                "auto_click": self.auto_click_enabled,
                "auto_click_price": self.auto_click_price
            }

            response = requests.post(
                f"http://localhost:8000/user/{self.user_id}/state",
                json=state
            )
            return response.status_code == 200
        except requests.RequestException:
            print("Failed to save user state")
            return False

    def add_click(self):
        if self.boost_active:
            self.clicks += self.multiplier * self.boost_multiplier
        else:
            self.clicks += self.multiplier

    def auto_click(self):
        if self.auto_click_enabled:
            self.clicks += self.multiplier

    def is_affordable(self, price: int) -> bool:
        return self.clicks >= price

    def buy_multiplier(self):
        if self.is_affordable(self.multiplier_price):
            self.clicks -= self.multiplier_price
            self.multiplier += 1
            self.multiplier_price *= 2
            return True
        return False

    def buy_boost_upgrade(self):
        if self.is_affordable(self.boost_price):
            self.clicks -= self.boost_price
            self.boost_multiplier += 5
            self.boost_price *= 2
            return True
        return False

    def activate_boost(self, duration_ms=5000):
        if not self.boost_active:
            self.boost_active = True