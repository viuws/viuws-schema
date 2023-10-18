from enum import Enum
from typing import Any, Optional

from pydantic import Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class EnvVarValueMapping(SchemaBaseModel):
    env_var: str = Field(alias="envVar")
    value: Any


class OCIRuntimeConfig(SchemaBaseModel):
    image: str
    tag: str = "latest"
    cwd: Optional[str] = None
    env: list[EnvVarValueMapping] = []
    args: list[str] = []


class IOCardinality(str, Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"


class Channel(SchemaBaseModel):
    id: str
    cardinality: IOCardinality = IOCardinality.MULTIPLE


class InputChannel(Channel):
    required: bool = False
    supported_file_patterns: Optional[list[str]] = Field(
        default=None, alias="supportedFilePatterns"
    )


class OutputChannel(Channel):
    generated_file_pattern: Optional[str] = Field(
        default=None, alias="generatedFilePattern"
    )


class Module(RootSchemaBaseModelV01):
    name: str
    description: str
    container: OCIRuntimeConfig
    input_channels: list[InputChannel] = Field(default=[], alias="inputChannels")
    output_channels: list[OutputChannel] = Field(default=[], alias="outputChannels")
    env_schema: Optional[Any] = Field(default=None, alias="envSchema")
    env_ui_schema: Optional[Any] = Field(default=None, alias="envUISchema")
    args_schema: Optional[Any] = Field(default=None, alias="argsSchema")
    args_ui_schema: Optional[Any] = Field(default=None, alias="argsUISchema")
    icon_url: Optional[str] = Field(default=None, alias="iconUrl")
