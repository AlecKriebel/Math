# Reproducibility environment

The release orchestration is standard-library Python and targets the user's
Apple-silicon Mac directly.  The development baseline observed on 2026-08-25
was macOS 26.5.2 (`arm64`) and Python 3.14.6 in the project virtual
environment.  The proof-specific Python dependencies remain locked in
`reproducibility/requirements.txt`, including NumPy 2.5.2 for the fresh
204-direction cut producer.

Every suite child receives `PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`,
`LC_ALL=C`, `LANG=C`, `TZ=UTC`, and `SOURCE_DATE_EPOCH` equal to the committed
Git timestamp.  On Darwin, the reported `ru_maxrss` unit is bytes.  Complete
stdout/stderr transcripts and per-command elapsed times are retained.

PDF reproduction uses the installed Tectonic 0.16.9 toolchain.  The verifier
runs only the arm64 executable with SHA-256
`38eff9059ed622672c9a2590415a8f01c043df4232baa459628a2cd86e512d95` and
runs two isolated builds with the exact command recorded in each source
archive, the fixed PDF `SOURCE_DATE_EPOCH=1787677101`, UTC, C locale, and
private TeX working directories, then requires the two PDF byte strings and
the delivered committed PDF to have the same SHA-256.  This publication epoch
is intentionally distinct from the later release commit timestamp.  A PDF
toolchain is not silently installed or inferred by this release layer.

Canonical compressed bytes are conditioned on the recorded Python/zlib and
TeX toolchains.  Clean-clone release runs must use the same locked environment;
logical certificate payloads remain independently hash-bound.
