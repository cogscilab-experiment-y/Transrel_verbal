class Pair:
    def __init__(self, first_stimulus: str, symbol: str, second_stimulus: str, stimulus_type_dict: dict):
        self.first_stimulus = first_stimulus
        self.symbol = symbol
        self.second_stimulus = second_stimulus
        self.stimulus_type_dict = stimulus_type_dict

    def reverse_symbol(self):
        self.symbol = self.stimulus_type_dict["lower"] if self.symbol == self.stimulus_type_dict["higher"] else self.stimulus_type_dict["higher"]

    def reverse_stimulus(self):
        self.first_stimulus, self.second_stimulus = self.second_stimulus, self.first_stimulus

    def reverse_pair(self):
        self.reverse_stimulus()
        self.reverse_symbol()

    def __repr__(self):
        return f"{self.first_stimulus} {self.symbol} {self.second_stimulus}"
