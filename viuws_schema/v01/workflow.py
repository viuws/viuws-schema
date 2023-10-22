from typing import Any, Optional

from pydantic import Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class ChannelResourceMapping(SchemaBaseModel):
    channel_id: str = Field(alias="channel")
    resource_id: str = Field(alias="resource")


class Task(SchemaBaseModel):
    id: str
    repo: Optional[str] = None  # None = inlined
    rev: Optional[str] = None  # Only for GitHub repos
    module_id: str = Field(alias="module")
    inputs: list[ChannelResourceMapping] = []
    outputs: list[ChannelResourceMapping] = []
    config: dict[str, Any] = {}


class Workflow(RootSchemaBaseModelV01):
    name: str
    tasks: list[Task] = []
    # TODO environments
    # TODO modules (inlined)
