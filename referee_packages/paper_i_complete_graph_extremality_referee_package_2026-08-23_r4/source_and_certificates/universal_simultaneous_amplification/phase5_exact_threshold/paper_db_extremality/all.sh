#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
"$paper_dir/submission/bootstrap_replay.sh" --development
"$paper_dir/build.sh"
