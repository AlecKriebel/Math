# Research log

Date: 2026-10-04 UTC. Exact target: ID 30002526, irreducible complex projective surface realization of every finitely presented group with NC singularities only.

Completion estimates below refer to resolution of this full target, not to completion of the investigation or likelihood that a particular calculation is correct. They are rough planning judgments.

## Source checkpoint, 13:38–13:41

Started from the requested catalogue URL, then read the pinned exact record and the primary OWR report. Confirmed the live row and bounded duplicate checks. Read the published Kapovich theorem and its local quotient calculation, and the reducible SNC result. Found two stronger 2016 official seminar announcements; no accompanying proof was found. Checked the author's dated 2019 statement, which still includes Whitney umbrellas. Reported this caveat before treating the target as unresolved. Full-target completion estimate: 5%.

## Approach 1: change the orbifold action / remove torsion

Checkpoint: 13:42. Derived the invariant ring for branch interchange with sign reversal: b^2=cs^2. Compared the smooth invariant ring when the transverse sign is not reversed, and identified the changed fixed-locus requirement. Tested the torsion-removal shortcut against the cone on RP^2 and the need to kill point stabilizers. A torsion-free replacement alone cannot realize all G. No group-preserving replacement action was constructed. Full-target completion estimate: 5%. Route blocked on missing global action and quotient-group control.

## Approach 2: birational local repair

Checkpoint: 13:42. Read Bierstone–Milman Example 1.7. Computed the origin blowup's self-reproducing pinch chart and the smooth charts from blowing up the entire double line. Derived the normalization and conductor map. The latter changes NC points, outside the restricted repair theorem, and its effect on global pi_1 is not automatic. Full-target completion estimate: 5%. Route blocked on preserving or reconstructing global gluing relations.

## Approach 3: split the conductor using a cover

Checkpoint: 13:43. Factored the pullback under w=t^2. The resulting smooth sheets have coincident tangent planes at the origin, so the cover does not directly give NC. The conductor map ramifies there. No global irreducible projective descent with the same pi_1 was established. Full-target completion estimate: 5%. Route blocked, with a concrete tangent-rank failure.

## Approach 4: smoothing/deformation

Checkpoint: 13:43. Verified that nonzero level sets of v^2-wu^2 are smooth, but isolated the separate deformation/topology gap. Built the nodal-cubic family control: its product with P^1 changes fundamental group from Z to Z^2 under smoothing. Used even b_1 for smooth projective varieties only as an obstruction to the stronger complete-smoothing shortcut. It is not an obstruction to the original NC target. Full-target completion estimate: 5%. Route blocked on a selective deformation with verified pi_1 invariance.

## Approach 5: connected-normalization NC self-gluing

Checkpoint: 13:44. Worked out an explicit nodal cubic normalization and its product with P^1, realizing G=Z without pinches. Its normalization is simply connected, so indiscriminate normalization loses the desired loop. Identified the exact unsupplied general step: algebraic conductor identifications and triple-point relators on a connected normalization, local NC checks, ample-line-bundle descent, and van Kampen computation. Full-target completion estimate: 5%. No arbitrary-presentation construction was obtained.

## Control checkpoint, 13:45

Completed five substantive, materially distinct approach blocks. Standard-library exact symbolic controls pass 506 assertions, including 481 bounded invariant-monomial controls. The all-degree invariant-generation proof is in the prose, not inferred from the finite bound. Negative controls reject the missing-factor identity and transverse-branch shortcut. All source hypotheses and limitations are stated separately from computations.

No additional proof-search block is being claimed beyond these five. No queue mutation, external outreach, merge, release or DOI creation was performed. This is an **unsolved** result with a frozen author packet awaiting a fresh independent audit; no full proof or verified prior resolution is asserted.
