# 6200022: Delzant diagonal convex cores

Start with RESULT.md. The disposition is an attributed prior negative resolution, with an elementary illustrative counterexample and a separately proved conditional boundary lemma. No novelty is claimed.

All files in this folder are authored analysis, authored code/results, or public provenance metadata. Third-party PDFs, extracted source text, images, full corpora, and private coordination material are deliberately excluded.

## Reproduce

Requires only Python 3.10+ standard library. From any working directory:

    python /path/to/folder/verify.py
    python -O /path/to/folder/verify.py

Each command first checks the exact manifest allowlist and file bytes, then reruns the exact arithmetic checks and compares their full JSON output. It exits nonzero on missing, altered, added, symlinked, or malformed payloads. It does not write into this folder. Do not put generated output or cache files inside it. The verifier's checks use explicit exceptions, never Python assert statements.

For a portable replay, copy the complete directory elsewhere and run the same two commands. VERIFY_TESTS.json records the actual normal, optimized, relocated, and negative-control outcomes for this freeze. MANIFEST.json binds every other payload file, including the replay receipt. The outer ZIP and the author's separate freeze receipt bind the final complete package.

The manifest protects against accidental or localized payload mutation under a trusted manifest. It is not a digital signature: changing a file and deliberately rebuilding all expected hashes creates a different package. Trust the separately delivered ZIP/manifest SHA-256 values when establishing identity.

Read PUBLIC_METADATA.json for source hashes, full-record review digests, publication status, and bounded search history. This package does not need the original corpora or PDF files to replay its computation.
