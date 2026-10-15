# PR36 independent arithmetic and graph priority audit

**Universal priority outcome: `PRIOR_APPLICATION`, independently sealed.** The negative answer to the literal AIM 2.6 target follows directly from an explicit algebraic family printed by Silverman in 1995. PR36's degree-11 graph may be a different critically fixed example, but the universal negative answer must not be promoted as a novel resolution.

This is a source-specific priority audit. It follows the assignment that mathematical verification preceded priority work; it does not replace the three mathematical family certificates for the proposed degree-11 construction. It adds zero proof-attempt turns to the original 1/5 budget. No sibling or root priority report/mechanism was read, including after sealing this finding. No source-dependent fresh proof-search route was opened.

## Exact claim and decisive old construction

The full original `source_record.problem`, complete upstream prior report, full `CANDIDATE.md`, and original `SOURCES.md` were read first. The literal universal question is: “Are all PCF maps defined over their field of moduli?” The partial odd-postcritical criterion in the imported title is not a hypothesis.

[Silverman, *The field of definition for dynamical systems on P1*, Compositio Mathematica 98(1995),269–304](https://www.numdam.org/item/CM_1995__98_3_269_0/), Introduction printed p.271 equation(1), explicitly displays
\[
 f_3(z)=i\left(\frac{z-1}{z+1}\right)^3.
\]
The Example printed p.296 extends it to all odd d≥3 and states exact field of moduli Q and a nontrivial obstruction. The no-real-model consequence is stated in the Introduction and follows from the norm criterion on pp.296–297. The official primary PDF was retrieved independently (3,149,856bytes), and printed pp.271,295,296,297 were visually inspected because the text extractor omitted important equations.

The source does not explicitly call this family PCF. The independent artifact `INDEPENDENT_SILVERMAN_SOURCE_CONSEQUENCE.md` proves the missing PCF property and re-proves every required descent assertion without relying on an unread cohomological theorem:

- The homogeneous formula `[i(X−Y)^d:(X+Y)^d]` has degree d with exactly two critical points ±1, each local degree d.
- For d=3, the exact critical orbit is
  \[
  1\to0\to-i\to-1\to\infty\to i\to1.
  \]
  For all odd d, the same six-point set is invariant; d=1mod4 gives two 3-cycles and d=3mod4 gives this 6-cycle. All critical points are periodic, so the map is PCF.
- Every holomorphic automorphism permutes ±1 and their two images 0,infinity. If it fixes them, it is identity; if it swaps them, it must be T(z)=−1/z. This T fails commutation at infinity for odd d. Therefore Aut(f_d)=1.
- Complex conjugation sends f_d to T f_d T^−1. Because the coefficients lie in Q(i), every element of Gal(Qbar/Q) preserves the class, so the absolute field of moduli is exactly Q.
- A(z)=−1/bar(z) is its unique antiholomorphic automorphism. It is fixed-point-free. A real model would produce a commuting antiholomorphic reflection with a fixed circle, contradicting uniqueness. Thus there is no real model, in particular no Q-model.

This covers PCF, algebraicity, the exact absolute field of moduli, and failure to descend. There is no limiting, numerical, graph-realization, flexible-Lattès or real-versus-totally-real gap. Degree3 already suffices to disprove the full universal claim.

## What the priority conclusion means

The exact universal negative outcome is a **fully proved elementary source consequence** of an explicit 1995 construction. This audit does not claim to have identified the first paper or person who noticed its PCF property, nor an old theorem literally phrased as a negative answer to this AIM question. Those historical recognition questions remain bounded search gaps; they do not revive novelty for the universal conclusion obtainable from the old map.

The original upstream report's caution that general Silverman counterexamples need a separate PCF check was appropriate, but its statement that no verified PCF counterexample was found is superseded by the six-point computation above. It is unnecessary to invoke a general theorem asserting that all pseudo-real maps are PCF, which would be false.

The original candidate's exact degree11 critically fixed graph is a narrower construction claim. Nothing in the old bicritical example establishes its prior exact appearance. That example has two critical points on nontrivial cycles and is not critically fixed. An exact-degree11 or critically-fixed contribution would require separately scoped novelty evaluation and cannot inherit the claim of a new answer to universal AIM2.6.

## Earlier arithmetic and pseudo-real sources

[Hidalgo–Quispe, *On Real and Pseudo-Real Rational Maps*](https://arxiv.org/abs/1502.05306) current v4, posted7July2021, Sections2.5 and4–5, was read through the operative proofs and explicit examples. Lemmas4–5 relate reflections/real models and antiholomorphic symmetries/real fields of moduli; Theorem6 gives the trivial-automorphism pseudo-real criterion. Its Section5.1 printed p.20 reproduces the precise Silverman family. This confirms attribution, but the decisive source remains1995. Theorem8/Example2 degree13 and Theorem9 quotient constructions are general pseudo-real families; their PCF property is not established simply by those statements. Theorem11's real examples with field-of-moduli obstruction are a separate arithmetic phenomenon. No PCF conclusion for that family was used.

The v1 PDF endpoint returned406. Literal arXiv history records v1 on18February2015, v2 on3October2017, v3 on10February2021, v4 on7July2021. No v4-specific assertion is backdated to2015 without reading that version. Its references lead to Milnor2000, Goodman–Hawkins2014, Hidalgo2014 and other prior symmetry/descent work.

[Milnor, *On Rational Maps with Two Critical Points*](https://arxiv.org/abs/math/9709226), v3 posted26May1999 (journal2000), complete Section5 including Lemma5.1's proof, was checked. It treats the antipode-preserving region of bicritical moduli and antiholomorphic involutions. The depicted attracting examples are approximate parameters; no exact PCF/FOM obstruction is inferred from those pictures. Goodman–Hawkins2014 is a recorded bounded unread lead: the primary AMS PDF returned403. No outreach was attempted.

## Earlier graph classification and examples

[Cordwell–Gilbertson–Nuechterlein–Pilgrim–Pinella, *On the classification of critically fixed rational maps*](https://arxiv.org/abs/1308.5895), arXivv1 posted27August2013, journal2015, was checked in the introduction, complete Section7.3 (realization/naturality and graph-injectivity proof), complete Section9 (Tischler graph and inverse), and complete Section11 worked examples. The source explicitly uses orientation-preserving graph isomorphisms; connected blown-up graphs realize critically fixed maps with degree edge-count+1. Thus the realization machinery already existed, even while general surjectivity remained open there. The worked examples reach degree6, with exact expressions in several smaller cases and numerical expressions in others. No exact FOM counterexample statement or this degree11 decorated graph was located in the inspected material. This is bounded negative evidence, not an exhaustive novelty certificate. The endpoint for the current journal metadata returned403. The embedded PDF compile date23September2018 is not treated as a first-publication date; literal arXiv history has one2013version.

[Hlushchanka, *Tischler graphs of critically fixed rational maps and their applications*](https://arxiv.org/abs/1904.04759), archivedv1 posted9April2019, was independently retrieved and its operative classification proof read: Theorem2, orientation convention, complete Sections4–5, Corollary6, Proposition7 and Lemma8 (v1 numbering). The charge-graph construction and natural inverse already occur in this earlier version, rather than first appearing in2025v2. Its Section3 concrete example has real coefficients. The source supplies established mechanisms relevant to PR36; it does not by itself state the proposed decorated degree11 field-of-moduli obstruction. Again, no universal novelty can survive the independent Silverman counterexample regardless of this narrower graph search gap.

## BBM warning and later arithmetic status

[Bonifant–Buff–Milnor, *Antipode Preserving Cubic Maps: the Fjord Theorem*](https://arxiv.org/abs/1512.01850), v1 posted6December2015, introduction and Lemmas2.3–2.4 with their displayed proofs were checked. The primary source genuinely asserts unique critically finite centers of hyperbolic components, using earlier Milnor results. Its displayed near q≈0.394−2.24i or q≈0.1476−1.927i pictures alone do not verify exact PCF parameters or exclude all reflecting symmetries. No statement of a fully exact BBM-center FOM counterexample is imported here; the dependency proofs and exact center algebraicity/symmetry would need their own audit. This remains a plausible warning/source-consequence route, while the Silverman family already settles the universal priority gate.

[arXiv2405.03612](https://arxiv.org/abs/2405.03612) is **withdrawn**, with v1 posted6May2024 and v2 withdrawal9May2024. The author reports a confusion between equality of ramification degrees and equality of vanishing orders. No theorem of that withdrawn paper is established input. [Bresciani, *Uniform bounds for fields of definition in projective spaces*, arXiv2405.03621v1](https://arxiv.org/abs/2405.03621), also posted6May2024, is a distinct eight-page preprint read completely for scope. Its claimed bounded extension degree is not the assertion that every PCF map descends over its field of moduli. This audit neither substitutes it for the withdrawn characterization nor certifies all of its external dependencies.

The live AIM page was independently retrieved by default urllib: HTTP200,33,521bytes,SHA256 `990076ea9a8b9a23c9a6a34e6686eda087be82cd616c02d743e996a9c1e7d178`. It repeats the universal problem2.6 without an added odd-cardinality hypothesis. A live unresolved-looking page is not proof of mathematical novelty.

## Computation, controls and closure

`verify_silverman.py` uses only exact Gaussian-integer projective evaluations and exact polynomial coefficients. The actual run checks odd degrees3,5,7,9,11,13,15, both orbit types, Wronskians and the conjugation identity. The all-odd-degree result is proved by the two residue classes modulo4 in the sealed proof, not extrapolated from the finite checks.

Six actual negative/positive controls reject: even degrees2,4,6; removal of i (a real map with extra holomorphic T); a false critically-fixed claim; and a corrupted cubic orbit row. `CONTROL_SETUP_CORRECTION.json` preserves an initial failed control design. The real-coefficient mutant commutes with both an antipode and a reflection because it has a nontrivial holomorphic symmetry; expecting antipode noncommutation was incorrect. The corrected test rejects the required trivial-automorphism premise. This does not affect the old map's proof.

`SOURCE_READING_LEDGER.json`, primary/date retrieval receipts, scope and assessment seals, exact-check results, and the authored closure manifest bind the audit. Downloaded foreign PDFs/HTML/text/rendered pages remain under ignored `tmp/foreign_sources` and are excluded from authored closure. Only this assigned family folder was written. Main was retained; no queue/state/history mutation, remote change, preprint, release, DOI or external message was made.

**Strongest verified result:** an explicit degree3 PCF map over Q(i), already printed1995, has exact absolute field of moduli Q and no real model. **Exact remaining priority gap:** earliest explicit recognition of its PCF consequence and narrower exact-degree11/critically-fixed graph priority; these do not affect `PRIOR_APPLICATION` for universal AIM2.6.
