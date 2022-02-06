from vocabulary import Vocabulary
import pickle
import os


class Unit:
    def __init__(self, name):
        self.name = name
        self.vocabularies = list()

    def __repr__(self):
        return self.name + " enthält " + str(len(self.vocabularies)) + " Vokabeln."

    def add(self, new_vocab):
        self.vocabularies.append(new_vocab)

    def get_all(self):
        return self.vocabularies

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        self.name = new_name

    def save(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "units/" + self.name + ".unit"
        abs_file_path = os.path.join(script_dir, rel_path)
        pickle.dump(self, open(abs_file_path, "wb"))

    def load(self, name):
        script_dir = os.path.dirname(__file__)
        rel_path = "units/" + name
        abs_file_path = os.path.join(script_dir, rel_path)
        return pickle.load(open(abs_file_path, "rb"))

    # ONLY FOR DEVELOPING PURPOSES
    # SHOULD NEVER BE CALLED BY NORMAL USER
    def update_vocab_objects(self):
        for old_vocab in self.vocabularies:
            position = self.vocabularies.index(old_vocab)
            new_vocab = Vocabulary(old_vocab.get_deu(), old_vocab.get_spa())
            self.vocabularies[position] = new_vocab
