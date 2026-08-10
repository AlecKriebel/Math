# T3-2 certification report

Date: 2026-08-10

## Decision

The independent audit was correct on both load-bearing objections. The
inherited T3-2 proof is not certified, and no replacement manuscript is ready
for arXiv yet.

The repair has produced five independently audited exact-scope physical-time
theorem statements, with the fourteen-partner rank-two theorem sharing its
top support with—but not overlapping—the earlier residual pair. None uses
tightness as finite support, and none
attempts to prove recurrence of the raw embedded jump chain. No physical
T3-2 counterexample is known.

## Current gate table

| Component | Status |
| --- | --- |
| Three independent finite atlas replays | Pass |
| Deficiency-zero/product-Poisson branch | Pass |
| Scalar aggregate-debt inequality | Pass at its uniform-margin scope |
| Actual-current-target identity and local return paths | Pass locally |
| Generic proof-interface regressions | Pass |
| Exact `{C,A+C,B+C}` seven-support seam | Pass |
| Exact signed-service support theorem | Pass at its displayed-support scope |
| Exact `{B,2A,B+C}` / `{0,A,C}` theorem | Pass |
| Global finite support/tier interface | Pass as an enumeration certificate |
| Affine-stoichiometric tier-feasibility theorem | Pass; 151 classwise closures |
| Fourteen-partner rank-two theorem | Pass; 14 new pairs, zero prior overlap |
| All-active-only reversible-top Foster theorem | Pass; 51 new positive pairs |
| One-active killed-carrier lemma | Pass locally; stopped kernel remains open |
| Two-active promotion/phase classification | Pass as structural enumeration |
| Three-active flat-phase classification | Pass as structural enumeration |
| Tightness to one fixed finite inactive phase | Withdrawn |
| Raw embedded-occupation closure | Withdrawn |
| Universal one-active/countable-phase closure | Open |
| Remaining twelve asymptotic interface gates | Open |
| Global T3-2 theorem | Not certified |

## Exact physical-time advances

The seven-support seam in
`research_notes/certified_exact_shielded_seam.md` uses a direct factorial
Foster estimate or, in its autonomous branch, an explicit parity law times a
product-Poisson law.

The signed theorem in `research_notes/signed_service_seam_full_proof.md`
combines a positive linear workload outside a thin tube with stopped
regeneration cycles inside it. Squaring the proper workload converts the
order-`1/B` signed-service probability into a uniform negative cycle drift.
Its exact scope is not stable under arbitrary support enlargement.

The residual theorem in `research_notes/residual_pair_full_proof.md` treats

\[
 \{B,2A,B+C\}\quad\&\quad\{0,A,C\}.
\]

It constructs a proper return workload and a core with
`A=O(sqrt(q)), C=O(1)`, where `q=A+2B`. A short physical-time window has an
exact Riccati limit and strict negative expected `q` drift. Transient
immigration--death domination, a fixed cleanup margin, and polynomial
exceptional-return moments supply the missing pointwise and endpoint-cost
estimates. Independent adversarial review found no remaining gap for any
strongly connected orientation or positive present rates.

The certified extension in
research_notes/rank_two_global_return_all14.md treats all fourteen lower
supports that occur with the same rank-two top linkage. Ten are controlled
directly by the outer quadratic workload; four require an unbounded-\(C\)
physical-time regeneration. Its explicit cleanup estimate controls every
added lower source before returning to the transient Riccati core. The
phase classifier is applied after the single residual branch above has
already been removed, so the prior-branch overlap is zero and the
overlap-free contribution is fourteen positive-invariant pairs.

## Exact remaining interface

The support audit in `research_notes/global_atlas_interface_closure.md`
starts from 4,761 positive-invariant and 408 signed unique ordered support
pairs. After applying only proved disjoint branches, the Anderson--Kim
one-step tier theorem certifies another 1,219 positive and 159 signed pairs.
Exactly 2,312 positive and 199 signed pairs remain at that stage.

The exact affine-stoichiometric filter in
`research_notes/stoichiometric_gate_feasibility.md` checks every failed
pair--descriptor incidence, not only the twelve displayed representatives.
It proves that 151 pairs have no class-feasible bad descriptor and closes them
by a class-local entropy Foster argument. Independent audits verified both
the levelwise Gordan alternative and that class-local implication. The
certified remainder was 2,169 positive and 191 signed pairs. The audited
rank-two family then contributes \(14-0=14\) new positive-invariant pairs
and zero signed pairs, leaving 2,155 positive and 191 signed pairs. The
independently audited all-active-only selector then contributes 51 disjoint
positive-invariant pairs and no signed pairs. Its 209 failed incidences all
meet the reversible two-node curvature-cofactor theorem, while every
realizable boundary descriptor passes the ordinary tier criterion. The
classwise Foster proof uses the same rate-adjusted entropy throughout and
leaves 2,104 positive and 191 signed pairs.

Those raw counts compress to twelve canonical asymptotic gate types. The
one-active local carrier theorem now identifies the exact stopped finite
fast/slow kernel still needed; it does not yet prove that kernel's uniform
old-debt clearance or marked Foster gluing. The two-active and three-active
notes give exact rank/phase decompositions without promoting their structural
labels to recurrence claims.

## Reproducible package status

Run the non-mutating finite replay with:

```bash
python3 -I -B verify_read_only.py
```

The replay checks exact algebra, regressions, support enumeration, and tier
geometry. It does not computationally certify the analytic stopping-time
proofs or T3-2.

## Release decision

The inherited archive has stale hashes, undocumented runtime assumptions,
and mutating verification behavior. Those defects will be replaced, not
patched in place. A new manuscript, PDF, manifest, archive hash, and release
metadata will be built only after every remaining analytic gate is closed.

The accurate public status is:

> Candidate T3-2 theorem under adversarial repair. The fourteen-partner
> rank-two theorem, the 51-pair all-active-only Foster theorem, the other
> exact physical-time interfaces, the complete finite tier geometry, and
> 151 classwise affine-filter closures are certified; universal stopped-phase
> and common-entropy closure remain open.
