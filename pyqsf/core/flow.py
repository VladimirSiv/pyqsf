"""
PyQSF flow module
"""

from typing import List, Dict, Any
from enum import Enum

from pyqsf.core.element import Element
from pyqsf.exceptions import FlowNotFound, FieldWrongType


# fmt: off
class FlowField(Enum):
    """Fields of Flow Object"""

    FLOW = "Flow"
    FLOW_ID = "FlowID"
    PROPERTIES = "Properties"
    TYPE = "Type"


class FlowEntryField(Enum):
    """Fields of Flow Entry Object"""

    FLOW_ID = "FlowID"
    ID      = "ID"
    TYPE    = "Type"


# fmt: on
class FlowEntry:  # pylint: disable=too-few-public-methods
    """Implements Flow Entry"""

    def __init__(self, data: dict[str, Any]):
        # fmt: off
        self.data: Dict[str, Any]   = data
        self.flow_id: str           = self._get(FlowEntryField.FLOW_ID,    str)
        self.id: str                = self._get(FlowEntryField.ID,         str)
        self.type: str              = self._get(FlowEntryField.TYPE,       str)
        # fmt: on

    def _get(self, field: FlowEntryField, _type: Any, required=True):
        value = self.data.get(field.value)
        if required and not isinstance(value, _type):
            raise FieldWrongType("Flow Entry", field, _type, type(value))
        return value


class Flow(Element):  # pylint: disable=too-few-public-methods
    """Implements Flow"""

    def __init__(self, data: Dict[str, Any]):
        super().__init__(data)
        # fmt: off
        self.flow_id: str               = self._get_att(FlowField.FLOW_ID,      str)
        self.properties: dict           = self._get_att(FlowField.PROPERTIES,   dict)
        self.type: str                  = self._get_att(FlowField.TYPE,         str)
        # fmt: on
        self._entries: List[FlowEntry] = self._parse_flow_entries()

    def get_block_ids(self) -> List[str]:
        """Returns Block IDs"""
        return [x.id for x in self._entries]

    def _parse_flow_entries(self) -> List[FlowEntry]:
        flow = self._get_att(FlowField.FLOW, list)
        if not isinstance(flow, list) or len(flow) == 0:
            raise FlowNotFound()

        entries = []
        for entry in flow:
            entries.append(FlowEntry(entry))
        return entries

    def _get_att(self, field: FlowField, _type: Any, required=True):
        value = self.payload.get(field.value)
        if required and not isinstance(value, _type):
            raise FieldWrongType("Flow", field, _type, type(value))
        return value
