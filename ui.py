# coding=utf-8
from Tkinter import Frame, Button, EW, E, W, SE, SW, Label, Entry, Checkbutton, IntVar, StringVar, \
    Text, DISABLED, END, NORMAL, N, S
from ttk import Combobox

from typing import Optional

from custom import AutocompleteBox
from send_message import send_message


class StoresLoaderUI(Frame):
    def __init__(self, master=None, **kw):
        # type: (Frame, **object) -> None
        Frame.__init__(self, master, **kw)
        self.grid()
        self._create_widgets()

    def _create_widgets(self):
        Label(self, width=30, height=10, text='Obtendo lista de lojas atualizada...') \
            .grid(row=0, column=0)


class AppUI(Frame):
    def __init__(self, master=None, defaults=None, stores_info=None, **kw):
        # type: (Frame, Optional[dict], Optional[dict], **object) -> None
        Frame.__init__(self, master, **kw)
        stores_info = stores_info or {}
        self.stores_info = {'%s - %s' % (i['StoreCode'], i['Name']): i['IpAddress']
                            for i in stores_info}
        self.grid(padx=10, pady=10, sticky=(N, W, E, S))
        self.message_input = None
        self.token = StringVar(value='')
        self.timeout = IntVar(value=-1)
        self.address = StringVar(value='')
        self.type = StringVar(value='')
        self.service = StringVar(value='')
        self.format = StringVar(value='')
        self.is_base_64 = IntVar(value=0)
        self.replace_0 = IntVar(value=1)
        self.message_output = None
        self.send_button = None
        self._create_widgets()
        self.grid_propagate()
        self.master.bind('<Control-s>', lambda e: self.send_message())
        # self.master.resizable(False, False)
        if defaults is not None:
            self._fill_defaults(defaults)

    def _fill_defaults(self, defaults):
        # type: (dict) -> None
        for key, value in defaults.iteritems():
            if key == 'message_input':
                self.message_input.delete('1.0', END)
                self.message_input.insert('1.0', value)
            elif hasattr(self, key):
                getattr(self, key).set(value)

        pass

    def _create_widgets(self):
        int_validator = (self.register(self._validate_int), '%P', '%S')

        Label(self, text='Endereço:')\
            .grid(row=0, column=0, sticky=E)
        AutocompleteBox(self, entries=self.stores_info.keys(), textvariable=self.address)\
            .grid(row=0, column=1, sticky=EW)

        Label(self, text='Type:')\
            .grid(row=1, column=0, sticky=E)
        Entry(self, textvariable=self.type)\
            .grid(row=1, column=1, sticky=EW)

        Label(self, text='Service:')\
            .grid(row=2, column=0, sticky=E)
        Entry(self, textvariable=self.service)\
            .grid(row=2, column=1, sticky=EW)

        Label(self, text='Token:')\
            .grid(row=3, column=0, sticky=E)
        Entry(self, textvariable=self.token)\
            .grid(row=3, column=1, sticky=EW)

        Label(self, text='Format:')\
            .grid(row=4, column=0, sticky=E)
        Combobox(self, textvariable=self.format, values=('param', 'string', 'xml'))\
            .grid(row=4, column=1, sticky=W)

        Label(self, text='Timeout:')\
            .grid(row=5, column=0, sticky=E)
        Entry(self, textvariable=self.timeout, validate='key', validatecommand=int_validator)\
            .grid(row=5, column=1, sticky=EW)

        Label(self, text='Base 64:')\
            .grid(row=6, column=0, sticky=E)
        Checkbutton(self, variable=self.is_base_64)\
            .grid(row=6, column=1, sticky=W)

        Label(self, text='Replace \\0:') \
            .grid(row=7, column=0, sticky=E)
        Checkbutton(self, variable=self.replace_0) \
            .grid(row=7, column=1, sticky=W)

        self.message_input = Text(self, width=40, height=11)
        self.message_input.grid(row=0, column=2, rowspan=8)

        self.send_button = Button(self, text='Enviar (Ctrl + s)', command=self.send_message)
        self.send_button.grid(row=8, column=0, pady=5, columnspan=3, sticky=SE+SW)

        Label(self, text='Resposta (na área de transferência):')\
            .grid(row=9, column=0, columnspan=3)

        self.message_output = Text(self, width=66, height=8, state=DISABLED)
        self.message_output.grid(row=10, column=0, columnspan=6)
        self.message_output.columnconfigure(0, weight=1)
        self.message_output.rowconfigure(10, weight=1)

    # noinspection PyMethodMayBeStatic
    def _validate_int(self, new_value, text_inserted):
        # type: (str, str) -> bool
        if new_value == '':
            return True
        if text_inserted not in '0123456789-':
            return False
        try:
            int(new_value)
            return True
        except ValueError:
            return False

    def _fill_response(self, value):
        # type: (str) -> None
        self.message_output.config(state=NORMAL)
        self.message_output.delete('1.0', END)
        self.message_output.insert('1.0', value)
        self.message_output.config(state=DISABLED)

    def send_message(self):
        self.send_button.config(state=DISABLED)
        data = self.message_input.get('1.0', END).encode('utf-8').rstrip()
        if self.replace_0.get():
            data = data.replace('\\0', '\0')
        try:
            address = self.address.get()
            if address in self.stores_info:
                address = self.stores_info[address]
            resp = send_message(address, self.type.get(), self.service.get(),
                                self.token.get(), self.format.get(), data, self.timeout.get(),
                                bool(self.is_base_64.get()))
            self.clipboard_clear()
            self.clipboard_append(resp.replace('\0', '\n'))
            self.update()
        except Exception as ex:
            resp = 'ERROR: {}'.format(ex)
        self._fill_response(resp)
        self.send_button.config(state=NORMAL)


if __name__ == '__main__':
    app = AppUI()
    app.master.title('Send HV Message')
    app.mainloop()
