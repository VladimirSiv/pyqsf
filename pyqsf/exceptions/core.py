"""
PyQSF core exceptions module
"""


class PyQSFBaseException(Exception):
    """Implements PyQSF Base Exception"""


class FileNotFound(PyQSFBaseException):
    """Implements File Not Found Exception"""

    def __init__(self, filepath: str) -> None:
        super().__init__(f"File path '{filepath}' does not exist.")


class QSFNotValid(PyQSFBaseException):
    """Implements QSF Not Valid Exception"""

    def __init__(self, reason: str = "") -> None:
        message = "Provided QSF file is not valid."
        if reason:
            message += " Reason: " + reason
        super().__init__(message)


class BlockEntryNotFound(PyQSFBaseException):
    """Implement Block Entry Not Found"""

    def __init__(self, _id: str):
        super().__init__(f"Block entry with id: `{_id}`, not found.")


class QuestionNotFound(PyQSFBaseException):
    """Implement Question Not Found"""

    def __init__(self, _id: str):
        super().__init__(f"Question with id: `{_id}`, not found.")


class QuestionTypeNotFound(PyQSFBaseException):
    """Implement Question Type Not Found"""

    def __init__(self, _type: str):
        super().__init__(f"Question type `{_type}` not found")


class ElementTypeNotFound(PyQSFBaseException):
    """Implements Element Type Not Found"""

    def __init__(self, _type: str) -> None:
        super().__init__(f"Survey Element of type `{_type}` not recognized.")


class FlowNotFound(PyQSFBaseException):
    """Implements Flow Not Found"""

    def __init__(self) -> None:
        super().__init__("Survey Flow not found.")


class FieldWrongType(PyQSFBaseException):
    """Implements Field Wrong Type"""

    def __init__(self, name, field, expected, got) -> None:
        super().__init__(
            f"{name} field `{field.value}` wrong type. Expected `{expected}`, got `{got}`."
        )
