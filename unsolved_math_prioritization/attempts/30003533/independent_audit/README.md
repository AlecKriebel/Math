# Independent review package

This package contains only authored audit material, a correction patch, scripts, and public verification metadata. It contains no third-party PDFs or extracted source text.

Start with AUDIT_REPORT.md and ACCEPTANCE.json. The original author packet remains a separate, unchanged input. CORRECTIONS.patch applies inside a disposable copy of that packet with `patch -p1`; do not patch the frozen original. CORRECTED_MANIFEST.json supplies the expected resulting manifest. Author-era pending-review flags are preserved as historical metadata; ACCEPTANCE.json records this independent decision.

## Reproduction

Requirements: Python 3 using only its standard library. The full audit runner also uses the standard patch command to independently test the delivered diff. No network or downloaded software is used by either script.

Run `python -B independent_controls.py --packet /path/to/original/public` for independent finite controls and schema/integrity validation. Repeat with `-O` and `-OO`. Its default trusted manifest is the frozen original's digest. To check a patched disposable copy, supply `--manifest 10e904a94ffabba520bd60ebbfb27f0dd41eb0d248f49eb7680ed0dd7e6aaf94` as well. This program performs no writes and works when both input and review package are read-only.

The full runner expects this review directory to be a writable copy adjacent to its original input at `../public`, with the original packet retaining frozen modes 0444 for files and 0555 for the directory. Run as an unprivileged account: `python -B run_audit.py`. It verifies the original, reproduces the defects, tests mutations and read-only relocation, independently applies the correction patch, and regenerates review outputs only in the writable review copy. The source packet's bytes and modes are checked unchanged at completion. Running this output-producing runner directly from the frozen review package is unnecessary; use a writable review copy.

The independent controls do not import the author controls or verifier. Their exact and numerical counts are separate. Passing them does not certify the boundary PDE or resolve the high-frequency problem.

AUDIT_MANIFEST.json binds every review file except itself. Compare its digest with the external audit freeze receipt; replacing an executable and all trusted hashes cannot be detected from an untrusted package alone.
