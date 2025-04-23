import pytest
from pyqsf.core.qsf import (
    QualtricsSurveyFile,
    FileNotFound,
    QSFNotValid,
    QuestionNotFound,
    ElementTypeNotFound,
)
from pyqsf.core.question import Question
from pyqsf.core.block import BlockEntry


@pytest.fixture
def template(datadir, request):
    return datadir.join(request.param)


@pytest.mark.parametrize(
    "template",
    (
        [
            "brand_perceptions.qsf",
            "customer_service_contact_center.qsf",
            "employee_exit_interview.qsf",
            "needs_based_analytics.qsf",
            "pricing_study.qsf",
            "transactional_effort_customer_score.qsf",
        ]
    ),
    indirect=True,
)
def test_read_templates(template):
    qsf = QualtricsSurveyFile(template)
    for question in qsf.questions:
        assert issubclass(question.__class__, Question)
    for block in qsf.blocks:
        assert issubclass(block.__class__, BlockEntry)


@pytest.mark.parametrize(
    "template",
    (["test.qsf"]),
    indirect=True,
)
def test_file_not_found(template):
    with pytest.raises(FileNotFound):
        QualtricsSurveyFile(template)


@pytest.mark.parametrize(
    "template",
    (["corrupted.qsf"]),
    indirect=True,
)
def test_file_corrupted(template):
    with pytest.raises(QSFNotValid) as exc:
        QualtricsSurveyFile(template)
    assert str(exc.value) == "Provided QSF file is not valid. Reason: Cannot load JSON."


@pytest.mark.parametrize(
    "template",
    (["no_survey_entry.qsf"]),
    indirect=True,
)
def test_survey_entry_not_present(template):
    with pytest.raises(QSFNotValid) as exc:
        QualtricsSurveyFile(template)
    assert (
        str(exc.value)
        == "Provided QSF file is not valid. Reason: SurveyEntry not present."
    )


@pytest.mark.parametrize(
    "template",
    (["no_survey_elements.qsf"]),
    indirect=True,
)
def test_survey_elements_not_present(template):
    with pytest.raises(QSFNotValid) as exc:
        QualtricsSurveyFile(template)
    assert (
        str(exc.value)
        == "Provided QSF file is not valid. Reason: SurveyElements not present."
    )


@pytest.mark.parametrize(
    "template",
    (["question_not_found.qsf"]),
    indirect=True,
)
def test_question_not_found(template):
    with pytest.raises(QuestionNotFound) as exc:
        QualtricsSurveyFile(template)
    assert str(exc.value) == "Question with id: `TEST`, not found."


@pytest.mark.parametrize(
    "template",
    (["survey_element_not_found.qsf"]),
    indirect=True,
)
def test_survey_element_not_found(template):
    with pytest.raises(ElementTypeNotFound) as exc:
        QualtricsSurveyFile(template)
    assert str(exc.value) == "Survey Element of type `TEST` not recognized."
