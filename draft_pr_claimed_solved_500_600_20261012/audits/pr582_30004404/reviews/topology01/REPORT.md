# Independent topology audit: PR 582 / problem 30004404

**Verdict: PASS for the complete counterexample to the literal universal OWR question.** No mathematical repair is required. A minor citation-locator correction is recommended below. The result does not settle whether some other hyperbolic knot admits a persistent free subgroup of rank two, and it carries no novelty or priority certification.

This audit binds to the candidate acquired from declared PR head `e4b27ac757babc1aea75149ea986ed2beea438f9`, with author manifest SHA-256 `4f6575af14a3e8b72e61202c45e411b4febcaa7770c3e7e8af45576eda6218f8`. All 22 files in the parent's acquisition snapshot and all ten author-manifest entries were checked against their recorded sizes and hashes. This verifies the local acquisition binding; I did not independently query or alter the current remote PR state. The mathematical verdict concerns the frozen proof and its stated scope.

## 1. Independence and exact target

The initial source checkpoint was saved at **2026-10-15 05:24:31 UTC**, before reading the candidate, its source ledger, its historical audit, or a prior verdict. Its receipt records its hash and the unread-candidate state. The assignment's proposed mechanism was treated as a hypothesis, so this is source-first adversarial verification, not an assertion of blindness to that mechanism. No other reviewer's findings were read or requested. After the checkpoint I read all four requested candidate files and the historical audit's entire report, corrections, source receipts, code, and result. The research log records read-scope clarification and later checks without rewriting the early checkpoint.

The source is [Motegi's contribution to OWR 8/2020](https://ems.press/content/serial-article-files/46844), joint work with Ito and Teragaito, printed pp. 491-493; the final question is on printed p. 493 / PDF page 29. Its hypotheses and equation have the following precise mathematical content. Write

\[
G_K=\pi_1(E(K)),\qquad
N_{p/q}=\langle\!\langle\mu^p\lambda^q\rangle\!\rangle,
\qquad
q_r:G_K\longrightarrow\pi_1(K(r)).
\]

Here \((\mu,\lambda)\) is the meridian and preferred longitude, \(p,q\) are coprime, and \(\ker q_r=N_r\). The assertion being tested is

\[
\forall K\,[K\text{ hyperbolic in }S^3,
\ \forall r\in\mathbb Q\;|\pi_1(K(r))|=\infty]
\quad\exists H\leq G_K:\ H\cong F_2,
\ H\cap\bigcup_{r\in\mathbb Q}N_r=\{1\}.
\]

In particular, this is not an existential quantifier over the knot. It is also not disjointness from the intersection of kernels. Distribution of intersection over union shows that the subgroup must inject under **each** filling quotient. A single nonidentity element of \(H\) killed by a single rational filling defeats that \(H\). The witness may depend on \(H\) and its free basis.

The rational index includes \(0=0/1\), which kills the longitude. It excludes the meridional coefficient \(\infty=1/0\), which kills the meridian and yields \(S^3\). The phrase concerning absence of finite surgery consequently concerns nonmeridional slopes. Reading it to include the meridional filling would make its class of knots empty and contradict the source's explicit rational index and preceding discussion. No cofinite-slope exception is printed.

The imported catalogue record agrees with the primary question. Its dated open-status assessment is not evidence against a checkable counterexample and is not a proof of novelty.

## 2. The 2026 question: full context and possible inherited hypotheses

I read the [full v1 PDF](https://arxiv.org/pdf/2604.01697v1), the [full Section 7.1 in HTML](https://arxiv.org/html/2604.01697v1), its preceding definitions and relevant theorem hypotheses, and both pages 16-17 visually. The current abstract record lists v1, submitted 2 April 2026; it does not list a later version as of this check.

The source's set \(\mathcal S(g)\) is a subset of \(\mathbb Q\), consisting of slopes that kill \(g\). Its persistent elements are nonidentity elements with \(\mathcal S(g)=\varnothing\). Section 7.1 makes a subgroup persistent exactly when all its nonidentity elements are persistent. Thus its group property is exactly the all-rational injectivity property above; zero is not excluded as an exceptional, solvable, or nonhyperbolic slope.

Definition 1.5 introduces torsion surgery and states that it is finite or reducing; it then announces a focus on hyperbolic knots without such surgery. Theorems 1.6-1.7 expressly repeat that hypothesis. Question 7.1 itself prints only that \(K\) is hyperbolic, followed by the rank-two persistence question. No no-finite-surgery condition and no rational-slope exception is explicitly repeated there. Section 1.1's realization-property result has additional hypotheses excluding Seifert or reducing surgery, but those are hypotheses of that separate result, not a redefinition of persistence or an exception in Question 7.1.

There are two useful qualifications:

1. The question's fixed-arbitrary-\(K\) wording has a universal reading. Its surrounding paragraph, however, discusses the absence of any known positive hyperbolic examples, which also motivates an existential search for one. A figure-eight negative example does not resolve that existential problem. The candidate and historical audit already preserve this distinction; neither rewrites the printed question as literally existential.
2. Even if one imports the earlier no-torsion-surgery focus into the later question, that does not remove this counterexample. Brittenham-Wu Lemma 2.1 excludes reducing surgeries on the hyperbolic figure-eight knot, and the all-rational argument below excludes finite surgeries. The alternative interpretation therefore supplies no hidden hypothesis that defeats the example.

The 2026 preprint itself also states, in the proof of Lemma 2.4, that figure-eight has no finite surgery. That is useful corroboration from an identified primary full text. This audit does not substitute that uncited assertion for the classical all-slope verification below, or claim that these authors already supplied the particular negative argument.

## 3. Topology imports and their actual scope

The private downloads' hashes all match the six candidate receipts exactly. `SOURCE_LEDGER.json` gives exact URLs, byte lengths, SHA-256 values, read pages, visually inspected pages, and limitations. It distinguishes the author-hosted and arXiv preprints from the uninspected published journal PDF. A matching hash establishes source identity, not truth.

### Figure-eight identification, completeness, and framing

[Thurston's Chapter 4](https://library.slmath.org/nonmsri/gt3m/PDF/4.pdf) is electronic version 1.1, March 2002, of the 1980 notes. Sections 4.1-4.3 construct and analyze the complete two-ideal-tetrahedron figure-eight structure. The completeness equations are visible on printed p. 54 / PDF page 12. The knot is the explicitly named figure-eight, not a different two-tetrahedron cusped manifold. Brittenham-Wu identify their \(K_{[2,-2]}\) as figure-eight; Gukov-Manolescu's conventions identify \(4_1\) likewise. No link-to-knot or sister-manifold substitution occurs.

Thurston's Sections 4.5-4.6 define primitive filling pairs with first coefficient on the meridian and second on the longitude. Thus \((0,1)\) is longitude filling and \((1,0)\) meridian filling. His generalized standalone symbol \(\infty\), used instead of an ordered pair, denotes an unfilled cusp; that is a different notational use from the rational coefficient \(1/0\) in the OWR source. The proof uses the primitive pairs correctly and does not confuse these two conventions.

Theorem 4.7, printed p. 61 / PDF page 19, supplies a hyperbolic metric for all figure-eight surgery manifolds except the symmetry classes represented by

\[
(1,0),\ (0,1),\ (1,1),\ (2,1),\ (3,1),\ (4,1).
\]

The same page records sign symmetry from an orientation-reversing homeomorphism; Section 4.6 describes the action on meridian and longitude. Consequently the rational exceptions are exactly

\[
E=\{0,\pm1,\pm2,\pm3,\pm4\}.
\]

The six unoriented manifold symmetry types must not be mistaken for six rational slopes. Nor does the theorem assert that its exceptions have finite groups. Its following discussion explicitly separates proving hyperbolicity outside that list from analyzing the exceptions.

### Toroidal and Seifert exceptional cases

The [Brittenham-Wu author preprint](https://homepage.math.uiowa.edu/~wu/papers/p32.pdf) is a 12-page preprint marked as such, rather than the journal's pp. 97-113. Its Introduction fixes standard meridian-longitude rational slopes and excludes the meridian. Theorem 1.1(4), on preprint p. 2, gives the following classification:

| Rational coefficients | Type | Reason the fundamental group is infinite |
|---|---|---|
| \(\mathbb Q\setminus E\) | Hyperbolic | Compactness of a finite cover contradicts universal cover \(\mathbb H^3\). |
| \(0,4,-4\) | Toroidal | An essential torus injects \(\mathbb Z^2\). |
| \(1,-1\) | Seifert over \(S^2(2,3,7)\) | Infinite hyperbolic triangle-group quotient. |
| \(2,-2\) | Seifert over \(S^2(2,4,5)\) | Infinite hyperbolic triangle-group quotient. |
| \(3,-3\) | Seifert over \(S^2(3,3,4)\) | Infinite hyperbolic triangle-group quotient. |

The preprint credits its figure-eight case to Thurston. Its concluding proof on p. 12 expressly says that Thurston's hyperbolicity result is stronger. Thus this is compatible evidence with correct historical credit, not a second independent discovery of the classification. I also retrieved arXiv `math/0011005v1` and checked its first two pages; it corroborates this theorem and version identity. I did not access a full publisher PDF and do not transfer a journal page number to an inspected preprint page.

Here are the necessary hypotheses behind the infinity column:

* Each filled manifold is a closed orientable 3-manifold, obtained from the orientable knot exterior by gluing a solid torus. A hyperbolic metric on a closed manifold is complete. Its universal cover is \(\mathbb H^3\). If the fundamental group were finite, that universal cover would be a finite cover of a compact space and therefore compact, a contradiction.
* Toroidal means an essential incompressible torus. An orientable torus embedded in an orientable 3-manifold is two-sided. The loop theorem gives \(\pi_1\)-injectivity; Thurston states the equivalence with the injective definition on printed p. 71. A finite group cannot contain \(\mathbb Z^2\). No assumption that an arbitrary immersed torus injects is being made.
* For a Seifert fibration over \(S^2(a,b,c)\), killing the regular fiber produces the orbifold quotient
  \[
  \Delta(a,b,c)=\langle u,v,z\mid u^a=v^b=z^c=uvz=1\rangle.
  \]
  The relevant orbifold Euler characteristics are \(-1/42,-1/20,-1/12\), respectively. They are negative, so the classical hyperbolic-triangle construction yields infinite triangle groups. Hence the surjecting manifold groups are infinite. Being Seifert fibered alone would not suffice, because spherical-base cases can have finite fundamental group.

The base orders are read from [Gukov-Manolescu, Section 9.4, p. 71](https://web.stanford.edu/~cm5/surgeries.pdf). Section 4.1, printed p. 18, explicitly defines their \(M(b;a_i/b_i)\) as a Seifert fibration over \(S^2\), with the denominators giving fiber multiplicities. The required positive-slope assignments are well-defined in that notation.

Their middle display does literally put a negative subscript \(-3\) beside the positive coefficient 2. This is a printed defect, not an OCR error. I do not assert that the displayed equality is true. Independently, knot surgery has \(|H_1(K(p/q))|=|p|\) when \(p\ne0\), so coefficients 2 and \(-3\) cannot give orientation reversals of the same manifold: the orders are 2 and 3. The Seifert homology determinants from the three positive data are 1,2,3, agreeing with coefficients 1,2,3. For the negative coefficients the candidate uses Thurston's independently documented sign symmetry, which gives the same abstract group properties under orientation reversal. There is no circular repair of the source's equation.

These cases exhaust **all** rational slopes, including nonintegral slopes of unbounded denominator. They prove that figure-eight satisfies the target's no-finite-nonmeridional-surgery premise. The algebraic controls do not compute this classification.

### The zero-filling torus bundle

[Vu The Khoi, printed p. 524](https://math.ac.vn/public/uploads/files/0803519.pdf), explicitly identifies zero surgery on figure-eight as a torus bundle. The preceding page defines the \(p/q\)-surgery notation and begins the figure-eight example in Section 3. This is an actual full-source statement, used as a known topology input, not a claim that this article proves the identification anew.

Thurston's printed p. 70 / PDF page 28 also describes the mapping torus of \(A=\begin{pmatrix}2&1\\1&1\end{pmatrix}\), but its first surgery coordinate is visibly D-shaped in this electronic edition. The following sentence uses \((0,1)\) and \((0,-1)\). The candidate correctly discloses the glyph and independently supports the zero identification with Khoi. The particular matrix is supplementary; the obstruction only needs some torus-bundle structure over a circle.

There is one minor locator issue: Khoi's first example is headed by an unnumbered figure-eight label in Section 3. It is not printed as Section 3.1. The exact page 524 is correct. Replacing the candidate's `§3.1` with `Section 3, figure-eight example, p. 524` would improve precision without altering the frozen proof's mathematical meaning.

## 4. Independent logical verification of the obstruction

For a torus bundle \(T^2\to M\to S^1\), the homotopy exact sequence gives

\[
1\longrightarrow\mathbb Z^2\longrightarrow\pi_1(M)
\longrightarrow\mathbb Z\longrightarrow1.
\]

The first injection uses \(\pi_2(S^1)=0\), and the quotient uses the connected fiber. Therefore the commutator subgroup of \(\pi_1(M)\) lies in its abelian kernel. In particular \(\pi_1(M)''=1\). Splitting the extension, choosing a monodromy matrix, or proving a faithful affine model is unnecessary. The group is infinite because it surjects onto \(\mathbb Z\). No inference from solvability to finiteness occurs.

Let \(H\le G_{4_1}\) be any actual subgroup isomorphic to \(F_2\), with a free basis \(a,b\). Put

\[
c=[a,b],\quad d=aca^{-1},\quad w=[c,d],
\qquad [x,y]=xyx^{-1}y^{-1}.
\]

Both \(c,d\) lie in \(H'\). Under the zero-filling homomorphism their images lie in the abelian commutator subgroup of its metabelian target. Thus \(q_0(w)=1\), indeed \(H''\le\ker(q_0|_H)\).

The word does not vanish abstractly in \(F_2\). Free reduction yields `xyXYxxyXYXyxxYXX`, where capitals denote inverses. This is a nonempty word of length 16 with no adjacent inverse pair. As an independent finite-quotient certificate, assign, on the letters \(0,1,2,3\),

\[
x=(1\ 2\ 3),\qquad y=(0\ 1).
\]

Using the multiplication convention specified in the control script, the same \(w\) evaluates to \((0\ 1)(2\ 3)\), which is nonidentity. This second certificate does not assume the permutation generators are free; any nonidentity image proves a free word is nontrivial.

The isomorphism from the abstract free group to the chosen embedded \(H\) preserves that nonidentity element. Hence

\[
\{1\}\ne H\cap N_0
\subseteq H\cap\bigcup_{r\in\mathbb Q}N_r.
\]

This holds for every such \(H\), with the same slope zero. The figure-eight knot is admissible by Section 3. Therefore it is a complete counterexample to the exact universal target. No existence or special construction of a particular \(H\) is required to prove that none can have the property. Nontrivial individual persistent elements and cyclic persistent subgroups remain compatible with this argument.

## 5. Historical corrections and new falsification controls

The earlier `audit-independent/AUDIT.md` was read in full after the independent checkpoint. Its result was not used as proof authority. Its material corrections and caveats withstand this fresh source check:

| Earlier correction or caveat | Independent finding |
|---|---|
| The original expression is a union over all rational slopes. | Confirmed visually, including zero. |
| The later printed question is not literally an existential quantifier over knots. | Confirmed, while retaining the unresolved positive-example problem. |
| The D-shaped coordinate must not alone be treated as a clean zero-surgery receipt. | Confirmed visually; Khoi gives an explicit independent statement. |
| The middle negative-slope Gukov-Manolescu equality is erroneous and must not be used. | Confirmed visually and falsified independently by homology orders. |
| Negative slopes should use the independently sourced amphichiral symmetry. | Confirmed from Thurston's framing and symmetry discussion. |
| Seifert, infinite, solvable, torsion-free, and containing \(F_2\) are different properties. | The proof uses the precise implications it needs and does not conflate them. |
| Finite controls do not prove the topology or the all-slope quantifier. | Correct; the universal deduction relies on imported theorems and explicit arguments. |

`independent_controls.py` and `independent_results.json` add a distinct finite-permutation mechanism and a homology check. Results:

* All 576 ordered pairs of \(S_4\) were evaluated; 168 give a nonidentity value of \(w\), with a concrete first witness preserved. All 36 pairs in the embedded metabelian \(S_3\) give identity, guarding against a broken commutator evaluation.
* The Seifert homology determinants and orbifold characteristics are exact rational/integer calculations. Finite first homology is never interpreted as finite fundamental group.
* All ten author-manifest files and all 22 acquisition-snapshot files match. The six independent PDF receipt identities match the candidate's source receipts.
* Both pre-existing scripts were executed after reading their code. The author's 30,625 parameter-pair output and the old independent 10,125 parameter-pair output reproduce byte-for-byte.

Run `python3 independent_controls.py` in this review folder. Its default reads the preserved original attempt directory in this audit; an optional first argument selects that directory explicitly. It performs no network access or Git writes and writes only stdout. Its companion JSON is the expected stdout. Source receipt comparisons use authored metadata, so the ignored private PDF cache is not required for reproduction.

## 6. Decision, actionable notes, and limits

**No mathematical blocker was found.** The candidate meets the full original target by disproving its universal assertion, rather than proving an easier replacement. The source imports support every rational-slope case and the zero-filling law obstruction. The head-bound proof already contains the material scope and typography caveats.

The only recommended text refinement is the Khoi section locator described above; it is not a reason to withhold mathematical PASS. If a later public summary cites the 2026 question, preserve both its arbitrary-\(K\) wording and the separate unresolved existential motivation. If desired, add that even an inherited no-torsion-surgery restriction does not remove figure-eight. Do not promote these optional explanatory improvements into an assertion that the later authors' intended scope has been determined.

The strongest verified result is that a particular admissible hyperbolic knot, \(4_1\), admits no free subgroup of rank two surviving every rational nonmeridional filling. The exact remaining gap in that result is **none**, conditional on the clearly identified classical topology inputs. They were checked in primary full sources, not re-proved from a surgery diagram or verified in a proof assistant.

Historical priority remains uncertified. The 2026 authors' discussion is disclosed, and this audit makes no claim of a first solution or a newly discovered surgery classification. It neither determines whether any other hyperbolic knot admits a positive example nor treats a version omitting finitely many slopes as solved. No inaccessible cyclic-persistent full text, generalized search result, or missing prior publication is used as proof evidence.

All authored outputs are sealed by ordinary `SHA256SUMS`. Primary PDFs, extracted full texts, HTML, and renderings remain under ignored `.cache/` and are excluded from that seal and from delivery. No candidate or old-review files were edited, no branch/index/remote writes occurred, and no manuscript, release, DOI, or external communication was initiated. Final audit completion estimate: **100% for this verification scope**, with the separate existence and priority questions explicitly open.
