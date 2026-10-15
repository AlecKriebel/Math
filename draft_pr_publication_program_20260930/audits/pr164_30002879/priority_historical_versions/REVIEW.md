# PR164 historical versions priority audit

**Disposition: the full ordinary Gerstenhaber result has an explicit prior public equivalent. It should not be promoted as a novel solution of the target.** Long–Shi–Zhou, arXiv:2609.19560v1, dated 17 September 2026, gives the full cup product and bracket for the same characteristic-two seven-dimensional algebra. Its presentation is exactly equivalent to the current candidate, as verified below. This predates the original 30 September 2026 disclosure. The ordinary Lie target is distinct from any additional strict squaring or higher-brace structure.

The narrower historical finding is more nuanced: Xu 2008 gives the ring of the exact example; Hermann's 2014 and 2016 arXiv versions give the ambient bracket, the structure-preserving maps, and a general theorem whose special case is exactly this one-point extension and already proves injectivity. I did not locate an explicit full Lie presentation of the example in those four old arXiv texts. The normalized characteristic image is an unstated short consequence of the machinery and a coordinate calculation. Ingredients alone are not treated as an explicitly published answer to Hermann Question 5.

## Boundaries, provenance, and independent assessment

The audit fixes the current candidate at SHA256 `db79e3c12fb044df91934137dcacd9473460eedefc6f9043e682986c96c0e66b`; the immutable original proof is SHA256 `439bb5ac541dcc7cb0e6fbf5b30a22501f23f330b4f970fe641fb54234bd46be` at original head `7c8acab3ff84c6c8caadec8998296936a156e0bd`. The original proof was hashed; the mathematical target used here is the corrected candidate explicitly supplied for this audit. INPUTS.json identifies all allowed external workspace inputs and what was read.

FIRST_ASSESSMENT.md and FIRST_ASSESSMENT_SEAL.json were sealed mode 0444 at 2026-10-12T09:49:17.798006+00:00, before receiving or reading any parent/sibling priority conclusion. The first assessment was confined to Xu/Hermann/OWR primary texts and recorded a VOR gap. Only after the seal did the root task provide the primary locator for Long–Shi–Zhou. No root/sibling verdict was consulted; the new paper was downloaded directly and its mathematical content assessed afresh. The first files remain unchanged. This makes the change from a historical direct-consequence assessment to explicit prior overlap traceable.

This is a priority audit, not a certification of global literature absence, researcher independence, plagiarism, journal peer review, or every line of the candidate proof. No outside individual was contacted or any outreach prepared. No Git, PR, main-branch, remote, release, Zenodo, index, or spreadsheet mutation was performed. Third-party full texts, extracted text, diffs, renderings, and transient material are confined to private/.

## Claim and source question

For any field K of characteristic two, let A=K[x,y]/(x²,y²), M=A/(y), and B=[[A,M],[0,K]]. The proposed answer identifies HH*(B), including its cup product and degree-minus-one ordinary Gerstenhaber bracket, with

\[
L=K\cdot1+(y,u)R,\qquad R=K[x,y,u,v]/(x^2,y^2),\quad |x|=|y|=0,\ |u|=|v|=1,
\]

\[
[F,G]=F_xG_u+F_uG_x+F_yG_v+F_vG_y.
\]

Here u=partial_x and v=partial_y. The original coefficient map gamma induced by B→B/BeB=A is injective, has image L, and preserves the bracket. This includes degree zero, the nontrivial permutation module, the precise image and all brackets; dimensions alone do not meet the success criterion.

The original OWR primary source is Report 24/2015, workshop 3–9 May 2015; Crossref gives print publication 15 February 2016. Question 5 is on printed p1363, PDF p47. Lemma 4 on the same page already identifies the coefficient map with the derived quotient map and states preservation of product and bracket. Its question asks for the precise Lie algebra and whether the displayed coefficient sequence can determine it. The year in the report label and the print publication year are different facts.

## Xu versions: what is prior and what is not explicit

Both [Xu v1](https://arxiv.org/pdf/0805.3295v1) (21 May 2008) and [Xu v2](https://arxiv.org/pdf/0805.3295v2) (29 July 2008) were acquired in full, 20 PDF pages each. Section 2.1 defines the tensor-induced characteristic homomorphism. Lemma 2.4.1 and Theorem 2.4.2, PDF p13 in both versions, compare coefficient maps and corner restrictions. Section 3.1 computes the exact EI-category E0 and its Hochschild ring: v1 pp14–16, v2 pp15–17, with the final decomposition on p16 in both. The action fixes h and interchanges the two arrows by g; in x=g−1,y=h−1 coordinates it is the nontrivial module A/(y).

The nilpotent coefficient summands are represented by 1+h=y, g+gh=(1+x)y, and 1+g=x. The first two support full group-cohomology polynomials; the x summand supports the positive ordinary-category subring. The ordinary summand is already included. Xu v2 adds a polynomial-subring description of that ordinary cohomology directly in Section 3.1; v1 refers to the earlier ordinary-cohomology paper instead. Those are genuine prior ring computations, not merely a non-finite-generation statement. The positive-degree dimensions 4n+2 and degree-zero dimension 3 follow from the decomposition.

Care is needed with coordinates: Xu's ordinary-cohomology indeterminates are not automatically the candidate's partial_x and partial_y. Group degree-one cocycles correspond to (1+x)partial_x and (1+y)partial_y. These factors are units, so the relevant retained ideal agrees with the candidate's ideal after correctly identifying the annihilator/regular directions. Likewise, Xu's map phi_E0 onto ordinary cohomology is not the original coefficient gamma onto HH*(A). Treating them as the same without his compatible corner diagram would skip a necessary identification.

The old ring presentation and compatible restriction descriptions make L a short reconstruction; they do not print the complete bracket of HH*(B). A complete-file keyword and statement inventory plus close reading of all relevant sections found no such explicit full Lie table or formal-Poisson subalgebra presentation in the two Xu versions. The audit did not infer absence merely from abstracts or titles.

## Hermann versions: a closer disguised theorem

[Hermann v1](https://arxiv.org/pdf/1411.0836v1), submitted 4 November 2014, is 45 pages. [V2](https://arxiv.org/pdf/1411.0836v2), submitted 2 June 2016, is 47 pages. The arXiv history records v2 as final/to appear and says Section 9 was rearranged and fixed. Both complete texts were acquired. Proposition 6.12 is on p31 in both versions. **Corollary 6.17 is already in v1 p32 and persists in v2 p33.** This is important prior art that the candidate's credit to Proposition 6.12 alone understates.

Take D=K[t]/(t²), U=D^ev=K[a,b]/(a²,b²), with diagonal bimodule D: both a and b act by t. Set x=a and y=a+b. This invertible characteristic-two change gives U≅K[x,y]/(x²,y²), and D≅U/(y). Therefore Hermann's exact upper triangular algebra U[D] is B, not just a loosely related example. Corollary 6.17 supplies, for every n≥1,

\[
0\longrightarrow HH^n(B)\longrightarrow HH^n(U)\longrightarrow HH^n(D)\longrightarrow0,
\]

and the corner map is a strict Gerstenhaber homomorphism. Thus positive-degree injectivity and characteristic-map surjectivity are prior theorem special cases. No appeal to an unsupported finiteness or vanishing condition is needed. The displayed center sequence similarly gives injectivity of projection to U in degree zero: a central pair (a,c) has a mod y=c, so its image is K+yA.

The group generator h−1 in the source may be (a+b)(1+a) rather than a+b, depending on whether the generators of C2×C2 are chosen as the two tensor factors or a regular generator and their product. This is an invertible algebra change and both annihilate the module. It does not alter the exact algebra. It must not be silently identified with the two-dimensional trivial module.

The characteristic coordinates chi(x)=x, chi(y)=0, chi(u)=0, chi(v)=eta are not explicitly listed for this example in the old papers checked. They follow by tensoring the elementary two-variable bimodule resolution with M and comparing the one-variable y-resolution. This is a short all-degree coordinate computation, not a new injection theorem. In particular, chi is a cup-algebra homomorphism; it is not a Gerstenhaber homomorphism to a bracket on Ext: chi([v,y])=1 while chi(y)=0. The distinction in Hermann's statement—g preserves the Gerstenhaber structure, h is stated as a graded algebra map—must be retained.

For the original coefficient sequence, Theorem 8.11 and its proof (v1 pp40–41; v2 pp41–42) already identify its map with the derived quotient map and establish bracket preservation. V2 Corollary 8.15, p43, specializes to triangular matrices and the exact coefficient sequence in question. On E=Kf+Ke relative cochains, both this map and the A-corner component of g are restriction to all-A inputs followed by A-output projection. With coefficients A all mixed/corner-output components vanish. Since E is separable, this computes ordinary Hochschild cohomology. Consequently the canonical-map identification needed to transfer Corollary 6.17's injectivity to gamma is routine and already sits inside prior map machinery. This audit does not find a substantive new target theorem remaining in the candidate's gamma/use-of-sequence claim.

Hermann's ambient elementary-abelian-group bracket is in v1 9.2 p42 and v2 9.3–9.4 pp44–45. V1 contains a visibly contradictory extra mixed-zero bracket term and different claims about nilpotent-generated Gerstenhaber ideals. V2 removes the extra mixed-zero term, separates weak and strong ideal notions, and changes the quotient conclusions. Neither version's Section 9 gives the full bracket for E0; both conclude with future-work quotient questions. The v1 errors and the further squaring statements are not used here. The category multiplication/orientation in 9.6/Lemma 9.7 also needs the opposite-algebra correction already made in the candidate; characteristic two removes reversal signs for the ordinary structures at issue.

## Published versions: exact acquisition gap

The publisher citation for Hermann spans journal pp687–759, 73 inclusive pages; the arXiv v2 file has 47 pages. Xu's journal citation spans pp1872–1893, 22 inclusive pages; each arXiv version has 20. Page-count differences can be typesetting, but they cannot establish identical text. No exact correspondence of sections/pages with either VOR is certified.

The publisher metadata XML reports cover dates 20 August 2016 for Hermann and 20 December 2008 for Xu. Default Elsevier API responses contain bibliographic coredata only, despite a full-text-retrieval response wrapper. ScienceDirect article and PDF requests returned HTTP403; explicit API FULL XML/plain/PDF requests returned HTTP401. Later PDF attempts without FULL returned HTTP429, and were not repeatedly retried. HAL returned challenge HTML rather than a PDF. The Xu ordinary-cohomology citation follow-up located a repository record, but its attempted PDF download returned HTTP404. These bodies/errors and fetch timestamps are preserved privately with metadata in FETCH_RECORDS.json. No full VOR was read. Hence absence of an additional VOR solution remains unproved. The gap no longer blocks the overall priority disposition because the separate explicit prior source below suffices.

## Post-seal explicit prior solution and exact equivalence

[Long–Shi–Zhou v1](https://arxiv.org/pdf/2609.19560v1) is the full 44-page *Gerstenhaber algebra structure on the Hochschild cohomology ring of the Xu–Snashall algebra*. Its [arXiv version record](https://arxiv.org/abs/2609.19560v1) reports v1 submitted 17 September 2026 at 01:41:24 UTC; the PDF has the same dated arXiv stamp. The record calls it a detailed version of a submitted paper. This audit does not equate that submission timestamp with an independently captured announcement instant or assert journal peer review. The dated version precedes the 30 September original disclosure, and is also prior to the current 12 October audit. No later version is needed for the overlap.

The exact algebra is shown on PDF p2 and defined again in Section 3, p11: two square-zero commuting loops a,b at vertex1 and an arrow c to vertex2, with ac=0. Lemma 3.1 gives the seven basis elements e1,e2,a,b,c,ba,bc. Under the paper's path product convention, set

\[
a\mapsto y\in A,\quad b\mapsto x\in A,\quad c\mapsto1\in M.
\]

Then ac=0 is yM=0, and bc maps to x in M. The corner loop algebra is A, and the other corner is K. This is the exact B for arbitrary K of characteristic two. If a reversed path convention is used, take the opposite before comparing; the target ordinary structures have the same characteristic-two comparison. The actual source conventions and basis already give the direct identification.

Theorem 7.1 (PDF pp32–34) supplies a countable homogeneous-generator ring presentation; Theorem 8.3 (p41) specifies all generator brackets and asserts the full Gerstenhaber algebra. To avoid mistaking a notation match for an isomorphism, define the following explicit map, with the left side denoting their generators:

| Prior generator | Image in L | Index range |
|---|---|---|
| X_n,1 | Y_n=yv^n | n≥0 |
| X_n,2 | Z_n=xyv^n | n≥0 |
| X_n,3 | P_n=uv^(n−1) | n≥1 |
| X_n,4 | Q_n=xuv^(n−1) | n≥1 |

All degree-zero cases are included. The unit maps to 1. Their Section 4 coefficients have z3=a=y,z4=b=x,z6=ba=xy. Their Section 5 comparison sends the pure-loop resolution generators to the signed shuffle; in characteristic two this is the same shuffle comparison used in the candidate. Thus this map has the expected canonical corner interpretation, in addition to being an abstract algebra isomorphism.

**All-degree ring verification.** Substitute these four monomials into the relations of Theorem 7.1. The zero products follow from y²=x²=0. Relations comparing products of the P and Q families compare identical monomials. The source's displayed normal basis maps to 1; Y_n,Z_n; P_n,Q_n; yu^(l+1)v^(n−1), xyu^(l+1)v^(n−1); and u^(l+2)v^(n−1), xu^(l+2)v^(n−1), with n≥1,l≥0 where applicable. These are distinct and exhaust precisely the monomial basis of K+(y,u)R. This proves both surjectivity and injectivity in every degree over every characteristic-two field, independently of numerical matching.

**All-degree bracket verification.** Write s=m+n−1 and take m,n≥1. Formal differentiation gives:

| Pair | Bracket |
|---|---|
| Y_m,Y_n | (m+n)Y_s |
| Y_m,Z_n | (m+n)Z_s |
| Y_m,P_n | (n−1)P_s |
| Y_m,Q_n | (n−1)Q_s |
| Z_m,Z_n | 0 |
| Z_m,P_n | Y_s+(n−1)Q_s |
| Z_m,Q_n | Z_s |
| P_m,P_n | 0 |
| Q_m,P_n | P_s |
| Q_m,Q_n | 0 |

Coefficients reduce modulo two, giving exactly the parity cases in Theorem 8.3. For degree zero, differentiating against y gives mY_(m−1), mZ_(m−1), (m−1)P_(m−1), (m−1)Q_(m−1) respectively. Differentiating against xy gives mZ_(m−1), 0, Y_(m−1)+(m−1)Q_(m−1), Z_(m−1) respectively. Terms with the undefined P_0 or Q_0 have coefficient zero and disappear; m=1 is therefore covered without an exception hidden in notation. Degree-zero pairs bracket to zero and the unit brackets to zero. This is the entire source table. Since both sides obey the Gerstenhaber biderivation rule and these families generate the rings, the bracket agreement extends to every element, not only to generators or low degrees.

The own-code diagnostic compare_presentations.py additionally checked 1,515 ring-relation instances, 1,536 bracket-relation instances, and normal-basis equality/injectivity through degree12, using exact F2 arithmetic. COMPARISON_CHECK.json records PASS. This is a bounded error-detection check; the preceding algebraic argument establishes all degrees and arbitrary characteristic-two fields.

## Weak versus strong quotients

Long–Shi–Zhou Definition 8.5/Theorem 8.6 (PDF p42), inspected visually, keeps the weak condition [G,G]⊆G distinct from the strong condition [HH*,G]⊆G. The weak nilpotent-generated ideal equals the cup nilpotent ideal, so its quotient is not finitely generated. The strong Gerstenhaber-ideal quotient is K. Those are extra results; neither is a substitute for the full bracket theorem.

This distinction is consistent with L itself. The cup nilpotent ideal is L∩(x,y)R. Its quotient is K+uK[u,v], which has infinitely many independent degree-graded generators uv^j. It is a Lie subalgebra ideal for the cup product, but not a strong Lie ideal: xu is nilpotent and [xu,u]=u. Thus the strong closure contains all P_n through [Q_n,P_1]=P_n; together with the nilpotent families, it contains every nonconstant basis monomial and leaves precisely K. This is a falsifiable consistency check, not a reinterpretation of the target as a quotient question.

## Final classification and remaining gap

- **Exact full ordinary Gerstenhaber answer:** explicitly prior in Long–Shi–Zhou Theorems 7.1/8.3, with the checkable isomorphism above. This defeats a novelty claim both at the original disclosure and at the audit date.
- **Earlier exact ring:** explicit prior in Xu Section 3.1; full bracket not located in the two old versions checked.
- **Injection and map preservation:** Hermann Corollary 6.17 already gives injection/surjectivity for a disguised exact special case in 2014; Theorem 8.11/OWR Lemma 4 supply original coefficient-map machinery. The normalized coordinate chi/image calculation and explicit identification of gamma are short consequences, not a demonstrated additional new research theorem.
- **Candidate's concise Poisson presentation and chain proof:** can be a useful exposition/rederivation with correct citations. A new proof route or normalized coordinates do not make the already explicitly computed target result novel.
- **Unresolved acquisition:** neither old VOR was acquired; no global absence, exact old-VOR equivalence, or author-independence conclusion follows. The disposition does not depend on resolving those gaps.

The historical family mechanism, source dates, locators, access limitations, and post-seal change are preserved in SOURCE_LOCATORS.json, VERSION_COMPARISON.md, RESULT.json, and research_log.md. Public allowlisting is restricted to this auditor's own notes/code/metadata; third-party content is excluded. Completion estimate for this scoped audit: 100%, with the precisely stated VOR acquisition gap retained.
