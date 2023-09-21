from typing import Any, Optional

from pydantic import Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class ModuleConfig(SchemaBaseModel):
    inputs: dict[str, str] = {}
    outputs: dict[str, str] = {}
    env: dict[str, Any] = {}
    args: list[str] = []


class Task(SchemaBaseModel):
    module_repo: Optional[str] = None
    module_rev: Optional[str] = None
    module_path: str
    module_config: ModuleConfig = Field(alias="moduleConfig")
    environment_id: Optional[str] = Field(default=None, alias="environment")


class Environment(SchemaBaseModel):
    name: str
    base_dir: str = Field(alias="baseDir")
    data_mappings: dict[str, str] = Field(default={}, alias="dataMappings")


class Workflow(RootSchemaBaseModelV01):
    name: str
    tasks: dict[str, Task] = {}
    environments: dict[str, Environment] = {}
