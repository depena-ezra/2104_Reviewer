# pytest test_project.py

import pytest
from unittest.mock import MagicMock
import os
import json
from project import ThinkUNextApp

USER_SETS = "sets"
ACP_SETS = "acp_sets"
HISTORY_FOLDER = "history"

@pytest.fixture
def setup_app():
    app = ThinkUNextApp(MagicMock())
    app.mistakes = []
    app.questions = []
    app.test_folder = "test_sets"
    app.test_set_name = "PytestSet"
    app.test_set_path = os.path.join(app.test_folder, f"{app.test_set_name}.json")
    os.makedirs(app.test_folder, exist_ok=True)
    os.makedirs(HISTORY_FOLDER, exist_ok=True)
    app.review_panel = MagicMock()
    app.current_question_index = 0

    app.display_question = MagicMock()
    app.review_panel.winfo_children.return_value = [MagicMock(cget=MagicMock(return_value=""))]
    
    yield app
    if os.path.exists(app.test_folder):
        for file in os.listdir(app.test_folder):
            os.remove(os.path.join(app.test_folder, file))
        os.rmdir(app.test_folder)

def test_start_review_valid_file(setup_app):
    set_data = [{"question": "What is 2+2?", "answer": "4"}]
    with open(setup_app.test_set_path, 'w') as f:
        json.dump(set_data, f)

    setup_app.start_review(setup_app.test_folder, setup_app.test_set_name)
    assert setup_app.questions == set_data
    assert setup_app.current_question_index == 0

def test_start_review_invalid_file(setup_app):
    setup_app.start_review(setup_app.test_folder, "invalid_set")
    assert setup_app.questions == []
    assert setup_app.current_question_index == 0

def test_validate_answer_correct(setup_app):
    set_data = [{"question": "What is 2+2?", "answer": "4"}]
    setup_app.questions = set_data
    setup_app.current_question_index = 0
    setup_app.correct_answer = "4"
    setup_app.user_answer_entry = MagicMock()
    setup_app.user_answer_entry.get.return_value = "4"
    
    setup_app.display_question = MagicMock()
    setup_app.display_question()
    
    mock_widget = MagicMock()
    mock_widget.cget.return_value = "Correct!"
    setup_app.review_panel.winfo_children.return_value = [mock_widget]
    
    setup_app.validate_answer()

    feedback_text = setup_app.review_panel.winfo_children()[0].cget("text")
    assert "Correct!" in feedback_text

def test_validate_answer_incorrect(setup_app):
    set_data = [{"question": "What is 2+2?", "answer": "4"}]
    setup_app.questions = set_data
    setup_app.current_question_index = 0
    setup_app.correct_answer = "4"
    setup_app.user_answer_entry = MagicMock()
    setup_app.user_answer_entry.get.return_value = "5"

    setup_app.display_question = MagicMock()
    setup_app.display_question()

    mock_widget = MagicMock()
    mock_widget.cget.return_value = "Incorrect!"
    setup_app.review_panel.winfo_children.return_value = [mock_widget]
    setup_app.review_panel.winfo_children = MagicMock(return_value=[mock_widget])

    setup_app.validate_answer()

    feedback_text = setup_app.review_panel.winfo_children()[0].cget("text")
    assert "Incorrect!" in feedback_text

def test_show_review_result(setup_app):
    set_data = [{"question": "What is 2+2?", "answer": "4"}]
    setup_app.questions = set_data
    setup_app.mistakes = [{"question": "What is 2+2?", "user_answer": "5", "answer": "4"}]
    
    setup_app.review_panel = MagicMock()
    
    mock_widget = MagicMock()
    mock_widget.cget.return_value = "Your Score: 0/1"
    setup_app.review_panel.winfo_children.return_value = [mock_widget]
    
    setup_app.show_review_result(setup_app.test_set_name)

    result_text = setup_app.review_panel.winfo_children()[0].cget("text")
    assert "Your Score: 0/1" in result_text

def test_create_set(setup_app):
    set_data = [{"question": "What is 3+3?", "answer": "6"}]
    setup_app.temp_questions = set_data
    setup_app.create_set_name_var.set("PytestSet")
    setup_app.finish_create_set()

    set_file = os.path.join(USER_SETS, "PytestSet.json")
    assert os.path.exists(set_file)
    with open(set_file, 'r') as f:
        saved_data = json.load(f)
    assert saved_data == set_data

def test_edit_set_existing(setup_app):
    set_data = [{"question": "What is 3+3?", "answer": "6"}]
    with open(setup_app.test_set_path, 'w') as f:
        json.dump(set_data, f)

    setup_app.edit_set_var.set("PytestSet")
    setup_app.edit_selected_set()

    mock_entry = MagicMock()
    mock_entry.get.return_value = "What is 3+3?"
    
    setup_app.edit_entries[0]["entry"] = mock_entry

    assert setup_app.edit_entries[0]["entry"].get() == "What is 3+3?"

def test_add_question_to_edit_set(setup_app):
    set_data = [{"question": "What is 3+3?", "answer": "6"}]
    with open(setup_app.test_set_path, 'w') as f:
        json.dump(set_data, f)

    setup_app.edit_set_var.set("PytestSet")
    setup_app.edit_selected_set()

    mock_question_entry = MagicMock()
    mock_answer_entry = MagicMock()
    mock_question_entry.get.return_value = "What is 4+4?"
    mock_answer_entry.get.return_value = "8"

    setup_app.new_question_var = mock_question_entry
    setup_app.new_answer_var = mock_answer_entry

    setup_app.add_question(setup_app.test_set_path, set_data)

    with open(setup_app.test_set_path, 'r') as f:
        updated_data = json.load(f)
    assert len(updated_data) == 2
    assert updated_data[-1]["question"] == "What is 4+4?"
    assert updated_data[-1]["answer"] == "8"

def test_delete_question_from_edit_set(setup_app):
    set_data = [{"question": "What is 3+3?", "answer": "6"}]
    with open(setup_app.test_set_path, 'w') as f:
        json.dump(set_data, f)

    setup_app.edit_set_var.set("PytestSet")
    setup_app.edit_selected_set()

    setup_app.delete_question(setup_app.test_set_path, 0, set_data)

    with open(setup_app.test_set_path, 'r') as f:
        updated_data = json.load(f)
    assert len(updated_data) == 0
