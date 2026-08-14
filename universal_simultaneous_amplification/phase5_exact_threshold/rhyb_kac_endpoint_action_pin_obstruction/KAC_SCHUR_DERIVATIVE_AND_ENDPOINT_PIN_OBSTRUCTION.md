# Kac Schur derivatives and the endpoint-pin obstruction

Date: 2026-08-13 (America/Los_Angeles)

No graph search, parameter search, determinant ansatz, literature search, or
external communication was used.

## 1. Status and scope

**EXACT DERIVATIVE IDENTITY AND SCOPED PROOF-ROUTE OBSTRUCTION.**  The
singleton Kac reward really is a directional derivative of a pinned object,
but the object is the Schur complement of the **full nonempty-subset
generator**.  It is not a directional derivative of either vertex endpoint
action.

This distinction cannot be repaired by an ordinary coordinate source or
hard coordinate pin in the endpoint action.  On every loopless complete
regular module the two endpoint actions are the same function, so all such
pins, values, and derivatives agree between Bd and dB.  The two full-state
Kac rewards are nevertheless different.  Already on `K_2` they are both
positive for `1<r<2` and equal

\[
                 \psi_B={1\over r},\qquad
                 \psi_D={2-r\over r}.                 \tag{1}
\]

Consequently no rule-blind construction from the endpoint action and an
ordinary root-coordinate pin can recover the two Kac residues.  Any bridge
from the new global-minimum theorem to

\[
                         r^3\psi_{B,i}\psi_{D,i}\leq1 \tag{D-KAC}
\]

must add rule-specific, coalescence-sensitive full-state information.

This result does **not** prove or refute `(D-KAC)`.  It closes only the
proposal that `(D-KAC)` follows by interpreting the two Kac factors as the
same kind of directional derivative or coordinate-pinned value of the two
natural endpoint actions.

## 2. The exact full-state Schur derivative

Let `Q` be the row generator of a finite recurrent chain, let `i` be a
singleton root, and put `R=Omega\{i}`.  The killed block `Q_RR` is
nonsingular.  For a column reward `g`, introduce the diagonal Feynman--Kac
tilt and its scalar root Schur complement

\[
 \Sigma_i(\theta)
  =Q_{ii}+\theta g_i
   -Q_{iR}\{Q_{RR}+\theta D_{g_R}\}^{-1}Q_{Ri}.       \tag{2}
\]

Because `Q 1=0`,

\[
 Q_{RR}^{-1}Q_{Ri}=-\mathbf1_R,
 \qquad
 Q_{ii}-Q_{iR}Q_{RR}^{-1}Q_{Ri}=0.                    \tag{3}
\]

Differentiate (2) at zero.  With

\[
                         G_i=(-Q_{RR})^{-1}\geq0,
\]

one obtains

\[
\begin{aligned}
 \Sigma_i'(0)
 &=g_i+Q_{iR}Q_{RR}^{-1}D_{g_R}Q_{RR}^{-1}Q_{Ri}\\
 &=g_i+Q_{iR}G_ig_R.                                  \tag{4}
\end{aligned}
\]

The right side is exactly the singleton Schur/Kac reward

\[
 \boxed{\quad
 \Sigma_i'(0)=\psi_i
 =g_i+Q_{iR}G_ig_R
 =q_i\,\mathbb E_i\int_0^{\tau_i^+}g(X_t)\,dt.
 \quad}                                                \tag{5}
\]

Thus the directional-derivative idea is correct before state-space
compression.  It retains the killed occupation of every nonroot subset in
`G_i`.

## 3. What endpoint-action derivatives contain

For either endpoint action `J`, let `z_*` be its positive minimum and let
`H=D^2J(z_*)`, which is positive definite by the proved Picone
decomposition.  The ordinary root-source envelope

\[
               M_i(\eta)=\min_z\{J(z)-\eta z_i\}       \tag{6}
\]

has, locally at zero,

\[
 \boxed{
 M_i'(0)=-z_{*,i},\qquad
 M_i''(0)=-(H^{-1})_{ii}.}                             \tag{7}
\]

Indeed `DJ(z_eta)=eta e_i`, so `z_eta'=H^{-1}e_i`, and
the envelope theorem gives (7).  Likewise the hard-pin profile

\[
             A_i(\xi)=\min\{J(z):z_i=\xi\}             \tag{8}
\]

satisfies

\[
 A_i'(z_{*,i})=0,\qquad
 A_i''(z_{*,i})
   =H_{ii}-H_{iR}H_{RR}^{-1}H_{Ri}
   ={1\over(H^{-1})_{ii}}.                             \tag{9}
\]

These are vertex-branching endpoint and Hessian data.  Compare (5): the
Kac derivative instead contains the Green kernel of the full coalescing
subset chain.  No equality between (5) and (7)--(9) follows from global
minimality.

## 4. Exact regular-module obstruction

Take the loopless complete graph `K_s`, with

\[
 P_{ij}={1\over s-1}\quad(i\ne j),\qquad
 \pi_i={1\over s}.
\]

It has `a=t=1`.  The two branching endpoints are the same constant

\[
                         b_i=s_i=p_0={r-1\over r},       \tag{10}
\]

and the two endpoint actions coincide identically:

\[
 \boxed{
 J_B(z)=J_D(z)
 ={1\over rs}\sum_i\Phi(z_i)-{1\over2s}z^TPz.}        \tag{11}
\]

Therefore their unpinned minima, source envelopes (6), hard-pin profiles
(8), and all derivatives of those objects are identical.  At the active
point their common Hessian is

\[
                              H=rI-P.                  \tag{12}
\]

The exact stationary nonempty-subset laws give the per-root singleton
atoms and mean densities

\[
\begin{aligned}
 u_i&={r-1\over r^s-1},&
 \rho_B&={(r-1)r^{s-1}\over r^s-1},\\
 v_i&={(s-1)(r-1)\over s(r^{s-1}-1)},&
 \rho_D&={(s-1)(r-1)r^{s-2}\over s(r^{s-1}-1)}.
                                                               \tag{13}
\end{aligned}
\]

Writing `beta_U=rho_U-p_0` and using
`beta_B=u_i psi_B,i`, `beta_D=v_i psi_D,i` gives

\[
 \boxed{
 \psi_{B,i}={1\over r},\qquad
 \psi_{D,i}={s-r^{s-1}\over r(s-1)}.}                 \tag{14}
\]

Their difference is

\[
 \psi_{B,i}-\psi_{D,i}
 ={r^{s-1}-1\over r(s-1)}>0.                           \tag{15}
\]

The dB reward in (14) is positive exactly when `r^(s-1)<s`, zero at
equality, and negative when `r^(s-1)>s`.  Hence reciprocals may be used
only in the first regime.  The obstruction itself is an algebraic signed
reward statement and does not require positivity.

For a witness wholly inside the active range relevant here, take `s=2`.
Then (1) holds and both rewards are strictly positive throughout
`1<r<2`, in particular throughout
`3/2<=r<=151/100`.  Thus even where `(D-KAC)` is a genuine positive-factor
obligation, the identical pinned endpoint actions do not identify its two
different factors.

## 5. Consequence for the proof route

The endpoint global-minimum theorem is a theorem for the two linear
branching survival problems on vertex types.  The Kac residue (5) is a
first-order Feynman--Kac response of the recurrent coalescing process on
nonempty subsets.  Equation (11) shows that ordinary coordinate pinning of
the former cannot reconstruct the rule orientation retained by the latter.

A viable variational bridge would therefore have to introduce at least one
new ingredient, such as a full-subset source, a rule-specific coalescence
correction, or a proved comparison from the full Schur derivative (5) to an
endpoint-action quantity.  Merely applying the two global-minimum
inequalities to matched coordinate pins is circularly missing the desired
root residue.

## 6. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_kac_endpoint_action_pin_obstruction/verify_kac_endpoint_action_pin.py
```

The replay checks the generic Schur derivative, the endpoint
source/hard-pin Hessian algebra, the complete-graph reward simplifications,
and the active `K_2` stationary laws directly from their exact generators.
