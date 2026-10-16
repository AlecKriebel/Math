# Version-bound whole-manuscript review evidence

`review01/` preserves the first whole-package adversary's eleven authored files
and original seal, plus root acceptance and repair records. That report binds
the earlier frozen133-entry archive, not the revised current archive. Its M1
finding is addressed by REVIEW01_RESOLUTION.json and the current provenance
wrappers; the next fresh review is a separate release gate. No publication is
claimed by these dated records.

These are historical review utilities, not additional portable-harness jobs.
`review01/package_integrity.py` intentionally checks the original repository
review01_frozen layout and its fixed133-entry inventory; do not run it against
this revised archive. That original snapshot is preserved in the repository
case audit. The independently authored mathematical `independent_controls.py`
requires only the pinned SymPy/mpmath libraries and writes a result beside its
script; copy it to a temporary folder if independently replaying it. Root's
isolated replay matched its original result byte-for-byte. The documented
portable ten-job harness is `verification/run_verification.py` and needs no
repository layout, private source or network.
