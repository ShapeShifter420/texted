import re
import argparse
from twin import Text_win
import curses
from ftp_com import FtpInterpreter


def main():
    parser = argparse.ArgumentParser(description='text editor argument')
    parser.add_argument('name', type=str, default='newfile.txt',
                        help='name of file')
    parser.add_argument('-c', '--encode', default='UTF-8', help='code')
    namespaces = parser.parse_args()
    if not check_correct(namespaces.name) == []:
        print('Please use correct input')
        exit(0)
    try:
        texteditor = texted()
        texteditor.get_text_from_file(namespaces.name, namespaces.encode)
        texteditor.get_key()
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()


def check_correct(name):
    return re.findall('[/, \\, <, >,:,\",?,|, *]', name)



class texted():
    def __init__(self):
        self.src = curses.initscr()
        self.filename = ''
        curses.cbreak()
        self.src.keypad(1)
        curses.noecho()
        curses.start_color()
        self.src.refresh()

    def get_text_from_file(self, filename, encode):
        self.text_win = Text_win(self.src, filename, encode)
        self.filename = filename
        self.encode = encode
        filename_win = self.src.subwin(1, curses.COLS - 1, 0, 1)
        filename_win.addstr("file:" + filename)
        filename_win.refresh()
        self.make_text_win()

    def write(self):
        self.text_win.save()

    def make_text_win(self):
        self.makestatus('EDIT   '+'('+str(self.text_win.pagenum+1)+')')
        self.src.refresh()
        self.text_win.edit()
        self.src.refresh()
        self.makestatus('COMMAND')

    def makestatus(self, stat):
        status = self.src.subwin(1, curses.COLS - 1, curses.LINES - 1, 0)
        status.addstr(stat)
        status.refresh()

    def get_key(self):
        while True:
            char = self.src.getch()
            if char == ord('q'):
                self.src.keypad(0)
                break
            elif char == ord('w'):
                curses.beep()
                self.write()
            elif char == ord('e'):
                curses.beep()
                self.make_text_win()
            elif char == ord('n'):
                curses.beep()
                self.text_win.goto_nextpage()
                self.make_text_win()
            elif char == ord('m'):
                curses.beep()
                self.text_win.goto_prepage()
                self.make_text_win()
            elif char == ord('r'):
                curses.beep()
                self.get_text_from_file(self.filename, self.encode)
            elif char == ord('p'):
                curses.beep()
                curses.nocbreak()
                curses.echo()
                curses.endwin()
                print('Введите имя хоста: home.dimonius.ru')
                print('')
                # ftp = FtpInterpreter()
                # ftp.do_connect(input('Введите имя хоста: '))
                # filename = ''
                # while True:
                #     command = input('ftp>>')
                #     if 'list' in command:
                #         ftp.do_list()
                #     elif 'cd' in command:
                #         ftp.do_cwd(command.split(' ')[1])
                #     elif 'cd ..' in command:
                #         ftp.do_pwd()
                #     elif 'download' in command:
                #         ftp.do_pwd()
                #     elif 'open' in command:
                #         filename = command.split(' ')[1]
                #         break
                #     elif 'download' in command:
                #         ftp.do_pwd()
                # texteditor = texted()
                # texteditor.get_text_from_file(filename, 'UTF-8')
                # texteditor.get_key()


def start_page():
    pass


if __name__ == '__main__':
    main()
