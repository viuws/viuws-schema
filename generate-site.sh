#!/usr/bin/env bash
basedir=$( cd "$( dirname "${BASH_SOURCE[0]}" )"; pwd -P )
for version in $(viuws-schema versions); do
    rm -rf "${basedir}/_site/${version}"
    mkdir -p "${basedir}/_site/${version}"
    for model in $(viuws-schema models --version ${version}); do
        viuws-schema generate --version ${version} ${model} > "${basedir}/_site/${version}/${model,,}.json"
    done
    generate-schema-doc --expand-buttons --no-link-to-reused-ref --deprecated-from-description "${basedir}/_site/${version}" "${basedir}/_site/${version}"
done
