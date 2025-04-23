"""
PyQSF block module
"""

from typing import Dict, Any, List
from enum import Enum

from pyqsf.core.element import Element
from pyqsf.exceptions import FieldWrongType, BlockEntryNotFound


# fmt: off
class BlockEntryField(Enum):
    """Fields of Block Entry Object"""

    BLOCK_ELEMENTS  = "BlockElements"
    DESCRIPTION     = "Description"
    ID              = "ID"
    OPTIONS         = "Options"
    TYPE            = "Type"


class BlockElementField(Enum):
    """Fields of Block Element Object"""

    TYPE = "Type"
    QUESTION_ID = "QuestionID"


class BlockElementType(Enum):
    """Block Element Types"""

    QUESTION = "Question"
    PAGE_BREAK = "Page Break"


# fmt: on


class PageBreak:  # pylint: disable=too-few-public-methods
    """Implements Page Break class"""


class BlockElement:  # pylint: disable=too-few-public-methods
    """Implements Block Element"""

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.type = self._get(BlockElementField.TYPE, str)
        if self.type == BlockElementType.QUESTION.value:
            self.question_id = self._get(BlockElementField.QUESTION_ID, str)

    def _get(self, field: BlockElementField, _type: Any, required=True):
        value = self.data.get(field.value)
        if required and not isinstance(value, _type):
            raise FieldWrongType("Block Element", field, _type, type(value))
        return value


class BlockEntry:  # pylint: disable=too-few-public-methods
    """Implements Block Entry"""

    def __init__(self, data: Dict[str, Any]):
        # fmt: off
        self.data = data
        self.block_elements: List[Dict[str, Any]]   = self._get(BlockEntryField.BLOCK_ELEMENTS,   list)
        self.description: str                       = self._get(BlockEntryField.DESCRIPTION,      str)
        self.id: str                                = self._get(BlockEntryField.ID,               str)
        self.options: Dict[str, Any]                = self._get(BlockEntryField.OPTIONS,          dict, required=False)
        self.type: str                              = self._get(BlockEntryField.TYPE,             str)
        # fmt: on

        self.elements: List[BlockElement] = [
            BlockElement(e) for e in self.block_elements
        ]

    def _get(self, field: BlockEntryField, _type: Any, required=True):
        value = self.data.get(field.value)
        if required and not isinstance(value, _type):
            raise FieldWrongType("Block Entry", field, _type, type(value))
        return value


class Block(Element):  # pylint: disable=too-few-public-methods
    """Implements Block"""

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        self.block_elements = self._get_block_elements()

    def get_block_by_id(self, _id: str):
        """Returns Block IDs"""
        for block in self.block_elements:
            if block.id == _id:
                return block
        raise BlockEntryNotFound(_id)

    def _get_block_elements(self) -> List[BlockEntry]:
        if isinstance(self.payload, dict):
            return [BlockEntry(v) for v in self.payload.values()]
        return [BlockEntry(e) for e in self.payload]
