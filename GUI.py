import note
import note_base
import PySimpleGUI as gui
import customtkinter

class ButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.buttons = []

        self.my_note_base = note_base.note_base('note_organization_base.db')
        texts = self.my_note_base.execute_request("SELECT hdr FROM notes")

        for text in texts:
            self.buttons.append(customtkinter.CTkButton(master=self, command=self.button_callback, text= text, hover = True, anchor="sw"))

        row = 0
        for c in self.buttons:
            c.grid(row=row, column=0, padx=4, pady=4, sticky="nsew")
            row+=1

    def button_callback(self):
        self.textbox.insert("insert", self.combobox.get() + "\n")

class TextFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = customtkinter.CTkTextbox(master=self)
        self.header.grid(row=0, column=0,  padx=20, pady=(20, 0), sticky="nsew")

        self.main_text = customtkinter.CTkTextbox(master=self)
        self.main_text.grid(row=1, column=0,  padx=20, pady=(20, 0), sticky="nsew")

        # для ссылок - фрейм с открытием по кнопке заметки
        # фрейм фиксированный и количество кнопок диначмически изменяется на основе запроса
        self.links = customtkinter.CTkTextbox(master=self)
        self.links.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="nsew")

        # создавать динамически нужное количество полей для источников, доавить кнопку + для добавления еще одного поля
        self.sources = customtkinter.CTkTextbox(master=self)
        self.sources.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="nsew")






class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x600")
        self.title("small example app")
        self.minsize(300, 200)

        # create 2x2 grid system
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.my_button_frame = ButtonFrame(master=self, width=0, height=0)
        self.my_button_frame.grid(row=0, column=0, rowspan=3, padx=4, pady=4, sticky="nsew")

        self.my_text_frame = TextFrame(master=self, width=0, height=0)
        self.my_text_frame.grid(row=0, column=1, rowspan=3, padx=4, pady=4, sticky="nsew")

        # self.textbox = customtkinter.CTkTextbox(master=self)
        # self.textbox.grid(row=0, column=1,  padx=20, pady=(20, 0), sticky="nsew")

        # self.textbox1 = customtkinter.CTkTextbox(master=self)
        # self.textbox1.grid(row=0, column=1,  padx=20, pady=(20, 0), sticky="nsew")

        # self.combobox = customtkinter.CTkComboBox(master=self, values=["Sample text 1", "Text 2"])
        # self.combobox.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # self.button = customtkinter.CTkButton(master=self, command=self.button_callback, text="Insert Text")
        # self.button.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        # self.combobox1 = customtkinter.CTkComboBox(master=self, values=["Sample text 1", "Text 2"])
        # self.combobox1.grid(row=2, column=0, padx=20, pady=10, sticky="ew")


        #добавить скролабл ФРЕЙМ
        #в скролабл фрэйме сделать много-много кнопок
        # нажатие на кнопку провоцирует передачу ID (правда как?)

        # self.buttons = []
        # self.buttons.append(customtkinter.CTkButton(master=self, command=self.button_callback, text="Insert Text"))
        # #self.button1 = customtkinter.CTkButton(master=self, command=self.button_callback, text="Insert Text")
        # self.buttons[0].grid(row=2, column=1, padx=20, pady=10, sticky="ew")



    def button_callback(self):
        self.textbox.insert("insert", self.combobox.get() + "\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()