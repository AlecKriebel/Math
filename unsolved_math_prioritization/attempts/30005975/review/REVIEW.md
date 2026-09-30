# Independent review: tame stacky-curve Brauer partial (30005975)

**Verdict: PASS_SCOPED_TAME_FORMULA_AND_GERBE_DIAGNOSTICS.** No mandatory correction. The full original question remains **unsolved, 3/5**.

Reviewed artifact: `PARTIAL.md`, SHA256
`27e178e2c1b22e8e18ab32c3ff117ac4b4672dc7b799f2d18fd3d2a019fad51a`.

This is an independent AI mathematical/source review, not human peer review or a priority certification. The reviewer used its inherited runtime without changing settings; its exact model identifier was not exposed.

## 1. Original scope and sources

The original OWR40/2024 contribution defines a stacky curve as a separated finite-type algebraic stack, pure of dimension one, with finite inertia. Question1 is on printed p.2337; the definition and cohomological Brauer convention occur on p.2336. I read the complete relevant contribution and visually checked the question page. Its scope includes tame non-DM stabilizer group schemes and generic inertia. The artifact correctly uses the torsion subgroup of lisse-etale H²(Gm), with the standard smooth-coefficient fppf comparison, and makes no general Azumaya comparison claim.

I checked Achenjang v3 Corollary2.16, Propositions3.8–3.9 and4.3–4.4, Bishop v2 conventions1.3, Theorem2.7 and Proposition3.7, and Stacks Tag0ADD. The later Bishop–Newman and Lopez papers have narrower or different hypotheses and do not justify promoting this package to a general solution. These source theorems are credited inputs; this review audits their application, not every proof in those papers.

## 2. Dense schematic-open formula

### Local coprime-torsion step

The quotient presentation required by Achenjang Corollary2.16 has a strictly henselian local finite cover and an actual finite linearly reductive group scheme G, with trivial residue-field action. Over the algebraically closed base the residue field at a closed point is k. In characteristic p, its connected part Delta is diagonalizable of p-power order and its etale quotient Q has order prime to p. These are group-scheme facts, not statements about geometric point counts.

Proposition4.3 gives H²([Spec A/Delta],Gm)=0 and annihilates its Picard group M by |Delta|. In Proposition4.4 the relevant source in the exact tail is M^Q. This is still annihilated by |Delta|. Its image in H²(Q,k×) is also annihilated by |Q|, by finite-group transfer. Bezout therefore kills that image: if u|Delta|+v|Q|=1, every image element b equals u|Delta|b+v|Q|b=0. Hence the asserted isomorphism follows, not merely a surjection. In characteristic zero M=0. Functorial restriction to the residual gerbe identifies the same Q and group-cohomology term.

### Global spectral sequence

The separated finite-type coarse algebraic space has local dimension at most one; Tag0ADD therefore makes it a scheme. The coarse map satisfies c_*Gm=Gm, since invertible invariant functions descend. The dense open meets all components, so its closed complement is a finite set of closed k-points.

For q>0, the sheaf R^q c_*Gm restricts to zero on that open. A sheaf supported on a finite closed set is the pushforward of its restriction to that set, as can be checked on geometric stalks. The etale topoi of the algebraically closed points have no higher cohomology, and closed pushforward is exact. Thus H^p(C,R^q c_*Gm)=0 for p,q>0. Bishop's stated curve Tsen theorem supplies H^p(C,Gm)=0 for p>=2, including the singular/nonreduced case used here.

For total degree two only E_2^(0,2) remains. Its possible outgoing differentials are d_2 to (2,1) and d_3 to (3,0), both zero; higher targets have negative second degree and there are no incoming differentials. Hence the direct sum of local H²(Q_i,k×) is exactly H²(X,Gm). The finite Schur multipliers make this finite prime-to-p torsion, as claimed. Connected tame inertia produces no extra local p-primary term in this setting.

The dense **schematic** open is indispensable. Without it the higher pushforwards need not have finite support, and the argument does not compute their cohomology or transgressions.

## 3. The two generic-gerbe examples

The stacks have the same coarse P¹ and the same geometric stabilizer mu_l times mu_l, with l invertible. They are proper tame DM stacks. The root construction is a gerbe of roots of a line bundle, not a divisor root stack.

For Y=root_l(O(1)/P¹), the tautological weight-one line bundle L satisfies l[L]=pi*[O(1)]. The character-weight sequence shows

    Pic(Y) = (Z H + Z L)/(l L−H) = Z,

and its units are k×. Since k× is l-divisible, Kummer gives H¹(Y,mu_l)=Pic(Y)[l]=0. Choosing mu_l=Z/l is legitimate over this algebraically closed field. The cyclic-gerbe pushforwards R¹=Z/l and R²=0, together with H²(P¹,Gm)=H¹(P¹,Z/l)=0, give H²(Y,Gm)=0. Applying the same cyclic calculation over Y then gives H²(Y times Bmu_l,Gm)=0.

As a separate check on the neutral value, start instead with Y_0=P¹ times Bmu_l. The split cyclic classifying-stack sequence gives H²(Y_0,Gm)=0, but Pic(Y_0)=Z plus Z/l. Kummer now gives H¹(Y_0,mu_l)=Z/l. A second cyclic classifying-stack calculation gives H²(Y_0 times Bmu_l,Gm)=Z/l. This independently recovers the neutral answer without the submitted relative-P¹ spectral-sequence route. It agrees with the alternating Schur commutator calculation.

These examples demonstrate dependence on the global gerbe class. They do not provide a classification of arbitrary bands, nor contradict the dense-schematic-open theorem.

## 4. Connected generic inertia and Artin–Schreier normal form

For Z=A¹ times Bmu_p in characteristic p, diagonalizability makes mu_p linearly reductive although it is not etale. Achenjang Proposition3.9 applies to this connected cyclic group and gives H²(Z,Gm)=H¹_et(A¹,Z/p), since the scheme Brauer term vanishes. The Artin–Schreier sequence and affine coherent-cohomology vanishing identify this with the additive quotient k[x]/(F−1)k[x]. It is not a quotient by an ideal.

I independently checked the normal form by an explicit monomial telescoping identity. For a term a x^(d p^j), where p does not divide d, set b_i=a^(p^(−i)). Then

    (F−1) sum_(i=1)^j b_i x^(d p^(j−i))
       = a x^(d p^j) − a^(p^(−j)) x^d.

This gives the proposed representative and an explicit reduction certificate. Constants vanish over the algebraically closed field by surjectivity of a->a^p−a. If a nonzero reduced positive-degree polynomial were h^p−h, its leading degree would be divisible by p, a contradiction. Thus the normal form is unique. Frobenius-root additivity makes the identification F_p-linear; no k-linearity is asserted.

The finite-field controls intentionally retain the warning that constants are not all Artin–Schreier differences in a finite field. That finite-field limitation does not apply to the algebraically closed base of the theorem. Effective computation for arbitrary k would require effective field operations and Frobenius roots, as the artifact states.

## 5. Independent controls and limitations

All **77,458** submitted assertions replayed with a byte-identical receipt. The separate checker passes **40,882** exact assertions. It uses:

- Bezout annihilator certificates rather than enumerating only possible cyclic images
- Picard Smith invariants for root_l(O(d)), including the neutral and O(1) cases
- associativity of finite Heisenberg extensions and their commutators
- closed-form Artin–Schreier monomial telescoping over F8, F27 and F25, including4,500 polynomial cases
- explicit finite-field constant-surjectivity countercontrols
- total-degree-two Leray differential bookkeeping

The controls do not prove the imported stack-local structure or Tsen theorems. The mathematical audit above explains exactly how those inputs are used. No unresolved gap was found in the stated partial claims. Preserve the original status **unsolved3/5** and all generic-inertia, non-DM and cohomological-Brauer qualifications.

### Sources

- Original report: https://ems.press/content/serial-article-files/50042
- Achenjang v3: https://arxiv.org/abs/2410.06217v3
- Bishop v2: https://arxiv.org/abs/2507.08780v2
- Schematic locus: https://stacks.math.columbia.edu/tag/0ADD
- Later nodal scope: https://arxiv.org/abs/2509.20629v3
- Later semisimple-group scope: https://arxiv.org/abs/2601.05370v1
