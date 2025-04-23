import pytest
from pyqsf.core.element import Element, ElementField
from pyqsf.exceptions import FieldWrongType


ELEMENT = {
    "SurveyID": "SV_test123abc",
    "Element": "EL",
    "PrimaryAttribute": "Primary Attribute",
    "SecondaryAttribute": "Secondary Attribute",
    "TertiaryAttribute": None,
    "Payload": None,
}


def test_element_init():
    element = Element(ELEMENT)
    for field in ElementField:
        assert element.__getattribute__(field.name.lower()) == ELEMENT[field.value]


def test_element_field_wrong_type():
    data = {**ELEMENT, "Element": 1}
    with pytest.raises(FieldWrongType) as exc:
        Element(data)
    assert (
        str(exc.value)
        == "Element field `Element` wrong type. Expected `<class 'str'>`, got `<class 'int'>`."
    )
