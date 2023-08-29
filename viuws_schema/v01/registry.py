from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class ProcessRef(SchemaBaseModel):
    id: str
    path: str


class Registry(RootSchemaBaseModelV01):
    processes: list[ProcessRef] = []
