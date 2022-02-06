class Vocabulary:
    def __init__(self, deu, spa):
        self.deu = deu
        self.spa = spa
        self.correct_counter = 0
        self.incorrect_counter = 0
        self.last = 0

    def __repr__(self):
        return self.deu + " ist auf Spanisch " + self.spa

    def get_deu(self):
        return self.deu

    def set_deu(self, new_deu):
        self.deu = new_deu

    def get_spa(self):
        return self.spa

    def set_spa(self, new_spa):
        self.spa = new_spa

    def get_right(self):
        return self.correct_counter

    def add_right(self):
        self.correct_counter += 1
        self.last = 1

    def get_wrong(self):
        return self.incorrect_counter

    def add_wrong(self):
        self.incorrect_counter += 1
        self.last = 0

    def get_last(self):
        return self.last
