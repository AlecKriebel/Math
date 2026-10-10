# Portable integrity and exact replay

Use Python 3.10 or later; all checkers use only the standard library. No network,
scholarly PDFs, datasets or original workstation paths are required. From any
working directory, run:

```sh
python3 -B /path/to/30005171/verify_publication.py
python3 -B -O /path/to/30005171/verify_publication.py
```

The wrapper rejects altered, missing or extra files, symbolic links, unsafe
manifest paths and nonregular filesystem objects. It authenticates the frozen
author and audit manifests and original archive, then checks every listed byte
count and SHA-256. The outer manifest includes every publication file except
itself; a trusted commit or external manifest hash is the anchor for that outer
manifest. It does not claim cryptographic protection against an attacker who
can replace the entire trusted package.

Replays run in an isolated temporary copy with both ordinary and optimized
Python, leaving the distributed files unchanged. The frozen author verifier's
stdout has one extra trailing newline beyond `checks_result.json`; the wrapper
retains the exact stdout in `checks/author.stdout.json`, checks it byte-for-byte,
and separately checks the JSON value against the frozen recorded result.
The independent output must match `independent_checks.json` byte-for-byte.
The author's inventory verifier must match `checks/integrity.stdout.json`.

The relative layout is intentional. The frozen independent script expects
`public_candidate/` and `authored_candidate.tar.gz` next to its own parent folder.
Keep that layout when copying or downloading the packet. The authored archive
is included exactly as audited, not rebuilt; its ten regular members are checked
against the ten frozen directory files. No extracted archive member is executed.

Individual commands, from this directory:

```sh
python3 -B public_candidate/verify_math.py
python3 -B public_candidate/verify_integrity.py
python3 -B independent_audit/independent_checks.py
```

Exact checks cover all 22 genus-45 signatures, all 12 threshold candidates and
their obstructing counts, the Markov-eleven exclusion, eight limiting-net
factorizations and hyperelliptic dimension regressions. The independent code
uses conductor equations and shortest residue-class paths rather than importing
the author's implementation. Finite arithmetic supports the written geometric
proofs; it does not resolve the full conjecture or certify the imported literature.

The original TeX source and ten-page PDF are pinned separately. Optional local
typesetting can use a standard LaTeX distribution with the packages named in
the manuscript preamble. A new TeX build may differ in PDF metadata or layout;
do not replace the pinned original when checking historical integrity.
