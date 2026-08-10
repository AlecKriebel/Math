#!/usr/bin/env bash
set -euo pipefail

# Compatibility entry point: the active quick gate is the frozen n=4 base
# certificate check.  Historical universe/probe checks are not active theorem
# evidence because the probe bytes bind a superseded base.
exec "$(cd "$(dirname "$0")" && pwd)/verify_schema3_n4_quick.sh"
