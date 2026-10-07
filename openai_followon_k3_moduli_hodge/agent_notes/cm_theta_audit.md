# Independent CM theta and local-parameter audit

Checkpoint: **2026-10-06 21:36 PDT**. Auditor: priority-audit subagent. Scope completion: **100% of the assigned close-reading audit of `04-theta.tex` and `05b-satake-frobenius.tex`**. This is an audit-coverage estimate, not a probability that the entire CM theorem is true. The project's mathematical completion remains unresolved until the independent geometric Frobenius/Hecke and remaining CM assembly audits are reconciled.

## Verdict and limits

**No substantive gap found in the two assigned sections after close reading and attempted falsification of their covariance, fixed-input approximation, inverse-action, raw Satake, and valuation arguments.** Their conclusions remain dependent on the stated standard global Weil/unitary-splitting inputs and on the geometric Hecke/Frobenius setup in `05a-moduli.tex` and `05b-frobenius.tex`. In particular this note does **not** certify that the geometric Frobenius congruence holds for this PEL space, nor certify the complete upstream rational Hodge conjecture proof. The parent researcher is auditing those separate issues.

The sections correctly distinguish the circle-scalar unitary splitting from a double-cover lift, a pointwise theta-input limit from a common congruence level, the total fixed input from the later factorization into new rational summands, the inverse geometric Hecke action from the direct Weil action, and semisimplicity of a finite radial quotient from semisimplicity of ambient Hecke cohomology. These distinctions are doing mathematical work; dropping any of them would invalidate the shortcut proof.

## Exact sources and method

Read-only clone: `/Users/alec/Desktop/math`, pinned commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, public source https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-September-30-2026 . No upstream edits, contact, Git mutation, release, or publication were made.

All source paths below are under that preprint's `build/sections/`:

| Source | Bytes audited | SHA-256 |
|---|---|---|
| `04-theta.tex` | All 1,064 lines, with repeated reads of covariance, splitting, approximation | `c3c42f2820a8f42b7e1b4dda2e4c984336fde72b09f7683afb3bed9e64237027` |
| `05b-satake-frobenius.tex` | All 383 lines | `36aaa88e48f9c556daa5b474b37caa51607dd6f7453a5d9607ea07b7267f84f3` |
| `05c-cm-types.tex` | Read to check the immediate slope/Hodge boundary of the Satake calculation; no complete independent certification | `7cd65bc8883c6bf513c89e841ae85812be096354516c1b90f58e81b52cb5bd79` |

Also checked `05a-moduli.tex` good-prime/embedding labels, approximately lines 350–399; selected introduction, main inclusions, and bibliography. The external comparison used primary sources:

* Borade et al., https://arxiv.org/html/2402.16808v2 , sections 3.1–3.1.1 and 4.1–4.1.1. The local character restrictions and circle extension are explicit; the global extension is the restricted product modulo scalars whose product is one. The global lifting proposition states compatibility with the canonical rational symplectic section on rational unitary points. Thus the exact compatibility required by `04-theta.tex` is supported, rather than merely an unrelated existence of local splittings. The bibliography's published DOI is https://doi.org/10.1007/s00029-025-01047-4 .
* Bergeron–Millson–Moeglin, https://arxiv.org/html/1306.1515v2 , section 7.2 and Remark 7.3: adelic theta construction and determinant twists when the splitting characters change. Restricting to special unitary groups removes those twists. This was cross-checked with the circle-extension formulation above rather than using a blanket claim that the metaplectic double cover splits over every unitary group.
* Gross, *On the Satake isomorphism*, author PDF https://people.math.harvard.edu/~gross/preprints/sat.pdf , equation (3.14) and Proposition 3.6. The raw GL_n minuscule transform has factor q^{i(n-i)/2}; for n=3 the two noncentral generators both have factor q. The rationality assertion applies because rho=(1,0,-1) is integral on the relevant cocharacter lattice.
* Weil, 1964 original, https://webhomes.maths.ed.ac.uk/~v1ranick/papers/weil2.pdf . Inspected the linear-subgroup normalization and the cited original framework; the scan/OCR limits mean I did not independently rederive every global metaplectic theorem cited at I no.13, III no.41, IV nos.43–45. The use of the standard rational theta functional and paired lifts is an explicit remaining standard input, not an independently formalized result of this audit.

No claim here is based on a negative keyword search, a paper abstract, or a successful PDF build. No Lean build was run for this audit.

## Theta construction: checkable deductions

### Symplectic form, holomorphy, determinant, and tensor target

At `04-theta.tex:105–252`, with Hermitian forms linear in the first argument,

    psi(v tensor p, v' tensor p') = Tr_{E/F}(delta h_V(v,v') h_P(p,p')),
    c(delta) = -delta.

Swapping arguments conjugates the Hermitian product and negates the trace expression. Nondegeneracy follows from trace duality after varying the second argument by E scalars. The active positive filtration is

    F_mu = L tensor P_mu,
    F_cmu = Q^* tensor P_mu^*,   Q^* = ann(L).

The second expression is the holomorphic annihilator; replacing it with the metric orthogonal complement in V would introduce antiholomorphic dependence. The real positivity sign is realizable by weak approximation in F. At compact places a full one-sided embedding summand is selected with sign determined by d.

The determinant identity is

    det F_P = L^(2n) tensor C_P,
    (det F_P)^(1/2) = L^n tensor C_P^(1/2).

The constant factors have trivial **SU(V)** action, but are not discarded for scalar U(V) transformations later. For n=1 the c-mu projection of the first tensor has target L tensor Q^*=Omega_D^1; for n=2 the double-alternating second tensor has target L^2 tensor wedge^2 Q^*=K_D. The double alternation is well defined on a symmetric product because exchanging its factors reverses both exterior signs.

### Covariance and completion

At `04-theta.tex:378–518`, write J=CZ+D. The real Gaussian generator calculations give

    omega_infinity(g) f_(Z,z)
      = j(g,Z)^(-1) exp(-pi i z^t J^(-1) C z) f_(gZ,J^(-t)z),
    j(g,Z)^2 = det J.

I checked the upper unipotent, diagonal linear, and Fourier generator formulas and the composition identity for J^{-1}C. Rational invariance of the theta sum puts the **direct** transformed finite input on the left. Keeping the input fixed instead produces its **inverse** action, which is the convention used in the later geometric lemma.

The completion identity

    J^(-1) (Im(gZ))^(-1) J^(-t)
       = (Im Z)^(-1) - 2i J^(-1)C

cancels the Jacobi exponential. Hence T_k transforms as j Sym^k(J), with the positive filtration, not its dual. The quadratic completion has no linear term, so the projected T_1 is holomorphic. The whole completed T_2 need not be holomorphic; the paper only proves holomorphy after its prescribed projection at rational endpoint decompositions.

### Genuine finite stabilizers and global splitting

At `04-theta.tex:538–690`, the splitting characters must restrict to epsilon_{E/F}^{dimension}. The proof of their existence through extension from the closed idele-class subgroup is coherent: C_F embeds properly into C_E, with the norm-one kernel compact and norms restricting by squaring. The global unitary splitting input is exactly the primary result identified above. Determinant twists vanish on SU(V).

At infinity, on the active maximal compact subgroup the filtration determinant is ell^(2n), while compact SU(3) determinants are trivial. Its winding is even, so the SU(V) real-group action lifts to the double cover with square-root character ell^n. A circle lift and this double lift differ by a continuous character of a connected semisimple group, which is trivial. This supplies the rational covariance with the honest finite action. At a split finite place the normalized inverse-substitution action and the unitary action likewise differ by a character of SL_3; perfectness removes it. Outside SL_3 the bare-lift scalar remains necessary and is explicitly retained in the scalar-relation proof.

Smoothness of this honest finite action gives a common open stabilizer for any **finite** list of Schwartz inputs, and sufficiently deep principal congruence neighborhoods lie inside it. No false congruence-subgroup property is used.

### Cotangent span and nonzero rank-two form

At `04-theta.tex:700–765`, for a fixed period Z and fixed nonzero lattice point x_0, use

    phi_k = 1_(x_0 + k O_hat_F^3).

Its rational support is x_0+k O_F^3. The completed first tensor equals the ordinary theta gradient. For nonzero lattice m and sufficiently large k,

    ||x_0+km|| >= k ||m||/2.

The Gaussian tail therefore tends to zero and T_1(phi_k) tends to the nonzero scalar multiple of x_0 displayed in the text. Minkowski lattice vectors complex-span the first-tensor fiber. The span of actual values is closed because the fiber is finite dimensional. Thus actual inputs span, and finitely many actual ones can be selected before choosing a common principal level. The proof does **not** require a common level for the infinite limiting sequence.

At `04-theta.tex:832–908`, the normalized degree-two product coefficient has mixed coefficient one. The unmixed terms vanish under double alternation because they have both multiplicity vectors on the same line. The mixed term is the wedge of the two projected first tensors, up to the fixed constant-line trivialization. Since each line's one-form values span a two-dimensional cotangent fiber, one can choose independent values and obtain a nonzero top form. Factorization of an arbitrary finite Schwartz input on a rational direct sum into a finite sum of tensor products is justified by compact support and local constancy, not by an infinite tensor expansion.

### Fixed-total-input continuity and rational sign switch

At `04-theta.tex:910–1051`, the rational symplectic space W, the rational SU action, reference Schrödinger coordinates, finite Weil action, and **one total finite input phi** stay fixed. Only the compact-place positive multiplicity subspaces vary. The active total pieces stay exactly fixed. The compact-place determinant action remains trivial on SU(3), and the active determinant is ell^4 throughout. Therefore the same finite stabilizer gives descent to the same compact X throughout the neighborhood.

A finite precompact chart cover of X and a small compact parameter neighborhood give a common positive lower bound for Im Z and bounds for every fixed derivative order. The input's rational support remains in the same finite union of lattice cosets. A polynomial times a uniformly positive Gaussian is summable with all fixed derivatives. Projection and smooth constant-line frames preserve those bounds. This proves C-infinity continuity on the fixed quotient; it does not smuggle in changes of input, denominators, level, or Hecke correspondence as the approximation improves.

If d_1+d_2=d_3+d_4, the two sign multisets match at every compact pair. A local relabeling permits weak approximation of a chosen vector by one w in W(E). Its nonzero norm and sign are open conditions; the orthogonal complement varies continuously by the explicit projection formula. The active W_mu is definite, so no active-place approximation constraint is required and the active total filtration is unchanged. Consequently rational endpoint decompositions can approach the original total period data arbitrarily closely with the fixed phi. Starting from a nonzero holomorphic xi, the pairing integral with xi-bar is nonzero; continuity keeps the pairing with xi'-bar nonzero for sufficiently close rational endpoints. Only **after** these endpoints are fixed are their finitely many factor inputs taken to a common further level. An unramified finite cover multiplies the integral by its degree. I found no circular dependence of the input or level on the approximation limit.

## Local Hecke calculation: checkable deductions and geometric boundary

### Inversion and the radial module

At `05b-satake-frobenius.tex:34–108`, the active determinant-zero group is SL_3. Strong approximation for the simply connected special-unitary group with a noncompact active real factor allows a rational representative gamma with gamma_w in K_q g and all other components integral and marking preserving. For changed lattice g^{-1}Lambda, this gamma takes it to Lambda. The covariance identity

    gamma^* Theta(omega_f(gamma) phi) = Theta(phi)

then gives inverse action on a fixed input. If gamma_w=kg, K_q invariance implies omega(gamma_w^{-1})phi=omega(g^{-1})phi. Raw branch summation gives no degree divisor or extra q power. This inference is sound **provided the algebraic Hecke correspondence constructed in the geometric section has exactly these lattice branches and pullback convention**. This prerequisite is outside my full assigned audit.

SL_3(Z_q) is transitive on a fixed primitive-valuation shell. Local constancy at zero and compact support make its invariant Schwartz space the finite span of b_j=1_{q^j Z_q^3}; these functions are independent. For

    D_q b(x) = q^(3/2) b(q^{-1}x),

one has D_q b_j=q^(3/2)b_{j+1}, so the radial space is a cyclic Laurent module. This holds for the local inputs after separating finitely many adelic factors and averaging under the local compact group.

### Scalar relation, phases, and conjugate valuation

At `05b-satake-frobenius.tex:110–206`, principalizing w^m=(a) and putting r=a/bar(a) gives a norm-one scalar with valuation +M at w and -M at bar(w). Its units at the finitely many exceptional other places enter common open input stabilizers after a positive power. The argument uses **bare rational symplectic lifts**, rather than an arbitrary circle scalar; therefore the residual finite lift phases are roots of unity. The normalized local scalar action on a radial input is D_q^M, including q^{3M/2}.

At the active infinite place the filtration scalar exponents are (1,-1,-1): the determinant contributes -1, and the squared projected conjugate factor contributes -2. Total squared exponent is -3. At a compact selected full summand it is -3d(tau). The determinant's constant line is included; it is only SU-trivial. Covariance therefore yields

    D_q^M = omega on theta one-form classes,
    omega^2 = zeta product_tau tau(r)^(-3d(tau)).

Thus omega and all roots e_0^M=omega are algebraic and every complex conjugate has modulus one. The same M, r, omega can be chosen for a finite separated family using common stabilizers. This proof never assumes that such an algebraic number is a root of unity: it has deliberately nonzero q-adic valuations.

The good-prime labeling selects w=p_c, bar(w)=p_1. For g=sigma|_E,

    sum_tau d(tau) nu_iota(sigma tau(r)) = -M d(g^{-1}).

It follows that nu_iota(sigma e_0)=+3d(g^{-1})/2, hence for the **inverse geometric** parameter e=e_0^{-1},

    nu_iota(sigma e) = -3d(g^{-1})/2 = -3v(g)/2.

I checked the inverses and both signs against the prime labels. Switching either the Hecke inverse or w/bar(w) label changes the CM type; both are essential.

### Raw minuscule calculation and Satake parameter

At `05b-satake-frobenius.tex:218–339`, the quotient by D_q^M-omega is a sum of one-dimensional eigenspaces because the polynomial is separable and omega is nonzero. This is a statement about the radial quotient; it does not assert semisimplicity of Hecke acting on all cohomology.

The computational GL_3 extension is rho(h)b=|det h|^{-1/2}b(h^{-1}x). For i=1,2, raw minuscule right cosets correspond to sublattices between qLambda and Lambda of index q^i. There are q^2+q+1 each, and respectively q+1 or one contain a fixed primitive vector. This gives

    T_1 b_0 = q^(1/2)((q+1)b_0 + q^2 b_1),
    T_2 b_0 = q(b_0 + (q^2+q)b_1),
    T_3 b_0 = D_q b_0.

On D_q=e_0, b_1=q^{-3/2}e_0 b_0. The eigenvalues become q e_1(e_0,q^{1/2},q^{-1/2}), q e_2 of the same triple, and e_3. Gross's raw transforms are q e_1,q e_2,e_3; thus the direct parameter is {e_0,q^{1/2},q^{-1/2}}. Inversion sends it to its reciprocal: T_1^vee=T_3^{-1}T_2 and T_2^vee=T_3^{-1}T_1, with no degree factor. The active geometric projective parameter is therefore {q^{1/2},q^{-1/2},e_0^{-1}}. Restriction to determinant-zero GL_3 agrees with SL_3; rho=(1,0,-1) is integral, so scalar conjugation acts on the rational Satake character. The possible sign change of q^{1/2} is a common projective sign, leaving the third entry +/-sigma(e).

Independent exact finite-incidence enumeration was saved in `sources/downloads/priority_cm_radial_counts.json`. For primes q=2,3,5,7,11 it returns total planes/lines 7,13,31,57,133; planes through e_1 respectively 3,4,6,8,12; and one line through e_1 each. All asserted formulas pass. This computation checks only the lattice-incidence factors; it cannot validate the geometric congruence or global theta covariance.

Reproducer: enumerate nonzero triples in F_q^3, normalize the first nonzero coordinate to one, and take the resulting projective points. Points encode lines; normal points encode planes. A plane contains e_1 iff its normal's first coordinate is zero. A line contains e_1 iff its normalized vector is (1,0,0). Count and compare with q^2+q+1, q+1, and 1.

### Central finite order and downstream slope boundary

At `05b-satake-frobenius.tex:347–383`, T_3 has a unique lattice branch. A norm-one scalar with the required active valuations identifies a positive power of the changed lattice with the original and then a further power fixes the finite marking. For C_0 the ideal I selects one prime per conjugate pair, so I bar(I)=(q). If I^m=(a) then a bar(a)=q^m u for a totally positive F-unit u; b=a^2/u has the valuations of I^{2m} and b bar(b)=q^{2m}. This resolves the possible nonsquare unit without requiring it to be a norm. The same scalar preserves embedding filtrations in every Hermitian component. Its further powered marking is trivial. Consequently central actions are finite order on the full tuple space and its Albanese, **assuming those central correspondences are the lattice actions defined earlier**.

I read `05c-cm-types.tex` only to check how these output signs are used. Its central normalization gives b^3 e' a root of unity and all complex conjugates of b have modulus one. The cubic-root candidates are b q^{3/2}, b q^{1/2}, and q b e'; degree-one Weil weight picks b q^{1/2}. The resulting normalized slope is 1/2 - nu(e')/3, hence zero or one with exactly the prescribed v sign. The Hodge argument requires algebraic Hecke projectors preserving filtration; it applies weak admissibility both to a summand and its complement, rather than inferring Hodge type from Newton slopes alone. The text explicitly addresses this essential condition. The scalar-conjugate dimension check takes matrix ranks in an actual coefficient compositum, rather than identifying geometric conjugation with scalar conjugation. Those local transitions were coherent. Their upstream Frobenius polynomial and algebraic-projector realization remain separate prerequisites.

## Falsification checklist and next decision

| Attempted failure | Result in assigned source | Exact outstanding boundary |
|---|---|---|
| Positive filtration dualized or antiholomorphic | Tensor target and ann(L) are consistent | Standard real Gaussian representation |
| Global splitting only projective or rationally incompatible | Circle formulation and canonical rational compatibility explicitly supported by primary theorem | Standard unitary global lifting theorem is assumed |
| Infinite sparse-input limit granted a common level | Finite actual inputs selected first | None found in this inference |
| Approximation changes input/denominator norm or requires unrelated levels | Total W, finite action, phi, and X fixed throughout | No quantitative approximation bound claimed or needed |
| Quadratic completion falsely declared holomorphic | Only double-alternating rational endpoint projection is used | None found |
| Geometric Hecke has direct rather than inverse action | Covariance yields inverse; the proof keeps raw branch sum | Must verify actual PEL correspondence matches lattice branch convention |
| Missing Satake degree/modulus factor | Explicit incidence and Gross normalization agree | Geometric Frobenius congruence itself unverified here |
| Rational scalar phase is arbitrary complex character | Bare paired lifts retain finite Weil phases; square weight computed | Full original Weil theorem treated as standard input |
| Wrong Galois inverse or w/bar(w) label | Checked -3v(g)/2 output | Correct prime labels must remain unchanged downstream |
| Ambient Hecke semisimplicity silently assumed | Only radial quotient diagonalized | Remaining generalized-character extraction separate |
| Central polarization unit requires unavailable square root | a^2/u construction works | Central PEL tuple action must have asserted multiplier convention |

Recommendation to parent: **Do not stop the program because of a defect in these two sections on this audit's evidence. Do not promote the upstream CM theorem solely on this scoped pass.** Reconcile the separate geometric Frobenius congruence audit, algebraic Hecke/projector realization, CM-type rational descent, and final algebraicity assembly before regarding the all-base K3 result as proved. The priority audit independently says the moduli corollary has low incremental originality even if the upstream chain succeeds.
