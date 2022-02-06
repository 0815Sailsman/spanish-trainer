from bs4 import BeautifulSoup
import os
import urllib.request, urllib.error, urllib.parse
import pickle


class Verb:
    def __init__(self, infinitv):
        self.infinitiv = infinitv

        # download webpage
        self.html = self.get_html()

        # extract data and save here
        self.text_forms = self.extract_forms()

        
        self.indicativo_presente = self.text_forms[0:6]
        self.indicativo_futuro = self.text_forms[6:12]
        self.indicativo_preterito_imperfecto = self.text_forms[12:18]
        self.indicativo_perfecto_compuesto = self.text_forms[18:24]
        self.indicativo_preterito_pluscuamperfecto = self.text_forms[24:30]
        self.indicativo_preterito_anteriror = self.text_forms[30:36]
        self.indicativo_futuro_perfecto = self.text_forms[36:42]
        self.indicativo_condicional_perfecto = self.text_forms[42:48]
        self.indicativo_condicional = self.text_forms[48:54]
        self.indicativo_preterito_perfecto_simple = self.text_forms[54:60]
        self.imperativo = self.text_forms[60:65]
        self.subjuntivo_presente = self.text_forms[65:71]
        self.subjuntivo_futuro = self.text_forms[71:77]
        self.subjuntivo_preterito_imperfecto = self.text_forms[77:83]
        self.subjuntivo_preterito_pluscuamperfecto = self.text_forms[83:89]
        self.subjuntivo_futuro_perfecto = self.text_forms[89:95]
        self.subjuntivo_preterito_imperfecto_2 = self.text_forms[95:101]
        self.subjuntivo_preterito_pluscuamperfecto_2 = self.text_forms[101:107]
        self.subjuntivo_preterito_perfecto = self.text_forms[107:113]
        self.gerundio = self.text_forms[113]
        self.gerundio_compuesto = self.text_forms[114]
        self.infinitivo = self.text_forms[115]
        self.infinitivo_compuesto = self.text_forms[116]
        self.participado_pasado = self.text_forms[117]

    def get_html(self):
        url = "https://konjugator.reverso.net/konjugation-spanisch-verb-" + self.infinitiv + ".html"
        response = urllib.request.urlopen(url)
        return response.read()
        
    def extract_forms(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        raw_forms = soup.find_all(class_="verbtxt")
        text_forms = list()
        for entry in raw_forms:
            text_forms.append(entry.get_text())
        return text_forms
    
    def save(self):
        script_dir = os.path.dirname(__file__)
        rel_path = "verbs/" + self.infinitiv + ".verb"
        abs_file_path = os.path.join(script_dir, rel_path)
        pickle.dump(self, open(abs_file_path, "wb"))


def load(name):
    script_dir = os.path.dirname(__file__)
    rel_path = "verbs/" + name
    abs_file_path = os.path.join(script_dir, rel_path)
    return pickle.load(open(abs_file_path, "rb"))
