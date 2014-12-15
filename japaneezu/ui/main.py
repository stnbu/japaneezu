# -*- coding: utf-8 -*-

import urwid
import curses

config = {
    'prompt_on_quit': True,
}


class DialogFrame(urwid.Frame):
    def __init__(self, *args, **kwargs):
        self.escape = kwargs.pop('escape')
        urwid.Frame.__init__(self, *args, **kwargs)
    def keypress(self, size, key):
        if key in ('tab', 'up', 'down'):
            if self.focus_part == 'body':
                if key in ('tab', 'down'):
                    self.set_focus('footer')
            elif self.focus_part == 'footer':
                if key in ('tab', 'up'):
                    self.set_focus('body')
        elif key in ['esc',]:
            self.escape()
        return self.__super.keypress(size, key)

class DialogBase(urwid.WidgetWrap):
    __metaclass__ = urwid.signals.MetaSignals
    signals = ['commit']
    parent = None
    def __init__(self, width, height, data, header_text=None, loop=None, buttons=None):
        if loop is None:
            raise ValueError('loop is a required argument.')

        width = int(width)
        if width <= 0:
            width = ('relative', 80)
        height = int(height)
        if height <= 0:
            height = ('relative', 80)

        self.body = self.make_body(data)

        self.frame = DialogFrame(self.body, focus_part = 'body', escape=self.on_negatory)
        if header_text is not None:
            self.frame.header = urwid.Pile( [urwid.Text(header_text),
                urwid.Divider(u'\u2550')] )
        w = self.frame
        # pad area around listbox
        w = urwid.Padding(w, ('fixed left',2), ('fixed right',2))
        w = urwid.Filler(w, ('fixed top',1), ('fixed bottom',1))
        w = urwid.AttrWrap(w, 'body')
        w = urwid.LineBox(w)
        # "shadow" effect
        w = urwid.Columns( [w,('fixed', 1, urwid.AttrWrap(
            urwid.Filler(urwid.Text(('border',' ')), "top")
            ,'shadow'))])
        w = urwid.Frame( w, footer = urwid.AttrWrap(urwid.Text(('border',' ')),'shadow'))
        self.loop = loop
        self.parent = self.loop.widget
        w = urwid.Overlay(w, self.parent, 'center', width+2, 'middle', height+2)
        self.view = w
        self.buttons = buttons
        if self.buttons is None:
            self.buttons = [("OK", True, self.on_affirmative), ("Cancel", False, self.on_negatory)]
        elif isinstance(self.buttons, basestring):
            if self.buttons.lower() in ('yesno', 'yes/no', 'yes-no'):
                self.buttons = [("Yes", True, self.on_affirmative), ("No", False, self.on_negatory)]
            elif self.buttons.lower() in ('okcancel', 'ok/cancel', 'ok-cancel'):
                self.buttons = [("OK", True, self.on_affirmative), ("Cancel", False, self.on_negatory)]
        self.add_buttons(self.buttons)
        self.exitcode = None
        urwid.WidgetWrap.__init__(self, self.view)
    def make_body(self, data):
        'please implement'
    def callback(self):
        'please implement'
    def add_buttons(self, buttons):
        l = []
        for name, exitcode, callback in buttons:
            b = urwid.Button(name, callback, user_data=exitcode)
            b.exitcode = exitcode
            b = urwid.AttrWrap( b, 'button normal','button select' )
            l.append( b )
        self.buttons = urwid.GridFlow(l, 10, 3, 1, 'center')
        self.frame.footer = urwid.Pile( [ urwid.Divider(u'\u2500'),
            self.buttons ], focus_item = 1)
    def _button(self, *args, **kwargs):
        if len(args) == 3:
            _class, button, _status = args
            self.exitcode = button.exitcode
        self.loop.widget = self.parent
    def on_affirmative(self, *args, **kwargs):
        self._button(self, *args, **kwargs)
        urwid.emit_signal(self, 'commit', self.callback())
    def on_negatory(self, *args, **kwargs):
        self._button(self, *args, **kwargs)
    def show(self):
        self.loop.widget = self.view

class YesNoDialog(DialogBase):
    def __init__(self, *args, **kwargs):
        kwargs['buttons'] = 'yes/no'
        DialogBase.__init__(self, *args, **kwargs)
    def make_body(self, data):
        return urwid.Filler(urwid.Text(data))
    def callback(self, *args, **kwargs):
        return self.exitcode

class JapanezuReader(object):

    def __init__(self):
        self.header = urwid.AttrWrap(urwid.Text('header'), 'header')
        self.reader = urwid.ListBox(urwid.SimpleListWalker([]))
        self.topmost = urwid.Frame(urwid.AttrWrap(self.reader, 'body'), header=self.header)

    def main(self, *args, **kwargs):
        self.loop = urwid.MainLoop(
            widget=self.topmost,
            palette={},
            unhandled_input=self.unhandled_input,
            pop_ups=True,
            handle_mouse=False)
        self.loop.run()

    def quit(self):
        raise urwid.ExitMainLoop()

    def user_quit(self, response):
        if response is True:
            self.quit()

    def unhandled_input(self, k):
        if not isinstance(k, basestring):
            return k
        if k.lower() == 'q':
            if not config['prompt_on_quit']:
                self.quit()
            dialog = YesNoDialog(30, 10, data='Are you sure you want to quit?',
                            header_text='Quitting Application', loop=self.loop)
            urwid.connect_signal(dialog, 'commit', self.user_quit)
            dialog.show()

def main():
    JapanezuReader().main()

if __name__ == '__main__':
    main()
