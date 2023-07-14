import inspect
import json
from typing import IO, Any, Optional, get_args

import click
from pydantic.json_schema import JsonSchemaMode, models_json_schema

from .schemas import SCHEMA_MODULES_BY_VERSION, SchemaBaseModel
from .schemas import current as current_schema_module


@click.group(name="viuws-schema")
@click.version_option()
def cli() -> None:
    pass


@cli.command(name="versions", help="List all supported schema versions.")
def versions() -> None:
    for version in SCHEMA_MODULES_BY_VERSION.keys():
        click.echo(version)


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
    "--title",
    "title",
    type=click.STRING,
    help="Title of the generated JSON Schema.",
)
@click.option(
    "--description",
    "description",
    type=click.STRING,
    help="Description of the generated JSON Schema.",
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
@click.argument("entities", type=click.STRING, nargs=-1)
def generate(
    version: str,
    mode: JsonSchemaMode,
    title: Optional[str],
    description: Optional[str],
    indent: int,
    output_file: Optional[IO[Any]],
    entities: list[str],
) -> None:
    schema_module = SCHEMA_MODULES_BY_VERSION[version]
    schema_type_mappings = {
        schema_type_name: schema_type
        for schema_type_name, schema_type in inspect.getmembers(
            schema_module, inspect.isclass
        )
        if issubclass(schema_type, SchemaBaseModel)
    }
    if entities:
        schema_types: list[type[SchemaBaseModel]] = []
        for schema_type_name in entities:
            schema_type = schema_type_mappings.get(schema_type_name)
            if schema_type is None:
                raise click.BadParameter(
                    f"'{schema_type_name}' not in {tuple(schema_type_mappings.keys())}",
                    param_hint="entities",
                )
            schema_types.append(schema_type)
    else:
        schema_types = list(schema_type_mappings.values())
    if len(entities) == 1:
        schema_type = schema_types[0]
        json_schema_data = schema_type.model_json_schema(by_alias=True, mode=mode)
    else:
        json_schema_data = models_json_schema(
            [(schema_type, mode) for schema_type in schema_types],
            by_alias=True,
            title=title,
            description=description,
        )[1]
    json_schema_str = json.dumps(json_schema_data, indent=indent)
    click.echo(message=json_schema_str, file=output_file)
