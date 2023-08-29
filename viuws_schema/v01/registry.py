from .base import RootSchemaBaseModelV01


class Registry(RootSchemaBaseModelV01):
    processes: dict[str, str] = {}
