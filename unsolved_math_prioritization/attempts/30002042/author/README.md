# 30002042: scoped degree and finiteness audit

Read RESULT.md for the mathematical outcome and APPROACHES.md for the five approaches. STATUS.json is the machine-readable scope boundary. SOURCES.json records public source locations and the exact inspected PDF hashes. INPUT_BINDING.json records only public verification hashes and sizes, not dataset contents.

The arbitrary-polytope finiteness question remains unresolved by this attempt. A September 2026 preprint claims the properly qualified degree theorem. The source's t notation is not a defined univariate specialization. Literal degree conventions are treated separately and do not constitute a resolution of the standard compound question.

The author package is awaiting a fresh independent mathematical audit before publication. It contains no source PDF, copied paper text, raw dataset, or private coordination record.

## Verification

Use the separately supplied trusted BOOTSTRAP.py, immutable ZIP and external manifest. Invoke:

    python -I -S -B BOOTSTRAP.py AUTHOR_SAFE_FREEZE.zip AUTHOR_EXTERNAL_MANIFEST.json
    python -I -S -B -O BOOTSTRAP.py AUTHOR_SAFE_FREEZE.zip AUTHOR_EXTERNAL_MANIFEST.json

Exact filenames may be longer. The bootstrap contains fixed hashes for the ZIP and manifest, verifies all archive members before any packet code runs, rejects nonregular or unexpected entries, and runs checks.py from its verified bytes in an isolated interpreter. The ordinary/optimized distinction refers to optimization, with isolation enabled in both. Running the bootstrap without -I -S is refused before any filesystem-dependent import. Keep the bootstrap hash itself as a separately trusted anchor.

checks.py verifies small exact lattice counts and symbolic polynomial identities. It does not verify cited deep theorems, source retrieval, or the complete prose proof, and it is not a formal proof certificate. The packet does not claim publication, independent-audit acceptance, or CI success.
