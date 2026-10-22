# Independent primary-source, full-target, and priority recheck for PR628

Candidate: `677673860f9e67dffc610f52384f0bd60e65e363`.

Problem: 30000403 / OWR-1188-004. Review completed 2026-10-21 UTC.

## Verdict

The prior-implication finding is independently corroborated. The candidate's full scoped universal upper bound, and its degree-one assertion for geometric cover-point stabilizer V4, follow from the prior general compression framework with a short, explicit split-target torsor argument. The noncyclic conclusion is stronger than the packet: every noncyclic geometric cover-point stabilizer gives degree one. Known quadratic-obstruction examples already supply the universal lower bound. I found no mathematical gap in this implication and no primary-source reason to reverse the earlier closure on the ground that the universal bound still requires a substantive new discovery.

This is not a finding that a preexisting paper states the identical Hurwitz theorem verbatim, explicitly announces a solution of OWR-1188-004, or contains the candidate's exact six-point coordinates. No such historical statement was located in the bounded search. An independently noticed application or alternate proof may itself be new; this audit does not establish that smaller historical claim. The precise supported disposition is **prior implication verified; substantive novelty of the universal-resolution claim unsupported; preserve the mathematical proof and explicit certificate**.

The mathematical validity of the candidate is not rejected. I independently checked the finite lower-bound certificate using exact arithmetic. No stronger actual-cover, fixed-data, pointwise, effective, or positive-characteristic target is substituted for the packet's target.

## Independence and custody

The assigned review directory is the only location written. Git object reads were used to capture the candidate proof and clarification note. No Git/provider/PR/sheet mutation, commit, push, release, or external communication was performed. No other agent or chat was contacted. No old cached PDF was reused: every primary PDF used below was downloaded freshly. Old audit text was read only after the source-first checkpoint.

`SOURCE_FIRST_CHECKPOINT.md` was created at filesystem birth time 2026-10-21T17:59:27.900038Z and has SHA256 `e56852523b0da05e31bad4fd9b931a72ad39a647baed38478f9fdfcf1850ada1`. Its manually entered 18:03 UTC label was ahead of the clock; the research log records this timestamp correction without changing that checkpoint's sealed bytes. The checkpoint already contained the independently reconstructed original question, later theorem hypotheses, and the conic/gerbe bridge before the old priority verdict was read.

The immutable candidate proof is Git blob `f55a5f7bf7639ec14e265b26a38580ff4d4bf4ec`, SHA256 `20cb77c2ac8befd8d2f9be9a421d2925580c29e24002a1abc8e3dedb13caeb5a`. The clarification note is blob `00a87d5b189ba00fc6dc91981449b631f83fbd75`, SHA256 `6e3cfc1f66f0fbd297c97d2d660779492984d9d4ddac7d5c4ebcdc56a77d4f8a`. Full bindings are in `INPUT_BINDINGS.json`.

## Original question and its exact scope

Primary source: Cadoret's contribution to *The Arithmetic of Fields*, Oberwolfach Report 6/2006, printed pp.325-328, PDF pages 9-12. The freshly retrieved PDF matches the supplied SHA256 `803471040d06fcc1f83d5a0bd605e72bfd3a61434ee2a3dcd5259c48e2869412`. Printed pp.325-327 were also visually inspected to distinguish the fonts denoting actual objects and coarse moduli points.

Printed p.325 fixes characteristic zero, a finite group G, and nontrivial inertia classes C. Ordinary G-isomorphisms respect the deck-group identification; reduced isomorphisms allow a projective change of target. It constructs ordinary and reduced coarse spaces over the data field Q_C. Printed p.326 asks for an optimal upper bound on

\[
m_k(p^{\mathrm{rd}})=\min_{p\in\Pi^{-1}(p^{\mathrm{rd}})}[k(p):k],
\qquad p^{\mathrm{rd}}\in\mathcal H^{\mathrm{rd}}(C)(k).
\]

The discussion assumes r>=3. Printed p.327 distinguishes lifting coarse points from defining actual covers, and supplies older, generally larger bounds. Tower and hyperelliptic applications are separate statements.

The following scope assessment is an interpretation of those definitions, not a change of the question:

| Issue | Source/candidate assessment |
|---|---|
| Ordinary versus reduced | The target is a point in the ordinary space before the PGL2 quotient. |
| Inner versus absolute | The G-marking is retained. Replacing it by an absolute cover would change the problem. |
| Coarse point versus actual object | The target is a rational coarse point, equivalently a marked-cover field of moduli for a fixed split target. It need not provide a marked-cover model. |
| Target curve | The ordinary point uses the specified split P1, so mere descent to an arbitrary conic is insufficient. |
| Field quantifier | Every characteristic-zero k carrying the fixed data, not only number fields, finitely generated fields, or real fields. If a reduced point is given over an enlarged k, degrees are relative to that k. |
| Branch quantifier | At least three distinct branch points; no colliding branch points or wild ramification. |
| Stabilizer | E is the stabilizer of a coarse cover point in PGL2. It can be strictly smaller than the branch-set stabilizer. |
| Optimality | A sharp global constant answers the universal-bound formulation. It does not classify the optimum separately for every fixed datum or every point. The packet expressly says so. |

The candidate therefore addresses the natural universal-constant form of the original question. It does not overclaim an actual-cover theorem. Reading the question instead as requiring a complete pointwise or fixed-data classification would require an additional objective absent from both this packet's theorem and its stated result.

## Primary-source versions and dates

The source ledger records every fresh retrieval, its hash, exact locators, and limits. Essential readings were as follows.

1. **Cadoret, author-hosted GPGL2 manuscript, 24 PDF pages.** Fresh hash `705e6ec3b07bb11140f05ac70467ab96456f0ba444805e905ee60b188d402f76`. Read definitions in section 1.1, Corollaries 3.9 and 3.11 on manuscript p.13, and the complete Remark 3.14 on p.15. That remark gives quadratic necessity in cyclic base-invariant examples while leaving all its bounds' optimality unsettled. Its actual construction specifies odd n>=6, so choosing odd n>=7 is safe; its opening phrase is not proof of all even n cases.

2. **Cadoret, 2008 publication record.** DOI [10.1007/s11856-008-0019-0](https://doi.org/10.1007/s11856-008-0019-0). The publisher confirms March 2008, volume 164, pp.19-59, received 14 October 2005 and revised 16 September 2006. The nominal publisher PDF request returned an HTML subscription/cookie response. Consequently this review does **not** assert that manuscript Remark 3.14 is the identical numbered remark in the version of record. The manuscript's body and the publisher's bibliographic dates are separate evidence.

3. **Bresciani, divisor preprint, arXiv:2211.03438v1.** The arXiv version record dates it to 7 November 2022. Fresh hash `712012ee8faa1ca54a858031ae4f3a864d8a82c14a2ac28523af8a678f576738`. Read section 1; Proposition 2 and its proof, pp.3-4; Lemma 11 and proof, pp.7-8. Proposition 2 is a theorem about arbitrary finite etale gerbes, not just divisor gerbes. It forces the band to be cyclic tame when the source rational curve is nonsplit and the geometric fibers are irreducible genus-zero curves. Lemma 11 separately addresses split-P1 descent.

4. **Bresciani, published divisor paper.** Fresh institutional version-of-record PDF hash `a5c092e1cd1ffe5e1e47b93d6fbe15b122c6fc4164284bcc0e1a9613c1e93db6`. Journal of Algebra 647 (2024), 72-98, DOI [10.1016/j.jalgebra.2024.02.021](https://doi.org/10.1016/j.jalgebra.2024.02.021); PDF front matter gives available online 1 March 2024. The general result is **Proposition 28**, printed pp.89-91, not Proposition 2. The split-divisor criterion is **Lemma 26**, printed p.88, not Lemma 11. The hypotheses/conclusions needed here agree with the cited preprint results. The expanded published proof was checked rather than inferred from matching titles.

5. **Bresciani, general structures, arXiv:2303.01409v2.** Version record: v1 2 March 2023; v2 28 November 2023. Fresh v2 hash `ec3c50004c1576c0f7110be426e9ae43f13f6138412d9257a9c17f23a9f7dd03`. Read the setup, Theorem 2, Definition 5, Lemma 6, and the constructions/proofs through Corollary 10, pp.2-6; also the split-variety warning before Definition 15 on pp.9-10. The setup permits arbitrary k and nontrivial arithmetic twisting. Geometric stabilizers are finite tame groups.

6. **Bresciani, published general-structures paper.** Fresh publisher PDF hash `9675a0481be75cc46fe03897f2a161db6771c50d6dfd817bedbe0376685141d0`. DOI [10.1007/s40574-023-00399-z](https://doi.org/10.1007/s40574-023-00399-z), online 27 November 2023, volume 17 (2024), pp.613-624. Theorem 2, Definition 5 and Lemma 6 retain those numbers. Relevant printed pages are 615-618. The preprint v2 appears one day after the publisher's online date; they must not be assigned the same date without qualification.

7. **Huggins, arXiv:math/0407088v1.** Fresh hash `126b76a8fd3320030f7a801cd6a72d12c8eed84756ed87c9e1ba697adcbbe8a2`; version record 6 July 2004. Lemma 5.5 and Proposition 5.6, pp.11-12, give the underlying cyclic pseudo-real hyperelliptic family used by Cadoret. I read the displayed cocycle failure visually. This independently supplies dated quadratic-obstruction examples without assuming the inaccessible 2008 body has the manuscript's numbering.

All essential source PDFs were freshly retrieved, including both later published versions. HTTP Last-Modified dates are retrieval/cache metadata and are not substituted for publication or arXiv submission dates.

## Checkable implication from the prior framework

This derivation is written out here. It is not a quotation of a theorem asserting the precise Hurwitz conclusion. Let H=PGL2 over k, with char(k)=0.

### 1. The relevant finite-stabilizer homogeneous space

For a given rational reduced point x, let F be its ordinary geometric orbit, with its reduced scheme structure descended to k. The geometric quotient property makes the geometric fiber one orbit. Equivalently, reduce the scheme fiber; in characteristic zero reduction is geometrically reduced, and field-valued points kill nilpotents. Thus a K-point of F is a K-point of the original coarse fiber.

Over an algebraic closure, F is H/E. The finite geometric group E stabilizes a **coarse marked-cover point**. Its faithful permutation action on the finite branch set implies finiteness: an element fixing all of at least three distinct points of P1 is identity. E is finite etale in characteristic zero.

No arithmetic form of E is assumed constant. This construction is made over k before choosing any geometric object. In particular, arbitrary outer/Galois twisting of the geometric group is retained.

### 2. A faithful auxiliary family, and its compression conic

Form the finite etale gerbe

\[
\mathscr R=[F/H]
\]

and the representable P1-family

\[
\mathscr U=[(F\times\mathbf P^1)/H]\longrightarrow\mathscr R.
\]

Geometrically these are BE and [P1/E]. E acts faithfully on the auxiliary projective line because E is literally a subgroup of PGL2. These are exactly the faithful universal-family data permitted by the prior general-structures framework (Definition 5/Lemma 6 and Theorem 2). This is an abstract coarse-orbit structure. It is not the gerbe of actual marked covers, whose central inertia could act trivially on the target.

The coarse space Y of U is a smooth projective geometrically connected genus-zero curve: after geometric base change it is P1/E, and finite quotients of a smooth curve have smooth coarse curves; the invariant rational function field is rational. The descent preserves properness and smoothness, so Y is a conic over k, possibly nonsplit.

The union of the fixed points of nonidentity elements of E is finite. Therefore the trivial-inertia locus of U is a nonempty open which is isomorphic to a nonempty k-open Y0 in Y. It gives a rational map

\[
Y\dashrightarrow\mathscr R.
\]

After pullback along a geometric object of R this morphism has fiber a nonempty open of P1. That fiber is irreducible and has genus-zero smooth completion. This verifies the actual fiber hypothesis of Bresciani's Proposition 2 / published Proposition 28; it is stronger than merely knowing that Y itself has genus zero.

### 3. A compression point yields an ordinary point on split P1

This is the crucial additional step. Neutrality of R by itself would only supply a twisted target and would not prove the desired statement.

Let K/k be an extension and choose y in Y0(K). The corresponding object of U(K) consists of an H-torsor T and an H-equivariant map

\[
T\longrightarrow F\times\mathbf P^1.
\]

Its second component is a K-point of the associated Brauer-Severi curve C_T. Since a genus-zero curve with a rational point is split, the PGL2-torsor/conic correspondence makes T trivial. Trivializing T and evaluating the first component produces a point in F(K). This establishes a coarse lift on the prescribed split target.

Conversely, a point f in F(K), together with any K-point of P1, yields an object of U(K) and hence a K-point of Y. Every extension K of a characteristic-zero field is infinite, and a split conic has infinitely many K-points, so Y(K) nonempty implies Y0(K) nonempty. Consequently

\[
F(K)\ne\varnothing\quad\Longleftrightarrow\quad Y(K)\ne\varnothing
\]

for every field extension K/k. This is an exact conic criterion for the ordinary coarse lifting problem.

### 4. Universal bound two

If Y is split, choose a k-point of Y0. If Y is nonsplit, embed it as a smooth plane conic. In the dual plane, exclude the tangent locus and all lines meeting the finite geometric complement Y minus Y0. That excluded set is proper and k-defined. Since k is infinite, a k-line exists outside it. Its intersection with Y is an etale degree-two divisor contained in Y0. Because Y has no k-point, it is one closed point of separable degree two. Thus Y0(K), and then F(K), is nonempty for some [K:k]=2.

This works for every geometric stabilizer, including E=1 and every cyclic E. It uses only conic index <=2, never the false assertion that all arbitrary 2-torsion Brauer classes have index two.

### 5. Noncyclic stabilizers, including V4

If E is noncyclic and Y has no k-point, apply the prior Proposition 2 / published Proposition 28 to Y rationally mapping to R. Each hypothesis was checked above: k is a field; Y is an anisotropic rational curve; R is a finite etale gerbe; and the geometric fibers of the rational map are irreducible genus-zero curves. The theorem makes the geometric band cyclic. But R over the algebraic closure is BE, so its geometric band is E. This is a contradiction. Hence Y is split and F(k) is nonempty.

In particular E=V4 gives degree one with no assumption on a Galois-equivariant normalizer section or a trivial Galois action on E. An elementary corroboration uses the three branch values of P1 -> P1/E for a noncyclic characteristic-zero subgroup: they descend to an odd-degree divisor on Y, forcing Y to split. The general proposition avoids needing this classification-based branch-signature argument.

This five-step chain establishes the entire scoped upper-bound theorem, not only a divisor analogue. The passage from a coarse Hurwitz orbit to a faithful auxiliary family and the torsor calculation close the cover-versus-divisor and split-versus-twisted gaps.

## Known sharpness, and the packet's explicit example

The universal constant cannot be one. The Huggins family has a real field of moduli and no real model; its branch divisor cannot be moved to a real divisor on split P1, since any real even reduced branch divisor on split P1 defines a hyperelliptic double-cover model over the real field. The reduced C2-cover class is real by uniqueness of a double cover with prescribed geometric branch divisor. Thus the ordinary coarse lift fails over the real field and exists over its quadratic algebraic closure. Choosing the odd n>=7, m=3 subfamily also agrees with the safe portion of Cadoret's manuscript Remark 3.14. These examples already force two for a universal bound ranging over every field and branch number.

This argument does not require that the earlier examples have six branches or field Q. The packet's particular Q(i) six-point example is a useful stronger concrete realization of the same global lower-bound obstruction.

I independently recomputed the packet's fifteen projective four-subset J-values in Q(i) using `fractions.Fraction` pairs and no floating-point comparison. All fifteen are distinct, proving that its six-point divisor has trivial projective stabilizer: every stabilizing permutation must preserve every four-subset and hence every complementary pair, so it fixes each point. The involution tau(z)=-1/conjugate(z) was checked to permute the six points as (01)(23)(45). Its lack of fixed points contradicts conjugacy to real conjugation if an ordinary real lift existed. This validates the exact lower-bound certificate; it does not claim that the exact coordinates appeared previously.

The independent program and `SHARPNESS_CERTIFICATE.json` are retained. The first attempt to import SymPy failed because it is absent from the default Python; no environment modification was made. The completed check uses only the standard library.

## Bounded current primary-literature search

The search, on 2026-10-21, covered the exact Cadoret title, the exact problem identifiers, reduced/ordinary Hurwitz lifting with degree-two or quadratic terminology, Bresciani/Cadoret together, general structures, divisor descent, and rational-map FOD/FOM terminology. `SEARCH_LEDGER.md` records the queries and relevant primary hits. Search-engine snippets were discovery aids, not substitutes for the primary passages used in the proof.

A relevant current primary hit was Naccarato, *The arithmetic of critical values I: equicritical quartic polynomials*, DOI [10.1093/imrn/rnag141](https://doi.org/10.1093/imrn/rnag141), with freshly obtained arXiv:2501.03244v3 dated 25 June 2026. Section 3.2, PDF p.10, discusses rational degree-one lifting and the distinction between base invariant and full branch stabilizer. It cites Cadoret and gives results for polynomial data. This does not contradict the quadratic universal bound: deciding whether a specific point lifts over the original field is a different problem. It also is not evidence that the exact universal Hurwitz conclusion was historically advertised as solved.

Hidalgo's primary arXiv record 2411.08006 concerns universal actions on rational maps and quadratic FOD/FOM bounds. It is neighboring corroboration, not an identified equivalence between arbitrary marked Hurwitz data and a rational-map action. No stronger conclusion is inferred from that title or abstract.

No source located by this bounded search explicitly names OWR-1188-004 as resolved with the identical theorem. No exhaustive absence or earliest-priority guarantee follows from a web search. The decisive point is the displayed short implication from dated, freshly checked prior theory plus older sharpness, not an assertion about missing search hits.

## Adversarial scope checks and remaining gaps

| Route or proposed obstruction | Result | Exact limit |
|---|---|---|
| Coarse point replaced by actual cover | Avoided: F is the ordinary coarse orbit. | Actual central descent obstruction remains outside target. |
| Neutral gerbe mistaken for split line | Closed by the explicit PGL2-torsor argument. | Neutrality alone would be insufficient. |
| Branch stabilizer substituted for cover stabilizer | Avoided: E=Stab_H(p). | Equality is used only for the C2 sharpness examples, where uniqueness proves it. |
| Only constant arithmetic groups covered | Avoided: quotient gerbe is formed over k. | Only its geometric band is identified with E. |
| Nonreduced fiber | Harmless for field-valued points; use reduced homogeneous orbit. | Requires the stated geometric quotient property. |
| Trivial stabilizer | Gives the usual conic obstruction, not automatic degree one. | Nonsplit conics occur. |
| Nontrivial cyclic stabilizer | Universal degree <=2 applies. | No universal degree-one assertion. |
| Noncyclic stabilizer | Prior proposition forces split compression. | Includes V4 and is stronger than the packet. |
| Arbitrary characteristic-zero fields | Infinitude, separability, tame inertia and conic argument all hold. | No finite-generation or number-field assumption. |
| r<3, repeated branches, wild characteristic | Excluded exactly as in the audited target. | Cannot be presented as a proved repair. |
| Exact historical first occurrence | Undetermined. | Does not change the displayed mathematical implication. |
| Published2008 remark numbering/body | Not verified. | Cite the author manuscript locator with a distinct publication DOI. |

Mathematical gap in the prior implication: **none identified**. A new manuscript could present the homogeneous-space application or the elementary V4 realization as an alternate proof, with full prior credit, but this record does not establish historical novelty of those smaller contributions. Strengthening merely to all noncyclic stabilizers does not restore a new theorem: the prior proposition already gives that statement. Changing to actual cover models, pointwise/fixed-data optimality, explicit equations/algorithms or characteristic p would require additional research and is not a completed repair of the current packet.

The retained useful material is the valid elementary normalizer proof, its elliptic realization of arbitrary cubic etale/S3 action, and the exact small Q(i) obstruction certificate. The audit makes no allegation of copying and does not erase these artifacts. The required caution is to distinguish their possible expository or example-level value from an established substantive new solution of an unsolved universal bound.
