# Research log: regular transposition sector at fitness two

Date: 2026-08-08 (America/Los_Angeles)

## Initialization

- Scope is only symmetric stochastic zero-diagonal kernels `P`, equivalently
  regular undirected weighted graphs after scaling.
- Target is the transposition midpoint inequality

  `rho_dB((P + sigma P sigma)/2, 2) >= rho_dB(P, 2)`.

- The phase-four heat-bath, even/odd Schur, local bonus, and odd killing
  identities are frozen and will not be rederived unless an exact audit finds
  an error.
- A proof here would establish the regular-kernel complete-graph maximizer,
  not the unrestricted weighted-graph theorem.

## 2026-08-08 08:55 PDT -- hostile orbital screens and surviving structure

- Built direct subset-chain screens for random symmetric stochastic kernels
  and transposition orbits at orders five through seven.  No endpoint or
  midpoint-curvature failure appeared.  These runs were used for discovery
  only and are not a proof.
- Added boundary screens using convex mixtures of fractional perfect
  matchings.  Again no failure appeared; optimizers tended toward disconnected
  or already transposition-invariant boundary points.  This is numerical only.
- The exact second-derivative decomposition consistently split into a negative
  direct heat-bath term and a positive committor-response term.  The response
  was large (typically 70--83 percent of the direct magnitude), so discarding
  it or bounding it termwise by the raw concavity bonus is not viable.
- Hostile checks exactly/numerically closed several tempting shortcuts:
  the active configuration chain is not generally reversible; a pointwise
  pair-disagreement response bound fails; and coverage alone remains
  insufficient by the inherited exact order-four sector counterexample.

## 2026-08-08 09:42 PDT -- exact complete-kernel rank/cut reduction

- At the complete kernel, derived the exact first-order source

  `L' h_0(S) = -f_k q(S)`

  where `q(S)` is the cut of the row-zero perturbation and `|S|=k`.
  Consequently the first committor derivative is exactly one killed cut mode,
  `h_1(S)=-v_k q(S)`.
- Reduced `v` to a tridiagonal strictly diagonally dominant M-matrix on ranks
  `2,...,n-2` and derived exact uniform-subset formulas for `E[q^2]`, the
  inside and outside squared perturbation masses, and the complete rank
  occupation measure.
- Derived a complete exact Hessian formula

  `Phi''/||Delta||_E^2 = -D + sum_k ell_k v_k`,

  with every response coefficient `ell_k` strictly positive.
- Built an independent exact labelled/lumped derivative solver for the
  four-cycle direction.  It agrees with the rank formulas and proves strict
  negative curvature exactly through order fourteen.

## 2026-08-08 10:14 PDT -- PROVED all-n strict local regular maximality

- Found the explicit supersolution

  `bar(v)_k = (21/20) ((n+k)/(4n-2k)) f_k`.

  After `a=k-2`, `b=n-k-2`, the residual numerator is a 45-term polynomial
  with strictly positive integer coefficients; the exact denominator is
  positive.  M-matrix comparison therefore gives `0<v<bar(v)` at every rank.
- Closed the remaining all-size sum.  For `n>=9`, proved pointwise

  `ell_k bar(v)_k < D_{k-1}`

  by an exact polynomial certificate split into `b=0,...,4` and `b>=5`.
  The latter uses positivity of both `H_0(a,c+5)` and
  `128 H_0(a,c+5)+H_1(a,c+5)`, together with
  `2^(-b-2)<=1/128`.  For `n=6,7,8`, the exact total upper-bound ratios are
  respectively

  `265019/275520`,
  `32970550983/36455056000`, and
  `383371803381/446439422000`.

  Orders four and five solve exactly with Hessian per squared-edge norm
  `-27/637` and `-367616/7498125`.
- **PROVED:** for every `n>=4`, the complete kernel has zero first derivative
  and strictly negative second derivative in every nonzero symmetric,
  zero-diagonal, row-zero direction.  It is therefore a strict local maximum
  of dB fixation at fitness two inside the regular-kernel polytope.
- Replayed both exact verification paths successfully:

  1. `verify_local_complete_hessian.py` (rank/cut formulas, rational finite
     cases, and integer polynomial certificates);
  2. `derive_complete_hessian.py --min-n 4 --max-n 14` (independent exact
     labelled/lumped subset chain).
- Scope boundary: this is an all-`n` **local theorem at the complete kernel**.
  It does not prove global orbital symmetrization and says nothing about
  nonregular graphs.

## 2026-08-08 10:28 PDT -- global-orbit reduction audit

- Derived the exact center Hessian identity at an arbitrary
  transposition-invariant regular midpoint:

  `phi''(0)=<mu,L_2 g>+2<mu,L_1 G_- L_1 g>`.

  Thus center curvature is precisely a direct bonus versus killed odd-sector
  feedback inequality.  The new theorem proves it only at the complete
  midpoint, where the harmonic rank/cut structure closes the feedback.
- The finite-amplitude midpoint gap retains the inherited killed-sector
  identity and remains the most direct global target.
- At a noncentral orbit point, exact differentiation instead involves the
  full Green operator `(-L_t)^(-1)`.  The base generator does not commute with
  the transposition, and a two-layer conjugate lift does not create odd
  killing.  Therefore orbit-wide differential concavity does not directly
  reduce to the same killed-sector norm bound.  This is a structural route
  separation, not a counterexample to concavity.
- Exactly solved the inherited hostile order-four orbit.  Its full profile is

  `phi(x)=(101 x^2-71629)/(2(69 x^2-85241))`,

  and its second derivative is strictly negative for `|x|<=1`.  This exact
  example is evidence only; `verify_k4_orbit_profile.py` reconstructs the
  labelled chain and checks the identity symbolically.
