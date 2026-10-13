# Independent adversarial audit: strict Calabi–Yau threefold dynamics

Date: 2026-10-03 (UTC). Target: **30005961 / OWR-14298581-008**, queue rank 504.

## Verdict

**PASS_PARTIAL.** The frozen package correctly presents five unsuccessful construction routes and valid, carefully bounded calculations and obstructions. No blocking mathematical defect was found within those stated bounds. This verdict is **not** a solution, a new-example certificate, a novelty finding, a classification of all strict Calabi–Yau threefolds, or authorization to publish.

The full target remains **unresolved after five attempts**. No new underlying threefold has been constructed. In particular, changing an automorphism on either known variety does not advance the required existence claim.

Audited author-manifest SHA-256:

`089b4bef99b12d6ba3d41149f21282fe8d569d4b46f3c1a4b3ab8b0e29740a3a`

All six manifest-listed files match their frozen byte lengths and hashes. They were checked again after all testing and are unchanged. The author's checker was copied to a temporary directory before execution because it writes a results file beside itself. The replayed result is byte-identical to the frozen `exact_results.json`.

## 1. Target and interpretation

The primary target is Oguiso's Question 12 on p. 1823 of the [official Oberwolfach report](https://ems.press/content/serial-article-files/50039?nt=1). Its strictness conditions are smoothness, projectivity over the complex numbers, simple connectedness, and trivial canonical **line bundle**. The automorphism must be biregular, have positive entropy, and admit no equivariant dominant rational map to a curve or surface. The underlying variety must differ from X3 and X7.

The package keeps these conditions throughout. The Hodge vanishings used in §1 follow from simple connectedness, Hodge theory, and Serre duality; they are not substituted for simple connectedness. Birational examples, merely numerically trivial canonical classes, and additional dynamics on X3/X7 are correctly insufficient.

The more general examples question in Question 1 cannot be used to evade the narrower Question 12. The stated unresolved disposition is justified directly by the absence of a candidate meeting the full target, independently of any claim about completeness of the literature.

## 2. Imported dependencies and source hazards

The relevant theorem statements were checked in their primary texts, rather than inferred from abstracts or a database assessment:

- [Oguiso–Truong](https://arxiv.org/abs/1306.1590), §3, Theorem 4.1, Lemma 4.3 and Proposition 4.4: generically finite equivariant comparison of dynamical degrees; in dimension three, unequal first and second degrees imply primitivity for a bimeromorphic selfmap of a compact Kähler manifold; the scalar-quotient lift mechanism.
- [Oguiso–Sakurai](https://arxiv.org/abs/math/9909175), Theorems 3.3–3.4 and Lemma–Definition 4.1: the isomorphism case, the birational contraction classification, and the explicit maximal-contraction factorization equation. Their broader Calabi–Yau convention permits nontrivial fundamental groups. The extra cases have fundamental groups C3 and C3 × C3 and do not satisfy the present target. The isomorphism case is of Type A and also does not give a simply connected strict example.
- [Gachet](https://jep.centre-mersenne.org/articles/10.5802/jep.277/), definition and Theorems 1.1–1.2, pp. 1220–1221: the strict Calabi–Yau convention, freeness in codimension two, and the two-example classification for the relevant isolated quotient construction.
- [Oguiso's Ueno-type paper](https://arxiv.org/html/2401.04386v3), Example 4.1, Theorems 4.2–4.3 and Lemma 4.6: the Klein-quartic abelian threefold, order-seven eigenspaces, unique projective crepant resolution, and the automorphism 1+g.
- [Oguiso's Picard-number-two paper](https://arxiv.org/abs/1206.1649), Theorem 1.2(1), and [Cantat–Oguiso](https://arxiv.org/abs/1107.5862), Theorems 1.3 and 3.3: respectively the odd-dimensional finite automorphism group result in the stated Calabi–Yau setting and the generic Wehler distinction between biregular and birational groups.

Three source-transcription traps were tested:

1. The official OWR report gives **d2 > d1** for the cited X7 map. The [arXiv v1 report](https://arxiv.org/html/2407.17297v1) reverses this. Direct exact computation supports the final report, as the frozen proof states.
2. OWR's verbal definition of maximality points the wrong way for the subsequent argument. The original OS displayed equation is **Φ = μ ∘ φ0**. The frozen proof uses that equation, not the reversed wording.
3. OT's discussion of its displayed matrix calls it an element of SL(3,Z). Its determinant is **−1**. The frozen package correctly uses GL(3,Z), and this typo does not obstruct an abelian-variety automorphism.

These corrections do not furnish new mathematics or a new variety.

## 3. Route-by-route mathematical audit

### Route 1: hyperbolic matrices on X3 — PASS at the stated scope

The claimed inverse multiplies the displayed matrix to the identity on both sides. Its characteristic polynomial is t³−mt+1 and its determinant is −1. For every integer m ≥ 3, the three disjoint sign-change intervals supply three distinct real roots α < 0 < β < γ. The root sum gives |α| = β+γ, hence |α| > γ > 1 > β > 0.

The wedge calculation on the abelian cover gives d1 = α² and d2 = α²γ², with d2 > d1 > 1. This is not merely a spectral calculation on an arbitrary vector space: the map is an integral automorphism of E³, commutes with the scalar group, descends, and lifts through the invariant singular-point blow-up. Applying the same construction to its inverse proves biregularity. The dominant generically finite rational comparison then applies to the actual lifted map. OT's **dimension-three, bimeromorphic** criterion supplies primitivity; no higher-dimensional extrapolation is needed.

The parameter-uniform proof, rather than the 98 finite checks, supports the assertion for all m ≥ 3. All maps act on the same X3. This is a verified known construction mechanism and no solution to the further-variety problem.

### Route 2: finite quotients and X7 — PASS with essential hypotheses

For the nontrivial scalar subcase, an invariant volume form forces ξ³ = 1. Pullback across the free quotient locus and extension across its finite complement justify the necessity. The order-three elliptic scalar forces the equianharmonic complex structure. The claim is about nontrivial scalars, not arbitrary translation actions or arbitrary finite quotients.

For the broader isolated quotient argument, the hypotheses are sufficient and properly retained: an abelian threefold, a finite action free outside finitely many points, a projective crepant resolution that is an isomorphism over the free locus, and a strict resulting threefold. A general ample surface can avoid the finitely many bad points. Its cover is finite étale, and the **ambient tangent bundle restricted to the surface**, not the surface tangent bundle, pulls back to a trivial rank-three bundle. Integration under a finite étale cover then gives c2(X)·ν*H = 0. The birational c2-contraction classification applies. Connectedness of the resolution fibers follows from proper birationality to a normal target. In the everywhere-free case the quotient retains an infinite finite-index abelian fundamental group and cannot be strict.

The finiteness of the bad locus is essential. An ample surface cannot generally avoid a fixed curve; no assertion about all fixed-curve quotients follows. The paper's freeness-in-codimension-two hypothesis means precisely the appropriate isolated behavior in dimension three. Dropping simple connectedness also changes the classification.

For X7, 1+g is an actual integral endomorphism with inverse −(g+g³+g⁵). The cyclotomic relation holds in the endomorphism algebra, as is also explicit in the primary construction. It commutes with g and lifts biregularly by uniqueness of the projective crepant resolution. The three squared eigenvalue moduli are a, b, c with a > b > 1 > c > 0, elementary symmetric values 5, 6, 1, and abc = 1. Therefore d1 = a and d2 = ab = 1/c > a. Passing to the inverse swaps d1 and d2, not the underlying variety. No unproved choice of resolution or new X is concealed here.

### Route 3: surface × elliptic-curve quotients — PASS for product-induced maps

The map to E/G_E is invariant under the diagonal finite group and descends to the quotient. A normalizing product automorphism induces an automorphism of that base curve, giving the stated semiconjugacy. Composing with any birational model retains a dominant rational fibration. Thus the particular induced map is imprimitive even if its entropy is positive and a strict resolution happens to exist.

No connected-fiber condition is needed for the target's definition of an equivariant rational fibration. The package correctly avoids asserting that all abstract automorphisms of all such resolutions are product-induced or imprimitive. Failure of simple connectedness of the unquotiented product is a separate obstruction.

### Route 4: Picard rank and regularization — PASS

On the integral divisor lattice modulo torsion, a biregular map acts unimodularly and preserves the top intersection form. At rank two, spectral radius r > 1 forces two real eigenvalues with absolute values r and r⁻¹. Nonreal conjugates would instead both have modulus one. Every cubic monomial then has weight of absolute value r^(2i−3), for i = 0,1,2,3. None equals one, so invariance would force the entire cubic to vanish, contradicting the positive cube of an ample class. Rank one has only the positive integral unit action. Finally, log-concavity with d0 = 1 implies that d1 = 1 forces every dynamical degree to be one, so entropy is zero.

This argument genuinely establishes the stated entropy obstruction for all smooth projective threefolds of Picard number at most two; it does not require Calabi–Yau assumptions. It also explains the odd-dimensional extension. In even dimension a middle zero-weight monomial appears, so the same conclusion cannot be inferred. Nor does this argument itself prove the full automorphism group finite: that stronger Calabi–Yau claim is separately cited.

The generic Wehler theorem is applied to a threefold hypersurface of multidegree (2,2,2,2) in (P¹)⁴, with genericity retained. Its birational automorphisms do not automatically become regular. Ordinary blow-up discrepancy (r−1)E is nonzero for a nonempty smooth center of codimension at least two; positive intersection with an ample square prevents numerical triviality. This excludes the unrestricted blow-up repair, not all crepant model changes.

### Route 5: nef eigenclasses, maximal contractions and rigidity — PASS as conditional

For an expanding nef eigenclass D, intersection invariance gives D³ = 0 and c2·D = 0. The eigenray cannot contain a nonzero rational vector: that would make the eigenvalue a rational algebraic unit, hence ±1. Both the action and its inverse preserve the integral lattice, which is the necessary justification for the unit assertion.

The resulting class is real, nonzero, and on the nef boundary. It is not a line bundle, is not proved semiample, and does not decide whether a different rational c2-null nef class exists. A rational linear functional does not force a rational point on an irrational face of a closed cone. No hidden rational-approximation or abundance step is valid here.

The semiample proposition has a sound separate proof. A numerically nonzero semiample line bundle yields a positive-dimensional morphism; after Stein factorization its pullback polarization has c2 pairing zero. Let φ0 be maximal with the original OS factorization direction. Applying the universal property to φ0 ∘ f and φ0 ∘ f⁻¹ gives inverse base morphisms, because φ0 is surjective. Thus φ0 is equivariant. Primitivity forces a three-dimensional base; connected fibers and characteristic zero make this generically finite contraction birational. The strict classification then leaves only X3 and X7.

Consequently, if a genuinely new target exists, the conjunction of rational c2-null nef-class existence and nef integral semiampleness must fail on it. Neither assumption is established by this package. The implication agrees with the published OWR conditional argument; it is not unconditional nonexistence.

The known examples' rigidity is an imported geometric fact. Contraction with the volume form identifies H¹(T_X) with H²,¹(X), so its vanishing excludes local deformations. The checker's invariant torus H²,¹ weights alone do **not** calculate the resolution's full Hodge theory. The package explicitly respects this distinction. No global deformation or singular-transition exclusion follows.

## 4. Reproducibility and adversarial tests

Run from any working directory:

`python3 audit_controls.py /path/to/frozen/public`

With no argument, the script uses the sibling `public` directory. It uses only the Python standard library. It reads the author package without modifying it and writes `audit_controls.json` beside the audit script. No PDF, network access, corpus, external service, or private record is needed.

Independent checks do not import the author's checker or reuse its polynomial determinant routine:

- All 98 cases m = 3,...,100: rational Gaussian elimination for determinants, two-sided inverse identities, four exact characteristic-polynomial evaluations, Cayley–Hamilton identity, and independent Sturm counts of one root in each of the three intervals.
- X7: cyclic convolution in Z[C7] modulo the sum-of-powers relation, the inverse sign, unit norm 1, elementary symmetric values, the cubic relation for all three conjugates, and the regular six-dimensional representation's characteristic polynomial (t³−5t²+6t−1)².
- Independent Sturm root counts in the three rational X7 intervals, giving the exact separation c < 1 < b < a.
- Ten mutated result records are rejected: determinant sign, characteristic polynomial, missing matrix, invalid interval, X7 symmetric value, inverse sign, reversed dynamical-degree ordering, even-dimensional weights, extra scalar order, and a torus H²,¹ weight.
- Three further algebra-level controls distinguish the omitted negative inverse sign, m = 2's root at the forbidden interval boundary, and the zero weight in even dimension.

An additional isolated replay copied only the seven frozen files and the audit script to a temporary tree and launched from an unrelated working directory. It passed without source or private directories. Separate corruptions of the proof bytes and the frozen manifest were both rejected before algebra replay.

Result: **98 independent matrix cases pass; 13 mathematical/result controls pass; two integrity corruptions are rejected; isolated portability passes; replay is byte-identical; frozen files are unchanged.** These are bounded exact-algebra checks, not machine verification of algebraic geometry or a proof search for new examples.

## 5. Scope, hygiene, and remaining limitations

There is no mathematical HOLD within the frozen partial scope. Publication must nevertheless preserve the unresolved/five-attempt/no-novelty status. No broad nonexistence claim, new primitive variety, or full-target promotion is supported.

The manifest allowlist, not a recursive directory copy, is the release boundary. A pre-existing `__pycache__/check_exact.cpython-312.pyc` is outside that allowlist and must be excluded. This audit did not create or alter it. Source PDFs and full extracted texts were consulted locally; none are included in this audit deliverable. The deliverable contains only this commentary, independent code, generated controls, and a manifest.

A fresh bounded search on the audit date found no primary-source solution to the exact target. The [May 2026 KIAS abstract](https://www.kias.re.kr/kias/activities/seminars/view.do?edate=&menuNo=404003&mjrcdnm=&pageIndex=1&sdate=2026-04-29&seqno=PGN1720260402-0006) is explicitly about birational Wehler dynamics; [Kaur–Prendergast-Smith](https://link.springer.com/article/10.1007/s11565-024-00506-8) likewise supplies a birational primitivity criterion. These do not close the regularity gap. Negative search is not a literature-completeness theorem.

The author's historical timestamps and earlier bounded repository-duplicate search are provenance records, not mathematical evidence; this audit did not independently rerun remote repository exploration. No remote mutation was performed. Future discoveries, non-isolated quotient actions, higher-rank crepant modifications, and unrelated varieties remain outside the proved exclusions.

**Final disposition: PASS_PARTIAL for the frozen obstruction/verification package; full target unresolved; no novelty; no new X; no full promotion.**
