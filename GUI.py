import note
import note_base
import customtkinter

global destroing_add_link_window
global button_frame
global menu_frame
global text_frame
global links_frame
# #объект заметки, с которой идет работа прямо сейчас
current_note = note.note(None,None,None,None,None,None,None,None,None)
#объект базы заметок, с которым происходит работа
current_db = note_base.note_base('note_organization_base.db')

#определить цвета как глобальные переменные!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class ToplevelDelLink(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("note organized app - удаление ссылки")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Выберите удаляемую ссылку")
        self.label.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

        self.button_frame = DelLinkButtonFrame(self)
        self.button_frame.grid(row=1, column=0, padx=4, pady=4, sticky="nsew")

class DelLinkButtonForLinkButtonFrame():
    def __init__(self, index, master, text):
        self.__index = index

        strlen = 58
        if (text != None):
            if (len(text) > strlen):
                out = text[0:strlen + 1] + " ..."
                text = out

        self.button = customtkinter.CTkButton(master=master, width=460, height=40, command=self.button_call,
                                              text=text, hover=True, anchor="w", fg_color="#636363")

    def button_call(self):

        deleted_link_id = getattr(self,"_DelLinkButtonForLinkButtonFrame__index")

        global current_db
        global current_note
        global text_frame
        new_links_ids = current_db.del_link_id_in_db(deleted_link_id, current_note.get_note_id(), current_note.get_the_list_of_links_to_other_splitted())
        current_note.update_list_of_links_to_other_notes(new_links_ids)
        text_frame.clean_box()
        text_frame.update_data_in_text_box(current_note)
        top_level_del_link.destroy()


class DelLinkButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs, ):

        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.buttons = []
        self.update_buttons()

    def update_buttons(self):

        global current_db
        global current_note

        texts = current_db.execute_request("SELECT hdr, n_id FROM notes ORDER BY n_id")

        list_of_links = current_note.get_the_list_of_links_to_other_splitted()

        if(len(list_of_links)>0):
            for text in texts:
                for link in list_of_links:
                    if (link != None):
                        if (text[1] == int(link)):
                            self.buttons.append(
                                DelLinkButtonForLinkButtonFrame(text[1], self, text[0]))

        row = 0
        for c in self.buttons:
            c.button.grid(row=row, column=0, padx=4, pady=4, sticky="nsew")
            row += 1

class ToplevelAddLink(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")
        self.title("note organized app - добавление ссылки")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(self, text="Выберите заметку для добавления ссылки")
        self.label.grid(row=0, column=0, padx=4, pady=4, sticky="nsew")

        self.button_frame = LinkButtonFrame(self)
        self.button_frame.grid(row=1, column=0, padx=4, pady=4, sticky="nsew")

class LinkButtonForLinkButtonFrame():
    def __init__(self, index, master, text):
        self.__index = index

        strlen = 58
        if (text != None):
            if (len(text) > strlen):
                out = text[0:strlen + 1] + " ..."
                text = out

        self.button = customtkinter.CTkButton(master=master, width=460, height=40, command=self.button_call,
                                              text=text, hover=True, anchor="w", fg_color="#636363")

    def button_call(self):
        # здесь можно просто добавить ссылку в текущий объект!!!!!

        added_link_id = getattr(self,"_LinkButtonForLinkButtonFrame__index")

        global current_db
        global current_note
        global text_frame
        new_links_ids = current_db.add_link_id_in_db(added_link_id, current_note.get_note_id())
        current_note.update_list_of_links_to_other_notes(new_links_ids)
        text_frame.clean_box()
        text_frame.update_data_in_text_box(current_note)
        top_level_add_link.destroy()



class LinkButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs, ):

        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.buttons = []
        self.update_buttons()

    def update_buttons(self):

        global current_db
        global current_note

        texts = current_db.execute_request("SELECT hdr, n_id FROM notes ORDER BY n_id")

        #получить номера уже имеющихся ссылок
        list_of_links = current_note.get_the_list_of_links_to_other_splitted()
        list_of_links.append(str(current_note.get_note_id()))

        uniq_id = True
        for text in texts:
            for link in list_of_links:
                if(link!=None):
                    if (text[1] == int(link)):
                        uniq_id = False
            if(uniq_id == True):
                self.buttons.append(
                    LinkButtonForLinkButtonFrame(text[1], self, text[0]))
            uniq_id = True

        row = 0
        for c in self.buttons:
            c.button.grid(row=row, column=0, padx=4, pady=4, sticky="nsew")
            row += 1





class ButtonForButtonFrame():
    def __init__(self, index, master, text):
        self.__index = index

        # вот здесь можно добавить /n и тогда заголовок будет отображаться в 2 строчки
        strlen = 58
        if(text!=None):
            if (len(text) > strlen):
                out = text[0:strlen + 1] + " ..."
                text = out

        self.button = customtkinter.CTkButton(master=master, width=460, height=40, command=self.button_call,
                                                  text=text, hover=True, anchor="w", fg_color="#636363")

    def button_call(self):
        print(self.__index)
        # здесь убить процесс, который был до этого запущен (если был запущен) и создать новый с отслеживанием изменений
        # в файле????

        #НАЖАТИЕ НА КНОПКУ ПРОВОЦИРУЕТ И СОХРАНЕНИЕ СОСТОЯНИЯ ТЕКУЩЕГО ОБЪЕКТА, ЕСЛИ ОН НЕ ПУСТ
        # состояния текст боксов и объекта:
        # пустые текст боксы и пустой объект
        # в текст боксы что-то написали, объект пустой
        # текстбокс не пустой, объект тоже не пустой
        # при нажатии на кнопку я ожидаю что: если текстбоксы не пустые и объект пуст - записать новую заметку
        global menu_frame
        menu_frame.button_add_call()

        global current_note
        global current_db
        global text_frame
        text_frame.clean_box()
        current_note = current_db.open_note(self.__index)
        text_frame.update_data_in_text_box(current_note)

    def get_index(self):
        return getattr(self, "_ButtonForButtonFrame__index")

class ButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs, ):

        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.buttons = []
        self.update_buttons()

    def update_buttons(self):

        for button in self.buttons:
            button.button.destroy()

        global current_db
        texts = current_db.execute_request("SELECT hdr FROM notes ORDER BY n_id")

        self.buttons.clear()

        sequense_number = 0;
        for text in texts:
            self.buttons.append(
                ButtonForButtonFrame(sequense_number, self, text[0]))
            sequense_number += 1

        row = 0
        for c in self.buttons:
            c.button.grid(row=row, column=0, padx=4, pady=4, sticky="nsew")
            row += 1


class LinksFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.buttons = []
        self.update_links_buttons()
    def update_links_buttons(self):
        for button in self.buttons:
            button.button.destroy()

        global current_db
        global current_note
        if((current_note.get_the_list_of_links_to_other_notes()!=None)
                |(current_note.get_the_list_of_links_to_other_notes()!="")):
            links = current_db.get_list_of_links_id(current_note.get_the_list_of_links_to_other_notes())

        self.buttons.clear()

        if(links!=None):
            for link in links:
                self.buttons.append(
                    ButtonForButtonFrame(link[1], self, link[0]))
                    # Button_For_ButtonFrame(link[1], self, link[0]))

        row = 0
        for c in self.buttons:
            c.button.grid(row=row, column=1, padx=4, pady=4, sticky="nsew")
            row += 1

    def delete(self):
        self.update_links_buttons()

    def get(self):
        return_str = ""
        for button in self.buttons:
            return_str+=button.get_index()
            return_str+="|"
        return return_str

class TextFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        sticky = "nsew"

        # в целом можно сделать массив и обращаться по индексам, будет меньше кода, но, возможно, пострадает восприятие
        width = 650
        self.header = customtkinter.CTkTextbox(master=self, width=width, height=30)
        self.header.grid(row=0, column=0, padx=4, pady=(4, 4), sticky=sticky)
        # self.header.insert("0.0", "hello")
        self.header.focus_set()

        self.main_text = customtkinter.CTkTextbox(master=self, width=width, height=210)
        self.main_text.grid(row=1, column=0,  padx=4, pady=(4, 4), sticky=sticky)

        global links_frame
        links_frame = LinksFrame(self, width=650, height=60)
        self.links_frame = links_frame
        self.links_frame.grid(row=2, column=0, padx=4, pady=(4, 4), sticky=sticky)

        # для ссылок - фрейм с открытием по кнопке заметки
        # фрейм фиксированный и количество кнопок диначмически изменяется на основе запроса
        # self.links = customtkinter.CTkTextbox(master=self, width=width, height=60)
        # self.links.grid(row=3, column=0, padx=4, pady=(4, 4), sticky=sticky)

        # массив пояснений????7?
        self.links_creation_explanation = customtkinter.CTkTextbox(master=self, width=width, height=60)
        self.links_creation_explanation.grid(row=4, column=0, padx=4, pady=(4, 4), sticky=sticky)

        # для тегов - фрейм с открытием по кнопке заметки
        self.tags = customtkinter.CTkTextbox(master=self, width=width, height=30)
        self.tags.grid(row=5, column=0, padx=4, pady=(4, 4), sticky=sticky)

        # создавать динамически нужное количество полей для источников, доавить кнопку + для добавления еще одного поля
        self.sources = customtkinter.CTkTextbox(master=self, width=width, height=60)
        self.sources.grid(row=6, column=0, padx=4, pady=(4, 4), sticky=sticky)

        self.excerpts = customtkinter.CTkTextbox(master=self, width=width,height=60)
        self.excerpts.grid(row=7, column=0, padx=4, pady=(4, 4), sticky=sticky)

    def clean_box(self):
        self.header.delete("0.0", "end")
        self.main_text.delete("0.0", "end")
        self.links_frame.delete()
        self.links_creation_explanation.delete("0.0", "end")
        self.tags.delete("0.0", "end")
        self.sources.delete("0.0", "end")
        self.excerpts.delete("0.0", "end")

    def if_textbox_is_empty(self):
        strs_in_tb = []
        strs_in_tb.append(self.header.get("0.0", "end"))
        strs_in_tb.append(self.main_text.get("0.0", "end"))
        strs_in_tb.append(self.links_frame.get())
        strs_in_tb.append(self.links_creation_explanation.get("0.0", "end"))
        strs_in_tb.append(self.tags.get("0.0", "end"))
        strs_in_tb.append(self.sources.get("0.0", "end"))
        strs_in_tb.append(self.excerpts.get("0.0", "end"))
        for str in strs_in_tb:
            if((str != '\n')&(str!="")):
                return False
        return True

    def return_data_for_note_obj(self):
        global current_db
        strs_in_tb = []
        str = self.header.get("0.0", "end")
        strs_in_tb.append(str[0:len(str)-1])
        str = self.main_text.get("0.0", "end")
        strs_in_tb.append(str[0:len(str)-1])
        str = self.links_frame.get()
        strs_in_tb.append(str)
        str = self.links_creation_explanation.get("0.0", "end")
        strs_in_tb.append(str[0:len(str)-1])
        str = self.tags.get("0.0", "end")
        strs_in_tb.append(current_db.return_ids_str_by_tags(str[0:len(str)-1]))
        #сформировать строку через notebase
        str = self.sources.get("0.0", "end")
        strs_in_tb.append(str[0:len(str)-1])
        str = self.excerpts.get("0.0", "end")
        strs_in_tb.append(str[0:len(str)-1])
        i = 0
        for str in strs_in_tb:
            if(str!=None):
                if (len(str) == 0):
                    strs_in_tb[i] = None
            i+=1
        return strs_in_tb

    def update_data_in_text_box(self, note_object = note):
        global current_db

        if (note_object.get_note_title() != None):
            text_frame.header.insert("0.0", note_object.get_note_title())

        if (note_object.get_the_main_text_of_the_note() != None):
            text_frame.main_text.insert("0.0", note_object.get_the_main_text_of_the_note())

        if (note_object.get_the_list_of_links_to_other_notes() != None):
            global links_frame
            links_frame.update_links_buttons()

        if(note_object.get_explanation_of_creating_a_link_to_other_notes()!= None):
            text_frame.links_creation_explanation.insert("0.0", note_object.get_explanation_of_creating_a_link_to_other_notes())

        # из строки идентификаторов тегов базы данных получить строку с тегами в текстовом формате!!!!!
        list_of_note_tag = note_object.get_list_of_note_tag(current_db)
        if(list_of_note_tag!= None):
            text_frame.tags.insert("0.0", list_of_note_tag)

        if(note_object.get_list_of_note_sources()!= None):
            text_frame.sources.insert("0.0", note_object.get_list_of_note_sources())

        if(note_object.get_excerpt_from_the_source_for_clarification()!= None):
            text_frame.excerpts.insert("0.0", note_object.get_excerpt_from_the_source_for_clarification())



class MenuFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.segemented_button = customtkinter.CTkSegmentedButton(master=self,
                                                             values=["Удалить заметку", "Добавить заметку", "Удалить ссылку", "Добавить ссылку"],
                                                             command=self.segmented_button_callback)
        self.segemented_button.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")


        self.top_level_add_link = None
        self.top_level_del_link = None

    def segmented_button_callback(self,value):
        if(value=="Удалить заметку"):
            self.button_del_call()
        if(value=="Добавить заметку"):
            self.button_add_call()
        if(value=="Удалить ссылку"):
            self.button_del_link_call()
        if (value == "Добавить ссылку"):
            self.button_add_link_call()
        print("segmented button clicked:", value)
        self.segemented_button.set("")

    def button_del_link_call(self):
        self.save_object_value()
        if self.top_level_add_link is None or not self.top_level_add_link.winfo_exists():
            global top_level_del_link
            top_level_del_link  = ToplevelDelLink(self) #поменять!!!!!!!!!!!!!!
            self.top_level_del_link = top_level_del_link # create window if its None or destroyed
            self.top_level_del_link.focus()
        else:
            self.top_level_add_link.focus()  # if window exists focus it
        self.save_object_value()

    def button_add_link_call(self):
        # не забыть сохранить состояние объектов!!!!!!!!!!!1
        self.save_object_value()
        if self.top_level_add_link is None or not self.top_level_add_link.winfo_exists():
            global top_level_add_link
            top_level_add_link  = ToplevelAddLink(self)
            self.top_level_add_link = top_level_add_link # create window if its None or destroyed
            self.top_level_add_link.focus()
        else:
            self.top_level_add_link.focus()  # if window exists focus it
        self.save_object_value()

    def button_del_call(self):
        # если будет время - сделать окно подтверждения действия
        global current_note
        global current_db
        global text_frame
        global button_frame
        global links_frame
        if(current_note.if_object_empty()==False):
            current_db.delete_note(getattr(current_note, "_note__note_identifier"))
            text_frame.clean_box()
            button_frame.update_buttons()
            current_note.clean_object()
            links_frame.update_links_buttons()
        else:
            if(text_frame.if_textbox_is_empty()==False):
                text_frame.clean_box()
        print("Deleted")

    def save_object_value(self):
        global current_note
        global current_db
        global text_frame
        global button_frame
        global links_frame
        #возможно перенести часть функционала в класс note?
        if(current_note.if_object_empty()==True):
            if(text_frame.if_textbox_is_empty()==False):
                data_to_change = text_frame.return_data_for_note_obj()
                data_to_change.append(current_db.get_free_note_id_from_note_base())
                data_to_change.append("txt")
                current_note.change_object(data_to_change)
                current_db.add_note(current_note)
                button_frame.update_buttons()
                links_frame.update_links_buttons()
        else:
            data_to_change = text_frame.return_data_for_note_obj()
            data_to_change.append(current_note.get_note_id())
            data_to_change.append("txt")
            current_note.change_object(data_to_change)
            current_db.add_note(current_note)
            button_frame.update_buttons()
            links_frame.update_links_buttons()

    def button_add_call(self):
        global current_note
        global current_db
        global text_frame
        global button_frame
        global links_frame
        #возможно перенести часть функционала в класс note?
        if(current_note.if_object_empty()==True):
            if(text_frame.if_textbox_is_empty()==False):
                data_to_change = text_frame.return_data_for_note_obj()
                data_to_change.append(current_db.get_free_note_id_from_note_base())
                data_to_change.append("txt")
                current_note.change_object(data_to_change)
                current_db.add_note(current_note)
                button_frame.update_buttons()
                links_frame.update_links_buttons()
        else:
            data_to_change = text_frame.return_data_for_note_obj()
            data_to_change.append(current_note.get_note_id())
            data_to_change.append("txt")
            current_note.change_object(data_to_change)
            current_db.add_note(current_note)
            current_note.clean_object()  # кажется, вот эта строка мне мешает слегка
            text_frame.clean_box()
            button_frame.update_buttons()
            links_frame.update_links_buttons()

        # кнопка работает когда приложение только что открыли или удалили заметку (т.е. объект заметки пустой)
        # в этом случае нажатие на кнопку провоцирует:
        # проверка наличия текста в текстбоксах
        # если хоть где-то текст есть:
        # заполнение полей объекта текущей заметки
        # получение свободного id
        # запись в базу заметок
        # обновить кнопки
        # в противном случае ничего не происходит

        # или когда была открыта какая-то заметка (т.е. объект заметки не пуст)
        # в этом случае нажатие на кнопку провоцирует:
        # выбрать данные из текстбоксов, так как возможно данные изменились
        # сравнение текущего объекта и записи в базе данных (или просто запись по умолчанию, если что, потом поменяю)
        # если есть изменения - записать объект в базу и очистить текущий объект, очистить текстбоксы, обновить кнопки.
        print("Add")



class WindowFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.segemented_button = customtkinter.CTkSegmentedButton(master=self,
                                                             values=["Главная", "Поиск", "Генерация"],
                                                             command=self.segmented_button_callback)
        self.segemented_button.set("Главная")  # set initial value
        self.segemented_button.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")

    def segmented_button_callback(value):
        print("segmented button clicked:", value)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_appearance_mode("dark")

        self.geometry("1000x600")
        self.title("note organized app")
        self.minsize(300, 200)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.window_frame = WindowFrame(master=self, width=100, height=40)
        self.window_frame.grid(row=0,column=0,columnspan=2, padx=4, pady=4, sticky="nsew")

        global menu_frame
        menu_frame = MenuFrame(master=self, width=100, height=40)
        self.my_menu_frame = menu_frame
        self.my_menu_frame.grid(row=1, column=0, columnspan=2, padx=4, pady=4, sticky="nsew")

        global text_frame
        text_frame = TextFrame(master=self, width=0, height=0)
        self.my_text_frame = text_frame
        self.my_text_frame.grid(row=2, column=1, padx=4, pady=4, sticky="nsew")

        global button_frame
        button_frame = ButtonFrame(master=self, width=0, height=0)
        self.my_button_frame = button_frame
        self.my_button_frame.grid(row=2, column=0, padx=4, pady=4, sticky="nsew")


if __name__ == "__main__":
    app = App()
    app.mainloop()

