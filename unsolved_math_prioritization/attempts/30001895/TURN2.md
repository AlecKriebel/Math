# Author turn 2: saturated vertices and critical counterexamples

2026-10-03 UTC. Problem 30001895, r-element component only.
Status: unfinished; author response 2 of 5. Subjective completion estimate: 20%.
The main inequality remains a conjecture for general r≥3. The reductions in
TURN1.md are preserved; none is being treated as a full solution.

This response explores structural covering and edge-criticality. Computation
checks two explicit examples, rather than enlarging the previous exhaustive
scan. The published hyperplane refutation remains credited prior work.

## 1. Newly located prior coverage: r=2

Alfaro, Rubio-Montiel and Vázquez-Ávila, *Covering and 2-degree-packing numbers
in graphs*, Open J. Discrete Applied Mathematics 7(1) (2024), 1–10,
[DOI](https://doi.org/10.30538/psrp-odam2024.0094), Proposition 5 and Theorem 6
on p. 3, prove τ(G)≤ν₂(G)−1 for finite simple graphs with |E(G)|>ν₂(G).
Their degree-packing parameter agrees exactly with TURN1.md. The primary
[publisher text](https://pisrt.org/psr-press/journals/odam/04-vol-7-2024-issue-1/covering-and-2-degree-packing-numbers-in-graphs/)
and PDF were checked. [arXiv:1707.02254v3](https://arxiv.org/abs/1707.02254v3)
is dated 9 December 2019, with an initial version from 2017. Its abstract
states the connected case; the published Proposition 5 states the general
simple-graph case. Alternatively, add the connected-component inequalities,
using τ≤|E|=ν₂ for components of maximum degree at most two.

Together with the packing growth, padding, and finite-obstruction reductions
of turn 1, this supplies a credited affirmative answer for r=2 and every
3≤q≤p, including arbitrary nonvacuous families. This is prior literature,
not a new theorem from this attempt. It does not cover r≥3. The proof's
path-and-cycle mechanism does not immediately extend to hypergraphs.

## 2. A general covering certificate from any maximal packing

Let H be a finite hypergraph of distinct nonempty edges of rank at most r.
Let M⊆H be an inclusion-maximal r-packing, and define

    S = {v : degree_M(v)=r},
    N = {e∈M : e∩S is nonempty},
    M₀ = M\N,
    D = |N|−|S|.

Here maximal means that no one edge can be added, and does not mean maximum
cardinality. Every edge of H\M meets S, since otherwise it could be added.
Every vertex in S is incident with r edges of N. Since each edge has at
most r vertices, counting incidences gives

    r|S| ≤ r|N|, hence D≥0.

The set S together with any transversal of M₀ covers H. Therefore

    τ(H) ≤ |S|+τ(M₀)
         = |M|−D−(|M₀|−τ(M₀)) ≤ |M|.               (4)

In particular the universally valid bound τ(H)≤ν_r(H) follows by choosing
a maximum packing. This is weaker than the desired saving r−1; no novelty
is claimed for this elementary incidence argument.

For a maximum packing, define the certificate saving

    Q(M)=D+|M₀|−τ(M₀).

If Q(M)≥r−1, (4) proves the desired inequality for that H. For an r-uniform
H, let b count incidences between edges of N and vertices outside S. Then
r|N|=r|S|+b, so D=b/r exactly. This identifies a concrete source of savings.
For rank-at-most-r H, missing edge positions also contribute to D.

Another sufficient case for uniform H is |V(H)|≤ν_r(H), where V(H) is the
union of the edges. Any |V(H)|−r+1 vertices form a transversal, giving the
required upper bound. A general counterexample therefore needs more
vertices than its maximum packing size.

## 3. Why maximum-packing surplus is still insufficient

Turn 1 showed that an arbitrary maximal packing can fail to provide the
desired bound even in K₄. Maximum cardinality fixes that particular failure,
but maximizing Q(M) over all maximum packings is not a complete method.

Take the seven triples

    012, 034, 056, 135, 146, 236, 245

on vertices {0,1,2,3,4,5,6}, and adjoin the triple 017 using a new vertex 7.
Call the resulting 3-uniform family H. The first seven triples are the Fano
plane lines. Every pair of old vertices hits exactly five of those seven
triples; a pair involving vertex 7 hits at most three. Thus τ(H)≥3. The
triple {0,1,2}, viewed as a transversal, hits all eight edges, so τ(H)=3.

The full eight-edge family has degree four at vertices 0 and 1. Deleting
one edge gives a 3-packing precisely when the deleted edge contains both
0 and 1, namely 012 or 017. Thus ν₃(H)=7 and these are exactly its two
maximum packings.

- Delete 017: all seven old vertices are saturated, N=M, M₀ is empty,
  and Q(M)=7−7=0.
- Delete 012: precisely vertices 0,1,3,4,5,6 are saturated, all seven
  selected edges meet them, M₀ is empty, and Q(M)=7−6=1.

Consequently max Q(M)=1<r−1=2, while |V(H)|=8>ν₃(H)=7. Both sufficient
certificates above fail, even though τ(H)=3≤5=ν₃(H)−2 is easily true.
The accompanying structural_checks.py verifies every stated finite value
by direct enumeration and produces turn2_structural_results.json.

This is a counterexample only to the completeness of the surplus strategy.
It is not a counterexample to the target. Any further use of this route
requires another mechanism, such as exploiting transversal-criticality.

## 4. Structure forced on an edge-minimal counterexample

Assume a counterexample to C_r exists and choose one, H, with as few edges
as possible, for fixed r. By private padding before minimization, one may
work within exactly r-uniform families. All statements below also hold in
the rank-at-most-r formulation. Write t=τ(H), k=ν_r(H), and h=|H|.
Then Δ(H)>r and t≥k−r+2.

**Proposition.** For every e∈H,

    Δ(H\{e})>r,
    ν_r(H\{e})=k,
    τ(H\{e})=t−1,
    t=k−r+2.                                       (5)

Proof. If Δ(H\{e})≤r, then k=h−1 because H is not an r-packing. A vertex
of degree greater than r in H must have degree exactly r+1. Take that
vertex and one representative from each edge not containing it. This gives
a transversal of size at most 1+h−(r+1)=h−r=k−r+1, a contradiction.

Thus every single-edge deletion still has maximum degree greater than r.
By minimality it satisfies the conjectured inequality. Removing one edge
decreases τ by at most one and cannot increase ν_r. Hence

    k−r+1 ≤ t−1 ≤ τ(H\{e})
           ≤ ν_r(H\{e})−r+1 ≤ k−r+1.

All inequalities are equalities, proving (5). ∎

So a minimal counterexample is τ-critical, meaning every edge deletion
reduces the transversal number, while no edge deletion reduces ν_r. In
particular the violation is exactly one above the target, not arbitrarily
large. At r=3 its parameters must satisfy τ=ν₃−1.

It is also incidence-connected after discarding isolated vertices. Indeed,
τ and ν_r are additive across components, and (4) shows ν_r−τ≥0 in each
component. Since the total deficiency ν_r−τ is at most r−2, any component
with Δ>r is itself a counterexample. Minimality leaves only that component.

Finally t≥3. A τ-critical family with t=1 has only one edge. A τ-critical
family with t=2 is a minimally empty-intersection family; it has at most
r+1 edges by the rank-r Helly argument from turn 1. Every vertex misses at
least one edge, so its maximum degree is at most r. Both alternatives
contradict Δ(H)>r.

## 5. A finite critical-family bound for each t

Bollobás, *On generalized graphs*, Acta Math. Acad. Sci. Hungar. 16 (1965),
447–452, Theorem 2 on p. 452, gives at most binom(t+r−1,r) edges for a
t-critical r-uniform hypergraph. The formula was checked in the original
[paper scan](https://web.vu.lt/mif/s.jukna/EC_Book_2nd/Bollobas.pdf).

For completeness, its set-pair argument applies here as follows. For each
edge e, choose a (t−1)-transversal T_e of H\{e}. It is disjoint from e,
or it would cover H. If f≠e, then f∩T_e is nonempty. The classical Bollobás
set-pair inequality therefore gives h≤binom(t+r−1,r). This is a credited
standard theorem, not a new bound. With all isolated vertices removed,
there are at most r·binom(t+r−1,r) vertices.

For r=3 and t=3, a minimal counterexample would therefore have ν₃=4,
at most ten edges and at most thirty vertices, and satisfy every condition
in (5). This is a bounded, structurally justified search class, but it has
not been classified or exhausted here. The bound grows with t and does
not reduce the whole conjecture to a single finite computation.

## 6. Exact remaining gap and next mechanism

Known prior coverage now includes r=2; the general r≥3 question remains
unsettled by this work. Neither the saturation certificate nor the critical
reduction proves that a counterexample is impossible. The extended Fano
example blocks reliance on saturation surplus alone.

A genuinely new next step would analyze τ-critical uniform families subject
to (5), using their private (t−1)-transversals, or construct such a family
with ν_r=t+r−2. The small t=3 regime is now explicitly bounded. No further
author turn should simply relabel the same unproved packing inequality as
a lemma. Independent mathematical review remains pending.
