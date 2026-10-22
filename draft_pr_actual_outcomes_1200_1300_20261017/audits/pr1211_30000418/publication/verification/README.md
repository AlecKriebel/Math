# A five-list obstruction on an eleven-vertex tree — verification, version1.0

Run `python3 -B replay.py` after extracting the archive. Python3 and its
standard library suffice; no network or solver dependency is needed.
The runner authenticates every manifest member, executes a fresh global
enumeration, and compares the complete result with `expected_results.json`.
It writes only `results.json`, which is intentionally excluded from the
manifest. `MANIFEST.json` excludes itself; the external build receipt binds it.
The primary `verify.py` also works with `python3 -B -O verify.py` or `-OO`;
its mathematical acceptance conditions do not rely on assertions.

`specimen.json` binds the eleven named vertices, ten edges, five-lists and
the paper's ordinary witness. The fixed-instance driver explicitly checks
these bindings and enumerates every solution, checking all-pair distance
constraints. It returns common-palette counts0,0,0,0,8,6336 for sizes1–6,
and zero for the bad five-lists. A thousand seeded six-list samples and
three rejected witness corruptions are implementation checks only.
The proofs in `manuscript/main.tex` and `corrected_edition/PROOF.md` establish
the universal six-list bound and all independent pendant-path extensions.
No finite sample proves those quantifiers.

`independent_family/` preserves an immutable construction-input reconstruction,
using constraint propagation and a tree-state method. Run its optional
`python3 -B independent_family/replay.py` in **ordinary Python mode**.
That historical frozen replay uses assertions; optimized `-O`/`-OO` execution
is not supported or certified for this optional family. Its freeze is
preserved, not recreated by replay. It received the construction/definitions
but no expected answer or candidate proof, and froze before parent comparison.
This was construction-input verification, not independent discovery or a
wholly blind research process.

`corrected_edition/` contains all eight corrected PR proof/audit/metadata
files. The main result is unchanged. A supplementary recurrence now explicitly
checks local list membership and parent-edge compatibility before its child
distinct-representative test. Invalid local pairs are infeasible even at leaves.
Original submitted hashes and the distinction between historical and fresh
executions remain in the provenance/source records. Neither the eight-file
manifest nor an old audit receipt substitutes for the executable checks here.

`priority/` contains the two independently frozen bounded source audits,
their cross-challenge and exact comparison code/data for the older cyclic
Fiala–Škrekovski2001 five-list obstruction. Each comparison script may be run
from its own directory. Downloaded third-party papers, text extractions,
images and source-author code are **not included**. Local input filenames in
their source receipts are research locators, not missing archive promises.
The known tree bound and earlier general-graph separation are credited.
Inaccessible or unlocated sources leave historical priority and present
openness unresolved. No firstness, minimality or new-method claim is made.

AI tools were used extensively for research, proofs, source investigation,
code, internal reviews and writing. This package and note are unrefereed;
no external human peer review or formal proof-assistant certification is
claimed. Authored package content is released under CC BY4.0 by Alec Kriebel,
ORCID0009-0001-9320-500X. Source attribution and historical metadata are
retained. The preprint PDF and archive are separate deposit files.
