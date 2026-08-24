# Independent nonlinear/PDE rereview of v1.0.8

**Date:** 2026-08-23

**Scope:** the v1.0.8 response to the prior D5 finding, including the
fixed-integrated-mass Fourier/Fredholm construction, high-mode estimate,
sectorial center-manifold setting, positivity, exchange of stability,
complementary spectral-gap continuation, scaled family, robustness, and local
exponential stability in fixed-mass `H^1`.

## Bottom line

**The prior D5 expository defect is repaired.**  The new Fourier-block proof
correctly establishes the kernel, range, cokernel, closed range, and Fredholm
index on the fixed-integrated-mass spaces.  The `k^{-2}` estimate is correct and
is strong enough to turn compatible `L^2` Fourier data into an `H_N^2`
preimage.  The subsequent sectorial, center-manifold, spectral-continuation,
and linearized-stability claims have the hypotheses required by the standard
Crandall--Rabinowitz, Henry, and Kato results cited in the paper.

I found **no fatal, major, or minor mathematical defect**, no added hypothesis,
and no weakened conclusion in this repair.  I also found no new PDE overclaim.
The PDE conclusion remains local for each fixed dimension and fixed scaling
parameter, exactly as stated.  One missing subscript in the Supplement is
cosmetic only (see “Residual issue”).

Classification by evidentiary type:

- Fourier/Fredholm decomposition and high-mode inverse estimate:
  **independently verified deductively**.
- Fixed-mass invariance, kernel/cokernel, transversality, reflection, branch
  positivity, and scaled-variable transfer: **independently verified**.
- Center-manifold existence, analytic spectral continuation, and local
  exponential stability: **verified conditional on the cited standard
  functional-analytic theorems**, with their hypotheses checked here.
- Finite spectral calculations at `m=3,4,149` and both scaling endpoints:
  **supporting falsification checks only**, not proof of the all-dimensional
  assertion.

## Materials and comparison

I compared v1.0.8 with the preserved v1.0.7 snapshot, rather than with stored
claims or PASS files.  The load-bearing PDE changes are:

- `source_snapshot/manuscript/main.tex:734-811`;
- `source_snapshot/manuscript/supplement.tex:947-1015`;
- `source_snapshot/proof_audit/branch_stability.tex:1-70`.

The scaled-family transfer and robustness statements were reread in full at:

- `source_snapshot/manuscript/main.tex:844-888,890-1029`;
- `source_snapshot/manuscript/main.tex:1093-1113`;
- `source_snapshot/proof_audit/stable_pareto_family.tex:217-358`;
- `source_snapshot/proof_audit/robustness.tex:1-15`.

The conservation and fixed-mass definitions were cross-checked at
`source_snapshot/manuscript/main.tex:191-220`,
`source_snapshot/proof_audit/conservation.tex:1-19`, and
`source_snapshot/proof_audit/semipositive_conservation.tex:30-44`.

I rendered and visually inspected the revised manuscript PDF pages 10--14 and
Supplement PDF pages 17--19.  The repaired argument is present and legible in
the rendered artifacts; no equation clipping, missing symbols, or source/PDF
discrepancy was found.  The canonical and journal PDFs are byte-identical.  The
canonical and submission TeX files differ only in relative paths for included
figures/tables.

## Independent reconstruction

### 1. Fixed-mass spaces and the homogeneous block

Let

\[
 E_c=\left\{u\in L^2((0,\pi);\mathbb R^{m+1}):
 \int_0^\pi c^Tu=0\right\},\qquad
 X_c=H_N^2\cap E_c.
\]

Pointwise `c^T f(x)=0` and the Neumann boundary conditions give

\[
 \int_0^\pi c^T D u''=c^TDu'\big|_0^\pi=0,
\]

so the nonlinear flow and every linearization preserve the affine
fixed-integrated-mass class and its tangent space.  This requires no positivity
of the first entry of `c`; semipositivity affects global coercivity, not this
local invariant-subspace argument.

In the normalized Neumann cosine basis, the mass constraint affects only the
constant coefficient: `c^T u_0=0`.  Since `c^T A_m=0`, the zero-mode matrix
maps `c^perp` into `c^perp`.  The earlier homogeneous calculation proves that
zero is algebraically simple.  Equivalently, `ker A_m=span{rho_m}` and
`c^T rho_m=17-8m != 0` for `m>=3`.  Therefore

\[
 A_m:c^\perp\longrightarrow c^\perp
\]

is a bijection.  Thus the repaired text does not silently assume away the
conservation zero.

### 2. Fourier blocks, range, and Fredholm index

The cosine transform unitarily identifies

\[
 \mathcal L_0=A_m+D_m\partial_{\xi\xi}
\]

with the blocks `B_k=A_m-k^2D_m`.  The exact earlier certificates provide:

- `B_0` invertible on `c^perp`;
- `ker B_1=span{r}` and `ran B_1=ell^perp`, with algebraically simple zero;
- `B_k` invertible for every `k>=2`.

For any subordinate matrix norm and
`k^2 >= 2 ||D_m^{-1}A_m||`, direct multiplication gives

\[
 B_k=-k^2D_m\left(I-k^{-2}D_m^{-1}A_m\right),
\]

and the Neumann series yields

\[
 \|B_k^{-1}\|\le 2\|D_m^{-1}\|k^{-2}.
\]

If compatible data have cosine coefficients `g_k`, then the finitely many low
coefficients have bounded preimages and the high coefficients satisfy
`||u_k|| <= C k^{-2}||g_k||`.  Hence

\[
 \sum_{k\ge2}(1+k^4)\|u_k\|^2<\infty,
\]

so `u` lies in `H_N^2`.  Conversely, the first-mode left-nullvector gives the
only compatibility condition.  Therefore

\[
 \ker\mathcal L_0=\operatorname{span}\{r\cos\xi\},
\]

\[
 \operatorname{ran}\mathcal L_0=
 \left\{g\in E_c:\int_0^\pi\ell^Tg\cos\xi=0\right\}.
\]

The range is closed, its codimension is one, and the kernel dimension is one;
the index is zero.  Identifying the cokernel with the `L^2` orthogonal
complement gives `span{ell cos xi}`.  This proves the claims at
`main.tex:749-777`, `supplement.tex:949-982`, and
`proof_audit/branch_stability.tex:9-29`.

### 3. Crandall--Rabinowitz and reflection

The stationary mapping from `X_c x R` to `E_c` is analytic: in one dimension,
`H_N^2` embeds into `L^infinity`, and the mass-action field is quadratic.  Its
linearization is the Fredholm operator above.  Differentiating the factor
`(1-mu)D_m partial_xixi` with respect to `mu` and applying it to
`r cos xi` gives `D_m r cos xi`; its cokernel pairing is

\[
 \frac\pi2\ell^TD_mr\ne0.
\]

Thus the Crandall--Rabinowitz transversality hypothesis is met.  Reflection
`u(xi) -> u(pi-xi)` preserves the boundary conditions and integrated mass,
commutes with the vector field, and negates the critical cosine.  A standard
equivariant center-manifold construction therefore makes the reduced vector
field odd.  The revised manuscript also correctly distinguishes that reduced
flow from the stationary Lyapunov--Schmidt equation (`main.tex:734-744`).

### 4. Sectoriality and the `H^1` phase space

On the closed invariant space `E_c`, positive diagonal Neumann diffusion with
domain `X_c` is the restriction of a diagonal analytic-semigroup generator.
The restriction remains sectorial and has compact resolvent.  Spectrally, its
half-order fractional domain is

\[
 D((-D_m\partial_{\xi\xi})^{1/2})=H^1\cap E_c
\]

with an equivalent norm.  The finite-dimensional reaction Jacobian is a
bounded multiplication perturbation and preserves sectoriality.

In one space dimension, `H^1` embeds into `L^infinity` and is a Banach algebra;
for the quadratic mass-action nonlinearity,

\[
 \|uv\|_{L^2}\le C\|u\|_{H^1}\|v\|_{H^1}.
\]

Consequently the Nemytskii map is analytic (in particular smooth) from fixed-
mass `H^1` to `L^2`.  These are the standard hypotheses for Henry's local
semilinear flow, center-manifold theorem, and principle of linearized
stability.  The citations are appropriately scoped: Henry Chapter 5 concerns
linearized stability near an equilibrium and Chapter 6 concerns invariant
manifolds; Kato Chapters IV and VII concern stability and analytic
perturbation, respectively.

### 5. Complementary gap and exchange of stability

At onset, the exact all-mode result puts every noncritical eigenvalue in the
open left half-plane.  The bound

\[
 \alpha(A_m-k^2D_m)\le
 \left\|(A_m+A_m^T)/2\right\|_2-k^2d_{\min}\to-\infty
\]

shows that only finitely many modes can approach a fixed right half-plane.
The finitely many noncritical eigenvalues therefore have a strictly negative
maximum for each fixed `m`.

Along a branch, Fourier modes are no longer invariant because the patterned
reaction Jacobian is spatially dependent.  The revised proof does not rely on
mode invariance there.  Instead, the domain stays `H_N^2`, the diffusion
coefficient remains uniformly positive locally, and the new reaction
Jacobian is a small bounded multiplication perturbation.  The family is an
analytic type-(A) sectorial family when parameterized by branch amplitude.
Uniform elliptic resolvent bounds exclude spectrum entering from infinity;
inside a bounded spectral region, Kato/Riesz-projection continuation preserves
the finite complementary gap.  This is the correct mechanism.

The reduced center eigenvalue on either nonzero branch is

\[
 \eta_m\mu+3c_mA_\pm(\mu)^2+O(\mu^2)
 =-2\eta_m\mu+O(\mu^2)<0.
\]

Combining it with the complementary gap yields strict spectral negativity.
Henry's linearized-stability principle then gives local exponential
asymptotic stability in the fixed-mass `H^1` phase space.  Neumann conditions
on a bounded interval break continuous translation symmetry, so no unremoved
translation-neutral eigenvalue remains.

### 6. Positivity of the branch

Crandall--Rabinowitz produces the stationary branch in `H_N^2`.  For each fixed
`m`, `H_N^2` embeds continuously into `C^0`; because the base equilibrium is
componentwise one, sufficiently small branch elements remain componentwise
strictly positive.  This proves the unit-family assertion at
`main.tex:783-786` without requiring a dimension-uniform neighborhood.

For the scaled family, the normalized branch likewise converges to one in
`H_N^2`.  Multiplication by the fixed positive diagonal matrix
`H_m(L)^{-1}` preserves every component's sign, including at both inclusive
scaling endpoints (`main.tex:1020-1029`).

### 7. Equilibrium-scaled family

For fixed `m` and certified `L`, normalized perturbations use mode matrices

\[
 \widehat B_k=H_m(L)(A_m-k^2\Delta_m).
\]

The fixed-mass covector is `H_m(L)^{-1}c`, and

\[
 (H_m^{-1}c)^T H_m A_m=c^TA_m=0.
\]

The first-mode right kernel is unchanged; the left vector is
`tilde ell=H_m^{-1}ell`.  The high-mode factorization becomes

\[
 \widehat B_k=-k^2H_m\Delta_m
 \left(I-k^{-2}\Delta_m^{-1}A_m\right),
\]

which supplies the same `O(k^{-2})` inverse estimate.  All diagonal entries of
`H_m(L)` and `H_m(L)Delta_m` are positive at `L_0` and `L_1`.  Thus the
Fredholm, sectorial, spectral-gap, positivity, and `H^1` conclusions transfer
without an omitted endpoint hypothesis.

### 8. Retuned robustness

The proposition is correctly restricted to each fixed `m` and certified `L`,
to perturbations inside the positive-equilibrium realization manifold, and to
one retuned scalar diffusion multiplier (`main.tex:1093-1113`).  The simple
real critical eigenvalue and its nonzero multiplier derivative give a unique
nearby critical multiplier by the implicit-function theorem.  Positivity of
diffusion and boundedness of the reaction Jacobian hold uniformly in a small
parameter neighborhood, controlling the spectral tail; finite eigenvalues,
the cubic sign, and the branch gap vary continuously.  No arbitrary nearby
point, global basin, far-from-onset result, or dimension-uniform radius is
claimed.

## Boundary and adversarial checks

The standalone script `agent_pde_rereview/independent_pde_checks.py` imports no
project module or certificate.  It reconstructs `A_m`, `D_m`, `c`, `r`, `ell`,
and the endpoint scalings directly from the printed definitions.

Command:

```text
/Users/alec/Documents/Math/.venv/bin/python3 independent_pde_checks.py
```

Outcome: exit `0`, wall time `1.90 s`.

- Exact arithmetic at `m=3,4,7` verified `c^TA_m=0`, rank `m`, the
  nonorthogonal homogeneous right kernel, the critical right and left kernels,
  one-dimensionality, the signs of `ell^Tr` and `ell^TD_mr`, and the high-mode
  factorization.
- At both `L_0` and `L_1`, exact checks verified the transformed conservation
  covector, left kernel, left/right nonorthogonality, and invariant
  transversality numerator.
- Independent numerical sweeps at `m=3,4,149`, for the unit family and both
  endpoints, found strictly negative homogeneous, noncritical first-mode, and
  higher-mode spectral bounds.  The closest observed complementary margin was
  about `7.34e-4` at `m=149`; it is small but positive, consistent with the
  theorem's non-uniform locality.
- The Neumann-series inverse inequality was tested at and above its calculated
  threshold.  The largest observed left/right ratio was below `0.500`, safely
  within the claimed bound `1`.

The full machine-readable summary is
`agent_pde_rereview/results/independent_pde_checks.json`.  These finite checks
are explicitly not used to prove the infinite-mode or all-dimensional claims;
those follow from the deductive estimates above and the exact certificates
audited previously.

## Residual issue

**Cosmetic notation only.**  At `manuscript/supplement.tex:980-982`, the scaled
mode matrices are printed as `H_m(L)(A_m-k^2 Delta)` although the defined
matrix is `Delta_m`.  Context is unambiguous, and the main manuscript uses
`Delta_m`.  Replacing `Delta` by `Delta_m` would remove the typo.  It changes no
hypothesis, conclusion, estimate, or headline claim.

## What remains conditional

I did not reprove the general Crandall--Rabinowitz, Henry, or Kato theorems.
Their use is standard and their concrete hypotheses have been checked above.
The official source records confirm the cited scope:

- [Crandall--Rabinowitz, “Bifurcation from Simple Eigenvalues”](https://www.sciencedirect.com/science/article/pii/0022123671900152);
- [Henry, *Geometric Theory of Semilinear Parabolic Equations*](https://link.springer.com/book/10.1007/BFb0089647);
- [Kato, *Perturbation Theory for Linear Operators*](https://link.springer.com/book/10.1007/978-3-642-66282-9).

No global existence for arbitrary data, global attraction, quantitative basin,
dimension-uniform branch radius, or stability far from onset was verified or
claimed.

## Final scoped verdict

**PDE REPAIR VALID AS STATED.**  D5 is closed.  The functional-analytic portion
of Theorems 6.1 and 7.1 and Proposition 8.1 is valid, conditional only on the
standard cited theorems in the ordinary referee sense.  The optional
`Delta -> Delta_m` correction is cosmetic and does not warrant a technical
validity downgrade.
