# PR17 independent primary-source, scope, and interpretation audit

Target: 30000224 / OWR-824-008. Frozen head: `dae2b77074945443e1b91c92f641ff9feff12235`.

Audit date: 2026-10-01 UTC. Assigned audit gate: complete (100%). Original mathematical problem: **not resolved by this note or this audit**.

## Verdict

**PASS for the restricted mathematical content and the partial/stalled disposition.** No mandatory correction to the three propositions or their stated scope was found. No complete positive or negative resolution of the exact unrestricted target was verified in the bounded current search. This is not a worldwide absence certificate, a priority determination, or an endorsement of a solution claim.

The published Hassanzadeh article's metadata was verified independently, but its complete version-of-record text was inaccessible (Wiley PDF/XML routes returned HTTP 403; web full-text routes returned the abstract). Its complete arXiv v2 text, relevant proofs, and displayed hypotheses were checked. A claim that this audit compared the full published text with v2 would be incorrect.

No historical REVIEW, review_summary, parent conclusions, or sibling reports were read before the independent first-conclusion checkpoint, and none was needed afterward. No canonical files, Git state, environment, live PR, paper, tracker, or Zenodo item was changed. No external individual was contacted.

## Exact target and boundaries

[OWR 19/2005](https://ems.press/content/serial-article-files/45993?nt=1), PDF page 44 / printed page 1116, and [Singh–Walther v2](https://arxiv.org/pdf/math/0701524v2), PDF page 8, give the same polynomial ring in four variables and the same map to `K[s^4,s^3t,st^3,t^4]`. The characteristic-zero question asks for **any** ideal b with radical a and Cohen–Macaulay quotient. It does not assume that b is homogeneous, binomial, a complete intersection, or of a specified multiplicity.

Both original pages were visually checked. Both explicitly state `H_a^i(R)=0` for `i >= 3`; the Singh–Walther glyph is a genuine greater-than-or-equal sign, not a strict inequality. Their positive-characteristic comparison attributes a set-theoretic complete-intersection construction to Hartshorne. That fact does not answer the characteristic-zero question. The report is numbered for the 2005 workshop; [EMS metadata](https://ems.press/journals/owr/articles/824) gives publication on 31 March 2006.

The target concerns the dimension-two affine cone quotient. Its smooth projective rational curve being locally Cohen–Macaulay does not imply its homogeneous coordinate ring is Cohen–Macaulay. Likewise, Cohen–Macaulayness of a proposed quotient at one unspecified localization is insufficient for the original global ring claim. The note's first two propositions use the global CM hypothesis; its third uses homogeneous arithmetic CMness at the vertex and on Proj.

Extension to an algebraic closure is legitimate here: the semigroup prime is geometrically prime, radical equality follows after extension from `b subset a` and `a^N subset b`, and CMness ascends under field extension. No embedding of an arbitrary characteristic-zero field into C is needed for the three restrictions. Statements about Du Bois singularities below apply to the corresponding complex cone, as the note says.

## Theorem-to-application checks

### Ma–Schwede–Shimomoto

[Complete v3](https://export.arxiv.org/pdf/1605.02755v3), dated 14 April 2017: Proposition 4.9 on PDF page 16 requires a regular local ring essentially of finite type over C and a quotient that is Du Bois but non-CM. Its proof uses surjectivity from every nilpotent thickening onto the reduced quotient's local cohomology. Here `u=s^2t^2` is absent from A but `u^2,u^3` belong to A, so A is not seminormal and hence cannot be Du Bois. The implication has the direction needed by the note; non-Du-Boisness is not evidence for existence of a CM thickening.

Corollary 4.10, PDF page 17, requires a homogeneous reduced target, Du Bois away from the vertex, and a nonzero **nonpositive-degree** local-cohomology component below dimension. Its conclusion excludes set-theoretic CMness; it is not permission to homogenize b. The note computes `H_m^1(A)=K(-1)`, concentrated in degree +1. Since A is a domain, `H_m^0(A)=0`; no degree <=0 defect remains below dimension two. Thus the stated obstruction cannot apply. Proposition 4.4 also independently relates positive-degree defect to failure of Du Boisness in this isolated-cone setting.

### Boix–Eghbali

[Complete v2](https://arxiv.org/pdf/1806.04405v2), revised 12 June 2021: Remark 5.7, PDF page 18, matches the exact quartic after `x0,x1,x2,x3 = w,x,y,z`. The displayed complete intersection is `(wz-xy, wy^2-x^2z)`. Under Segre coordinates the cubic is `ab(bc^3-ad^3)`; the residual lines and the divisor of type (1,3) are exactly those used in the note.

Theorem 5.8 on that page is a **regular-local** conditional theorem. It requires a flat local endomorphism, injectivity of the stated transition maps on Ext, `m not subset zd(R/I)`, and an already CM source-side thickening b whose iterated endomorphism images are cofinal with its powers. The endomorphism setup also fixes a decreasing cofinal family for I. Its conclusion is CMness of the linked ideal J under those assumptions. Linkage alone, or the displayed factorization, supplies none of the missing thickening/injectivity/cofinality conditions. The note correctly refuses this shortcut.

Caution for future reuse: adjacent Remark 5.10 contains wording that calls this toric quotient nonreduced, although the displayed J is prime. This audit does not rely on that remark or transfer its assertion to characteristic zero.

### Hassanzadeh

[Complete v2](https://arxiv.org/pdf/2409.05705v2), submitted 12 February 2025; manuscript date 13 February: Theorem 1.2 spans PDF pages 2–3. The regular ambient ring satisfies its Serre condition and the residual codimension is s=2. The source I has four minimal quadratic generators, r=4. The first alternative demands `s >= r` and local persistence of r generators; already `2 >= 4` fails. The second requires local infinite residue field, generation by a proper sequence, and `pdim Z_i <= r-i-1` for every i>=1. It is not a statement for arbitrary linked ideals.

The exhibited c is a cycle, is not a boundary, and is killed in H1 by all four variables. Thus depth H1=0 at m. The exact sequences in the note give depth(R/I)=1, depth I=2, depth Z1=3, depth B1=1, and depth Z2=2. Auslander–Buchsbaum gives `pdim Z2=2`, whereas the required bound is `4-2-1=1`. This suffices to reject the proposed second application without deciding its proper-sequence hypothesis.

Definition 3.18 and the **actual** Corollary 3.19 are on PDF page 22. Sliding depth requires `depth H_i >= d-r+i`; for H1 this is 1, so its socle rejects SD. The displayed corollary requires a regular local ring and SD. The introductory summary on page 3 additionally mentions an infinite residue field and `G_s^-`; that internal mismatch is not an error in the frozen note, which relies only on the failing SD hypothesis. Theorem 3.16's proof on page 21 constructs a free approach under its explicit cycle hypotheses; it does not bypass them.

[Publisher metadata](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/jlms.70108) and the publisher's Crossref deposit identify JLMS 111(3), e70108, first published 6 March 2025. The version-of-record theorem text was not compared.

### Classical binomial and normal-bundle inputs

[Eisenbud–Sturmfels, published author-hosted copy](https://eisenbud.github.io/papers/pdfs/1996-002.pdf), Duke Math. J. 84(1), July 1996: Section 2, Theorem 2.1 and Corollary 2.2 on PDF/printed pages 11–14 classify Laurent binomial ideals and show radicality in characteristic zero. The algebraically closed hypothesis in their decomposition statement is safely handled by the note's direct coefficient-one group-algebra proof over arbitrary K. Primary contraction from the Laurent ring is the extra step needed for the proposed CM thickening; radicality of an arbitrary polynomial binomial ideal would be a false stronger assertion.

[Eisenbud–Van de Ven, published copy](https://eisenbud.github.io/papers/pdfs/1981-001.pdf), Math. Ann. 256 (1981), 453–463: the characteristic-zero setting is on printed page 453, and page 463 states the quartic normal bundle is `O_P1(7) directsum O_P1(7)`. The paper's notation uses degree on the abstract rational curve. The note correctly expresses the conormal bundle as `O_P1(-7)^2`; ambient O_C(1) instead pulls back to O_P1(4). Its independent cubic frame avoids depending on an unverified normal-bundle assertion.

## Independent mathematical validation

The one-dimensional deficiency is exact: degree-one A omits only u, all degree-eight exponents are present, and induction covers all degrees >=2. B is free of rank four over K[w,z], with basis 1,x,u,y. The short exact sequence with quotient K(-1) yields depth A=1 and the stated defect. These facts are classical semigroup/normalization input, not a resolution.

For a binomial candidate, global CMness and a unique minimal prime force a-primaryness. The four variables lie outside a, so Laurent localization contracts back exactly. Evaluating a binomial at (1,1,1,1) forces coefficient ratio one. The characteristic-zero group algebra is reduced, hence the candidate equals a and fails CMness. No homogeneity assumption is needed.

For a candidate containing q, S=R/(q) is normal CM of dimension three and P=a/(q) has height one. At primes containing P, catenarity and the CM quotient give maximal CMness of the ideal J by the depth lemma; elsewhere J=S. Hence J is rank-one reflexive. Its height-one localizations determine `J=P^(r)`, a symbolic power. Grading preservation forces homogeneity. On the quadric it defines rC of type (r,3r); `H^1(I_D(r))` has dimension `2r-1>0`. That contradicts arithmetic CMness. The proof controls arbitrary b precisely because homogeneity is derived in this special q-containing case.

For homogeneous generic multiplicity two, primaryness turns the generic square-zero inclusion into `a^2 subset b`. The nilpotent ideal sheaf is a torsion-free rank-one module on the smooth C, hence a line bundle L. Its conormal quotient and the independently verified splitting force `L=O_P1(e)` with e>=-7. Twisting by two gives `h^0(O_Y(2))=e+18>=11`, impossible for the surjective arithmetic-CM restriction from the ten-dimensional R2. Generic multiplicity one likewise gives b=a. No argument homogenizes an arbitrary nonhomogeneous b, and none is silently assumed.

Own `independent_replay.py` imports no frozen verifier and passed **35** exact assertions. It checks exponent slices, derivative/frame identities and covering minors, all four Koszul annihilations, and the exact rank-6/rank-7 nonboundary certificate. These finite checks corroborate identities; the universal conclusions above depend on the stated algebraic proofs.

## Corrections, priors, and exact remaining gap

Mandatory mathematical/source-target corrections: **none found**. Mandatory limits on how this audit may be reported: do not say it checked the complete published Hassanzadeh text, certified worldwide openness, proved novelty, or extended the multiplicity-two obstruction to arbitrary nonhomogeneous b.

Recommended provenance improvements are to pin the MSS citation to v3 and Boix–Eghbali to corrected v2, and to quote the actual Corollary 3.19 on page 22 if its hypotheses are expanded later. The frozen note already identifies Hassanzadeh v2 and makes no novelty claim. The binomial theory, quartic normal bundle, ribbon quotient mechanism, and quadric cohomology are classical inputs; this audit found no reason to label the packaged deductions as new discoveries.

The exact unexcluded class is an a-primary **non-binomial** ideal whose quotient has nonzero nilpotent q. If homogeneous, its generic multiplicity is >=3. For nonhomogeneous ideals the note gives no multiplicity-two exclusion; it gives no general reduction to homogeneous ideals. No construction or obstruction for this remaining class was obtained in this validation-only audit. Current primary literature located in the bounded search does not supply one. The partial/stalled disposition is faithful.
