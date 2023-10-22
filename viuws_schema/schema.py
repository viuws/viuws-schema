from packaging.version import Version

from . import v01

SCHEMA_MODULES = {
    Version(schema_module.VERSION).major: schema_module
    for schema_module in sorted([v01], key=lambda x: Version(x.VERSION).major)
}

current_schema_module = v01
