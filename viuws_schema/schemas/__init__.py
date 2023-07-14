from . import v01
from .base import SchemaBaseModel

current = v01

ALL_SCHEMA_MODULES = [v01]
SCHEMA_MODULES_BY_VERSION = {
    schema_module.VERSION: schema_module for schema_module in ALL_SCHEMA_MODULES
}


__all__ = [
    "current",
    "SchemaBaseModel",
    "ALL_SCHEMA_MODULES",
    "SCHEMA_MODULES_BY_VERSION",
]
