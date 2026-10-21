# PR789 source and geometry audit

This is a source-first independent mathematical audit of the exact claimed-solved candidate at aa44dec3baf8c1cd179cf8b55f32be95c74ee81a. Read INITIAL_POSITION.md (frozen before candidate exposure), SOURCE_GEOMETRY_DERIVATION.md, then CANDIDATE_COMPARISON.md and VERDICT.json. The candidate's projective-line quotient passes; no mathematical repair is required. Priority is not audited here.

The source/full-body directory scratch/ is private working evidence, deliberately excluded from this authored packet and any distributable ZIP. PRIMARY_BINDINGS.json records exact source hashes and inspection metadata. Without --source-root the checker does not claim to have rehashed the primary bodies. Without --input-root it does not claim to have replayed exact input bindings. Original author/audit executables are not launched by this checker.

Check the externally supplied SHA256 of verify_packet.py before executing, then run:

    python3 -I -B verify_packet.py --packet-root PACKET --expected-manifest-sha256 EXTERNAL_MANIFEST_PIN --expected-checker-sha256 EXTERNAL_CHECKER_PIN --input-root INTAKE --source-root OPTIONAL_PRIVATE_BODY_DIRECTORY --replay

Omit the optional --source-root pair when those bodies are unavailable. Repeat with -O if desired. Fixed exact arithmetic diagnostics are supporting reproducibility checks; universal domain, kernel, THCR and source-scope arguments are written mathematics. The checker provides ordinary static file-integrity checks, not a race-free adversarial filesystem sandbox.

External candidate source hash and original head are hard-coded in the checker; all58 original files additionally bind both Git SHA1 and SHA256. Only one problem was inspected. No external mutations, external contact or priority claim are made.
