from typing import Any, Optional

from pydantic import Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class EnvVar(SchemaBaseModel):
    name: str
    value: Optional[str] = None
    property: Optional[str] = None


class Argument(SchemaBaseModel):
    name: str
    value: Optional[str] = None
    property: Optional[str] = None


class OCIRuntimeConfig(SchemaBaseModel):
    image: str
    tag: str = "latest"
    cwd: Optional[str] = None
    env: list[EnvVar] = []
    args: list[Argument] = []
    # TODO editor env/args


class Channel(SchemaBaseModel):
    id: str
    # TODO cardinality


class InputChannel(Channel):
    pass
    # TODO required
    # TODO wait = False
    # TODO consumed file patterns


class OutputChannel(Channel):
    pass
    # TODO produced file patterns


class Module(RootSchemaBaseModelV01):
    name: str
    description: str
    container: OCIRuntimeConfig
    input_channels: list[InputChannel] = Field(default=[], alias="inputChannels")
    output_channels: list[OutputChannel] = Field(default=[], alias="outputChannels")
    config_schema: Optional[dict[str, Any]] = Field(default=None, alias="configSchema")
    config_ui_schema: Optional[dict[str, Any]] = Field(
        default=None, alias="configUISchema"
    )
    icon_url: Optional[str] = Field(default=None, alias="iconUrl")
    # TODO allow custom input/output channels
