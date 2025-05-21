class GameLogic:
    def __init__(self):
        self.clicks = 0
        self.multiplier = 1
        self.multiplier_price = 10
        self.auto_click_enabled = True

    def add_click(self):
        self.clicks += self.multiplier

    def auto_click(self):
        if self.auto_click_enabled:
            self.add_click()

    def is_affordable(self, price: int) -> bool:
        return self.clicks >= price

    def buy_multiplier(self):
        if self.is_affordable(self.multiplier_price):
            self.clicks -= self.multiplier_price
            self.multiplier += 1
            self.multiplier_price *= 2
            return True
        return False
