from typing import Literal

from pydantic import Field

from ..base import SchemaBaseModel


class SchemaBaseModelV01(SchemaBaseModel):
    schema_version: Literal["0.1"] = Field(default="0.1", alias="schemaVersion")
