import note_base as nb
import note

def main():

    note_base_obj = nb.note_base('note_organization_base.db')
    # note_obj = note.note("HHHHHHH","$$$$$$$$$$","txt", note_base_obj.get_free_note_id_from_note_base(), None, None, None, None, None)
    # note_base_obj.add_note(note_obj)
    # note_base_obj.edit_note(note_obj)
    # note_base_obj.get_free_note_id_from_note_base()
    # note_base_obj.delete_note(3)
    # note_obj = note_base_obj.open_note(4)
    note_base_obj.open_note(100)

if __name__=="__main__":
    main()
