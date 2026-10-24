# A certified planar spectral-path specialization of the Maslov challenge

## Scope and result

Row 1900 / ID 20002401. This is a partial-progress audit, not a solution of the broad AIM challenge and not a novelty claim. The original wording is corpus-recovered; live original-page verification failed (502 and certificate mismatch, with no bypass). Bounded physical-planar self-adjoint elliptic paths are an inferred specialization.

We prove, with an executable exact-rational arithmetic certificate, that the Dirichlet Cauchy-data path for

L = −Δ + (1/4) cos(x) cos(y), Ω=(0,π)², Lu=t u, 1≤t≤3,

has Maslov index −1 relative to the Dirichlet subspace, with the symplectic convention below. This is a nonseparable multiplication potential in Cartesian coordinates, not a one-dimensional ODE or an identification of physical dimension with phase-space dimension. The calculation is an analytically certified planar benchmark with computer-checked rational bounds, not an implemented general interval boundary solver. The proof does not require numerical eigenfunctions, rounded transcendental evaluations, or treating a truncation as the full PDE.

## 1. Approach one: pin down the analytic boundary problem

Work over real functions. The form a(u,v)=∫Ω(∇u·∇v+Vu v), V=(1/4)cos x cos y, on H¹₀(Ω) is closed and semibounded. Its self-adjoint realization has domain D(L_D)={u∈H¹₀(Ω):−Δu∈L²(Ω)}. This definition, rather than an assumed smooth-boundary H² trace description, handles the square's corners. Bounded V does not change this operator domain. The compact embedding H¹₀→L² gives compact resolvent. The family L_D−t has this fixed domain, with bounded norm-analytic perturbation −tI.

For solutions u∈H¹(Ω) of Lu=tu, weak conormal trace g∈H⁻¹/²(∂Ω) is defined by
<g,γ_D v>=∫Ω(∇u·∇v+(V−t)uv), v∈H¹(Ω).
Independence of extension follows from the weak equation. Put X=H¹/²(∂Ω), X*=H⁻¹/²(∂Ω), H=X⊕X*, and
ω((f,g),(h,k))=<k,f>−<g,h>.
Let G(t) be the Cauchy-data subspace and D={0}⊕X*. The standard elliptic Cauchy-data theorem for bounded Lipschitz domains, bounded smooth real potential, and unique continuation gives a real analytic Fredholm-Lagrangian path (G(t),D); trace identifies G(t)∩D with ker(L_D−t). These analytic facts are inputs from existing theory, not consequences of our rational script. The applicable statements and convention appear in Cox–Latushkin–Sukhtayev, arXiv:2206.07677v1, §8.1, equations (8.1)–(8.6); the negative eigenvalue-count convention is (1.18). Its §4 treats weak traces on Lipschitz domains. We inspected those passages in the retained primary PDF, not only its abstract.

Here unique continuation is applicable to −Δ plus smooth bounded potential: a solution with both traces zero extends by zero across a flat boundary segment as a weak solution and vanishes by unique continuation. Thus no eigenfunction loses its crossing through zero Cauchy trace. The Fredholm and analytic-path theorem is not replaced by a formal Dirichlet-to-Neumann graph at a pole. There is no assertion that a single Dirichlet-to-Neumann chart remains bounded through the eigenvalue.

At a crossing t*, take a differentiable solution lift u(t) with u(t*)=u in the Dirichlet eigenspace; such local lifts follow from the analytic Cauchy-data construction. Differentiating (L−t)u(t)=0 gives (L−t*)u'=u. Green's identity with γ_D u=0 yields ∫u²=<γ_N u,γ_D u'>. Therefore the crossing form is
Q(Tr u)=ω(Tr u,(Tr u)')=−<γ_Nu,γ_Du'>=−∥u∥².
This explicitly fixes the sign; it is not a free convention chosen after the interior count. Every spectral-parameter crossing is regular and negative definite, including a multiple eigenvalue. Transverse endpoints imply that the Maslov index equals minus the number of Dirichlet eigenvalues in (1,3), counted with multiplicity. This is prior Morse–Maslov theory, used openly as an input.

Outcome: boundary sign and analytic domains are controlled for this specialization. Residual: arbitrary varying coefficients/domains/boundary conditions need their own analytic path theorem and chart certificates.

## 2. Approach two: exact infinite-tail Schur certificate

Use the normalized Dirichlet sine basis e_mn=(2/π)sin(mx)sin(ny). Set P=projection onto e_11 and Q=I−P. On QL², Q(−Δ)Q≥5I because m,n≥1 and (m,n)≠(1,1) imply m²+n²≥5. Multiplication by V has norm ≤1/4. Thus, for all t∈[1,3],
C(t)=Q(L_D−t)Q ≥ (5−1/4−3)I=(7/4)I,
so ∥C(t)⁻¹∥≤4/7. The domain of C is QD(L_D), fixed and invariant under the Laplacian; bounded QVQ is a permissible self-adjoint perturbation. All off-diagonal blocks are bounded. This is a genuine infinite-dimensional coercivity bound, not a finite sample.

The diagonal scalar is a(t)=2−t since <e_11,V e_11>=0. The coupling is exactly b=QV e_11=(1/16)e_22, by cos x sin x=(1/2)sin(2x). Hence ∥b∥²=1/256. Exact elimination gives
S(t)=2−t−<b,C(t)⁻¹b>.
The operator has a kernel iff S(t)=0, and its kernel is then spanned by e_11−C(t)⁻¹b. Indeed the Q equation uniquely gives y=−C⁻¹b x, and substitution gives Sx=0. This also proves simplicity, without assuming genericity.

Writing r(t)=<b,C⁻¹b>, positivity and the inverse bound give 0<r(t)≤1/448. A useful strict lower bound follows from Cauchy–Schwarz in the C energy inner product:
<e_22,C⁻¹e_22> ≥ 1/<e_22,C e_22> = 1/(8−t) ≥ 1/7.
Here e_22 belongs to D(C), and its V diagonal is zero. Thus r(t)≥1/1792 throughout [1,3].

The resolvent identity gives (C⁻¹)'=C⁻², since C'=-I. Therefore
S' = −1−<b,C⁻²b>, with −1−1/784 ≤ S' ≤ −1.
No uncontrolled finite difference or inverse derivative is used. At 1, S≥447/448>0; at 3, S≤−1−1/1792<0. Exactly one simple root exists. Its enclosure is
2−1/448 ≤ t* ≤ 2−1/1792.
In particular t* is strictly less than 2: the finite one-mode truncation misses the nonzero coupling correction, while the infinite-tail certificate catches it.

Outcome: a nonzero off-diagonal infinite tail is certified, not merely assumed. Limit: this is an interior spectral decomposition combined with the proved boundary crossing identity, not a general boundary-mode implementation.

## 3. Approach three: independent min–max and homotopy checks

The form inequalities −Δ−1/4≤L_D≤−Δ+1/4 give λ₁(L_D)∈[7/4,9/4] and λ₂(L_D)≥19/4. Thus there is precisely one eigenvalue in (1,3), counted with multiplicity, already independently verifying the count. Its multiplicity is one because λ₂>3. This check is coarser than the Schur enclosure and uses no Schur inverse.

For V_s=(s/4)cos x cos y, 0≤s≤1, these same endpoint gaps hold uniformly. The analytic Fredholm-Lagrangian two-parameter family therefore has no endpoint crossing. Homotopy invariance reduces its Maslov index to the zero-potential square, whose only eigenvalue in (1,3) is 2, with negative crossing form. This is a second conceptual route to −1, not an additional independent discovery. It verifies sign consistency and detects a mistaken claim that the potential has no effect on the crossing location.

Outcome: two independent analytic count checks agree with the tail certificate. Residual: these cheap comparisons cease to decide the count when endpoint gaps are comparable to the potential bound.

## 4. Approach four: repair the general nested chart theorem

For possible extension, suppose A(t) is a bounded self-adjoint norm-C¹ chart operator on a fixed Hilbert space F⊕T, F finite-dimensional, with block matrix [[a,b*],[b,C]], and C uniformly boundedly invertible. Assume a verified symplectic chart identifies its kernel and crossing form with the desired Fredholm-Lagrangian pair, including the sign convention. This last condition is indispensable.

Define S=a−b*C⁻¹b and E x=(x,−C⁻¹b x). Then AE x=(Sx,0), so kernels are exactly identified. Since E*AE=S, differentiation and AE x=0 on ker S show <x,S'x>=<E x,A'E x> there. In particular the crossing forms are congruent, not merely equal in determinant zero sets. The derivative to validate is
S'=a'−b' *C⁻¹b−b*C⁻¹b'+b*C⁻¹C'C⁻¹b.
Omitting the final inverse-derivative term is an error. For unbounded interior operators like the example, use fixed-domain resolvent identities with bounded off-diagonal blocks rather than silently applying the bounded-chart theorem.

A second finite Schur reduction is allowed only when its complementary finite block is certified invertible throughout its box. A scalar residual s with certified strict endpoint signs and derivative bounded away from zero certifies one simple crossing and its sign. A multiple crossing cannot be certified by scalar simple-root logic. It needs a separately validated kernel cluster and an inertia certificate for its crossing form; spectral-parameter paths here already supply negative definiteness analytically.

Global certification must partition the parameter interval into disjoint owned crossing boxes and no-crossing closed pieces, certify all endpoints and chart-switch points transverse, and verify symplectic chart overlap maps. A zero may have only one owner. For the present example there is a single global interior Schur chart, one crossing box [199/100,2], and two no-crossing pieces [1,199/100] and [2,3], whose common endpoints are nonzero. Boundary charts are supplied by the analytic Cauchy-data theory, not numerically constructed or claimed to have passed an overlap test.

Outcome: a precise conditional certificate theorem, with derivatives and ownership corrected. Residual: general PDE applications still owe validated boundary charts, coupling, and inverse/tail bounds.

## 5. Approach five: executable certificate, rejection tests, and limits

CHECK.py uses only Python's exact Fraction arithmetic. It validates the coefficient identities encoded as exact sine-mode shifts, tail gap, coupling norm, root bracket, derivative bound, chart ownership inequalities, and independent min–max endpoint gaps. It rejects deliberately weakened/wrong certificates: missing coupling, reversed derivative correction, zero tail gap, an overstated tail spectral floor, a crossing box wholly below the root, and reversed Maslov sign. All checks are explicit exceptions rather than Python asserts, so optimization does not erase them. The output is a JSON record of exact rational values and named tests. Both normal and python -O runs must agree. Independent adversarial review caught an unvalidated tail_floor argument that could produce an inverted interval for a non-benchmark input; the repaired script pins the proved floor to 5, checks correction/root ordering, and rejects that mutation. The mathematical baseline bounds were unchanged.

This is proof-checking of elementary exact inequalities attached to analytic arguments, not a formal proof assistant, interval integration, or numerical validation of the cited general trace theorem. The script's sine-mode identities are checked algebraically; the mathematical derivation of the infinite-tail spectral gap and potential norm appears above. It does not claim to discover all crossings from a finite mesh.

The fixed checker rejects the tested zero-tail-gap, incorrect coupling/sign, overstated spectral-floor, and missed-crossing-box inputs. These tests do not establish failure safety for arbitrary finite-model derivative or coupling errors. For arbitrary physical-planar paths, a validated FEM/boundary-element residual estimator could supply the missing tail/trace bounds, but this work contains no such implementation. Likewise Fredholm determinant winding can replace crossing isolation only after trace/Schatten remainder and contour nonvanishing certificates; no determinant computation was executed here. These are genuine residuals, not completed algorithms.

## Literature and status boundary

Primary sources: Cox–Latushkin–Sukhtayev, https://arxiv.org/abs/2206.07677 (retained PDF §4, §8.1 and introductory identity (1.18) inspected here; abstract page reopened 2026-10-21); Beck–Jaquette, https://arxiv.org/abs/2105.06895 (spatial-ODE validated precedent); Latushkin–Sukhtaiev, https://arxiv.org/abs/1610.09765 (elliptic Maslov foundations, not independently proof-audited here); Beck–Jaquette–Pieper, https://arxiv.org/abs/2510.24417 and https://doi.org/10.1016/j.jde.2026.114514 (2026 Part I resonant-bundle spatial-ODE work). Source/status details for the latter references are inherited from the supplied recovery gate, not a new full-text audit. Part I does not close the general physical-planar boundary/tail certificate; failure to locate Part II is not proof it does not exist.

No novelty is claimed for Schur complements, min–max bounds, homotopy invariance, or the Morse–Maslov identity. The concrete nonzero-coupling planar example is the deliverable. The general original challenge remains unresolved here; worldwide open status is not established by a bounded search.
