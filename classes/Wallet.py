
class Wallet:
    def __init__(self) -> None:
        self._initial_value = 2500
        self.reset()

    def reset(self):
        self._current_euros = self._initial_value
        self._current_dollars = 0
        self._current_value = self._initial_value
        self._previous_value = self._current_value

    @property
    def current_euros(self):
        return self._current_euros
    
    @property
    def current_dollars(self):
        return self._current_dollars

    @property
    def current_value(self):
        return self._current_value

    @property
    def previous_value(self):
        return self._previous_value
    
    def step(self, action, obs):
        ask_open = obs['AO'] # prix d'achat
        bid_open = obs['BO'] # prix de vente

        match(action):
            # Achat de dollars avec euros
            case 2 :
                self._current_dollars += (self._current_euros / ask_open)
                self._current_euros = 0
                # self._current_euros % ask_open
                
            # Pas d'action
            case 0 :
                ...
            # Vente de dollars contre euros
            case 1 :
                self._current_euros += (self._current_dollars * bid_open)
                self._current_dollars = 0
                
        self._previous_value = self._current_value
        self._current_value = self._current_euros + (self._current_dollars * bid_open)




