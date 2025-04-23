import pytest
from pyqsf.core.block import (
    Block,
    BlockElement,
    BlockEntry,
    BlockEntryField,
    BlockEntryNotFound,
    FieldWrongType,
)

BLOCK = {
    "SurveyID": "SV_87VGOSKOVpHuohE",
    "Element": "BL",
    "PrimaryAttribute": "Survey Blocks",
    "SecondaryAttribute": None,
    "TertiaryAttribute": None,
    "Payload": {
        "1": {
            "BlockElements": [],
            "Description": "Trash \/ Unused Questions",
            "Options": None,
            "ID": "BL_123abctest1231",
            "Type": "Trash",
        },
        "2": {
            "BlockElements": [
                {"QuestionID": "QID21", "Type": "Question"},
                {"QuestionID": "QID1", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID2", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID3", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID4", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID5", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID6", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID11", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID7", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID8", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID9", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID10", "Type": "Question"},
                {"Type": "Page Break"},
                {"QuestionID": "QID12", "Type": "Question"},
            ],
            "Description": "Employee Exit Interview",
            "ID": "BL_123abctest1232",
            "Options": {"BlockLocking": None, "RandomizeQuestions": "false"},
            "Type": "Standard",
        },
    },
}


def test_block_init_dict():
    block = Block(BLOCK)
    assert len(block.block_elements) > 0
    for index, bl_el in enumerate(block.block_elements):
        assert isinstance(bl_el, BlockEntry)
        for field in BlockEntryField:
            assert (
                bl_el.__getattribute__(field.name.lower())
                == BLOCK["Payload"][f"{index + 1}"][field.value]
            )
        for el in bl_el.elements:
            assert isinstance(el, BlockElement)


def test_block_init_list():
    payload = [BLOCK["Payload"]["1"]]
    data = {**BLOCK, "Payload": payload}
    block = Block(data)
    assert len(block.block_elements) > 0


def test_block_entry_not_found():
    block = Block(BLOCK)
    with pytest.raises(BlockEntryNotFound):
        block.get_block_by_id("TEST")


def test_block_entry_found():
    block = Block(BLOCK)
    entry = block.get_block_by_id("BL_123abctest1232")
    assert isinstance(entry, BlockEntry)
    assert entry.id == "BL_123abctest1232"


def test_block_entry_field_wrong_type():
    entry = {**BLOCK["Payload"]["2"], "Type": 1}
    data = {**BLOCK, "Payload": {**BLOCK["Payload"], "2": entry}}
    with pytest.raises(FieldWrongType) as exc:
        Block(data)
    assert (
        str(exc.value)
        == "Block Entry field `Type` wrong type. Expected `<class 'str'>`, got `<class 'int'>`."
    )


def test_block_element_field_wrong_type():
    entry = {
        **BLOCK["Payload"]["2"],
        "BlockElements": [{"QuestionID": "QID21", "Type": 1}],
    }
    data = {**BLOCK, "Payload": {**BLOCK["Payload"], "2": entry}}
    with pytest.raises(FieldWrongType) as exc:
        Block(data)
    assert (
        str(exc.value)
        == "Block Element field `Type` wrong type. Expected `<class 'str'>`, got `<class 'int'>`."
    )
