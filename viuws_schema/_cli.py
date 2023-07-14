import inspect
import json
from typing import IO, Any, Optional, get_args

import click
from pydantic.json_schema import JsonSchemaMode

from .schemas import SCHEMA_MODULES_BY_VERSION, SchemaBaseModel
from .schemas import current as current_schema_module


@click.group(name="viuws-schema")
@click.version_option()
def cli() -> None:
    pass


@cli.command(name="versions", help="List all supported versions.")
def versions() -> None:
    for version in SCHEMA_MODULES_BY_VERSION.keys():
        click.echo(version)


@cli.command(name="schemas", help="List all supported schemas.")
@click.option(
    "--version",
    "version",
    type=click.Choice(list(SCHEMA_MODULES_BY_VERSION.keys())),
    default=current_schema_module.VERSION,
    show_default=True,
    help="ViUWS Schema version.",
)
def schemas(version: str) -> None:
    schema_module = SCHEMA_MODULES_BY_VERSION[version]
    for schema_name, schema_type in inspect.getmembers(schema_module, inspect.isclass):
        if issubclass(schema_type, SchemaBaseModel):
            click.echo(schema_name)


@cli.command(name="generate", help="Generate a JSON Schema.")
@click.option(
    "--version",
    "version",
    type=click.Choice(list(SCHEMA_MODULES_BY_VERSION.keys())),
    default=current_schema_module.VERSION,
    show_default=True,
    help="ViUWS Schema version.",
)
@click.option(
    "--mode",
    "mode",
    type=click.Choice(get_args(JsonSchemaMode)),
    default="validation",
    show_default=True,
    help="JSON Schema generation mode.",
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
    "--file",
    "output_file",
    type=click.File("w"),
    help="Output file path.",
)
@click.argument("schema", type=click.STRING)
def generate(
    version: str,
    mode: JsonSchemaMode,
    indent: int,
    output_file: Optional[IO[Any]],
    schema: str,
) -> None:
    schema_module = SCHEMA_MODULES_BY_VERSION[version]
    schema_type = getattr(schema_module, schema, None)
    if schema_type is None or not issubclass(schema_type, SchemaBaseModel):
        schema_names = [
            schema_name
            for schema_name, schema_type in inspect.getmembers(
                schema_module, inspect.isclass
            )
            if issubclass(schema_type, SchemaBaseModel)
        ]
        raise click.BadParameter(
            f"'{schema}' not in {schema_names}", param_hint="schema"
        )
    json_schema_data = schema_type.model_json_schema(by_alias=True, mode=mode)
    json_schema_str = json.dumps(json_schema_data, indent=indent)
    click.echo(message=json_schema_str, file=output_file)
