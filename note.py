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


