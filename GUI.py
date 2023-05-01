import note
import note_base
import customtkinter
import tkinter
import generator

global app
global destroing_add_link_window
global button_frame
global button_and_tag_frame
global find_button_frame
global menu_frame
global find_menu_frame
global type_and_find_menu_frame
global text_frame
global links_frame
generation = generator.Generation()
# #объект заметки, с которой идет работа прямо сейчас
current_note = note.note(None,None,None,None,None,None,None,None,None)
#объект базы заметок, с которым происходит работа
current_db = note_base.note_base('note_organization_base.db')

#определить цвета как глобальные переменные!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

class ButtonAndTagButtonForFrame():
    def __init__(self, index, master, text, tag_or_note):
        self.__index = index
        self.__tag_or_note = tag_or_note
        self.__text = text

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
        global menu_frame
        menu_frame.button_add_call()
        global generation
        global current_note
        global current_db
        global text_frame
        text_frame.clean_box()
        str_for_gen = ""
        data_to_update = []
        if(self.__tag_or_note=="note"):
            current_note = current_db.open_note(self.__index)
            note_title = current_note.get_note_title()
            data_to_update.append("Создано NOA на основе заметки с темой: '" + note_title + "'")
            str_for_gen = current_note.get_the_main_text_of_the_note()
            if(len(str_for_gen)>500):
                str_for_gen = str_for_gen[0:500]
        if (self.__tag_or_note == "tag"):
            data_to_update.append("Создано NOA на основе тега: '" + current_db.return_tag_by_id((self.__index,))[0] + "'")
            result_tag_text = current_db.get_txts_by_tag(str(self.__index))
            if(len(result_tag_text)>0):
                for result in result_tag_text:
                    if(len(str_for_gen)<500):
                        str_for_gen+=result
                if(len(str_for_gen)>500):
                    str_for_gen = str_for_gen[0:500]
            else:
                str_for_gen = self.__text
        result_str = generation.generate(str_for_gen)
        data_to_update.append(result_str)
        current_note.change_object(data_to_update)
        text_frame.update_data_in_text_box(current_note)

class ButtonAndTagFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):

        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.buttons = []

    def update_buttons(self, tag_or_note):
        global current_db
        if (len(self.buttons)>0):
            for button in self.buttons:
                button.button.destroy()
            self.buttons.clear()
        if(tag_or_note=="tag"):
            tags = current_db.get_the_list_of_tags()
            if(tags!=None):
                for tag in tags:
                    self.buttons.append(ButtonAndTagButtonForFrame(tag[0],self,tag[1], tag_or_note))
        if (tag_or_note == "note"):
            texts = current_db.execute_request("SELECT hdr, n_id FROM notes ORDER BY n_id")
            for text in texts:
                self.buttons.append(
                    ButtonAndTagButtonForFrame(text[1], self, text[0], tag_or_note ))
        row = 0
        for c in self.buttons:
            c.button.grid(row=row, column=0, padx=4, pady=4, sticky="nsew")
            row += 1

class TypeAndFindMenuFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.entry_variable = tkinter.StringVar()
        self.entry = customtkinter.CTkEntry(master=self,
                                       width=120,
                                       height=25,
                                       state = "disabled",
                                       textvariable=self.entry_variable)
        self.entry.bind(sequence='<Return>', command=self.search_accordance)
        self.entry.grid(row=0, column=0, columnspan=2, padx=4, pady=0, sticky="nsew")

        self.segemented_button = customtkinter.CTkSegmentedButton(master=self,
                                                             values=["По тегу", "По открытой заметке", "По теме"],
                                                             command=self.segmented_button_callback)
        self.segemented_button.set("")  # set initial value
        self.segemented_button.grid(row=1, column=0, columnspan=2, padx=4, pady=4, sticky="nsew")

    def segmented_button_callback(self, value):
        global current_note
        global menu_frame
        global button_and_tag_frame
        menu_frame.button_add_call()
        if(value=="По тегу"):
            self.entry.configure(state="disabled")
            button_and_tag_frame.update_buttons("tag")
        if(value=="По открытой заметке"):
            self.entry.configure(state="disabled")
            button_and_tag_frame.update_buttons("note")
        if(value=="По теме"):
            self.entry.configure(state="normal")
        print(value)

    def search_accordance(self, *args):
        global menu_frame
        global text_frame
        menu_frame.button_add_call()
        text_frame.clean_box()
        global current_db
        global find_button_frame
        global generation
        global current_note
        str_for_generate = self.entry_variable.get()
        data_to_update = []
        data_to_update.append("Создано NOA на основе темы: '" + str_for_generate + "'")

        # Возможно в этом месте поискать что-то в заметках пользователя
        # и наверное стоит добавить многопоточность

        result_str = generation.generate(str_for_generate)
        data_to_update.append(result_str)
        current_note.change_object(data_to_update)
        text_frame.update_data_in_text_box(current_note)

        print(result_str)

class FindButtonForButtonFrame():
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
        global menu_frame
        menu_frame.button_add_call()

        global current_note
        global current_db
        global text_frame
        text_frame.clean_box()
        current_note = current_db.open_note(self.__index)
        text_frame.update_data_in_text_box(current_note)

class FindButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs, ):

        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.buttons = []
        header_and_id_list = []
        self.update_buttons(header_and_id_list)

    def update_buttons(self, header_and_id_list):
        if (len(self.buttons)>0):
            for button in self.buttons:
                button.button.destroy()
            self.buttons.clear()
        if(len(header_and_id_list)>0):
            exist_flag = False
            exist_ids = []
            for header_and_id in header_and_id_list:
                for exist_id in exist_ids:
                    if(header_and_id[1]==exist_id):
                        exist_flag = True
                        break
                if(exist_flag==False):
                    self.buttons.append(
                        FindButtonForButtonFrame(header_and_id[1], self, header_and_id[0]))
                exist_flag = False
                exist_ids.append(header_and_id[1])
            row = 0
            for c in self.buttons:
                c.button.grid(row=row, column=0, padx=4, pady=4, sticky="nsew")
                row += 1

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
                                                             command=self.segmented_button_callback,
                                                             height=25)
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
                if(button_frame!=None):
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
            if (button_frame != None):
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

class FindMenuFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.entry_variable = tkinter.StringVar()
        self.entry = customtkinter.CTkEntry(master=self,
                                       width=120,
                                       height=25,
                                       textvariable=self.entry_variable)
        self.entry.bind(sequence='<Return>', command=self.search_accordance)
        self.entry.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")

    def search_accordance(self, *args):
        global current_db
        global find_button_frame
        str_for_search = self.entry_variable.get()
        headers_and_id_list = current_db.find_accordance_in_db(str_for_search)
        find_button_frame.update_buttons(headers_and_id_list)
        print(self.entry_variable.get())

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


    def segmented_button_callback(self, value):
        global app
        global menu_frame
        global find_menu_frame
        if(value=="Главная"):
             # возможно здесь сделать просто save, чтобы состояние объекта сохранилось  и при переходе
                                         # к главной вкладке можно было бы просто продолжить редактирование
            app.change_button_frame(value)
            app.change_menu_frame(value)
            menu_frame.button_add_call()

        if (value == "Поиск"):

            app.change_button_frame(value)
            app.change_menu_frame(value)
            menu_frame.button_add_call()

        if (value == "Генерация"):
            app.change_button_frame(value)
            app.change_menu_frame(value)
            menu_frame.button_add_call()
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

    def change_button_frame(self, initialize_type):
        self.my_button_frame.destroy()
        self.initialize_button_frame(initialize_type)
        self.my_button_frame.grid(row=2, column=0, padx=4, pady=4, sticky="nsew")

    def initialize_button_frame(self, initialize_type):
        global button_frame
        global find_button_frame
        global button_and_tag_frame

        if(initialize_type=="Главная"):
            button_frame = ButtonFrame(master=self, width=0, height=0)
            self.my_button_frame = button_frame

        if(initialize_type=="Поиск"):
            find_button_frame = FindButtonFrame(master=self, width=0, height=0)
            self.my_button_frame = find_button_frame

        if (initialize_type == "Генерация"):
            button_and_tag_frame = ButtonAndTagFrame(master=self, width=0, height=0)
            self.my_button_frame = button_and_tag_frame


    def change_menu_frame(self, initialize_type):

        self.my_menu_frame.destroy()
        self.initialize_menu_frame(initialize_type)
        self.my_menu_frame.grid(row=1, column=0, columnspan=2, padx=4, pady=4, sticky="nsew")

    def initialize_menu_frame(self, initialize_type):
        global menu_frame
        global find_menu_frame
        global type_and_find_menu_frame

        if(initialize_type=="Главная"):
            menu_frame = MenuFrame( master=self, width=100, height=40)
            self.my_menu_frame = menu_frame

        if(initialize_type=="Поиск"):
            find_menu_frame = FindMenuFrame(master=self, width=100, height=40)
            self.my_menu_frame = find_menu_frame

        if (initialize_type == "Генерация"):
            type_and_find_menu_frame = TypeAndFindMenuFrame(master=self, width=100, height=40)
            self.my_menu_frame = type_and_find_menu_frame



if __name__ == "__main__":
    global app
    app = App()
    app.mainloop()

