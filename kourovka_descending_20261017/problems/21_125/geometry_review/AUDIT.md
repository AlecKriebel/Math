# Independent adversarial audit of the canonical Hydra cover calculations

**Outcome: PASS for the stated partial results and bounded calculations.** No full solution of Kourovka 21.125(b), originality determination, abstract nonembedding theorem, or publication approval follows. This is an independent AI audit; it is not human peer review or a formal proof assistant check.

The exact seven audited inputs and their byte hashes are in `INPUT_MANIFEST.json`. The author files were read without modification. Review completion: **100% of this narrow audit**; completion of the original research objective is not asserted.

## Claims and primary-source checks

Dison–Riley's published *Hydra groups*, printed page 511, gives exactly

\[
G_m=\langle s,\alpha_1,\ldots,\alpha_m\mid
\alpha_1^{-1}s\alpha_1=s,\quad
\alpha_i^{-1}s\alpha_i=\alpha_{i-1}\ (i>1)\rangle
\]

and states that its universal square presentation complex is CAT(0). I checked the cached published text and the publisher/author primary sources, not a different Hydra analogue. [Published article](https://ems.press/journals/cmh/articles/12184), [publisher PDF](https://ems.press/content/serial-article-files/43323?nt=1).

I independently fetched the corrected Haglund–Wise author manuscript and checked Theorem 1.1 and Definitions 3.1–3.2. Its A-special criterion requires embedded two-sided hyperplanes, no direct self-osculation, and no inter-osculation; indirect self-osculation is allowed. Definition 3.2's original unqualified “special” omits the two-sided condition, so it is not literally the same definition as A-special. Every hyperplane here is two-sided, making that distinction immaterial for these finite covers. Theorem 4.2 supplies the local-isometry characterization. The quoted criterion in the author's note is therefore accurate. [Corrected primary manuscript](https://www.imo.universite-paris-saclay.fr/~frederic.haglund/special%28corrected%29.pdf).

The source byte hashes, locators, and access time are in `SOURCE_MANIFEST.json`; raw source files are cached solely for checking.

## Independent derivation of incidence and orientations

Use a right action. The relator is equivalent to

\[
s\alpha_i=\alpha_i\alpha_{i-1},\qquad \alpha_0=s.
\]

The square starting at a cover vertex \(v\) has vertices

\[
v,\quad vS,\quad vSA_i=vA_iA_{i-1},\quad vA_i.
\]

Its opposite geometric edges are precisely

\[
(\alpha_i,v)\sim(\alpha_i,vS),\qquad
(s,v)\sim(\alpha_{i-1},vA_i).
\]

In both pairs their positive orientations agree across the square. Consequently all elementary parallelisms preserve the displayed positive transverse orientation. No chain of parallelisms can reverse it, proving two-sidedness, including for self-intersecting immersed hyperplanes.

Hyperplanes are exactly the connected components of this edge parallelism graph. A square is a self-intersection exactly when its two consecutive edge classes agree. This proves the author's DSU test mathematically; my checker does not reuse that DSU or either formula as its implementation. It walks the entire four-edge boundary of each square, records the actual geometric edge occurrences, and connects the opposite occurrences. Its connected components are computed by explicit graph traversal.

At the base complex, these identifications connect the labels \(s,\alpha_1,\ldots,\alpha_{m-1}\), while \(\alpha_m\) remains alone. There are exactly the claimed two immersed hyperplanes for \(m\ge2\). The last square always crosses distinct base hyperplanes. Lifts of distinct base hyperplanes cannot merge, so its lifts can never be self-intersections. All other square levels may self-intersect.

The source's nonpositive curvature assertion is also compatible with the explicit link. There are no repeated corner pairs. In a potential triangle, choose the largest generator index appearing. Its positive germ has only the two \(s\)-germs as lower-index neighbors; its negative germ has only the two previous-generator germs as lower-index neighbors (the previous generator is \(s\) for index 1). Those two neighbors are not adjacent to one another, ruling out the triangle. Thus the square complex's link is flag.

## Hyperplane subgroup and the regular-cover criterion

The immersed hyperplane \(H\) has one vertex for the midpoint of \(s\) and one for each \(\alpha_j\), \(1\le j<m\). Its non-loop midsegments from square levels 2 through \(m\) form a spanning tree. The remaining midsegments comprise a loop at the \(s\)-midpoint from square 1 and a loop at each \(\alpha_j\)-midpoint from square \(j\). There are exactly \(m\) independent graph loops.

Lift the \(s\)-midpoint at the identity to fix the base lift. The first loop translates it by \(\alpha_1\). The tree arc through square \(i\) transports it to the \(\alpha_{i-1}\)-edge based at \(\alpha_i\). The loop there transports that edge's start by right multiplication by \(s\). Returning through the tree then ends at the \(s\)-edge based at \(\alpha_i s\alpha_i^{-1}\). Hence the image of the hyperplane fundamental group, or equivalently the stabilizer of the base lift, is

\[
L_m=\langle\alpha_1,\ \alpha_i s\alpha_i^{-1}\ (2\le i\le m)\rangle.
\]

There is no hidden use of injectivity of a finite quotient in this computation. A hyperplane lift's edge component records the same stabilizer via loops in the immersed hyperplane.

For \(i<m\), square \(i+1\) transports the \(s\)-edge based at \(\alpha_{i+1}^{-1}\) to the \(\alpha_i\)-edge based at the identity. The two branches of square \(i\) at the identity therefore lie in the same lifted hyperplane exactly when \(\alpha_{i+1}\) belongs to its stabilizer. In the regular finite quotient cover this becomes

\[
q(\alpha_{i+1})\in q(L_m).
\]

Regular deck transformations act transitively on the square lifts, so checking one starting vertex per level suffices. This proves both directions of the stated no-self-intersection criterion for **regular** quotient covers. It was not asserted for arbitrary nonregular covers, and my acceptance does not extend it to them.

The involution filter is valid: if \(q(\alpha_i)^2=1\), then the generator \(q(\alpha_i s\alpha_i^{-1})\) of \(q(L_m)\) equals \(q(\alpha_i^{-1}s\alpha_i)=q(\alpha_{i-1})\). For \(i\ge3\), the criterion forces square level \(i-2\) to self-intersect.

## Abelian monodromy and boundary cases

In an abelian action image the relation gives \(A_{i-1}=S\) for every \(i\ge2\). For \(m\ge3\), both \(A_1=S\) and \(A_2=S\) follow. Square 2 identifies \((s,v)\) with \((\alpha_1,vS)\); square 1 identifies the latter with \((\alpha_1,v)\). These are the two crossing branches of square 1. The proof works for infinite actions too, uses no regularity assumption, and excludes every abelian-monodromy cover of this particular complex from being A-special.

The threshold matters. For \(m=2\), \(A_2=S\) need not hold. The degree-two action with \(S\) trivial and \(A_2\) a transposition gives a countercheck against extending the lemma to rank 2. The bounded and wreath experiments also exhibit known rank-two positive behavior. No statement about a different cubulation of the abstract Hydra group is warranted by this geometric obstruction.

## Bounded census completeness and reproduction

The permutations \(S\) and \(A_m\) determine all lower \(A_i\) recursively; the remaining relation is exactly commutation of \(S\) with \(A_1\). Simultaneous conjugation can put any \(S\) into the chosen representative of its cycle type. Enumerating all \(A_m\in\mathrm{Sym}(n)\) then includes every action up to simultaneous conjugacy. The orbit test checks connectedness. This is an exhaustive redundant enumeration, **not a count of isomorphism classes**.

I independently reproduced all 34 stored census rows: ranks 2–6 through degree 6, and ranks 3 and 5 in degrees 7 and 8. The independent code examined **1,969,795 pairs**, retaining **136,958 connected actions** across those rows. All counts, minima of self-crossing squares, every stored level-clean count and level minimum, and all supplied level witnesses match. In particular there is no connected crossing-free rank-3 or rank-5 canonical cover of degree at most 8. This says nothing about degree 9 or higher, other cubulations, or abstract group embeddings.

Reproduction command from the repository root:

```text
python3 kourovka_descending_20261017/problems/21_125/geometry_review/independent_incidence_check.py
```

The independent checker imports only the Python standard library, never the author's modules. `INDEPENDENT_RESULTS.json` records the exact reproduced results. Runtime on this audit host was about 16 seconds.

## Wreath example and full specialness check

My wreath action uses coordinate changes, with group elements encoded as a base vector and a rotation. Right multiplication by \(S\) increments the base coordinate at the current rotation; right multiplication by \(T\) increments the rotation. This differs from the author's explicit multiplication implementation but yields the same regular action.

For \(C_2\wr C_3\), the three coordinate involutions are distinct. With \(\alpha_3=T\), the elements \(S\), \(T^{-1}ST\), and \(TST^{-1}\) occupy the three different coordinates. The first two lower \(\alpha\)-relations follow from commutation of base coordinates. The computed subgroup

\[
q(L_3)=\langle S,TST^{-1}\rangle
\]

misses both \(q(\alpha_2)=T^{-1}ST\) and \(q(\alpha_3)=T\). Thus the 24-sheeted regular cover really has no self-intersections.

To challenge the stronger specialness claim, my code constructs each vertex link from actual oriented edge occurrences at square corners. It then inspects all pairs of germs, distinguishing equal transverse orientations from opposite ones. Finally it tests whether the two hyperplanes of each non-corner germ pair cross in any other square. This independently recovers the full defect counts, rather than inferring specialness from the regular subgroup filter.

For the rank-3 24-sheeted example the exact counts are:

| Defect | Count |
|---|---:|
| Self-intersecting squares | 0 |
| Direct self-osculating germ pairs | 0 |
| Indirect self-osculating germ pairs | 72 |
| Inter-osculating germ pairs | 96 |

The 96 inter-osculating germ pairs disqualify this cover. The rank-2 action is A-special. All 12 supplied wreath rows, including degrees 64 and 81 and ranks 2–5, match independently. The regular hyperplane subgroup membership criterion was also checked independently against incidence in every wreath row. The higher-rank shallow construction regains self-intersections, exactly as reported.

## Adversarial outcome and exact remaining gap

I actively tested opposite action conventions, basepoint conjugation in the stabilizer, the distinction between regular and nonregular covers, loops with two germs, direct versus indirect osculation, the rank-2 boundary, and the temptation to extrapolate a finite negative search. None produces a substantive objection to the frozen inputs. The original HW vocabulary is distinguished above; it does not change these two-sided examples.

The accepted positive output is a self-intersection-free finite rank-3 canonical cover that still fails inter-osculation, together with a known rank-2 positive case. The accepted negative output is the abelian-monodromy canonical-cover obstruction and a bounded census. Neither settles virtual specialness for \(m\ge5\). That requires a finite special cover, another special model, or a rigorous virtual RAAG embedding; alternatively a genuine group obstruction would have to persist over every finite-index subgroup and every allowable special model. **No such complete argument is supplied or approved here.**
