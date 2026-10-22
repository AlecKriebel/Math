# Four-point obstruction attempt: a precise rank criterion

## Status

The proposed sufficiency of excluding the known four-element algebras R1, R2, R3 is **not proved here**. Necessity is immediate and is old obstruction machinery. The following independent argument isolates a concrete metric lemma whose proof would suffice, without presuming that closure preserves unweighted distances. It applies to infinite graphs as well as finite ones.

## Setup

Let G be an apiculate graph, S a nonempty apex-closed subset, and J(x,y)=S intersect I_G(x,y). Let H have vertex set S and an edge xy precisely when J(x,y)={x,y}. For u in S put x <=_u y when x belongs to J(u,y). This is a partial order. Define

r_u(v) = maximum number of strict steps in a chain from u to v in this order.

This maximum exists: every such chain has at most d_G(u,v) strict steps. This does not require finite intervals or a finite graph. Maximum-length chains are saturated. If consecutive points x<y in such a chain had a third point of J(x,y), that point could be inserted, by graph metric betweenness. Consequently every maximum-length chain is an H-path. In particular H is connected and d_H(u,v) <= r_u(v).

## Proposition: an exact edge-rank characterization

The interval system J is realized by the unweighted graph H if and only if the following property holds for every u and every H-edge xy:

1. If x<_u y, then r_u(y)=r_u(x)+1.
2. If y<_u x, then r_u(x)=r_u(y)+1.
3. If x and y are incomparable in <=_u, then r_u(x)=r_u(y).

### Necessity

If J=I_H, any maximum-length chain from u to v is an H-geodesic, so r_u(v)=d_H(u,v). Adjacent distances from u differ by at most one. If they differ by one, the nearer endpoint lies on an H-geodesic to the farther endpoint and is therefore comparable in <=_u. Conversely comparable adjacent points have distances differing by one. These give all three assertions.

### Sufficiency

The three assertions imply that r_u is 1-Lipschitz on H. Every u-v path therefore has length at least r_u(v). The saturated chain above gives a path of exactly that length, proving d_H(u,v)=r_u(v).

If z belongs to J(u,v), choose saturated chains from u to z and from z to v. Their concatenation is a chain in <=_u and an H-path, because original graph betweenness is transitive along an interval. Every edge along it increases r_u by one, by assertion 1. Its length is therefore r_u(v)=d_H(u,v). Thus z belongs to I_H(u,v).

Conversely, along an H-geodesic from u to v, the total increase of r_u equals its length. Every edge must consequently increase r_u by one. Assertion 3 excludes incomparable endpoints, and assertion 2 excludes a decrease in the basepoint order. Thus the path is an increasing <=_u chain. Each of its vertices belongs to J(u,v), proving I_H(u,v) subset J(u,v).

Finally interval equality reproduces the restricted apex operation: its fixed-basepoint meets are determined by these intervals. Thus H is apiculate and is the required realization.

## What the proposed four-point theorem must still establish

Suppose S contains no closed copy of R1, R2 or R3. By Part II, Lemma 4, every four-element closed subalgebra is graphical. To prove the candidate characterization, it suffices to deduce the three edge-rank assertions above from that hypothesis for every such S. Conversely a counterexample must exhibit a canonical edge and basepoint violating at least one assertion.

There are two logically separate difficulties:

- Comparable-edge failure: saturation need not a priori imply that all maximal chains in a basepoint interval have the same length. One must exclude a rank jump larger than one at a cover, not merely observe that the ambient graph's distance rises.
- Incomparable-edge failure: a canonical edge can join two branches whose maximal chain lengths from the basepoint differ. Ambient edge lengths after compression are unequal, and closure does not by itself equalize them.

A tempting route is to derive graded interval lattices from R1-exclusion, then derive equal ranks on incomparable edges from R2/R3-exclusion. Neither implication has been established here. In particular, the closure of four selected witnesses may introduce further vertices; one cannot simply apply the four-point classification to a nonclosed quartet.

The known quadrangle result (Part II, Lemma 5) does imply that an R1-free apiculate **graph** satisfies the quadrangle condition. Applying this directly to H is circular before its apex realization has been established. Likewise, the sufficient triangle condition for geometric interval spaces in Part II Section 6 is stronger than what is needed here: the graphical house already has metric triangles with unequal side lengths. A proof relying on that condition would exclude a verified positive example.

## Proven scope

The rank proposition is a necessary-and-sufficient realization test for each closed subset, not the requested structural classification. It is an authored reduction, without a claim of novelty. The finite atlas result remains evidence only. The unrestricted four-point sufficiency claim, and therefore the classification questions, remain open within this work.

## Additional bounded counterexample search

A deterministic-seed randomized experiment sampled 4,000 Erdos–Renyi graphs of orders 8, 9 and 10, with edge probabilities chosen from 0.15, 0.25, 0.4, 0.55, 0.7 and 0.85. Of these samples, 2,810 were connected, 412 were apiculate, and 288 had no bad four-point closed subset. Every proper closed subset of size at least five in those 288 samples was tested by canonical reconstruction and full apex-table comparison; no counterexample was found. These are sample counts, not distinct isomorphism classes. Seed: 1815. Script: computation/random_four_point_search.py. This is weak supplementary evidence, not a proof or exhaustive order-eight test.
