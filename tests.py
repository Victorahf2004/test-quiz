import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

#MEUS NOVOS TESTES COMMIT 2 DA AULA PRÁTICA 1
def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title="q1", points=0)
    with pytest.raises(Exception):
        Question(title="q2", points=300)

def test_create_choice_with_invalid_text():
    question = Question(title="q1")
    
    with pytest.raises(Exception):
        question.add_choice("", True)
    with pytest.raises(Exception):
        question.add_choice(('a'*200), False)

def test_create_multiple_choice_question():
    question = Question(title="q1")

    question.add_choice("a", False)
    question.add_choice("b", True)
    
    choice_a = question.choices[0]
    choice_b = question.choices[1]
    assert len(question.choices) == 2
    assert choice_a.text == 'a'
    assert not choice_a.is_correct
    assert choice_b.text == 'b'
    assert choice_b.is_correct == True

def test_set_correct_choices():
    question = Question(title="q1")

    question.add_choice("a", False)
    question.add_choice("b", False)
    question.add_choice("c", False)
    choice_a = question.choices[0]
    choice_b = question.choices[1]
    choice_c = question.choices[2]
    choice_c_id = question.choices[2].id
    correct_choice_ids = [choice_c_id]
    question.set_correct_choices(correct_choice_ids)

    assert not choice_a.is_correct
    assert not choice_b.is_correct
    assert choice_c.is_correct == True

def test_correct_selected_choices():
    question = Question(title="q1")

    question.add_choice("a")
    question.add_choice("b")
    question.add_choice("c")
    choice_c = question.choices[2]
    correct_choice_ids = [choice_c.id]
    question.set_correct_choices(correct_choice_ids)
    selected_choice_ids = [choice_c.id]
    correct_selected_choices = question.correct_selected_choices(selected_choice_ids)

    assert len(correct_selected_choices) == 1
    assert correct_selected_choices[0] == choice_c.id

def test_reset_question_choices():
    question = Question(title="q1")

    question.add_choice("a")
    question.add_choice("b")
    question.add_choice("c")
    question.remove_all_choices()

    assert len(question.choices) == 0

def test_remove_choice():
    question = Question(title="q1")

    question.add_choice("a")
    question.add_choice("b")
    choice_a_id = question.choices[0].id
    question.remove_choice_by_id(choice_a_id)

    assert len(question.choices) == 1
    assert question.choices[0].id != choice_a_id
    assert question.choices[0].text == "b"

def test_remove_invalid_choice():
    question = Question(title="q1")

    question.add_choice("a")
    question.add_choice("b")
    
    with pytest.raises(Exception):
        invalid_id = 350
        question.remove_choice_by_id(invalid_id)

def test_set_invalid_correct_choices():
    question = Question(title="q1")

    question.add_choice("a")
    question.add_choice("b")
    question.add_choice("c")

    invalid_id = 350
    invalid_correct_choice_ids = [invalid_id]
    with pytest.raises(Exception):
        question.set_correct_choices(invalid_correct_choice_ids)

def test_correct_invalid_selected_choices():
    question = Question(title="q1")

    question.add_choice("a")
    question.add_choice("b")
    question.add_choice("c")
    choice_c = question.choices[2]
    correct_choice_ids = [choice_c.id]
    question.set_correct_choices(correct_choice_ids)

    choice_a_id = question.choices[0].id
    invalid_selected_choice_ids = [choice_a_id, choice_c.id]
    with pytest.raises(Exception):
        correct_selected_choices = question.correct_selected_choices(invalid_selected_choice_ids)

#MEUS NOVOS TESTES, COMMIT 3 DA AULA PRÁTICA 1

@pytest.fixture
def multiple_choice_question():
    multiple_choice_question = Question(title="q1", max_selections=2)
    multiple_choice_question.add_choice("a")
    multiple_choice_question.add_choice("b")
    multiple_choice_question.add_choice("c")
    choice_c = multiple_choice_question.choices[2]
    multiple_choice_question.set_correct_choices([choice_c.id])
    return multiple_choice_question

def test_correct_selected_choices_when_all_wrong(multiple_choice_question):
    choice_a = multiple_choice_question.choices[0]

    empty_correct_selected_choices = multiple_choice_question.correct_selected_choices([choice_a.id])

    assert len(empty_correct_selected_choices) == 0

def test_correct_selected_choices_with_mixed_selection(multiple_choice_question):
    choice_a = multiple_choice_question.choices[0]
    choice_c = multiple_choice_question.choices[2]

    correct_selected = multiple_choice_question.correct_selected_choices([choice_a.id, choice_c.id])

    assert len(correct_selected) == 1
    assert correct_selected[0] == choice_c.id    