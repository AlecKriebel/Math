# What can presently be certified

## 1. Target and convention

Let A_m = −Δ + m² on real L²(Rⁿ), m>0, and let χ be multiplication by the
indicator of the unit ball D. In one spatial dimension D=(−1,1). The Cauchy-data
one-particle space is H_m^{1/2} ⊕ H_m^{−1/2}, equivalently the A_m^{±1/4}
Sobolev realization. Its complex structure is

    i_m = [[0, A_m^(−1/2)], [−A_m^(1/2), 0]].

Writing K_m = −i_m log Δ_D gives

    K_m = [[0, M_−(m)], [−M_+(m), 0]],
    M_±(m) = 2 A_m^(±1/4) arcoth(B_m) A_m^(±1/4),
    B_m = closure(A_m^(1/4) χ_(1/4) A_m^(−1/4)
                +A_m^(−1/4) χ_(−1/4) A_m^(1/4) − I).

The Sobolev cutting projections and closures are essential. This is the
BCM Proposition 2.3 construction, not a claim that χ is bounded on every
Sobolev space. In the global block realization,

    M_+ = A_m^(1/2) M_− A_m^(1/2).

The exact problem asks whether M_− is independent of m and whether it is a
position-space multiplication operator. Equality is in this time-zero
realization, not equality after choosing arbitrary mass-dependent unitaries.
The second question includes any possibly mass-dependent multiplier. A formula
for one angular sector, for a leading singular term, or for a finite cutoff
does not settle it.

## 2. Strongest result: an exact conjugation obstruction

Put q(x)=1−|x|² and ω_m=A_m^(1/2). On the Schwartz space, for every n≥1 and m>0,

    ω_m q ω_m
      = −∇·q∇ + m²q + (n−1)I + m² A_m^(−1).                 (2.1)

This is an identity of operators on Schwartz functions. For m>0, ω_m and its
inverse preserve Schwartz space, so all compositions are defined there.
The proof is in Attempt 2 and checked symbolically in dimensions 1–5.

The last summand has a strictly positive integral kernel off the diagonal:

    G_m(z) = ∫₀^∞ exp(−m²t) (4πt)^(−n/2) exp(−|z|²/(4t)) dt,
    z≠0.                                                       (2.2)

Consequently, if 0≤h∈C_c^∞(D) is nonzero, then ω_m q ω_m h is strictly positive
outside the closed ball. All other terms in (2.1) vanish there.

Here is the precise modular consequence, including its domain condition:

**Global ansatz obstruction.** Suppose a proposed modular realization has
M_−=c q globally, c≠0, as a multiplication operator whose domain includes
Schwartz functions; its conjugate block agrees with ω_m M_− ω_m on
C_c^∞(D); and these vectors lie in the generator domain. Then that realization
cannot preserve the standard subspace of data supported in the ball.

Indeed, modular invariance of that closed real subspace implies that the
generator maps each vector in its domain and the subspace back into the
subspace: take the difference quotient of its invariant unitary group. Applied
to (h,0), this contradicts the nonzero exterior component −M_+h.

This is a genuine obstruction to the globally extended massless-parabola
ansatz under the stated realization. It is not a proof that the *restriction*
of M_− to the ball differs from the parabola: its exterior action enters
ω_m M_− ω_m because ω_m h is not supported in the ball. Nor does it exclude
arbitrary nonpolynomial multipliers. No unproved core assertion is suppressed
to upgrade the obstruction into a complete answer.

## 3. Other checked deductions

1. The finite-dimensional mass derivative has an exact resolvent formula.
   Both the exterior A-factors and B vary with the mass. A nonzero derivative
   of B alone therefore proves nothing about the derivative of M_−. Domain
   and endpoint-control difficulties block the continuum derivative route.
2. Dilation gives

       M_−(m,R) = R U_R M_−(mR,1) U_R^−1,
       (U_Rh)(x)=R^(−n/2)h(x/R).

   Rotational covariance forces any global multiplier to be radial. Entropy
   positivity and tangent-wedge comparison give necessary restrictions, but
   leave a large family of possible multipliers. These do not prove that the
   conformal expression is the only possibility.
3. An exact four-dimensional one-particle structure has a strictly non-diagonal
   M_− in its fixed position basis, and adding a scalar to A changes M_−.
   This refutes a possible *abstract* algebraic cancellation argument. It is
   explicitly not a discretization certificate for the massive scalar field.
4. The arcoth singularity at ±1 prevents a generic norm-convergence argument.
   Arbitrarily close matrices can have arcoth values separated by a fixed
   amount. We give a quantitative bound with a fixed spectral gap and a
   precise continuum witness/error criterion; the required continuum error
   bounds were not obtained.

## 4. What remains open here

- Establishing or disproving mass independence for the actual continuum block,
  with the precise identification and domains justified.
- Establishing a nonzero off-diagonal continuum distributional matrix element,
  or proving exact multiplication and identifying the multiplier.
- Upgrading numerical angular-momentum dependence to a certified continuum
  witness, with discretization, exterior-cutoff, and endpoint errors controlled.

Strong-resolvent continuity of the modular group cannot simply be differentiated
to identify the unbounded Cauchy-data block. A scalar “leading local term”
calculation is not equality of the full kernel. These are explicit stopping
gaps, not claims of impossibility of a future proof.

**Final classification:** five-attempt budget exhausted, exact source target
unresolved. The public-facing material is a partial research report and
verification package, not a solution paper. No theorem of novel priority is
claimed. The complete derivations and their limits are recorded in the five
attempt files.

