#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
"$paper_dir/replay.sh"
"$paper_dir/build.sh"
