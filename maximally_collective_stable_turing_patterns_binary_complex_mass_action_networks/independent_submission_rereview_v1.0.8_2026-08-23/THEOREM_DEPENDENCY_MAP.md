# Independent theorem-dependency map for v1.0.8

This map was reconstructed from the current manuscript and supplement. The
author-supplied `review_maps/` files were not used as proof. Line references
are to the immutable `source_snapshot/`.

## Common algebraic foundation

1. Indexed binary-complex reactions (`manuscript/main.tex:145-186`) define
   `Y_m`, `Gamma_m`, and the unit-equilibrium field.
2. Reaction balances, the maximal stoichiometric minor, and the semipositive
   covector give rank `m`, the two-dimensional steady-flux kernel, the positive
   flux cone, and `im Gamma_m=c^perp` (Proposition 2.1,
   `main.tex:191-220`; `supplement.tex:31-63`).
3. The mass-action derivative identity
   `J=Gamma diag(v)Y^T H`, together with the inverse rate construction, gives
   all and only positive-equilibrium Jacobians `A_m(a,b)H` (Proposition 2.2,
   `main.tex:222-253`).

These are deductive algebraic steps. Exact finite matrix reconstruction is
corroboration, not the all-dimensional proof.

## Principal-subsystem localization

`Reaction graph + path forcing + m=3 direct case + b=2a deletion`

`-> exhaustive SCC classification (Lemma 3.1, main.tex:260-309)`

`-> two strict long-cycle modulus bounds + boundary-triad Routh gap`

`-> every nonempty principal block of order <m is Hurwitz`

`+ lower-bidiagonal Schur elimination and det B_core=2a^2b`

`-> signed X-core determinant <0 -> positive real eigenvalue`

`-> Theorem 3.2: first unstable principal order m=n-1 (main.tex:311-362)`

`-> Corollary 3.3, with the general-matrix endpoint conditional on the cited
Satnoianu result and the stable-pattern clause conditional on Theorem 6.1.`

The `b=2a` and Schur-complement steps are deductive. Finite SCC enumeration at
`m=3,...,8` and exact determinants are adversarial corroboration.

## General diffusion-ray theorem and network law

`Principal-minor expansion + det J=0 + positive lower-order signed minors +
positive sum of order-(n-1) signed minors`

`-> beta_k(D)>0 for k>=2 and strict monotonicity in ray parameter`

`+ strict monotonicity of chi_s(lambda) on lambda>=0`

`-> Theorem 4.1: iff threshold, uniqueness, ordinary algebraic simplicity,
and exact positive-real band (main.tex:379-428).`

Independently:

`core determinant + interior-omission boundary triad + two restricted
nullvectors`

`-> complete omission table (Proposition 5.1, main.tex:445-492)`

`+ homogeneous relative stability -> simple conservation zero and positive
order-(n-1) coefficient`

`+ Theorem 4.1`

`-> Theorem 5.2: necessary-and-sufficient stationary diffusion law and unique
ray threshold (main.tex:503-549).`

`-> elementary contrast optimization and strict equality exclusions`

`-> Theorem 5.3: fixed-H infimum, unit infimum, topology-wide product bound,
and sharpness as an infimum (main.tex:558-596).`

All implications above are deductive. The exact theorem explicitly does not
exclude nonreal instability after the positive-real band.

## Unit-equilibrium stable Turing branch

`Selected rational r,D + exact right/left kernel identities`

`+ 35-term homogeneous modulus certificate (m=3 treated directly)`

`+ 77-term spatial certificate and characteristic derivative`

`-> homogeneous stability, first-mode algebraic simplicity, transversality,
and exclusion of all competing modes.`

`Reaction-wise quadratic tensor + unique gauge-fixed w_0 + unique w_2`

`+ generic four-factor recurrence + boundary determinant nonvanishing`

`+ exact contraction N_m=R_m+C_m hfrak and shifted-positive sign certificates`

`-> eta_m>0 and c_m<0 in the reduced flow.`

`Fixed-mass invariance + Fourier block decomposition + O(k^-2) inverses`

`-> closed range, one-dimensional kernel/cokernel, Fredholm index zero`

`+ Crandall--Rabinowitz transversality + reflection oddness`

`-> two local stationary branches and H_N^2-to-C^0 positivity`

`+ center eigenvalue sign + finite complementary gap + elliptic spectral-tail
control + sectorial H^1 semilinear theory`

`-> Theorem 6.1: local exponential asymptotic stability in fixed-mass H^1
(main.tex:627-808).`

The matrix, recurrence, contraction, and sign steps are exact algebra. The
functional-analytic conclusion is verified conditional on the cited standard
Crandall--Rabinowitz, Henry, and Kato results, whose concrete hypotheses are
checked in the paper and in `agent_pde_rereview/PDE_REREVIEW.md`.

## Equilibrium-scaled family

`Certified inclusive interval [L_0,L_1] + positive diagonal equilibrium
scaling H_m(L)`

`-> physical equilibrium/rates/diffusion and normalized row-scaled operator`

`+ 22-term homogeneous and 84-term spatial modulus certificates, with the
m=3 exceptional Routh case`

`+ transformed adjoint, algebraic-simplicity contradiction, unchanged
transversality numerator`

`+ physical conservation gauge, N_ref and S_m bounds, tau_m(L)<1/20`

`-> c_m(L)<0 throughout both inclusive endpoints`

`+ the same fixed-mass Fredholm/sectorial branch argument and positive
diagonal back-scaling`

`-> stable positive local branches for every fixed m,L`

`+ exact contrast formulas/product and monotonicity`

`-> unique within-family minimizer L_0 and Theta(sqrt(m)) endpoint`

`+ Theorem 5.3 product lower bound`

`-> Theorem 7.1: exponent 1/2 is optimal among stationary-crossing
realizations of this topology (main.tex:844-1046).`

No constant-optimal or global Pareto-frontier statement follows or is claimed.

## Boundary example and robustness

- The near-threshold `m=3` positive-cubic result (Eq. 61,
  `main.tex:1061-1071`; `supplement.tex:882-945`) is a finite exact rational
  control example. It is explicitly not a universal nonlinear gap.
- Simple-eigenvalue continuation, one nonzero multiplier derivative, finite
  low-mode gaps, uniform high-mode ellipticity, and smooth cubic/branch data
  imply Proposition 8.1 (`main.tex:1093-1113`). The result is local for fixed
  `m,L`, remains on the positive-equilibrium realization manifold, and retunes
  one scalar multiplier.

## Evidence boundary

- Deductive proof: reaction balances, graph forcing, determinant/minor
  expansions, inequalities, Fredholm Fourier estimates, and local robustness
  interface.
- Exact computer algebra: generated coefficient expansions, rational matrix
  solves, recurrence contractions, and shifted polynomial identities.
- Finite exact regression: selected dimensions and endpoint instances; useful
  for falsification but not an all-dimensional proof.
- Floating point: branch spectral sweeps, numerical-provenance checks, and
  simulations; never used to establish a theorem.
- Citation-dependent: the general matrix historical endpoint and the standard
  infinite-dimensional bifurcation/semigroup/perturbation theorems.
