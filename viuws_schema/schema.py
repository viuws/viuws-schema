from packaging.version import Version

from . import v01

SCHEMA_MODULES = [v01]
MAJOR_SCHEMA_VERSIONS = sorted(
    Version(schema_module.VERSION).major for schema_module in SCHEMA_MODULES
)
MAJOR_SCHEMA_VERSION_MODULES = {
    Version(schema_module.VERSION).major: schema_module
    for schema_module in SCHEMA_MODULES
}

current_schema_module = v01
