"""
PyQSF question module
"""

from typing import Dict, Any, Tuple
from enum import Enum

from pyqsf.core.element import Element
from pyqsf.exceptions import FieldWrongType, QuestionTypeNotFound


# fmt: off
class QuestionType(Enum):
    """Question Types"""

    MC = "MC"
    DB = "DB"
    TE = "TE"
    MATRIX = "Matrix"


class QuestionField(Enum):
    """Fields of Question"""

    CONFIGURATION           = "Configuration"
    DATA_EXPORT_TAG         = "DataExportTag"
    LANGUAGE                = "Language"
    NEXT_ANSWER_ID          = "NextAnswerId"
    NEXT_CHOICE_ID          = "NextChoiceId"
    QUESTION_DESCRIPTION    = "QuestionDescription"
    QUESTION_ID             = "QuestionID"
    QUESTION_TEXT           = "QuestionText"
    QUESTION_TYPE           = "QuestionType"
    SELECTOR                = "Selector"
    VALIDATION              = "Validation"


# fmt: on
class Question(
    Element
):  # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """Implements Base Question class"""

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        # fmt: off
        self.configuration: Dict[str, Any]  = self._get(QuestionField.CONFIGURATION,        dict)
        self.data_export_tag: str           = self._get(QuestionField.DATA_EXPORT_TAG,      str)
        self.language: Dict[str, Any]       = self._get(QuestionField.LANGUAGE,             dict)
        self.next_answer_id: int            = self._get(QuestionField.NEXT_ANSWER_ID,       int)
        self.next_choice_id: int            = self._get(QuestionField.NEXT_CHOICE_ID,       int)
        self.description: str               = self._get(QuestionField.QUESTION_DESCRIPTION, str)
        self.question_id: str               = self._get(QuestionField.QUESTION_ID,          str)
        self.question_description: str      = self._get(QuestionField.QUESTION_DESCRIPTION, str)
        self.question_text: str             = self._get(QuestionField.QUESTION_TEXT,        str)
        self.question_type: str             = self._get(QuestionField.QUESTION_TYPE,        str)
        self.selector: str                  = self._get(QuestionField.SELECTOR,             str)
        self.validation: Dict[str, Any]     = self._get(QuestionField.VALIDATION,           dict,   required=False)
        # fmt: on

    def _get(self, field: QuestionField, _type: Any, required=True) -> Any:

        value = self.payload.get(field.value)
        if required and not isinstance(value, _type):
            raise FieldWrongType("Question", field, _type, type(value))
        return value


class MCQuestionField(Enum):
    """Fields of MC Question"""

    # fmt: off
    CHOICES         = "Choices"
    CHOICE_ORDER    = "ChoiceOrder"
    DATA_VISIBILITY = "DataVisibility"
    DEFAULT_CHOICES = "DefaultChoices"
    GRADING_DATA    = "GradingData"
    # fmt: on


class MCQuestion(Question):  # pylint: disable=too-few-public-methods
    """MC Question class"""

    def __init__(self, data):
        super().__init__(data)
        # fmt: off
        self.choices: Tuple[dict, list] = self._get_mc(MCQuestionField.CHOICES,            (dict, list))
        self.choice_order: list         = self._get_mc(MCQuestionField.CHOICE_ORDER,       list)
        self.data_visibility: dict      = self._get_mc(MCQuestionField.DATA_VISIBILITY,    dict, required=False)
        self.default_choices: bool      = self._get_mc(MCQuestionField.DEFAULT_CHOICES,    bool, required=False)
        self.grading_data: list         = self._get_mc(MCQuestionField.GRADING_DATA,       list, required=False)
        # fmt: on

    def _get_mc(self, field: MCQuestionField, _type: Any, required=True) -> Any:

        value = self.payload.get(field.value)
        if required and not isinstance(value, _type):
            raise FieldWrongType("MC Question", field, _type, type(value))
        return value


class TEQuestion(Question):  # pylint: disable=too-few-public-methods
    """TE Question class"""


class DBQuestion(Question):  # pylint: disable=too-few-public-methods
    """DB Question class"""


class MatrixQuestion(Question):  # pylint: disable=too-few-public-methods
    """Matrix Question class"""


def QuestionFactory(  # pylint: disable=invalid-name
    question_type: str, data: Dict[str, Any]
) -> Question:
    """Question Factory Function"""

    types = {
        QuestionType.MC.value: MCQuestion,
        QuestionType.TE.value: TEQuestion,
        QuestionType.DB.value: DBQuestion,
        QuestionType.MATRIX.value: MatrixQuestion,
    }

    if question_type not in types:
        raise QuestionTypeNotFound(question_type)

    return types[question_type](data)
