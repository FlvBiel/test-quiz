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

def test_question_rejects_points_outside_allowed_range():
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title="q1", points=0)
    with pytest.raises(Exception, match="Points must be between 1 and 100"):
        Question(title="q1", points=101)


def test_question_can_be_created_with_custom_max_selections():
    question = Question(title="q1", max_selections=3)

    assert question.max_selections == 3


def test_adding_choices_assigns_sequential_ids():
    question = Question(title="q1")

    first = question.add_choice("a")
    second = question.add_choice("b")
    third = question.add_choice("c")

    assert [first.id, second.id, third.id] == [1, 2, 3]


def test_adding_choice_returns_the_created_choice():
    question = Question(title="q1")

    choice = question.add_choice("Answer", is_correct=True)

    assert choice in question.choices
    assert choice.text == "Answer"
    assert choice.is_correct


def test_question_rejects_empty_choice_text():
    question = Question(title="q1")

    with pytest.raises(Exception, match="Text cannot be empty"):
        question.add_choice("")


def test_question_rejects_choice_text_longer_than_100_characters():
    question = Question(title="q1")

    with pytest.raises(Exception, match="Text cannot be longer than 100 characters"):
        question.add_choice("a" * 101)


def test_removing_choice_keeps_other_choices():
    question = Question(title="q1")
    first = question.add_choice("a")
    second = question.add_choice("b")
    third = question.add_choice("c")

    question.remove_choice_by_id(second.id)

    assert question.choices == [first, third]


def test_removing_unknown_choice_id_reports_an_error():
    question = Question(title="q1")
    question.add_choice("a")

    with pytest.raises(Exception, match="Invalid choice id 99"):
        question.remove_choice_by_id(99)


def test_correcting_selected_choices_returns_only_correct_selections():
    question = Question(title="q1", max_selections=3)
    correct = question.add_choice("correct", is_correct=True)
    incorrect = question.add_choice("incorrect")
    another_correct = question.add_choice("also correct", is_correct=True)

    result = question.correct_selected_choices(
        [incorrect.id, correct.id, another_correct.id]
    )

    assert result == [correct.id, another_correct.id]


def test_correcting_more_than_allowed_selections_reports_an_error():
    question = Question(title="q1", max_selections=1)
    first = question.add_choice("a", is_correct=True)
    second = question.add_choice("b")

    with pytest.raises(Exception, match="Cannot select more than 1 choices"):
        question.correct_selected_choices([first.id, second.id])

@pytest.fixture
def question_with_multiple_choices():
    """Cria uma questão com alternativas para reutilizar nos testes."""
    question = Question(
        title="Qual é a capital do Brasil?",
        max_selections=2
    )
    question.add_choice("Brasília", is_correct=True)
    question.add_choice("Rio de Janeiro")
    question.add_choice("São Paulo")
    question.add_choice("Salvador")
    return question


def test_fixture_question_contains_multiple_choices(question_with_multiple_choices):
    question = question_with_multiple_choices

    assert len(question.choices) == 4
    assert [choice.text for choice in question.choices] == [
        "Brasília", "Rio de Janeiro", "São Paulo", "Salvador"
    ]


def test_fixture_question_corrects_selected_choices(question_with_multiple_choices):
    question = question_with_multiple_choices
    correct_choice = question.choices[0]
    incorrect_choice = question.choices[1]

    result = question.correct_selected_choices(
        [correct_choice.id, incorrect_choice.id]
    )

    assert result == [correct_choice.id]