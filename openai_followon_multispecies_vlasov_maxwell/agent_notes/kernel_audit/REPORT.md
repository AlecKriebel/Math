# Independent signed-kernel audit

Checkpoint: 2026-10-06 21:23:47 America/Los_Angeles (2026-10-07 04:23:47 UTC).
Owned scope: source/receiver kernel, signed identity, local coefficient,
selection arithmetic, and the mechanism for extending these to fixed finite
species. No external individuals were contacted. No repository or publication
operation was performed by this agent.

Best-guess completion within this agent's assigned scope: kernel mathematics
95%; global target mathematics 35%; publication package 0%. These numbers are
work estimates, not proof evidence. Global continuation, baseline occupation,
priority, formalization, and a complete package remain outside this audit.

## What was actually read and checked

All source references below refer to `sources/upstream_pinned/preprints/Global-classical-solutions-of-the-three-dimensional-relativistic-Vlasov-Maxwell-system-September-23-2026/build/sections/`.

* `setup.tex`: entire file; the impulse bootstrap and momentum doubling.
* `retarded.tex`: entire file; source-label Jacobian, fields, acceleration bounds,
  and retarded receiver measure.
* `cancellation.tex`: entire file, independently derived algebra and multiplier
  bounds.
* `direct.tex`: entire file; read all tables, balancing, angular/momentum sums.
  This does not independently establish the occupation inputs.
* `direction.tex`: entire file; read the stopping argument, projected selection,
  and direction-based occupation. No independent certificate for occupation.
* `selection.tex`: entire file; checked all exponent inequalities in lines
  130–270 by exact rational arithmetic and reviewed transition/time weights.
* `closure.tex`: entire file; checked simultaneous-bootstrap algebra and
  continuity argument.

No Lean declarations or builds were inspected by this agent. The result below
is ordinary mathematics plus a narrowly scoped exact arithmetic certificate;
it is not a claim of a formalized impulse estimate or theorem.

## Strongest verified statement

The signed source/receiver identity is kinematic: it holds for arbitrary
differentiable strictly timelike source and receiver curves, with arbitrary
accelerations. It does not require equal charges, equal masses, positive
charges, or a one-species Lorentz law. Multiplication by the fixed signed
source/receiver factor preserves it. Its receiver-derivative coefficient and
projected coefficient admit the same angular/radial exponents, with fixed
species-dependent multiplicative constants. Thus charge signs and positive
mass ratios do not obstruct the actual kernel cancellation.

This does **not** by itself establish the global multispecies theorem. It
establishes the decisive algebraic extension and the selected-coefficient
mechanism conditional on valid baseline/direction occupation estimates for
the simultaneous bootstrap. A complete proof still requires those estimates,
local theory, continuation, and dependency validation.

## Exact normalization and coupling

Write physical momentum as `p_a`, normalized momentum `v=p_a/m_a`, and
`F_a(t,x,v)=m_a^3 f_a(t,x,m_a v)`. Then

\[
q(v)=\sqrt{1+|v|^2},\quad u(v)=v/q(v),\quad
\lambda_a=e_a/m_a,
\]
\[
\partial_t F_a+u\cdot\nabla_xF_a+
\lambda_a(E+u\times B)\cdot\nabla_vF_a=0,
\quad \rho=\sum_a e_a\int F_a\,dv,
\quad j=\sum_a e_a\int uF_a\,dv.
\]

Using `f_a(t,x,m_a v)` without the factor `m_a^3` would instead put the
Jacobian factor into every Maxwell source and energy term. Either convention
is valid; mixing them is not. Here all displayed formulas use `F_a`.

The conserved positive energy and flux are

\[
\mathcal U=\tfrac12(|E|^2+|B|^2)+\sum_b m_b\int qF_b\,dv,
\quad \mathcal S=E\times B+\sum_b m_b\int quF_b\,dv.
\]

The kinetic work of species b is `e_b E·∫uF_b dv`; it cancels its signed
Maxwell work. Thus energy positivity uses `m_b>0` and `F_b>=0`, not charge
positivity or neutrality. Specieswise particle cone flux satisfies
`∫r²q d F_b ≤ H_0/m_b`, since all species' contributions to the total flux
are nonnegative. Every fixed mass enters the resulting constants explicitly.
No uniformity as a mass tends to zero is implied.

For a receiver of species a, let `K_a=V_a'` in normalized momentum. Each source
b's contribution to its force has the fixed factor

\[
c_{ab}=\lambda_a e_b=e_a e_b/m_a.
\]

The source velocity derivative itself is
`b_b=λ_b q_b^{-1}(I-u_b⊗u_b)(E+u_b×B)`. Therefore the raw acceleration
kernel includes the sign of `λ_b`, and it would be incorrect to replace it
by an unsigned acceleration before integrating by parts.

## Independent derivation of the signed identity

Set `t=s+r`, `rn=X_a(t)-Y_b(s)`, `d=1-n·u_b`, `D=1-n·a`, and
`e=1-a·u_b`; the last `e` is geometric and is not a species charge. Use
`q_b^{-2}=1-|u_b|²`, `q_a^{-2}=1-|a|²`, and

\[
t'=d/D,\quad r'=d/D-1,\quad
rn'=N_0=(d/D)(a-n)+n-u_b.
\]

Strict timelikeness gives `d,D>0`. The source-label map has Jacobian
`dz=d dy dv`, because the fixed-time flow has determinant one and the
retarded inverse flow is the rank-one perturbation
`I-(u_b,V_b')⊗(n,0)`. This determinant calculation is independent of
`λ_b`. Combining with `dt/ds=d/D` yields

\[
F_{b0}\,dz\,ds=D F_b\,dy\,dv\,dt.
\]

Let `Q=D I+n⊗a`, `H=Q/D`, `g=(u_b-n)/d`, and
`k_0=u_b-(e/D)n`. Then `Hg=k_0/d`. In branch measure the interior force
kernel, with its common factor `c_ab/(4π)` removed, is

\[
\mathcal K=-\frac Hr\partial_s^{(u_b)}g
-\frac{Hg}{r^2q_b^2d}.
\]

The product rule and the following exact identities give its decomposition:

\[
\partial_a k_0[A]=n(A\cdot k_0)/D,
\]
\[
N_0\cdot u_b-d r'-q_b^{-2}=-ed/D,
\]
\[
r d(k_0)'_n=-\frac{ed}{D}
\left(N_0+\frac{n(N_0\cdot a)}D\right),
\]
\[
N_0+\frac{n(N_0\cdot a)}D+k_0
=\frac dD\left(a-\frac{n}{q_a^2D}\right).
\]

Since `a'=a_t d/D`, the result is exactly

\[
\boxed{\mathcal K=-\left(\frac{k_0}{rd}\right)'
+\frac{e}{r^2D^2}\left(\frac{n}{q_a^2D}-a\right)
+\frac{n(a_t\cdot k_0)}{rD^2}.}
\]

This is cancellation.tex 49–102 with the source and receiver energies
distinguished. The identity is linear in all terms; multiplying by negative
`c_ab` does not change it. Importantly, the source acceleration disappears
exactly, including its sign and mass factor. In `dt dy dv` measure the
residuals for a,b are

\[
\mathcal R_{ab}=c_{ab}\frac{F_b e}{r^2D}
\left(\frac{n}{q_a^2D}-a\right),\quad
\mathcal A_{ab}=c_{ab}\frac{F_b n(a_t\cdot k_0)}{rD}.
\]

Now `a_t=q_a^{-1}(I-a⊗a)K_a`, where **K_a is the full shared-field
force**, not the force of b alone. The ensuing estimate is coupled and
cannot be obtained by adding one-species theorems.

## Primitive, cutoffs, and pointwise estimates

At the same dyadic representatives as upstream, `q_b~p`, `q_a~w`,
`d~θ²`, `D~φ²`, `r~h`, and `θ≤16κφ`, one has

\[
|e-D|\lesssim\phi\theta,\quad |k_0|\lesssim\theta/\phi,
\quad |P_a k_0|\lesssim\theta,\quad |P_a n|\lesssim\phi.
\]

The nonprojected receiver term/cutoff-derivative majorant is
`C |c_ab| F_b θ |K_a|/(w r φ²)`; its projected version gains φ.
The moving projector `Π=w P_a/|V_a|` has
`|Π_t k_0|≤C θ|K_a|/(wφ)`, so its derivative has the projected size.
No species ratio occurs in this geometric computation; ratios are confined
to the fixed factors and density/energy constants.

Source cutoff derivatives use the source Lorentz law and therefore acquire
an additional fixed factor `|λ_b|`. Their bounds are
`C |c_ab λ_b| [F_b φG/(r p θ²)+F_b φ|B|/(r p)]`.
This is the only additional source-acceleration coefficient. It changes
constants, not powers. Derivatives of the selected partition sum can be
assigned to adjacent unselected supports only after factoring out the common
physical multiplier, as correctly specified in cancellation.tex 165–169.

The initial-cone boundary primitive is bounded with `D k_0=Du_b-ne` and
the initial momentum bound; no lower bound on receiver D is required there.
The tip is removed with a radial cutoff and an `O_comp(γ)` error. Labelwise
collision exclusion is valid separately for each source species by the
`O(ζ²)` grid argument in retarded.tex 412–427. A finite species union of
these null sets remains null.

## Species-dependent coefficient and selection arithmetic

For one small bin at a fixed receiver time, positivity and the cone budget
give the two-sided coefficient

\[
U_{ab}\le C_{ab}w^{-1}
\min\{h^2(p\theta)^3,(p\theta h\phi^2)^{-1}\},
\]

where one may take the density part proportional to
`|c_ab| ||F_b0||∞` and the flux part proportional to
`|c_ab| H_0/m_b`. The projected coefficient gains φ in the density bound.
The constant is finite for fixed finite species and fixed positive masses;
it need not be small.

Independently checking selection.tex 130–270 produced no arithmetic flaw:

1. `Δ=ε(α+b+y+H)`, with `ε=1/100000`, obeys
   `Δ<4z/99995<z/1000` from near selection and energy occupation.
2. If the representative coefficient were unsafe, the energy far inequality
   forces `H>z/2+3(α+c)-4Δ`, hence
   `H>(496/1000)z+3(α+c)`. Near selection gives
   `3.5α+1.5c+2y<.753z`, `z>500/751`, and `mφ>P^.3`.
3. Stable-cell occupation gives `b<H/2-min(α,c)+y+.002z`, so
   `2y>H/3+.328z+2min(α,c)` and `H<.8076z`.
   Consequently `α+c<.105z`, `z>200/221`, `1-α>.895`, and
   `.16max(z,1-α)<y<.49min(z,1-α)`: the improved window applies.
4. Improved occupation with `β=29/25` gives
   `βy>H/3+.33z+2min(α,c)`. Near selection gives
   `βy<.582z-.29H`. Thus `H<(378/935)z<.41z`, contradicting
   `H>.496z`.

Therefore the exact representative inequality `U≤w^{-1/2}W` applies unchanged
with simultaneous all-species P,M,A; the actual coefficient has the factor
`C_ab`. Summing fixed finitely many b and all selected dyads gives
`Σ_b coefficient≤C w^{-1/2}`. Multiplying by the simultaneous baseline
absolute-force estimate `∫|K_a|≤C√w B(I,w)` cancels √w. This is the
correct coupled closure mechanism. Charges need not make the receiver term
positive; the coefficient is estimated in absolute value.

The closure choices in closure.tex 46–55 have sufficient slack:
`CηM≤A/16`, `Cη√A≤A/16`, and `2Aη≤A/8`, while
`Cη+2M√η≤M/4`. A finite-species maximum can be used in the open/closed
continuity argument and the momentum-doubling argument without changing their
logic, provided all prior estimates have truly been proved simultaneously.

## Boundary tests and limitations

* `e_a=0`: `K_a=0`, receiver momentum is constant, every pair factor vanishes.
* `e_b=0`: b is free transport and contributes no Maxwell source; its charged
  kernel contribution vanishes. It may still be included harmlessly in positive
  energy and maximum momentum.
* Equal masses `m_a=m_b=m` and opposite charges `+1,-1`: factors are
  `+1/m` for equal signs and `-1/m` for opposite signs. Exact cancellation
  is unchanged. Source accelerations have signs `±1/m` before cancellation.
* Identical species with the same mass/charge can be combined by adding their
  F densities. Distinct charges cannot generally be combined because their
  characteristic accelerations differ.
* One species with `m=e=1` reproduces every upstream displayed kernel.
* Fixed extreme mass ratios enlarge `H_0/m_b`, `|λ_b|`, and `|c_ab|`;
  no estimate here is uniform toward mass zero or an infinite species limit.
* Nearly null source or receiver velocities retain `d,D>0`; denominators
  grow but the exact identity remains valid. No massless limit is claimed.
* Net total charge can be nonzero: a three-dimensional Coulomb tail behaves
  as `r^{-2}` and has finite exterior field energy. Neutrality does not enter
  this kernel or energy audit. Continuation data modifications still need
  independent validation for signed charge density.

## Reproducible certificate

Run `python3 checks/kernel_audit/exact_kernel_certificate.py` from the project
folder. Python 3 standard library only. The certificate fixes n=(0,0,1) by
rotation covariance and expands denominator-cleared polynomial residuals in
the six independent components of a,u. The scalar geometry identity and all
three components of the vector geometry identity have identically zero
coefficient dictionaries. The derivative formula for k0 and product rule
then give the displayed signed identity. Supplementary assembled checks use
292 exact rational inputs, arbitrary signed accelerations, zero/identical/
opposite/nearly null velocities, and radii `10^-6,1,10^6`.

Output: `universal_polynomial_residuals=[0,0,0,0]`,
`exact_rational_combined_checks=292`, `result=PASS`.
This certifies the kernel algebra only; it certifies no PDE solution,
occupation estimate, bootstrap, continuation theorem, priority, or publication.

## Source hashes

SHA-256:

* retarded.tex: `eedf365c0be2cefacecc93c2825b4991ccad1d32826d83aa24eb4b63ccf37be2`
* cancellation.tex: `6b615a3b4ba0fbb6d04ea2e88b441dabdd51f6b33fc976b23407413fc9ae162a`
* direct.tex: `aed0cd43a04c66b5ffb4bb30de2377dafa1eaa58a6c5e7d0c40865662f9e6de1`
* direction.tex: `aeab95505df9a9d2b8bca153832ea69039eb0fa078788775ea15e34fb8531432`
* selection.tex: `1ece8e662bff978906fbc1ddc578ea09a89322accee598d043aa3a7403583445`
* closure.tex: `499230223647c95c6e9d536c78e9cd5dd098a011d9213b733daaab3d8bba8e89`
* setup.tex: `40a7d4abe6fa5d9dc96a6ffd689e602a10bb7a1cf3bd9fd8f0caa70cf72a9cf7`
* exact_kernel_certificate.py: `2a72fa2d10d0b437077a01bca259538b739851fe78c53abc3c098b199c4bf377`

## Exact remaining gap and route status

No counterexample or kinematic/sign obstruction was found. The signed-kernel
route is **not blocked by species signs or masses**. This agent has not
independently reconstructed the occupation proofs or validated local theory.
It would be circular to call the above conditional mechanism a global theorem
until those exact remaining dependencies are independently proved. The root
must not promote a full solution solely from this report or certificate.
