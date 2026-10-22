# Qualified F-pure-threshold theorem and singular boundary example

Problem 20000276 / AIM-ALGEBRAIC_GEOMETRY-0276, rank 757.
Publication acceptance note, 2026-10-05 UTC.

**Original target: unsolved; three of five substantive approaches used.**
The independent mathematical audit passes the explicit regular-local theorem
and singular F-pure counterexample. It does not certify resolution of the
original AIM problem, whose primary ring conventions remain unverified.
No historical novelty, first-resolution, or human-peer-review claim is made.

## Accepted theorem

Let `(R,m)` be an F-finite Noetherian regular local ring of characteristic
`p>0`. Let every `I_n`, for `n>=1`, be nonzero and proper, and suppose
`I_a I_b` is contained in `I_(a+b)` for all positive `a,b`. Then

`lim_n n fpt_R(I_n) = sup_n n fpt_R(I_n)`

in the extended positive reals, allowing positive infinity. Descendingness
and finite generation of the Rees algebra are unnecessary. The proof uses
finite free Frobenius, the fixed-factor limit `k fpt(I^k J) -> fpt(I)`, and
finitely many residue classes. See [the complete proof](author/PROOFS.md)
and [the independent audit](audit/AUDIT_REPORT.md).

## Accepted singular boundary

In the F-finite F-pure local ring
`R=(F_p[x,y,z]/(xy))_(x,y,z)`, put `h=x+y`, `I_(2a)=(z^a)` for `a>=1`,
and `I_(2a+1)=(h z^(a+1))` for `a>=0`. This multiplicative graded family
has a two-generated Rees algebra and nonzero proper terms containing
nonzerodivisors. Its normalized F-pure thresholds are exactly 2 on positive
even indices and 0 on odd indices. It is not descending.

This refutes unrestricted F-pure-ring convergence. It does not refute the
regular-local theorem or resolve a target with unstated strong F-regularity.
Global thresholds, non-F-finite rings, singular strongly F-regular rings,
and variants permitting zero terms have not been settled by this packet.

## Citation clarification and source gate

The Koley–Kumar named filtration invariant applies to descending filtrations
with finite limit. At infinity, the accepted crossing equality identifies
their common extended upper and lower limits. For arbitrary non-descending
graded families, it is an extension of the crossing construction. This note
clarifies attribution in section 7 of the frozen author proof without
modifying that audited historical snapshot.

The original [AIM problem page](http://aimpl.org/testandmultiplierideals/1/)
was unavailable during author and audit inspections (HTTP 502/timeouts).
Imported source and prior-report byte identities were checked, but those
records do not recover the primary ring conventions. The 2026 Koley–Kumar
publisher listing was verified; its final published full text was not
audited. Bounded literature checks are not evidence of novelty.

## Packet and reproducibility

- `author/`: nine unchanged frozen author files
- `audit/`: thirteen unchanged independent-audit files
- `FREEZE_VERIFICATION.json`: archive sizes, hashes, and byte-match results
- `PUBLICATION_STATUS.json`: accepted claims and remaining scope gate
- `PUBLICATION_MANIFEST.json`: complete file inventory and SHA-256 values
- `verify_publication.py`: portable integrity, scope, and finite-control replay

Run `python3 verify_publication.py` from any working directory, using the
script's path. The wrapper checks exact file membership and hashes, pins
both frozen manifests, and replays 282,118 author and 52,161 independent
exact assertions. Finite tests supplement the general proof and audit.

External public-source bytes are deliberately excluded. To recheck their
recorded bindings, supply all four options together:
`--problems PATH --research PATH --catalog PATH --pdf-directory DIRECTORY`.
The PDF directory requires the filenames documented in
`audit/verify_source_metadata.py`. An ordinary portable run reports external
source verification as not run; it does not imply a fresh source retrieval.

The frozen author README's pending-review language and both packets'
no-remote-write statements describe their historical creation stages.
The later independent audit and this acceptance note govern this publication.
Both freezes remain unchanged. Publication checkpoint: 100% for packaging
and the explicitly scoped proof/audit; the original-target scope gate remains
open, with no numerical estimate for recovering that missing context.

This packet includes authored mathematics, code, and public verification
metadata only. It contains no source PDFs, extracted source text, raw dataset
contents, or private coordination material. The associated queue patch changes
only this row's Status, Turns, and Findings; it does not regenerate the queue.
