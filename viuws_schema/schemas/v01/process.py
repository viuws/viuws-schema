from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field, Json

from .base import SchemaBaseModelV01


class Cardinality(str, Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"


class OCIRuntimeConfig(BaseModel):
    image: str
    tag: str = "latest"
    cwd: Optional[str] = None
    env: dict[str, Any] = {}
    args: list[str]


class Channel(BaseModel):
    name: str
    description: str
    cardinality: Cardinality = Cardinality.MULTIPLE


class InputChannel(Channel):
    required: bool = False
    supported_file_patterns: Optional[list[str]] = Field(
        default=None, alias="supportedFilePatterns"
    )


class OutputChannel(Channel):
    generated_file_pattern: Optional[str] = Field(
        default=None, alias="generatedFilePattern"
    )


class Process(SchemaBaseModelV01):
    name: str
    description: str
    container: OCIRuntimeConfig
    input_channels: dict[str, InputChannel] = Field(default={}, alias="inputChannels")
    output_channels: dict[str, OutputChannel] = Field(
        default={}, alias="outputChannels"
    )
    env_json_schema: Optional[Json[Any]] = Field(default=None, alias="envJSONSchema")
    env_ui_schema: Optional[Json[Any]] = Field(default=None, alias="envUISchema")
    args_json_schema: Optional[Json[Any]] = Field(default=None, alias="argsJSONSchema")
    args_ui_schema: Optional[Json[Any]] = Field(default=None, alias="argsUISchema")
