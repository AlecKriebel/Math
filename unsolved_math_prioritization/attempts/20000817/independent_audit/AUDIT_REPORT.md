# Independent adversarial audit: monomial component signatures

Problem 20000817 · AIM-ARITHMETIC_GEOMETRY-0063 · rank 760  
Audit date: 2026-10-05  
**Verdict: PASS, scoped to rigorous partial progress. The general problem is not solved.**

## 1. Scope and disposition

The frozen author archive is `MONOMIAL_SIGNATURES_20000817_AUTHOR_SAFE_FREEZE.zip`, 21,964 bytes, SHA-256 `ff634df72962777e7fd39797542604251c8c1b4d8c6ccedf52b2dc5696c78592`. Its ten files match the working author packet byte for byte. The archive and author files were not modified.

All authored proofs, the research report, source/provenance metadata, the author verifier and its saved output were reviewed. The complete selected prior report was read; the three complete input corpora were independently hashed and parsed. All eight supplied PDF fingerprints were independently reproduced from existing local bytes. Primary scholarly pages were separately inspected. These checks do not independently reconstruct every proof in the imported classification literature, nor authenticate the author's historical search log.

The correct target is equality of the entire sets of monomial points on components of the ordinary affine/projective Hilbert scheme. The catalog title is not the complete problem. [AIM Problem 16](https://aimath.org/WWN/hilbertschemes/hilbertschemes.pdf) confirms that scope and gives only a tentative Liebling remark.

The five approaches in the report are substantive and correctly distinguished: source/prior-work reconciliation; universal smoothability and anchors; exact length-eight incidence; arbitrary-characteristic projective boundary; and explicit collision falsification. The main additions over the supplied prior report are the full higher-dimensional length-eight signature and the explicit projective separator, with characteristic-range reconciliation and the general no-anchor obstruction. None resolves arbitrary pairs of nonsmoothable components. No novelty certification is given.

## 2. Universal smoothability and the affine reduction: PASS

The distraction proof is complete over an algebraically closed field in every characteristic. A finite lower set requires only finitely many distinct scalars. For a minimal forbidden exponent, every allowed grid exponent has a smaller coordinate, so the associated product vanishes at all selected points. Its leading monomial is the forbidden monomial for a global monomial order. The initial-ideal inclusion bounds colength above; evaluation on distinct points bounds it below. Equality identifies a radical ideal with the required monomial initial ideal.

A connected torus preserves each irreducible component. A finite Gröbner basis for a global monomial order admits an integral positive weight realizing its monomial leading terms; the associated flat degeneration stays on the same closed component. No improper appeal to projectivity of the affine Hilbert scheme is needed.

At the curvilinear ideal, the regular sequence gives tangent dimension nd. The smoothable component through it has dimension nd; hence the local ring is regular. This distinguishes that component. Every monomial point of any other component lies on two distinct components and is ambient-singular. The distinction between ambient smoothness and smoothness on one reduced component is maintained.

The published reference for universal monomial smoothability is [CEVV, Proposition 4.15](https://msp.org/ant/2009/3-7/ant-v3-n7-p02-p.pdf). The older arXiv proposition number means something different; the packet flags this correctly.

## 3. Exact length-eight signature: PASS

### Necessity

The rank-eight tautological algebra exists on the entire affine Hilbert scheme, and multiplication by each coordinate is a globally defined bundle endomorphism. Normalized traces are regular and commute with trivialization. Since the stated characteristic restriction excludes 2, division by 8 is valid. On a length-eight local algebra they recover the support coordinates: each centered multiplication operator is nilpotent.

Centered triple products vanish on the (1,4,3) stratum. The pair-product map has rank three there. Vanishing sections and vanishing 4-by-4 minors define closed conditions, so both conditions hold on the reduced closure. At a monomial point the coordinates are nilpotent and the trace centers vanish. All degree-three monomials therefore vanish, while the dimension of the quadratic piece is at most three. Length eight gives 1+e+q=8, hence e>=4. This proves precisely the claimed necessity. It does not assert that rank remains equal to three on the boundary.

### Sufficiency, including every higher ambient dimension

For e=4 the four-variable core is all surviving variables. For e=5 there are two surviving quadrics and at most four variables in their union of supports. For e=6 there is one quadric, and for e=7 none. Thus a four-variable core containing every surviving quadric always exists. There are enough unused core quadrics to select the required e−4 distinct promotions.

The displayed multiplication table is a unital commutative algebra over k[t]: every nonunit product belongs to the span of the quadratic labels and extra-variable labels, and that whole span annihilates the maximal ideal. Thus all triples of nonunits vanish identically. Associativity holds over the integer polynomial ring and after arbitrary field base change, including parameter zero.

The module has eight independent basis labels. All of them are polynomially generated by the ambient coordinates: the quadratic labels are prescribed products, and the extra labels are coordinate images themselves. Hence this is an embedded flat Hilbert family, not merely a family of abstract vector spaces. At zero its entire product table agrees with the monomial quotient. At a nonzero parameter, the independent three-dimensional square is spanned by the quadratic labels and promoted extra labels; the four core labels are a basis modulo the square. Unused ambient coordinates map to zero throughout. This proves the universal converse for arbitrary n, not just the finite dimensions tested by the script.

The closure formulation is essential. The literal generic-Hilbert-function shorthand in CEVV's theorem statement cannot exclude higher-embedding-dimension boundary points. The packet's closure warning and explicit family correctly avoid that reading. The imported two-component classification and its characteristic restriction are checked against [CEVV, Theorem 1.1 and its Section 6 proof](https://msp.org/ant/2009/3-7/ant-v3-n7-p02-p.pdf).

### Counting and tests

For each e, choosing the surviving coordinate variables and any 7−e quadrics among them gives a lower set. There are no additional cubic restrictions because all cubics are declared zero. Conversely every ideal satisfying the criterion arises uniquely in this way. The binomial formula follows, including the boundary functions (1,5,2), (1,6,1), and (1,7).

Independent enumeration gives:

- n=4: 684 total monomial ideals, signature 120
- n=5: 2,145 total; signature 600+105=705
- n=6: 5,507 total; signature 1,800+630+21=2,451
- n=7: 12,300 total; signature 4,200+2,205+147+1=6,553

All author length-zero-through-eight counts in dimensions 1–7 match. The 247 reduced flat models split as 120, 105, 21, and 1 by embedding dimension. Each passes 512 polynomial associativity identities and 64 exact special-fiber product comparisons. The geometric proof, not these finite checks, establishes membership.

## 4. Tangent and abstract fixed-point controls: PASS

A separately written verifier linearizes multiplication-matrix commutators on the border-basis chart. It does not import the author's Taylor-syzygy implementation.

- Collision: 17 border monomials, 136 unknowns, rank 103 over Q, tangent dimension 33
- Curvilinear anchor: 25 border monomials, 200 unknowns, rank 168 over Q, tangent dimension 32
- All 120 (1,4,3) monomial ideals: tangent histogram 33:12, 38:12, 41:18, 42:4, 43:24, 44:4, 52:40, 57:6

The results exactly match the author output despite the different presentation. These rational calculations alone are not used to certify positive-characteristic ranks. The published collision is the stated variable permutation; its any-characteristic assertion occurs in CEVV's published Lemma 5.4, numbered 5.9 in arXiv v2.

The union-of-two-conics control is also correct. The torus has three distinct characters, including in characteristic two, so its ambient fixed points are the coordinate points. Exactly two lie on either conic. The conics are smooth even in characteristic two because the remaining partial derivatives and the equation cannot vanish at a projective point. This is an abstract torus-scheme control, not an ordinary-Hilbert-scheme counterexample.

## 5. Projective Borel boundary: PASS

[Reeves–Stillman, Theorem 1.4](https://pi.math.cornell.edu/~mike/7670-fa20/references/reeves-stillman-lex-1997.pdf) explicitly works over an arbitrary field and makes the saturated lexicographic point ambient-smooth. A connected Borel subgroup preserves each projective component, and properness permits the Borel fixed-point theorem on each reduced component.

For exactly two Borel-fixed points, [Ramkumar v4, Theorem A and the paragraph immediately following it](https://arxiv.org/html/1907.13335v4) explicitly extends the geometry using characteristic-independent deformation computations and [Staal's arbitrary-characteristic classification](https://arxiv.org/html/2107.02204v2). Characteristic two excludes Ramkumar's case (ii) from the two-point classification; it is not an unproved exceptional two-point case. The packet conditions on the actual number of Borel-fixed closed points and is therefore correct in every characteristic.

These are point-set assertions. The proof does not assume that the Borel fixed subscheme is reduced, equate it to the torus fixed subscheme, or replace positive-characteristic Borel-fixedness by strong stability. The algebraically closed hypothesis also avoids the finite-field issue identified in Staal's Example 4.8.

## 6. Projective separator and embedded-point obstruction: PASS

[Bertone–Cioffi–Roggero, Example 6.12](https://arxiv.org/pdf/1503.03768v2) identifies the dimension-12 conic-plus-line component and dimension-15 twisted-cubic-plus-point component and their equal double-generic initial ideal in characteristic zero. This imported collision is smaller than equality of full signatures.

The claimed intersection ideal is exactly generated by x1x3, x2x3, x0²x1, x0²x2. The two component ideals are saturated, and intersection preserves saturation. Their sum has irrelevant radical, so the corresponding projective schemes are disjoint. The plane double line is a (1,2) complete intersection with polynomial 2t+1; the other line has polynomial t+1. Their union has polynomial 3t+2 and is locally Cohen–Macaulay without any zero-dimensional associated points.

The conic deformation remains disjoint from the fixed line for every parameter: the only candidate intersection is [1:0:0:0], and substitution into the conic equation gives 1. The relative conic is flat, for example by its monic quadratic presentation on the plane, and the line is constant. The disjoint union is flat. Nonzero fibers are smooth conic-plus-line schemes. The locus of all such pairs is irreducible (an open subset of the product of the smooth-plane-conic parameter space and the line Grassmannian), so it lies in the stated component; no special-family membership shortcut is required.

For exclusion from the other component, the flag Hilbert scheme of inclusions with polynomials 3t+1 and 3t+2 is projective. Its image in the second Hilbert scheme is closed and contains the dense twisted-cubic-plus-isolated-point locus. Every member of its closure therefore contains a subscheme with polynomial 3t+1, even if the extra point becomes embedded in a limit.

Such an inclusion in the proposed union would give an exact sequence whose nonzero kernel has constant Hilbert polynomial 1. A coherent sheaf with that polynomial is zero-dimensional. At a support point, a local parameter nonzerodivisor on the Cohen–Macaulay curve acts injectively on its structure sheaf, while a power annihilates the finite-length kernel. This is impossible. Thus the embedded-point possibilities do not evade the argument.

An independent inclusion-exclusion calculation gives the Hilbert series

(1−2z²−z³+3z⁴−z⁵)/(1−z)^4 = (1+2z+z²−z³)/(1−z)^2.

It yields 3d+2 for every d>=2, with initial values 1 and 4. Direct monomial counts through degree 32 agree. The proof of the Hilbert polynomial is symbolic, rather than inferred from finitely many values.

## 7. Corrections, limitations, and release decision

**Mandatory corrections: none.** The frozen packet may retain its mathematical claims as a scoped partial result.

Optional editorial improvements:

1. Normalize the malformed inline mathematical delimiters and missing backslashes in `PROOFS.md`; the meanings are unambiguous.
2. Replace “Staal's classification omits one characteristic-two case” by “case (ii) is excluded in characteristic two because it no longer has exactly two Borel-fixed points.” This avoids suggesting a gap in Staal's theorem.
3. The irreducibility explanation for the smooth conic-plus-line parameter space could be added to Proposition 7.1 for a completely explicit component-membership argument. It is a standard, valid implicit step.

The general affine and ordinary projective injectivity questions remain unresolved by this work. The Liebling thesis was not recovered in full and no full-signature counterexample was verified. The current survey's solved punctual-curvilinear question and the irrational-component result address different questions. Source metadata is checked, not a comprehensive certificate that all later literature has been found. Repository absence/search claims are historical bounded observations and were not independently repeated in this audit. The unknown catalog review-hash serialization remains explicitly uncertified.

The audit directory contains authored audit prose, original verification code, and bibliographic/hash/result metadata only. No source PDF, source extract, raw corpus record, or private coordination file is included. No remote write was made.
