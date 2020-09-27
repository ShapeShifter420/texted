import curses
import os
from curses.textpad import Textbox


class Text_win:
    def __init__(self, window, filename, encode):
        self.filename = filename
        self.encode = encode
        self.ost = ""
        self.gen = self.get_text()
        self.pages = [self.makepage()]
        self.screen = window
        self.pagenum = 0
        self.istest = False
        self.text_win = self.screen.subwin(curses.LINES - 2,
                                           curses.COLS-1, 1, 0)

    def edit(self):
        self.text_win.clear()
        try:
            self.text_win.addstr(self.pages[self.pagenum])
        except curses.error:
            pass
        textbox = Textbox(self.text_win, insert_mode=True)
        if not self.istest:
            textbox.edit()
            self.pages[self.pagenum] = collect(textbox)
            curses.flash()

    def save(self):
        with open(self.filename, "w", encoding=self.encode) as file:
            text = ""
            for i in self.pages:
                text += "".join(i)
            file.write(text)

    def goto_nextpage(self):
        self.pagenum += 1
        if self.pagenum == len(self.pages):
            self.pages.append(self.makepage())

    def goto_prepage(self):
        if self.pagenum != 0:
            self.pagenum -= 1

    def get_text(self):
        if os.path.isfile(self.filename):
            with open(self.filename, encoding=self.encode) as myfile:
                for i in myfile:
                    yield i
        else:
            yield ""
        return

    def makepage(self):
        text = ""
        lines = curses.LINES - 2
        while True:
            try:
                if self.ost:
                    line = self.ost
                else:
                    line = next(self.gen)
                lines -= checklines(line)
                if lines > 0:
                    text += line
                else:
                    text += line[:(curses.COLS - 1) *
                                  (lines + checklines(line) + 1) + 1]
                    self.ost = line[(curses.COLS - 1) *
                                    (lines + checklines(line) + 1) + 1:]
                    break
            except StopIteration:
                break
        return text


def collect(textwin):
    result = ""
    for l in range(textwin.maxy+1):
        textwin.win.move(l, 0)
        stop = textwin._end_of_line(l)
        for c in range(textwin.maxx+1):
            if c > stop:
                break
            result = result + chr(curses.ascii.ascii(textwin.win.inch(l, c)))
        result = result + "\n"
    return result


def checklines(rawtext):
    dop = 1 + int(len(rawtext) / (curses.COLS - 1))
    return dop
