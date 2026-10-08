# KP-4.84 independent audit

**Decision:** mathematical partial report accepted; target unresolved after five approaches. The original exact checker requires optimization-safe validation and read-only execution support. The separate supplied patch provides both.

This folder contains only authored analysis, executable checks, patch text, and source-free verification metadata. It contains no copied primary-source documents, source excerpts, dataset records, or private coordination files.

- `AUDIT.md`: complete mathematical, source-scope, and reproducibility audit.
- `INPUT_AND_SOURCE_PINS.json`: original packet identity, verified public source hashes and sizes, dataset match results, and inspection limits.
- `exact_checks_hardening.patch`: minimal separate patch against the original `exact_checks.py`.
- `exact_checks_hardened.py`: the patched checker, with explicit runtime guards and stdout-only default output.
- `reproduce_checks.py` and `REPRODUCTION.json`: reproducible UID/EUID 1000 testing, including original and hardened normal/-O/-OO runs, real read-only permission probes, four mutations, and optional external output.
- `independent_checks.py` and `INDEPENDENT_CHECKS.json`: independent bounded exact calculations, including a six-point-permutation model of the wreath product.
- `MANIFEST.sha256.json`: audit file pins; the manifest excludes itself.

Run the hardened checker without changing the original packet:

    python -B exact_checks_hardened.py
    python -B -O exact_checks_hardened.py
    python -B -OO exact_checks_hardened.py

An optional `--output PATH` writes a deliberate copy of the JSON. Default execution writes only to stdout. All three modes produce the frozen original JSON byte-for-byte.

Reproduce the audit tests as UID 1000, giving an existing original public packet and a new, nonexistent work directory:

    python -B reproduce_checks.py PATH_TO_ORIGINAL_PUBLIC NEW_WORK_DIRECTORY
    python -B independent_checks.py

The original packet remains unchanged at input manifest SHA-256 `3308459e594672876a4953fac77a08719bb4cd52f13e3992a54600fff5904a5b`. Integrating the patch into a successor packet requires deliberately generating that packet's own manifest; the audit does not silently alter historical pins.

Illman's finite smooth equivariant-triangulation theorem remains an identified external input whose original full text was not newly inspected. No assertion of full resolution or exhaustive novelty checking is made. This audit adds zero mathematical attempts and performs no publication or global queue edit.
