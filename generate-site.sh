#!/usr/bin/env bash
for version in $(viuws-schema versions); do
    mkdir -p _site/${version}
    viuws-schema generate --version ${version} --title "ViUWS Schema"  --description "Visual Uppsala Workflow System (ViUWS) Schema, version ${version}"  > _site/${version}/schema.json
done
