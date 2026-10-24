# Canonical Hydra cube covers: exact obstructions and a small-rank experiment

**Status: verified by author calculations; independent adversarial review pending.** This is a method-level partial investigation, not a resolution of Kourovka21.125(b). No originality claim is made for the elementary lemmas or small-rank results.

## 1. Exact cubulation and the unresolved target

For the ordinary Hydra group G_m, Dison–Riley, *Hydra groups*, CMH88(2013), printed p.511, gives the compact nonpositively curved square complex X_m with one vertex, oriented edges s,alpha_1,...,alpha_m, and square relations

    alpha_1^-1 s alpha_1 = s,
    alpha_i^-1 s alpha_i = alpha_(i-1)  (2<=i<=m).

This presentation is isomorphic to the original Hydra group. Its CAT(0) universal cover is established prior work. We study finite covers of this particular cubulation. Virtual specialness of the abstract group allows other, even noncompact, special cubulations, so failure of a cover construction here cannot disprove the Notebook assertion.

The base complex has two immersed hyperplanes for m>=2: H containing the edges s,alpha_1,...,alpha_(m-1), and K containing alpha_m. At each square i<m the two crossing branches belong to H, while the last square crosses H and K. Every square identifies opposite positive edge orientations, so both hyperplanes, and all their lifts to covers, are two-sided.

## 2. Exact edge-equivalence computation

A finite cover can be encoded by permutations S,A_1,...,A_m of its vertices, acting on the right, satisfying A_i^-1 S A_i=A_(i-1), with A_0=S. Write (x,v) for the oriented positive x-edge with initial vertex v. The square based at v with boundary s alpha_i alpha_(i-1)^-1 alpha_i^-1 gives precisely these elementary parallelisms:

    (alpha_i,v) ~ (alpha_i,v S),
    (s,v) ~ (alpha_(i-1),v A_i).

For i=1 the second formula reads (s,v)~(s,v A_1). Connected components of this finite edge-equivalence graph are exactly the immersed hyperplanes of the cover. A square i based at v self-intersects if and only if the classes of (s,v) and (alpha_i,v) coincide. The code checks the defining permutation relations first and uses only these exact opposite-edge identifications.

## 3. No abelian cover cleans the canonical complex in rank at least three

**Lemma.** If m>=3 and a cover of X_m has abelian monodromy, then every lift of square1 is a hyperplane self-intersection. The cover need not be finite for this assertion.

**Proof.** Commutativity of the monodromy and the relations imply A_1=S and A_2=S (since 2<m). For every vertex v, square2 identifies (s,v) with (alpha_1,v A_2)=(alpha_1,v S). Square1 identifies (alpha_1,v S) with (alpha_1,v). Thus the two branches crossing in square1 based at v lie in the same hyperplane. This is forbidden in a special cube complex. QED.

This excludes covers obtained from finite abelian quotients and all transitive finite actions with abelian image. It does not exclude nonabelian finite covers, different cube complexes, or virtual specialness of G_m.

## 4. Hyperplane subgroup and regular-cover filter

Choose the midpoint of the positive s-edge as basepoint of H. The graph H has the s-vertex and the alpha_j-vertices (j<m), with the square-i arcs joining the s-vertex to the alpha_(i-1)-vertex for i>=2. These m-1 arcs form a spanning tree. The remaining m loops give the stabilizer

    L_m = < alpha_1, alpha_i s alpha_i^-1 (2<=i<=m) >.

Indeed square1 contributes the alpha_1 loop at the s-midpoint. Transport across square i to the alpha_(i-1)-midpoint, around its loop dual to square i-1, and back ends at the s-edge translated by alpha_i s alpha_i^-1. The spanning-tree loop calculation gives all generators. This is a subgroup of the original group, not a quotient assertion.

For i<m, the branch dual to the alpha_i edge at the identity belongs to alpha_(i+1)^-1 H. Consequently a **regular** cover induced by a quotient q:G_m->Q has no hyperplane self-intersections if and only if

    q(alpha_j) not in q(L_m) for each 2<=j<=m.

Square m has branches from the distinct base hyperplanes H,K and cannot be a self-intersection. This criterion concerns self-intersection only; direct self-osculation and inter-osculation require additional checks. Membership in L_m is not inferred from finite images.

A useful immediate filter: if q(alpha_i)^2=1 for some i>=3, then

    q(alpha_i s alpha_i^-1)=q(alpha_(i-1)) belongs to q(L_m),

so square i-2 self-intersects. Thus elementary involution quotients cannot clean these canonical cubulations in rank>=3. This is not an obstruction to abstract embeddings in right-angled Coxeter groups.

## 5. A finite wreath-product countercheck against overinterpreting small searches

Let Q=(C_2)^3 semidirect C_3, where T rotates the three base factors. Let S be the involution in one base factor. Use the right regular action of Q on its24elements. For rank3, set alpha_3=T, alpha_2=T^-1 S T and alpha_1=S. The relations hold because base factors commute. Here

    q(L_3)=<S,T S T^-1>,

which misses both alpha_2 (the third base factor) and T. Thus this24-sheeted regular cover has **no hyperplane self-intersections**. In contrast, every connected permutation cover of degree<=8 enumerated below retains a self-intersection. The bounded negative result does not extend even to degree24, let alone to the abstract group.

The full exact incidence checker finds that this cover has **96 inter-osculating germ pairs**, and hence is **not special**. It has no direct self-osculations. With the same wreath action at rank2, the full checker finds an A-special24-sheeted cover, reproducing only known small-rank virtual specialness. With m>=4 this shallow wreath construction collapses alpha_1,...,alpha_(m-2) to S, so the first self-intersections return.

The other regular examples C_2 wr C_4 (degree64) and C_3 wr C_3 (degree81) show the same rank3 pattern: self-intersections disappear, but inter-osculation remains. Their exact finite outputs are in wreath_cover_results.json. The checker uses the corrected Haglund–Wise *Special cube complexes*, Theorem1.1: embedded, two-sided hyperplanes, no **direct** self-osculation, and no inter-osculation. Indirect self-osculation is reported separately and allowed by that criterion.

## 6. Reproducibility and exact bounded scope

Run with Python3 standard library:

    python3 cover_search.py
    python3 wreath_cover.py

`cover_search.py` exhausts ranks2..6, cover degrees1..6. It fixes one S permutation of each cycle type and exhausts all top permutations T, derives lower A_i recursively, checks the last commuting relation, and retains connected actions. Every transitive action is conjugate to one examined, though equivalent actions can occur repeatedly. Therefore the counts are counts of representatives examined, **not** counts of isomorphism classes of covers. Extended results for ranks3/5 in degrees7/8 were computed with the same exported search function and are preserved in cover_search_extended.json. Those pairs number75600 for degree7 and887040 for degree8 per rank.

All rank3/5 connected actions examined through degree8 have a self-intersection; no conclusion about higher degrees or all cubulations follows. Results level_crossing_results.json separately count crossings by square level. The complete direct/inter-osculation checker inspects all square corners, all germs at all vertices, and all pairs of hyperplanes that cross anywhere in the cover; it does not infer specialness merely from absence of self-crossings.

## 7. Remaining mathematical gap

An affirmative solution needs a finite special cover, a different special model, or another rigorous virtual-specialness construction for every m>=5. No such construction is obtained here. The canonical-cover route requires separation of the explicit hyperplane subgroup and the relevant hyperplane double cosets in finite quotients; residual finiteness alone does not give that separation. The displayed wreath example makes the difference concrete: removing all self-intersections still leaves inter-osculation.
