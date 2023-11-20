import wx
import wx.dataview as dv
from db import VocabularyDatabase


class add_data_window(wx.Frame):
    def __init__(self, parent, title, vocab_db):
        super(add_data_window, self).__init__(parent, title=title, size=(400, 250))
        self.vocab_db = vocab_db
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Word/Phrase
        word_box = wx.BoxSizer(wx.HORIZONTAL)
        label1 = wx.StaticText(panel, label="Word/Phrase:")
        word_box.Add(label1, 0, wx.Right, 8)
        self.text_word = wx.TextCtrl(panel)
        word_box.Add(self.text_word, 1, wx.EXPAND)
        sizer.Add(word_box, 0, wx.EXPAND | wx.ALL, 10)

        # Definition
        definition_box = wx.BoxSizer(wx.HORIZONTAL)
        label2 = wx.StaticText(panel, label="Definition:")
        definition_box.Add(label2, 0, wx.RIGHT, 8)
        self.text_def = wx.TextCtrl(panel)
        definition_box.Add(self.text_def, 1, wx.EXPAND)
        sizer.Add(definition_box, 0, wx.EXPAND | wx.ALL, 10)

        # Note
        note_box = wx.BoxSizer(wx.HORIZONTAL)
        label3 = wx.StaticText(panel, label="Note:")
        note_box.Add(label3, 0, wx.RIGHT, 8)
        self.text_note = wx.TextCtrl(panel)
        note_box.Add(self.text_note, 1, wx.EXPAND)
        sizer.Add(note_box, 0, wx.EXPAND | wx.ALL, 10)

        # Button to submit
        add_button = wx.Button(panel, label="Add")
        add_button.Bind(wx.EVT_BUTTON, self.add_word_data)
        sizer.Add(add_button, 0, wx.CENTER, 10)

        panel.SetSizer(sizer)

    def add_word_data(self, event):
        word = self.text_word.GetValue()
        definition = self.text_def.GetValue()
        note = self.text_note.GetValue()

        if not word.strip():
            wx.MessageBox("The 'Word/Phrase' field must be filled in.", "Error", wx.OK | wx.ICON_ERROR)
            return

        existing_word = self.vocab_db.check_word_exists(word)

        if existing_word:
            dlg = wx.MessageDialog(self, f"{word} already exists. Do you want to update it?", "Word Exists", wx.YES_NO |
                                   wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()

            if result == wx.ID_YES:
                word_id = self.vocab_db.update_data(word)
                self.vocab_db.word_data[word_id] = {"word": word, "definition": definition, "note": note}
            else:
                self.vocab_db.add_new_word(word, definition, note)

        else:
            self.vocab_db.add_new_word(word, definition, note)

        self.vocab_db.save_data()

        self.Close()
        self.GetParent().update_list()

class edit_word_info_window(wx.Frame):
    def __init__(self, parent, title, vocab_db, word="", definition="", note=""):
        super(edit_word_info_window, self).__init__(parent, title=title, size=(400, 250))
        self.vocab_db = vocab_db
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Word/Phrase
        word_box = wx.BoxSizer(wx.HORIZONTAL)
        label1 = wx.StaticText(panel, label="Word/Phrase:")
        word_box.Add(label1, 0, wx.Right, 8)
        self.text_word = wx.TextCtrl(panel)
        word_box.Add(self.text_word, 1, wx.EXPAND)
        sizer.Add(word_box, 0, wx.EXPAND | wx.ALL, 10)

        # Definition
        definition_box = wx.BoxSizer(wx.HORIZONTAL)
        label2 = wx.StaticText(panel, label="Definition:")
        definition_box.Add(label2, 0, wx.RIGHT, 8)
        self.text_def = wx.TextCtrl(panel)
        definition_box.Add(self.text_def, 1, wx.EXPAND)
        sizer.Add(definition_box, 0, wx.EXPAND | wx.ALL, 10)

        # Note
        note_box = wx.BoxSizer(wx.HORIZONTAL)
        label3 = wx.StaticText(panel, label="Note:")
        note_box.Add(label3, 0, wx.RIGHT, 8)
        self.text_note = wx.TextCtrl(panel)
        note_box.Add(self.text_note, 1, wx.EXPAND)
        sizer.Add(note_box, 0, wx.EXPAND | wx.ALL, 10)

        # Set initial value on text boxes
        self.text_word.SetValue(word)
        self.text_def.SetValue(definition)
        self.text_note.SetValue(note)

        # Button to submit
        add_button = wx.Button(panel, label="Apply")
        add_button.Bind(wx.EVT_BUTTON, self.edit_data)
        sizer.Add(add_button, 0, wx.CENTER, 10)

        panel.SetSizer(sizer)

    def edit_data(self, event):
        word = self.text_word.GetValue()
        definition = self.text_def.GetValue()
        note = self.text_note.GetValue()

        word_id = self.vocab_db.update_data(word)
        self.vocab_db.word_data[word_id] = {"word": word, "definition": definition, "note": note}

        self.vocab_db.save_data()

        self.Close()
        self.GetParent().update_list()

class MyFrame(wx.Frame):
    def __init__(self, parent, title, vocab_db):
        super(MyFrame, self).__init__(parent, title=title, size=(1000, 700))
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.vocab_db = vocab_db

        self.panel = wx.Panel(self)

        # Button to open a window to add new data
        button = wx.Button(self.panel, label="Add")
        button.Bind(wx.EVT_BUTTON, self.on_button_click_to_add_new_word)
        # Button to open a window to edit word info
        edit_button = wx.Button(self.panel, label="Edit")
        edit_button.Bind(wx.EVT_BUTTON, self.on_button_click_to_edit_word_info)

        # Button to search word in field by user input
        search_button = wx.Button(self.panel, label="Search")
        search_button.Bind(wx.EVT_BUTTON, self.on_search)
        # Search box
        self.search_ctrl = wx.SearchCtrl(self.panel)
        self.search_ctrl.SetPosition((10, 10))
        # List for method of search
        choices = ["Word/Phrase", "Definition", "Note"]
        self.combo_box = wx.ComboBox(self.panel, choices=choices)
        # List of Vocabulary using DataViewListCtrl
        self.dvlc = dv.DataViewListCtrl(self.panel, style=dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_HORIZ_RULES)

        # Adding columns to DataViewListCtrl
        self.dvlc.AppendTextColumn("Word/Phrase")
        self.dvlc.AppendTextColumn("Definition")
        self.dvlc.AppendTextColumn("Note")

        # Populate the DataViewListCtrl
        for word in self.vocab_db.word_data.values():
            self.dvlc.AppendItem([word["word"], word["definition"], word["note"]])

        # Set the size of the columns to fit the content
        for i in range(self.dvlc.GetColumnCount()):
            self.dvlc.Columns[i].SetWidth(wx.COL_WIDTH_AUTOSIZE)

        # Configure font on field
        font = wx.Font(35, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Times New Roman")
        self.dvlc.SetFont(font)

        # Place widget
        horizontal_sizer_search = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_sizer_search.Add(self.search_ctrl, 1, wx.EXPAND)
        horizontal_sizer_search.Add(self.combo_box, 0, wx.LEFT, 10)
        horizontal_sizer_search.Add(search_button, 0, wx.LEFT, 10)

        horizontal_sizer_button = wx.BoxSizer(wx.HORIZONTAL)
        horizontal_sizer_button.Add(button, 0, wx.LEFT, 10)
        horizontal_sizer_button.Add(edit_button, 0, wx.LEFT, 10)

        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer.Add(horizontal_sizer_button, 0, wx.ALL | wx.CENTER, 10)
        vertical_sizer.Add(horizontal_sizer_search, 0, wx.ALL | wx.EXPAND, 5)
        vertical_sizer.Add(self.dvlc, 1, wx.ALL | wx.EXPAND, 10)
        self.panel.SetSizer(vertical_sizer)

        frame_sizer = wx.BoxSizer()
        frame_sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(frame_sizer)
        self.Layout()

    def on_size(self, event):
        # Resize columns when the frame size changes
        for i in range(self.dvlc.GetColumnCount()):
            self.dvlc.Columns[i].SetWidth(wx.COL_WIDTH_AUTOSIZE)
        event.Skip()

    def on_button_click_to_add_new_word(self, event):
        # Logic for the button click
        new_window = add_data_window(self, "Add Word", self.vocab_db)
        new_window.Show()

    def on_button_click_to_edit_word_info(self, event):
        selected_row = self.dvlc.GetSelectedRow()
        if selected_row != -1:
            word = self.dvlc.GetTextValue(selected_row, 0)
            definition = self.dvlc.GetTextValue(selected_row, 1)
            note = self.dvlc.GetTextValue(selected_row, 2)
            edit_window = edit_word_info_window(self, "Edit Word", self.vocab_db, word, definition, note)
            edit_window.Show()

    def on_search(self, event):
        selection = self.combo_box.GetStringSelection()
        if selection == "Word/Phrase":
            search_text = self.search_ctrl.GetValue().lower()
            for item in range(self.dvlc.GetItemCount()):
                word = self.dvlc.GetValue(item, 0).lower()
                self.select_and_focus_line(search_text, word, item)
            # if search box is empty, undo selection.
            if not search_text:
                self.dvlc.UnselectAll()
        elif selection == "Definition":
            search_text = self.search_ctrl.GetValue().lower()
            for item in range(self.dvlc.GetItemCount()):
                definition = self.dvlc.GetValue(item, 1).lower()
                self.select_and_focus_line(search_text, definition, item)
            # if search box is empty, undo selection.
            if not search_text:
                self.dvlc.UnselectAll()
        elif selection == "Note":
            search_text = self.search_ctrl.GetValue().lower()
            for item in range(self.dvlc.GetItemCount()):
                note = self.dvlc.GetValue(item, 2).lower()
                self.select_and_focus_line(search_text, note, item)
            # if search box is empty, undo selection.
            if not search_text:
                self.dvlc.UnselectAll()

    def select_and_focus_line(self, text, item_of_value, item):
        if text in item_of_value:
            item_obj = self.dvlc.RowToItem(item)
            self.dvlc.Select(item_obj)
            self.dvlc.EnsureVisible(item_obj)
            self.dvlc.SetFocus()
        else:
            item_obj = self.dvlc.RowToItem(item)
            self.dvlc.Unselect(item_obj)

    def update_list(self):
        # Delete all existing rows
        self.dvlc.DeleteAllItems()

        # Iterate over the data in the database and add it to the list
        for word in self.vocab_db.word_data.values():
            # AppendItem takes a list of values corresponding to each column
            self.dvlc.AppendItem([word["word"], word["definition"], word["note"]])

        # Optionally resize columns to fit their content
        for i in range(self.dvlc.GetColumnCount()):
            self.dvlc.Columns[i].SetWidth(wx.COL_WIDTH_AUTOSIZE)

    def on_close(self, event):
        # Save data and clean up before closing
        self.vocab_db.save_data()
        event.Skip()


def main():
    app = wx.App(redirect=False)
    vocab_db = VocabularyDatabase("vocabulary.db")
    try:
        frame = MyFrame(None, "Vocabulary APP", vocab_db)
        frame.Show()
        app.MainLoop()
    finally:
        vocab_db.close()


if __name__ == "__main__":
    main()

