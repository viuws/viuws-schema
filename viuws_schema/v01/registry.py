from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class ModuleRef(SchemaBaseModel):
    id: str
    path: str


class PluginRef(SchemaBaseModel):
    id: str
    path: str


class Registry(RootSchemaBaseModelV01):
    modules: list[ModuleRef] = []
    plugins: list[PluginRef] = []
    repos: list[str] = []
