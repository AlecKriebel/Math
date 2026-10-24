# Nonabelian holonomy research log for 21.124

## 2026-10-24T22:33:01Z — independent family opened

Goal: resolve the unrestricted finite noncommuting holonomy gap for the reviewed four-edge Pell CAT(0) F5-by-Z candidate, either by an actual finite-holonomy vertex-injective witness or by a theorem excluding every finite linear image and dimension. The pairs are (3,2),(20,14),(119,84). The complete problem remains unresolved; estimated discovery completion **4%**.

Mechanism families are kept distinct: (i) rational signed permutation and other finite group representations, (ii) arbitrary-order finite dihedral representations via exact Laurent determinants and torsion-point bounds, and (iii) a general finite-orbit/group-ring formulation. A bounded search cannot substitute for the universal assertion. Arbitrary original vertex rotations are not presumed trivial.

## 2026-10-24T22:35:00Z — signed permutation evidence

The local system compiler is unavailable because its Xcode license has not been accepted; no system setting or license was changed. A small dependency-free Node implementation instead screens exact matrix ranks modulo 65521. For B3, all 23,040 triples with first element up to signed-cycle conjugacy give no horizontal kernel. For B4, all 2,949,120 such triples give 14 modular candidates, all of which have no horizontal rational kernel under a separate Fraction-based elimination. These are finite exact exclusions, not a universal holonomy theorem. They cover the sign-standard S4 representation missing from the preceding degree-five permutation search. Estimated discovery completion **4%**.

The current fixed-space modular rank comparison is safe at odd characteristic for signed permutation constraints, but is being replaced by an integer signed-graph fixed-space computation to make this part independent of an unstated rank fact.

## 2026-10-24T22:36:00Z — arbitrary-order dihedral reduction

For a noncommuting irreducible finite orthogonal 2D representation, all stable-letter matrices are rotations or reflections in a finite dihedral group. Normalize the phase of one reflection to 1. The six scalar equations on A,conj(A),B,conj(B),T,conj(T) have a two-variable Laurent determinant with 7 or 9 terms, computed exactly in dihedral_determinant.py. All seven patterns are preserved in dihedral_determinants.json. No torsion classification is claimed yet. The outstanding tasks are to bound all root orders rigorously, handle rank-deficient torsion supports and singular kernels, and then confront higher-dimensional irreducible finite groups. Estimated discovery completion remains **4%**.

## 2026-10-24T22:39:07.051716+00:00 — arbitrary-order dihedral partial frozen for review

DIHEDRAL_OBSTRUCTION.md and its six computation artifacts are frozen in DIHEDRAL_MANIFEST.json. Every necessary minimal-relation partition has exponent lattice Z²; hence all torsion zeros have phases in mu210. The exact 7 x 44,100-pair check leaves only (1,1), whose stable-letter matrices commute. This proposes an all-finite-dihedral obstruction, with arbitrary original vertex rotations handled by the powers argument. A fresh independent reviewer is requested. The full higher-dimensional finite-group gap remains; discovery completion **4%**. The signed-graph fixed-space implementation has also replaced the modular fixed-space comparison, with unchanged B3/B4 results.

## 2026-10-24T22:55:47.585081+00:00 — root exact positive certificate defeats candidate negative route

Root found and exactly reconstructed a positive517-type symmetric multiset. independent_positive_check.py independently checks every full signed projection balance using integer arithmetic, all positive multiplicities, total95419250146190292634685757020254542, gcd1 and all norm identities. Thus the universal all-Q-negative assertion for this candidate is **DEFEATED**, while the reviewed abelian/dihedral obstructions remain valid. The primary full positive-implication review is coordinated by root. Full21.124 discovery estimate **4%**.

## 2026-10-24T22:55:47.585081+00:00 — broader mechanism and terminal family scope

HEIGHT_SMOOTHING.md gives a precise rational-function positivity criterion and proves its height-convolution sufficiency. The first fresh reviewer caught the claim that a Z shift made negative X/Y powers ordinary; corrected to a polynomial in Z with nonnegative integer Laurent coefficients in X,Y, preserving horizontal support. Corrected note refrozen atd59c85f4f08a12ac4eaa6d5af55658b57ef70a1623e91e39bb20c09f6b29ba21. The proposed general Gram-to-positive-rational-kernel implication remains unsupported and is marked blocked at that central assertion. SYNTHESIS.md records every family mechanism, evidence, status and exact gap. No complete21.124 solution, originality claim or publication follows. Full-goal estimate **4%**; assigned Pell negative candidate is closed by a positive witness, pending the fresh full implication audit.

## 2026-10-24T22:56:24.720979+00:00 — final smoothing quantifier repair

Fresh reviewer additionally requested that the explicit family parameter m be stated to be an integer, since its threshold4m−3 is an integer exponent. Applied that prose-only correction and refroze HEIGHT_SMOOTHING.md at4ca4fb4f8af3fa4a6f545398340ecd060a773a6817eb6ac34e63f89396e702d9. Checker/results unchanged. Full21.124 discovery estimate **4%**.

## 2026-10-24T22:56:56.678189+00:00 — terminal review reconciliation

Inspected actual regular_reduction_review/RECEIPT.json (PASS, exact proofhash6372e5f...) and pell_positive_review/RECEIPT.json (PASS, full exact positive witness, VRC and virtual specialness by prior theorems). Thus the original Pell negative route is conclusively defeated under the independently reviewed criterion. No outstanding substantive objection remains to the positive candidate result. The full Kourovka question is still unresolved. Updated best guess completion toward full21.124 research goal **6%**, reflecting the exact resolved candidate and clarified mechanism, not a solved-problem claim.
