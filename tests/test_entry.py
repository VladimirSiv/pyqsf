import pytest
from pyqsf.core.entry import SurveyEntry, SurveyEntryField
from pyqsf.exceptions import FieldWrongType


SURVEY_ENTRY = {
    "SurveyID": "SV_test123abacdefg",
    "SurveyName": "Test",
    "SurveyDescription": None,
    "SurveyOwnerID": "UR_test123abacadefg",
    "SurveyBrandID": "qualtricsxmq7n55g7ct",
    "DivisionID": None,
    "SurveyLanguage": "EN",
    "SurveyActiveResponseSet": "RS_test123abacdf",
    "SurveyStatus": "Inactive",
    "SurveyStartDate": "0000-00-00 00:00:00",
    "SurveyExpirationDate": "0000-00-00 00:00:00",
    "SurveyCreationDate": "2025-04-21 10:07:03",
    "CreatorID": "UR_test123abacadefg",
    "LastModified": "2025-04-21 10:07:04",
    "LastAccessed": "0000-00-00 00:00:00",
    "LastActivated": "0000-00-00 00:00:00",
    "Deleted": None,
}


def test_survey_entry_init():

    entry = SurveyEntry(SURVEY_ENTRY)
    assert SURVEY_ENTRY == entry.data
    for field in SurveyEntryField:
        assert entry.__getattribute__(field.name.lower()) == SURVEY_ENTRY[field.value]


def test_survey_entry_error():

    survey_entry = {
        **SURVEY_ENTRY,
        **{SurveyEntryField.SURVEY_NAME.value: 1},
    }
    with pytest.raises(FieldWrongType) as exc:
        SurveyEntry(survey_entry)
    assert (
        str(exc.value)
        == "Survey Entry field `SurveyName` wrong type. Expected `<class 'str'>`, got `<class 'int'>`."
    )


def test_survey_entry_not_required():

    del SURVEY_ENTRY[SurveyEntryField.DELETED.value]
    entry = SurveyEntry(SURVEY_ENTRY)
    for field in SurveyEntryField:
        if field == SurveyEntryField.DELETED:
            continue
        assert entry.__getattribute__(field.name.lower()) == SURVEY_ENTRY[field.value]
