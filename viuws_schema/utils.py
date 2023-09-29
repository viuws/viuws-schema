from . import v01

SCHEMA_MODULES = [v01]

current_schema_module = v01


def major_version(version: str) -> str:
    return version.split(".")[0]


def minor_version(version: str) -> str:
    return version.split(".")[1]


def patch_version(version: str) -> str:
    return version.split(".")[2]
