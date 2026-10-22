# Independent adversarial audit: characteristic-free surface Lemmas A/B

**Verdict:** Lemmas A and B are mathematically sound under their printed hypotheses. No material objection or remaining mathematical gap was found in the assigned surface scope. The strongest verified conclusion is the nonvanishing of the conductor adjoint space H^0(S,c(e-2)) for every integral degree-e surface S in P^3 over an algebraically closed field, e>=2; its nonzero section lifts to the claimed polynomial vanishing on every reduced singular curve.

This is a proof audit using standard theorems, direct deductions, explicit boundary examples, and limited finite controls. It is not a claim of novelty, a complete audit of sections C/D, or a global literature determination.

## Provenance and independence

- Target: problem 30002792, OWR-13494-011; original PR 293 head supplied by root: `6e717193f93c8a321cce1ce35a00eed1ecfb56e7`.
- Read only `original/PUBLIC_TURN_2.md` and `original/source_record.json` from the pinned source package.
- Recorded `INDEPENDENT_DERIVATION.md` before primary-source verification. No original `final_review`, fresh review, other ongoing agent, or other chat was consulted.
- All writes are in this assigned review directory. No checkout/index/branch operation, commit, push, release, remote mutation, or contact with an individual occurred. Read-only public source retrieval was used. The root's ledger search was supplied context and was not independently repeated here.

## Exact audited claims

**A.** If X is a smooth integral projective surface over an algebraically closed field, H is nef, H^2=e>=2, and |H| contains an integral curve C, then H^0(X,omega_X(2H)) is nonzero.

**B.** If S is an integral surface of degree e>=2 in P^3 over that field, there is a nonzero polynomial of degree e-2 vanishing on every reduced singular curve of S.

The characteristic is arbitrary. No separability of the Albanese map, curve map, or conductor restriction is assumed. The integral representative is required in A. A general plane, rather than an arbitrary plane, is used in B.

## A: independent verification

### Picard smoothness is justified

When pg>0, multiplication by the square of a defining section of C directly proves A. When pg=0, Serre duality gives H^2(O_X)=0.

For a square-zero extension of Artin k-algebras, the kernel in the units sequence is the additive sheaf O_X tensored with the extension ideal. The obstruction to lifting an invertible sheaf therefore lies in H^2(O_X) tensored with that ideal and vanishes. The locally finite type Picard scheme is formally smooth, hence smooth. Its tangent space is H^1(O_X); the reduced identity component is dual to Alb(X), so q=dim Alb(X).

This implication does not assume characteristic zero. It appears explicitly in the cited [Liedtke notes, printed pp. 13–14](https://cims.nyu.edu/~tschinke/books/simons12/lectures.pdf). More precise direct support is [Kleiman, Proposition 5.19, printed p. 47](https://arxiv.org/pdf/math/0504020), together with Corollary 5.13 (p. 44) and the Albanese construction in Remark 5.25 (p. 51). The complete relevant statements and lifting proof were read, not merely a search snippet.

### The big-nef curve generates the Albanese, including inseparably

Choose the base point on the normalization Cn of C. Its map into A=Alb(X) factors through its Jacobian. Let B be the image abelian subvariety and b:X->A/B the quotient map. Then b|_C is constant, including as a morphism: C is reduced, and equality after its dominant normalization implies equality on C.

For an ample M on A/B, N=b^*M is nef and N.H=N.C=0. Since H^2>0, algebraic Hodge index implies N^2<=0 with equality only for N numerically trivial; nefness gives N^2>=0. This exact positive-square formulation is [Bădescu, Corollary 2.4, printed p. 18, official preview](https://page-one.springer.com/pdf/preview/10.1007/978-1-4757-3512-3_2). The chapter explicitly works in arbitrary characteristic. In particular, it does not require H to be ample.

If b were nonconstant, a curve on X maps nonconstantly to b(X), and its normalized finite map onto its image has positive degree, whether separable or inseparable. The degree of N on that curve is therefore positive. This contradicts numerical triviality. Thus b is constant. The quotient homomorphism A->A/B and the zero homomorphism agree after composition with the based Albanese morphism; uniqueness in its universal property makes the quotient zero. Hence B=A.

It follows that q<=g(Cn)<=pa(C). The second inequality is the normalization exact sequence: the difference is the length of a finite quotient. No injectivity statement on tangent spaces or differentials of Jacobians is used.

### Riemann–Roch and duality have the right signs

Set g=pa(C). Adjunction gives K_X.H=2g-2-e. In the pg=0 branch,

chi(omega_X(2H))
=1-q+((K_X+2H).2H)/2
=1-q+K_X.H+2e
=e+2g-1-q
>=e+g-1>=1.

Moreover h^2(omega_X(2H))=h^0(O_X(-2H))=0: an effective divisor of class -2H would have negative intersection -2e with nef H, and a nowhere-vanishing section would force H^2=0. Therefore h^0=chi+h^1>=1. In fact the audited argument proves h^0>=e+pa(C)-1 in this pg=0 branch.

There is no omitted vanishing theorem here. The standard algebraic RR, Serre duality, and arithmetic adjunction formulas were checked against Liedtke, printed pp. 17–18.

## B: independent verification

### Resolution is projective and has finitely many relevant centers

Finite type schemes over a field are excellent, so normalization nu:Y->S is finite. A normal surface is regular in codimension one and Cohen–Macaulay, and its singular locus is a finite set of closed points. [Stacks, Theorem 54.14.5, tag 0BGP](https://stacks.math.columbia.edu/tag/0BGP) constructs the resolution through normalized blowups. Its proof and [Lemma 54.6.5, tag 0BFZ](https://stacks.math.columbia.edu/tag/0BFZ) permit the centers to remain over those finitely many singular points. The blowups are projective; their normalizations are finite in this setting. Hence q:X->Y can be projective and an isomorphism over Y_reg, and X is smooth projective over the perfect field k. Its contracted curves have only finitely many images in S.

This step uses resolution of surfaces, which is available in positive characteristic. It does not invoke unresolved higher-dimensional resolution.

### The pulled-back plane section is integral

The hypotheses of [Stacks Lemma 37.32.3, tag 0G4C](https://stacks.math.columbia.edu/tag/0G4C) hold for the hyperplane embedding of S: it has no base points, and two suitable planes cut a nonempty codimension-two subscheme. Hence a general plane section E is geometrically irreducible. Apply [Lemma 33.47.3, tag 0FD4](https://stacks.math.columbia.edu/tag/0FD4) to the smooth open S_reg, whose map to P^3 is an immersion. It gives generic reducedness on E. The plane curve E is a hypersurface, so it is Cohen–Macaulay and has no embedded associated points; E is therefore integral. A general E is not contained in S_sing.

Intersect this nonempty open condition in the dual projective space with the open condition of avoiding the finite images of q's exceptional curves. Over algebraically closed k this intersection is nonempty. Put f=nu q and C=f^*E.

Every curve component of C must dominate E, because all f-contracted curves have been avoided. Over the generic point of E, the morphism f is an isomorphism (that point lies in S_reg). Thus C has exactly one component and multiplicity one. The Cartier divisor C on smooth X is Cohen–Macaulay and has no embedded associated points; generic reducedness then implies reducedness. This proves C integral. The no-embedded-point principle is explicitly supported by [Stacks 31.4.3–4, tag 05AJ](https://stacks.math.columbia.edu/tag/05AJ).

No smooth Bertini claim for |H| on X is needed. Inseparable behavior where E meets the conductor can affect individual fibers but does not create another divisor component or generic multiplicity.

### Canonical sheaves and the conductor

Over Y_reg the resolution is an isomorphism. A section of omega_X restricts injectively to a rational top form regular on Y_reg. For normal Y its canonical sheaf is reflexive and equals the extension from Y_reg. Hence q_*omega_X injects into omega_Y. The S2 property of the dualizing sheaf and the normal-domain reflexivity criterion were checked in [Stacks tag 0AWH](https://stacks.math.columbia.edu/tag/0AWH) and [tag 0AVB](https://stacks.math.columbia.edu/tag/0AVB).

The cited [Kollár, with appendix by Dao, Definition 46 and equation (48.1)](https://arxiv.org/html/1811.00042v2) gives the conductor and normalization-duality formulation. Its finite-map codimension condition (18.2) is satisfied here. To remove any possible ambiguity between that paper's TfS2-dualizing sheaves and the actual canonical sheaves, the ordinary finite-duality statement follows directly from [Stacks tag 0AX2](https://stacks.math.columbia.edu/tag/0AX2): the dualizing complexes of the two Cohen–Macaulay surfaces are omega_S[2] and omega_Y[2]; the degree -2 cohomology of finite derived Hom gives

nu_*omega_Y=Hom_S(nu_*O_Y,omega_S).

For a finite birational extension A subset B of domains in the same fraction field, every A-linear map B->A is multiplication by an element c of that field. Since 1 belongs to B, c belongs to A, and the condition is cB subset A. Thus Hom_A(B,A) is precisely the conductor. As omega_S is invertible, the displayed sheaf is c tensor omega_S. This is finite duality, not a separable trace argument.

For the hypersurface S, omega_S=O_S(e-4). Projection formula therefore injects f_*omega_X(2H) into c(e-2). Since H=f^*O_S(1) is nef, H^2=e by the birational projection formula, and |H| contains the integral C just established, A supplies a nonzero section of c(e-2).

### Vanishing holds on the whole reduced singular curve

If D is any reduced integral singular curve, its generic local ring is a one-dimensional nonregular Noetherian local domain. A normal such domain is a DVR and regular; see the actual statement and proof of [Stacks tag 00PD](https://stacks.math.columbia.edu/tag/00PD). Thus S is nonnormal at that generic point. A conductor element invertible there would imply equality with its normalization, impossible.

It follows that c is contained in the prime ideal of D at its generic point. The image of any local section of c in O_D is zero generically; since D is integral, it is zero everywhere. Hence c is contained in I_D as a sheaf, not merely set-theoretically at generic points. The argument works for every singular curve and does not require a reduced conductor.

Finally the hypersurface exact sequence twisted by e-2 has kernel O_{P^3}(-2). [Stacks Lemma 30.8.1, tag 01XS](https://stacks.math.columbia.edu/tag/01XS) gives H^1(P^3,O(-2))=0, so the nonzero section lifts to a nonzero polynomial. Its restriction belongs to every I_D(e-2), proving B exactly as stated.

## Adversarial outcomes and reasonable clarifications

No attempted counterexample satisfies the printed hypotheses and defeats the conclusion. `EXPLICIT_CONTROLS.md` records sharp failure at e=1, failure at e=0, attainment at the smooth quadric, a nef nonample blowup example, the nonreduced-Picard boundary, and a family with genuinely inseparable conductor.

Only optional expository refinements are recommended:

1. Cite Kleiman Prop. 5.19 and Bădescu Cor. 2.4 explicitly, rather than broad chapter references.
2. State that the nonempty open conditions on E are intersected in the dual projective space, and spell out the Cohen–Macaulay/no-embedded-point implication once.
3. After generic conductor vanishing, add the integral-curve restriction argument to make vanishing on the entire reduced curve explicit.
4. If desired, replace the curve-existence sentence in A with: a suitable power of M is very ample; a hyperplane cutting b(X) properly and nontrivially pulls back to a nonzero effective divisor, which has positive degree against an ample divisor on X, contradicting numerical triviality.

These are readability improvements, not repairs of a material mathematical defect.

## Evidence classes and remaining scope

- **Standard theorem inputs:** surface resolution; Picard representability and duality; Jacobian universal property; Hodge index; RR, adjunction, Serre duality; Bertini for an immersion; finite canonical duality; hypersurface adjunction; projective-space cohomology.
- **Checked deductions:** q<=g(Cn)<=pa(C), positivity of the Euler characteristic, integrality of C, canonical injection, conductor containment in every singular-curve ideal, and the polynomial lift.
- **Explicit mathematical controls:** the families and boundary examples in `EXPLICIT_CONTROLS.md`.
- **Finite controls:** `finite_controls.py` and its recorded output `FINITE_CONTROLS.json`, in characteristics 2,3,5,7,11,13. They check examples only and carry no universal proof burden.
- **Exact remaining gap in A/B:** none found. Independent audits of the line-configuration reduction/ACM argument and a current novelty/priority determination remain outside this assigned surface review.

Audit completion estimate for the assigned surface review: **100%**.
