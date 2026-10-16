# An explicit rank-two entropy-minimizing Fano degeneration

Alec Kriebel · Independent researcher · ORCID0009-0001-9320-500X

Preprint version1.0.0,16October2026. The paper gives an explicit smooth Fano
fivefold with a nontrivial canonical first degeneration and a global
entropy-minimizing valuation of rational rank two. The construction uses
established geometric and analytic inputs; its exact moment equations and
universal irrational-ratio argument are explained in the paper.

The two intended deposit assets are `rank-two-fano-note.pdf` and
`rank-two-fano-verification.zip`. `note.tex` is the actual paper source;
metadata and deposit declarations have matching copies in `verification/`.
This README serves both the outer repository packet and the extracted ZIP:
`verification/` paths refer to the outer packet; the extracted ZIP root is that
directory's content. The actual paper PDF is the separate deposit asset and
is not included inside the verification ZIP.
The original PR888/PID30005079 source at head
`a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7` is preserved unchanged as all21files
under `verification/source/`, totaling98055bytes. Original claimed effort1/5
is retained. The top-level historical proof, corrections and reports are
preserved for provenance; its README is current and its original research log
has a dated assembly checkpoint appended.

## Verification

Independently authenticate the launcher and obtain the external current
manifest or portable-index SHA256 before execution. A program cannot establish
the trustworthiness of its own startup bytes. Neither manifest contains its
own hash. Final core pins and execution receipts are maintained separately
from this candidate to avoid changing the archive after verification.

From the outer directory, use an independently obtained `CURRENT_PIN`:

```text
python3 -I -S -B portable.py current CURRENT_PIN --verify-only
python3 -I -S -B portable.py current CURRENT_PIN --dependency-dir WHEEL_DIRECTORY
python3 -I -S -B -O portable.py current CURRENT_PIN --dependency-dir WHEEL_DIRECTORY
```

From the extracted verification archive, use its independent `PACKAGE_PIN`:

```text
python3 -I -S -B portable.py verify PACKAGE_PIN --verify-only
python3 -I -S -B portable.py verify PACKAGE_PIN --dependency-dir WHEEL_DIRECTORY
python3 -I -S -B portable.py build PACKAGE_PIN OUTSIDE_DIRECTORY/rank-two-fano-verification.zip --dependency-dir WHEEL_DIRECTORY
```

`--verify-only` authenticates bytes and structure while executing zero archival
code. A build requires the complete default replay; it rejects
`--verify-only`, existing outputs, symbolic-link output traversal and output
inside any indexed input directory, including physical APFS aliases.

Use CPython3.11 or later and the exact two official wheels in
`verification/dependencies.json` (or `dependencies.json` inside the ZIP).
Download those explicit URLs yourself and place only those two wheel files
in a dedicated directory. The tool checks full-file hashes and imports their
authenticated bytes directly as ZIPs; it performs no network access or
installation. Wheels and runtimes are excluded from the deposit assets.
The chosen interpreter and standard library remain trusted, unpinned inputs.
There is no operating-system sandbox or adversarial concurrent-filesystem
race guarantee. Exact compressed ZIP reproducibility is limited to the same
Python ZIP implementation and zlib runtime.

The automated replay executes the unchanged original publication launcher and
its two original checkers only. Their positive JSON/stdout outputs must match
exactly. Each complete replay uses one actual original-root process and six
actual checker subprocesses: two positives, two original-assertion negative
controls, and two damaged-code rejections before execution. The root's original
four-edition/three-transition checks and three in-process damaged-patch controls
also run. The original launcher rejects actual optimized Python, so the wrapper
launches it with actual optimization0. Checker processes use actual optimization1
when outer optimization is enabled, while original source is explicitly compiled
with `optimize=0` to retain assertions. Measured flags and requested/effective
modes are recorded separately; no flags are spoofed.

The outer check also verifies closed typed inventories, exact metadata/deposit
identity, actual TeX/meta/deposit/tool copy equality, ZIP records and complete raw
DEFLATE consumption, and a fresh deterministic ZIP reconstruction. It authenticates
the PDF bytes and checks its PDF header. It does not formally verify mathematical
theorem inputs, PDF rendering or TeX-to-PDF correspondence. Parent paper rendering
and all-five-page visual inspection are documented in the included PDF receipts.

## Evidence and scope

Family folders sit directly inside `verification/` and preserve only each
externally authenticated safe manifest's files and its separate envelope.
They include independent geometry, global-minimizer, arithmetic/rank, artifact,
priority, focused-note and format analyses. These are dated historical snapshots:
pending statements and hashes can refer to earlier drafts or engineering fixtures.
Read them with the later parent dispositions and editorial-delta record in
`root_evidence/`. Earlier fixture receipts do not claim final-paper clearance.
Some preserved audit scripts require private fixtures or source bodies and are
historical evidence, rather than a self-contained automated test suite. The
rank checker's relative source-manifest layout is retained.

Optional source-only checking authenticates all three complete native corpora
before extracting the exact catalog/problem pair and never reads or executes
archival candidate code:

```text
python3 -I -S -B portable.py source-only --catalog CATALOG --problems PROBLEMS --reports REPORTS --primary-dir PRIMARY_DIRECTORY
```

The optional primary directory uses exactly seven pinned route-input bodies.
Those seven are not every paper cited by the final note or priority audit; the
Li–Li and other inspected bodies have separate pins in the priority ledgers.
No complete corpora, primary-source PDFs, wheel bodies, installed runtimes,
rendered pages, private fixtures or scratch files are in the verification ZIP.

Miao–Wang's threefold factor, Wang–Zhu's toric soliton, Han–Li's global criterion
and Blum–Liu–Xu–Zhuang's degeneration results are credited. Earlier nontrivial
first centers of Li–Li are also credited; the rational rank of their second
example was not certified in the sources inspected. The bounded priority search
is not a novelty, historical-firstness, exhaustive-priority or continued-openness
certificate. No claim that every two-component optimizer has irrational direction
is made.

AI tools were used extensively in developing, checking and preparing the work,
and the adversarial reviews were performed by AI agents. This is an unrefereed
preprint. Independent human peer review and formal verification have not been
completed. Passing software checks is auxiliary evidence and does not supply
mathematical acceptance or publication approval. No outside individual was
contacted on behalf of this independent research effort.

## Published record

Published preprint: [10.5281/zenodo.23411227](https://doi.org/10.5281/zenodo.23411227). Two successive NEW independent whole-package reviews cleared the same179-file package before merge. PUBLICATION_RECEIPT.json records the exact accepted revision, final review links, production deposit and unique tracker row. This later outer README/log/manifest annotation adds the receipt; the five-page paper, metadata and150-member verification ZIP remain unchanged. The README inside the ZIP is the frozen pre-publication version.
