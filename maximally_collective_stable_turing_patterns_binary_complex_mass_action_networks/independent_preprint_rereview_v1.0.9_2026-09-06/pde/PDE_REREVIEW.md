# Independent nonlinear and PDE rereview of v1.0.9

Target: commit `94d5177485b9680be8b77f13448abf1f923963e8`, read from the
parent audit's immutable `source_snapshot`. Date: 2026-09-06.

**Verdict within this review's scope: no new mathematical revision is
required.** The near-threshold example now has the previously missing
reaction-to-cubic and complete onset checks. The unit-equilibrium and scaled
all-dimensional local PDE conclusions survived this rereview. This verdict
does not certify publication packaging, the complete literature comparison,
or areas assigned to the other referees.

An independent cross-review after completing the PDE audit confirms the
algebra referee's separate minor hypothesis omissions in the two standalone
theorem exports. See `EXPORT_HYPOTHESIS_CROSSREVIEW.md`. Those corrections
are required for the supporting summaries, while the main theorem already
has the correct hypotheses.

## Scope and independence

I read main Sections 6 onward and Supplement S5 onward, including the generic
harmonic recurrence and its implementation, the new near-threshold verifier,
the physical-to-normalized transformation, the homogeneous mass gauge, the
normal-form and Fredholm arguments, and the branch-stability and robustness
claims. I did not take a previous referee verdict or a successful production
verifier run as mathematical evidence.

The independent program `independent_pde_checks.py` imports no project code.
It differentiates an explicitly assembled polynomial reaction field to
obtain the Jacobian and Hessian. Its interval certificates for the
near-threshold example use a Bernstein basis on `[0,1/1000]`, whereas the
public verifier uses a reciprocal substitution onto a nonnegative orthant.
The difference in mechanisms avoids merely replaying the same sign test.
The script uses explicit failure conditions and does not rely on Python
assertions. The saved `INDEPENDENT_RESULTS.json` and `INDEPENDENT_RUN.log`
record a completed PASS.

## Closure of the earlier near-threshold concern

The relevant revised prose is `manuscript/supplement.tex:950–997`; the public
implementation is `independent_verifier/frontier_verify_near_threshold.py`,
especially lines 88–168.

The current public code obtains `A(3)` and its Hessian through `pareto_core`,
whose matrix and quadratic tensor are assembled reaction by reaction from
the indexed source and product complexes. It constructs the prescribed
critical vector, obtains diffusion from `(A r)_i/r_i`, solves the left null
vector, solves the conservation-gauged zero-mode equation, and solves the
second harmonic. It then contracts the Hessian to compute the cubic. The
large rational expression is now an equality target for this derivation;
it is no longer the only source of the cubic value.

My separate reaction-field differentiation and overdetermined mass-gauge
solve recover exactly

\[
c_3(\varepsilon)=\frac{6}{1379}
 +\frac{421985}{11409846}\varepsilon+O(\varepsilon^2).
\]

The exact rational expression is recorded in the independent JSON, so this
series is accompanied by its checkable unreduced meaning. Independent
Bernstein certificates establish the following for every
`0 < epsilon <= 1/1000`:

- All four diffusivities are strictly positive.
- The reconstructed cubic is strictly positive, and the left/right critical
  pairing is nonzero.
- The crossing coefficient is strictly positive.
- For every `t >= 1`, the characteristic coefficients `a1`, `a2`, `a3`,
  `a4/(t-1)` and the Hurwitz expressions `H2`, `H3` have the required strict
  signs. Here `a4/(t-1)` means its canceled polynomial continuation at `t=1`.

At `t=1`, `a4=0` and `a3>0`, so the zero has algebraic multiplicity one.
The complementary cubic is Hurwitz because `a1,a2,a3,H2>0`.
For `t>1`, `a4>0` and the strict quartic Routh–Hurwitz inequalities give
Hurwitz stability. The independently checked identity

\[
\eta=\frac{\ell^T D_\varepsilon r}{\ell^T r}
 =\frac{\partial_ta_4(1)}{a_3(1)}>0
\]

establishes the orientation of the parameter `mu=1-t`. The homogeneous
fixed-mass cubic is independently recovered as
`(lambda+7)(lambda^2+5lambda+2)`.

These are enough for the claimed primary, transverse, subcritical
fixed-dimensional example. The statement does not claim an exact nonlinear
contrast infimum or a universal nonlinear gap. In particular, the endpoint
`epsilon=0` is correctly excluded: diffusion vanishes there and the onset
problem degenerates. The current prose expressly declines an
epsilon-uniform bifurcation neighborhood.

The algebra referee independently cross-checked this interpretation after
completing a separate audit. For `mu<=0`, each nonzero mode has
`t=(1-mu)k^2>=1`; only `k=1,mu=0` is critical. For small positive `mu`,
all `k>=2` remain in `t>1`. The sign conditions therefore establish the
claimed primary onset with the stated orientation; a positive cubic gives
subcritical branches, and the text makes no stability claim for those
subcritical branches. The reciprocal review found no missing domain or
uniformity qualification.

### Why the independent interval certificate is sufficient

For a canceled numerator and denominator, extract any power of epsilon,
which has known positive sign on the stated open interval. Expand the
remaining polynomial by nonnegative powers of `s=t-1`. For each coefficient
polynomial `p(epsilon)`, write `epsilon=z/1000`, with `0<=z<=1`, and convert
to the Bernstein basis. The basis functions are nonnegative and sum to one.
Nonnegative Bernstein coefficients prove each block nonnegative; strictly
positive coefficients in the `s^0` block prove strict positivity for every
`s>=0`, including the boundary `s=0`. Both numerator and denominator are
treated, so no unproved denominator sign or interval pole is hidden.

## Reconstruction of the main local PDE proof

### 1. Homogeneous mass restriction and mode spectrum

For the unit family, `c^T f=0` identically, not merely at the equilibrium.
Neumann boundary conditions give
`integral c^T D u'' = c^T D [u']_0^pi = 0` even when the diagonal diffusion
entries differ. Thus the restriction is by integrated mass; a pointwise
constraint `c^T u(x)=0` would be incorrect and is not used.

The homogeneous conservation eigenvalue is simple and is removed on the
homogeneous `c^perp` coefficient. For nonzero cosine modes the mean condition
places no additional restriction. The critical `k=1` block has one simple
zero, and all other blocks have negative spectrum.

I independently regenerated the exact modulus polynomials with 35, 77, 84
and 22 nonzero monomials. Every coefficient has the stated sign. I also
checked positive pure-axis monomials, so absence of a constant term is not
mistakenly used on its own to assert origin-only equality. These checks
verify actual polynomial identities and equality cases; they are not
spectral sampling.

The chain estimates that apply these fixed boundary polynomials remain
valid for all integer dimensions. For example, writing a scaled chain
factor as a positive multiple of `1+L lambda` plus the nonnegative real
number `(t-1)/K_i` can only increase its modulus in the closed right
half-plane. The homogeneous estimate uses the separate sufficient boundary
`nu L^2 >= 5/4` for `nu>=2`. The exceptional case `nu=1` uses its actual
cubic Routh inequality. Neither lower endpoint is asserted to be a true
dynamical stability boundary.

### 2. Fredholm property and the infinite-dimensional complement

The operator on the fixed-integrated-mass tangent spaces has domain
`H_N^2` and range space `L2`. The modewise inverses satisfy `O(k^-2)` at
large `k`, obtained from the displayed Neumann-series factorization.
This maps compatible `L2` data into `H_N^2`; it proves closed range and
Fredholm index zero, with kernel `r cos(x)` and cokernel `ell cos(x)`.
The transversality pairing is nonzero and has the correct sign.

The infinite-dimensional conclusion does not rely on checking finitely many
arbitrarily selected spatial modes. At onset, the symmetric-part estimate
places the high spectrum arbitrarily far into the left half-plane. Along a
small patterned branch the reaction Jacobian is a bounded multiplication
perturbation and the positive diffusion coefficients remain bounded below.
Fixed-domain sectorial resolvent estimates control high frequencies; only
a finite collection of isolated low eigenvalues then needs continuation.
Fourier modes need not remain uncoupled on the patterned branch for this
argument to work.

### 3. Cubic coefficient, reflection, and branch stability

The factors `-1/4` in both correction equations follow from the factor
`1/2` in the quadratic Taylor expansion and
`cos^2(x)=(1+cos(2x))/2`. Projection of the third-order reaction term gives
`B(r,w0) + B(r,w2)/2`. The zero-mode gauge removes the freedom to add the
homogeneous conservation eigenvector. These choices are consistent between
the dynamic center-manifold coefficient and the stationary reduction.

I read the generic recurrence verifier as an algebraic proof: it anchors
both critical vectors to boundary and interior equations, verifies the
zero-mode solution and mass gauge, verifies the second-harmonic boundary
solve and interior recurrence, and explicitly reduces the remaining chain
sum to its polynomial and harmonic-sum components. Its formula is an
identity in the rational function field, not a fit to a finite sequence of
dimensions. The boundary denominator has the stated shifted-positive
certificate. No assumption of the target cubic sign occurs in this bridge.

Independent exact reaction-derived contractions in dimensions 3, 4, 6 and 9
agree with the stated unit numerator. These are finite checks of the
reaction-to-formula interface, supplementary to the generic proof.

Reflection about the midpoint preserves the PDE and fixed-mass class and
negates the critical cosine. The equivariant reduced vector field is odd;
the cubic has negative sign and the crossing coefficient has positive
sign. Consequently the nonzero branches for small positive `mu` have a
negative center eigenvalue, while the complementary gap persists.

The generator is sectorial with compact resolvent; its half-order phase
space is the corresponding fixed-mass `H1` space. In one dimension the
quadratic Nemytskii map is smooth from `H1` to `L2`. These are the relevant
hypotheses for the cited center-manifold and linearized-stability results.
The proof invokes those classical analytic-semigroup theorems rather than
reproving them. I found no missing application hypothesis. The patterned
branch converges to a strictly positive constant in `H_N^2`, hence uniformly,
so strict componentwise positivity follows for sufficiently small amplitude.
Neumann conditions on an interval do not supply a continuous translation
neutral direction.

### 4. Physical scaling and the homogeneous gauge

For `xhat=H x`, the physical system becomes
`xhat_t=H[f(xhat)+(1-mu)Delta xhat'']`. The effective stationary equation is
unchanged. Dynamic left vectors and integrated-mass covectors change to
`H^-1 ell` and `H^-1 c`, respectively. This is consistent with physical
diffusion `Dphys=H Delta`; no mistaken similarity or preservation of
eigenvalues under arbitrary row scaling is assumed.

The second harmonic is unchanged after canceling the invertible row factor.
The zero harmonic changes by exactly `tau rho`. My independent symbolic
summation bridge derives `tau` for symbolic dimension and formal harmonic
sum directly from

\[
\sum_{i=2}^{m-1}\frac1{K_i}
 =\mathfrak h_m-\frac1{K_1}+\frac1{K_{m-1}},\qquad
\sum_{i=2}^{m-1}\frac{i-2}{K_i}
 =K_2\sum_{i=2}^{m-1}\frac1{K_i}-(m-2).
\]

It agrees with the printed rational gauge and both printed derivative
identities. Independent shifted-polynomial checks establish the reference
margin `Nref>1/100`, and the endpoint comparison for `tau<1/20` is an exact
identity with the stated sign. The bound `-1/10<S<0` then yields
`N(L)>1/200`, including when `tau` is negative. The critical pairing is
strictly negative; it both proves the cubic sign and rules out a generalized
eigenvector at zero. The crossing numerator is unchanged after scaling.

The separate finite checks solve the complete mass-gauged correction for
symbolic `L` in dimensions 3, 4, 6 and 9. They agree with the gauge identity
and have the claimed cubic margin and sign at both exact algebraic
endpoints in every tested dimension. This is eight exact endpoint checks;
the all-dimensional interval claim comes from the generic proof above.

### 5. Robustness and quantifiers

The perturbation statement fixes a dimension and a certified `L`. Positive
steady fluxes and positive equilibrium coordinates parameterize allowable
nearby realizations, preserving the reaction topology and conservation
identity. Spatially homogeneous rate and diffusion perturbations preserve
reflection. After an interval rescaling to a fixed reference domain, the
simple eigenvalue and nonzero scalar-diffusion derivative allow the implicit
function theorem to continue one nearby crossing. Positivity, low-mode
gaps, high-frequency resolvent bounds and the negative cubic sign persist
locally. This proves a retuned local statement, not that each unretuned
nearby parameter point is itself critical.

The manuscript correctly declines dimension-uniform robustness, global
attraction, arbitrary-data bounds, a uniform near-threshold limit, or a
constant-optimal complete Pareto frontier. The finite interval and diagonal
diffusion conditions are essential and are stated. I found no hidden
strengthening of these quantifiers in the central conclusions.

## Optional wording improvement, not a required correction

At `manuscript/main.tex:655–656`, “the well-mixed Jacobian, equivalently the
homogeneous k=0 mode restricted to c^perp, is stable” can be made unambiguous
by writing “the well-mixed Jacobian restricted to c^perp is Hurwitz.” The full
Jacobian has its conservation zero. Context and the following proof already
make the intended restriction clear, so this is an optional wording
improvement, not a newly discovered theorem failure or a publication blocker.

## Evidence and residual limits

| Approach family | Evidence in this round | Status | Remaining gap |
|---|---|---|---|
| New near-threshold example | Reaction differentiation, exact harmonic solves, independent Bernstein interval certificates, exact Routh expressions | Verified | None for the stated fixed-dimensional local claim |
| Unit all-dimensional local branch | Full proof reconstruction, generic recurrence inspection, independent modulus regeneration and finite reaction contractions | Verified within scope | Classical center-manifold and linearized-stability results are invoked |
| Scaled local branch | Physical transformation, generic mass-gauge summation, shifted sign certificates, symbolic-L finite solves and exact endpoints | Verified within scope | No global or dimension-uniform stability conclusion is supplied or claimed |
| Retuned robustness | Hypothesis-by-hypothesis implicit-function and sectorial-gap argument | Verified within scope | Neighborhood sizes are not explicit; the proposition does not promise them |
| Numerical figures and release assets | Assigned to other referees | Not adjudicated here | See the parent referee report |

No new mandatory nonlinear/PDE change is identified by this round. The old
near-threshold gap is closed in the actual current source and independently
verified, not merely described as closed in an editing summary.
