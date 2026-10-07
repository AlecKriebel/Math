# Research log: fixed-binary-alphabet automata lower bounds

## 2026-10-06 21:13 PDT / 2026-10-07 04:13 UTC — intake checkpoint

Mathematical resolution: 10% best guess. Publication package: 0% best guess.
These estimates measure remaining work; they do not certify conclusions.

Persistent objective: resolve both binary lower bounds rigorously, audit a complete preprint, publish on production Zenodo and record the verified DOI in the specified tracker. Publication is authorized only after mathematical, priority and package conditions pass.

Read workspace AGENTS.md. Dedicated folder did not previously exist. Shared checkout is main at 6c0de5e6e901dfd6f2569fdcb11e0c5ac76eca06 with numerous unrelated changes; shared index initially empty. Unrelated projects and PRs are outside scope. Upstream clone is read-only, pinned at adc7f1241b42e322a6451854ab7e4b4c146bf78a; remote main/HEAD still match that pin at intake. Any builds run in project-local copies. No external individual has been contacted.

The source README reports mixed verification. Read both manuscript-specific citation blocks, scope document 129, actual theorem declarations and machine models. Strongest presently checked statement: both inputs concern nonempty relation products over all relations on h points; empty product is identity. Their lower bounds have not yet been independently certified.

Independent agents: original determinization argument; original complementation argument; binary compiler/construction; primary-literature priority audit; pinned formal build and axiom audit. Preserve early independence. Established binary adjacency encoding is already printed in Kapoutsis (2013); attribution and exact counts need checking.

Shared main is behind current remote main. Use isolated index and commit-tree based on freshly fetched remote main for owned files only; never alter shared index/checkout, force-push, reset, or create a branch. No GitHub releases.

## 2026-10-06 21:20 PDT / 2026-10-07 04:20 UTC — proof/package checkpoint

Mathematical resolution: 92% best guess. Publication package: 45% best guess.
Strongest verified result: full uniform source compiler in (3h³−h)/2+2
marked states / one fewer ordinary states, exact sh² target pullback,
all-word complement equivalence, and h³ source fooling set. Independent
reduction adversary found no defect and ran 4,472,832 equivalence checks;
root reran both original and independent checkers, plus upstream finite
algebra probes. Separate manuscript/semantic audits of each original
exponential lower bound found no substantive gap. All exponential
obstructions remain credited to those external theorems.

Formal reproduction limitation: 41 byte-identical actual proof modules,
source scans and matching Comparator signatures were checked, but disk
exhaustion prevented dependency acquisition and kernel build / axiom
printing / Comparator execution. Only owned failed caches were removed.
There is no claim of reproduced formal verification. This limitation is
stated globally; dependency validation is by the independent handwritten
proof audits, not the failed build.

Priority audit confirms adjacency coding appears in Kapoutsis 2011/2013;
public R816 supplies other coding machinery with quadratic input only.
Our note is an explicitly attributed fixed-binary consequence, plus strict
alignment/source accounting, with no first claim. No duplicate unrestricted
exponential binary theorem was found in inspected sources. Public release
of the upstream input was verified October 6, distinct from manuscript dates.

Six-page standalone manuscript compiled in the built-in editor; an actual
exported PDF also compiled with Tectonic and all six pages were rendered and
visually inspected. Full package freeze, clean reproduction, and two fresh
complete-package reviewers remain pending. Initial safe checkpoint was
pushed as 281e5a6a20ee1b672cd940125f6733ab8f3f10a8 without changing shared
checkout/index. One concurrent remote-main update rejected an earlier push;
retry used newly read remote parent, without force-push or reset.

## 2026-10-06 21:22 PDT / 2026-10-07 04:22 UTC — complete candidate checkpoint

Mathematical resolution: 95% best guess. Publication package: 65% best guess.
The frozen candidate has a standalone six-page PDF/source, publication README,
metadata manifest and deterministic verification ZIP. Clean temporary-directory
reproduction passed all four original/independent scripts and the PDF build.
The exact files and SHA-256 values are in reviews/candidate01_hashes.json;
local Zenodo check passed for production. No remote deposit has been created.
First fresh complete-package adversary is reviewing the exact candidate,
original target, primary input proofs, all dependency/priority records and code.
Second fresh complete-package review is required after the first pass/repairs.
The deposit will use the repository tool's four-file upload kit, not releases.

## 2026-10-06 21:25 PDT / 2026-10-07 04:25 UTC — boundary repairs

Mathematical resolution: 95% best guess. Publication package: 72% best guess.
First full-package reviewer independently inspected both original central
proofs, all PDF pages, current priority comparators, source hashes and scripts;
no mathematical/semantic gap found so far. Supplement repair: include main.tex
and create tmp on clean reproduction; exact ZIP extraction and all four checks
plus PDF rebuild passed. Reviewer requested reconciliation of an early audit's
conditional wish for a formal build with the final explicit handwritten
validation basis. Original auditor is reconsidering that sentence candidly.

The gws shared instruction prerequisite was missing at its installed skill
path. Attempting `gws generate-skills --help` invoked generation instead of
help and created a new root skills directory and docs/skills.md. Birth times
confirmed both were newly generated at 21:24:19 PDT; no tracked files existed
at those paths. Moved the new directory and index into this project's sources
folder, preserving the pre-existing shared docs directory and its contents.
Read the generated shared reference and current API schemas. No spreadsheet
API read/write has occurred. The user's explicit post-publication tracker
update authorization supersedes skill-level repeated confirmation guidance.
Local production deposit state for this manifest does not exist. No draft
creation/publication has been attempted.

## 2026-10-06 21:29 PDT / 2026-10-07 04:29 UTC — first complete review passed

Mathematical resolution: 98% best guess. Publication package: 80% best guess.
First complete-package review found no unresolved substantive mathematical,
semantic, priority/attribution, disclosure, license, PDF or reproducibility
issue in exact candidate03. Report and all five hashes are preserved.
The reviewer independently read both original central handwritten proofs,
all actual PDF pages, all source hashes, and the primary prior statements;
exact ZIP extraction reran all four checks and rebuilt the standalone PDF.
The earlier audit's proposed formal-build gate was preserved and explicitly
reassessed by its original author: it was an extra verification preference,
not a missing handwritten mathematical obligation. Formal verification is
still unverified and never claimed. The fresh second reviewer has begun
from original proofs rather than previous favorable verdicts.

The final supplement is SHA-256
98387ea3646a73c09db831269111e796e1ceded5a290cf518b8e140b09726a3b.
PDF, TeX, README and publication metadata remain identical to initial full
candidate. No new proof edits are planned. Source remote main still matches
the pinned upstream commit. Production creation remains gated on the fresh
second review, without requesting approval already granted by the user.
