
class Porfolio:

    def __init__(self, initial_balance= 5000,commision=.01 ) -> None:

        self._initial_balance = initial_balance
        self._comission = commision
        self.reset()

    @property
    def last_move(self):
        return self._last_move

    def process(self, action, price):
        self._last_move = 0
        if action == 0 and self._coins == 0 and self._balance > 0:
                self._last_paid = (self._balance * (1-self._comission))
                self._coins = self._last_paid / price
                self._balance = 0
        elif action == 1 and self._coins > 0 and self._balance == 0:
            sell = (price * self._coins) * (1-self._comission)
            self._coins = 0
            self._last_move = sell - self._last_paid
            if sell <= self._initial_balance:
                self._balance = sell
            else:
                self._balance = self._initial_balance
            


                

    def reset(self):
        self._balance = self._initial_balance
        self._sum = 0
        self._coins = 0
        self._last_move = 0
        self._last_paid = 0