from Tkinter import Entry, StringVar, Listbox, END, ACTIVE, Frame

from typing import Union, Iterable


class AutocompleteBox(Entry):
    def __init__(self, master=None, entries=None, *args, **kwargs):
        # type: (Frame, Union[list, tuple], *object, **object) -> None
        Entry.__init__(self, master, *args, **kwargs)
        self.entries = entries or []
        self.variable = kwargs.get('textvariable') or StringVar()
        self['textvariable'] = self.variable
        self.variable.trace('w', self._changed)
        self.bind('<Return>', self._selection)
        self.bind('<Up>', self._up)
        self.bind('<Down>', self._down)
        self.bind('<Escape>', self._destroy_listbox)
        self.listbox = None

    def _create_listbox_with_entries(self, entries):
        # type: (Iterable) -> None
        if self.listbox is None:
            self.listbox = Listbox()
            self.listbox.bind('<Double-Button-1>', self._selection)
        self.listbox.place(x=self.winfo_x() + 10, y=self.winfo_y() + 30)
        self.listbox.delete(0, END)
        for e in entries:
            self.listbox.insert(END, e)

    def _destroy_listbox(self, *_, **__):
        if self.listbox is None:
            return
        self.listbox.place_forget()

    def _get_filtered_entries(self):
        filter_str = self.variable.get()
        return tuple(e for e in self.entries if filter_str in e)

    def _changed(self, *_, **__):
        if self.variable.get() == '':
            return self._destroy_listbox()
        words = self._get_filtered_entries()
        if len(words) == 0:
            return self._destroy_listbox()
        self._create_listbox_with_entries(words)

    def _selection(self, *_, **__):
        self.variable.set(self.listbox.get(ACTIVE))
        self._destroy_listbox()
        self.icursor(END)

    def _move_listbox_selection(self, amount):
        if self.listbox is None:
            return
        list_size = int(self.listbox.size())
        current_selection = self.listbox.curselection()
        index = int(current_selection[0] if len(current_selection) > 0 else list_size)
        self.listbox.selection_clear('0', str(list_size - 1))
        index = index + amount
        if index < 0:
            index = list_size - 1
        elif index >= list_size:
            index = 0
        str_index = str(index)
        self.listbox.selection_set(str_index)
        self.listbox.activate(str_index)
        self.listbox.see(str_index)

    def _up(self, *_, **__):
        self._move_listbox_selection(-1)

    def _down(self, *_, **__):
        self._move_listbox_selection(+1)


if __name__ == '__main__':
    from Tkinter import Tk
    root = Tk()
    entry = AutocompleteBox(entries=['a', 'b', 'aaa', 'bab'], master=root)
    entry.grid()
    root.mainloop()
