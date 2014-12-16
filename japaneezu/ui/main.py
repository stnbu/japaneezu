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

    palette.dialog_body = PaletteEntry(foreground=colors.DARK_BLUE, background=colors.WHITE)
    palette.dialog_header = PaletteEntry(foreground=colors.DARK_MAGENTA, background=colors.LIGHT_GREEN)
    palette.dialog_footer = PaletteEntry(foreground=colors.DARK_MAGENTA, background=colors.WHITE)
    palette.dialog_border = PaletteEntry(foreground=colors.DARK_RED, background=colors.WHITE)
    palette.button = PaletteEntry(foreground=colors.LIGHT_GRAY, background=colors.DARK_BLUE)
    palette.reveal_focus = PaletteEntry(foreground=colors.WHITE, background=colors.DARK_RED)

    palette.body = PaletteEntry(foreground=colors.BLACK, background=colors.LIGHT_GRAY)
    palette.header = PaletteEntry(foreground=colors.WHITE, background=colors.DARK_RED)
    palette.line = PaletteEntry(foreground=colors.BLACK, background=colors.LIGHT_GRAY)

    def __init__(self):
        self.header = urwid.AttrMap(urwid.Text('header'), self.palette.header.name)
        self.reader = urwid.ListBox(urwid.SimpleListWalker([]))
        self.topmost = urwid.Frame(urwid.AttrMap(self.reader, self.palette.body.name), header=self.header)

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
            d = dialog.YesNoDialog(width=30,
                                   height=10,
                                   data='Are you sure you want to quit?',
                                   header_text='Quitting Application',
                                   loop=self.loop,
                                   palette=self.palette)
            urwid.connect_signal(d, 'commit', self.user_quit)
            d.show()

def main():
    curses.wrapper(JapanezuReader().main)

if __name__ == '__main__':
    main()
