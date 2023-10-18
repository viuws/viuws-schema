from typing import Any, Optional

from pydantic import Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class ChannelResourceMapping(SchemaBaseModel):
    channel_id: str = Field(alias="channel")
    resource_id: str = Field(alias="resource")


class EnvVarValueMapping(SchemaBaseModel):
    env_var: str = Field(alias="envVar")
    value: Any


class ModuleConfig(SchemaBaseModel):
    inputs: list[ChannelResourceMapping] = []
    outputs: list[ChannelResourceMapping] = []
    env: list[EnvVarValueMapping] = []
    args: list[str] = []


class Task(SchemaBaseModel):
    id: str
    name: str
    module_id: str = Field(alias="module")
    module_config: ModuleConfig = Field(alias="moduleConfig")
    module_repo: Optional[str] = Field(default=None, alias="moduleRepo")
    module_rev: Optional[str] = Field(default=None, alias="moduleRev")
    environment_id: Optional[str] = Field(default=None, alias="environment")


class Environment(SchemaBaseModel):
    id: str
    name: str
    base_dir: str = Field(alias="baseDir")


class Workflow(RootSchemaBaseModelV01):
    name: str
    tasks: list[Task] = []
    environments: list[Environment] = []
