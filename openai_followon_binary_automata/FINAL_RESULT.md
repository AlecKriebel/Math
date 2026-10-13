# Verified final result and publication

Alec Kriebel; ORCID https://orcid.org/0009-0001-9320-500X.
Checkpoint: 2026-10-06 21:36 PDT. Mathematical resolution: 100% best guess.
Publication package: 100% best guess. Percentages are planning summaries,
not evidence; proofs, reviews, hashes and service readbacks are the evidence.

## Mathematical result

For h>=2, encode every binary relation on h points by its row-major h^2
adjacency bits. K_h consists of complete-block encodings whose relation
product is nonempty; the empty identity product accepts. All malformed
lengths reject. The explicit marked right-only NFA has exactly
N_h=(3h^3-h)/2+2 states; an ordinary epsilon-free NFA has N_h-1 states.
Every ordinary one-way NFA for this exact language needs at least h^3 states.
The step-for-step pullback of an s-state binary target has exactly sh^2 states.

Every marked binary 2DFA recognizing K_h satisfies
2^floor((h-2)/31)<=4(sh^2+2)^2. Every marked binary 2NFA recognizing
the full complement in all binary words satisfies
2^floor((h-2)/127)<=2(sh^2+1), with zero-step finite acceptance.
The manuscript gives the positive-run variant. Both imply
2^Omega(N_h^(1/3)); no 2^Omega(n), L!=NL or stronger uniform separation
is claimed. Markers, empty words, incomplete blocks, partial rows, stays,
left moves and infinite nonaccepting runs are handled explicitly.

The exponential obstructions are inherited from the two OpenAI family-129
manuscripts at commit adc7f1241b42e322a6451854ab7e4b4c146bf78a.
Binary adjacency coding is older machinery attributed to Kapoutsis, and
the original liveness family is credited to Sakoda and Sipser. Our scope
is an explicit binary consequence, complete exact compilers, full-universe
complement accounting and a strict-alignment cubic one-way bound. There
is no claim of firstness or an independent solution of the base conjecture.
The bounded priority audit and original citations are retained.

## Audited package and limitations

The standalone six-page main.tex/paper.pdf, publication README and exact
verification.zip comprise the reviewed four-file deposit. The authoritative
identities are reviews/candidate04_hashes.json. Two distinct complete-package
reviewers inspected the original proofs, full candidate, dependency/priority
evidence, executable artifacts, PDF and metadata. The second began from
scratch. Supplement clean-build repairs and two precise Theorem 1.1 citation
corrections were independently rechecked; no substantive issue remains.
Their full reviews, responses and exact-version evidence are under reviews/.
Four standard-library checkers passed independent exact-archive reproduction.
Finite checks support but do not replace uniform proofs.

Extensive AI assistance is disclosed. This preprint has not undergone
conventional human peer review or refereeing. Actual Lean source statements
and proof bodies were inspected, but a kernel rebuild, axiom printing and
Comparator execution were not reproduced after local disk exhaustion.
Neither reproduced formal verification nor binary formalization is claimed.
The independently checked handwritten arguments are the dependency basis.

## Verified production publication

Title: Binary consequences of relation-liveness automata lower bounds.
Publication date: 2026-10-06. License: CC BY 4.0 for the new note and
original supplements; retained upstream local source copies have their own
Apache-2.0 license and are not included in the deposit ZIP.

Zenodo record: https://zenodo.org/records/23202966
DOI: 10.5281/zenodo.23202966
DOI URL: https://doi.org/10.5281/zenodo.23202966
The repository tool completed check, stage, inspect, publish with confirmed
actual draft ID 23202966, then inspect --check-doi. Submitted/public state,
metadata and exact file set/bytes/MD5 were verified. All four unauthenticated
public downloads match the reviewed SHA-256 hashes. The DOI resolver returned
HTTP 200 to this record, independently of publication confirmation.
Nonsecret receipts are in receipts/zenodo-*. No release or duplicate pathway
was used.

## Verified tracker

Spreadsheet: 1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20.
Numeric sheet ID: 1254632077, resolved from live metadata to Math Puzzles.
Headers: Original Problem; Solution Chat URL; DOI; Notes.
The exact DOI/deposit ID/title search returned no existing entry.
One RAW row was appended at 'Math Puzzles'!A35:D35 and independently read back
with exact matching values. The optional unknown chat URL is blank.
Metadata, duplicate search, intended row, append and readback receipts are
in receipts/tracker-*. Unrelated sheet rows were not modified or republished.

## Repository custody

All work is confined to this dedicated project. Owned checkpoints were
pushed directly to current remote main through an isolated index; shared
checkout, branch and index were preserved. Final sources, metadata, reviews
and nonsecret publication/tracker receipts are included in the final owned
checkpoint. The frozen deposited files remain unchanged. Live theorem and
approach status files were updated after publication; the immutable ZIP
retains their reviewed prepublication snapshots.
