# The scaled orbit: a convex Lyapunov and an exact two-cycle obstruction

Date: 2026-08-13 (America/Los_Angeles)

## Status

**PROVED THEOREM AND STRUCTURAL OBSTRUCTION.**  Every finite reversible
adjoint dB survival map has a family of nonincreasing convex ratio
Lyapunov functionals relative to its positive fixed point.  These
functionals are unsigned: they measure distance from the fixed point but do
not determine on which side its ordinary average lies.

That distinction is necessary already on the deterministic reversible
two-cycle.  For every imbalanced two-cycle and every

\[
                         {3\over2}\le r\le {151\over100},
\]

the genuine scaled Bd-started orbit satisfies

\[
 E_p y_1<E_p y_2,
 \qquad y_0=(r-1)q,quad y_{j+1}=\mathcal F_r(y_j).       \tag{1}
\]

Thus the raw averaged orbit is not nonincreasing even in the exact fitness
band containing `R_hyb`; its failure occurs immediately after the first
step, without a kernel search.  On the same entire class one nevertheless
has

\[
                         E_p y_1>E_p s,                  \tag{2}
\]

so the desired endpoint-versus-first inequality survives this sharp
period-two test.

This note does **not** prove (2) for general reversible adjoint data.  The
global endpoint gap remains open.

## 1. A universal convex ratio Lyapunov

Let `R` be irreducible and reversible with respect to a positive measure
`m`, and let

\[
 \mathcal F_r(y)_i={r(Ry)_i\over1+r(Ry)_i},
 \qquad \mathcal F_r(s)=s,qquad 0<s_i<1.               \tag{3}
\]

For the diffuse-adjoint parametrization

\[
 R=D_a^{-1}PD_a,qquad p=\pi a,
\]

where `P` is reversible under `pi`, one may take

\[
                         m_i=\pi_i a_i^2=p_i a_i.        \tag{4}
\]

Put `h=1-s` and define the fixed-point Doob kernel and its reversible
measure by

\[
 K_{ij}={R_{ij}s_j\over(Rs)_i},
 \qquad
 \nu_i=m_i s_i(Rs)_i={m_i s_i^2\over r h_i}.            \tag{5}
\]

The kernel is row stochastic.  Detailed balance for `R` gives

\[
 \nu_iK_{ij}=m_iR_{ij}s_is_j
             =m_jR_{ji}s_js_i=\nu_jK_{ji},              \tag{6}
\]

so `nu` is invariant for `K`.

For any positive vector `y`, write

\[
 z_i={y_i\over s_i},qquad u_i=(Kz)_i.
\]

The fixed-point equation in (3) gives the exact ratio evolution

\[
 {\mathcal F_r(y)_i\over s_i}
       ={u_i\over h_i+s_i u_i}.                         \tag{7}
\]

The scalar on the right lies on the closed segment joining `u_i` to one:

\[
 {u\over h_i+s_i u}
 =u+{s_i u\over h_i+s_i u}(1-u).                        \tag{8}
\]

Let `psi:[0,infinity)->R` be convex and minimized at one.  Convexity along
the segment (8), followed by Jensen for `K`, yields

\[
 \psi\!\left({u_i\over h_i+s_i u_i}\right)
 \le\psi(u_i)
 \le\sum_jK_{ij}\psi(z_j).                             \tag{9}
\]

Summing against the invariant measure proves the Lyapunov theorem

\[
 \boxed{
 \sum_i\nu_i\psi\!\left({\mathcal F_r(y)_i\over s_i}\right)
 \le
 \sum_i\nu_i\psi\!\left({y_i\over s_i}\right).}       \tag{10}
\]

This holds for every `r>1`, not merely near `R_hyb`.  Examples include
the quadratic ratio deviation and the two one-sided hinge losses
`(z-1)_+` and `(1-z)_+`.

The minimum condition in (10) is exactly why this theorem cannot by itself
prove a signed average comparison.  Both excess and deficit are charged
nonnegatively.  Moreover the natural invariant weight
`nu_i=m_i s_i^2/(r h_i)` is not the target weight `p_i s_i` which would
turn a ratio average into `E_p(y-s)`.

## 2. Exact orbit identity

Every orbit point also satisfies a useful scalar identity.  If
`y^+=F_r(y)`, then

\[
 Ry={y^+\over r(1-y^+)},
\]

and adjointness gives `E_pRy=E_py`.  Hence

\[
 \boxed{
 E_p(y-y^+)
 ={1\over r}E_p\!\left[
       {y^+\{r y^+-(r-1)\}\over1-y^+}
                      \right].}                         \tag{11}
\]

The scalar integrand in (11) is strictly convex, since its second
derivative is

\[
                         {2\over r(1-z)^3}>0.            \tag{12}
\]

It changes sign at `(r-1)/r`.  Thus (11) is an exact one-step identity, but
not a termwise Lyapunov sign.  The two-cycle below shows that its average
can alternate even for the special scaled Bd-started orbit.

## 3. Deterministic reversible two-cycle

Take

\[
 p={1\over1+\kappa}(1,\kappa),\qquad
 P=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 R=\begin{pmatrix}0&\kappa\\1/\kappa&0\end{pmatrix},   \tag{13}
\]

where `kappa>0`.  This is the reversible two-type quotient obtained from
the ground ratio `a_2/a_1=kappa`.  The Bd extinction vector and dB survival
fixed point are

\[
 q_1={\kappa r+1\over r(\kappa+r)},\qquad
 q_2={\kappa+r\over r(\kappa r+1)},                     \tag{14}
\]

\[
 s_1=1-q_2={\kappa(r^2-1)\over r(\kappa r+1)},\qquad
 s_2=1-q_1={r^2-1\over r(\kappa+r)}.                    \tag{15}
\]

Put `c=r-1`, `y_0=cq`, and iterate (3).  The first two images are

\[
 (y_1)_1={\kappa(\kappa+r)c\over
                 \kappa^2r-\kappa^2+\kappa r^2+1},
 \qquad
 (y_1)_2={c(\kappa r+1)\over
                 \kappa^2+\kappa r^2+r-1},             \tag{16}
\]

\[
 (y_2)_1={\kappa r c(\kappa r+1)\over
  \kappa^2r^3-\kappa^2r^2+\kappa^2+2\kappa r^2-\kappa r+r-1},
                                                                    \tag{17a}
\]

\[
 (y_2)_2={r c(\kappa+r)\over
  \kappa^2r-\kappa^2+2\kappa r^2-\kappa r+r^3-r^2+1}.  \tag{17b}
\]

All displayed denominators are positive for `r>1`, `kappa>0`.

## 4. The desired gap is positive on every two-cycle

Write

\[
 U=\kappa+{1\over\kappa}\ge2,
\]

\[
 A_0(r)=r^4-2r^3+r+1,qquad
 B_0(r)=r^5-r^4-3r^2+3r+2,                             \tag{18}
\]

and

\[
 D_1=\kappa^2+\kappa r^2+r-1,qquad
 D_2=\kappa^2(r-1)+\kappa r^2+1.                       \tag{19}
\]

Exact reduction gives

\[
 \boxed{
 E_p(y_1-s)=
 {\kappa^2(\kappa-1)^2(r-1)
       \{A_0(r)U+B_0(r)\}
  \over
  r(\kappa+r)(\kappa r+1)D_1D_2}.}                    \tag{20}
\]

For `r>=3/2`, expansion at `r=3/2+v` gives

\[
 A_0={13\over16}+v+{9\over2}v^2+4v^3+v^4>0,           \tag{21}
\]

while

\[
 2A_0+B_0=(r+1)^2(r^3-r^2-3r+4)
 ={125\over32}+{125\over16}v+{105\over4}v^2
   +{49\over2}v^3+{17\over2}v^4+v^5>0.               \tag{22}
\]

Since `U>=2`, (21)--(22) prove (2), strictly when `kappa!=1`, throughout
the requested interval and in fact for every `r>=3/2`.

At `r=2`, (20) reduces to the previously stored boundary check

\[
 {3\kappa(\kappa-1)^2\over
  2(\kappa+2)(2\kappa+1)(\kappa^2+4\kappa+1)}.
\]

## 5. The raw average immediately reverses direction

Define

\[
\begin{aligned}
 A(r)&=r^4-2r^3+r-1,\\
 B(r)&=r(2r^4-2r^3-4r-1),\\
 C(r)&=r^6+3r^4-6r^3-4r^2-4r+2,\\
 H_r(U)&=A(r)U^2+B(r)U+C(r)-2A(r).                    \tag{23}
\end{aligned}
\]

Also put

\[
\begin{aligned}
 D_3&=\kappa^2(r-1)+\kappa r(2r-1)+r^2(r-1)+1,\\
 D_4&=\kappa^2\{r^2(r-1)+1\}+\kappa r(2r-1)+(r-1).
                                                                    \tag{24}
\end{aligned}
\]

Then exact simplification gives

\[
 \boxed{
 E_p(y_2-y_1)=
 {-\kappa^3(\kappa-1)^2(r-1)^3 H_r(U)
  \over D_1D_2D_3D_4}.}                                \tag{25}
\]

It remains only to check `H_r(U)<0`.  On
`3/2<=r<=151/100`, all three polynomials

\[
 A(r),\qquad \partial_UH_r(2)=4A(r)+B(r),\qquad H_r(2) \tag{26}
\]

are strictly negative.  An elementary exact check is obtained by putting
`v=r-3/2 in [0,1/100]`: each polynomial has a negative constant term and
strictly positive remaining coefficients, hence is increasing, while its
value at `v=1/100` is respectively

\[
 -{117704599\over10^8},\qquad
 -{50178754149\over5\,10^9},\qquad
 -{19376852101199\over10^{12}}.                        \tag{27}
\]

Because `A<0`, the derivative `2AU+B` decreases with `U`.  Equations
(26)--(27) therefore imply

\[
 H_r(U)\le H_r(2)<0\qquad(U\ge2).                       \tag{28}
\]

Every factor outside `-H_r(U)` in (25) is positive when `kappa!=1`.
This proves the strict raw-average reversal (1).

For example, at the entirely rational point `r=3/2`, `kappa=2`,

\[
 E_p(y_0-y_1)={67\over3780}>0,qquad
 E_p(y_2-y_1)={1\over405}>0,                            \tag{29}
\]

while

\[
                         E_p(y_1-s)={23\over3780}>0.     \tag{30}
\]

The scaled orbit therefore has an immediate sawtooth in its raw average,
even though its first iterate remains above the fixed-point average.

## 6. Consequence for the proof route

The ratio Lyapunov (10) is a genuine contraction theorem, and the
two-cycle obstruction (25) shows why it cannot simply be replaced by the
ordinary average.  A general proof of

\[
                    E_p\mathcal F_r((r-1)q)\ge E_ps     \tag{31}
\]

must retain signed endpoint information beyond convex distance to `s`--for
example, the coupled ground orders in the existing five-ground reduction.
Iterating the first-step average inequality, even at `R_hyb`, is not a
valid route.

## 7. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_scaled_orbit_lyapunov/verify_scaled_orbit_lyapunov.py
```

The replay reconstructs the endpoint vectors and orbit images, derives
(20) and (25), and verifies every rational interval sign exactly.
