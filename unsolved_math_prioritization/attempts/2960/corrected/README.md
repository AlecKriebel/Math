# Corrected checker slice: KP-4.84 / 2960

This separate slice applies the frozen audit patch to the frozen original checker.
The original 7-file research packet and 10-file independent audit remain unchanged.
The report needs no mathematical correction. This checker correction replaces 17
removable assertions, adds explicit Gram-matrix and subgroup-count checks, and
writes only to stdout unless `--output PATH` is requested.

Run `python -I -S -B exact_checks.py`, optionally adding `-O` or `-OO` before
the script path. All modes must produce the complete frozen `EXACT_CHECKS.json`
bytes. This is bounded exact algebra, not a proof of the smooth realization
problem. Use the publication's externally authenticated bootstrap for acceptance.
