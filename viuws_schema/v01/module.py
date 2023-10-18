from enum import Enum
from typing import Any, Optional

from pydantic import Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class OCIRuntimeConfig(SchemaBaseModel):
    image: str
    tag: str = "latest"
    cwd: Optional[str] = None
    env: dict[str, Any] = {}
    args: list[str]


class IOCardinality(str, Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"


class IOSpec(SchemaBaseModel):
    name: str
    description: str
    cardinality: IOCardinality = IOCardinality.MULTIPLE


class InputSpec(IOSpec):
    required: bool = False
    supported_file_patterns: Optional[list[str]] = Field(
        default=None, alias="supportedFilePatterns"
    )


class OutputSpec(IOSpec):
    generated_file_pattern: Optional[str] = Field(
        default=None, alias="generatedFilePattern"
    )


class Module(RootSchemaBaseModelV01):
    name: str
    description: str
    container: OCIRuntimeConfig
    inputs: dict[str, InputSpec] = Field(default={}, alias="inputs")
    outputs: dict[str, OutputSpec] = Field(default={}, alias="outputs")
    env_schema: Optional[Any] = Field(default=None, alias="envSchema")
    env_ui_schema: Optional[Any] = Field(default=None, alias="envUISchema")
    args_schema: Optional[Any] = Field(default=None, alias="argsSchema")
    args_ui_schema: Optional[Any] = Field(default=None, alias="argsUISchema")
