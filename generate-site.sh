#!/usr/bin/env bash
for version in $(viuws-schema versions); do
    mkdir -p _site/${version}
    for schema in $(viuws-schema schemas --version ${version}); do
        viuws-schema generate --version ${version} ${schema} > _site/${version}/${schema,,}.json
    done
    generate-schema-doc --expand-buttons _site/${version} _site/${version}
done
