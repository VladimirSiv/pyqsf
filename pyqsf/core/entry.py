"""
PyQSF entry module
"""

from typing import Dict, Any
from enum import Enum

from pyqsf.exceptions import FieldWrongType


# fmt: off
class SurveyEntryField(Enum):
    """Fields of Survey Entry Object"""

    SURVEY_ACTIVE_RESPONSE_SET  = "SurveyActiveResponseSet"
    SURVEY_BRAND_ID             = "SurveyBrandID"
    SURVEY_CREATION_DATE        = "SurveyCreationDate"
    CREATOR_ID                  = "CreatorID"
    DELETED                     = "Deleted"
    DIVISION_ID                 = "DivisionID"
    SURVEY_DESCRIPTION          = "SurveyDescription"
    SURVEY_EXPIRATION_DATE      = "SurveyExpirationDate"
    SURVEY_ID                   = "SurveyID"
    SURVEY_LANGUAGE             = "SurveyLanguage"
    LAST_ACCESSED               = "LastAccessed"
    LAST_ACTIVATED              = "LastActivated"
    LAST_MODIFIED               = "LastModified"
    SURVEY_NAME                 = "SurveyName"
    SURVEY_OWNER_ID             = "SurveyOwnerID"
    SURVEY_START_DATE           = "SurveyStartDate"
    SURVEY_STATUS               = "SurveyStatus"


# fmt: on
class SurveyEntry:  # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """Implements Survey Entry"""

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        # fmt: off
        self.creator_id: str                    = self._get(SurveyEntryField.CREATOR_ID,                    str)
        self.deleted: str                       = self._get(SurveyEntryField.DELETED,                       str, required=False)
        self.division_id: str                   = self._get(SurveyEntryField.DIVISION_ID,                   str, required=False)
        self.last_accessed: str                 = self._get(SurveyEntryField.LAST_ACCESSED,                 str)
        self.last_activated: str                = self._get(SurveyEntryField.LAST_ACTIVATED,                str)
        self.last_modified: str                 = self._get(SurveyEntryField.LAST_MODIFIED,                 str)
        self.survey_active_response_set: str    = self._get(SurveyEntryField.SURVEY_ACTIVE_RESPONSE_SET,    str)
        self.survey_brand_id: str               = self._get(SurveyEntryField.SURVEY_BRAND_ID,               str)
        self.survey_creation_date: str          = self._get(SurveyEntryField.SURVEY_CREATION_DATE,          str)
        self.survey_description: str            = self._get(SurveyEntryField.SURVEY_DESCRIPTION,            str, required=False)
        self.survey_expiration_date: str        = self._get(SurveyEntryField.SURVEY_EXPIRATION_DATE,        str)
        self.survey_id: str                     = self._get(SurveyEntryField.SURVEY_ID,                     str)
        self.survey_language: str               = self._get(SurveyEntryField.SURVEY_LANGUAGE,               str)
        self.survey_name: str                   = self._get(SurveyEntryField.SURVEY_NAME,                   str)
        self.survey_owner_id: str               = self._get(SurveyEntryField.SURVEY_OWNER_ID,               str)
        self.survey_start_date: str             = self._get(SurveyEntryField.SURVEY_START_DATE,             str)
        self.survey_status: str                 = self._get(SurveyEntryField.SURVEY_STATUS,                 str)
        # fmt: on

    def _get(self, field: SurveyEntryField, _type: Any, required=True):
        value = self.data.get(field.value)
        if required and not isinstance(value, _type):
            raise FieldWrongType("Survey Entry", field, _type, type(value))
        return value
