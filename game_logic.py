class GameLogic:
    def __init__(self):
        self.clicks = 0
        self.multiplier = 1
        self.multiplier_price = 10
        self.auto_click_enabled = True

        self.boost_active = False
        self.boost_multiplier = 1  # початковий множник буста
        self.boost_price = 50  # початкова ціна буста

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