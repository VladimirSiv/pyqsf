import pytest
from pyqsf.core.flow import Flow, FlowEntry, FlowField, FlowEntryField
from pyqsf.exceptions import FlowNotFound, FieldWrongType


FLOW = {
    "SurveyID": "SV_abc123testefg",
    "Element": "FL",
    "PrimaryAttribute": "Survey Flow",
    "SecondaryAttribute": None,
    "TertiaryAttribute": None,
    "Payload": {
        "Flow": [
            {
                "FlowID": "FL_3",
                "ID": "BL_abc123testefg",
                "Type": "Standard",
            }
        ],
        "FlowID": "FL_1",
        "Properties": {"Count": 3},
        "Type": "Root",
    },
}


def test_flow_init():
    flow = Flow(FLOW)
    assert flow.get_block_ids() == [FLOW["Payload"]["Flow"][0]["ID"]]
    assert flow.flow_id == FLOW["Payload"]["FlowID"]
    assert len(flow._entries) == 1

    entry = flow._entries[0]
    assert isinstance(entry, FlowEntry)
    for field in FlowEntryField:
        assert (
            entry.__getattribute__(field.name.lower())
            == FLOW["Payload"]["Flow"][0][field.value]
        )


def test_flow_not_found():
    payload = {**FLOW["Payload"], "Flow": []}
    data = {**FLOW, "Payload": payload}
    with pytest.raises(FlowNotFound):
        Flow(data)


def test_flow_field_wrong_type():
    payload = {**FLOW["Payload"], "Type": 1}
    data = {**FLOW, "Payload": payload}
    with pytest.raises(FieldWrongType) as exc:
        Flow(data)
    assert (
        str(exc.value)
        == "Flow field `Type` wrong type. Expected `<class 'str'>`, got `<class 'int'>`."
    )


def test_flow_entry_field_wrong_type():
    payload = {
        **FLOW["Payload"],
        "Flow": [
            {
                "FlowID": 1,
                "ID": "BL_abc123testefg",
                "Type": "Standard",
            }
        ],
    }
    data = {**FLOW, "Payload": payload}
    with pytest.raises(FieldWrongType) as exc:
        Flow(data)
    assert (
        str(exc.value)
        == "Flow Entry field `FlowID` wrong type. Expected `<class 'str'>`, got `<class 'int'>`."
    )
