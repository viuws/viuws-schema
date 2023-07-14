#!/usr/bin/env bash
for version in $(viuws-schema versions); do
    mkdir -p _site/${version}
    for model in $(viuws-schema models --version ${version}); do
        viuws-schema generate --version ${version} ${model} > _site/${version}/${model,,}.json
    done
    generate-schema-doc --expand-buttons --no-link-to-reused-ref _site/${version} _site/${version}
done
