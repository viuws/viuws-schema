from enum import Enum
from typing import Any, Literal, Union

from pydantic import Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01

JSFunction = Any


class PluginType(str, Enum):
    IMPORT = "import"
    EXPORT = "export"


class PluginBase(SchemaBaseModel):
    name: str
    type: PluginType


class ImportPlugin(PluginBase):
    type: Literal[PluginType.IMPORT]
    import_menu_item: str = Field(alias="importMenuItem")
    import_function: JSFunction = Field(alias="importFunction")


class ExportPlugin(PluginBase):
    type: Literal[PluginType.EXPORT]
    export_menu_item: str = Field(alias="exportMenuItem")
    export_function: JSFunction = Field(alias="exportFunction")


class Plugin(RootSchemaBaseModelV01):
    plugin: Union[ImportPlugin, ExportPlugin] = Field(discriminator="type")
