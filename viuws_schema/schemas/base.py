from pydantic import BaseModel, Field


class SchemaBaseModel(BaseModel):
    schema_version: str = Field(alias="schemaVersion")
