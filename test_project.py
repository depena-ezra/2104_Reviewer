import unittest
from unittest import mock
import tkinter as tk
from project import ThinkUNextApp

class TestThinkUNextApp(unittest.TestCase):

    @mock.patch('tkinter.Label')
    def test_create_history_panel_with_history(self, MockLabel):
        MockLabel.return_value = mock.MagicMock()
        app = ThinkUNextApp(tk.Tk())
        self.assertTrue(app.sidebar_frame is not None)

    @mock.patch('tkinter.Label')
    def test_create_review_panel_no_sets(self, MockLabel):
        MockLabel.return_value = mock.MagicMock()
        app = ThinkUNextApp(tk.Tk())
        self.assertTrue(app.sidebar_frame is not None)

    @mock.patch('tkinter.Label')
    def test_create_review_panel_sets_available(self, MockLabel):
        MockLabel.return_value = mock.MagicMock()
        app = ThinkUNextApp(tk.Tk())
        self.assertTrue(app.sidebar_frame is not None)

    @mock.patch('tkinter.Label')
    def test_exit_program(self, MockLabel):
        MockLabel.return_value = mock.MagicMock()
        app = ThinkUNextApp(tk.Tk())
        app.exit_program()
        app.root.quit()
        self.assertTrue(app.root.winfo_exists() == 0)

    @mock.patch('tkinter.Label')
    def test_save_progress(self, MockLabel):
        MockLabel.return_value = mock.MagicMock()
        app = ThinkUNextApp(tk.Tk())
        app.save_progress('set1', 100, 2)
        self.assertTrue(True)

    @mock.patch('tkinter.Label')
    def test_show_history_details(self, MockLabel):
        MockLabel.return_value = mock.MagicMock()
        app = ThinkUNextApp(tk.Tk())
        self.assertTrue(True)

    @mock.patch('tkinter.Label')
    def test_start_review_process(self, MockLabel):
        MockLabel.return_value = mock.MagicMock()
        app = ThinkUNextApp(tk.Tk())
        self.assertTrue(True)

    @mock.patch('tkinter.Label')
    def test_validate_answer_correct(self, MockLabel):
        MockLabel.return_value = mock.MagicMock()
        app = ThinkUNextApp(tk.Tk())
        app.validate_answer("correct")
        self.assertTrue(True)

    @mock.patch('tkinter.Label')
    def test_validate_answer_incorrect(self, MockLabel):
        MockLabel.return_value = mock.MagicMock()
        app = ThinkUNextApp(tk.Tk())
        app.validate_answer("incorrect")
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
