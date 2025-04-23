"""
PyQSF element module
"""

from typing import Dict, Any
from enum import Enum

from pyqsf.exceptions import FieldWrongType


# fmt: off
class ElementField(Enum):
    """Fields of Element Object"""

    ELEMENT                 = "Element"
    ID                      = "SurveyID"
    PAYLOAD                 = "Payload"
    PRIMARY_ATTRIBUTE       = "PrimaryAttribute"
    SECONDARY_ATTRIBUTE     = "SecondaryAttribute"
    TERTIARY_ATTRIBUTE      = "TertiaryAttribute"


# fmt: on
class Element:  # pylint: disable=too-few-public-methods
    """Implements Element"""

    def __init__(self, data: Dict[str, Any]):
        # fmt: off
        self.data: Dict[str, Any]       = data
        self.element: str               = self._get_el(ElementField.ELEMENT,                 str)
        self.id: str                    = self._get_el(ElementField.ID,                      str)
        self.payload: Dict[str, Any]    = self._get_el(ElementField.PAYLOAD,                 (dict, list),  required=False)
        self.primary_attribute: str     = self._get_el(ElementField.PRIMARY_ATTRIBUTE,       str)
        self.secondary_attribute: str   = self._get_el(ElementField.SECONDARY_ATTRIBUTE,     str,           required=False)
        self.tertiary_attribute: str    = self._get_el(ElementField.TERTIARY_ATTRIBUTE,      str,           required=False)
        # fmt: on

    def _get_el(self, field: ElementField, _type: Any, required=True):
        value = self.data.get(field.value)
        if required and not isinstance(value, _type):
            raise FieldWrongType("Element", field, _type, type(value))
        return value
