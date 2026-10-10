# Independent deep audit: perfect-cone Prym indeterminacy

## Verdict and frozen object

**PASS, strictly scoped to the retained results and the honest unsolved status.** I found no substantive gap in the restricted all-components-invariant theorem, including branchwise-fixed nodes. Its geometric conclusion depends on the correctly matched published perfect-cone criterion and the exact Friedman–Smith degeneration characterization. The unrestricted all-genus target is **not proved**. No counterexample to it, new literature resolution, or novelty determination has been established.

The audited author packet contains nine regular files, totaling 55,023 bytes. Its externally pinned manifest SHA-256 is `13a5055116fbed43fe1b2f355da34b8ff12d1e4aba0deac99ee1cbe26b023941`; the 21,817-byte `RESEARCH.md` SHA-256 is `16df888b6648f4de38e7c82b4de42e29f9fd5d84fc833e19a93a8029b0d59167`. These bindings were checked before and after the audit. Originals were not changed. No remote mutation or publication was performed, and no helper reviewer was used.

There is one nonblocking wording issue: Approach 3 calls the coordinate system “the integral basis (3),” although the coedge list displayed in (3) has index two. Read this as the ambient integral basis used to write (3), not as a claim that those coedges form an integral basis. The next sentence, the displayed matrix, and every computation use the correct ambient basis. An editorial clarification would help but does not change the proof or verdict.

## 1. Identity, imported results, and source limits

The primary target is the equality between perfect-cone indeterminacy for the map from admissible covers of base genus g+1 to principally polarized abelian varieties of dimension g and the union of the **closures** of FS2 and FS3. The 2014 OWR Question 3, printed page 2189, and the 2017 JEMS Question 7.4, printed page 692, were visually re-inspected. The closures and dimensions agree with the author note. They are neither the all-FS second-Voronoi statement nor the central-cone problem.

Dependencies checked directly in the supplied public-source PDFs:

- JEMS §3.1 supplies the relevant admissible-cover compactification and the no-branch-interchange condition at fixed nodes. Its smooth stack has normal-crossing boundary; the coarse space need not be smooth.
- JEMS §3.2 identifies integral anti-invariant cohomology with the dual of **projected** anti-invariant homology. This is exactly the lattice the note uses.
- JEMS (5.1), Remark 5.5, Theorem 5.6(2), and Remark 5.8 give the primitive coedge normalization, the perfect-cone minimum-one metric criterion, and the stack/coarse extension interpretation used here.
- JEMS Remark 6.1 gives the exact connected-invariant-subcurve characterization of an FS_n degeneration. This closes the geometric direction of the restricted theorem; it is not merely a necessary test for FS membership.
- JEMS Theorem 6.4, Theorem 7.1, and Remark 7.2 match the generic FS classification and the all-genus/low-dimension limits reported by the author.
- JEMS Appendix D and Theorem 5.1 support the cited wedge and Jacobian ingredients. The audit does not purport to reprove those published general theorems.

The EMS publisher page was independently opened and confirms the authors, journal, publication year, DOI, and page range. The current arXiv v1 page was independently opened and confirms Zakharov's July 20, 2026 preprint and the base-genus-four, target-dimension-three resolution problem. The thesis introductory Theorem 1.0.1, on printed pages 2–3, was visually checked: its result concerns base genus five and target dimension four, with the codimension-ten qualification. The later thesis discussion does contain inconsistent genus indexing; it is not a sound basis for silently upgrading that statement. The author's cautious use of the introduction is appropriate. Neither source settles the unrestricted question here. The complete thesis code/enumeration was not rerun.

A bounded new literature search did not locate a complete answer. This is not an openness certificate. The exact unsolvedmath.com page remained an inherited, explicitly disclosed access limitation; no attempt was made to circumvent its reported 403. Raw AI corpora were absent and not inspected. The author packet's repository-history checks are reported as prior-work metadata, not independently repeated by this mathematical audit. Its description of PR #600 as a different target is not used as a mathematical premise.

Primary public references:

1. Klaus Hulek, “The Prym map revisited,” OWR 39/2014, pp. 2187–2190. https://doi.org/10.4171/OWR/2014/39
2. Sebastian Casalaina-Martin, Samuel Grushevsky, Klaus Hulek, Radu Laza, “Extending the Prym map to toroidal compactifications of the moduli space of abelian varieties,” JEMS 19 (2017), 659–723, appendix by Mathieu Dutour Sikirić. https://doi.org/10.4171/JEMS/678
3. Josh Frinak, 2018 thesis, “Degeneration of Prym Varieties: A computational approach to the indeterminacy locus of the Prym map and degenerations of cubic threefolds.” https://math.colorado.edu/~casa/teaching/mentoring/frinakthesis.pdf
4. Dmitry Zakharov, “Resolution of the Prym map in genus 4,” arXiv:2607.18134v1, preprint. https://arxiv.org/abs/2607.18134v1

## 2. Fixed-node contraction, with the integral lattice retained

Let F contain all fixed edges in an all-vertices-fixed covering graph. Admissibility means these edges are fixed with their orientations, not reversed. Hence the involution acts identically on H1(F,Z). Contract each connected component of F, including any cycles in F. Integral graph homology fits into the exact sequence

    0 -> H1(F,Z) -> H1(cover,Z) -> H1(contracted cover,Z) -> 0.

The last map is onto integrally: a quotient cycle can be lifted by connecting its successive endpoints inside the contracted connected subgraphs with integral paths. Its kernel is the indicated cycle lattice.

Write P_-=(1-iota)/2. The contraction induces an onto map of P_-H1 lattices by equivariance and integral surjectivity. If an anti-invariant vector maps to zero, it lies in the real span of H1(F,Z), which is invariant. Its simultaneous invariant and anti-invariant membership makes it zero. Thus the induced map is a lattice isomorphism, not just an equality of dimensions or a rational comparison.

Dualizing gives the corresponding integral anti-invariant cohomology isomorphism. Noncontracted edge cochains pull back to their original edge cochains. Consequently the relation iota(e*)=-e* in full cohomology is preserved, so primitive normalization is preserved as well. A fixed edge has zero anti-invariant coedge; it contributes no nonzero prescribed ray. The rank-zero case is harmless: the empty quadratic-form criterion is vacuous and the monodromy cone is zero.

This is stronger than deleting fixed edges. For example, take two fixed vertices with two exchanged edge pairs and two branchwise-fixed joining edges. After contracting the fixed edges, the two exchanged pairs become loop pairs on one vertex and the lattice is Z^2, admitting the unit metric. Deleting the fixed edges instead leaves FS2 and gives a false obstruction. The independent controls detect exactly this failure mode.

For FS closure membership, a partition into the two limiting connected components cannot cross a fixed edge: all joining nodes of an FS degeneration come in exchanged pairs. Thus every component of F lies entirely on one shore. Conversely, a connected quotient shore lifts to a connected original shore because every contracted F-component is connected. The number of exchanged joining pairs is unchanged. This proves preservation of each exact FS_n closure condition, not only preservation of their union.

## 3. Integral anti-invariant cohomology and primitive coedges

After contraction, the covering graph doubles each edge of a connected multigraph G while fixing its vertices. Choose compatible orientations. Write t_e for the difference of the two coedge classes over e. These t_e are linearly independent over R: a nonzero anti-cochain cannot be an invariant coboundary. The anti-invariant dimension is the number of edge orbits, so they give real coordinates, including at loops.

If an integral cochain has coefficients (a_e,b_e), its class is anti-invariant precisely when its sum with its involute is an integral coboundary. Equivalently, a+b=B^T f for an integer vertex function f. In t-coordinates its anti-part is (a-b)/2. Reduction modulo two therefore gives a cut-code word. Conversely, for any integral d with d=B^T f modulo two, the choices

    a=(B^T f+d)/2,    b=(B^T f-d)/2

are integral and produce d/2. Both containments are established, giving

    L=Z^E + (1/2) C(G).

This concerns the lattice of cohomology classes, not a substitution of the integral anti-homology lattice. On FS2, the correct L contains (t1+t2)/2 but not t1/2 alone. The dual of integral anti-homology incorrectly contains the latter and changes primitive normalization and the extension answer. A separate audit control computes this distinction from full graph cycles.

For a nonloop bridge, its singleton is a cut word, so t_e/2 is integral. The entire lattice lies in (1/2)Z^E, so no greater division can be hidden. Conversely, integrality of t_e/2 forces a singleton cut and hence a bridge. This matches (5.1): the sum of the lifted coedges is zero exactly in this bridge case. The primitive coedge is t_e/2 for bridges and t_e otherwise.

Since all singleton bridge words belong to the code, they split off as coordinate factors. Clearing bridge coordinates in any codeword remains inside the code. The remaining code has no weight-one words, and in primitive coordinates the lattice is a direct product of ordinary Z bridge factors and the residual half-code lattice. In particular, a cut of size two made merely of two unrelated bridges does not create a false FS2 obstruction. Paired separating nodes in the base, loop pairs, and genuine short bonds are distinguished correctly.

## 4. Metric criterion: both directions, every form

For a binary linear code with no weight-one words, put L_C=Z^r+(1/2)C and prescribe every coordinate unit vector to have quadratic value one.

Sufficiency is exact. For the unit Euclidean metric, a nonzero integral vector has value at least one. In a nonzero parity coset of weight w, at least w coordinates have absolute value at least 1/2, so the value is at least w/4. Therefore minimum nonzero codeword weight at least four supplies a positive definite metric satisfying every required equality and inequality. Equality at weight four is allowed; it is not a defect or a limiting nonpositive form.

Necessity does not rely on a diagonal ansatz. For a word supported on S, changing any signs of its half-unit coordinates changes the vector by an integer vector. Every sign choice remains in L_C and is nonzero. Summing its outer products over all sign choices cancels the off-diagonal entries and leaves (1/4) times the sum of the coordinate outer products. Every putative form satisfying the coedge equalities thus has average value |S|/4 on these lattice vectors. For |S|=2 or 3 this is strictly below one, contradicting the lattice minimum. The claim concerns all real positive definite forms, not only rational candidates or finite searches. The bridge factors are orthogonal unit summands for sufficiency and irrelevant to the negative certificate.

The audit independently enumerates all binary subspaces of F2^r through r=5, filters out weight-one words, and checks their nearest parity-coset values. It also checks the sign-average outer-product identity through support size nine. These computations exercise, but do not replace, the argument above.

## 5. From short codewords to the exact geometric closures

A residual weight-two or weight-three word is an actual graph cut with no bridge among its edges. Suppose one shore were disconnected. Each of its connected components meets the other shore, since G is connected. It cannot meet it in just one edge, since that edge would then be a bridge in G. Thus two such components require at least four crossing edges, a contradiction. Apply the same argument to the other shore. Hence every such word is a bond, a cut with both shores connected.

Conversely, a bond of size two or three cannot contain a bridge: deleting that single bridge would be a proper separating subcut, contradicting minimality of the bond. Thus exactly these bonds give the residual words of weights two and three.

Doubling the n edges in such a bond gives exactly 2n joining nodes in exchanged pairs between two connected invariant covering subcurves. JEMS Remark 6.1 is the exact geometric equivalence to membership in the closure of FS_n. The reverse implication gives the same bond after fixed-edge contraction. Alternatively, smooth all nodes internal to the two subcurves while retaining the joining nodes; admissible-cover deformation coordinates allow this, and the result is the two-component FS_n form. The source criterion applies to the actual given cover, so component weights and stability are not being discarded to manufacture a nonexistent geometric cover.

The two directions together establish, on this restricted graph class,

    perfect-cone nonextension <=> residual short word <=> FS2 or FS3 degeneration.

This completes the restricted theorem with the correct closures. A doubled triangle provides a useful check: it has three covering components but has size-two bonds, so it is in the FS2 closure even though it is not a generic two-component FS2 example.

## 6. Graph admissibility and realization: an important scope distinction

“No edge inversion” is not by itself a complete geometric realization certificate for a graph with fixed vertices. On the normalization of an invariant component, the fixed node branches are ramification points of a smooth double cover. Their number at each component must be even by Riemann–Hurwitz. A loop fixed branchwise contributes two branches. For instance, two vertices joined by one fixed edge have odd fixed-branch degree at each endpoint and do not by themselves describe the required kind of admissible cover with every component invariant.

This does not invalidate the author's theorem, which begins with an actual admissible double cover, or the author's finite graph tests, which use no fixed edges. It does affect how the independent fixed-edge enumeration is reported: of 3,848 connected fixed-edge algebraic configurations tested, 424 have even fixed-branch degrees and admit realization with suitable component genera. The other 3,424 are algebraic stress tests only.

For completeness, such even-degree fixtures can be realized by choosing each quotient component smooth of genus at least two. Choose distinct branch points for the fixed incidences. An even branch divisor has a square root line bundle over C; the resulting double cover is connected when branched, and a nontrivial connected etale double cover can be chosen when the divisor is empty. Glue ramification branches at fixed edges and pair ordinary fibers equivariantly at the exchanged nodes. Local involutions at fixed nodes preserve the branches. Stability and global connectedness hold. The total genera satisfy the required double-cover relation. Thus these controls do not conflate arbitrary graph symmetries with actual covers.

The author's K5 example is valid with elliptic base components: five genus-one vertices and ten quotient edges give base arithmetic genus 11. Connected etale double covers of the elliptic components, glued at the twenty covering nodes in exchanged pairs, give covering genus 21 and Prym dimension 10. The reduced cut weights are four and six, so the unit metric applies. This is a valid higher-rank example; its novelty is not asserted.

Actual separating edges of the covering graph have zero coedge and must be omitted. A separate realizable fixture with a fixed central vertex, two exchanged outer vertices, and one loop on each outer vertex has two exchanged separating joining edges. Their coedges vanish on every integral cycle; only the loop-pair ray survives, and the anti-rank is one. This is different from a bridge of the contracted quotient graph in the all-fixed case, whose two lifts form a cycle and require the half-primitive normalization. Fixed-edge reversals and fixed-loop branch exchanges are separately rejected as inadmissible.

The exchanged-component limitation is real. Two triangles exchanged by the involution and joined at one fixed vertex have three exchanged edge orbits but anti-invariant cohomology rank one. The independent cycle calculation confirms this rank. They can be realized geometrically with base genus four and covering genus seven. Thus extending the independent-coordinate formula merely by counting exchanged edge orbits would be false. This example is a scope obstruction to that proof, not a counterexample to the perfect-cone equality; the wedge/Jacobian argument handles this particular cover.

## 7. Other four approaches

### Invariant one-vertex gluing

At a fixed cut vertex, every integral cycle is a sum of cycles from the two invariant pieces. The homology splitting is integral and equivariant, and hence so are the projected lattices and their cohomological duals. Nonzero coedges and primitive divisibilities belong to the individual factors. Orthogonal summation proves sufficiency of the two factor metrics; restriction proves necessity. The exchanged-isomorphic-piece block has anti-cohomology pairs (a,-a), with the expected ordinary coedges under identification with one copy. The cited cographic extension theorem is correctly imported. No decomposition of all remaining covers into these pieces is proved or claimed.

The overlapping-gluing warning is sound: the two triples {u,v,u+v} and {u,v,u-v} separately admit minimum-one metrics, but their union violates the parallelogram identity. This is not promoted to a realizable counterexample.

### Matroids and proper faces

The FS coedge matrix has determinant of absolute value two for n>=2. Every proper maximal subset can be completed with the first ambient coordinate vector to a unimodular basis, with the obvious coordinate completion if the special coedge is omitted. This verifies the saturation claim, including the smallest n. The controlling coordinate interpretation is explicit: let e1,...,en be an **ambient integral lattice basis**, identified in t-coordinates by e1=(t1+...+tn)/2 and ei=ti for i>=2. Then the listed coedges are a=2e1-e2-...-en and e2,...,en, so a maps to t1. The matrix Q_n is the Gram matrix in the ambient e-basis: its upper-left entry is n/4, its other first-row entries are 1/2, and its lower-right block is the identity. It is not a Gram matrix in a presumed unimodular coedge basis. All ray equalities are evaluated on the actual vectors a,e2,...,en in ambient integral coordinates. The proper-face argument deliberately appends e1 to get determinant one; it does not claim determinant one for the full coedge set. The sign-average vectors have integral e-coordinates and the primitive-coedge computation uses the correct half-code lattice. Thus no retained metric, primitive criterion, sign-average, or face calculation relies on the full coedge set being unimodular.

The displayed metric has Schur complement 1/4 and determinant 1/4. Under the correct lattice-basis change, its minimum is min(1,n/4). Thus generic FS4 disproves the proposed unimodularity shortcut while satisfying the perfect-cone criterion. Proper faces do not determine full-cone extendability. The wording clarification about “basis (3)” above is the only issue found here.

### Finite rational certificates and graph screening

The strict lower bound Q-lambda I>0 and the integer box cutoff give a valid sufficient certificate. For a vector outside the box, lambda times the squared Euclidean norm exceeds one, including when 1/lambda is a perfect square because the first omitted coordinate is B+1. Failure of a candidate or lower bound is not a nonextension proof; the author correctly says so. The independent checker uses exact LDL elimination rather than the author's determinant/Sylvester implementation to verify the four supplied positive metric examples, and exact rational lattice enumeration reproduces their minima.

The author screen is limited to 772 connected labelled simple graphs of at most five vertices, plus stated fixtures. It does not enumerate all admissible involutions or establish a finite reduction of the unrestricted theorem. The audit expands cycle-lattice checks to six vertices but makes no broader theorem from that finite expansion.

### Toroidal subdivision and descent

The rank-two outer-product identity for the new ray is exact. Both displayed containing cones have the claimed minimum-one metrics; an integral unimodular substitution identifies the second with the usual binary hexagonal form. The original FS2 cone still has the sign-average obstruction. Consequently a subdivision on which each piece maps into a target cone is not evidence that the original cone maps into a single cone. This is a valid obstruction to the descent shortcut, and Zakharov's low-genus resolution is not misrepresented as such a descent theorem.

## 8. Independent executable evidence and negatives

`independent_controls.py` is newly written and imports no author module. Its central calculation constructs an integral fundamental-cycle basis of the **entire covering graph**. Evaluating the t_e against those cycles gives an integer matrix T. The condition that d/2 represent integral cohomology is T d=0 modulo two. The computed parity-kernel dimension and containment are compared with the contracted quotient cut space. Primitive contents are computed as gcds of full cohomology coordinates and compared with bridges found by edge deletion. This is independent of the author's direct cut-code classifier.

Completed checks:

- All 27,476 connected labelled simple graphs on at most six vertices received the full cycle-lattice and primitive-content calculation. Counts by vertex number are 1, 1, 4, 38, 728, 26,704; positive classifications are 1, 1, 3, 16, 126, 1,402.
- For all 772 graphs through five vertices, FS bonds were independently found as minimal edge-deletion separators. The six-vertex run does not claim this additional deletion enumeration.
- All 3,848 connected fixed-edge configurations in the specified four-state-per-vertex-pair family through four vertices were checked; 424 satisfy the geometric parity condition. Each received contraction and allowed-partition checks, and minimal edge-deletion bond comparisons.
- Nine named loop/bridge/fixed-node/higher-rank fixtures, plus a separately computed exchanged-vertex example, were checked.
- All binary subspaces through rank five were examined; 194 have no weight-one words, counting the vacuous zero-dimensional case.
- Four independent positive metric certificates pass. FS metric positivity and determinant identities were additionally checked through n=12.
- Ten mathematical negative controls distinguish wrong lattices, missing primitive normalization, deletion instead of contraction, exchanged-vertex overreach, odd branch degrees, overlapping metric incompatibility, unimodularity overreach, omitted closures, and fixed-edge/loop branch inversions.
- Eleven independent frozen-binding mutation controls were rejected, including a self-consistent file-plus-manifest rewrite. These are external-digest binding tests; the original author's eight separate semantic integrity controls were also rerun successfully.

The final independent run passes 578,827 recorded assertions, as detailed in `INDEPENDENT_RESULTS.json`. An assertion count is an execution description, not a confidence measure or a universal proof. The independent calculations corroborate the conceptual proof and challenge common wrong alternatives; they do not certify all genera by finite computation.

## 9. Reproducibility, publication scope, and final boundary

The original author's verifier reproduces 5,325 assertions, 772 simple graphs, all four metric certificates, six rejected mathematical controls, and eight integrity negatives. A relocated replay of both checkers, with the exact pinned packet copied into a temporary directory, is recorded separately. The independent output must match byte-for-byte under relocation, and the original packet hashes remain unchanged.

The audit directory is publication-safe authored material: this report, executable controls, results, binding and source metadata, replay evidence, and its own manifest. It contains no PDFs, extracted primary-source text, page images, raw external records, or private coordination files. Public-source hashes, byte counts, titles, URLs, and inspection descriptions are recorded as metadata only. The audit manifest intentionally excludes itself; its digest is an external identifier.

Accepted retained result: the all-components-invariant infinite subfamily theorem, the gluing lemma, exact metric/obstruction certificates, and the stated bounded computations, with the published dependencies identified above. The strongest remaining gap is the unrestricted class with genuinely exchanged covering components and coupled coedges. None of the five approach families removes that gap. The proper final problem status remains **unsolved after 5/5 approaches**, with no novelty claim and no claim of an all-genus solution.
