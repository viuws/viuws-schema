import inspect
import json
from typing import Optional, TextIO

import click
from packaging.version import Version

from .base import RootSchemaBaseModel
from .schema import SCHEMA_MODULES, current_schema_module


@click.group()
@click.version_option()
def cli() -> None:
    pass


@cli.command(name="versions", help="List all supported major schema versions.")
def versions() -> None:
    for major_schema_version in SCHEMA_MODULES.keys():
        click.echo(major_schema_version)


@cli.command(name="models", help="List all supported models.")
@click.option(
    "--version",
    "major_schema_version_str",
    type=click.Choice([str(x) for x in SCHEMA_MODULES.keys()]),
    default=str(Version(current_schema_module.VERSION).major),
    show_default=True,
    help="Major schema version.",
)
def models(major_schema_version_str: str) -> None:
    schema_module = SCHEMA_MODULES[int(major_schema_version_str)]
    for model_type_name, model_type in inspect.getmembers(
        schema_module, inspect.isclass
    ):
        if issubclass(model_type, RootSchemaBaseModel):
            click.echo(model_type_name)


@cli.command(name="generate", help="Generate a JSON Schema for the specified model.")
@click.option(
    "--version",
    "major_schema_version_str",
    type=click.Choice([str(x) for x in SCHEMA_MODULES.keys()]),
    default=str(Version(current_schema_module.VERSION).major),
    show_default=True,
    help="Major schema version.",
)
@click.option(
    "--indent",
    "indent",
    type=click.IntRange(min=0),
    default=2,
    show_default=True,
    help="JSON indentation level.",
    metavar="INTEGER",
)
@click.option(
    "-o",
    "json_schema_file",
    type=click.File("w"),
    help="Output JSON Schema file.",
)
@click.argument("model_type_name", metavar="MODEL", type=click.STRING)
def generate(
    major_schema_version_str: str,
    indent: int,
    json_schema_file: Optional[TextIO],
    model_type_name: str,
) -> None:
    schema_module = SCHEMA_MODULES[int(major_schema_version_str)]
    model_type = getattr(schema_module, model_type_name, None)
    if model_type is None or not issubclass(model_type, RootSchemaBaseModel):
        root_model_type_names = [
            model_type_name
            for model_type_name, model_type in inspect.getmembers(
                schema_module, inspect.isclass
            )
            if issubclass(model_type, RootSchemaBaseModel)
        ]
        raise click.BadParameter(
            f"'{model_type_name}' not in {root_model_type_names}", param_hint="MODEL"
        )
    json_schema_data = model_type.model_json_schema(by_alias=True)
    _remove_json_schema_titles_inplace(json_schema_data)
    json_schema_str = json.dumps(json_schema_data, indent=indent)
    click.echo(message=json_schema_str, file=json_schema_file)


@cli.command(name="upgrade", help="Upgrade the specified model instance.")
@click.option(
    "--to-version",
    "to_major_schema_version_str",
    type=click.Choice([str(x) for x in SCHEMA_MODULES.keys()]),
    default=str(Version(current_schema_module.VERSION).major),
    show_default=True,
    help="Major schema version to upgrade to.",
)
@click.option(
    "--strict/--no-strict",
    "strict",
    default=None,
    show_default=True,
    help="Whether to raise an error on invalid fields.",
)
@click.option(
    "--indent",
    "indent",
    type=click.IntRange(min=0),
    default=2,
    show_default=True,
    help="JSON indentation level.",
    metavar="INTEGER",
)
@click.option(
    "-o",
    "output_model_instance_file",
    type=click.File("w"),
    help="Output data file.",
)
@click.argument("model_type_name", metavar="MODEL", type=click.STRING)
@click.argument("model_instance_file", metavar="FILE", type=click.File())
def upgrade(
    to_major_schema_version_str: str,
    strict: Optional[bool],
    indent: int,
    output_model_instance_file: Optional[TextIO],
    model_type_name: str,
    model_instance_file: TextIO,
) -> None:
    model_data = json.load(model_instance_file)
    from_major_schema_version = Version(model_data["schemaVersion"]).major
    from_schema_module = SCHEMA_MODULES[from_major_schema_version]
    from_model_type = getattr(from_schema_module, model_type_name, None)
    if from_model_type is None or not issubclass(from_model_type, RootSchemaBaseModel):
        root_from_model_type_names = [
            model_type_name
            for model_type_name, model_type in inspect.getmembers(
                from_schema_module, inspect.isclass
            )
            if issubclass(model_type, RootSchemaBaseModel)
        ]
        raise click.BadParameter(
            f"'{model_type_name}' not in {root_from_model_type_names}",
            param_hint="MODEL",
        )
    to_schema_module = SCHEMA_MODULES[int(to_major_schema_version_str)]
    to_model_type = getattr(to_schema_module, model_type_name, None)
    if to_model_type is None or not issubclass(to_model_type, RootSchemaBaseModel):
        root_to_model_type_names = [
            model_type_name
            for model_type_name, model_type in inspect.getmembers(
                to_schema_module, inspect.isclass
            )
            if issubclass(model_type, RootSchemaBaseModel)
        ]
        raise click.BadParameter(
            f"'{model_type_name}' not in {root_to_model_type_names}", param_hint="MODEL"
        )
    model_instance = from_model_type.parse(model_data, strict=strict)
    upgraded_model_instance = to_model_type.upgrade(model_instance)
    upgraded_model_json = upgraded_model_instance.model_dump_json(
        indent=indent, by_alias=True
    )
    click.echo(message=upgraded_model_json, file=output_model_instance_file)


@cli.command(name="validate", help="Validate the specified model instance.")
@click.option(
    "--strict/--no-strict",
    "strict",
    default=None,
    show_default=True,
    help="Whether to raise an error on invalid fields.",
)
@click.argument("model_type_name", metavar="MODEL", type=click.STRING)
@click.argument("model_instance_file", metavar="FILE", type=click.File())
def validate(
    strict: Optional[bool],
    model_type_name: str,
    model_instance_file: TextIO,
) -> None:
    model_data = json.load(model_instance_file)
    major_schema_version = Version(model_data["schemaVersion"]).major
    schema_module = SCHEMA_MODULES[major_schema_version]
    model_type = getattr(schema_module, model_type_name, None)
    if model_type is None or not issubclass(model_type, RootSchemaBaseModel):
        root_model_type_names = [
            model_type_name
            for model_type_name, model_type in inspect.getmembers(
                schema_module, inspect.isclass
            )
            if issubclass(model_type, RootSchemaBaseModel)
        ]
        raise click.BadParameter(
            f"'{model_type_name}' not in {root_model_type_names}", param_hint="MODEL"
        )
    model_type.parse(model_data, strict=strict)


def _remove_json_schema_titles_inplace(*args) -> None:
    for arg in args:
        if isinstance(arg, dict):
            arg.pop("title", None)
            _remove_json_schema_titles_inplace(*arg.values())
        elif isinstance(arg, list):
            _remove_json_schema_titles_inplace(*arg)
