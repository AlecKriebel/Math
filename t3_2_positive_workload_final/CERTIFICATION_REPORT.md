# T3-2 certification report

Date: 2026-08-09

## Decision

The independent audit is correct on its two load-bearing objections. The
inherited T3-2 theorem is not certified and the supplied release is not ready
for arXiv.

The proposed physical-time repair is the right change of target, but it is not
a proof as written. In particular, pointwise shell-dependent negative drift
does not imply finite mean clearing, and a lexicographic descent with finite
primary duration does not control a heavy-tailed lower-component reset.

No physical T3-2 counterexample was found.

## What remains certified

| Component | Status |
| --- | --- |
| Three independent finite atlas replays | Pass |
| Deficiency-zero/product-Poisson branch | Pass |
| Scalar aggregate-debt inequality | Pass at its stated uniform-margin scope |
| Actual-current-target identity and local return paths | Pass locally |
| Four generic proof-interface regressions | Pass |
| Exact `{C,A+C,B+C}` shielded/available seam | Pass analytically after repair |
| Seven compatible shielded supports for that exact seam | Pass |
| Tightness to one fixed finite inactive phase | Withdrawn |
| Raw embedded-occupation closure | Withdrawn |
| Universal one-active/countable-phase closure | Open |
| Universal shielded/available interface | Open |
| Signed exceptional-service seam | Open |
| Global T3-2 theorem | Not certified |

## New theorem-level progress

The former smallest obstruction

\[
 \{2B,A+B\}\quad\&\quad\{C,A+C,B+C\}
\]

has been repaired without conditioning on activation and without counting
fast embedded jumps. A global factorial potential balances the fast neutral
linkage to at most linear positive drift, while the catalyst-scaled
monomolecular linkage supplies coercive negative physical-time drift. An
independent adversarial proof review found no defect under the exact stated
hypotheses.

The finite support reduction shows that the argument covers all seven
positive-invariant shielded supports compatible with the fixed available
support. Six use Foster drift; the autonomous `{0,2C}` case uses an explicit
parity law times a product-Poisson law.

This result is recorded in
`research_notes/certified_exact_shielded_seam.md` and replayed by
`src/exact_shielded_seam.py`.

## First exact remaining gate

The first arbitrary pairing not reduced to product form is

\[
 L_0=\{B,2A,B+C\},\qquad L_1=\{0,A,C\}.
\]

The fast linkage preserves \(q=A+2B\) and has an explicit conditional
product law. Under that law, \(C\) is Poisson and
\(\mathbb E[A]=\Theta(\sqrt q)\); therefore the available linkage has
averaged \(q\)-drift \(-\Theta(\sqrt q)\). This strongly suggests recurrence
and rules out a critical averaged birth-death mechanism.

Two simpler bridges nevertheless fail:

1. a natural complex-balanced factorial potential can have positive drift
   of order \(n^2\) at \((A,B,C)=(n,n^2,0)\);
2. for \(H=A+2B+C\), after a positive actual target the next workload change
   can be positive with probability tending to one.

The exact missing result is a pointwise, shell-uniform killed busy-period or
Poisson-corrector estimate joining a large-\(C\) proper-workload region to the
\(A=\Theta(\sqrt q)\) averaged descent region. Stationary product form and an
\(L^2\) spectral gap do not alone supply the required weighted endpoint
control from arbitrary initial phases.

Details are in `research_notes/remaining_fast_phase_corrector.md`.

## Release audit

The inherited archive's manifest and finite suite replay, but the public
certification surfaces overclaim the analytic scope. The clean-extraction
report has stale generated-report hashes, the accessible outer archive hash
does not match the previously reported hash, and the verifier is mutating and
non-hermetic. Python and TeX prerequisites are undocumented, and release
metadata such as license, citation file, precise classwise theorem scope, and
repository/tag provenance are missing.

These are repairable release-engineering defects, but repairing them now
would not make the theorem true. A final arXiv source/PDF archive should be
built only after the remaining mathematical gates close.

## Reproducible package status

Run the current non-mutating finite replay with:

```bash
python3 -I -B verify_read_only.py
```

The command covers the generic regressions and exact-seam finite algebra. It
does not claim computational certification of the analytic seam proof or of
T3-2.

## Hard stop

No replacement theorem manuscript or PDF was created. Doing so would violate
the supplied final-repair program's hard stop and would present an open
killed-resolvent lemma as a proved global theorem. The correct public status
is:

> Candidate T3-2 theorem under repair. The finite atlas, local debt identity,
> and one exact physical-time shielded/available seam are certified. A
> residual fast-phase busy-period corrector and the signed-service seam remain
> open.
