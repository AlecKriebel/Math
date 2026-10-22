# Independent priority audit: PR #1102 / problem 30006658

Audit date: 17 October 2026. This is a bounded current-literature and primary-source audit, not a proof of universal priority. No external communication was attempted. No other PR was reviewed. Mathematical correctness is the responsibility of the separate independent proof audits.

## Disposition

**PASS for proceeding to a carefully attributed research note, subject to the mathematical and final-package audits. No prior full resolution was located. Do not mark this problem `already_solved` on the evidence found here.**

The supported contribution is the affirmative answer to Greenlees's stated question for positive-dimensional compact Lie groups, by a short synthesis of established theorems. The finite-group case, the finite-ideal theorem, compact-proxy Morita theory, and filtered approximation are prior mathematics. A paper claiming any of these ingredients as a new method would fail this audit. A paper giving the full consequence, proving the connection, and clearly crediting those ingredients is supported by this search. This audit does not establish that no unpublished or unindexed proof exists.

## Exact target and originating source

Let p be prime, k a characteristic-p field, G a compact Lie group, and

\[
 R=C_*(\Omega((BG)^\wedge_p);k).
\]

The target is

\[
 \pi_0G\text{ not p-nilpotent}\quad\Longrightarrow\quad
 \pi_*(\Gamma_kR\longrightarrow R)=0
\]

in every degree. It is a statement about the induced homotopy map, not derived nullity. Completing BG before looping is essential.

The [official Oberwolfach source](https://ems.press/content/serial-article-files/53607?nt=1), Greenlees's contribution pp. 592–595, has this question at Question 2.2, printed p. 594 / zero-based PDF page 53. Its literal question assumes positive dimension and the displayed component-group condition. The surrounding discussion first uses adjoint orientability to identify a shifted dual, while the question itself does not repeat that hypothesis. The proposed theorem answers the literal question and also covers the orientable contextual reading. The coefficient field and completion convention are established in the contribution's opening context and §1.3. No reversal of the component-group hypothesis, mistaken cochain/chain algebra, or nullity requirement was found. The question is genuinely posed there; it is not merely an example or a request for an already stated corollary.

The report describes the workshop of 22–27 February 2026. The date of the workshop alone does not establish continued openness in October; the later article and current search below are therefore necessary.

## Current Greenlees article

The [live arXiv abstract](https://arxiv.org/abs/2504.03050) identifies v3, 27 April 2026, as the latest version. The fetched [versioned PDF](https://arxiv.org/pdf/2504.03050v3) has 385127 bytes and SHA256 `9ca43feae410f109e1e62a2de184a897b30f8966c4b90b7f28e90cf3dcd10eae`, agreeing with the earlier recorded copy. All of §6 and the relevant proxy/duality sections were independently read.

The [published article](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/blms.70405) is *Bulletin of the London Mathematical Society* 58(6) (2026), e70405. The publisher page gives 1 June 2026 as first publication. Current [publisher-deposited Crossref metadata](https://api.crossref.org/works/10.1112/blms.70405) includes publication-history assertions for receipt on 18 December 2025, acceptance on 3 May 2026, and publication on 1 June 2026. The metadata's receipt date should not be confused with the April 2025 first arXiv posting.

Direct web-tool access to Wiley HTML failed, and a direct epdf request returned HTTP 403. A background browser successfully displayed the full published HTML. Its §6 was independently inspected, including formulas after bringing the relevant sections into view. The current publication retains the restricted claims described in the matrix. No byte-equivalence between publisher and arXiv PDFs is asserted; no publisher PDF was obtained. This access limitation does not leave the published theorem statements uninspected.

## Comparison matrix

| Primary source and locator | Established scope/mechanism | Relation to the candidate |
|---|---|---|
| Greenlees arXiv v3 §6.A; published §6.1 | The norm analysis is introduced under adjoint k-orientability. | Candidate uses no untwisted duality identification and removes that hypothesis. |
| Greenlees v3/published Lemma 6.2 | Finite G: homotopy norm is an isomorphism in the p-nilpotent case and zero otherwise. | Entire finite-group portion is old; do not count it as the new result. |
| Greenlees v3/published Lemma 6.3 | Connected compact Lie groups give an equivalence. | Outside the target antecedent, since their component group is trivial. |
| Greenlees v3 §6.E / published §6.5, Lemma 6.5(ii) | Nilpotent component-group action; in the non-p-nilpotent case, vanishing on a specified generated submodule, plus zero after projection to the completed component-group loop homology. | Neither clause says the whole map vanishes. The omitted submodule/image gap is precisely not filled by quoting this lemma. |
| Greenlees v3/published Remark 6.6 | Full vanishing under the displayed tensor-product collapse hypothesis. | A known restricted full answer. The candidate does not establish or assume that collapse. |
| Benson, *An algebraic model for chains on ΩBG∧p*, Trans. AMS 361(4) (2009), 2225–2242, Theorems 1.1–1.2 and §§3–7; [official PDF](https://www.ams.org/journals/tran/2009-361-04/S0002-9947-08-04728-4/S0002-9947-08-04728-4.pdf) | Squeezed resolutions and their algebraic/topological interpretation for finite groups. | Prior finite-group mechanism; no arbitrary positive-dimensional compact-Lie norm theorem found. Greenlees §7 explicitly retains finite G. |
| Dwyer–Greenlees–Iyengar (2006), Definition 4.6, Theorem 4.9, Proposition 4.17, §4.22, §5.7; [publisher-version mirror](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/dwgriy.pdf) | Compact proxies, effective construction and proxy-smallness for completed loop chains of every compact Lie group over Fp. | Supplies the full topological finiteness machinery. It does not itself state the target's vanishing conclusion. The extension of the compact proxy to k is routine scalar extension, not a new finiteness theorem. |
| Briggs–Iyengar–Stevenson, NYJM 31 (2025), 701–721, Definition 2.1/Ind-completion/Remark 2.3 at p. 703 and Lemma 4.1 proof at p. 709; [published PDF](https://nyjm.albany.edu/j/2025/31-26p.pdf) | Localizing categories generated by compact proxies are Ind-completions; the proof explicitly writes an E-module as a filtered homotopy colimit of perfect objects and tensors the diagram. | Prior source for the candidate's approximation mechanism. This belongs in the paper's principal bibliography, not only a buried supplemental note. No Hopf/no-finite-ideal norm-vanishing theorem occurs in the inspected paper. |
| Lomp, *Integrals in Hopf algebras over rings*, §2.4, [primary manuscript](https://arxiv.org/pdf/math/0307046) | A nonzero finite-dimensional one-sided ideal forces an ordinary field Hopf algebra to be finite-dimensional; credited to Sweedler. | Candidate's ungraded finite-ideal lemma and its coefficient-space/Hopf-module proof are classical. Their full proof is useful for checking conventions, not grounds for a novelty claim. |
| Sweedler, *Integrals for Hopf algebras*, Ann. Math. (2) 89 (1969), 323–335, Corollary 2.7; [journal metadata](https://annals.math.princeton.edu/1969/89-2/p07); Cuadra's [primary research manuscript](https://w3.ual.es/personal/jcdiaz/invest/public/segalois5.pdf), proof of main theorem | Cuadra explicitly invokes Sweedler Corollary 2.7 to pass from a finite-dimensional left ideal to finite dimension. | Corroborates original priority and exact locator for the algebraic fact. The original Sweedler body was not obtained; Lomp and Cuadra were inspected. Do not say the original proof was directly checked. |
| Ishiguro (2007), Proposition 1.3(a), printed p. 199; [official PDF](https://msp.org/gtm/2007/10/gtm-2007-10-011p.pdf) | p-compactness of BG requires p-nilpotence of π0G; explicitly restates the author's 2001 Proposition 3.1. | Entire infinite-total-homology input is old. Only the necessary direction is needed. Original 2001 body was not separately inspected. |
| Davis–Greenlees, *Gorenstein duality and universal coefficient theorems*, [arXiv:2206.11391v2](https://arxiv.org/pdf/2206.11391v2), §5.E Lemma 5.7/Remark 5.8 | In its commutative/algebraic-cellularization setting, cellular homotopy is torsion; over a finite field this is locally finite. | Close antecedent to a locally-finite-image argument, but its algebraic-cellularization hypothesis is not proved for unrestricted completed loop chains. Treating it as universal would transfer the central difficulty to an unsupported hypothesis. |
| Raksit, *Hochschild homology and the derived de Rham complex revisited*, Selecta Math. 32 (2026), 61, [§2.4](https://link.springer.com/article/10.1007/s00029-026-01154-w) | A norm/Tate construction for dualizable bialgebra objects with a stipulated invertible duality twist. | A contemporary general-norm search candidate, not the target theorem. In D(k), the target loop algebra has infinite total homology and is not k-dualizable. Its hypotheses do not directly imply the unrestricted result. |

The parity-bosonization passage is standard graded-Hopf technology. It avoids a sign error in applying an ordinary theorem, but should not be advertised as a new construction. The broader vanishing criterion in the report is a useful elementary consequence of the two classical mechanisms. No source was located stating that exact combined criterion; absence of a located formulation is not evidence of a new general theory.

## What is added beyond the sources

The checkable connecting observation is as follows. A compact proxy lets every individual cellular homotopy class be represented through a module with finite-dimensional total homotopy. Under an A-linear map to the regular module, its homotopy image is a finite-dimensional graded one-sided ideal. Sweedler's theorem rules out such an image when the homotopy Hopf algebra is infinite-dimensional. DGI and Ishiguro verify these hypotheses for the target loop algebra.

No single inspected prior theorem states the unrestricted answer, and the known restricted theorem does not imply it by deletion of its hypotheses. The candidate supplies this connecting argument. All mathematical input theorems predate the question; that is compatible with a new consequence answering the question, but limits how its novelty should be presented. The proposition is not an independent new theorem of Hopf algebra or category theory merely because its proof is reproduced in a new paper.

## Source defects and safeguards

1. The OWR and Greenlees-v3 bibliography labels Benson's volume 361 article with year 2008. The official article gives the issue date April **2009**, while electronic publication occurred on 19 November 2008. Use the ordinary journal citation 361 (2009), 2225–2242 and, if needed, record the electronic date separately.
2. In both v3 and the live published Lemma 6.2 proof, the displayed sentence includes an apparent equality between kΠ and the entire completed loop-chain algebra. The surrounding comparison only requires the degree-zero quotient. The equality is not valid for general non-p-nilpotent finite G. The independent proof must not import it; its own argument correctly keeps completion and all homological degrees.
3. The context also uses a degree-zero-is-k assertion across its stated ring cases. For loop chains, the correct general degree-zero algebra is k[π1((BG)∧p)], which need not be k. This is another reason not to replace the independent proof by a scalar-determination argument copied from that paragraph. This observation does not challenge the independently proved target or turn Lemma 6.5 into a full theorem.
4. The original question appears within a duality discussion. The paper should state explicitly why it can dispense with orientability rather than silently identifying cellularization with a shifted untwisted dual.

These are source-precision controls, not a request to contact the author or prepare outreach.

## Publication wording supported by this audit

Recommended abstract/introduction wording:

> We give an affirmative answer to Question 2.2 of Greenlees concerning the homotopy of the cellularization map for completed classifying spaces. If G is a compact Lie group whose component group is not p-nilpotent, this map is zero in every degree over every field of characteristic p. The proof combines compact-proxy approximation with the classical finite-ideal theorem for Hopf algebras.

Recommended priority sentence:

> The finite-group case and the compact-Lie cases subject to nilpotent-action or tensor-collapse hypotheses were established by Greenlees. Our argument gives the unrestricted vanishing conclusion without using those additional hypotheses.

Do not claim a first-ever proof, exhaustive novelty certification, an unexplained new method, a new finite-ideal theorem, new filtered-colimit machinery, derived nullity, or resolution over arbitrary coefficient rings. The paper may decisively prove and answer the exact mathematical question while making modest claims about priority. The AI-use and unrefereed-status disclosure should remain explicit.

## Residual uncertainty and falsifiable reopening criteria

The priority recommendation is based on inspected primary texts, current version checks and the dated queries in QUERY_LEDGER.json. It is not based on search ranking alone. A result would defeat the novelty conclusion if it states the same unrestricted homotopy vanishing for this algebra, or gives a more general published vanishing theorem whose hypotheses are already known for all these groups without supplying the candidate's connecting argument. No such result was found.

Unindexed manuscripts, unpublished knowledge, and omitted literature remain possible. The Greenlees personal bibliography currently linked from his homepage is a 2025 document and is stale for current-status purposes; it cannot certify October 2026 openness. Original Sweedler 1969 and Ishiguro 2001 bodies remain uninspected, but their ingredients are affirmatively credited, not presented as novel. There is no evidence here of a priority defeat requiring reclassification or abandonment. Outside expert input could improve assurance; under the independent-research policy no outreach is prepared or initiated.

Audit completion: **100% of this assigned bounded priority audit**, with the limitations above. This is not a percentage probability of universal priority.
