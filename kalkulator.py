import tkinter as tk

#kolory
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"
WHITE = "#FFFFFF"
OFF_WHITE = "#F8FAFF"
LIGHT_BLUE = "#CCEDFF"

#fonty
SMALL_FONT = ("Lato", 16)
LARGE_FONT = ("Lato", 30, "bold")
DIGIT_FONT = ("Lato", 24, "bold")
DEF_FONT = ("Lato", 20)

#klasa
class Calculator:
    #init
    def __init__(self):
        #konfiguracja okna
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0, 0)
        self.window.title("Kalkulator")

        #co jest w liniach current i total
        self.total_expression = ""
        self.current_expression = ""

        #konfiguracja ramek
        self.display_frame = self.create_display_frame()
        self.buttons_frame = self.create_buttons_frame()

        #konfiguracja gridu
        self.buttons_frame.rowconfigure(0, weight=1)

        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        #labele
        self.total_label, self.label = self.create_display_labels()

        #słownik liczb
        self.digits ={
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3: (3,3),
            0:(4,2), '.':(4,1)
        }

        #metoda tworząca przyciski cyfr
        self.create_digit_buttons()

        #przypisanie znaków operacji do działań
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        #metoda tworząca przyciski operacji
        self.create_operator_buttons()

        # metoda tworząca przyciski specjalne (clear i equal)
        self.create_special_buttons()
        self.bind_keys()

    #tworzenie labeli (linii w których wykonywane są operacje matematyczne)
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=24, font=SMALL_FONT)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                                   fg=LABEL_COLOR, padx=24, font=LARGE_FONT)
        label.pack(expand=True, fill="both")

        return total_label, label

    #tworzenie ramek
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    #dodawanie do tego co jest w linii
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    #metoda tworząca przyciski cyfr
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGIT_FONT, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    #wstawianie do linii znaków operacji
    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = "" #czyszczenie
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        n=0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, font=DEF_FONT, bg=OFF_WHITE, fg=LABEL_COLOR, borderwidth=0, command=lambda x=operator: self.append_operator(x) )
            button.grid(row=n, column=4, sticky=tk.NSEW)
            n+=1

    #przycisk i metoda do czyszczenia labeli
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="CLEAR", font=DEF_FONT, bg=OFF_WHITE, fg=LABEL_COLOR, borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    #podnoszenie do kwadratu
    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", font=DEF_FONT, bg=OFF_WHITE, fg=LABEL_COLOR, borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    #pierwiastek kwadratowy
    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", font=DEF_FONT, bg=OFF_WHITE, fg=LABEL_COLOR, borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    #metoda na liczenie
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))

            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    #tworzenie przycisku =
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", font=DEF_FONT, bg=LIGHT_BLUE, fg=LABEL_COLOR, borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    #wstawianie przycisków specjalnych
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    #update'owanie labeli z działaniami
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f'{symbol}')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11]) #do 11 miejsc

    #klawiatura numeryczna
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    #uruchamianie
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()