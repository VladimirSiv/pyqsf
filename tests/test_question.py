import pytest
import json
from pathlib import Path
from pyqsf.core.question import (
    Question,
    QuestionField,
    QuestionType,
    QuestionFactory,
    TEQuestion,
    MatrixQuestion,
    DBQuestion,
    MCQuestion,
    MCQuestionField,
)
from pyqsf.exceptions import FlowNotFound, FieldWrongType, QuestionTypeNotFound


@pytest.fixture
def question_example(datadir, request):
    mc_question = datadir.join(request.param)
    return json.loads(Path(mc_question).read_text())


@pytest.mark.parametrize(
    "question_example",
    (["mc_question.json"]),
    indirect=True,
)
def test_question_init(question_example):
    data = question_example
    question = Question(data)
    for field in QuestionField:
        assert (
            question.__getattribute__(field.name.lower())
            == data["Payload"][field.value]
        )


@pytest.mark.parametrize(
    "question_example",
    (["mc_question.json"]),
    indirect=True,
)
def test_question_field_wrong_type(question_example):
    payload = {**question_example["Payload"], "QuestionID": 1}
    data = {**question_example, "Payload": payload}
    with pytest.raises(FieldWrongType) as exc:
        Question(data)
    assert (
        str(exc.value)
        == "Question field `QuestionID` wrong type. Expected `<class 'str'>`, got `<class 'int'>`."
    )


@pytest.mark.parametrize(
    "question_example",
    (["mc_question.json"]),
    indirect=True,
)
def test_mc_question(question_example):
    data = question_example
    mc_question = MCQuestion(data)
    for field in MCQuestionField:
        assert (
            mc_question.__getattribute__(field.name.lower())
            == data["Payload"][field.value]
        )


@pytest.mark.parametrize(
    "question_example",
    (["mc_question.json"]),
    indirect=True,
)
def test_mc_question_field_wrong_type(question_example):
    payload = {**question_example["Payload"], "Choices": 1}
    data = {**question_example, "Payload": payload}
    with pytest.raises(FieldWrongType) as exc:
        MCQuestion(data)
    assert (
        str(exc.value)
        == "MC Question field `Choices` wrong type. Expected `(<class 'dict'>, <class 'list'>)`, got `<class 'int'>`."
    )


def test_question_factory_type_not_found():
    with pytest.raises(QuestionTypeNotFound) as exc:
        QuestionFactory("TEST", {})
    assert str(exc.value) == "Question type `TEST` not found"


@pytest.mark.parametrize(
    "question_example",
    (["mc_question.json"]),
    indirect=True,
)
def test_question_return_mc_question(question_example):
    question = QuestionFactory(QuestionType.MC.value, question_example)
    assert isinstance(question, MCQuestion)


@pytest.mark.parametrize(
    "question_example",
    (["te_question.json"]),
    indirect=True,
)
def test_question_return_te_question(question_example):
    question = QuestionFactory(QuestionType.TE.value, question_example)
    assert isinstance(question, TEQuestion)


@pytest.mark.parametrize(
    "question_example",
    (["matrix_question.json"]),
    indirect=True,
)
def test_question_return_question_question(question_example):
    question = QuestionFactory(QuestionType.MATRIX.value, question_example)
    assert isinstance(question, MatrixQuestion)


@pytest.mark.parametrize(
    "question_example",
    (["db_question.json"]),
    indirect=True,
)
def test_question_return_db_question(question_example):
    question = QuestionFactory(QuestionType.DB.value, question_example)
    assert isinstance(question, DBQuestion)
