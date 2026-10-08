# Minimal surfaces: accepted scoped partials

Problem **10300008 / AMR-102-0008**, rank **1003**. Disposition: **unsolved, 5/5 approaches**.

The independent audit accepts the original mathematical proof unchanged. It establishes restricted characteristic-form compatibility and conformal exactness criteria, a compact-leaf homology/isotopy necessary obstruction, a fixed-representative tangency obstruction, special simultaneous torus families, and a failure of naive metric averaging. The tangency example is removable by an independent isotopy. There is no general construction or counterexample after independent isotopies. These results do not establish novelty or the complete current literature status.

Read [the unchanged proof](author_original/packet/PROOF.md), [the independent mathematical audit](audit/AUDIT.md), and [the exact acceptance](audit/ACCEPTANCE.json).

## Preservation and the required correction

- `author_original/` and its ZIP preserve every original byte, including historical pending-review labels and the historical annotated replay receipt.
- `audit/` and its ZIP preserve the independent review and exact acceptance. This acceptance supersedes the historical pending-review labels.
- `author_corrected/` differs only in `test_bootstrap.py`. [The actual three-line patch](audit/HARNESS_CORRECTION.patch) makes newly created disposable mutation fixtures writable. It never changes the frozen source permissions or any mathematical payload. The publication verifier applies the actual patch and compares every member.
- The original harness fails when read-only modes are preserved, because it tries to mutate its read-only disposable copies. The independent verifier reproduces this defect before testing the correction. The original replay receipt is preserved as historical evidence rather than silently repaired.
- The nine-file author manifest does not cover its outer bootstrap or harness. The publication manifest and independent archive pins bind those files separately, as well as the corrected harness, audit executables, and acceptance.

## Replay

Use Python 3.12 or later on a non-root Unix account with enforced ordinary file permissions. No network, third-party packages, source documents, or datasets are needed.

Run `python3 -I -S -B BOOTSTRAP.py`, then repeat with `-O` and `-OO` before the script name. Run `python3 -I -S -B TEST_MUTATIONS.py` in the same three modes for publication-boundary hostile/malformed controls. The bootstrap accepts an alternate packet directory for relocated replay and an optional `--integrity-only` flag after that directory.

The corrected author harness replays six positive layout/mode cases and rejects 78 integrity-mutation runs. The author finite checks report 916 algebra cases and 50 malformed/claim controls. The independent harness supplies 917 algebra cases, 12 algebraic boundary controls, 30 hostile/malformed author-bootstrap runs, and its own read-only corrected replays. Repetitions across modes are not distinct mathematical cases. Written arguments, rather than bounded computations, establish the geometry.

The complete external publication manifest is `PUBLICATION_MANIFEST.json`. Before execution, compare the manifest, `BOOTSTRAP.py`, and `VERIFY_PUBLICATION.py` SHA-256 hashes with independently supplied publication pins. The bootstrap checks the verifier before execution; the verifier authenticates the exact recursive inventory before staging executable bytes. A mutable script cannot authenticate itself without an external trust anchor. Tests assume a trusted interpreter, standard library, operating system, and quiescent filesystem. This is local verification, not proof-assistant certification, human peer review, or a GitHub CI pass.

## Public-source boundary

Only authored proofs, mathematical audits, acceptance reports, source-free executable controls, and public verification metadata are distributed. Public source titles/URLs, hashes, byte counts, and dated inspection history are retained in the source audit and metadata files. Source PDFs, copied source text/images, dataset contents, and private coordination files are excluded. The source and corpus audits describe local rehashes and bounded historical retrieval/inspection; no new publication-stage literature survey or full-source network retrieval is claimed.

The repository change is limited to this attempt and the rank-1003 QUEUE row's Status, Turns, and Findings cells. Other queue bytes, including existing notes, chat links, and the inherited leading hash line, are preserved. Draft review only; no merge or release.
