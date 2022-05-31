# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator  # noqa: F401
from models.validation_error import ValidationError


class HTTPValidationError(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    HTTPValidationError - a model defined in OpenAPI

        detail: The detail of this HTTPValidationError [Optional].
    """

    detail: Optional[List[ValidationError]] = None

HTTPValidationError.update_forward_refs()