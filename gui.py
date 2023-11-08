import wx
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
        self.text_note = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
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
                word_id = self.vocab_db.updata_data(word)
                self.vocab_db.word_data[word_id] = {"word": word, "definition": definition, "note": note}
            else:
                self.vocab_db.add_new_word(word, definition, note)

        else:
            self.vocab_db.add_new_word(word, definition, note)

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
        button.Bind(wx.EVT_BUTTON, self.on_button_click)



        # List of Vocabulary
        self.list_ctrl = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        self.list_ctrl.InsertColumn(0, "Word/Phrase", width=wx.LIST_AUTOSIZE_USEHEADER)
        self.list_ctrl.InsertColumn(1, "Definition", width=wx.LIST_AUTOSIZE_USEHEADER)
        self.list_ctrl.InsertColumn(2, "Note", width=wx.LIST_AUTOSIZE_USEHEADER)

        # Increase font size for ListCtrl items
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.list_ctrl.SetFont(font)

        # Adjust column widths after adding all items
        self.Bind(wx.EVT_LIST_COL_END_DRAG, self.on_col_end_drag, self.list_ctrl)
        self.Bind(wx.EVT_SIZE, self.on_size)

        for i, word in enumerate(self.vocab_db.word_data.values()):
            self.list_ctrl.InsertItem(i, word["word"])
            self.list_ctrl.SetItem(i, 1, word["definition"])
            self.list_ctrl.SetItem(i, 2, word["note"])

        # Place widget
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button, 0, wx.ALL | wx.CENTER, 10)
        sizer.Add(self.list_ctrl, 1, wx.ALL | wx.EXPAND, 10)
        self.panel.SetSizer(sizer)

        frame_sizer = wx.BoxSizer()
        frame_sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(frame_sizer)
        self.Layout()

    def on_size(self, event):
        # Resize last colum to fill space on window resize
        self.resize_last_column()
        event.Skip()

    def on_col_end_drag(self, event):
        # Resize last column to fill space when user manually resizes columns
        self.resize_last_column()
        event.Skip()

    def resize_last_column(self):
        width = self.list_ctrl.GetClientSize().width - self.list_ctrl.GetColumnWidth(0) - self.list_ctrl.GetColumnWidth(1)
        self.list_ctrl.SetColumnWidth(2, max(width, 100))

    def on_button_click(self, event):
        new_window = add_data_window(self, "Add Word", self.vocab_db)
        new_window.Show()

    def update_list(self):
        self.list_ctrl.DeleteAllItems()

        for i, word in enumerate(self.vocab_db.word_data.values()):
            self.list_ctrl.InsertItem(i, word["word"])
            self.list_ctrl.SetItem(i, 1, word["definition"])
            self.list_ctrl.SetItem(i, 2, word["note"])

    def on_close(self, event):
        self.vocab_db.save_data()
        event.Skip()


def main():
    app = wx.App()
    vocab_db = VocabularyDatabase("vocabulary.db")
    try:
        frame = MyFrame(None, "Vocabulary APP", vocab_db)
        frame.Show()
        app.MainLoop()
    finally:
        vocab_db.close()


if __name__ == "__main__":
    main()

