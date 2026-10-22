# Independent audit B: compact three-class anti-invariant counterexample

Date: 2026-10-07 UTC. Target: problem 30004549 / OWR-2654829-012, integrability clause.

## Verdict and exact scope

**ACCEPTED AS A FULL COUNTEREXAMPLE TO THE STATED INTEGRABILITY CLAUSE.**

The construction in the pinned candidate supplies a smooth, closed, connected real four-manifold and a smooth nonintegrable almost-complex structure with at least three independent real de Rham classes represented by closed anti-invariant two-forms. No correction to its mathematics is required by this audit. The generic-vanishing clause is a separate, previously proved theorem. This verdict is a mathematical audit of the argument, not a claim of novelty, journal acceptance, or formal proof-assistant verification.

Audited candidate:

- Basename: `R3_counterexample_candidate.md`
- Size: 9997 bytes
- SHA-256: `50a267656e6a5412a2e14208ada5aec203df4c5385be63b831029188cb1cf39e`
- This audit read the entire frozen candidate, independently derived the local formulas, and checked primary sources. No other reviewer's report or acceptance conclusion was used.

## 1. Compact surface and initial classes

Let C denote the smooth compact double cover of the projective line defined in affine coordinates by y^2=z^6-1. The six zeros are simple, the polynomial is not a square, and the cover is connected. Six branch points give 2g(C)-2=2(-2)+6=2, hence genus two. There are two unramified points over infinity.

The two differentials eta_0=dz/y and eta_1=z dz/y are globally holomorphic. At a finite branch point, y is a local coordinate and differentiation of y^2=z^6-1 gives dz/y=dy/(3z^5), a regular nonzero multiple of dy. At infinity, with s=1/z and Y=y s^3, one has Y^2=1-s^6 and Y(0)=+1 or -1. Consequently eta_0=-s ds/Y and eta_1=-ds/Y are regular. Their ratio is the nonconstant function z, so they are complex-linearly independent.

For the elliptic curve T=mathbb C/(mathbb Z+i mathbb Z), dw is global and nowhere zero. Thus M=C x T is a smooth closed connected complex surface, and Omega_0=eta_0 wedge dw and Omega_1=eta_1 wedge dw are independent holomorphic two-forms. The candidate's use of the letter C in the displayed quotient for T is understood as the complex number plane, not the already named curve; this is only a harmless typography ambiguity.

For completeness, the three classes can be certified without a dimension count. A real combination

h=a Re(Omega_0)+b Im(Omega_0)+c Re(Omega_1)

is closed and self-dual for a product Hermitian metric. If h is exact, Stokes' theorem gives integral_M h wedge h=0. Self-duality gives h wedge h=|h|^2 vol, so h vanishes. Since h is the real part of the (2,0)-form (a-i b)Omega_0+c Omega_1, distinct bidegrees force that complex form to vanish, and independence gives a=b=c=0. This also verifies the candidate's equivalent harmonic-form argument.

## 2. The simultaneous local normal form

The point z=0,y=i is unramified, and y is holomorphic and nonzero on a sufficiently small chart. A local lift w of the elliptic coordinate exists around w=0. The change zeta=z, xi=w/y(z) has determinant 1/y(z), which is nonzero. In particular,

dzeta wedge dxi=(dz/y) wedge dw=Omega_0,

and Omega_1=zeta Omega_0. Writing zeta=u+i v and xi=x+i t gives

alpha=du wedge dx-dv wedge dt,
beta=du wedge dt+dv wedge dx,
gamma=u alpha-v beta.

The sign in the third identity is correct. Both alpha and beta are a frame on this chart even though their global extensions can vanish on other fibers.

## 3. The cutoff preserves the third form exactly

Fix a smooth cutoff rho compactly supported inside a coordinate ball B, equal to one on an open neighborhood of the origin. Let R=epsilon rho x^2/2. Both R dv and R v dv vanish on a collar of the boundary of B, so their zero extensions are globally smooth one-forms.

The three perturbed forms alpha, beta'=beta+d(R dv), and gamma'=gamma-d(R v dv) are therefore globally defined and closed, with exactly the original cohomology classes. No appeal to approximate closure or continuity of cohomology is involved.

Since d(R v dv)=v dR wedge dv=v d(R dv), the exact relation gamma'=u alpha-v beta' holds throughout B, including the entire transition region of the cutoff. Terms involving derivatives of rho do not spoil it. This is the decisive feature of the construction.

## 4. Positive plane, explicit realization, and global gluing

Use V=du wedge dv wedge dx wedge dt. Direct expansion gives

beta'=du wedge dt+(1-R_x)dv wedge dx-R_t dv wedge dt+R_u du wedge dv,
alpha^2=2V,
alpha wedge beta'=R_t V,
(beta')^2=2(1-R_x)V.

Consequently the wedge Gram matrix in the frame (alpha,beta') is

[[2,R_t],[R_t,2(1-R_x)]],

whose determinant is 4D for D=1-R_x-R_t^2/4. The sufficient bounds |R_x|<=1/4 and |R_t|<=1 give D>=1/2; fixed compactly supported rho makes these bounds available for all sufficiently small nonzero epsilon. The derivative R_u does not enter the determinant, so there is no omitted positivity condition on it.

Set q=R_t/2 and a=sqrt(D). Then B_0=(beta'-q alpha)/a has alpha wedge B_0=0 and B_0^2=alpha^2. The candidate's decomposable-form argument is correct. Here is an additional explicit coframe, valid even in the cutoff region:

phi_1=du-q dv+i a dv,
phi_2=dx+(i/a)(dt-q dx+R_u dv).

Its product is alpha+i B_0. Its four real constituent one-forms have nonzero determinant, in fact determinant one relative to (du,dv,dx,dt). Declaring phi_1 and phi_2 to be of type (1,0) therefore gives a unique smooth real almost-complex structure. This explicitly verifies existence and fixes the sign without an unproved positive-plane correspondence.

Where R vanishes identically near the boundary, q=0, a=1, R_u=0, and this is the original complex coframe. Setting J=J_0 outside B gives a globally smooth J. The construction uses no normalization at zeros of Omega_0 outside B. On B, alpha and beta' lie in the real (2,0)+(0,2) plane, and the exact third-form identity puts gamma' in that same plane. Outside B all three are their original anti-invariant forms. The independent classes proved above therefore give h_J^- >= 3.

All parameters and all derivatives vary smoothly in epsilon while D stays bounded below, proving the stated C-infinity convergence to J_0 as epsilon tends to zero.

## 5. Nonintegrability

On the open core where rho=1, set k=1-epsilon x and a=sqrt(k). The coframe simplifies to

phi_1=du+i a dv, phi_2=dx+i a^(-1)dt.

For k'=-epsilon, direct exterior differentiation gives

dphi_1 wedge phi_1 wedge phi_2=(k'/(2k))V.

This is nonzero for every nonzero epsilon. Under integrability, d of a (1,0)-form has no (0,2) component, and wedging it with the (2,0)-form phi_1 wedge phi_2 must give zero in complex dimension two. Thus the candidate's first obstruction is valid.

Independently, the coframe gives J partial_u=a^(-1)partial_v, J partial_v=-a partial_u, J partial_x=a partial_t, and J partial_t=-a^(-1)partial_x. With N(X,Y)=[JX,JY]-J[JX,Y]-J[X,JY]-[X,Y], the coordinate bracket calculation yields

N(partial_u,partial_x)=(a'/a)partial_u=-epsilon/[2(1-epsilon x)] partial_u.

It equals -epsilon/2 partial_u at the origin. The two tests agree in sign and normalization with the frozen candidate.

## 6. Reconciliation with nearby restrictions

The metric-related hypothesis is materially stronger than closeness or tameness. At a core point with x nonzero and epsilon x nonzero, suppose a metric g were compatible with both J_0 and J. On the invariant real plane spanned by partial_u,partial_v, compatibility with J_0 gives g_uu=g_vv. Compatibility with J gives g_uu=a^(-2)g_vv. Since a^2=1-epsilon x is not one and g_vv>0, this is impossible. There is no common compatible metric, so the metric-related deformation bound in Draghici-Li-Zhang, Theorem 1.1, does not exclude this construction.

Nor are the real and imaginary parts of the normalized complex volume form both closed. On the core,

d(beta'/a)=epsilon/(2a^3) dx wedge du wedge dt,

which is nonzero. Thus the usual closed complex-volume integrability argument does not apply. The two closed forms alpha,beta' need a nonconstant normalization to constitute a complex-volume pair.

The source's restriction for tamed examples with b^+<=3 also causes no problem. The Kähler product of a genus-two curve and an elliptic curve has h^(2,0)=2 and b^+=1+2h^(2,0)=5. Its canonical bundle is not trivial: eta_0 has zeros on the two fibers over infinity. The construction is not asserted to retain a fixed compatible symplectic form. Sufficiently small deformations are tamed by the original Kähler form, which is an open condition and is consistent with the bound h_J^-<=b^+-1=4.

## 7. Primary-source and literature verification

- [OWR 33/2020, publisher PDF](https://ems.press/content/serial-article-files/46869?nt=1), DOI [10.4171/owr/2020/33](https://doi.org/10.4171/owr/2020/33): the printed page 1687, PDF page 31, was read as text and visually inspected after rendering. Conjecture 2.5 is the unrestricted compact real four-dimensional implication under audit. There is no product exclusion, fixed-metric condition, or real-analytic requirement attached to it. The neighboring generic-vanishing question is separate. The preceding and following pages were also checked for context.
- [Draghici-Li-Zhang, arXiv:1104.2511v1](https://arxiv.org/abs/1104.2511): Conjecture 2.5 agrees with that target. Theorem 1.1 is the metric-related special case addressed above. Its assumptions cannot be silently extended to all small deformations.
- [Tan-Wang-Zhang-Zhu, On Cohomology of Almost Complex 4-Manifolds](https://link.springer.com/article/10.1007/s12220-014-9477-2), J. Geom. Anal. 25 (2015), 1431-1443: Theorem 1.1 in [arXiv:1112.0768v3](https://arxiv.org/pdf/1112.0768v3) proves that h_J^-=0 is open and dense in the C-infinity topology on all almost-complex structures of a closed four-manifold admitting them. Publisher metadata gives first publication 21 March 2014 and issue date July 2015. The fourth author Peng Zhu should not be omitted when giving a full author list.
- [Lejmi-Upmeier, arXiv:1507.00282](https://arxiv.org/abs/1507.00282): the current abstract page explicitly records withdrawal in September 2015 because Proposition 14's proof has a crucial sign error. Its unchanged abstract claiming integrability must not be treated as an accepted proof. It is not used to justify the counterexample.
- [Hind-Tomassini, On the Anti-invariant Cohomology of Almost Complex Manifolds](https://link.springer.com/article/10.1007/s12220-020-00461-8), with [author PDF](https://academicweb.nd.edu/~rhind/anti-invariant-2019-09-19.pdf): the compact four-dimensional construction there is on the Kodaira-Thurston manifold with maximum anti-invariant dimension two. The other higher-dimensional and noncompact examples do not establish this compact three-class example.
- [Sillari, Real analytic curves of almost complex structures (2026)](https://link.springer.com/article/10.1007/s00209-026-03991-z): its introduction continues to identify the generic-vanishing clause with the Tan-Wang-Zhang-Zhu theorem. It supplies no same counterexample in the inspected discussion.

Searches included the exact conjecture, three independent anti-invariant forms, Draghici-Li-Zhang integrability, compact counterexamples, genus/product constructions, compactly supported deformations, and dated 2023-2026 combinations. No same compact three-class counterexample or additional assumption defeating this one was located. This is a bounded negative search result only: novelty and absence from all literature remain unestablished. Mathematical acceptance here rests on the complete explicit construction, not on search silence.

## 8. Computational check and final disposition

The independently written `check_local_algebra.py` passed using SymPy. It checks the wedge Gram identities, the third-form differential relation, decomposability, the explicit full-transition coframe, J^2=-Id on the core, and the stated Nijenhuis component. It uses symbolic identities, not random numerical sampling. The mathematical reasoning above also verifies the global steps that this script does not address.

**Required mathematical corrections: none.**

**Accepted conclusion:** the integrability clause is false in its stated smooth compact connected four-dimensional scope. The accepted lower bound is h_J^- >= 3; this audit does not assert the exact value of h_J^- for the chosen cutoff. Generic vanishing remains a valid prior theorem, and no novelty or publication status is inferred.
