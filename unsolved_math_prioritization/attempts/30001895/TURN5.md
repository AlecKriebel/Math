# Author turn 5: degree-eight links and the remaining finite obstruction

2026-10-03 UTC. Problem 30001895, r-element component. Fifth and final
substantive author response. Status: exhausted, full target unresolved.
Subjective completion estimate: 35%. No sixth search response is authorized
by this research budget. Independent verification may assess the frozen
claims but must not become further unfinished proof search.

The hyperplane component remains a credited published negative result.
The r=2 component remains credited prior literature. This turn sharpens
the possible rank-three, τ=4 obstruction; it does not settle all ranks or
all transversal numbers. Every computational deduction below is conditional
on the stated exhaustive encoding and checker correctness, pending audit.

## 1. Excluding degree eight for a critical rank-three obstruction

Suppose H is a finite simple 3-uniform τ-critical family with τ(H)=4 and
ν₃(H)≤5. If v has degree eight, its link G has eight edges and satisfies
the private three-cover condition from turn 4: for each graph edge xy,
G\{xy} has a cover of at most three points avoiding x and y.

As before, Δ(G)≤4. If G has a vertex of degree four, every edge lies on
its closed neighborhood of five vertices. Thus G is K₅ with two edges
removed, which have either a shared endpoint or disjoint endpoints.

For Δ(G)≤3, fix a graph edge uv and a private cover T of size three. An
eight-edge simple graph has at least five vertices, so a smaller cover can
be padded while avoiding u,v. All seven other edges meet T. Hence

    7+|E(G[T])| = sum_(x∈T) degree_G(x) ≤9,

so G[T] has zero, one or two edges. Up to relabeling T these are the empty
graph, one edge, or a two-edge path. The normal forms from turn 4 therefore
extend to three internal cases, with the two endpoint-neighborhood masks
and seven multiplicities of nonempty neighborhoods outside T∪{u,v}.
Each multiplicity is at most three. All other conditions are exactly eight
edges and degree at most three.

The full enumeration contains 2,107 normal forms. The certificate provides
an offending edge for 2,097 of them. Each offending edge has no private
three-cover, checked against every possible cover triple. The remaining
ten forms come with explicit isomorphisms to the six-vertex graph D with
edge list

    01, 02, 03, 12, 13, 24, 45, 35.

This is a diamond (K₄ minus edge 23) whose two degree-two vertices are also
joined by the three-edge path 2–4–5–3. The independent checker reconstructs
every normal form by a Cartesian-product enumeration and checks every
obstruction or isomorphism. Thus the only possible links are the two
K₅-minus-two-edge types and D.

## 2. From private covers to a finite trace problem

Let W be the vertex set of one of these three links. For a graph edge f,
if G\{f} cannot be covered by two points avoiding f, its private
three-cover must consist of three points of W. Otherwise deleting points
outside W would give a cover of size at most two. Enumerate every possible
such three-cover and choose the actual one supplied by H's criticality.
If a two-cover is possible, impose no constraint from that edge.

This omission matters: for K₅ with adjacent missing pairs 01 and 02,
the edge 12 has a two-cover {3,4} after deletion. Its private transversal
in H may use an external point, so silently forcing it into W would be
invalid. The encoding explicitly omits that one constraint.

The resulting private-cover systems are:

- One system for K₅ minus two disjoint edges;
- One system for K₅ minus two adjacent edges, with edge 12 omitted;
- Four systems for D, from two binary choices and six forced covers.

For each system, any edge e∈H not containing v has a trace A=e∩W of size
one, two or three meeting every imposed private cover. All such traces
are enumerated, including traces that might not occur in H. The first
link gives 12 possible traces, the second 13, and each D system 12.

The actual set of distinct traces has no two-point transversal in W.
Otherwise those two points together with v cover H, contradicting τ=4.
Repetitions of a trace do not affect this condition.

For every subfamily of eligible traces without a two-point transversal,
the certificate supplies three distinct traces and three distinct graph
edges of G such that each w∈W belongs to at most three of the six selected
sets. Choose one actual non-v hyperedge for each selected trace, and use
the three v-edges corresponding to the graph edges. These six hyperedges
are distinct and form a 3-packing:

- The vertex v occurs in exactly the three star edges;
- Degrees at vertices of W are checked in the certificate;
- Every vertex outside W∪{v} occurs in at most the three non-v edges.

The last point handles shared external vertices explicitly. No splitting,
generic-position assumption, or private-padding assumption about actual
external vertices is needed for this packing argument.

Thus ν₃(H)≥6, a contradiction. Together with turn 4's degree-nine and
degree-ten exclusions, a rank-three, τ=4 critical obstruction must have
Δ(H)≤7.

## 3. Exact degree-eight certificate

build_degree8_certificate.py constructs the complete normal-form and trace
certificates. verify_degree8_certificate.py separately reconstructs the
full parameter spaces and checks all supplied witnesses. In particular it
recomputes every possible private-cover system, every eligible trace, and
every subset of eligible traces. It requires a valid six-edge packing
witness for every trace family with no two-point cover.

The checked totals are:

    2,107 graph-link normal forms;
    2,097 rejected forms and 10 verified diamond isomorphisms;
    58,992 private-cover triples examined;
    6 private-cover systems;
    28,672 trace subfamilies;
    1,290 explicit six-edge-packing witnesses.

Certificate turn5_degree8_certificate.json has SHA-256

    fe4cf2b16334ebb56453e676247dc34a5082853715092a4eb5eab7693ecd54dc.

The checker rejects an omitted normal form, an omitted packing witness,
and an invalid isomorphism. Reproduction uses ordinary Python with
assertions enabled:

    python3 build_degree8_certificate.py
    python3 verify_degree8_certificate.py

These checks establish the finite computation under its explicit encoding;
they do not replace independent review of the encoding's mathematical
applicability. No floating-point solver is used.

## 4. Counting the remaining (edge count, maximum degree) possibilities

For the still-possible τ=4, ν₃=5 critical family, turn 4 gives at most 19
edges. Write h=|H| and D=Δ(H). We now have 4≤D≤7 and h≥D+3, the latter
because one vertex and one representative from each missed edge give a
cover of size at most 1+h−D. Also h≥7.

Every six-edge subfamily must contain four edges incident with one vertex.
A vertex of degree d witnesses exactly

    F_h(d) = sum_(j=4 to 6) binom(d,j) binom(h−d,6−j)

of the six-element edge-index subsets. Counting witnesses with possible
overlap gives

    binom(h,6) ≤ sum_v F_h(degree(v))
               ≤ 3h · max_(4≤d≤D) F_h(d)/d.        (10)

The second inequality uses exactly 3h total incidences and ignores
low-degree vertices, which witness no such subsets. The right side is an
upper bound, so overlaps cannot invalidate the exclusion.

count_tau4_pairs.py evaluates (10) with exact rational arithmetic for every
remaining h≤19 and D≤7; no numerical rounding is used. The surviving pairs
are precisely

    D=4: h=7,8;
    D=5: h=8,9,10,11;
    D=6: h=9,10,11,12,13,14;
    D=7: h=10,11,12,13,14,15,16,17.

This leaves twenty parameter pairs. The complete arithmetic table is
turn5_counting_bounds.json. Survival is only a necessary condition.

## 5. A bounded exact attempt on those twenty cases

The turn-3 incidence encoding extends with targets of six edge indices.
Retain only support sets of size at least four. Each row still has capacity
three, and two saturated identical rows remain forbidden by simplicity.
The transversal-four hypothesis additionally forces:

    |A| ≤ h−3 for one support;
    |A∪B| ≤ h−2 for two supports;
    A∪B∪C ≠ [h] for three supports.

These conditions follow because the selected one, two or three vertices
could otherwise be supplemented by one representative from each uncovered
edge to make a three-point cover. Their violations persist under adding
further supports. Every six-index target must intersect some support in
at least four indices. As in turn 3, a maximum support can be relabeled
to {0,…,D−1}, and every other high support has size at most D.

critical_tau4_search.cpp searches this finite necessary system. The declared
per-case limits were 25,000 visited nodes and 45 seconds. A result with
`aborted: true` is unresolved even if its companion `satisfiable` field is
false; that field then means only that no witness was returned before the
limit. No aborted tree is included as an impossibility certificate.

An initial adaptation mistakenly retained arrays sized for ten edge indices.
Impossible counters exposed the error on larger inputs. All pilot results
were discarded. The arrays were corrected to seventeen rows, all twenty
cases were rerun in a fresh output directory, and only the corrected runs
are represented in turn5_tau4_search_results.json. A bounded address/undefined
behavior sanitizer probe then ran without a diagnostic; leak detection was
disabled because it is unsupported under the execution environment's ptrace.
The independent tree checker is the proof check, rather than this diagnostic.

Nine cases finished with complete impossibility trees:

    (h,D)=(7,4),(8,4),(8,5),(9,5),(10,5),
          (9,6),(10,6),(10,7),(11,7).

Their saved certificate contains 6,521 nodes. verify_tau4_certificate.py
reconstructs every candidate and checks every branch and impossibility leaf,
as in turn 3, with the additional pair- and triple-union conditions. It
explicitly reports that the parameter domain is incomplete and returns the
unresolved pairs. Its output is turn5_tau4_certificate_verification.json.
The complete certificate is turn5_tau4_partial_certificate.json.gz.

The eleven unresolved pairs are

    (11,5);
    (11,6),(12,6),(13,6),(14,6);
    (12,7),(13,7),(14,7),(15,7),(16,7),(17,7).

The node/time limits provide no mathematical conclusion about these cases
and do not establish computational infeasibility. They are simply where
this budgeted attempt stopped. A separate exploratory check of the degree-
seven link K₄ disjoint union K₂ was not promoted to an additional theorem.

## 6. Final scope and stop

The strongest candidate partial results are consolidated in FINAL_REPORT.md.
The full r-element question remains unresolved: the eleven rank-three,
τ=4 cases above are still possible, larger transversal numbers remain,
and general r≥4 is unresolved. The already-refuted hyperplane assertion
does not settle this separate requested component.

Five substantive author responses have now been used. No complete proof or
counterexample for the entire r-element component has been produced, and
the full imported record must not be marked solved. Freeze these artifacts
for a fresh, uninvolved mathematical and computational applicability audit.
