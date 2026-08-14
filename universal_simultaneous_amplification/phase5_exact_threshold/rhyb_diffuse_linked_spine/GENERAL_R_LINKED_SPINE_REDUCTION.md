# A reversible-spine reduction of the scaled endpoint gap

Date: 2026-08-13 (America/Los_Angeles)

No graph search, kernel search, literature search, or external communication
was used.

## 1. Status

**EXACT FULL-STATE REDUCTION; THE SIGN REMAINS OPEN.**  The outstanding
scaled endpoint-versus-first inequality is

\[
 E_p s\leq E_p\mathcal F_r((r-1)q),\qquad
 \mathcal F_r(y)={rRy\over1+rRy}.                         \tag{1}
\]

This note rewrites its complete gap as a pairing on one reversible Doob
spine.  If `K` is the spine kernel, `m` its reversible measure, and `A,x`
are the two explicit endpoint labels defined below, then

\[
 \boxed{
 G:=E_p\{\mathcal F_r((r-1)q)-s\}
   =\langle A,K(x-1)\rangle_m
   =\langle KA,x-1\rangle_m.}                            \tag{2}
\]

Equivalently,

\[
 \boxed{
 G=\langle A,x-1\rangle_m
  -{1\over2}\sum_{i,j}m_iK_{ij}(A_i-A_j)(x_i-x_j).}      \tag{3}
\]

Thus the missing sign is not lost in a rank profile or a collection of
marginals: it is exactly one coupled cross-Dirichlet term on the full
fixed-point spine.  Formula (3) is a reduction, not a proof that `G>=0`.
Neither a universal ordering of `A` and `x` nor a compensating variational
bound is proved here.

There is also an exact obstruction to importing the special `r=2`
temperature-adjoint argument.  At general fitness the two orientations use
different residuals

\[
 d=(r-1)q-s,\qquad d^*=(r-1)h-b,                         \tag{4}
\]

and

\[
                         d-d^*=(r-2)(q-h).               \tag{5}
\]

They coincide automatically at `r=2`, but not at `R_hyb`.  A deterministic
reversible two-cycle gives negative quadratic energies in both orientations
throughout the rational interval containing `R_hyb`.  This refutes only an
attempt to regard those quadratic pairings as nonnegative Dirichlet
energies; it does not refute (1).

## 2. Endpoint setup and five grounds

Let `P` be a finite row-stochastic kernel self-adjoint in `L^2(pi)`.  Let
`a>0`, normalized by `E_pi a=1`, and put

\[
 p=\pi a,\qquad R=D_a^{-1}PD_a,\qquad t={Pa\over a}.      \tag{6}
\]

Suppose the positive Bd and dB endpoints obey

\[
 tb=rqPb,\qquad s=rhRs,\qquad q=1-b,\quad h=1-s.         \tag{7}
\]

Write

\[
 c=r-1,\qquad X=cq,\qquad
 h_1={1\over1+rRX},\qquad v=as,\qquad w=aX.             \tag{8}
\]

Then `F_r(X)=1-h_1`, and subtracting the two reciprocal fixed-point
equations gives

\[
 \mathcal F_r(X)-s=h-h_1=rhh_1R(X-s).                   \tag{9}
\]

The five positive grounds and their node potentials are

\[
\begin{array}{c|ccccc}
 f&1&a&b&v=as&w=aX\\ \hline
 V_f=(Pf)/f&1&t&t/(rq)&1/(rh)&RX/X=Rq/q.
\end{array}                                               \tag{10}
\]

Only the last two grounds are needed to build the spine, but the full
five-ground identities remain available for any subsequent Picone
comparison.

## 3. The fixed-point spine

Use the positive dB ground `v=as` to define

\[
 K_{ij}:={P_{ij}v_j\over V_{v,i}v_i}
        =rh_iR_{ij}{s_j\over s_i}.                       \tag{11}
\]

Because `V_vv=Pv`, `K` is row stochastic.  It is reversible for the
unnormalized positive measure

\[
 m_i:=\pi_iV_{v,i}v_i^2
     ={\pi_i a_i^2s_i^2\over rh_i}
     ={p_i a_i s_i^2\over rh_i},                         \tag{12}
\]

since

\[
 m_iK_{ij}=\pi_iP_{ij}v_iv_j
           =\pi_jP_{ji}v_jv_i=m_jK_{ji}.                 \tag{13}
\]

The ratio of the two endpoint grounds is

\[
                         x={w\over v}={X\over s}.         \tag{14}
\]

The Doob transform transports this ratio exactly:

\[
 (Kx)_i={V_{w,i}\over V_{v,i}}x_i.                       \tag{15}
\]

More importantly, if `y=x-1`, then

\[
 (Ky)_i={r h_i\over s_i}R(X-s)_i.                        \tag{16}
\]

Combining (9) and (16) yields the pointwise identity

\[
 \boxed{\quad \mathcal F_r(X)_i-s_i=s_i h_{1,i}(Ky)_i.\quad} \tag{17}
\]

This is the exact signed endpoint information missing from the unsigned
convex ratio Lyapunov: the first-orbit displacement is a one-step spine
average of the *signed* ground ratio `x-1`.

## 4. Exact variational form

Define the positive label

\[
 A_i:={p_i s_i h_{1,i}\over m_i}
     ={r h_i h_{1,i}\over a_i s_i}.                     \tag{18}
\]

Multiplying (17) by `p_i` and summing proves the first identity in (2).
Reversibility of `K` proves the second.  Finally, polarization gives

\[
 \langle A,(I-K)(x-1)\rangle_m
 ={1\over2}\sum_{i,j}m_iK_{ij}(A_i-A_j)(x_i-x_j),        \tag{19}
\]

and subtracting (19) from `\langle A,x-1\rangle_m` proves
(3).

The two pieces in (3) have concrete endpoint forms:

\[
 \langle A,x-1\rangle_m=E_p\{h_1(X-s)\},                \tag{20}
\]

while (19) is their exact reversible edge correction.  A proof of (1)
would follow from the sharp comparison

\[
 {1\over2}\sum_{i,j}m_iK_{ij}(A_i-A_j)(x_i-x_j)
 \leq E_p\{h_1(X-s)\}.                                  \tag{21}
\]

Equation (21), with the definitions (8), (11), (12), (14), and (18)
retained, is the full-state Green/Picone target exposed by this reduction.
Dropping those linkages turns it into a stronger statement with no known
reason to hold.

## 5. Why the `r=2` adjoint square does not persist

Define the temperature-adjoint system

\[
 p'=pt,\qquad P'=D_t^{-1}R,\qquad
 R'=D_t^{-1}P,\qquad t'={1\over t}.                      \tag{22}
\]

The endpoint roles swap: `b'=s` and `s'=b`.  The original scaled input is
`X=cq`.  The transformed scaled input is `X'=ch`, and its first extinction
iterate is

\[
                         q_1={t\over t+rcPh}.             \tag{23}
\]

With the residuals (4), the two exact resolvent identities are

\[
 h-h_1=rhh_1Rd,\qquad
 q-q_1={rqq_1\over t}Pd^*.                               \tag{24}
\]

Consequently the orientation energies are

\[
 E_p\!\left[{d(h-h_1)\over rhh_1}\right]
     =E_p(dPd),                                          \tag{25}
\]

\[
 E_{p'}\!\left[{d^*(q-q_1)\over rqq_1}\right]
     =E_p(d^*Pd^*).                                      \tag{26}
\]

At `r=2`, (5) makes these the same residual and hence the same quadratic
pairing.  At a general fitness the common-energy step is unavailable.  In
particular, adding or comparing (25)--(26) cannot silently replace `d^*`
by `d`.

These pairings also have no automatic positive sign.  On the deterministic
two-cycle

\[
 P=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad
 p={1\over1+\kappa}(1,\kappa),                            \tag{27}
\]

take `kappa=1/4`.  Direct endpoint substitution gives the same value in
the two orientations:

\[
 E_p(dPd)=E_p(d^*Pd^*)
 =-{9(r-1)^2(r^2-r-5)(4r^2-4r-5)
       \over r^2(r+4)^2(4r+1)^2}.                        \tag{28}
\]

Both quadratic factors in the numerator are negative for
`3/2<=r<=151/100`, so (28) is strictly negative throughout that interval.
At `r=3/2` its value is `-34/5929`.  This is a conceptual obstruction to a
positive-energy interpretation, not a counterexample to the endpoint gap;
indeed the endpoint gap is positive on every deterministic two-cycle by the
separate exact two-cycle theorem.

## 6. What remains

The universal inequality (1), and hence the lower half of the diffuse
support sandwich at `R_hyb`, remains **OPEN**.  The next proof-first target
is not another finite-rank or marginal inequality.  It is a direct
two-root Green/Schur comparison that controls the orientation-sensitive
edge term in (3), ideally while retaining the positive square lost when
the two temperature-adjoint residuals in (4) are identified.

## 7. Exact replay

From the repository root run

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
rhyb_diffuse_linked_spine/verify_linked_spine.py
```
