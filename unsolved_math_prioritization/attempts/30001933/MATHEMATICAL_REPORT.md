# A sharp vertex-count obstruction to direct splitting integrality for rooted arborescences

Target: **30001933 / OWR-11451-006**, Integer Carathéodory Property (ICP) for rooted directed spanning-arborescence polytopes.

## Status and scope

The general ICP question is **unresolved by this work**. This report proves a partial structural boundary:

1. If deleting the root leaves a cactus as the underlying simple undirected graph, the arborescence polytope belongs to the sufficient splitting class of Gijswijt–Regts. Consequently it has ICP. Parallel arcs are allowed.
2. In particular, every rooted digraph on at most four vertices has that stronger splitting property.
3. An explicit rooted digraph on five vertices and eight arcs fails the splitting property: `P intersect (1-P)` has a fractional vertex.
4. The five-vertex example nevertheless has ICP, by an explicit totally unimodular flow lift and the existing Gijswijt–Regts projection theorem.

Thus five is the smallest possible number of vertices for this particular splitting obstruction. This is **not** an ICP counterexample, a resolution of the original problem, a claim of minimum arc count, or a claim of historical novelty. The sufficient-class and projection theorems are credited to Gijswijt–Regts. The proof below is exact.

## 1. Definitions and the exact target

Let D=(V,A) be a finite directed multigraph, and fix a root rho in V. An out-arborescence rooted at rho is a spanning directed tree whose arcs point away from rho. Equivalently, the root has indegree zero, every other vertex has indegree one, and there is no directed cycle. Let P(D,rho) be the convex hull of its arc-incidence vectors. We assume an arborescence exists; otherwise the ICP assertion is vacuous. Loops and arcs entering rho cannot be used and may be deleted, or retained as coordinates identically zero.

ICP says: for every positive integer k and every w in kP with integer coordinates, there are affinely independent integer points p_1,...,p_t of P and nonnegative integers n_1,...,n_t such that

`w = sum_i n_i p_i`, and `sum_i n_i = k`.

For this 0–1 polytope, its integer points are precisely arborescence incidence vectors. The root rho is a vertex, not a number of packed trees. Integer decomposition alone is weaker than ICP.

Write C for the sufficient class of rational polyhedra defined by the condition that, for all nonnegative integers a,b and integer vectors w,

`aP intersect (w-bP)`

is box-integer. A polyhedron is box-integer when intersection with every coordinate box having integral or infinite endpoints is an integer polyhedron. For bounded polyhedra, integrality means all vertices are integral.

Gijswijt–Regts prove: members of C have ICP; every coordinate projection of a member of C has ICP; polyhedra given by totally unimodular (TU) matrices and integral right sides belong to C. Membership in C itself is not generally preserved by coordinate projection.

## 2. An integral unique-lift lemma

**Lemma.** Suppose Q belongs to C, pi is a coordinate projection from Q onto P, and there is an integer matrix L such that `pi L = I` and `Q={Lx:x in P}`. Then P belongs to C.

**Proof.** For a,b,w as in the definition, put W=Lw, which is integral. Linearity and the inverse property give

`L(aP intersect (w-bP)) = aQ intersect (W-bQ)`.

An additional integral coordinate box on x is exactly an integral box on the corresponding projected coordinates of Q, with no restriction on the other coordinates. The right-hand side intersected with that box is integer because Q belongs to C. Coordinate projection of an integer polyhedron is integer. Its projection is precisely the specified box intersection of `aP intersect (w-bP)`. This proves the lemma. Zero scaling causes no difficulty for nonempty polytopes. ∎

The unique, integer-linear lift is essential. Section 5 gives a nonunique integral flow lift whose projection is outside C.

## 3. Cactus after deleting the root

For each unordered pair {u,v} of nonroot vertices joined by at least one arc, call all arcs between u and v its **edge group**. This includes both directions and all parallel copies. Let H be the simple undirected graph on V−rho with these unordered pairs as edges. Suppose H is a cactus: every edge lies on at most one simple cycle. Isolated vertices and disconnected components are allowed.

A subset F of the nonroot arcs is an undirected forest exactly when:

- it uses at most one arc from each edge group;
- on every simple cycle C of H, it uses at most |C|−1 arcs from that cycle's edge groups.

Indeed, a cycle in the multigraph is either a two-edge parallel cycle or projects to a simple cycle of H after extracting a minimal cycle. The listed constraints forbid both. Conversely a forest satisfies every listed inequality. Because H is a cactus, its simple cycles have pairwise disjoint edge sets; they may share vertices.

Construct a directed network as follows. Its auxiliary nodes are a source s, a sink t, a head node h_v for each nonroot vertex v, an edge-group node p_e for every edge e of H, and a cycle node q_C for every simple cycle C of H.

- Add `s -> q_C` with capacity |C|−1.
- If edge e lies on C, add `q_C -> p_e` with capacity 1.
- If e lies on no cycle, add `s -> p_e` with capacity 1.
- For every original nonroot arc u->v in edge group e, add a separate network arc `p_e -> h_v`, capacity 1. This network coordinate is the original coordinate x_(u,v).
- For every original root arc rho->v, add a separate arc `s -> h_v`, capacity 1, again carrying that original coordinate.
- Add `h_v -> t`, fixed to 1, for each v.
- Add `t -> s`, fixed to |V|−1.

All flows are nonnegative and obey flow conservation. Call the resulting bounded circulation polytope Q. A directed incidence matrix is TU, so Q belongs to C by the cited theorem.

Every integral circulation selects exactly one original incoming arc at each nonroot vertex. The edge-group capacities and cycle-node capacities ensure its nonroot arcs form a forest. It therefore contains no directed cycle. Following parent arcs backwards from any vertex must terminate at rho, since every nonroot vertex has a parent and there is no cycle. The selected arcs form an arborescence.

Conversely an arborescence satisfies the edge-group and cycle capacities, and its incidence vector extends to a circulation by sending the indicated sums through the group and cycle arcs. Therefore the coordinate projection of Q is exactly P: Q is integral, so projection is the convex hull of the projections of its integral points; both inclusions follow from the two combinatorial statements.

Moreover, the lift is unique and integer-linear. Flow on a group-input arc is the sum of the original arc coordinates in that group. Flow on `s -> q_C` is the sum over that cycle's groups. Flow on `h_v -> t` is the sum of original coordinates entering v. Flow on `t -> s` is the sum of all original coordinates. Every lifted coordinate is thus an integer linear expression in x. The lemma proves:

**Theorem 1.** If H is a cactus, P(D,rho) belongs to C and therefore has ICP.

**Corollary 2.** Every rooted directed multigraph with at most four vertices has this property. Deleting the root leaves at most three vertices, whose underlying simple graph is a cactus.

These are credited consequences of the existing TU/splitting theory, with the explicit network and preservation argument supplied here. No assertion of novelty is made.

## 4. Five-vertex splitting obstruction

Let V={0,1,2,3,4}, with root 0. Use the following eight arcs, in this order:

- a: 3->1
- b: 4->1
- c: 0->2
- d: 1->2
- e: 0->3
- f: 2->3
- g: 0->4
- h: 2->4

Write P=P(D,0), let w=(1,1,1,1,1,1,1,1), and define

`z=(1/2,1/2,1/2,1/2,1,0,0,1)`.

### Membership certificates

The four arc sets

`T1={a,d,e,h}`, `T2={b,c,e,h}`, `T3={a,c,f,g}`, `T4={b,d,f,g}`

are arborescences. This can be checked directly by following their parent chains to 0. They give

`z=(chi_T1+chi_T2)/2`, and `w-z=(chi_T3+chi_T4)/2`.

Consequently z belongs to `P intersect (w-P)`.

### Exact vertex certificate

Every point of P satisfies the indegree equations

`x_a+x_b=1`, `x_c+x_d=1`, `x_e+x_f=1`, `x_g+x_h=1`.

The directed triangles 1->2->3->1 and 1->2->4->1 give valid inequalities

`x_a+x_d+x_f <= 2`, and `x_b+x_d+x_h <= 2`.

Every coordinate of P lies between zero and one. On `Q=P intersect (w-P)`, the first triangle inequality applied to w−x yields

`x_a+x_d+x_f >= 1`.

At z, the following eight valid constraints are tight:

`x_e=1`, `x_f=0`, `x_g=0`, `x_h=1`,
`x_a+x_b=1`, `x_c+x_d=1`,
`x_b+x_d+x_h=2`, `x_a+x_d+x_f=1`.

They have a unique solution. The first four fix e,f,g,h. The next equations give `a+b=1`, `c+d=1`, `b+d=1`, and `a+d=1`. Thus `a=b=c=d=1/2`.

If z were a nontrivial convex combination of two points of Q, every active valid inequality and every affine-hull equality above would remain an equality at both points. Uniqueness would force both points to equal z. Hence z is a vertex of Q. It is fractional, so Q is not integer. Since Q is already contained in the integral box [0,1]^8, it is not box-integer.

**Theorem 3.** This five-vertex rooted-arborescence polytope is outside C. By Corollary 2, five is the smallest number of vertices for which such a failure can occur.

There is no ICP failure at the displayed w. For example,

`w = chi_{a,c,e,h} + chi_{b,d,f,g}`.

Both summands are distinct arborescences, hence affinely independent, with coefficients 1,1 totaling 2.

## 5. Why the obstruction example still has ICP

Here is an explicit TU lift certifying ICP for the entire example, not just the displayed w.

Consider three matching slots 1,2,3 for the five nonroot arcs. Allow:

- a and f in slots {1,2};
- b and h in slots {2,3};
- d in slot {2}.

A subset of these five arcs is matchable into the slots if and only if it is an undirected forest in H=K4 minus edge {3,4}. To verify this elementary claim, every subset of size at most two is matchable and acyclic; among triples the only unmatchable sets are {a,d,f} and {b,d,h}, exactly the two triangles. Every other triple is matchable: with d present, choose one arc from each side and assign the slots 1,2,3; without d, at least one side contributes two arcs, which take its two slots, and the other side contributes one arc, which takes the remaining exclusive slot. No set of four arcs is a forest on four vertices, and none is matchable into three slots.

Add three additional slots, one each for root arcs c,e,g, permitting that root arc only in its own slot. Now form the standard matching-flow network:

- source to each of the six slots, capacity 1;
- each slot to each arc-element node it permits, capacity 1;
- each arc-element node j to the head node of the original arc j, capacity 1; this coordinate is x_j;
- each of the four head nodes to the sink, fixed to 1;
- sink to source, fixed to 4.

Its circulation polytope L has a TU incidence system and integral bounds, so L belongs to C. Integral circulations choose exactly one incoming original arc at each nonroot vertex, with a forest among the selected nonroot arcs. These are exactly the arborescences, by the parent-chain argument. Every arborescence admits the slot matching just proved. Thus P is the coordinate projection of L. Gijswijt–Regts's projection theorem gives ICP for P.

Unlike the cactus network, this matching lift is not unique. For example the arborescence {a,c,e,g} has two matching lifts: a can use slot 1 or slot 2, while c,e,g use their dedicated slots. These give distinct feasible circulations with the same original arc vector. The existence of a TU lift therefore does not contradict the failure of P itself to belong to C.

## 6. Remaining gap and relation to earlier work

The original question ranges over arbitrary rooted digraphs. Neither the cactus theorem nor the eight-arc obstruction gives an ICP proof or counterexample for that range. An arbitrary directed-cut formulation cannot simply be inserted into C: Theorem 3 disproves that assumption. A successful lift must be justified; ordinary network-flow feasibility, arborescence packing, or IDP alone does not supply affine independence.

## Sources and credit

1. Dion Gijswijt and Guus Regts, *Polyhedra with the Integer Carathéodory Property*, Journal of Combinatorial Theory, Series B 102 (2012), 62–70, DOI https://doi.org/10.1016/j.jctb.2011.04.004. Definition (3), Theorems 1,5,6,11 and Question 2. Public journal copy: https://www.math.ucdavis.edu/~deloera/TEACHING/READINGSEMINAR/PAPERS/gijswijt%2Bregts.pdf . The projection theorem, sufficient class, TU implication, and known gammoid-intersection result retain their authors' credit.
2. Dion Gijswijt, joint work with Guus Regts, *Polyhedra with the Integer Carathéodory Property*, Oberwolfach Report53/2011, printed pp3025–3027, Question2. https://doi.org/10.4171/owr/2011/53 .
3. Lancini–Pisanu, *A horizon tour of box-total dual integrality*, Computer Science Review61(2026)100928, Open Question8.6, body p38/PDF p40. https://doi.org/10.1016/j.cosrev.2026.100928 . This records the current-source question; it is not proof of global openness or novelty.

The [mathematical audit](MATHEMATICAL_AUDIT.md) accepts the four scoped conclusions after the nonunique-lift witness was corrected to {a,c,e,g}. This proof-and-audit edition is AI-assisted and unrefereed; acceptance is not external human peer review, journal acceptance, or formal proof-assistant certification. The complete symbolic arguments are included. No computational certificate is distributed or required for those arguments.
