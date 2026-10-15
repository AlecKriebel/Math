# Independent review of the uniform-quasilocal concentration bridge

Review scope: `../QUASILOCAL_SOURCE_BRIDGE.md`, especially Parts A and C.
The precise reviewed input hash and UTC are recorded separately. The original
BMP1999 paper remains unavailable. The task supplied the indexed BMP2007
uniform cylinder-oscillation definition and its primary PDF URL; this review
does not upgrade that passage access to complete-source clearance.

**Verdict:** Part A's positive implication is mathematically valid under the
explicit uniform oscillation definition, i.i.d. finite-alphabet inputs, and
nondegenerate binomial weights. Its exponent is `exp(-c_R s^2 sqrt(N))`.
Part C's unbounded-density construction is valid and matches the independent
proof in `QUASILOCALITY_AND_UNBOUNDED_DENSITY.md`. The incompatibility remains
conditional on identifying the two correction fields; no such identification
or theorem-false conclusion is established.

## 1. Uniform approximation and null-set issues

The finite-cylinder representative proof gives bounded `Phi` and a bounded
cylinder function `Phi_R` with uniform error at most `delta` on the common
full-probability domain. Recentering gives `E Psi_R=1` and error at most
`2delta`, as stated. One may define `Psi_R` arbitrarily and boundedly on
zero-probability cylinder patterns. For the uniform approximation of all shifted
coordinates, intersect the full-measure domain over countably many integer
space-time shifts. This still has probability one. These observations justify
both applying independent-input bounded differences to an everywhere-defined
finite-cylinder function and transferring the estimate almost surely to `Phi`.

The transfer bound is exactly `|H_N(Phi)-H_N(Psi_R)|<=2delta`, since `sum b_N=1`.

## 2. Mean bound: use a separate window parameter and no positivity assumption

Fix the approximation radius `R` and a bound `B_R>=|Psi_R|`. Let `A>=1` be a
separate central-window parameter. Finite dependence gives

`Var(sum_(x in I)b_N(x)(Psi_R(shift_x eta)-1))
 <= C_R sum_(x in I)b_N(x)^2`.

For example, bound each covariance by `4B_R^2`, retain pairs at distance at
most `2R`, and apply `2b_x b_y<=b_x^2+b_y^2`. The earlier central-cell count
then gives

`E H_N(Psi_R) <= C_R sqrt(A/M+N^-1/2)
                    + C(B_R+1)/A^2`.                       (Q1)

The tail uses
`E|sum_(x in I)b_N(x)(Psi_R(shift_x eta)-1)|
 <= (B_R+1)b_N(I)`.
This explicit replacement matters because recentering a cylinder approximation
does not preserve nonnegativity. It is not necessary to impose nonnegativity:
the boundedness estimate proves the desired result directly. First choose `A`
large, then send `N` to infinity with `M_N` diverging, keeping `R` fixed.
Thus the mean tends to zero uniformly over deterministic alignments.

## 3. Independent-input sensitivity and the concentration exponent

For each input `z=(s,y)`, changing it affects only endpoint coordinates with
`|x-y|<=R` and only when `s` is among a fixed number of terminal time layers.
Using the norm's triangle inequality, its oscillation is at most

`c_z <= 2 B_R sum_(|x-y|<=R)b_N(x)`.

Extend `b_N` by zero outside its finite support. For a cube of radius `R` in
one space and one time coordinate, Young's inequality makes the calculation
fully explicit:

`sum_z c_z^2
 <= 4B_R^2(2R+1) ||1_[-R,R]*b_N||_2^2
 <= 4B_R^2(2R+1)^3 ||b_N||_2^2
 <= C_R/sqrt(N)`.                                         (Q2)

The relevant input union is finite, even though the environment itself is
infinite. Independent-input bounded differences therefore gives

`P(H_N(Psi_R)-E H_N(Psi_R)>s)
 <= exp(-2s^2/sum_z c_z^2)
 <= exp(-c_R s^2 sqrt(N))`.                               (Q3)

The oscillation bound does not depend on the number or width of partition
cells, so it remains valid for odd-width sheared cells and all alignments.
Counting all support coordinates without their weights would indeed lose the
factor needed in (Q2); the convolution calculation avoids that loss.

For fixed `epsilon`, choose `delta<epsilon/16`, then one fixed `R(delta)`.
By (Q1), eventually `E H_N(Psi_R)<epsilon/4`. Uniform approximation and (Q3)
then yield `P(H_N(Phi)>epsilon)<=exp(-c_epsilon sqrt(N))` after adjusting the
constant. No rate for the decay of cylinder oscillation, and no lower rate for
the divergence of `M_N`, is needed. This is a genuine positive implication for
the **stationary factor**, stronger than what covariance alone supplies.

## 4. Residual and source limitations remain distinct

Part A does not estimate the random difference between the single-origin
endpoint law and its stationary-factor ansatz. Qualitative almost-sure or
finite-moment convergence of that residual cannot be substituted for a
superpolynomial failure probability; the exact binomial modulation construction
already supplies a counterexample to that abstract substitution.

The source-bridge report appropriately leaves unresolved the original source's
window, mode of residual convergence, and correction-field identification.
Its conditional suggestion concerning a deterministic uniform residual is
reasonable. If completing that suggestion, a mere application of Markov to
the annealed tail would not supply an all-power probability bound. One can
instead combine mass normalization of the endpoint law with concentration of
the bounded quasilocal weighted field on a large fixed central window; the
central residual then controls the quenched outside mass. That would be an
additional explicit deduction from the stronger deterministic-residual
assumption, not an interpretation of an unspecified source `o(1)`.

The two minor expectation-proof clarifications above do not change Part A's
conclusion. Part C's funnel mechanism requires no revision. This review does
not assess the separate target i.i.d.-RWRE proof.
