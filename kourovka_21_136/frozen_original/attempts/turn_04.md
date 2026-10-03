# Attempt 4: an affine counterexample candidate and its obstruction

Date: 2026-10-03. Fourth substantive proof attempt for KOU-21.136.
The candidate fails. Exact finite computations below check the mechanism; they
do not certify any assertion about all profinite groups.

## 1. Why the candidate initially looks promising

Consider G = Z_p semidirect Z_p^times, with multiplication

  (b,u)(c,v) = (b+uc, uv).

The normal translation group A = {(b,1)} is torsion-free, but all its nonzero
elements of a fixed p-adic valuation are conjugate in G. Indeed

  (a,v)(b,1)(a,v)^(-1) = (vb,1).

Thus A contains c internally different infinite-order classes but meets only
countably many ambient classes: one for each finite valuation. This explicitly
demonstrates how the natural closed-subgroup reduction can lose the cardinal
information it needs. It is not a counterexample to inheritance of P from a
group satisfying P, because this G will fail P.

## 2. The complement creates continuum many new classes

The projection G -> Z_p^times is a continuous homomorphism to an abelian group.
Conjugate elements therefore have equal multiplier u. The principal-unit group
1+pZ_p (use 1+4Z_2 when p=2) is infinite, torsion-free, and has cardinal c.
The elements (0,u) for nonidentity units in that subgroup have infinite order
and pairwise different multiplier images. They consequently occupy c different
G-classes. The compression of translation classes is exactly offset by a new
family of nonconjugate infinite-order elements elsewhere in the group.

Replacing the complement by a profinite torsion group cannot retain this
mechanism: its action on a normal Z_p subgroup has torsion image in Z_p^times,
hence finite image. Then Attempt 2 already forces c classes among generators of
the translation subgroup. So both the infinite-unit and torsion-unit variants
of this simple construction fail.

## 3. Finite models and a closed-form class count

Let R = Z/p^n Z and G_n = R semidirect R^times. Conjugation is exactly

  (a,v)(b,u)(a,v)^(-1) = (vb+(1-u)a, u).

Fix u and let d = min(v_p(1-u),n), with v_p(0) truncated to n. Translation by
(1-u)a changes b by the ideal p^d R. Unit multiplication then has one orbit for
each of the d finite valuations 0,...,d-1 in R/p^d R and one for zero. Thus there
are d+1 conjugacy classes with multiplier u. Summing gives

  k(G_n) = phi(p^n) + sum_{j=1}^n p^(n-j)
         = p^(n-1)(p-1) + (p^n-1)/(p-1).

For multiplier 1, the n+1 translation classes have sizes 1 at zero and
(p-1)p^(n-k-1) at valuation k < n.

The standard-library script checks ten groups: p=2 with n=1,...,5; p=3 with
n=1,...,3; and p=5 with n=1,2. It constructs the actual pair multiplication and
inversion, enumerates full conjugacy orbits, compares them with the separate
explicit formula, and verifies both class counts and translation orbit sizes.
All assertions pass. The largest group checked has order 512. The total class
counts are respectively 2,5,11,23,47; 3,10,31; and 5,26.

Run: python3 checks/affine_controls.py
The exact output is checks/affine_results.json. No external package is required.

Every G_n is finite and has no infinite-order elements. These computations are
controls on fusion formulas, not finite approximations that prove the original
infinite-order claim. The infinite-group conclusion in section 2 comes from the
explicit abelian quotient and its torsion-free principal units.

## Outcome

The natural affine construction does not refute the conjecture. It also shows
why merely counting classes in a chosen non-torsion normal subgroup is not
enough. A hypothetical counterexample would need to control the classes of its
conjugating elements as well. Attempt 5 investigates the topology of the full
space of infinite-order classes, rather than a selected subgroup.
