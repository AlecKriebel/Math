#!/bin/sh
set -eu
cd "$(dirname "$0")"
python check_examples.py
python deficit_blocks.py >/dev/null
python gap_six_gadgets.py >/dev/null
python large_gap_gadgets.py >/dev/null
python padding_obstruction.py >/dev/null
python extension_failure.py >/dev/null
printf 'All exact checks passed. Full source conjecture remains unsolved.\n'
