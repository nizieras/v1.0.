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
        self.execute_request("CREATE TABLE if not exists tags(tag_id INTEGER, tag)")
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

    def links_id_correction(self, deleted_note_id):
        if(deleted_note_id==0):
            request_result = self.execute_request("SELECT n_id FROM notes ORDER BY n_id DESC")
            max_request_result = request_result.fetchone()
            if (max_request_result != None):
                req_res = self.execute_request("SELECT l_id FROM notes")
                l_ids = req_res.fetchall()
                for l_id in l_ids:
                    if (l_id != None):
                        if (l_id[0] != None):
                            str_for_change_str_in_db = ""
                            splited_l_id = l_id[0].split("|")
                            for split_l_id in splited_l_id:
                                if ((split_l_id != "") & (len(split_l_id) > 0)):
                                    str_for_change_str_in_db += str(int(split_l_id) - 1)
                                    str_for_change_str_in_db += "|"
                            self.execute_request_with_unknown_req_value("UPDATE notes SET l_id=? WHERE l_id=?",
                                                                        (str_for_change_str_in_db, l_id[0]))
                            self.made_commit()
        else:
            if (deleted_note_id != self.get_free_note_id_from_note_base()):
                req_res = self.execute_request("SELECT l_id FROM notes")
                l_ids = req_res.fetchall()
                for l_id in l_ids:
                    if (l_id != None):
                        if (l_id[0] != None):
                            str_for_change_str_in_db = ""
                            splited_l_id = l_id[0].split("|")
                            for split_l_id in splited_l_id:
                                if ((split_l_id != "") & (len(split_l_id) > 0)):
                                    if (int(split_l_id) > deleted_note_id):
                                        str_for_change_str_in_db += str(int(split_l_id) - 1)
                                        str_for_change_str_in_db += "|"
                                    else:
                                        str_for_change_str_in_db += split_l_id
                                        str_for_change_str_in_db += "|"
                            self.execute_request_with_unknown_req_value("UPDATE notes SET l_id=? WHERE l_id=?",
                                                                        (str_for_change_str_in_db, l_id[0]))
                            self.made_commit()


    def delete_note(self, deleted_note_id):
        self.execute_request_with_unknown_req_value("DELETE FROM notes WHERE n_id=?",(str(deleted_note_id), ))
        self.id_correction(deleted_note_id)
        self.deleted_note_id_delete_from_link_ids(deleted_note_id)
        self.links_id_correction(deleted_note_id)
        self.made_commit()
        print("[note_base]: deleted note with id = " + str(deleted_note_id) )

    #нужно еще немного потестировать!!!!!!!!!!!!!!!!!!!!!!1
    def deleted_note_id_delete_from_link_ids(self, deleted_note_id):
        link_ids = self.execute_request("SELECT l_id FROM notes").fetchall()
        if(link_ids!=None):
                for link_id in link_ids:
                    if (link_id[0] != None):
                        if (link_id[0].find(str(deleted_note_id) + "|") != -1):
                            str_to_db = (link_id[0].replace(str(deleted_note_id) + "|", ""))
                            self.execute_request_with_unknown_req_value("UPDATE notes SET l_id=? WHERE l_id=?",
                                                                        (str_to_db, link_id[0]))
                            self.made_commit()
                            # записать в базу данных измененную строку

    def add_link_id_in_db(self, link_id, note_id):
        l_id = self.execute_request_with_unknown_req_value("SELECT l_id FROM notes WHERE n_id=?",
                                                           (str(note_id),)).fetchone()
        str_l_id = l_id[0]
        if (str_l_id != None):
            str_l_id += str(link_id)
            str_l_id += "|"
        else:
            str_l_id = str(link_id)
            str_l_id += "|"

        self.execute_request_with_unknown_req_value("UPDATE notes SET l_id=? WHERE n_id=?",
                                                    (str_l_id, str(note_id)))
        self.made_commit()

        n_id = self.execute_request_with_unknown_req_value("SELECT l_id FROM notes WHERE n_id=?",
                                                           (str(link_id),)).fetchone()
        str_n_id = n_id[0]
        if (str_n_id != None):
            str_n_id += str(note_id)
            str_n_id += "|"
        else:
            str_n_id = str(note_id)
            str_n_id += "|"

        self.execute_request_with_unknown_req_value("UPDATE notes SET l_id=? WHERE n_id=?",
                                                    (str_n_id, str(link_id)))

        self.made_commit()
        return str_l_id

    def del_link_id_in_db(self, del_link_id, note_id, splited_link_ids):
        update_str = ""
        if(splited_link_ids!=None):
            for splited_link in splited_link_ids:
                if(splited_link!=str(del_link_id)):
                    update_str+= splited_link
                    update_str+="|"

        self.execute_request_with_unknown_req_value("UPDATE notes SET l_id=? WHERE n_id=?",
                                                    (update_str, str(note_id)))
        self.made_commit()

        note_obj = self.open_note(del_link_id)
        dli_splited_link_id = note_obj.get_the_list_of_links_to_other_splitted()
        dli_update_str = ""

        if(dli_splited_link_id!=None):
            for splited_link in dli_splited_link_id:
                if(splited_link!=str(note_id)):
                    dli_update_str+= splited_link
                    dli_update_str+="|"

        self.execute_request_with_unknown_req_value("UPDATE notes SET l_id=? WHERE n_id=?",
                                                    (dli_update_str, str(del_link_id)))

        self.made_commit()
        return update_str

    def open_note(self, desired_note_id):
        request_result = self.execute_request_with_unknown_req_value("SELECT * FROM notes WHERE n_id=?",
                                                                     (str(desired_note_id),))
        the_note_str = request_result.fetchone()
        print("[note_base]: open note with id = " + str(desired_note_id) )
        print(the_note_str)
        if(the_note_str!=None):
            return note.note(the_note_str[0],the_note_str[1],the_note_str[2],the_note_str[3],the_note_str[4],
                         the_note_str[5],the_note_str[6],the_note_str[7],the_note_str[8])
        else:
            return None

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

        req = self.open_note(data_to_update[3])
        if (req==None):
            self.execute_request_with_unknown_req_value("INSERT INTO notes ( hdr, txt, ftype, n_id, l_id,"
                                                    " s_id, e_id, lce_id, t_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", data_to_update)
        else:
            self.edit_note(note_obj)
        self.made_commit()
        print("[note_base]: add note with id = " + str(getattr(note_obj, "_note__note_identifier")))

    def return_tag_by_id(self, tag_id):
        res_of_req = self.execute_request_with_unknown_req_value("SELECT tag FROM tags WHERE tag_id=?", tag_id)
        return res_of_req.fetchone()

    def get_free_tag_id_from_tags_table(self):
        request_result = self.execute_request("SELECT tag_id FROM tags ORDER BY tag_id DESC")
        max_request_result = request_result.fetchone()
        if (max_request_result == None):
            print("[note_base]: free id in tags = 0")
            return 0
        else:
            print("[note_base]: free id in tags = ["+ str(int(max_request_result[0]) + 1) + "]")
            return (int(max_request_result[0]) + 1)
    def return_ids_str_by_tags(self, tags_str):

        # А если два тега рядышком написаны??????
        # проверить на вхождение пробела, если его нет - сразу перейти к записи?????
        result_str = ""
        if((tags_str!="")&(tags_str!=None)):
            if (tags_str.find(" ") == -1):
                if (tags_str.startwith("#") == True):
                    tag_for_req = (tags_str,)
                    res_of_req = self.execute_request_with_unknown_req_value("SELECT tag_id FROM tags WHERE tag=?",
                                                                             tag_for_req)
                    req_tag_id = res_of_req.fetchone()
                    if (req_tag_id == None):
                        tag_id = self.get_free_tag_id_from_tags_table()
                        data_to_table = tag_id, tags_str
                        self.execute_request_with_unknown_req_value("INSERT INTO tags (tag_id, tag) VALUES (?, ?)",
                                                                    data_to_table)
                        result_str += str(tag_id)
                        result_str += "|"
                    else:
                        result_str += str(req_tag_id[0])
                        result_str += "|"
            else:
                splited_tags_str = tags_str.split(" ")
                for tag in splited_tags_str:
                    if (tag.startswith("#") == True):
                        tag_for_req = (tag,)
                        res_of_req = self.execute_request_with_unknown_req_value("SELECT tag_id FROM tags WHERE tag=?",
                                                                                 tag_for_req)
                        req_tag_id = res_of_req.fetchone()
                        if (req_tag_id == None):
                            tag_id = self.get_free_tag_id_from_tags_table()
                            data_to_table = tag_id, tag
                            self.execute_request_with_unknown_req_value("INSERT INTO tags (tag_id, tag) VALUES (?, ?)",
                                                                        data_to_table)
                            result_str += str(tag_id)
                            result_str += "|"
                        else:
                            result_str += str(req_tag_id[0])
                            result_str += "|"
            return result_str

# возвращает несколько одинаковых чисел....
    def get_list_of_links_id(self,not_splited_link_ids):
        if((not_splited_link_ids==None)|(not_splited_link_ids=="")):
            return None
        else:
            return_list_of_splited_link_id = []
            splited_links_ids = not_splited_link_ids.split('|')
            for link_id in splited_links_ids:
                if((link_id!="")&(len(link_id)>0)):
                    data_to_req = (link_id,)
                    req_result = self.execute_request_with_unknown_req_value("SELECT hdr FROM notes WHERE n_id=?", data_to_req)
                    fetch_req_result = req_result.fetchone()
                    if(fetch_req_result!=None):
                        ret_data = (fetch_req_result[0], link_id)
                        return_list_of_splited_link_id.append(ret_data)
        return return_list_of_splited_link_id

    def find_accordance_in_db(self, searching_str):
        self.execute_request("CREATE VIRTUAL TABLE if not exists search USING fts5(header, text, tags, n_id)")
        main_values = self.execute_request("SELECT hdr, txt, n_id, t_id FROM notes").fetchall()

        for value in main_values:
            note_obj = self.open_note(int(value[2]))
            tag_str = note_obj.get_list_of_note_tag(self)
            data_to_insert = (value[0], value[1], tag_str ,value[2])
            self.execute_request_with_unknown_req_value("INSERT INTO search(header, text, tags, n_id) VALUES(?, ?, ?, ?)",
                                                        data_to_insert)
            self.made_commit()
        req_res = self.execute_request_with_unknown_req_value(
            "SELECT header, n_id FROM search WHERE search MATCH ? ORDER BY rank", (searching_str + "*",)).fetchall()
        if (req_res==None):
            req_res = self.execute_request_with_unknown_req_value(
                "SELECT header, n_id FROM search WHERE search MATCH ? ORDER BY rank", ("^" + searching_str,)).fetchall()
        if (req_res==None):
            req_res = self.execute_request_with_unknown_req_value(
                "SELECT header, n_id FROM search WHERE search MATCH ? ORDER BY rank", ("^" + searching_str + "*",)).fetchall()
        self.execute_request("DROP TABLE search")

        return req_res

    def get_txts_by_tag(self, tag_id):
        result = []
        req_res = self.execute_request("SELECT t_id, txt FROM notes").fetchall()
        for res in req_res:
            if(res[0]!=None):
                str_for_search = res[0]
                if (str_for_search.find(tag_id) !=-1):
                    result.append(res[1])
        return result

    def get_the_list_of_tags(self):
        res_of_req = self.execute_request("SELECT * FROM tags").fetchall()
        return res_of_req

