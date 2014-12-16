# -*- coding: utf-8 -*-

import urwid
import curses
from collections import OrderedDict
from urwid_utils.palette import PaletteEntry, Palette
from urwid_utils import dialog, colors


config = {
    'prompt_on_quit': True,
}

class JapanezuReader(object):

    palette = Palette()
    palette.body = PaletteEntry(foreground=colors.BLACK, background=colors.LIGHT_GRAY, mono=colors.STANDOUT)
    palette.header = PaletteEntry(foreground=colors.WHITE, background=colors.DARK_RED, mono=colors.BOLD)
    palette.line = PaletteEntry(foreground=colors.BLACK, background=colors.LIGHT_GRAY, mono=colors.STANDOUT)
    palette.button_normal = PaletteEntry(foreground=colors.LIGHT_GRAY, background=colors.DARK_BLUE)
    palette.button_select = PaletteEntry(foreground=colors.WHITE, background=colors.DARK_GREEN)

    def __init__(self):
        self.header = urwid.AttrWrap(urwid.Text('header'), 'header')
        self.reader = urwid.ListBox(urwid.SimpleListWalker([]))
        self.topmost = urwid.Frame(urwid.AttrWrap(self.reader, 'body'), header=self.header)

    def main(self, *args, **kwargs):
        self.loop = urwid.MainLoop(
            widget=self.topmost,
            palette=self.palette,
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
            d = dialog.YesNoDialog(30, 10, data='Are you sure you want to quit?',
                            header_text='Quitting Application', loop=self.loop)
            urwid.connect_signal(d, 'commit', self.user_quit)
            d.show()

def main():
    JapanezuReader().main()

if __name__ == '__main__':
    main()
