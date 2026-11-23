Editorial note: This preserves the complete authored text, with only operational artifact references, undistributed identities and byte counts, locations, and executable command descriptions edited for this prose edition. Mathematical proofs, full audit findings, counts, and limitations remain complete. The final structural theorem is independent of a finite computer bound. Earlier through-nine and through-ten results retain their historical scope in unchanged companion editions. Historical candidate conditions are reconciled in ACCEPTANCE_AND_DEPENDENCIES.md. Executable programs and raw enumeration outputs are not distributed.

# Final structural pass: the fully color-twisted minimal case is impossible

12 October 2026 UTC. Queue row 1754 / problem 3276 / OPG-1808. Fifth and final substantive structural pass in this program; no claim about a lifetime total.

## Status and exact scope

The unrestricted target remains unresolved here: a nonempty finite tournament with at most three arc colors should contain a directed cyclic rainbow triangle or an outgoing vertex reaching every other vertex by a monochromatic directed path, with color allowed to depend on the destination.

**Result. Every induced-minimal counterexample to this target has an intransitive group of direction-preserving automorphisms that are allowed to apply one global permutation of the colors.** This eliminates the fully color-permuting-transitive minimal-counterexample class left at odd orders divisible by nine in the previous structural packet, at every order. It does not say that every color-permuting-transitive tournament satisfies the target: an induced-minimal counterexample inside such a tournament need not inherit its symmetries. It does not eliminate arbitrary strict three-periodic obstruction cycles, and proves no new unrestricted finite-order bound.

The proof uses Shen Minggang's failed-predecessor lemma, credited and reproved in Lemma 2.1 of Georgakopoulos and Spruessel, *On 3-coloured tournaments*, arXiv:0904.1967v2. The circulation and small-palette lemma used below is proved again for completeness. No finite search, incidence theorem, module theorem, or divisibility-by-nine argument is needed for the new all-order exclusion. There is no novelty, priority, exhaustive literature-review, or present-day open-status claim.

Reachability within a specified color includes a length-zero path. For distinct endpoints, any monochromatic walk contains a monochromatic simple path after closed portions are removed. All concatenations and their ensuing contradictions below are therefore valid even if intermediate walks repeat vertices. Paths used to reach a different vertex have positive length. Indices on the obstruction cycle are modulo its order; class indices and color labels are modulo three.

## 1. A self-contained internal-fiber lemma

**Lemma 1 (color-preserving transitivity).** A nonempty finite tournament admitting a vertex-transitive group of exact-color-preserving automorphisms has a spanning strongly connected monochromatic color if at most three colors are allowed. For order greater than one, its order is odd. No regular or free group action is assumed.

**Proof.** For each color c, transitivity makes every c-outdegree equal to some d_c^+ and every c-indegree equal to d_c^-. Counting c-arcs by tails and heads gives d_c^+=d_c^-. In a finite balanced digraph every actual arc u->v lies on a directed cycle: the set R reachable from v has no exiting arc; if u is outside R the arc u->v enters R, making the sum of outdegree minus indegree on R strictly negative, whereas balance makes it zero. Thus v reaches u in the arc's color.

For each color c, automorphisms permute its strongly connected components (SCCs). Vertex transitivity makes all c-components equally large, so their number divides the tournament order m. The uncolored outdegree is (m-1)/2, so m>1 is odd. If a color does not span, its number of components is a divisor of odd m greater than one, hence at least three; its component E_c(x) through any fixed x has size at most m/3. Every vertex y lies in some E_c(x), because the actual arc between x and y is reversible in its color. With three allowed colors the E_c(x) all contain x, and therefore, if none spans,

    m = |union_c E_c(x)| <= sum_c |E_c(x)| - 2 <= m - 2,

a contradiction. Keeping unused colors as singleton components is harmless. For m=1 every color is spanning-strong under the reflexive convention. QED.

This is the same elementary small-palette mechanism as the accepted fourth-pass result. It proves a spanning strongly connected monochromatic subdigraph, not a monochromatic Hamilton cycle. The conclusion need not hold with four colors; a nine-vertex affine four-color counterfixture is retained in the tests.

## 2. The three-fiber rigidity argument

Let n=3m with m>=2. Label a tournament T by Z/nZ and write pred(x)=x-1. Assume:

1. Each vertex x reaches every vertex other than pred(x) by some monochromatic directed path, and reaches pred(x) in no color.
2. The shift h:x->x+3 preserves the direction and the exact color of every actual arc.
3. The residue classes V_r={x:x=r modulo 3}, r=0,1,2, have spanning strongly connected monochromatic colors c_r, respectively, and the three selected colors c_0,c_1,c_2 are distinct. The spanning paths in this hypothesis are internal to the corresponding induced class.

No uniqueness of the choice c_r is assumed. Neither minimality nor absence of cyclic rainbow triangles is assumed in this section. The shift h is transitive on each class; it is not transitive on the whole tournament.

**Proposition 2 (offmatching backward arcs).** Under these three assumptions, for every r, every x in V_r, and every y in V_{r-1} other than pred(x), the actual arc is

    x -> y in color c_{r+1}.

Consequently the triple 0,2,4 is a directed cyclic rainbow triangle.

**Proof.** Fix r and abbreviate A=V_r, B=V_{r-1}, C=V_{r+1}, and a=c_r, b=c_{r-1}, c=c_{r+1}. These are all three different colors.

First, no a-path goes from any x in A to any y in B. Otherwise, for any target y' in B choose a power h^t with h^t(y)=y'. Applying this exact-color-preserving automorphism to the purported path gives an a-path from h^t(x) in A to y'. The spanning a-strong subgraph on A supplies an internal a-path from the original x to h^t(x). Concatenation gives x an a-path to every y' in B, in particular pred(x), which is forbidden. The internal prepath may have length zero; the conclusion still has distinct endpoints.

Second, no b-path goes from x in A to any y in B, because the spanning b-strong subgraph on B would extend it to pred(x). Again, a zero-length extension when y=pred(x) causes no exception.

For every offmatching pair x in A, y in B with y!=pred(x), assumption 1 supplies a monochromatic path. The preceding exclusions force its color to be c. Hence

    x reaches y in color c whenever x in A, y in B, y!=pred(x).   (*)

There is no c-path between distinct vertices u,v of A, in either ordered direction. Indeed, if u reaches v in c, then pred(u)!=pred(v) by injectivity of pred, so (*) gives a c-path from v to pred(u). Concatenation would make u reach pred(u).

There is likewise no c-path between distinct vertices u,v of B. Put x=succ(v)=v+1, so x belongs to A and pred(x)=v. Since u!=v, (*) gives x a c-path to u. Any c-path u->v would then make x reach pred(x). This handles the other endpoint class without reversing any directed path.

Now take a simple c-path P from an offmatching x in A to y in B. It cannot visit C. If it did, let z in C be a vertex of P. For any y' in B choose h^t(y)=y'. Apply h^t to the suffix of P from z to y; this gives a c-path from h^t(z) in C to y'. The spanning c-strong subgraph on C connects z to h^t(z). Prepend the prefix from x to z. The resulting c-walk gives x reachability to every y' in B, including pred(x), a contradiction. This argument uses the exact-color symmetry of the suffix and the internal strong component on C, not a claim that a virtual reachability edge is an actual interval arc.

Thus every vertex of P is in A or B. If an intermediate vertex belongs to A, the prefix gives a c-path from x to a distinct vertex of A. If an intermediate vertex belongs to B, the suffix gives a c-path from that vertex to the distinct endpoint y in B. Both are impossible by the preceding two paragraphs. P has no intermediate vertex, so x->y is an actual c-arc, as claimed.

Finally, for n>=6 the three different vertices 0,2,4 have classes 0,2,1. None of the pairs 0->2, 2->4, 4->0 is its tail's predecessor pair: pred(0)=n-1 is not 2, pred(2)=1 is not 4, and pred(4)=3 is not 0. Applying the assertion at r=0,2,1 gives

    0 -> 2 in c_1,   2 -> 4 in c_0,   4 -> 0 in c_2.

This is an actual directed cycle and its colors are distinct. QED.

**Corollary 2.1 (internal rigidity).** Under the same assumptions, every actual arc inside V_r has color c_r.

**Proof.** The no-within-endpoint-class arguments above forbid c_{r+1}-reachability between distinct members of V_r. Applying the same arguments with A=V_{r+1}, B=V_r forbids c_{r-1}-reachability between distinct members of V_r. An actual arc is a path of its color, so only c_r remains. QED.

This corollary is not required for the triangle contradiction. The proof uses an automorphism that moves a terminal target while preserving color; mere strong connectivity does not provide that step. Equal-size blocks are not colored modules, and no uniform interclass directions or colors were assumed.

## 3. Excluding the fully symmetric induced-minimal case

**Theorem 3.** Let D be an induced-minimal counterexample to the stated source-or-cyclic-rainbow alternative with at most three colors. The group G of all permutations of vertices preserving direction and inducing one global permutation of the used colors is not vertex-transitive.

**Proof.** By Shen's lemma, as reproved in the cited Lemma 2.1, D has a distinguished directed Hamilton cycle C on which every vertex reaches all vertices except its predecessor. This cycle is unique with this failed-predecessor property; uniqueness among arbitrary Hamilton cycles is neither asserted nor needed. A singleton cannot be a counterexample, and neither can a two-vertex tournament, whose arc tail is a source. Thus n>=3.

Every g in G preserves monochromatic reachability and its failure. It therefore commutes with pred: g(pred(x))=pred(g(x)). A permutation commuting with one full n-cycle is a rotation of that cycle: its image at one vertex determines its image at all successive predecessors. Consequently G embeds in the cyclic rotation group C_n. The image on used colors is a genuine homomorphism, since the image color of any actual arc of a given used color determines that color's image. Unused labels can be filled in arbitrarily and have no effect on this argument.

Suppose G is transitive. A subgroup of C_n has each vertex orbit of size its group order, so transitivity makes G the whole C_n. In particular the one-step shift g:x->x+1 is a direction-preserving automorphism with a global color permutation sigma. Its underlying order is n. If n were even, g^(n/2) would swap a pair of vertices, reversing that pair's arc, which is impossible. Hence n is odd.

The order of sigma on used colors divides n and is odd. With at most three colors sigma is either identity or a three-cycle. If identity, the successive actual arcs of C all have one color; following C would let every vertex reach its predecessor, a contradiction. Thus sigma is a three-cycle, all three colors occur, and 3 divides n. Relabel colors so sigma(c)=c+1 modulo 3. Write n=3m; m is odd.

If m=1, the actual cycle C has three arcs whose colors are successive images under sigma, and is already a cyclic rainbow triangle. Otherwise m>=3. The kernel shift h=g^3 preserves exact colors and has the three residue classes V_0,V_1,V_2 as its orbits. It is transitive on each class, so Lemma 1 applied to the induced tournament D[V_0] supplies some spanning strong color c_0. Applying g and g^2 to its paths supplies spanning strong colors c_1=sigma(c_0) and c_2=sigma^2(c_0) within V_1 and V_2. These selected colors are distinct. This choice does not require proving in advance that a class has a unique spanning color.

All hypotheses of Proposition 2 now hold. That proposition supplies an actual cyclic rainbow triangle, contradicting the counterexample assumption. G is therefore intransitive. QED.

**Corollary 3.1 (automorphism boundary).** The group G of a hypothetical induced-minimal counterexample is cyclic of odd order and is a proper subgroup of C_n. If p is the least prime divisor of n, G has at least p vertex orbits. If n is prime, G is trivial.

**Proof.** The rotation argument works without transitivity. Any element of even order would have an involutive power swapping some vertex pair and reversing its arc, so G has odd order. The theorem says |G| is a proper divisor of n. Its number of equally sized free rotation orbits is n/|G|, a divisor of n greater than one, hence at least p. For prime n the only proper subgroup of C_n is trivial. QED.

This corollary concerns even those automorphisms that permute colors globally. It does not assert that an arbitrary induced subtournament inherits a symmetry of a larger tournament. It does not show that a three-periodic cycle word gives a color-twisted automorphism of all chords. The strict-periodic source problem remains outside this proof.

## 4. Nonvacuous rigid examples and sharp hypothesis boundaries

For every odd m>=1 let n=3m. The following tournament F_m has the exact failed-predecessor property and the full color-twisted shift symmetry, but contains a cyclic rainbow triangle and has no source. It shows the structural premises used before rainbow exclusion are nonvacuous.

Inside each residue class V_r, orient a circulant tournament on its m vertices by positive class-coordinate offsets 1 through (m-1)/2, and give all internal arcs color r. For cross pairs, specify each pair exactly once by taking x in V_r and y in V_{r-1}. If y=pred(x), orient y->x in color r-1; otherwise orient x->y in color r+1. The matching exceptions are exactly the Hamilton cycle arcs x->x+1 of color x modulo three. Translation by one vertex preserves orientation and rotates colors by one; the wrap from V_2 to V_0 translates both internal coordinates by one and preserves their circulant orientation.

For any fixed color c, its complete arc graph consists of the internal strong circulant on V_c, the forward matching arcs V_c->V_{c+1}, and the offmatching arcs V_{c+2}->V_{c+1}. There are no other c-arcs. Hence a vertex x in V_r reaches all of V_r and V_{r+1} in color r, and all of V_{r-1} except pred(x) directly in color r+1. In color r-1 it has no outgoing arc. None of these color graphs permits x to reach pred(x). This proves the exact failed-predecessor property. For m=1 it is the rainbow three-cycle. For m>=3, Proposition 2's triangle 0,2,4 is rainbow. These are not counterexamples to the target, because they satisfy its rainbow alternative.

A separate nine-vertex twisted-shift-invariant fixture is cyclic-rainbow-free and has every vertex as an outgoing source, yet no single color spans. It prevents claiming that color-permuting transitivity inherits the previous exact-color spanning theorem. A changed noncycle chord in a rigid fixture preserves the strict period-three cycle word but destroys the asserted global shift symmetry; that fixture prevents replacing an actual automorphism check with a cycle-word check. The tests also include the four-color affine obstruction to an unrestricted palette extension, reversed reachability checks, malformed matrices and palettes, and incorrect claimed strong colors.

## 5. Computation, verification, and remaining scope

The proof is all-order and independent of finite computation. The implementation checks its hypotheses explicitly and returns the actual rainbow witness; it does not diagnose induced minimality or discover arbitrary automorphism groups. Canonical code uses the fixed global color cycle c->c+1 and the displayed cycle order; a general three-cycle can be relabeled to this form for the theorem.

The packet tests enumerate every one of the 1,296 canonical color-twisted circulant encodings on nine vertices, with no cyclic-rainbow or failed-predecessor prefilter hidden in the generation. Exact BFS reachability is cross-checked against a separate Floyd-Warshall closure. Twelve encodings satisfy the exact failed-predecessor property in that fixed cycle order; all satisfy the forced-arc conclusion and have a cyclic rainbow triangle. The 432 cyclic-rainbow-free encodings all have every vertex as a source. This is a small implementation/fixture check, not a new unrestricted finite theorem. The independently maintained orbit-search lane is not incorporated as a premise.

Fixed rigid family members, positive relaxations, explicit false-extension fixtures, and failure gates are included with exact counts in STRUCTURAL_VERIFICATION.md and optimization-mode receipts. All failures use explicit exceptions, not removable Python assertions. Verification under normal Python, -O and -OO must agree apart from recorded optimization metadata. Frozen-byte integrity verification, including explicit corruption rejection, is separate from the mathematical proof and independent audit.

General asymmetric colored-prime tournaments with large incidence cores remain outside these results. The accepted unrestricted theorem through order ten and the incomplete period-twelve search remain exactly as before. No sixth structural pass, remote repository write, queue change, or publication action occurs in this task.
