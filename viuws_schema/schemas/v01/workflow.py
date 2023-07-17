from typing import Any, Optional

from pydantic import BaseModel, Field

from .base import SchemaBaseModelV01


class ProcessConfig(BaseModel):
    repository: Optional[str] = None
    revision: Optional[str] = None
    path: str
    inputs: dict[str, str] = {}
    outputs: dict[str, str] = {}
    env: dict[str, Any] = {}
    args: list[str] = []
    environment_id: Optional[str] = Field(default=None, alias="environment")


class Environment(BaseModel):
    name: str
    base_dir: str = Field(alias="baseDir")
    data_mappings: dict[str, str] = Field(default={}, alias="dataMappings")


class Workflow(SchemaBaseModelV01):
    name: str
    processes: dict[str, ProcessConfig] = {}
    environments: dict[str, Environment] = {}
