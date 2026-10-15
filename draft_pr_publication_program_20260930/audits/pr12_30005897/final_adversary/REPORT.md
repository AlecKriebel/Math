# Fresh complete adversarial acceptance audit: PR12

**Verdict: PASS for the full mathematical target and the explicitly credited
known-method-corollary disposition. No mandatory issue remains.** This is
an independent AI audit, not human peer review or formal certification.
Completion estimate: **100% of this acceptance audit**. No canonical edit,
Git mutation, or outreach was performed by this reviewer.

The final inspected candidate PROOF SHA256 is
`2d2e394d83ab96a6aee9b022d375fb1520499ed4aa360de51f7d1ed04f5b75ea`.
The initial pin was `782a92710ba0e1932bdf02e89f741df2fdf74651d09af260d1e0b1a391da8fa4`.
The change during review is solely the source-equation precision addendum,
which I also independently verified. Sections 1–6 are unchanged.

## Scope and independence

I read the complete proof and source record, reconstructed Sections 1–6,
and inspected the exact OWR standing assumptions and target before reading
sibling or historical mathematical verdicts. I then read the proposed
priority audit and frozen equivalent-method translation, independently
inspected K20's primary theorem statement, and reconstructed every bridge.
A separately delegated artifact/document audit checked the final pin and
historical labeling. Its mathematical scope was deliberately separate.

The target is exactly OWR 19/2024 p.1080, Open Problem (1), second
sentence. It concerns finite p≥1, bounded invertible scalar dissipative
composition operators, with finite positive wandering generator, without
bounded distortion. The first sentence's aggregate-mass criterion is
separate, and its earlier negative example is correctly credited. The
source's spectral convention for generalized hyperbolicity matches the
candidate. Real scalars and arbitrary measurable, possibly nonseparable
fibers are covered by the proof. [Source report](https://doi.org/10.4171/owr/2024/19).

## Mathematical attacks and outcome

The checkable analytic reconstruction is [RECONSTRUCTION.md](RECONSTRUCTION.md).
The following potential failure points were tested directly:

| Potential obstruction | Independent conclusion and tight candidate location |
| --- | --- |
| Hidden boundedness of pseudotrajectories or dual norm attainment | Neither is assumed; scaling and finite approximate norm attainment suffice. `PROOF.md:94–123`. |
| Sign or endpoint error in the necessary dual estimate | The uncancelled endpoints are a(a) and a(b+1); the interval and contradiction give the claimed d>4K²+1. `PROOF.md:125–148`. |
| p=1, arbitrary measure algebra, or nonseparability | Scalar L^q duality holds under sigma-finiteness; q=∞ indicators work, and finite W is exactly the source assumption. `PROOF.md:154–213`. |
| Inferring uniformity from separate fiber results | The uniform Banach estimate precedes localization. No such inference is made. An explicit family of unbounded flat plateaux defeats the invalid inference. `PROOF.md:197–213`. |
| Propagation or equal-drop boundary | Positivity and η<1 exclude the contradictory opposite drop. Points with both drops are consistently assigned to A0. `PROOF.md:215–261`. |
| Assuming a power split is one-step invariant | The finite intersection is indispensable and correctly used. A fresh two-residue example makes A0 fail one-step invariance, while the intersection repairs it. `PROOF.md:263–334`. |
| Noncommuting projections in the converse | The displayed Green series gives the exact recurrence without commutation. The truncation endpoints agree. `PROOF.md:336–361`. |
| Individual rather than global old tail limits | K20 Theorem 2.26 prints global closures; these yield clopen one-step bands and uniform entry into the contraction neighborhood. `EQUIVALENT_TRANSLATION.md:70–100`. |
| Periodic Stone points or free ultrafilters | Residues modulo r+1 exclude every φ^r fixed Stone point. `EQUIVALENT_TRANSLATION.md:32–40`. |
| Approximate-spectrum transfer introducing a central gap | The geometric coordinate cutoff has a vanishing normalized defect, with finite fiber measure cancelling. q=∞ is the identity case. `EQUIVALENT_TRANSLATION.md:42–68`. |
| Missing resolvent case | Gauge rotation excludes the whole unit circle; multiplier-invariant Riesz spaces yield clopen invariant bands. `EQUIVALENT_TRANSLATION.md:100`. |
| Wrong dual/primal orientation or density formula | The old central products equal the exact primal norm factors; support motion is opposite on the dual. A common large power yields the density drop. `EQUIVALENT_TRANSLATION.md:102–140`. |

Strictness of η<1 is used essentially. The finite-p scope is also genuine:
on densities ρ(n)=2^n, every finite-p composition is contracting, whereas
the corresponding L^∞ composition is an isometry and the pseudotrajectory
jδ·1 cannot be shadowed by a bounded orbit. The candidate correctly
excludes p=∞.

## Priority challenge: old stronger statements or only ingredients?

This audit did not infer `already_solved` merely because old results were
cited. The difficult global measurable uniform split is the substantive
conclusion already supplied by K20 Theorem 2.26. Its exact hypotheses are
met by the Stone representation and residue argument. K20 Theorem 5.4
already states the needed stronger abstract approximate-spectrum inclusion;
the concrete cutoff independently verifies its old disjoint-orbit
mechanism without importing the broader spectrum equality. The remaining
bridges are the prior orbit-density representation, the elementary
finite-forcing estimate, compactness, scalar product identities, and Riesz
decomposition. No substantial new indispensable splitting or uniformity
lemma was needed in the translation. [K20v2 primary text](https://arxiv.org/html/2009.09303v2).

Thus this is positive subsumption by previously stated stronger machinery,
with routine hypothesis translation, rather than a list of related older
ingredients. The support-band and density conclusions both follow. The
current explicitly qualified known-method-corollary disposition is
supported. It must retain its existing boundary: no earlier literal
printing or advertisement of the precise OWR composition statement was
established. A new application can sometimes be novel; the existence of
old ingredients alone would not exclude that. Here the old stronger
structure covers the central difficulty, so this review found no basis
for a first-resolution or new-theorem-priority claim. It does not claim
that all authors recognized this exact consequence in 2011 or 2020.

K11's original proof remains uninspected. The inspected structural premise
is its precise primary-author restatement in K20. The full text's version
header, independently freshly opened and downloaded, fixes 2020-12-19;
the HTML's internal 2026 date does not change that priority. The fresh
official HTML SHA256 equals the frozen source hash
`eaf64256c07d9854c076641980860535b7dc5d533428e645018eef19a6566830`.
The version-pinned PDF fetch returned 406; the previously pinned primary
PDF and fresh HTML were both inspected. Fulltexts remain in ignored `tmp`.

## Older equation (33): correction independently checked

The frozen family's plain isometric-shift example alone falsifies an
implicit shared-product operator identification, not the published norm
equality: the global norms coincide there. This historical limitation is
now explicitly qualified in current PROOF.md:465, PRIORITY_AUDIT.md:70,
and SOURCE_AUDIT.md's precision update, all linked to
[ROOT_EQ33_PRECISION.md](../ROOT_EQ33_PRECISION.md).

I independently verified the stronger allowed weighted-module example:
the actual stable norm at exponent two is 1/2 and the printed middle
norm is 3/4. I also independently verified the corrected operator identity
U^(1−n)T^nU^(−n−1) for the reversed operator powers. It can repair the
growth bound because the two outer U factors are subexponential. Hence
this is a repairable identity issue and does not refute the old theorem.
Both sufficient routes exclude it. The current package makes that
qualification correctly while preserving historical records.

## Reproduction and artifact integrity

[REPRODUCTION.json](REPRODUCTION.json) records isolated replay of the two
submitted scripts. Both exit successfully and semantically reproduce their
stored outputs exactly: 84 band models / 55,572 comparisons, 1,211 local
sequences, 30 telescoping checks, 31 noncommuting Green identities, 30
negative controls, and the independent 17,100 moving-cut comparisons.

[boundary_probes.py](boundary_probes.py) and
[BOUNDARY_PROBES.json](BOUNDARY_PROBES.json) contain fresh checks of
unbounded flat plateaux, p=1 triangular approximate fixed vectors,
the cutoff identity at q=1,2,4,∞, failure and repair of a power split,
strict drops up to η=99/100, 5,150 residue tests, the exact 1/2 versus
3/4 source-norm counterexample, and 30 replacement-identity checks.
These are finite probes and closed-form controls, not an infinite-dimensional
proof certificate. The analytic derivations carry the general conclusion.

The separately independent [integrity report](integrity_consistency/REPORT.md)
and [results](integrity_consistency/integrity_results.json) pass all 273
file/canonical hash checks across 20 manifest/provenance records. All 21
frozen originals match Git head
`19dfaccb52a7640eec79af28a778b4f22f93479a` byte-for-byte. Both inventories
are complete (21 original and 22 current files), and all 11 current
local/repository document links resolve in the workspace. Current claims
consistently credit earlier methods; upstream historical open status and
old review novelty language are labeled as preserved and superseded.
Remote publication of these local audit links is a later packaging step,
outside this no-Git audit.

The strongest verified result is the complete all-finite-p real/complex
target, with arbitrary measurable fibers, one-step measurable support
bands, and the density criterion. There is no mathematical scope gap
remaining. Historical literal-statement priority and the uninspected
original K11 proof are honest source boundaries, not missing steps in
the independently verified direct proof.
