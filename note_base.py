import sqlite3 as sql
import note

class note_base:


    def __init__(self,db_filename):
        self.__db_filename = db_filename
        self.open_db_connection()
        print("[note_base]: connection open")
        self.open_cursor()
        print("[note_base]: cursor created")

        # сделать id уникальным!!!!!!!! (возможно где-то еще)
        self.execute_request(
            "CREATE TABLE if not exists notes(hdr, txt, ftype, n_id INTEGER, l_id, s_id, e_id, lce_id, t_id)")
        self.execute_request("CREATE TABLE if not exists tags(tag_id, tag)")
        self.execute_request("CREATE TABLE if not exists excerpts(ex_id, ex)")
        self.execute_request("CREATE TABLE if not exists sources(src_id, src)")
        self.execute_request("CREATE TABLE if not exists recent_tags(tg_id, r_indctr)")
        self.execute_request("CREATE TABLE if not exists recently_opened_notes(nt_id, r_indctr)")
        self.execute_request("CREATE TABLE if not exists recently_used_src(src_id, r_indctr)")
        self.execute_request("CREATE TABLE if not exists favorite_notes(favorite_nt_id)")
        self.execute_request("CREATE TABLE if not exists education(ed_data)")
        self.execute_request("CREATE TABLE if not exists link_crtn_exp(nt_id, lnk_id, lce)")
        self.execute_request("CREATE TABLE if not exists undo_redo(nt_obj, nt_id, obj_vrsn)")


    def is_table_exist(self,table_name):
        # проверка наличия таблицы
        sql_table_name = self.__sql_cursor.execute("SELECT name FROM sqlite_master WHERE name='" + table_name + "'")
        if (sql_table_name.fetchone() != None):
            return True
        else:
            return False

    def execute_request(self, request):
        return self.__sql_cursor.execute(request)

    def execute_request_with_unknown_req_value(self, request, value):
        return self.__sql_cursor.execute(request, value)

    def made_commit(self):
        self.__sql_connection.commit()

    def close_cursor(self):
        self.__sql_cursor.close()

    def open_cursor(self):
        self.__sql_cursor = self.__sql_connection.cursor()

    def close_db_connection(self):
        self.__sql_connection.close()

    def open_db_connection(self):
        self.__sql_connection = sql.connect(self.__db_filename)


    def get_free_note_id_from_note_base(self):
        # сделать запрос из таблицы с проверкой наличия id
        # если id есть - узнать максимальный и присвоить free max+1
        # если id нет - свободный = 0
        request_result = self.execute_request("SELECT n_id FROM notes ORDER BY n_id DESC")
        max_request_result = request_result.fetchone()
        if (max_request_result == None):
            print("[note_base]: free id = 0")
            return 0
        else:
            print("[note_base]: free id = ["+ str(int(max_request_result[0]) + 1) + "]")
            return (int(max_request_result[0]) + 1)


    def id_correction (self, deleted_note_id):
        # ПРОВЕРКА НА СУЩЕСТВОВАНИЕ УДАЛЕННОЙ ЗАМЕТКИ???????
        # Если удалили заметку с id =0 и таблица не пустая - все значения уменьшаются на единицу
        if (deleted_note_id == 0):
            request_result = self.execute_request("SELECT n_id FROM notes ORDER BY n_id DESC")
            max_request_result = request_result.fetchone()
            if (max_request_result != None):
                self.execute_request("UPDATE notes SET n_id=n_id-1")
        # Иначе, если удалили заметку с id !=0 и !=Max, то значения с id> удаленного_id уменьшаются на единицу
        else:
            if (deleted_note_id != self.get_free_note_id_from_note_base()):
                if (deleted_note_id != 0):
                    self.execute_request_with_unknown_req_value("UPDATE notes SET n_id=n_id-1 WHERE n_id>?",
                                                                (str(deleted_note_id),))
        self.made_commit()
        print("[note_base]: id corrected")


    def delete_note(self, deleted_note_id):
        self.execute_request_with_unknown_req_value("DELETE FROM notes WHERE n_id=?",(str(deleted_note_id), ))
        self.made_commit()
        print("[note_base]: deleted note with id = " + str(deleted_note_id) )
        self.id_correction(deleted_note_id)


    def open_note(self, desired_note_id):
        request_result = self.execute_request_with_unknown_req_value("SELECT * FROM notes WHERE n_id=?",
                                                                     (str(desired_note_id),))
        the_note_str = request_result.fetchone() #ПРОВЕРКА НА ПУСТОТУ??????
        print("[note_base]: open note with id = " + str(desired_note_id) )
        print(the_note_str)
        return note.note(the_note_str[0],the_note_str[1],the_note_str[2],the_note_str[3],the_note_str[4],
                         the_note_str[5],the_note_str[6],the_note_str[7],the_note_str[8])


    def edit_note(self, note_obj = note):
        data_to_update = getattr(note_obj, "_note__note_title"), getattr(note_obj, "_note__the_main_text_of_the_note"), \
                         getattr(note_obj,"_note__note_file_type"), getattr(note_obj, "_note__list_of_links_to_other_notes"),\
                         getattr(note_obj, "_note__list_of_note_sources"), getattr(note_obj, "_note__excerpt_from_the_source_for_clarification"), \
                         getattr(note_obj,"_note__explanation_of_creating_a_link_to_other_notes"), \
                         getattr(note_obj,"_note__list_of_note_tag"), getattr(note_obj, "_note__note_identifier")

        self.execute_request_with_unknown_req_value("UPDATE notes SET hdr=?, txt=?, ftype=?, l_id=?,"
                                                    " s_id=?,e_id=?, lce_id=?, t_id=? WHERE n_id=?", data_to_update)
        self.made_commit()
        print("[note_base]: edit note with id = " + str(getattr(note_obj, "_note__note_identifier")))


    def add_note(self, note_obj = note):
        data_to_update = getattr(note_obj, "_note__note_title"), getattr(note_obj, "_note__the_main_text_of_the_note"), \
                         getattr(note_obj,"_note__note_file_type"), getattr(note_obj, "_note__note_identifier"),\
                         getattr(note_obj, "_note__list_of_links_to_other_notes"), getattr(note_obj, "_note__list_of_note_sources"),\
                         getattr(note_obj, "_note__excerpt_from_the_source_for_clarification"), \
                         getattr(note_obj,"_note__explanation_of_creating_a_link_to_other_notes"), \
                         getattr(note_obj,"_note__list_of_note_tag")

        self.execute_request_with_unknown_req_value("INSERT INTO notes ( hdr, txt, ftype, n_id, l_id,"
                                                    " s_id, e_id, lce_id, t_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data_to_update)
        self.made_commit()
        print("[note_base]: add note with id = " + str(getattr(note_obj, "_note__note_identifier")))
