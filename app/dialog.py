from tkinter import Toplevel, Frame, Button, ACTIVE, LEFT, font


class Dialog(Toplevel):
    """
    Code of this class is from http://tkinter.programujte.com/tkinter-dialog-windows.htm and slightly edited by me.
    This is base class for all dialog windows.
    """

    def __init__(self, parent, title=None):
        Toplevel.__init__(self, parent)

        self.font: font.Font = font.Font(family="serif", size=15)

        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.buttonbox()

        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5, side="top")

        # dialog remains always in front
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+150,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master: Frame):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        self.ok_btn: Button = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        self.ok_btn.pack(side=LEFT, padx=5, pady=5)
        self.cancel_btn: Button = Button(box, text="Zrušit", width=10, command=self.cancel)
        self.cancel_btn.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack(side="bottom")

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):
        return 1 # override

    def apply(self):
        pass # override