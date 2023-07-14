from typing import Any, Optional

from pydantic import BaseModel, Field, Json

from .base import SchemaBaseModelV01


class ProcessConfig(BaseModel):
    repository: Optional[str] = None
    revision: Optional[str] = None
    path: str
    inputs: dict[str, str] = {}
    outputs: dict[str, str] = {}
    env: dict[str, Any] = {}
    args: list[str] = []
    executor_id: str = Field(alias="executor")


class Workflow(BaseModel):
    name: str
    processes: dict[str, ProcessConfig] = {}
    environment_id: str = Field(alias="environment")


class Executor(BaseModel):
    name: str
    type: str
    config: Json[Any] = {}


class Environment(BaseModel):
    name: str
    base_dir: str = Field(alias="baseDir")
    data_mappings: dict[str, str] = Field(default={}, alias="dataMappings")
    executors: dict[str, Executor] = {}


class Project(SchemaBaseModelV01):
    name: str
    workflows: list[Workflow] = []
    environments: dict[str, Environment] = {}
