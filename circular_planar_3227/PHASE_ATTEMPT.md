# Circular (20,7) phase attempt: what is equivalent, and what actually fails

## Outcome

No proof of the general triangle-free planar subcubic bound was obtained. The unconstrained phase formulation is an exact rewriting of the coloring problem, not a relaxation or a new theorem. Two natural restrictions fail, even on small planar cubic examples. In particular, on the dodecahedral graph, **every even-2-factor choice fails a real phase lift confined to an interval of width at most 8**, while an explicit integral lift of width 9 succeeds. This is a counterexample only to the restricted narrow-band method, not to the desired circular-coloring bound.

The exact, dependency-free checker is `check_phase.py` in this directory. It runs in substantially less than a second in this environment.

## 1. Exact equivalence

Let a cubic graph have a perfect matching M whose complement F is an even 2-factor. Choose a biparity b:V→{0,1} alternating on every F-cycle, independently choosing a flip for each cycle. Put

c(v) = 10 b(v) + phi(v) modulo 20.

A (20,7) coloring requires c(v)-c(u) modulo 20 to lie in {7,...,13} on each edge. Consequently:

- If b(u) differs from b(v), the phase difference must lie in {-3,...,3} modulo 20.
- If b(u)=b(v), the phase difference must lie in {7,...,13} modulo 20.

Every F-edge is of the first kind. Only matching edges can be of the second kind. For fixed b, phi ↔ c is bijective. Therefore proving arbitrary modular phases exist proves exactly the original coloring assertion; it does not independently simplify it.

Invoking the standard Tait/Four-Color-Theorem consequence gives an even 2-factor for a bridgeless cubic plane graph. This does not itself handle bridges or the reduction from arbitrary subcubic graphs. Those reductions would still need to be justified in any full argument.

## 2. Constant phase per F-cycle fails

Take the pentagonal prism with top vertices t0,...,t4, bottom vertices s0,...,s4, ring edges, and rungs ti-si. The cycle

t0,t1,t2,t3,t4,s4,s3,s2,s1,s0,t0

is an even Hamiltonian 2-factor. Its complementary matching contains t0-t4 and s0-s4, whose endpoints have the same cycle biparity. A constant phase on the sole F-cycle gives phase difference zero on both edges, violating the required long difference. The graph is planar, cubic and triangle-free. In particular, these hypotheses cannot make constant phase on each chosen F-cycle work automatically.

This example does not assert that every alternative matching of the prism fails every other restricted method.

## 3. A genuinely stronger obstruction: interval width at most 8

Consider G(10,2), the standard dodecahedral graph. Use vertices 0,...,19 and indices i modulo 10, with edges

- i -- (i+1),
- i -- (10+i),
- (10+i) -- (10+(i+2)).

A narrow-band lift means all phases admit simultaneous real representatives in a common interval [a,a+W]. Subtracting a globally, assume [0,W]. For W≤9, modular constraints become the ordinary constraints

- |phi(v)-phi(u)|≤3 on opposite-b edges (short edges);
- |phi(v)-phi(u)|≥7 on same-b edges (long edges).

The maximum difference is automatically at most W. This is a real additional restriction and is not equivalent to arbitrary modular phases.

The checker exhaustively enumerates perfect matchings, keeps those with bipartite complementary 2-factor, and enumerates independent biparity flips modulo simultaneous global reversal. There are exactly 30 retained choices; every complementary factor is one Hamiltonian 20-cycle. Each has exactly six long matching edges.

### Human-readable obstruction for width strictly below 8

Every endpoint of a long edge must lie in the low interval [0,W-7] or the high interval [7,W], with its partner in the other interval. Low-high separation is at least 14-W>6 when W<8. Thus any two long-edge endpoints joined by a path of at most two short edges must belong to the same category. Identifying endpoints under these short paths produces a contradiction in all 30 cases.

For example take the complementary matching

(0,1), (2,3), (4,5), (6,16), (7,8), (9,19), (10,18), (11,13), (12,14), (15,17).

Its complementary Hamiltonian cycle, in cyclic order, is

0,10,12,2,1,11,19,17,7,6,5,15,13,3,4,14,16,18,8,9.

The long edges are

(0,1), (2,3), (4,5), (7,8), (10,18), (15,17).

The short paths 0--10, 10--12--2, and 2--1 force long-edge endpoints 0 and 1 into the same category, a contradiction.

### Exact certification at width 8

The endpoint-category argument alone is not enough at W=8. The checker instead enumerates the 2^6 possible orientations of the six long edges for each of the 30 cases. Every orientation leaves a system of difference constraints with integer coefficients:

- phi(v)≤phi(u)+3 and phi(u)≤phi(v)+3 for short edges;
- phi(u)≤phi(v)-7 for an oriented long edge u→v;
- 0≤phi(v)≤8.

An extra source variable encodes the bounds. Bellman–Ford initialized to zero either finds feasible potentials or detects a negative cycle. Every orientation is infeasible. This is an exact integer-arithmetic finite computation, not a floating-point MILP infeasibility claim, and rules out real as well as integer solutions at width 8. By containment it also rules out smaller widths.

## 4. Explicit successful width-9 solution

For the displayed matching/cycle, take the phases in vertex order 0,...,19:

7,0,1,8,9,2,5,8,1,4,7,3,4,5,6,2,3,9,0,6.

Using the cycle biparity with b(0)=0 gives colors

7,0,11,18,9,2,15,8,1,14,17,13,4,5,16,12,3,19,10,6.

The checker verifies directly that every edge's modular color difference is between 7 and 13 inclusive. Thus a width-9 integral phase lift succeeds. The minimum width among narrow-band lifts over all these choices is exactly 9, even for real phases. Indeed, if a feasible real lift had width W<9, translate its minimum to zero and floor every phase. Every short-edge inequality has the form phi(v)<=phi(u)+3 and every oriented long-edge inequality has the form phi(u)<=phi(v)-7; flooring preserves both because the constants are integers. The floored phases would lie in {0,...,8}, contradicting the verified width-8 infeasibility. The explicit width-9 lift gives equality.

## 5. Facial pentagons impose a useful local condition, but not a proof

On any 5-cycle, the number of same-b edges is odd: the number of opposite-b edges is even on every closed walk. All same-b edges belong to a matching, and a 5-cycle contains at most two matching edges. Hence every 5-cycle contains exactly one long edge. In an all-pentagonal cubic plane graph, counting incidences gives six long edges for the dodecahedron's twelve faces. This is a local constraint on any prospective phase construction, not a proof that compatible phases exist globally.

Planarity does not remove conflicts across both sides of an even cycle. The explicit obstruction above already occurs on a planar graph. A proof using planar noncrossing structure must allow sufficiently wide phases (at least width 9 here), genuinely modular/winding behavior, or another invariant. Simply restating the modular feasibility system, or asserting a width-8 lift, cannot close this lane.

## Scope and status

- General theorem: unresolved by this attempt.
- Constant-per-cycle phases: not universally valid for a chosen Tait factor.
- Width≤8 interval lifts: exactly refuted on the dodecahedron for every even factor/biparity choice.
- Width-9 lift: explicitly verified on that benchmark only.
- No external publication was performed.
