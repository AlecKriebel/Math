# Negative diffuse ground energy with positive endpoint support

Date: 2026-08-13 (America/Los_Angeles)

No graph search, kernel scan, literature search, or external communication
was used.

## 1. Status

**EXACT THEOREM-LEVEL OBSTRUCTION.**  The proposed stronger route

\[
                         K_{R_{\rm hyb}}\geq0             \tag{1}
\]

for every finite undirected-realizable diffuse adjoint kernel is false.
There is an explicit positive symmetric three-type family for which

\[
 \lim_{\eta\downarrow0}K_{R_{\rm hyb}}(\eta)<0,\qquad
 \lim_{\eta\downarrow0}T_{R_{\rm hyb}}(\eta)>0.          \tag{2}
\]

Thus the exact identity

\[
 T_r={r(r-1)\over4}K_r
 +{r\over r-1}E_p\!\left[
 h\left\{{u\over h}-{r-1\over2}
          \left(Px-{x\over h}\right)\right\}^{\!2}\right] \tag{3}
\]

cannot be closed by proving the first term nonnegative.  The square in (3)
is not merely a remainder: it strictly repays a negative ground energy on
this family.

This result does **not** refute the desired support inequality `T_Rhyb>=0`.
It refutes the natural scalar/convex strengthening isolated in
`R_DEPENDENT_DIFFUSE_SUPPORT_IDENTITY.md` and in the root-to-diffuse
reduction.  In accordance with the proof-first stopping rule, no graph or
kernel search follows.  Any successful variational or Picone proof of
`T_Rhyb>=0` must retain the coupled square, or an algebraically equivalent
multi-ground compensation.

## 2. Positive symmetric three-type family

Fix

\[
 0<\gamma<1,\qquad 0<\theta<1,
 \qquad 0<\eta<1-\gamma,
\]

and put `A_eta=1-gamma-eta`.  Let the physical type law and symmetric
weight matrix be

\[
 p^{(\eta)}=(A_\eta,\eta,\gamma),\qquad
 W^{(\eta)}=
 \begin{pmatrix}
 \eta&(1-\theta)/\eta&\theta/\gamma\\
 (1-\theta)/\eta&1&1\\
 \theta/\gamma&1&1/\eta
 \end{pmatrix}.                                          \tag{4}
\]

All entries of `p` and `W` are positive.  Define

\[
 \delta_i=\sum_jp_jW_{ij},\qquad
 P_{ij}={p_jW_{ij}\over\delta_i},\qquad
 R=D_p^{-1}P^TD_p,qquad t=R\mathbf1.                    \tag{5}
\]

Then `P` is row stochastic and is self-adjoint in

\[
 \pi_i={p_i\delta_i\over Z},\qquad
 Z=\sum_ip_i\delta_i.
\]

With `a_i=Z/delta_i`, one has

\[
 E_\pi a=1,qquad \pi_i a_i=p_i,qquad
 R=D_a^{-1}PD_a.                                         \tag{6}
\]

Thus (4)--(6) are exactly inside the reversible diffuse-adjoint class of
(3), with physical averaging measure `p`.

Let `b,s` be the positive endpoint survival vectors at fitness `r>1`:

\[
 t b=r(1-b)Pb,qquad s=r(1-s)Rs.                         \tag{7}
\]

Write

\[
 q=1-b,\quad h=1-s,\quad p_0={r-1\over r},
 \quad x=b-p_0,\quad u=s-p_0.                            \tag{8}
\]

The quantities in (2) are exactly

\[
 K_r={4\over r-1}E_p\!\left[{t x^2\over q}\right]
       -E_p\!\left[h\left(Px-{x\over h}\right)^2\right], \tag{9}
\]

\[
 T_r=(r-1)E_pq-E_ps.                                    \tag{10}
\]

## 3. Singular endpoint limit

Put

\[
 A=1-\gamma,qquad
 \mathcal T=1+{A\theta\over\gamma},qquad c=r-1,        \tag{11}
\]

and assume

\[
                         \mathcal T<r.                   \tag{12}
\]

The exact type degrees are

\[
\begin{aligned}
 \delta_A&=1+A_\eta\eta,\\
 \delta_B&={A_\eta(1-\theta)\over\eta}+\eta+\gamma,\\
 \delta_C&={A_\eta\theta\over\gamma}+\eta+{\gamma\over\eta}.
                                                               \tag{13}
\end{aligned}
\]

Consequently

\[
 P\longrightarrow
 \begin{pmatrix}
 0&1-\theta&\theta\\
 1&0&0\\
 0&0&1
 \end{pmatrix},                                          \tag{14}
\]

and

\[
 {t_A\over\eta}\longrightarrow
 L:=A+{1\over A}+{\theta\over\gamma},qquad
 \eta t_B\longrightarrow A(1-\theta),qquad
 t_C\longrightarrow\mathcal T.                         \tag{15}
\]

The subunit Bd extinction branch has

\[
 q_A\longrightarrow0,qquad q_B\longrightarrow1,qquad
 q_C\longrightarrow{\mathcal T\over r}.                \tag{16}
\]

The first equation in (7), equivalently

\[
 q_i={t_i\over t_i+r\{1-(Pq)_i\}},                       \tag{17}
\]

then gives the only singular ratio needed below:

\[
 {q_A\over\eta}\longrightarrow
 {L\over\theta(r-\mathcal T)}.                          \tag{18}
\]

For the dB branch,

\[
 h_A\longrightarrow1,qquad h_C\longrightarrow{1\over r}, \tag{19}
\]

while `h_B` converges to an interior value in `(0,1)`.  These limits follow
directly from (7); the `B` equation has an isolated subunit root, and its
exact value is immaterial because `p_B=eta`.

For completeness, (16)--(19) are stable limits rather than a selection of
formal algebraic roots.  The positive kernel has a unique subunit extinction
fixed point.  The limiting `C` equation has the isolated subunit root

\[
                         q_C={\mathcal T\over r}
\]

under (12), the `B` equation forces `q_B->1`, and then (17) forces (18).
The same monotone fixed-point argument gives (19).  Hence the limits
pass through every term of (9), including the apparently singular ratio
`t_A/q_A`.

## 4. Exact limit of the ground energy

From (16), the centered Bd labels converge to

\[
 x_A\to{1\over r},\qquad
 x_B\to-{c\over r},\qquad
 x_C\to{1-\mathcal T\over r}
             =-{A\theta\over\gamma r}.                 \tag{20}
\]

Equations (15), (18), and (20) give

\[
\begin{aligned}
 \lim_{\eta\downarrow0}E_p\!\left[{t x^2\over q}\right]
  ={}&{A\theta(r-\mathcal T)\over r^2}
      +{A(1-\theta)c^2\over r^2}
      +{A^2\theta^2\over\gamma r}.                     \tag{21}
\end{aligned}
\]

The three terms are respectively the `A`, `B`, and `C` type
contributions.  In particular, the vanishing mass of type `B` is exactly
repaid by its diverging temperature.

For the second term of (9), (14), (19), and (20) give

\[
 \left(Px-{x\over h}\right)_A
 \longrightarrow
 -{1+c(1-\theta)+A\theta^2/\gamma\over r},              \tag{22}
\]

\[
 \left(Px-{x\over h}\right)_C
 \longrightarrow{cA\theta\over\gamma r}.               \tag{23}
\]

The `B` label remains bounded and its `p_B`-weighted contribution vanishes.
Therefore

\[
\begin{aligned}
 \lim_{\eta\downarrow0}E_p\!\left[
 h\left(Px-{x\over h}\right)^2\right]
 ={}&{A\over r^2}
   \left\{1+c(1-\theta)+{A\theta^2\over\gamma}\right\}^{\!2}\\
 &+{c^2A^2\theta^2\over\gamma r^3}.                    \tag{24}
\end{aligned}
\]

Combining (9), (21), and (24) proves the closed formula

\[
\boxed{
\begin{aligned}
 K_r^{\rm lim}
 ={}&{4\over c}\left{
 {A\theta(r-\mathcal T)\over r^2}
 +{A(1-\theta)c^2\over r^2}
 +{A^2\theta^2\over\gamma r}\right}\\
 &-{A\over r^2}
   \left\{1+c(1-\theta)+{A\theta^2\over\gamma}\right\}^{\!2}
 -{c^2A^2\theta^2\over\gamma r^3}.
                                                               \tag{25}
\end{aligned}}
\]

## 5. Exact negative certificate at the hybrid endpoint

Take the rational parameters

\[
                         \gamma={1\over14},\qquad
                         \theta={1\over50}.               \tag{26}
\]

Then

\[
 A={13\over14},qquad \mathcal T={63\over50}<{3\over2}<R_{\rm hyb}. \tag{27}
\]

Exact simplification of (25) gives

\[
 \boxed{
 K_r^{\rm lim}
 =-{13\,Q(r)\over87{,}500{,}000\,r^3},}                 \tag{28}
\]

where

\[
 Q(r)=6{,}002{,}500r^3-24{,}158{,}800r^2
          +23{,}808{,}969r+32{,}500.                    \tag{29}
\]

On the whole rational interval `3/2<=r<=151/100`,

\[
 Q''(r)=36{,}015{,}000r-48{,}317{,}600>0,               \tag{30}
\]

\[
 Q'(151/100)=-{32{,}366{,}825\over4}<0,                 \tag{31}
\]

so `Q` is decreasing there, while

\[
                         Q(151/100)={25{,}054{,}027\over16}>0. \tag{32}
\]

Thus `Q(r)>0` throughout the interval.  The hybrid sextic

\[
 P_{\rm hyb}(r)=r^6-8r^5+22r^4-30r^3+21r^2-6r+1       \tag{33}
\]

has its unique root `R_hyb` in that interval.  Equations (28)--(32)
therefore prove

\[
                         \boxed{K_{R_{\rm hyb}}^{\rm lim}<0.} \tag{34}
\]

By convergence, every sufficiently small positive `eta` gives a finite
positive symmetric kernel with `K_Rhyb(eta)<0`.  This is an interior finite
counterexample to (1), obtained from an exact singular-limit theorem rather
than a kernel search.

## 6. The full support remains positive

The endpoint averages of this family have the already isolated limits

\[
 E_pb\longrightarrow1-{\gamma+A\theta\over r},qquad
 E_ps\longrightarrow{\gamma(r-1)\over r}.               \tag{35}
\]

Substitution in (10) gives

\[
 \boxed{
 T_r^{\rm lim}={A\theta(r-1)\over r}>0.}                \tag{36}
\]

For (26), this is

\[
                         T_r^{\rm lim}={13(r-1)\over700r}>0. \tag{37}
\]

Hence at `r=R_hyb`, (3) necessarily has a strictly positive square large
enough to compensate the negative contribution
`r(r-1)K_r/4`.  The pair quadratic's special double-root identity, encoded
by the hybrid sextic, does not rescue the scalar ground-energy sign: (34)
holds on the entire interval containing the sextic root.  Any use of that
double root in a diffuse support proof must act on the *combined* expression
(3), not on `K_r` alone.

## 7. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_diffuse_ground_energy_obstruction/verify_negative_ground_energy.py
```

The replay uses exact symbolic arithmetic.  It derives (25), specializes
and factors (28), verifies the rational derivative signs (30)--(32), counts
one sextic root in `(3/2,151/100)`, and checks the positive support formula
(36).
