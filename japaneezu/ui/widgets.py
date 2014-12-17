
import urwid

class JapanezuText(urwid.WidgetWrap):

    def __init__(self, content, reading=None):
        self.content = urwid.Text(content, align='left', wrap='clip')
        self.reading = urwid.Text(reading if reading else u'', align='left', wrap='clip')
        self.main = urwid.Pile([
            self.reading,
            self.content,
        ])
        self.__super.__init__(self.main)

    #@property
    #def width(self):
    #    width = max([len(self.reading.text), len(self.content.text)])
    #    return width + 1    #  FIXME
