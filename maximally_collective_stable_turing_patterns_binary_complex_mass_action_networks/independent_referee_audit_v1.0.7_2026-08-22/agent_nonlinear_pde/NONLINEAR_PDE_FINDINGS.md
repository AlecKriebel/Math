# Independent nonlinear/PDE referee findings

## Bottom line

Within my assigned scope, the nonlinear, spatial-spectral,
equilibrium-scaled-family, robustness, and fixed-mass semilinear-stability
claims are **valid as stated**. The exact algebraic claims were independently
reconstructed, including the all-dimensional cubic bridge that the shipped
finite verifier does not itself prove. The local PDE conclusions are verified
conditional only on standard simple-eigenvalue bifurcation, sectorial center
manifold, spectral perturbation, and linearized-stability theorems; the
manuscript satisfies their relevant hypotheses.

I found no false claim and no repair that changes a theorem hypothesis,
conclusion, dimension range, endpoint, or headline. I found two minor
reproducibility-description defects and one place where a short expository
addition would materially improve auditability. Exact repairs are listed
below. They do not change the mathematics.

This scoped result supports an overall technical verdict of **VALID AS
STATED**, subject to the other referees' independent findings on the linear
network and diffusion-law portions.

## Evidence classes

- **Deductive/exact independent reconstruction:**
  `agent_nonlinear_pde/independent_exact_checks.py`, which imports no project
  module and reads no project certificate. It reconstructs the reaction
  matrices and Hessian from the reaction list.
- **Exact author-code reproduction after semantic inspection:** the selected
  verifier entrypoints listed below.
- **Floating-point falsification only:** the `m=149` and dense noninteger
  damping sweeps in `results/independent_exact_checks.json`. These are not used
  to prove an all-dimensional statement.
- **Citation-dependent standard analysis:** the center-manifold,
  Crandall--Rabinowitz, Kato perturbation, and principle-of-linearized-stability
  steps.

The complete manuscript sources read were
`working_packet/repository/manuscript/main.tex` (1,217 lines) and
`working_packet/repository/manuscript/supplement.tex` (971 lines).

## Independently reconstructed dependency map

1. The indexed reaction list and unit steady flux give `A_m` and the symmetric
   quadratic Hessian `B_m` directly.
2. The homogeneous determinant identity and the `E35` modulus polynomial prove
   homogeneous relative stability for the unit family; `m=3` is a separate
   exact factorization.
3. The damped determinant identity and `E77` prove that at `t=1` the only
   closed-right-half-plane root is zero and that every `t>1` mode is Hurwitz.
   The exact derivative and left/right pairing prove algebraic simplicity and
   transversality.
4. Restriction to fixed integrated mass removes the homogeneous conservation
   zero. Fourier decomposition then gives a one-dimensional critical kernel
   and cokernel for the stationary PDE operator.
5. Reaction-wise conservation gives compatibility of the zero-harmonic solve;
   its mass gauge makes it unique. The `t=4` mode certificate makes the
   second-harmonic solve unique.
6. Fourier projection of the quadratic nonlinearity gives the exact cubic
   contraction. The printed recurrence reduces its interior sum to one
   polynomial sum plus the harmonic sum `\mathfrak h_m`; exact sign certificates then give `c_m<0` for
   every `m>=3`.
7. Reflection makes the center flow odd. Standard center-manifold and
   simple-eigenvalue bifurcation results give the two stationary branches;
   the reduced-flow derivative gives exchange of stability. Sectorial
   linearized stability gives local exponential stability in fixed-mass `H^1`.
8. In the scaled family, the concentration change produces the row-scaled
   operator `H_m(L)(A_m-t Delta_m)`, transformed adjoint `H_m(L)^{-1} ell`,
   and physical mass covector `H_m(L)^{-1}c`.
9. Separate `E22` homogeneous and `E84` spatial certificates give the inclusive
   interval. The second harmonic is unchanged, while the zero harmonic changes
   by the unique kernel gauge. Exact bounds on that gauge preserve the negative
   cubic sign.
10. Explicit entry ordering gives the physical contrast formulas, fixed
    product, and unique within-family minimizer. Standard simple-eigenvalue and
    gap perturbation arguments give the stated retuned local robustness.

## Claim-by-claim classifications

### Primary unit-equilibrium stable design (`Theorem 6.1`)

Source: `main.tex:595-772`, especially theorem statement `624-655`; Supplement
Sections S5--S6, `supplement.tex:205-465`.

| Claim | Classification | Independent basis |
|---|---|---|
| Homogeneous relative stability for every `m>=3` | **Independently verified** | Reconstructed `det(lambda I-A_m)=(1+lambda)^(m-3)P-R`; direct `m=3` factorization; rebuilt `E35` and its unique equality point. See `main.tex:657-671`, `supplement.tex:238-258`. |
| Critical right and left vectors | **Independently verified** | Symbolic all-`m` boundary and generic interior equations for `(A-D)r=0` and `(A-D)^T ell=0`; exact full matrices at `m=3,4,7,149`. Formulas are at `main.tex:598-612,705-713` and `supplement.tex:205-236`. |
| Algebraic simplicity | **Independently verified** | Re-derived the determinant derivative and `ell^T r<0`; rebuilt the harmonic-bound sign argument. See `main.tex:688-704` and `supplement.tex:276-289`. |
| Transversality | **Independently verified** | `ell^T D r<0` and `ell^T r<0`, hence `eta=(ell^TDr)/(ell^Tr)>0`; exact symbolic formulas and `m=149` check. See `main.tex:711-713`. |
| First-mode isolation and exclusion of complex competitors | **Independently verified** | Rebuilt `E77` from `F,G`; all 77 coefficients are positive, no constant term, and positive pure `x,z,s` anchors give equality only at `(lambda,t)=(0,1)`. See `main.tex:673-704`, `supplement.tex:259-289,795-814`. |
| Every higher Neumann mode stable | **Independently verified** | The same exact certificate holds for all real `t>1`, so in particular for `t=k^2`, `k>=2`; this excludes both real and wave instabilities. |
| Definitions/existence/uniqueness of `w0,w2` | **Independently verified** | Reconstructed the all-`m` zero-mode boundary equations, gauge, second-mode recurrence, four-variable boundary system, and its nonzero determinant. Exact matrices were checked at `m=3,4,7,149`. See `main.tex:715-725`, `supplement.tex:291-383`. |
| Fourier factors and cubic contraction | **Independently verified** | `cos^2=(1+cos2)/2` plus the `1/2 B(u,u)` convention gives both right sides `-B(r,r)/4`; `cos*cos2=(cos+cos3)/2` gives the factor `1/2` in the contraction. See `main.tex:715-725`. |
| All-dimensional cubic sign `c_m<0` | **Independently verified** | See the dedicated all-`m` derivation below. The numerator is positive and `ell^Tr<0`. See `supplement.tex:385-465`. |
| Odd reduced flow, two reflected positive branches | **Verified conditional on standard equivariant center-manifold/CR results** | Reflection preserves Neumann and fixed-mass spaces and sends `r cos xi` to its negative. `H_N^2 -> C^0` in 1D ensures positivity for each fixed `m`. See `main.tex:731-760`. |
| Exchange of stability and local exponential `H^1` stability | **Verified conditional on standard sectorial/Kato/Henry results** | The center eigenvalue is `-2 eta_m mu+O(mu^2)<0`; the complementary onset spectrum has a fixed-`m` gap, high modes tend left, and the branch linearization is a small bounded multiplication perturbation. See `main.tex:761-770`, `supplement.tex:930-940`. |
| Contrast bounds for `chi_stable` | **Independently verified modulo the preceding PDE theorem** | The lower bound is the stationary linear bound; the explicit stable design gives the upper bound. See `main.tex:650-654`. |

### Equilibrium-scaled stable family (`Theorem 7.1`)

Source: `main.tex:774-1006`, theorem statement `804-848`; Supplement Section
S7, `supplement.tex:467-777`.

| Claim | Classification | Independent basis |
|---|---|---|
| Inclusive interval and both endpoints | **Independently verified** | `L0<=L1` in the exceptional and general cases; all denominators/entries remain positive. Exact endpoint calculations were performed at `m=3,4`; numerical/high-dimensional regression at `m=149`. See `main.tex:776-790`. |
| Physical realization and rescaling | **Independently verified** | From `x*=H^{-1}1` and reciprocal source monomials, unit flux is exact; `D_phys=H Delta`; `hat x=Hx` yields `H{f(hat x)+(1-mu)Delta hat x_xx}`. See `main.tex:791-809,850-861`. |
| Transformed adjoint and algebraic simplicity | **Independently verified** | `q=H^{-1}ell` is the left nullvector of `H(A-Delta)`; `q^Tr=ell^TH^{-1}r<0` rules out a generalized eigenvector. See `main.tex:928-979`. |
| Homogeneous stability, `m=3` | **Independently verified** | Exact cubic Routh--Hurwitz calculation with `gamma=91L/90`; the endpoint satisfies `gamma>1/8`. See `main.tex:911-919`. |
| Homogeneous stability, `m>=4`, including `L=L0` | **Independently verified** | Rebuilt `E22`. At the boundary `U=0`, its linear `x,z` coefficients vanish, but its pure `x^2,z^2` coefficients remain positive; equality is still only `lambda=0`. The zero is simple. See `main.tex:878-918`, `supplement.tex:542-590,830-855`. |
| First mode and all `t>1` modes | **Independently verified** | Rebuilt `E84`; its grouped 84 coefficient polynomials are nonnegative and nonzero for `A>0`, with equality only at `(lambda,t)=(0,1)`. See `main.tex:863-876`. |
| Physical conservation gauge and `w0(L)` | **Independently verified** | The normalized fixed-mass covector is `H^{-1}c`; its pairing with `rho` is strictly negative on the interval, so the gauge correction is unique. Exact endpoint gauges checked at `m=3,4`. See `main.tex:929-942`. |
| All-dimensional scaled cubic sign | **Independently verified** | Rebuilt `N_ref>1/100`, `-1/10<S<0`, monotonicity of `tau`, endpoint comparison `tau<1/20`, and hence `N(L)>1/200`; denominator is negative. See `main.tex:939-979`, `supplement.tex:592-733`. |
| Componentwise positivity and branch stability | **Verified conditional on the same standard PDE results as Theorem 6.1** | Positive diagonal back-scaling preserves positivity; spectral and cubic hypotheses hold throughout the inclusive interval. See `main.tex:980-989`. |
| `chi_D`, `chi_H`, fixed product | **Independently verified** | Entry ordering gives `h_min=1`, `h_max=h_2`, `d_min=1/(91 nu L)`, `d_max=23/63`; multiplication gives the fixed identity. See `main.tex:990-1005`, `supplement.tex:744-777`. |
| Unique within-family minimum at `L0` | **Independently verified** | `chi_D` increases, `chi_H` decreases, and their ratio already exceeds one at `L0`; hence the maximum equals `chi_D` and is uniquely minimized at `L0`. No global Pareto claim is made. |
| Square-root exponent optimality | **Independently verified within the stated scope** | Endpoint formulas are `Theta(sqrt m)`; the topology-specific stationary product lower bound gives `max>sqrt(8(m-2))`. This is only for stationary crossings of this topology, as correctly stated. |

### Retuned local robustness (`Proposition 8.1`)

Source: `main.tex:1053-1073`; `supplement.tex:942-953`.

Classification: **verified conditional on standard smooth perturbation and
center-manifold results**.

The proposition is correctly restricted to perturbations within the positive
equilibrium realization manifold, with positive rates reconstructed from
positive flux/equilibrium data. The simple real eigenvalue and nonzero scalar
multiplier derivative give a locally unique retuned multiplier by the implicit
function theorem. Only finitely many low modes need individual continuation;
for a common small parameter neighborhood, if `delta` is a positive lower
bound for diffusion and `M` bounds the reaction Jacobian, the numerical-range
estimate `Re lambda <= M-k^2 delta` controls all high modes. The cubic sign and
branch spectral gap are open conditions. This proves the stated fixed-`m`,
codimension-one robustness and does not imply that arbitrary nearby parameter
points are already critical. No dimension-uniform radius is claimed.

## The all-dimensional cubic bridge

This was the strongest initial uncertainty because the shipped
`verify_cubic_sign.py` reconstructs full contractions only for
`m=3,4,5,6,8,10`, then compares them with a hard-coded formula.

I derived the bridge independently for symbolic `m`, without importing any
project helper:

1. The printed second-harmonic recurrence implies
   `w2_i-1-(1+4/K_i)w2_i=sigma`.
2. For an interior component,
   `B_i(r,w)=w_i-1-w_i-w_1/(63(m-2))`.
3. In the `w2` contraction,
   `T_i/(K_i-1 K_i)=K_i-3 K_i-2/(K_-1 K_0 K_1 K_2)`.
4. Therefore the only non-polynomial remainder is
   `sum_{i=3}^{m-1}1/K_{i-1}=\mathfrak h_m-1/K_1`; the polynomial part is
   `sum K_{i-3}K_{i-2}`.
5. An elementary finite-sum calculation gives exactly
   `(m-3)(24571m^2-97470m+96662)/3`, the identity printed in
   `proof_audit/cubic_coefficient.tex:52-58`.
6. Adding the independently reconstructed boundary contraction and the `w0`
   contraction makes the symbolic difference
   `N_m-[R_m+C_m \mathfrak h_m]` factor identically to zero.
7. Independently rebuilding the shifted polynomial signs gives `R_m>0`,
   `C_m<0`, and
   `R_m+C_m(m-2)/(90m-179)>0`. Since
   `\mathfrak h_m<=(m-2)/(90m-179)`, the numerator is positive. The independently
   reduced `ell^Tr` is negative.

Thus the all-dimensional cubic assertion is valid. The gap is in verifier
coverage/description, not in the theorem.

## Fixed-mass Fredholm and semilinear analysis

The paper's compressed argument can be made explicit as follows.

Let
`E_c={u in L^2(0,pi;R^n): integral c^T u=0}` and
`X_c=H_N^2 intersect E_c`. Reaction-wise conservation and the Neumann boundary
condition imply that the stationary linearization maps `X_c` into `E_c`.
Fourier decomposition is then exact:

- for mode zero the coefficient lies in `c^perp`, and `A|c^perp` is invertible
  and Hurwitz;
- every nonzero cosine mode automatically satisfies the integrated-mass
  condition;
- mode one has kernel `span{r}` and range of codimension one, annihilated by
  `ell`;
- every mode `k>=2` is invertible, and diffusion dominance gives a uniform
  high-mode inverse bound.

Consequently the PDE operator `X_c -> E_c` is Fredholm of index zero with
kernel `span{r cos xi}` and cokernel represented by `ell cos xi`. This also
shows directly why the homogeneous right kernel is removed: its pairing with
the mass covector is nonzero. The scaled case is identical after replacing the
mass covector by `H^{-1}c` and the adjoint by `H^{-1}ell`.

The positive diagonal Neumann diffusion operator restricted to `E_c` generates
an analytic semigroup; adding the bounded reaction Jacobian preserves
sectoriality and compact resolvent. Its half-order space is `H^1 intersect
E_c`. In one dimension `H^1` is a Banach algebra and embeds into `C^0`, so the
quadratic Nemytskii map is smooth `H^1 -> L^2`. The branch linearization is a
small bounded multiplication perturbation of the onset operator. The isolated
center eigenvalue is negative on the nonzero branch and the complementary gap
persists, so the standard principle of linearized stability yields local
exponential asymptotic stability in fixed-mass `H^1`.

The manuscript correctly distinguishes the dynamic reduced flow from the
stationary Lyapunov--Schmidt equation: see `main.tex:637-645,731-740`. Setting
the former to zero gives the latter; it does not identify the two as dynamical
objects.

The cited external tools are appropriate: Crandall--Rabinowitz's primary paper
states the one-dimensional kernel/cokernel and nondegeneracy framework for a
unique local bifurcating curve
([JFA 8 (1971), 321--340](https://www.sciencedirect.com/science/article/pii/0022123671900152));
Henry's monograph covers semilinear parabolic stability and invariant manifolds
([Springer LNM 840](https://link.springer.com/book/10.1007/BFb0089647)); Kato's
standard isolated-eigenvalue/spectral-projection perturbation theory supplies
the gap-continuation step. I therefore classify this portion as verified
conditional on standard cited results, not as a computer-algebra claim.

## Exceptional, endpoint, equality, and high-dimensional checks

- **`m=3`:** direct homogeneous factorization, exact kernel/adjoint,
  `w0/w2`, cubic contraction, exceptional scaled cubic Routh--Hurwitz proof,
  and both scaled endpoints were checked. At the upper scaled endpoint
  `L=90/91`, the gauge correction is exactly zero.
- **`m=4`:** direct determinant identities, exact nonlinear contractions, and
  both inclusive scaled endpoints were checked. At `L0=sqrt(10)/4`, the
  homogeneous certificate is exactly on `nu L^2=5/4` and remains strict away
  from zero.
- **`m=149`:** exact finite reconstruction checked kernels, adjoints,
  transversality, `w0/w2`, and the cubic identity/sign. At `L0`, midpoint, and
  `L1`, numerical spectra found no competing mode. At `L1` the rightmost
  nonzero homogeneous real part was about `-9.08e-4`; the claim is correctly
  fixed-dimensional, not uniform.
- **Modulus equality cases:** `E35` has positive pure `x,z` terms; `E77` and
  `E84` have anchors forcing `x=z=s=0`; at the `E22` boundary `U=0`, positive
  pure `x^2,z^2` terms force `x=z=0`. No equality case is inferred merely from
  a coefficient list without checking variable anchors.
- **Outside the scaled interval:** the exact `m=3` homogeneous cubic has an
  additional zero at `L=45/364` and a positive root below it. At the superseded
  `m=149,L=1/21` value, an independent floating computation found the unstable
  pair `0.00013655 +/- 0.88067839 i`. Conversely, `m=4` remained stable at
  `0.99L0`, supporting the paper's statement that `L0` is a sufficient
  certificate boundary, not an intrinsic threshold. Details are in
  `results/ADVERSARIAL_BOUNDARY_CHECKS.md`.

## Software semantics and reproduced commands

### What the relevant entrypoints genuinely check

- `verify_mode_isolation.py` (`1-94`) reconstructs `E35` and `E77`, compares
  them exactly with JSON term lists, proves the all-`m` onset derivative
  identity, and checks the determinant bridge at `m=3,4,5`. This is strong
  exact certificate evidence.
- `verify_harmonic_corrections.py` (`1-10`) checks `w0,w2` and the gauge only at
  `m=3,4,5,6,8,10` using formulas from `common.py`; it is finite exact
  regression, not an all-`m` derivation.
- `verify_cubic_sign.py` (`1-17`) checks shifted signs of three hard-coded
  polynomials, but reconstructs the contraction and compares it with the
  hard-coded `N_formula` only at `m=3,4,5,6,8,10`.
- `frontier_verify_exposition_identities.py:42-117` compares displayed `R,C`
  with `pareto_core.N0`, but `N0` is another hard-coded copy. Its generic
  second-harmonic determinant is exact; its expanded boundary solution is
  checked finitely at `m=3,4,5,6,8,10` (`235-307`).
- `frontier_verify_mode_certificates.py` reconstructs `E22,E84` exactly,
  connects the characteristic determinant at `m=3,4,5`, handles exceptional
  `m=3` exactly, checks equality anchors, and contains an exact rational Rouche
  enclosure for the superseded `m=149` endpoint.
- `verify_branch_stability.py` is explicitly a floating-point finite regression
  at `m=3,4,5,6,8,10`; it does not prove nonlinear PDE stability.
- `verify_pareto_family.py` is an aggregator. It runs exact coefficient and
  comparison certificates, but direct normal-form curves only at `m=3,4`.

`common.py` and `core.py` are byte-identical (same SHA-256
`c726d5db...e0847`), and the `dd_` harmonic/cubic scripts import the same
`common.py` formulas as their non-`dd_` counterparts. They are not independent
implementations of those formulas.

### Executions

- `python agent_nonlinear_pde/independent_exact_checks.py`: exit 0. The exact
  symbolic section plus the `m=149` spectrum sweep took about 89 seconds on the
  audit host.
- `python independent_verifier/verify_mode_isolation.py`: exit 0, 3.74 s.
- `python independent_verifier/verify_harmonic_corrections.py`: exit 0, 0.63 s.
- `python independent_verifier/verify_cubic_sign.py`: exit 0, 0.68 s.
- `python independent_verifier/verify_branch_stability.py`: exit 0, 0.76 s.
- `python independent_verifier/verify_pareto_family.py`: exit 0, 11.06 s.
- Four selected mutation tests (homogeneous coefficient, endpoint factor,
  77/84-term source, and Fourier factors): all four rejected the mutations;
  `4 passed in 0.61 s`.

Passing outputs were accepted only after the source-level descriptions above;
none is used as a substitute for the functional-analytic proof.

## Defects and exact repairs

### D1. All-`m` cubic verifier coverage is overstated

**Class:** minor reproducibility/documentation; **not mathematical**.

The public cubic entrypoints verify full contractions only in six dimensions
and compare against hard-coded closed forms. The claimed formula is valid, but
the program output alone does not establish it.

**Exact repair:** add a generic symbolic verifier implementing the recurrence
reduction and polynomial/harmonic split described in “The all-dimensional
cubic bridge” above, or incorporate
`agent_nonlinear_pde/independent_exact_checks.py`'s generic derivation. State
that the existing finite loops are regression tests. No theorem statement,
hypothesis, conclusion, endpoint, or headline changes.

### D2. Duplicate `dd_` coverage and the branch-stability filename can mislead

**Class:** minor reproducibility/expository.

The `dd_` harmonic/cubic scripts are not independent implementations, and
`verify_branch_stability.py` performs only finite floating spectral regression.
Its docstring is honest, but an audit ledger that counts entrypoint names can
overcount independent evidence.

**Exact repair:** label these as duplicate finite regression layers and rename
or document the branch script as `branch_spectral_regression`. No mathematical
change.

### D3. Fixed-mass Fredholm step is compressed

**Class:** expository only.

The conclusion is correct, but the paper would be easier to referee if it
included the four-mode Fourier argument in “Fixed-mass Fredholm and semilinear
analysis” above and explicitly stated that the fixed-mass restriction of the
analytic semigroup remains sectorial.

**Exact repair:** add that paragraph. No hypothesis, conclusion, or headline
change.

## Scope, limitations, and confidence

I did not prove the standard Henry/Kato/Crandall--Rabinowitz theorems from
scratch. I verified that the manuscript's spaces, smoothness, Fredholm index,
simple kernel/cokernel, transversality, sectoriality, and spectral-gap
hypotheses match their standard use. I did not claim global existence,
far-from-onset stability, a dimension-uniform basin, wave-instability
classification outside the certified profiles, or a global Pareto frontier;
the manuscript also expressly declines those claims.

Confidence in the exact nonlinear and scaled-family algebra is **very high**:
the central variable-dimension contraction was derived independently, not
sampled. Confidence in the local PDE conclusion is **high, conditional on
standard cited semilinear theory**. The strongest residual uncertainty is only
expository: the paper compresses the restricted-space Fredholm/sectorial
argument and its shipped cubic checker does not encode the all-`m` derivation.
Neither uncertainty changes the theorem's validity.
