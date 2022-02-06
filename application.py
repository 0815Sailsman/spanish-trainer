from vocabulary import Vocabulary
from unit import Unit
import sys
import os
from consts import *
import random
from colorama import *
import time


class Application:
    def __init__(self):
        init(autoreset=True)
        self.modes = [
            "Vokabeln üben",
            "Units hinzufügen",
            "Units bearbeiten",
            "Beenden"
        ]

        # TODO Hier einen Modus einbauen, der nach Performance sortiert
        self.training_modes = [
            "Der Reihenfolge nach",
            "Zufällig",
            "Fehler trainieren"
        ]

        self.training_directions = [
            "Deutsch gegeben, Spanisch gefragt",
            "Spanisch gegeben, Deutsch gefragt",
            "Zufällig"
        ]

        self.welcome()
        time.sleep(1)
        self.main()

    def main(self):
        while True:
            next_mode = self.select_from_list(self.modes)
            self.execute_mode(next_mode)

    def welcome(self):
        print(Fore.RED + "*" * 10)
        print(Fore.YELLOW + "Daniels Spanisch-Trainer")
        print(Fore.RED + "*" * 10)

    def get_next_mode(self):
        return input("Zahl des gewünschten Modus eingeben:\n")

    def train(self):
        unit_names = self.get_all_units()
        selected_unit_nr = self.select_from_list(unit_names)
        if selected_unit_nr == -1:
            os.system("cls")
            self.welcome()
            return None
        selected_unit_name = unit_names[selected_unit_nr]
        selected_unit = Unit("").load(selected_unit_name)
        trainig_mode = self.select_from_list(self.training_modes)
        trainig_direction = self.select_from_list(self.training_directions)

        total = 0
        correct = 0
        training_list = selected_unit.get_all()
        training_list_indexes = [x for x in range(len(selected_unit.get_all()))]
        if trainig_mode == 1:               # Zufallsmodus -> Kopieren und Mischen
            random.shuffle(training_list_indexes)
        elif trainig_mode == 2:
            removal_storage = list()
            for index in training_list_indexes:
                # print(index)
                if training_list[index].get_last() == 1:
                    # print("Was correct last time - Removing")
                    removal_storage.append(index)
            for index in removal_storage:
                training_list_indexes.remove(index)
        
        for index in training_list_indexes:
            total += 1
            result = self.test(training_list[index], trainig_direction)
            if result == True:
                correct += 1
                # training_list[index].add_right()
                selected_unit.get_all()[index].add_right()
            else:
                # training_list[index].add_wrong()
                selected_unit.get_all()[index].add_wrong()
        print(Fore.LIGHTCYAN_EX + "Fertig! " + str(correct) + "/" + str(total) + " Rückkehr zum Hauptmenü...")
        if correct == total:
            print(Fore.GREEN + 25 * "*")
            print(Fore.GREEN + "GEIL JUUUUNGE!!! ALLES RICHTI!!! EHRE ALLA")
            print(Fore.GREEN + 25 * "*")
        selected_unit.save()
        time.sleep(2.5)
        os.system('cls')
        self.welcome()

    def add(self):
        new_unit = Unit(input("Name der neuen Unit?\n"))
        os.system("cls")
        self.welcome()
        voc_counter = 0
        while True:
            try:
                print("Added " + str(voc_counter).zfill(2) + " vocabularies so far!")
                new_unit.add(self.get_new_vocabulary())
                voc_counter += 1
            except KeyboardInterrupt:
                break
        new_unit.save()
        os.system('cls')
        self.welcome()

    def edit(self):
        unit_names = self.get_all_units()
        selected_unit_nr = self.select_from_list(unit_names)
        selected_unit_name = unit_names[selected_unit_nr]
        selected_unit = Unit("").load(selected_unit_name)
        
        for vocabulary in selected_unit.get_all():
            print(vocabulary)
            if input("Ändern?\n") in JA:
                new_vocabulary = self.get_new_vocabulary()
                position = selected_unit.get_all().index(vocabulary)
                selected_unit.get_all()[position] = new_vocabulary
        selected_unit.save()


    def quit(self):
        sys.exit(0)

    def execute_mode(self, mode_id):
        if mode_id == -1:
            return None
        elif mode_id == 0:
            self.train()
        elif mode_id == 1:
            self.add()
        elif mode_id == 2:
            self.edit()
        elif mode_id == 3:
            self.quit()
        else:
            print(Fore.RED + "Kein valider Modus!")
            time.sleep(1)

    def get_all_units(self):
        script_dir = os.path.dirname(__file__)
        files = os.listdir(script_dir + "/units/")
        return files

    def visualize_list(self, p_list):
        print("\n")
        print(Fore.RED + "*" * 10)
        print("-1 - ABORT")
        for unit in p_list:
            print(str(p_list.index(unit)).zfill(2) + " - " + unit)
            time.sleep(0.1)
        print(Fore.RED + "*" * 10)
        print("\n")

    def select_from_list(self, p_list):
        self.visualize_list(p_list)
        while True:
            choice_str = input("Zahl des gewünschten Eintrags eingeben:\n")
            try:
                choice_int = int(choice_str)
                #if choice_int < 0:
                #    raise IndexError
                p_list[choice_int]
                break
            except ValueError:
                print(Fore.RED + "Bitte Zahl eingeben!\n")
                time.sleep(1)
                continue
            except IndexError:
                print(Fore.RED + "Bitte eine Zahl der möglichen Einträge angeben!\n")
                time.sleep(1)
                continue
        os.system('cls')
        self.welcome()
        return choice_int

    def test(self, vocabulary, direction):
        if direction == 0:
            given = vocabulary.get_deu()
            missing = vocabulary.get_spa()
            question = " auf Spanisch:"
        elif direction == 1:
            given = vocabulary.get_spa()
            missing = vocabulary.get_deu()
            question = " auf Deutsch:"
        elif direction == 2:
            if random.randrange(0, 2) == 0:
                given = vocabulary.get_deu()
                missing = vocabulary.get_spa()
                question = " auf Spanisch:"
            else:
                given = vocabulary.get_spa()
                missing = vocabulary.get_deu()
                question = " auf Deutsch:"

        answer = input(given + question + "\n")

        if ";" in missing:
            possible_solutions = missing.upper().split(";")
            if answer.upper() in possible_solutions:
                result = True
                print(Fore.GREEN + "Richtig\n")
            else:
                result = False
                print(Fore.RED + "Falsch")
                print("Eine Antwort wäre " + possible_solutions[0] + " gewesen\n")
        else:
            if answer.upper() == missing.upper():
                result = True
                print(Fore.GREEN + "Richtig\n")
            else:
                result = False
                print(Fore.RED + "Falsch")
                print("Die Antwort wäre " + missing + " gewesen\n")

        # TODO save result for later usage
        time.sleep(1)
        os.system('cls')
        self.welcome()
        return result

    def get_new_vocabulary(self):
        deu = input("Deutsche Übersetzung: ")
        spa = input("Spanische Übersetzung: ")
        new_vocabulary = Vocabulary(deu, spa)
        os.system('cls')
        self.welcome()
        return new_vocabulary
