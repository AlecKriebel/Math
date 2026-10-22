# Publication scope and provenance correction

Checked 4 October 2026 UTC.

## Queue provenance correction

The frozen public/SOURCE_GATE.md identifies
c87c275c638939b8008fd58db80657491d14971e as a fetched queue blob. That
identification confuses an embedded historical text header with Git metadata.
The queue file itself starts with that historical header. It is preserved
unchanged, along with every other pre-existing byte outside the two authorized
cells.

The publication base is main commit
1135765a7fe02d6c2bbeca7bc1a3a4a5259650a9. Its actual QUEUE.md Git blob, obtained
from the Git tree and independently verified by hashing the full file bytes,
is 59dba610d333684751e889818d21f66aba29cec9 (385,282 bytes).
The actual Git metadata, rather than the embedded header, governs publication.
This is a provenance correction only; the mathematical statements, review,
and frozen file hashes are unchanged.

## Exact change boundary

The only existing repository file changed is
unsolved_math_prioritization/QUEUE.md. Only row 557's Status and Turns cells
change from queued, 0/5 to unsolved, 5/5. All other cells, rows, links, headings,
whitespace, and bytes are preserved. No queue script or generated state file
is changed.

New files are limited to this problem's eight frozen public files, four
independent audit files, this scope statement, the entry README, and the
publication manifest. No source copies, source extracts, catalogue record,
corpus, private context, or conversation transcript are included.

This is an audited unresolved investigation. Publication does not turn the
restricted bi-Lipschitz and finite-zero boundary-growth results into a proof
for arbitrary homeomorphisms and singular fields. No qualifying counterexample
was constructed.
