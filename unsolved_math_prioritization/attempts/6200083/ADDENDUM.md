# Adopted editorial corrections and scope clarification

This addendum supersedes the corresponding wording in the unchanged frozen
author packet. It adopts the independent audit's three editorial corrections.
The disposition remains **unsolved, five substantive approaches used**. No
full-target proof or counterexample, novelty, or exhaustive literature status
is certified.

## Proper and geodesic examples

The broad sentence in `packet/analysis.md` Section 1 applies only to the two
verified in-scope actions: the parabolic cyclic action on H^2 in Section 2 and
the closed-surface-group action on the hyperbolic Cayley graph in Section 3.
Both use proper geodesic spaces and proper discrete isometric actions.

Section 6 is a failed cone-action proposal, not another verified proper
discrete action. The cone over a general compact metric base is only guaranteed
roughly geodesic by the inspected construction source. Its height-preserving
symmetry action has bounded orbits; its properness and discreteness are not
asserted. The intended orbit-limit realization is missing.

## Signed parabolic displacement

For every integer n, the correct formula in Section 2 is

    d(i,T^n i) = 2 asinh(|n|/2).

The following argument uses n=2^k>0, so its estimate and conclusion are unchanged.
The independently implemented signed control detects the omitted absolute value.

## Exact uniqueness argument

In Section 4, let H be the closed orientable surface group and K the hyperbolic
overgroup supplied by Matsuda--Oguni. Let M be the limit set of H in the boundary
of a finite-generator Cayley graph of K. The connected-tail lemma proves that M
is connected. It is a compact metrizable invariant set carrying a minimal
non-elementary convergence action: H is not virtually cyclic, and its Cayley
action has no parabolic subgroup.

Every nonidentity element h of H has infinite order and is loxodromic in K's
Cayley graph. Both endpoints are limits of positive and negative powers of h,
and hence lie in M. Restriction to M preserves its loxodromic behavior. A
parabolic subgroup of a convergence action contains no loxodromic element;
every nontrivial subgroup of this torsion-free H contains one. Therefore the
peripheral structure of this restricted action is empty.

If the action on M were geometrically finite, M and the usual Gromov boundary
of H would both be Bowditch boundaries for exactly the same pair (H,empty).
Equivariant uniqueness for that pair would produce a homeomorphism from the
boundary of H to M. Composing with M's inclusion in the boundary of K would
contradict Matsuda--Oguni's nonexistence of a continuous H-equivariant map.

This establishes failure of geometric finiteness for that restricted action.
It does not establish failure of local connectedness of M. Nonequivariant
Peano parametrizations are a different matter. The complete local-connectedness
target therefore remains unresolved by this work.

## Preserved evidence

The eight original author files, their freeze manifest, the complete independent
audit, and its embedded author archive are preserved byte-for-byte. The audit
accepts the partial strategy obstructions and unsolved disposition. The
author's 5,859 finite assertions and the auditor's 13,323 checks are reproducible
controls, not proofs of the infinite topology or the external source theorems.
