from enum import Enum
import random

MESSAGE = ("Test de alternativa simple, para cada pregunta, existe una única respuesta correcta, que aporta 0,"
         "5 puntos. Una pregunta errónea conlleva -0,25 puntos. Las preguntas sin contestar conllevan -0,05. Para la "
         "respuesta que considere correcta, traslade la letra que la identifica a la tabla situada a continuación. "
         "\\textbf{Se corregirá exclusivamente la tabla, y las marcas o señales efectuadas en el cuerpo del test no "
         "tendrán valor}.")
SUBJECT = "ASIGNATURA"
DEGREE = "GRADO"
DATE = "FECHA"
TIME = "HORA"
POINTS = "10 pts."
VARIATIONS = 10
OPTIONS = 4
QUESTIONS = []


class OPT(Enum):
    A = 0
    B = 1
    C = 2
    D = 3


class Question:
    def __init__(self, question_text):
        self.qt = question_text
        self.op = []

    def add_option(self, option_text):
        self.op.append(option_text)

    def get_answer(self):
        i = 0
        for option in self.op:
            if option[0] == '.':
                return OPT(i).name
            i += 1

    def print(self):
        print("\question " + self.qt, end='')
        print("\t\\begin{parts}")
        for option in self.op:
            if option[0] == '.':
                print("\t\t\part " + option[1:], end='')
            else:
                print("\t\t\part " + option, end='')
        print("\t\\end{parts}")
        print()

    def shuffle(self):
        random.shuffle(self.op)


def read_questions():
    file1 = open('questions.txt', 'r', encoding='utf8')
    lines = file1.readlines()

    count = 0
    for line in lines:
        if line != "\n":
            if count == 0:
                q = Question(line)
                QUESTIONS.append(q)
                count += 1
            else:
                QUESTIONS[-1].add_option(line)
                count += 1
                if count == (OPTIONS + 1):
                    count = 0


def print_document_header():
    s = ("%--------------------\n"
         "% Packages\n"
         "% -------------------\n"
         "\\documentclass[11pt,a4paper, answers]{exam}\n"
         "\\usepackage{ltablex, tabu}\n"
         "\\usepackage{tabularx}\n"
         "\\usepackage[utf8]{inputenc}\n"
         "\\usepackage[default]{lato}\n"
         "\\usepackage[T1]{fontenc}\n"
         "\\usepackage{tabto}\n"
         "\\usepackage{graphicx}\n"
         "\\usepackage[pdftex,linkcolor=black,pdfborder={0 0 0}]{hyperref}\n"
         "\\usepackage{enumitem}\n"
         "\\usepackage{ragged2e}\n"
         "\\usepackage{amsmath}\n"
         "\\usepackage[none]{hyphenat}\n"
         "\\usepackage{float}\n"
         "\\usepackage{caption}\n"
         "\\usepackage{multirow}\n"
         "\\usepackage{multicol}\n"
         "\\setlength{\columnsep}{1.25cm}\n"
         "\\usepackage{afterpage}\n\n"
         "\\newcommand\\blankpage{%\n"
         "    \\null\n"
         "    \\thispagestyle{empty}%\n"
         "    \\addtocounter{page}{-1}%\n"
         "    \\newpage}\n\n"
         "\\renewcommand{\solutiontitle}{}\n"
         "\\footer{}{\\thepage}{}\n"
         "\\pointpoints{p.}{pts.}\n"
         "\\linespread{1.2}\n\n"
         "\\usepackage[a4paper, lmargin=1.24 cm, rmargin=1.24 cm, tmargin=2.54 cm, bmargin=2.54 cm]{geometry}\n\n"
         "%-----------------------\n"
         "% Begin document\n"
         "%-----------------------\n"
         "\\begin{document}\n\n")
    return s


def print_test_header():
    s = ("\\begin{minipage}{2.25cm}\n"
         "  \\includegraphics[width=\\textwidth]{Logo.eps}\n"
         "\\end{minipage}\n"
         "\\mbox{}\hfill\n"
         "\\begin{minipage}[c]{6cm}\n"
         "    \\large\n"
         "    \\begin{flushright}\n"
         "    \\textbf{" + SUBJECT + "} \\\\\n"
         "    " + DEGREE + " \\\\\n"
         "    " + DATE + " \\\\\n"
         "    " + TIME + "\n"
         "    \\end{flushright}\n"
         "\\end{minipage}\n"
         "\\\\\n"
         "\\vspace{0.2in}\n"
         "\\\\\n"
         "\\begin{large}\n"
         "Nombre:\\\\\n"
         "Apellidos:\\\\\n"
         "DNI/NIE:\\\\\n"
         "\\end{large}\n"
         "\\justify\n"
         "\\vspace{-0.5in}\n"
         "\\section*{Test (" + POINTS + ")}\n"
         "\\noindent\\fbox{%\n"
         "    \\parbox{\\textwidth}{%\n"
         "     \\small\n"
         + MESSAGE + "\n"
         "    }%\n"
         "}\n"
         "\setcounter{page}{1}\n")

    return s

def generate_table():
    global QUESTIONS

    header = ""
    body = ""
    hh = "{ |"
    for i in range (1,len(QUESTIONS)):
        header = header + "\\textbf{" + str(i) + "} &"
        body = body + " & "
        hh = hh + " c | "
    header = header + "\\textbf{" + str(len(QUESTIONS)) + "} \\\\ \n"
    body = body + "\\\\ \n"
    hh = hh + " c | } \n"

    s = ("\\begin{table}[h] \n"
        "\\centering \n"
        "\\begin{tabular} \n"
        + hh +
        "\\hline \n"
        + header +
        "\\hline \n"
        + body +
        "\\hline \n"
        "\\end{tabular} \n"
        "\\end{table} \n")
    return s

def generate_table_solutions(answers):
    global QUESTIONS

    header = ""
    body = ""
    hh = "{ |"
    for i in range (1,len(QUESTIONS)):
        header = header + "\\textbf{" + str(i) + "} &"
        body = body + answers[i-1] + " & "
        hh = hh + " c | "
    header = header + "\\textbf{" + str(len(QUESTIONS)) + "} \\\\ \n"
    body = body + answers[len(QUESTIONS)-1] + " \\\\ \n"
    hh = hh + " c | } \n"

    s = ("\\centering \n"
        "\\begin{tabular} \n"
        + hh +
        "\\hline \n"
        + header +
        "\\hline \n"
        + body +
        "\\hline \n"
        "\\end{tabular} \n")
    return s

def main():
    global VARIATIONS
    types = []
    i = 0

    read_questions()

    print(print_document_header())

    if len(QUESTIONS) < VARIATIONS:
        VARIATIONS = len(QUESTIONS)

    while len(types) < VARIATIONS:

        if i > 0:
            print("\\newpage")
        i = i + 1
        print("%-------------------------------------------")
        print("%\t VARIACIÓN " + str(i))
        print("%-------------------------------------------")
        print(print_test_header())
        print("\n")
        print(generate_table())

        while True:
            for q in QUESTIONS:
                q.shuffle()
            random.shuffle(QUESTIONS)

            if QUESTIONS[0].qt not in types:
                types.append(QUESTIONS[0].qt)
                break

        answers = []
        for q in QUESTIONS:
            answers.append(q.get_answer())

        print("\\begin{questions}")
        print("\t\\begin{solution}")
        # for a in answers:
        #     print(a, end=" & ")
        # print("\n")
        print(generate_table_solutions(answers))
        print("\t\end{solution}")
        print("\\begin{multicols}{2}")
        print("\\small")

        for q in QUESTIONS:
            q.print()

        print("\\end{multicols}")
        print("\\end{questions}")
        print("%-------------------------------------------")

    print("\n")
    print("\\end{document}")


if __name__ == "__main__":
    main()
