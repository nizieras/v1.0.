import note_base

class note:

    def __init__(self, note_title, the_main_text_of_the_note, note_file_type ,note_identifier ,
                 list_of_links_to_other_notes, list_of_note_sources, excerpt_from_the_source_for_clarification,
                 explanation_of_creating_a_link_to_other_notes, list_of_note_tag):
        self.__note_title = note_title
        self.__list_of_note_tag = list_of_note_tag
        self.__list_of_note_sources = list_of_note_sources
        self.__the_main_text_of_the_note = the_main_text_of_the_note
        self.__excerpt_from_the_source_for_clarification = excerpt_from_the_source_for_clarification
        # сделать проверку, если вдруг что-то пойдет не так с определением id??????
        self.__note_identifier = note_identifier
        self.__list_of_links_to_other_notes = list_of_links_to_other_notes
        self.__note_file_type = note_file_type
        self.__explanation_of_creating_a_link_to_other_notes = explanation_of_creating_a_link_to_other_notes

    def clean_object(self):
        self.__note_title = None
        self.__note_identifier = None
        self.__note_file_type = None
        self.__list_of_note_tag = None
        self.__list_of_links_to_other_notes = None
        self.__the_main_text_of_the_note = None
        self.__excerpt_from_the_source_for_clarification = None
        self.__explanation_of_creating_a_link_to_other_notes = None
        self.__list_of_note_sources = None

    def if_object_empty(self):
        # Не совсем корректное определение пустоты????????????????????7
        if(self.__note_identifier==None):
            return True
        else:
            return False

    def change_object(self, data_to_change):
        self.__note_title = data_to_change[0]
        self.__the_main_text_of_the_note = data_to_change[1]
        self.__list_of_links_to_other_notes = data_to_change[2]
        self.__explanation_of_creating_a_link_to_other_notes = data_to_change[3]
        self.__list_of_note_tag = data_to_change[4]
        self.__list_of_note_sources = data_to_change[5]
        self.__excerpt_from_the_source_for_clarification = data_to_change[6]
        self.__note_identifier = data_to_change[7]
        self.__note_file_type = data_to_change[8]

    def get_note_id(self):
        return getattr(self,"_note__note_identifier")

    def get_note_title(self):
        return getattr(self,"_note__note_title")

    def get_the_main_text_of_the_note(self):
        return getattr(self, "_note__the_main_text_of_the_note")

    def get_the_list_of_links_to_other_notes(self):
        return getattr(self, "_note__list_of_links_to_other_notes")

    def get_explanation_of_creating_a_link_to_other_notes(self):
        return getattr(self, "_note__explanation_of_creating_a_link_to_other_notes")

    def get_list_of_note_tag(self, note_base_obj = note_base):

        list_of_tags_id = getattr(self, "_note__list_of_note_tag")
        if(list_of_tags_id!=None):
            splitted_list_of_note_ids = list_of_tags_id.split("|")
            note_tags_str = ""
            for tag_id in splitted_list_of_note_ids:
                note_tags_str+=note_base_obj.return_tag_by_id(tag_id)[0]
                note_tags_str+=" "
            return note_tags_str
        else:
            return None

    def get_list_of_note_sources(self):
        return getattr(self, "_note__list_of_note_sources")

    def get_excerpt_from_the_source_for_clarification(self):
        return getattr(self, "_note__excerpt_from_the_source_for_clarification")











