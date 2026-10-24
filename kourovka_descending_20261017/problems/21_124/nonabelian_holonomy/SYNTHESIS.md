# Nonabelian holonomy family: outcome and exact remaining scope

This family was tasked with resolving the all-finite-holonomy gap for the four-edge Pell CAT(0) F5-by-Z candidate, either by a negative theorem or by an explicit finite positive witness. **The proposed negative direction is DEFEATED by root's exact positive multiset.** The full Kourovka21.124 problem remains unresolved, and no complete-solution publication is justified by this family.

## Strongest findings

1. `DIHEDRAL_OBSTRUCTION.md` proves a genuine all-orders partial obstruction: every finite orthogonal action decomposing into invariant real summands of dimensions at most two kills the translation powers of a,b. This includes every finite dihedral group, in arbitrary dimension. The fresh independent `../dihedral_review/RECEIPT.json` passes the frozen proof and separately reproduces determinant, partition-lattice, torsion, and endpoint checks. This partial theorem remains valid despite the later positive result.
2. `FINITE_REGULAR_REDUCTION.md` proves that arbitrary original vertex rotations/cocycles introduce no additional existential gap: existence of any vertex-injective Euclidean-by-finite witness is equivalent to a horizontal rational regular-module solution, to an exact rank defect for a marked finite group, and to a finite rational multiset with the three matched projections. The full `../regular_reduction_review/RECEIPT.json` and its independent affine/regular-module secondary review both pass the exact frozen reduction. No theorem about all finite quotients is inferred from this equivalence.
3. Root's `../root_orbit/exact_multiset_certificate.json` gives517 symmetric pair types with positive integer multiplicities and total signed list size95419250146190292634685757020254542. My `independent_positive_check.py` does not import author code and checks the **full signed** projections, rather than reproducing the absolute-value-folded check. It confirms exact balances for every projected value, positive multiplicities, multiplicity gcd1, nonzero A,B, and the required Pell norm/cross-moment identities. Its receipt is `independent_positive_results.json`. The exact certificate supplies a finite positive witness through the reduction. Root has also built compressed permutations; the fresh `../pell_positive_review/RECEIPT.json` passes the full exact witness and its implication to VRC and virtual specialness by prior theorems. This is a positive result for the specified candidate, not a complete21.124 solution or novelty certificate.
4. `HEIGHT_SMOOTHING.md` proposes a more general construction criterion: a finite positive multiset exists exactly when there is a finite horizontal support carrying rational-function weights, strictly positive for every z>0, satisfying all projection identities. Positive denominator clearing and a common height convolution by (1+Z)^N produce nonnegative coefficients. A self-contained uniform homogenized-coefficient argument proves the smoothing step. Fresh review found and corrected the wording that a Z shift could make all horizontal Laurent powers ordinary; the corrected statement preserves horizontal support and permits Laurent powers in X,Y. The corrected hash is recorded in `HEIGHT_SMOOTHING_MANIFEST.json`. This mechanism is not a proof of Gram-compatibility sufficiency.

## Computational experiments and discarded routes

`SIGNED_SEARCH_SCOPE.md` records exact bounded B3/B4 and S6 searches. All produce no horizontal witness;14 modular B4 candidates were rejected by exact rational elimination. These bounds were never promoted to a universal negative conclusion. They are now explicit examples of how low-dimensional/low-degree absence can miss a genuine finite witness in much larger dimension.

An exploratory complex two-dimensional binary-dihedral determinant probe (`quaternionic_probe.py` and results) began before the positive certificate appeared. It computed7/9-term determinants and necessary partition-lattice counts. It was abandoned when the all-Q negative target was defeated; no binary-dihedral theorem, complete torsion classification, or negative conclusion is claimed from those preliminary artifacts.

The independent support inspection (`inspect_lp_support.py`) eliminated142 variables using exact positive two-term balance relations, reducing the root numerical517-support system to375 active variables and384 nonzero rows. This was a supporting attempt to simplify exact solving. Root's subsequent exact computation made the simplification unnecessary.

## Mechanism status and exact gaps

| Mechanism | Evidence | Current status | Exact gap |
|---|---|---|---|
|Abelian/dihedral finite holonomy obstruction|Reviewed exact torsion arguments|Verified partial|Cannot exclude higher-dimensional finite actions; an actual one now exists for Pell|
|All finite holonomy negative claim for Pell|Root exact positive multiset plus independent integer check|**DEFEATED**|No remaining negative route for this candidate|
|Finite regular module / finite multiset reformulation|Written algebraic proof; fresh audits|Supporting exact reduction|Not itself an existence theorem for arbitrary data|
|Bounded B3/B4/S6 search|Exact modular rank and rational survivor checks|Finite evidence only|Cannot bound required permutation degree or dimension|
|CAT(0) Gram compatibility⇒globally positive rational kernel|No proof; local covariance/distribution compatibility only|**BLOCKED at unsupported central assertion**|Construct one finite horizontal support and rational kernel positive on all z>0, or a new obstruction|
|Height convolution once such a kernel exists|Self-contained smoothing proof and exact test family|Proposed general tool under fresh review|Does not supply the globally positive kernel|

The old frozen dihedral/reduction notes describe the then-open higher-dimensional gap. This synthesis supersedes that historical status for the **specific Pell candidate**: the positive certificate now closes it against the negative conjecture. It does not resolve the unrestricted Kourovka problem or assert a new general virtual-specialness theorem.

Research-family checkpoint: the assigned candidate's positive-witness alternative has been attained with root's fresh full implication review passed. Best guess completion toward the **full21.124 discovery goal is now6%**. No originality audit for a complete Kourovka resolution, paper, DOI, Zenodo upload, Google Sheets entry, or human peer review is claimed. Root handles repository checkpoints; this subagent has made no git or publication changes.
