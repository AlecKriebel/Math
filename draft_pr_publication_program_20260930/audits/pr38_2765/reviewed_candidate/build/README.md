# PR38 current builder: separate static S1 execution revision

This sibling preserves every file in the CLOSED `current_preparation_family/`.
Its original builder SHA is
`dbb81b2573c1ed59845c2a46d11572b86862c5b4cc1eff926ba86fa84bd14bdd`;
its static closure SHA is
`0aa63f40183ab89166b37d807ce6b38e1e62a5de481fc0aa3d367e8d184d3638`.
That archive remains historical evidence. The source-first static adversary
found that the original retention allowlist rejects capture_runner's genuine
`.stdin` artifacts, so the original builder cannot freeze a successful actual
packet with the complete retained inputs. This correction makes no scientific
or mathematical verdict.

`S1_MINIMAL_REVISION.patch` contains the complete code difference. The revision
adds exactly `.stdin` to the first-party file capability list; validates every
nested stdin path, complete byte size and SHA through the same artifact guard
as stdout/stderr; and compares every retained stdin payload with a whole exact
original source input. This protocol admits only the unchanged current-measure
helper's `['git','hash-object','--stdin']` requests. Returned Git blobs must agree
with the exact snapshot pins, and all original16 inputs must be covered.
No stdin artifact is deleted, hidden, shortened or excluded.

The exact authorized source parent is now `current_execution_revision` under
`pr38_2765`. The repository/audit anchor calculation remains the same. Revision
code, contract, README, patch, log and self-excluded revision manifest are bound
under their actual audit-relative prefix and copied into current `build/`.
Root must pass the actual chosen wrapper and collector path/hash explicitly.
The sibling `root_replay_execution_revision/` is coordinated separately for its
prelaunch/timeout/OSError/setup failure-retention repair; this builder performs
no collector replay or imported research-code execution.

Everything else in the builder is byte identical to the CLOSED original source:
scope certificate `4e042ef2328c73cf871627ccf15c3ffe98366019c67c34951a7d9a221e1a47fa`,
original16/17 Git/archive pins, original math/code/source/whole receipts/turns,
full raw/SQL/source provenance, closed169, literal versus closed/finite-area
scope, periodic-orbit support, extended pairing and pi^2 normalization,
author30/reviewer72 whole JSON, actual3.9/SymPy1.14 and failed default3.14,
original2/5,new0/audit0, exact recursive retention, named twelve-column queue
proposal and absent-only atomic candidate publication. No old PASS transfers.

Root and the original static adversary must read the entire revised source and
patch before any execution. This family has not imported, compiled or executed
the builder and supplies no runtime test, actual replay or new verdict. The
NEW whole-current source-first gate remains pending. No shared, canonical,
inventory, Git, remote, paper/DOI/tracker/release or outside-person write occurs.

Static revision completion:100%. Research full-target heuristic partial-
progress estimate: unchanged15%; no substantive search or discovery.
