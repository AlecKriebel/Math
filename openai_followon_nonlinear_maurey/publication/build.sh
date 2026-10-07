#!/bin/sh
set -eu
cd "$(dirname "$0")"
mkdir -p output
tectonic main.tex --outdir output --keep-logs
