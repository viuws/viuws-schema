from enum import Enum
from typing import Any, Literal, Union

from pydantic import Field

from ..base import SchemaBaseModel
from .base import RootSchemaBaseModelV01


class PluginType(str, Enum):
    WORKFLOW_IMPORT = "workflowImport"
    WORKFLOW_EXPORT = "workflowExport"


class PluginInstance(SchemaBaseModel):
    name: str
    type: PluginType


class WorkflowImportPluginInstance(PluginInstance):
    type: Literal[PluginType.WORKFLOW_IMPORT]
    import_menu_item: str = Field(..., alias="importMenuItem")
    import_function: Any = Field(..., alias="importFunction")


class WorkflowExportPluginInstance(PluginInstance):
    type: Literal[PluginType.WORKFLOW_EXPORT]
    export_menu_item: str = Field(..., alias="exportMenuItem")
    export_function: Any = Field(..., alias="exportFunction")


class Plugin(RootSchemaBaseModelV01):
    plugin: Union[WorkflowImportPluginInstance, WorkflowExportPluginInstance] = Field(
        ..., discriminator="type"
    )