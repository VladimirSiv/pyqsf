"""
PyQSF qsf module
"""

import json
from pathlib import Path
from typing import Dict, Any, List, cast
from enum import Enum

from pyqsf.core.entry import SurveyEntry
from pyqsf.core.flow import Flow
from pyqsf.core.block import Block, BlockElementType, BlockEntry, PageBreak
from pyqsf.core.question import Question, QuestionFactory
from pyqsf.exceptions import (
    FileNotFound,
    QSFNotValid,
    ElementTypeNotFound,
    QuestionNotFound,
)


# fmt: off
class SurveyFileFields(Enum):
    """Fields of Survey File Object"""

    SURVEY_ENTRY    = "SurveyEntry"
    SURVEY_ELEMENTS = "SurveyElements"


class SurveyElementType(Enum):
    """Survey Element Types"""

    BLOCKS          = "BL"
    CT              = "CT"
    FLOW            = "FL"
    OPTIONS         = "SO"
    PREVIEW_LINK    = "PL"
    PROJECT         = "PROJ"
    QUESTION        = "SQ"
    QUESTION_COUNT  = "QC"
    RESPONSE_SET    = "RS"
    SCORING         = "SCO"
    STATISTICS      = "STAT"


# fmt: on
class QualtricsSurveyFile:  # pylint: disable=too-many-instance-attributes
    """Implements Qualtrics Survey File"""

    def __init__(self, filepath: str) -> None:
        self._json = self._load_file(Path(filepath))
        self._validate_qsf()
        self._blocks = cast(Block, None)
        self._ct = None
        self._flow = cast(Flow, None)
        self._options = None
        self._preview_link = None
        self._project = None
        self._question_count = None
        self._response_set = None
        self._scoring = None
        self._statistics = None
        self._questions: List[Question] = []
        self._parse_elements()
        self._structure = self._compose()

        self.entry = SurveyEntry(self._json[SurveyFileFields.SURVEY_ENTRY.value])

    @property
    def questions(self) -> List[Question]:
        """Returns Survey Questions"""
        result = []
        for elements in self._structure.values():
            for element in elements:
                if isinstance(element, Question):
                    result.append(element)
        return result

    @property
    def blocks(self) -> List[BlockEntry]:
        """Returns Survey Blocks"""
        return list(self._structure)

    def _load_file(self, filepath: Path) -> Dict[str, Any]:
        if not filepath.exists():
            raise FileNotFound(str(filepath))
        try:
            return json.loads(filepath.read_text(encoding="UTF-8"))
        except json.JSONDecodeError as err:
            raise QSFNotValid("Cannot load JSON.") from err

    def _validate_qsf(self) -> None:
        if not self._json.get(SurveyFileFields.SURVEY_ENTRY.value, False):
            raise QSFNotValid("SurveyEntry not present.")
        if not self._json.get(SurveyFileFields.SURVEY_ELEMENTS.value, False):
            raise QSFNotValid("SurveyElements not present.")

    def _parse_elements(self) -> None:  # pylint: disable=too-many-branches
        for element in self._json[SurveyFileFields.SURVEY_ELEMENTS.value]:
            _type = element.get("Element")
            if _type == SurveyElementType.QUESTION.value:
                self._questions.append(Question(element))
            elif _type == SurveyElementType.BLOCKS.value:
                self._blocks = Block(element)
            elif _type == SurveyElementType.FLOW.value:
                self._flow = Flow(element)
            elif _type == SurveyElementType.OPTIONS.value:
                self._options = element
            elif _type == SurveyElementType.PREVIEW_LINK.value:
                self._preview_link = element
            elif _type == SurveyElementType.PROJECT.value:
                self._project = element
            elif _type == SurveyElementType.QUESTION_COUNT.value:
                self._question_count = element
            elif _type == SurveyElementType.RESPONSE_SET.value:
                self._response_set = element
            elif _type == SurveyElementType.SCORING.value:
                self._scoring = element
            elif _type == SurveyElementType.STATISTICS.value:
                self._statistics = element
            elif _type == SurveyElementType.CT.value:
                self._ct = element
            else:
                raise ElementTypeNotFound(_type)

    def _compose(self) -> Dict[BlockEntry, Any]:
        result = {}
        for block_id in self._flow.get_block_ids():
            block = self._blocks.get_block_by_id(block_id)
            elements = []
            for element in block.elements:
                if element.type == BlockElementType.QUESTION.value:
                    element = self._get_question_by_id(element.question_id)
                elif element.type == BlockElementType.PAGE_BREAK.value:
                    element = PageBreak()
                elements.append(element)
            result[block] = elements
        return result

    def _get_question_by_id(self, _id: str) -> Question:
        for question in self._questions:
            if question.question_id == _id:
                return QuestionFactory(question.question_type, question.data)
        raise QuestionNotFound(_id)
