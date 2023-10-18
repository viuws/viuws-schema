from typing import Any, Optional

from pydantic import Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class ChannelResource(SchemaBaseModel):
    channel_id: str = Field(alias="channel")
    resource_id: str = Field(alias="resource")


class EnvVarValue(SchemaBaseModel):
    envvar: str
    value: Any


class URIResource(SchemaBaseModel):
    id: str = Field(alias="resource")
    uri: str


class ModuleConfig(SchemaBaseModel):
    inputs: list[ChannelResource] = []
    outputs: list[ChannelResource] = []
    env: list[EnvVarValue] = []
    args: list[str] = []


class Task(SchemaBaseModel):
    id: str
    name: str
    module_repo: Optional[str] = Field(default=None, alias="moduleRepo")
    module_rev: Optional[str] = Field(default=None, alias="moduleRev")
    module_id: str = Field(alias="module")
    module_config: ModuleConfig = Field(alias="moduleConfig")
    environment_id: Optional[str] = Field(default=None, alias="environment")


class Environment(SchemaBaseModel):
    id: str
    name: str
    base_dir: str = Field(alias="baseDir")
    uri_resources: list[URIResource] = Field(default=[], alias="uriResources")


class Workflow(RootSchemaBaseModelV01):
    name: str
    tasks: list[Task] = []
    environments: list[Environment] = []
