# Independent adversarial review — Zenodo 23572690

## Verdict and strongest result

**PASS at the exact stated hypotheses.** No substantive defect or unresolved mathematical gap was identified in the six-page manuscript's classification, with the structural inputs checked against the primary bodies specified below. This is an AI mathematical review, not human peer review, formal verification, publication clearance or a novelty certificate.

For any field \(k\) of characteristic zero and any **nonzero** polynomial \(h\), the following properties of the ordinary canonical Hochschild Gerstenhaber algebra of
\[
A_h=k\langle x,Y\rangle/(Yx-xY-h(x))
\]
are equivalent: \(h\) is squarefree; its canonical bracket is zero; a degree-minus-one bracket generator exists; a square-zero BV generator exists. Units count as squarefree. In the positive case the zero operator works. In the repeated-factor case no bracket generator exists at all, without imposing square-zero.

The separate literal embedded specialization \(h=0\) is \(k[x]\), for which the displayed negative-divergence operator is a BV generator. It is not the algebra obtained by setting \(h=0\) in the abstract two-generator presentation. The classification does not extend to positive characteristic, twisted-coefficient Hochschild cohomology, arbitrary Gerstenhaber algebras, Poisson analogues, or any Keller/Jacobian/Dixmier/étale conclusion.

## Custody, complete reading and independence

- Paper: *BV generators for polynomial Weyl subalgebras*, version 1.0.0, manuscript and Zenodo publication date 22 October 2026.
- Public six-page PDF: 78,866 bytes; SHA-256 `2c344b0baff06088f04f4468bd8f6365405e879f7004b169055aebedbdecd4e7`.
- Public source/verification ZIP: 100,928 bytes; SHA-256 `a7ab72e55fd0952d363f78f92bc418b9f1331ccefb1f75eaea8dda32868601e6`.
- Read the mandatory programme objective, all six actual published pages, complete TeX, and necessary current dependency notes. The embedded PDF is identical to the public standalone PDF. Source receipt, MD5/size/SHA checks, all 12 extracted source hashes, and review artifacts are bound in `evidence.json` and `source-custody.json`.
- Constructed and executed fresh controls before reading the packaged helper. They use localized normal-ordered Weyl operators and normalized-bar tensors, rather than the supplement's rational-polynomial-only implementation.
- No sibling report, scope findings, dedicated historical assessment, or `PRIORITY.md` was read. Raw primary PDFs/text and raw acquisition receipts in the scope cache were used. The paper and `DEPENDENCIES.md` contain author claims about prior source reading; these were incidentally encountered and did not substitute for the primary checks. The source manifest hashes `PRIORITY.md` as opaque bytes only.
- No public source, archived proof, publication draft, website, spreadsheet, Git state or external service was changed. No repair was attempted or required.

## Falsification targets and analytic findings

### Exact algebra, characteristic and scalar normalization

The proof requires ordinary \(\operatorname{HH}^\bullet(A_h,A_h)\), its canonical product and bracket, and a \(k\)-linear operator of degree minus one. The generator identity in the original question has an additional \(a\Delta(1)b\) term; it vanishes here because negative cohomology is zero. In degree one the identity becomes
\[
[a,b]=-\Delta(ab)+\lambda(a)b-\lambda(b)a,
\qquad \lambda=\Delta|_{H^1}:H^1\to k.
\]
Thus the manuscript's signs agree with its convention and with the commutator bracket of derivations.

For nonzero \(h\), the Ore relation gives PBW normal forms. The embedding \(Y=yh\) is compatible with \([y,x]=1\); the alternative generator \(hy\) differs by the polynomial \(h'\), so it generates the same subalgebra with \(x\). This statement is not used at \(h=0\), where an embedding of the abstract plane would fail.

The paper fixes the **monic** gcd \(d=\gcd(h,h')\) and \(\pi=h/d\). If \(h=\alpha\prod u_i^{e_i}\) with monic irreducibles, then \(d=\prod u_i^{e_i-1}\) and \(\pi=\alpha\prod u_i\). The source convention uses a monic radical, so its normalizer vectors differ by a nonzero scalar when \(h\) is nonmonic. Spans, divisibility and innerness are unaffected; equivalently, rescale \(Y\) by \(\alpha\). The present proof's own formulas are consistent with its choice of \(\pi\). No monicity hypothesis is missing.

Characteristic zero is essential in several distinct places: the leading PBW commutator coefficient, polynomial integration, separability of each irreducible, and the nonvanishing derivative used in the obstruction. No positive-characteristic conclusion follows. In particular, the formal characteristic-three example \((x^3)'=0\) already breaks the characteristic-zero radical/gcd reasoning.

### Center, cohomology quotient and the structural import

For a nonzero highest \(Y\)-degree term \(t_N(x)Y^N\), the highest term of \([t,x]\) is \(Nh t_N Y^{N-1}\). It cannot vanish in characteristic zero. Hence the centralizer of \(x\) in \(A_h\) is \(k[x]\). Commuting also with \(Y\) forces the derivative to vanish, so \(H^0=Z(A_h)=k\).

If \(D_f(x)=0,D_f(Y)=f\) is inner, its implementing element lies in \(k[x]\), and \(f=-ht'\). Conversely, integration over any characteristic-zero field gives an implementing polynomial for every multiple of \(h\). Thus \([D_f]=0\) if and only if \(h\mid f\), with the sign fixed by \(\operatorname{ad}_t=[t,-]\).

The actual primary resolution has precisely the manuscript's displayed differential. The cochain image is \(hA+h'A=dA\); the quotient is a vector-space/cochain-coordinate identification, not an assertion that this quotient's ordinary multiplication is the whole Hochschild cup product. The ideal is two-sided because \([Y,d]=hd'\in dA\). The length-two resolution gives vanishing above degree two. I checked the source's proof of the characteristic-zero image computation as well as its stated result.

The primary derivation decomposition gives \(H^1\) spanned by the \([D_f]\) and normalizer commutators \([\operatorname{ad}_{g a_n}]\). Its field hypotheses are characteristic zero, not algebraic closure. I also checked the normalizer theorem, the extension of \(D_f\) to the localization, and the characteristic-zero derivations-of-the-Weyl-algebra argument underlying that decomposition. The paper does not claim to compute these imported structures by finite experiments.

### Central annihilator: no missing denominator or finite-dimensional assumption

Extending \(D_d\) by \(D_d(y)=d/h=1/\pi\) respects the localized Weyl relation and sends \(Y=yh\) to \(d\). Applying the Leibniz rule to \(y^n\), then normal ordering, yields the displayed binomial sum. Each coefficient of \(D_d(g a_n)\) is
\[
\binom n{j+1}g d^jP_j h^{n-1-j},
\]
attached to \(y^{n-1-j}\). It therefore lies in the ambient basis span \(\bigoplus_m k[x]h^m y^m=A_h\). There is no remaining rational pole in the implementing element. For \(n=0\), the derivation kills \(g/d\). Consequently the commutators with all spanning classes are inner, and \(c=[D_d]\) is Lie-central.

If \(d\ne1\), then \(\deg(d/u)<\deg d<\deg h\) for each irreducible \(u\mid d\). Neither polynomial is zero, and they have different degrees. Their classes cannot become proportional modulo \(h\). This proves the nonzero and independent-companion conditions over the original field, even when \(u\) has no root there.

### Canonical cup comparison, including constant and linear relation terms

The degree-two comparison is checked in the normalized bar complex, not inferred from a commutative heuristic. For each \(s\ge2\), expanding the bar differential makes the interior terms telescope to
\[
\sum_{i=0}^{s-1}x^i[x]x^{s-1-i}-[x^s].
\]
The two leading bars contribute \(-[Yx]+[xY]=-[h]\). Constants vanish in normalized bars, and the remaining linear term supplies \(-h_1[x]\). Thus the full comparison has exactly the small-resolution differential, including the nonhomogeneous and constant cases. In degrees zero and one it lifts the identity, and no higher source module remains.

Pulling back the ordinary bar cup product gives the stated formula with all right-hand polynomial factors retained on the right. Setting the first derivation to \(D_f\) makes every correction term vanish **literally**, since \(D_f(x^i)=0\); the value is \(fE(x)\). For \(f=d\), this is in \(dA\) for every derivation \(E\), not merely the chosen obstruction derivation. Hence \(cH^1=0\) for the canonical cup product. This is the important product interface missing from a bracket-only argument; it is supplied correctly here.

### Obstruction against every candidate operator

Lie-centrality and cup annihilation give \(\lambda(c)b=\lambda(b)c\) for all \(b\in H^1\). An independent companion forces \(\lambda(c)=0\), after which \(c\ne0\) forces \(\lambda\equiv0\). This uses only a two-dimensional subspace at a time. It is valid for the possibly infinite-dimensional \(H^1\), with no continuity, finite rank, homogeneity-in-an-extra-grading, or choice of \(\Delta|_{H^2}\) assumption. Square-zero is not used.

For an irreducible repeated factor \(u\), put \(g=d/u\), \(L=\pi d'/d\), and define \(b(x)=\pi,b(Y)=LY\). In characteristic zero, \(u\mid\pi\) and \(L\) is a polynomial. The relation calculation
\[
Lh+h\pi'-h'\pi=0
\]
proves that this is an actual derivation of the presentation. The canonical cup is zero because \(g\pi=d(\pi/u)\). Direct evaluation of the commutator on both generators gives
\[
[D_g,b](x)=0,\qquad [D_g,b](Y)=Lg-\pi g'=h u'/u^2.
\]
This polynomial is nonzero and has degree \(\deg h-\deg u-1<\deg h\), so its derivation class is nonzero. This contradicts the necessary generator identity on a cup-zero pair and proves both nonexistence and a nonzero canonical bracket.

The direct definition of \(b\) is important: in the convention \(Y=yh\), \(\operatorname{ad}_{\pi y}(Y)\) differs by \(\pi h''-Lh'\), which need not vanish. The manuscript explicitly recognizes this term and does not use the false literal identification. Fresh operator checks independently confirmed it.

### Squarefree and zero boundary cases

When \(d=1\), the normalizer commutators are inner. The degree-one cohomology is spanned by commuting \([D_f]\), the higher cohomology vanishes from degree two onward, and brackets with \(H^0=k\) vanish. Thus the entire canonical bracket is zero, not only its degree-one part. \(\Delta=0\) consequently satisfies both the generator and square-zero conditions. This includes any nonzero constant \(h\), where the algebra is a rescaled Weyl algebra, and linear/squarefree higher-degree polynomials.

For the literal embedded \(h=0\), the algebra generated by \(x\) and \(0\) is \(k[x]\). Under its usual ordinary Hochschild identification, \(\Delta(f\partial_x)=-f'\) yields the commutator of vector fields and their action on functions with exactly the required signs. Its square is zero because it lands in degree zero, where it vanishes. The manuscript correctly separates this from the abstract polynomial plane.

The Nakayama map fixes \(x\) and sends \(Y\) to \(Y+h'\). For nonconstant \(h\), \(h'\ne0\), and \(Y,h'\) are linearly independent, so their invariant span has a nontrivial unipotent Jordan block. Hence the nonsemisimple branch of the original question is addressed, including squarefree positive and repeated-factor negative cases. For constants the map is the identity. No semisimplicity theorem was silently applied after dropping its hypothesis.

## Fresh controls and reproducibility

`fresh_weyl_controls.py` implements multiplication in \(k(x)[y]\) by the normal-ordering rule, applies derivations by repeated Leibniz insertion, and expands normalized-bar boundaries as tensors of basis monomials. It imports no supplied checker.

The final run passed **631 exact assertions across 12 polynomials**, including \(1,2,1/2,x,3(x^2+1),x(x-1),x^2,x^3,2(x-1)^3,(x-1)^2/2,(x^2+1)^2\), and a degree-seven polynomial with two repeated factors and leading coefficient three. It checked 96 normalizer primitives, 192 commutator identities, all complete bar comparisons, seven repeated-factor witnesses, and 16 polynomial pairs for all three relevant embedded-zero BV degree combinations.

For the actual \(h=x^2\) witness subspace \(\langle c,a,b\rangle\), the scalar equations required of a generator give coefficient-matrix rank 3 and augmented rank 4. This independently exposes inconsistency without invoking square-zero. Omitting the nonlinear bar correction fails for eight nonlinear examples. The localized operator computations detect the nonzero ambient correction term. A characteristic-three derivative control marks an excluded hypothesis boundary.

The first fresh run passed the ten initially selected model/operator/bar cases and then failed an auxiliary test because my harness used symbolic-expression modulo where coefficient reduction modulo three was intended. That failed script and its output remain in `fresh-controls-attempt1.*`. The correction affected only my harness; no manuscript defect or repair is inferred. The final run uses a polynomial over \(\mathbf F_3\) for that check and includes two additional rational-scalar cases. The corrected complete fresh run finished before the packaged checker was read.

Afterward, the unmodified `exact_checks.py` was read and executed in an isolated temporary copy with standard-library-only flags, once normally and once with `-OO`. Both outputs matched `CHECK_RESULTS.json` **byte for byte**. Its output reports 18 repeated-factor examples, six squarefree boundary examples, bar degrees 1–12, 72 coefficient/reciprocal checks, 12 embedded-zero Leibniz examples and five deliberately false controls. Those are finite diagnostics, not direct computation of the full Hochschild Gerstenhaber algebra or verification over every field. The package builder was not run. All 12 source files remained unchanged.

## Primary-source interfaces and attribution

`primary-reading-ledger.json` records exact URLs, hashes, editions and reading scope. The following interfaces were independently checked from raw primary sources:

- **Lopes–Solotar, publisher PDF** ([EMS](https://ems.press/content/serial-article-files/30909)): Proposition 2.1 supplies the ambient basis and commutators; Section 3 gives the exact free resolution/differential and vanishing above degree two; Proposition 3.9 and Corollary 3.11 give the characteristic-zero quotient; Section 6.1/Theorem 6.2 supply the cited derivation and center structure. The Nakayama paragraph was also read. The resolution's exactness is a published structural input; this review does not independently redo every contracting-homotopy calculation or the full positive-characteristic/Virasoro analysis.
- **Benkart–Lopes–Ondrus, author manuscript v2** ([arXiv](https://arxiv.org/abs/1406.1508v2)): checked Lemma 2.13, the characteristic-zero normalizer theorem and proof, Proposition 3.1, Theorem 4.9/Lemma 4.11, and Theorems 5.3/5.7, Proposition 5.9 and Theorem 5.13 with their relevant proofs. The spanning, innerness, localization and arbitrary-field hypotheses agree with the import. This is authenticated author-manuscript v2, not asserted byte-identical to the final journal PDF.
- **Original OWR question, publisher PDF** ([EMS](https://ems.press/content/serial-article-files/48175)): read the complete Lopes–Solotar contribution on printed pages 2702–2703. It asks about the embedded characteristic-zero family with a nonsemisimple Nakayama automorphism. Its general-algebra and Poisson questions are separate and are not answered here.
- **Kowalzig–Krähmer, author-host manuscript**: Theorem 1.7 and its application context explicitly require semisimplicity and concern ordinary cohomology, with twisted-coefficient homology entering the duality. It provides background, not a substitute proof for the nonsemisimple branch.
- **Herscovich–Li, publisher PDF**: Proposition 4.15 and its complete proof establish earlier no-generator nonexistence for \(\operatorname{FK}(3)\), already without imposing square-zero. The manuscript credits this antecedent correctly; it is not the present infinite-dimensional Ore-domain family.
- **Bian et al., author preprint v2**: checked Criterion 7.7 and Theorem 7.11 and their stated scope. The criterion assumes commuting relevant odd generators; the positive result is for truncated basic cycle algebras. It does not contradict the exhibited noncommuting cup-zero pair here.

No claims about completeness of the literature search were independently certified. The polynomial-family structure and general obstruction strategy are inherited and appropriately credited. The supported added result is this family-wide squarefree classification, derived using the displayed canonical cup comparison and obstruction. No firstness, current-openness or general conjecture resolution beyond the specified family follows from this review.

## Exact remaining gap

**None identified in the stated mathematical classification or embedded-zero addendum**, using the authenticated structural results at their stated hypotheses. Independent human refereeing and proof-assistant formalization have not occurred, and full historical priority was not established. The finite tests supplement the complete analytic argument above; they do not replace it. No follow-up conjecture was generated and no publication action was taken.
