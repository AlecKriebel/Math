# Accepted final frontier and remaining problem

The target is an outgoing universal monochromatic source or an actual directed cyclic rainbow triangle. A path's color can depend on its destination. Transitive rainbow triples are allowed. An incoming sink is not a substitute.

## All-order induced-minimal symmetry exclusion

[The structural proof](STRUCTURAL_PROOFS.md) gives the full argument. Shen's failed-predecessor theorem places an induced-minimal counterexample on a distinguished full cycle. Every direction-preserving symmetry that applies one global color permutation preserves the unique failed-predecessor relation, and thus commutes with this cycle. The symmetry group embeds into its rotations. Transitivity would force the entire rotation group, with an odd order and a three-cycling action on colors. The exact-color kernel has three residue-class orbits; it is not globally transitive.

On each fiber the self-contained balanced-SCC covering lemma gives a spanning strong color. A one-step shift transports a chosen color to three distinct fiber colors, without requiring uniqueness of strong-color choices. The complete reachability-to-every-nonpredecessor hypothesis, internal strong connectivity and kernel symmetry force every offmatching backward pair to be an actual arc in the third color. At order at least nine the actual vertices 0,2,4 form a cyclic rainbow triangle; at order three the distinguished cycle itself is rainbow. This excludes the whole transitive minimal class at every order. The argument is independent of the accepted finite bound.

Without transitivity the same centralizer argument makes the symmetry group a proper odd-order cyclic subgroup of the full rotation group. If p is the least prime divisor of the order, it has at least p vertex orbits; at prime order it is trivial. This is a necessary boundary for a hypothetical minimal counterexample, not an existence claim.

## Exact computational scope

[The finite proof](FINITE_PROOFS.md) gives a bijection with six-state distance vectors and exact monotone pruning for whole-tournament twisted rotations. It fixes the distinguished first arc, forbids every cyclic rainbow triangle and every monochromatic predecessor path, and omits other-to-other reachability, interval, incidence, primeness and minimality constraints. Thus its searched class is a relaxation of the fully transitive minimal class. Candidate zero scopes are 3,9,15,21,27,45,81. Candidate independent code covers larger orders 15,21,27,45; a separate audit implementation covers all seven listed orders. Literal unpruned complete models are exhausted only at 3 and 9.

The raw order-nine counts are 1296 total,432 rainbow-free,54 predecessor-only,zero both. Fixed first-arc counts are 216,72,18,zero. No quotient by an assumed six-fold normalization is used. The order-27 candidate run has 11 nodes and 589 tests. These quantities count encoded rotational models, not all tournaments and not isomorphism classes. Candidate input support through 99 is not a completion claim through 99.

## What remains

The previously accepted general bound remains ten. Its [separate whole/recursive quotient-core application](../3276_symmetry_incidence_20261012/BOUND_TEN_DEDUCTION.md) remains unchanged. Strict periodic lengths 3,6,9 were accepted earlier; periodic 12 is incomplete, so there is no length 12 exclusion. General asymmetric colored-prime full-core possibilities, all unrestricted orders above ten, and arbitrary strict three-periodic obstruction cycles remain unresolved here.

Even if an ambient tournament has a transitive global-color-permuting symmetry group, a minimal induced obstruction inside it need not inherit that group. Therefore the final theorem cannot be extended to all symmetric tournaments by induced minimization. The finite computations have no all-size conclusion; the all-size conclusion for the minimal symmetric subclass comes from the structural proof. This final pass closes the present investigation with the unrestricted target still unsolved.
