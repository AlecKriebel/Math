# Author turn 4: extremal links cannot be counterexamples

2026-10-03 UTC. Problem 30001895, r-element component. Author response 4 of 5.
Status: unfinished; completion estimate 30%. The general r≥3 target remains
unresolved. Earlier proofs, certificates, logs and manifests are unchanged.
All new deductions below await uninvolved review; novelty is not claimed.

This turn uses the private transversals of a critical family to constrain
vertex links. It does not enlarge the earlier hypergraph enumeration.
A small, different finite computation classifies nine-edge graph links;
its complete normal-form certificate has a separate checker.

## 1. A strict degree bound for a minimal counterexample in every rank

Let H be a finite, simple, r-uniform, τ-critical hypergraph, where r≥2 and
t=τ(H)≥2. Thus for every e∈H there is a transversal T_e of H\{e} with
|T_e|=t−1, and T_e∩e is empty. The latter follows because otherwise T_e
would cover H as well.

Fix a vertex v. For each edge e containing v, use the set pair

    (A_e,B_e)=(e\{v},T_e).

It has |A_e|=r−1, |B_e|=t−1, A_e∩B_e empty, and A_e∩B_f nonempty for e≠f.
Indeed T_f meets e and cannot contain v. The classical Bollobás set-pair
bound gives

    degree_H(v) ≤ binom(r+t−2,r−1).                 (7)

We also use its uniform equality statement: equality forces the pairs to
be all partitions of one (r+t−2)-element set W into an (r−1)-set and its
(t−1)-element complement. This is a credited theorem, stated explicitly as
Theorem 2.1 on p. 3 of Gerbner, Lemons, Palmer, Patkós and Szécsi,
*Almost intersecting families of sets*, [author-hosted primary paper](https://www.renyi.hu/~gerbner/papers/glpps2.pdf),
which attributes it to Bollobás. The original paper was checked in turn 2.
The equality statement, not merely the numerical inequality, is necessary
for the next deduction.

**Proposition 1.** Equality in (7) at any vertex forces

    H = all r-element subsets of W∪{v},
    |W∪{v}|=r+t−1.

Proof. Equality gives every edge {v}∪A with A an (r−1)-subset of W, and
gives T_e=W\A. Here v is outside W because it belongs to neither part of
any set pair. Every edge f not containing v must meet every T_e. These
T_e range over all (t−1)-subsets of W. Thus |W\f|≤t−2, giving |f∩W|≥r.
Since |f|=r, f lies wholly in W. Every edge of H is therefore contained in
the (r+t−1)-set W∪{v}. If an r-subset B of that set were missing, its
complement, of size t−1, would hit every edge of H. This contradicts τ=t.
Hence all r-subsets occur. ∎

For the complete r-uniform family on n=r+t−1 vertices, the n cyclic
intervals of length r form a simple r-packing: they are distinct because
1≤r<n, and each vertex occurs in exactly r intervals. Counting incidences
also gives ν_r≤n, so ν_r=n and τ=t=ν_r−r+1. Thus it satisfies the target.

Combining this with turn 2, an edge-minimal counterexample must satisfy

    Δ(H) ≤ binom(r+t−2,r−1)−1.                      (8)

Likewise equality in Bollobás' critical-edge bound forces the complete
family, so a minimal counterexample has

    |H| ≤ binom(r+t−1,r)−1.                        (9)

These are restrictions, not a contradiction for every remaining family.

## 2. The rank-three, transversal-four link problem

The next rank-three regime after turn 3 is t=4. A minimal counterexample
there would have ν₃=5, at most 19 edges by (9), and Δ≤9 by (8).
We now rule out degree nine as well.

Suppose a τ-critical 3-uniform H with τ=4 has a vertex v of degree nine.
Its link G is the simple graph with edges e\{v} for e∈H containing v.
It has nine edges. Every graph edge ab has a set T of at most three
vertices, disjoint from {a,b}, which covers all graph edges except ab.
This comes from the private transversal for {v,a,b}; points outside G
can be discarded. Padding to three points inside V(G)\{a,b} is possible
whenever needed, since a nine-edge simple graph has at least five vertices.
Call this the private three-cover condition.

For any graph edge ab, every neighbor of a other than b must belong to its
private cover. Therefore Δ(G)≤4. If some a has degree four, the private
cover for ab is exactly N(a)\{b}. This forces every edge of G to have both
endpoints in {a}∪N(a): an edge from outside to b∈N(a) misses the cover
for ab, and an edge wholly outside misses every such cover. There are
exactly five vertices in this set. Nine edges on five vertices form K₅
minus one edge.

It remains to exclude Δ(G)≤3. The following finite certificate establishes
that exclusion without assuming any graph classification theorem.

## 3. Complete normal forms for the remaining link graphs

Fix an edge uv of G and a private three-cover T={0,1,2}, disjoint from
u=3 and v=4. All eight edges other than uv meet T. Since Δ(G)≤3,

    8 + |E(G[T])| = sum_(x∈T) degree_G(x) ≤9.

Thus G[T] has either zero edges or one edge; in the latter case relabel
T so that its edge is 01. These are the two `internal` cases in the code.

Outside T, the only edge is uv. The neighborhoods in T of u and v have
size at most two, because each is already incident with uv. Every other
vertex has a nonempty neighborhood in T, represented by one of the seven
nonzero three-bit masks. Vertices having the same neighborhood are recorded
by multiplicities; each multiplicity is at most three by the degree bound
at a member of T. There are no other edges or nonisolated vertices.

The tuple

    (internal, u_mask, v_mask, seven neighborhood multiplicities)

therefore describes every possible graph in this case, up to a relabeling
of vertices outside T∪{u,v}. The remaining conditions are exactly nine
edges and degree at most three at all three vertices of T. These normal
forms need not represent pairwise nonisomorphic graphs; harmless repetition
does not affect completeness.

build_link_certificate.py enumerates the forms by recursive remaining-degree
capacities. There are exactly 1,691 admissible forms. For each it saves an
edge ab for which no three vertices disjoint from {a,b} cover G\{ab}.
The complete list is turn4_link_certificate.json. Its SHA-256 is

    a704edd20683cb991ad8e5e5710f06de1a4bc1135359792a53450f2d7c5d9522.

verify_link_certificate.py independently enumerates the entire Cartesian
product of multiplicities 0,…,3, both internal cases, and both endpoint
neighborhood masks. It applies the exact nine-edge and degree conditions
and checks that the certificate contains every resulting form, once as a
normal-form tuple. For each recorded obstruction it reconstructs the graph
and enumerates every three-element subset avoiding the edge endpoints,
verifying that each subset misses another edge. All 1,691 forms and 65,587
cover triples pass. The verifier uses only integer/set operations; it does
not rely on the builder's recursion or a solver verdict.

The graph has at least six vertices when Δ≤3 and there are nine edges, so
a cover of size less than three could always be padded to size three while
avoiding the endpoints. Testing triples therefore excludes all covers of
size at most three. This proves that the Δ(G)≤3 case cannot satisfy the
private three-cover condition.

Reproduction, with Python assertions enabled:

    python3 build_link_certificate.py
    python3 verify_link_certificate.py

Consequently every nine-edge link considered above is K₅ minus one edge,
conditional on the stated exhaustive encoding and certificate-checker
correctness. The final independent audit must assess those conditions.

## 4. A forced six-edge packing from K₅ minus one edge

Write V(G)=W={a,b,c,d,e}, with missing graph edge ab. Thus H contains the
nine triples {v}∪f for all pairs f⊆W except ab.

For an existing pair f, the graph G\{f} is K₅ with two edges missing.
Its vertex-cover number is three: an independent triple would require
three missing pairs, while an independent pair exists. Hence a private
three-cover for the hyperedge {v}∪f uses three vertices of W. Because it
avoids f, it must equal W\f.

Every hyperedge not containing v must meet all nine sets W\f, f≠ab.
If it contains at most two vertices of W, this is possible only when its
intersection with W is exactly {a,b}. Therefore every such hyperedge is
either a triple inside W or a triple {a,b,z} with z outside W∪{v}.

At least one external triple abz must occur. Otherwise {c,d,e} would cover
all H, contradicting τ=4. Moreover every triple B⊆W not containing both
a and b must occur. If such B were missing, then

    {v} ∪ (W\B)

would be a three-point cover: it hits every v-edge, every present triple
inside W, and every external abz because W\B meets {a,b}.

In particular acd and bce occur. Choose one external abz. The following
six edges of H then form a 3-packing:

    acd, bce, abz, vad, vbe, vde.

Their vertex degrees, in the order (v,a,b,c,d,e,z), are

    (3,3,3,2,3,3,1).

All six triples are distinct. The three v-edges are present because none
uses the missing pair ab. The complete edge list and degrees are also
saved in turn4_six_edge_packing.json. Therefore ν₃(H)≥6.

**Proposition 2.** A τ-critical 3-uniform family with τ=4 and ν₃≤5 cannot
have a vertex of degree nine. Combined with Proposition 1, it has Δ≤8.
This excludes a degree regime, not every τ=4 family.

## 5. Exact remaining obstruction

For r=3, t=4, an edge-minimal counterexample would now have

    τ=4, ν₃=5, 7≤|H|≤19, and 4≤Δ≤8,

as well as connectedness, τ-criticality and deletion-stable ν₃ from turn 2.
The lower edge bound follows from Δ≤|H|−3 when τ=4. The present turn has
not exhausted, excluded or constructed this remaining family.

For general r, the strict critical-degree and critical-edge bounds (8)–(9)
hold for a minimal counterexample, but they leave infinitely many parameter
values. No complete candidate proof or target counterexample has emerged.
The proof budget now has one substantive author response remaining.
