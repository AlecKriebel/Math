## Accepted scoped partial result; general efficient sampling unresolved

For finite connected undirected simple graphs with a prescribed retained root,
nonroot simplicial deletion has constant fibers of size equal to the deleted
vertex's degree. Uniform valid core orientations and independent exactly
uniform neighbor-label pivots give an exact sampler for rooted acyclic
orientations and, by the correspondence as presented by Benson, Chakrabarty
and Tetali, maximal parking functions. The complete substantive proof and
independent mathematical audit are retained; no blocking correction was found.

The result gives a 2^b times polynomial exact fallback in the number b of edges
of the computed residual core, exact equality of total-variation error for
valid core laws with independent uniform pivots and a certificate fixed
independently of sampling randomness, and a self-contained polynomial-time
chordal specialization. The low-level helpers assume a valid root-preserving
simplicial-deletion plan; this edition adds that optional documentation contract
without changing the algorithm.

The probability theorem requires an ideal independent-fair-bit interface.
Fair-bit rejection terminates almost surely with expected cost; sparse hashing
has its stated expected-cost interpretation; final output sorting adds
O(m log(m+1)), and arbitrary-precision costs are retained. SystemRandom is an
implementation choice, and seeded PRNG tests do not certify physical entropy.

The chordal existence result already follows from the stated 2022 theorem of
[Bezáková and Sun, Counting and Sampling Orientations on Chordal Graphs](https://doi.org/10.1007/978-3-030-96731-4_29),
via addition of a universal sink. The authenticated [12-page proceedings PDF](https://par.nsf.gov/servlets/purl/10355288)
contains the theorem but omits its referenced detailed appendix. That appendix
and the external claimed linear-time implementation were not audited. The
self-contained proof here does not depend on them. Attribution to
[Benson, Chakrabarty and Tetali](https://arxiv.org/abs/0801.1114) describes the
presentation used, not priority; their Remark 3.1 points to earlier antecedents.

The unrestricted [AIM sampling question, Problem 5](https://www.samuelfhopkins.com/docs/aim_chip-firing_problems.pdf)
remains unresolved by this work. Arbitrary large residual cores have an
exponential fallback. No general polynomial-time exact sampler, FPAUS,
rapid-mixing bound, impossibility theorem, novelty, or exhaustive current
literature status is claimed.

“Accepted” refers only to an independent internal AI audit of the stated
partial scope. These AI-assisted authored documents are unrefereed; no
external human peer review, journal acceptance, or formal proof-assistant
certification is claimed.

Recorded independent tests covered all 772 connected labelled graphs through
five vertices and all 3,807 root instances, 17,219 product outputs and execution
paths, 6,784 one-step fibers, 1,285 deletion prefixes, and additional six- and
seven-vertex graphs. Exact TV and fair-bit checks, universal-sink checks,
invalid-input controls, and the diamond order-sampling bias were tested.
Historical normal/-O/-OO audit receipts agreed byte for byte. These finite
checks corroborate implementations; written proofs establish the general
mathematical claims. Executable programs, detailed receipts, certificate
contents and raw datasets are omitted. This is a prose-only edition, not an
executable reproduction package.

Public source metadata preserves titles, URLs, PDF hashes and sizes, and
historical retrieval/inspection limits. Failed fresh NSF/DOI audit retrievals
are distinguished from review of the authenticated supplied PDF. Edition
preparation performed no new scholarly-source retrieval or inspection and no
new execution of the omitted mathematical test programs. Local byte-integrity
checks and publication-plan controls are distinct from mathematical tests.

Exactly nine authored proof/audit/acceptance and public source/verification
metadata files are proposed as additions. Source copies, extracted text and
images, executable code, datasets, private sources, private personal data and
private coordination material are excluded. QUEUE.md and unrelated paths stay
unchanged. The original candidate/audit packages remain unchanged; recorded
editorial differences retain complete substantive mathematics.

## Exact public-file identities

- `ACCEPTANCE.json`: 1,877 bytes; SHA-256 `0df4d8389574ba70e90b950cc1cfaa3489911aa7ff2f03d08d482fadc63e4d5f`.
- `ACCEPTANCE.md`: 2,928 bytes; SHA-256 `8e6de248c0b2f33635e4dc18833399e4dda711a61ff033ad1881e21e68a4ee5d`.
- `AUDIT.md`: 18,338 bytes; SHA-256 `1d0c416904ff447eaf2d57473208bf45dc72928dea0af903018498109c7ceb43`.
- `CORRECTIONS.md`: 2,939 bytes; SHA-256 `e0e68d628341a1125d22768fb538bc327459779047ce252c828faf8e66f2718e`.
- `MANIFEST.json`: 1,807 bytes; SHA-256 `1a30e5a0d609d1311d06e80c565a5293a359908edd9ee7a47010f77c975d9182`.
- `README.md`: 4,718 bytes; SHA-256 `bd76bd6ef3331d1c887bc9d93ef4b2b148ee7afd40dbb8cce0d77dbf31e1b2b5`.
- `RESULT.md`: 21,995 bytes; SHA-256 `1ad3c34ce579f39300b83b433741c876658faf690e4d97311043c76699998c96`.
- `SOURCES.json`: 2,483 bytes; SHA-256 `45485b5e283c844ee04e9d326c363438e3a67f594bf2685c29d8aac8d8f8f3ef`.
- `VERIFICATION.json`: 2,676 bytes; SHA-256 `df628d039165474141287ccf34d22d372801aa2d9b8032a91f7d83e9e0caa372`.

MANIFEST.json lists all nine members and hashes the other eight; this body independently pins its digest.

