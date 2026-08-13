# Complete four-ground Picone reduction for the factor-one boundary

Date: 2026-08-13 (America/Los_Angeles)

## Status

This note proves an exact reduction of the unresolved endpoint inequality

\[
                         \beta+\sigma\leq 1.                 \tag{1}
\]

The reduction is not itself a proof of (1).  It isolates one finite ordered
label lemma whose proof would establish (1), and gives an exact Farkas-dual
criterion for either proving that lemma or refuting this proof route.  In
particular, no search over kernels is needed: the remaining certificate
problem depends only on the six ordered ratios of four positive grounds.

## 1. Four positive ground states

Let `P` be a finite row-stochastic nonnegative kernel self-adjoint in
`<.,.>_pi`, and let `a,b,s` be positive vectors with `0<b,s<1`.  Put

\[
 q=1-b,\qquad h=1-s,\qquad v=as,\qquad t={Pa\over a}.          \tag{2}
\]

The Bd and dB endpoint equations at fitness two are

\[
 (Pa)b=2aq(Pb),\qquad v=2hPv.                                \tag{3}
\]

Thus `a,b,v` are three positive ground states of the same self-adjoint
kernel, with node potentials

\[
 V_a={Pa\over a}=t,\qquad
 V_b={Pb\over b}={t\over2q},\qquad
 V_v={Pv\over v}={1\over2h}.                                \tag{4}
\]

There is also a fourth positive ground which should not be discarded:
row-stochasticity gives

\[
                         f_0=1,\qquad V_0=1.                 \tag{4a}
\]

The target gap is

\[
 \Delta=1-\beta-\sigma
       =\langle 1,a(q-s)\rangle_\pi.                         \tag{5}
\]

Consequently it is enough to prove
`sum_i pi_i d_i >= 0`, where

\[
                         d_i=a_i(q_i-s_i).                    \tag{6}
\]

## 2. Cut-Picone identity

For any two positive vectors `f,g`, define

\[
 r_i={g_i\over f_i},\qquad
 c_i^{fg}=f_i g_i\left({(Pg)_i\over g_i}-{(Pf)_i\over f_i}\right).
                                                                    \tag{7}
\]

If `C_ij=pi_i P_ij=C_ji`, then every increasing function `psi` on the
finite ratio set satisfies the exact Picone identity

\[
 \sum_i\pi_i c_i^{fg}\psi(r_i)
 =-{1\over2}\sum_{i,j}C_{ij}f_if_j
        (r_i-r_j)(\psi(r_i)-\psi(r_j))\leq0.                 \tag{8}
\]

There is an equivalent cut form.  For every real `z`,

\[
 \sum_{i:r_i\leq z}\pi_i c_i^{fg}
 =\sum_{\substack{i:r_i\leq z\\j:r_j>z}}
      C_{ij}f_if_j(r_j-r_i)\geq0,                            \tag{9}
\]

and the full sum is zero.  Formula (9) follows by cancelling the internal
edges of the lower level set.  Conversely, summation by parts turns (9)
back into (8).  This cut identity is useful because it contains no
undetermined test function.

Apply (7) to the three pairs `(a,b)`, `(a,v)`, `(b,v)` and write

\[
\begin{array}{lll}
 r^{(1)}=b/a, & c^{(1)}=ab(V_b-V_a),\\
 r^{(2)}=s,   & c^{(2)}=av(V_v-V_a),\\
 r^{(3)}=as/b,& c^{(3)}=bv(V_v-V_b).
\end{array}                                                   \tag{10}
\]

These data are not independent.  Pointwise,

\[
 r^{(3)}={r^{(2)}\over r^{(1)}},\qquad
 c^{(3)}={b\over a}c^{(2)}-s c^{(1)}.                       \tag{11}
\]

The constant ground (4a) supplies three additional signed ratio orders:

\[
\begin{array}{lll}
 r^{(0a)}=a, & c^{(0a)}=a(t-1)=Pa-a,\\
 r^{(0b)}=b, & c^{(0b)}=b(V_b-1)=Pb-b,\\
 r^{(0v)}=v, & c^{(0v)}=v(V_v-1)=Pv-v.
\end{array}                                                   \tag{11a}
\]

Together, (10) and (11a) are the complete six-pair Picone data of the four
known grounds `{1,a,b,v}`.  Each obeys (8)-(9).  The three extra orders are
genuinely available in the physical normal form and strengthen the
certificate below.

## 3. Finite coupled-label certificate

**Certificate theorem.**  Suppose there are increasing functions
`psi_1,psi_2,psi_3`, each required only on its finite ratio set, such that

\[
 d_i+\sum_{k=1}^3c_i^{(k)}\psi_k(r_i^{(k)})\geq0
 \quad\hbox{for every }i.                                   \tag{12}
\]

Then `Delta>=0`, and hence (1) holds.

Indeed, multiply (12) by `pi_i` and sum.  Each of the three correction
terms has nonpositive sum by (8), so

\[
 \Delta=\sum_i\pi_i d_i
 \geq-\sum_{k=1}^3\sum_i\pi_i
      c_i^{(k)}\psi_k(r_i^{(k)})\geq0.                       \tag{13}
\]

This is a finite linear feasibility problem after the three ratio sets are
ordered.  Equal ratios must receive equal label values; consecutive
distinct levels carry the monotonicity inequalities.

More strongly, one may add an independent increasing label potential for
each of the three pairs in (11a), with its signed correction in (12).  The
same one-line proof gives (13).  This **complete four-ground certificate** is
at least as powerful as the displayed three-ground certificate and
is the strongest certificate obtainable by summing the pairwise Picone
inequalities of the four currently known grounds.

The use of all three pairs is essential to this route as presently known.
The corresponding one-pair statement is false on physically realizable
dense kernels, so no proof may silently discard the coupling in (11).

## 4. Exact theorem of alternatives

The certificate has a compact dual formulation.  Fix either the three pairs
in (10), or all six pairs in (10) and (11a), and call the selected pair set
`E`.  For a nonnegative vector `lambda`, define, for each `k in E`,

\[
 S_k(z)=\sum_{i:r_i^{(k)}\leq z}\lambda_i c_i^{(k)}.          \tag{14}
\]

**Farkas alternative.**  Exactly one of the following holds:

1. increasing label potentials satisfying (12) exist;
2. there is a vector `lambda>=0` such that

   \[
   \sum_i\lambda_i c_i^{(k)}=0,\qquad
   S_k(z)\geq0\quad\hbox{for every proper ratio cut and every }k\in E,
                                                                    \tag{15}
   \]

   but

   \[
                          \sum_i\lambda_i d_i<0.              \tag{16}
   \]

To see this, introduce one variable for each distinct level of each ratio
and impose consecutive inequalities `psi(level_m)<=psi(level_{m+1})`.
Farkas' lemma associates `lambda_i>=0` to the node inequalities (12) and a
nonnegative flow to every consecutive order edge.  Eliminating those flows
gives (15): their values are precisely the lower-prefix sums in (14).
The remaining strict dual inequality is (16).  This also proves the
converse by reconstructing each order-edge flow from the prefix sums.

For the physical measure `lambda=pi`, conditions (15) hold automatically
by the cut-Picone formula (9).  Taking `E` to be all six pairs gives the
strongest exact remaining label lemma currently exposed by this method:

> For the linked data (6), (10), (11), and (11a) arising from the two
> endpoint equations, every nonnegative `lambda` obeying all six
> simultaneous cut orders (15) has `sum_i lambda_i d_i>=0`.

A proof of this ordered four-ground lemma proves (1) through (12)-(13).
A finite exact violation of it refutes the entire coupled label-potential
route, even if (1) itself remains true.  This distinction prevents further
floating feasibility screens from being mistaken for evidence about the
endpoint theorem.

## 5. Consequence for the catalyst program

If (1) is proved, every exact diffuse adjoint branching trace at fitness two
satisfies

\[
  {1\over2}-\sigma\geq\beta-{1\over2}.                       \tag{17}
\]

Hence no construction whose limiting trace is fully described by this
diffuse finite-type normal form can have positive Bd response with
little-oh dB cost.  Any lower construction approaching every fixed
`r<2` would then have to retain a non-diffuse mechanism in the limit—for
example same-scale collisions or another interaction that is lost in the
independent branching reduction.  This implication is conditional on the
factor-one theorem; the present note establishes the exact proof bottleneck,
not that theorem.
