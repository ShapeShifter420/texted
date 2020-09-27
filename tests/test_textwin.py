import pytest
import stext.texted as tx
import curses
import stext.twin as tw


class Test_Texted:
    def test_correct_simple(self):
        assert tx.check_correct('new.txt') == []

    def test_correct_onespec(self):
        assert not tx.check_correct('*new.txt') == []

    def test_correct_quest(self):
        assert not tx.check_correct('ne?w.txt') == []

    def test_correct_all(self):
        assert tx.check_correct('abcdefgh') == []

    def test_all(self):
        src = curses.initscr()
        texteditor = tw.TextWin(src, 'somenotinos', 'UTF-8')
        texteditor.text += 'dd'
        texteditor.istest = True
        texteditor.save()

    def test_check_correct(self):
        assert tw.TextWin.check_correct('new.txt') == []

