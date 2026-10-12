Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The structural proof retains its original through-nine premise; the separately accepted through-ten application appears in BOUND_TEN_DEDUCTION.md. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Reproducing the independent structural-symmetry audit

Keep this directory beside the unchanged candidate directory `the original source packet` and its external pin. Python 3 standard library only is required.

## Fresh mathematical implementation tests

The original instructions specified running each command and retaining its JSON output outside the original frozen packet:

    original independent implementation replay under normal Python
    original independent implementation replay under Python -O
    original independent implementation replay under Python -OO

These run the complete independent checks in each mode. They import only the candidate implementation; the candidate oracle is not imported. Source mutants are temporary files and explicit failed checks are required.

## Fresh author replays

For each of normal Python, `-O`, and `-OO`, run:

    original implementation replay under normal Python

Compare with the matching frozen `the original operational record`, `the original operational record`, or `the original operational record`. Do not pass `--write-examples` to a frozen candidate. The recorded audit outputs exactly match the author's three original receipts.

## Author and audit integrity

    externally pinned integrity verification under normal Python
    externally pinned integrity verification under normal Python

Repeat with `-O` and `-OO`. Both commands verify pinned byte identity and scope gates; neither substitutes for proof review or fresh finite computations. `--self-test` works on temporary copies outside the frozen packet. Audit post-freeze receipts and terminal records are intentionally outside the frozen directory.

Read `STRUCTURAL_AUDIT.md` for the decision and exact limits, `STRUCTURAL_PROOF_REVIEW.md` for the full independent argument, and `the original operational record` for machine-readable scope. The all-size theorem is structural; no new general finite conjecture bound or unrestricted periodic exclusion is asserted.
