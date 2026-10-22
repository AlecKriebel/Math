# Author turn 1: exact packing reduction

2026-10-03 UTC. Problem 30001895 / OWR-11136-027, part 2′ only.
Status: partial deductions and bounded computation; central assertion unproved.
Best-guess completion toward resolving the r-element component: 10%.
This is one substantive author response. Source triage and the credited
hyperplane refutation used zero author turns. No novelty claim is made for
the elementary reductions below. They await independent mathematical review.

## Exact target and prior credit

Let r be a positive integer and let r+1 ≤ q ≤ p be integers. Let F be a
family of distinct r-element subsets of a ground set, with |F| ≥ p. Assume
every p distinct members contain q with nonempty common intersection.
Must F have a transversal of cardinality at most p−q+1?

The source does not specify finite F. We first treat finite F and prove
below that a theorem for finite families would extend to arbitrary families
of nonempty sets of rank at most r. Families here are simple, not multisets.
Empty member sets are excluded. The nonvacuity assumption |F| ≥ p is explicit.

Primary source: V. L. Dol’nikov, Problem 8(2′), OWR 44/2011, printed p. 2541,
[publisher PDF](https://ems.press/content/serial-article-files/46358).
Part 2, about hyperplanes, is a different requested component and is already
refuted by the finite planar line families of Keller–Smorodinsky,
[arXiv:1809.06451v2](https://arxiv.org/abs/1809.06451v2), Theorem 1.1.
That published negative certificate is prior work, not a new result here.
It does not establish either answer for part 2′.

## 1. Exact bounded-degree packing formulation

For a finite hypergraph H with m distinct nonempty edges, write τ(H) for its
transversal number and Δ(H) for its maximum vertex degree. For integer s≥1,
define ν_s(H) as the largest cardinality of a subfamily M⊆H such that every
vertex belongs to at most s members of M. Edges have multiplicity at most one.

**Lemma 1.** For m≥p and s=q−1, the common-intersection (p,q)-property is
equivalent to ν_s(H)≤p−1.

Proof. A p-member subfamily has no q members with a common vertex precisely
when its maximum vertex degree is at most q−1=s. A larger s-packing contains
a p-member s-packing. These observations give both directions. ∎

**Lemma 2.** For every finite H and s≥1,

    ν_(s+1)(H) ≥ min(m, ν_s(H)+1).

Proof. If a maximum s-packing uses every edge, both sides equal m. Otherwise
add any one edge outside it. Every vertex degree increases by at most one.
The resulting family is an (s+1)-packing of size ν_s(H)+1. ∎

Consequently, for s≥r,

    ν_s(H) ≥ min(m, ν_r(H)+s−r).                       (1)

**Exact equivalent conjecture C_r.** For every finite simple hypergraph H
of nonempty edges of rank at most r,

    ν_r(H) ≥ min(m, τ(H)+r−1).                       (2)

Equivalently, when Δ(H)>r (so ν_r(H)<m),

    τ(H) ≤ ν_r(H)−r+1.                              (3)

This is a conjectural inequality, not a theorem proved by this turn.

**Proposition 3.** The requested finite assertion for all r+1≤q≤p is
equivalent to C_r. It suffices to settle q=r+1 for all p.

Proof of sufficiency. Assume C_r and let H have the target (p,q)-property,
where m≥p. Put s=q−1≥r. Lemma 1 gives ν_s≤p−1<m, whence ν_r<m. Thus (3)
applies. The minimum on the right of (1) cannot equal m, as ν_s<m. Hence
ν_s≥ν_r+s−r, and

    τ ≤ ν_r−r+1 ≤ ν_s−s+1 ≤ p−s = p−q+1.

Proof of necessity. For Δ(H)>r, one has m≥r+1 and r≤ν_r<m, since any r
edges have maximum degree at most r. Put p=ν_r+1 and q=r+1. Then m≥p≥q,
and Lemma 1 gives the (p,q)-property. The target assertion implies (3).
When Δ(H)≤r, one has ν_r=m, and (2) is automatic. ∎

The exact-r/rank-at-most-r equivalence used in this proposition is justified
in the next section. No bounded-degree hypothesis is added to H itself:
the bounded-degree condition applies only to the packing subfamily.

## 2. Uniformization and arbitrary-family reduction

**Lemma 4 (private padding).** The target for nonempty sets of rank at most r
is equivalent to the target for exactly r-element sets, for q≥2.

Proof. For each edge E of size smaller than r, adjoin r−|E| new elements
which occur in no other edge and are outside the original ground set. Call
the padded family H′. Distinct edges remain distinct. For any two or more
distinct edges, their common intersection is unchanged by padding, so the
(p,q)-property is preserved. A transversal of H is a transversal of H′.
Conversely, replace every private new element used by a transversal of H′
with one arbitrary element of its unique nonempty original edge. This hits
H and does not increase cardinality. Thus τ(H′)=τ(H). Restricting a theorem
for rank-at-most-r families to uniform ones gives the converse. ∎

**Lemma 5 (finite obstruction).** If a family H of nonempty sets of size at
most r has no transversal of size at most t, it has a finite subfamily with
the same property, of size at most 1+r+⋯+r^t.

Proof by induction on t≥0. For t=0, choose any edge; the hypothesis ensures
one exists. For t≥1, choose E∈H. For every x∈E, let H_x consist of the edges
not containing x. This family has no (t−1)-transversal: otherwise adjoining
x would give a t-transversal for H. By induction choose a finite witness
W_x⊆H_x of size at most 1+r+⋯+r^(t−1). Put W={E}∪⋃_(x∈E)W_x. Its size
has the claimed bound. If T of size at most t hit W, choose x∈T∩E. As no
member of W_x contains x, T\{x} would hit W_x, a contradiction. ∎

**Corollary 6.** A positive answer for finite nonvacuous families implies a
positive answer for arbitrary nonvacuous families of rank at most r.

Proof. Put t=p−q+1. If H had no t-transversal, Lemma 5 would give a finite
witness W. Enlarge W to a finite W′⊆H of size at least p, using |H|≥p.
It inherits the (p,q)-property, so the supposed finite theorem would give a
t-transversal for W′ and hence W, a contradiction. ∎

Thus the finite/infinite distinction introduces no further mathematical gap
once the finite theorem is proved. The finite theorem itself remains open
within this attempt. For exact-r families the corollary uses their existing
rank bound; no infinite cardinal arithmetic is involved.

## 3. Sanity checks, sharpness, and one blocked shortcut

The boundary p=q follows directly from rank-r Helly: if all edges have empty
total intersection, choose E and, for each x∈E, an edge excluding x. These at
most r+1 edges have empty intersection. Extend them to p edges, contradicting
the (p,p)-property. This proves only that boundary case.

For r≥2, let H consist of r+1 edges sharing one vertex, with pairwise disjoint
(r−1)-element petals, together with k disjoint r-element edges outside them.
Then τ=k+1, ν_r=k+r, and m=k+r+1. Taking p=m and q=r+1 gives equality
τ=p−q+1. Thus the constant in (3) cannot be improved. For r=1, distinct
singleton edges never have a common point in pairs, so no nonvacuous target
instance exists when q≥2; C_1 is automatic.

A merely inclusion-maximal r-packing cannot replace a maximum one. In K_4
(viewed as a rank-2 hypergraph), a triangle is an inclusion-maximal 2-packing
of size 3, yet τ(K_4)=3>3−2+1. A 4-cycle is a maximum 2-packing and has size 4.
Thus a naive cover bound from arbitrary saturated vertices of a maximal
packing is blocked. A successful augmentation proof must use stronger
optimality or a new structural mechanism.

## 4. Bounded exhaustive checks

The accompanying C++ program enumerates every labelled simple r-uniform
hypergraph on each stated n-vertex ground set. It computes τ and ν_r with
integer subset dynamic programming, and tests (3) only when Δ>r.

For τ, choose one edge e of H; every cover uses some v∈e, so
τ(H)=1+min_(v∈e) τ(H minus all edges containing v). For ν_r, H itself is
feasible when Δ≤r. Otherwise every feasible subfamily omits an edge, giving
ν_r(H)=max_(e∈H)ν_r(H\{e}). Both recurrences use strict subsets, processed
before H. The empty-family values are zero.

Cases (n,r): (4,1), (5,2), (6,2), (5,3), (6,3), (6,4), (6,5).
No violation was found. In particular all 2^20=1,048,576 3-uniform labelled
families on six vertices were examined; 1,039,503 had Δ>3. Exact per-case
counts are in turn1_exhaustive_results.json. A separate direct enumeration
of vertex covers and packing subfamilies agrees for (4,2) and (5,3), as
recorded in turn1_independent_bruteforce.json. This second algorithm is a
self-check, not independent mathematical review.

Reproduction:

    g++ -O2 -std=c++17 -Wall -Wextra -Werror exhaustive_uniform.cpp -o exhaustive
    ./exhaustive 6 3
    python3 verify_small.py

These small finite cases give no proof for arbitrary n or r and no justified
confidence estimate for the universal assertion. The next proof turn must
introduce a structural mechanism or counterexample construction beyond the
equivalent inequality (3); a restatement of it will not count as progress.

## 5. Literature checks made during the turn

Targeted searches for simple k-matchings, transversal number, bounded-degree
edge packing, and Dol’nikov (p,q) assertions located terminology but no
source proving (2). This is a bounded negative search, not a novelty claim.
Sources about 2-packings in linear systems or k-matchings defined by
pairwise intersection size use different restrictions or parameters.
They have not been imported as the central inequality.

The exact unresolved step is (3) for an arbitrary finite rank-r hypergraph
with Δ>r. No theorem establishing it has been cited or assumed.
