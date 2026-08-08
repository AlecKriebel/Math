# Heterogeneous dense pair protection cannot improve dB establishment

Date: 2026-08-08 (America/Los_Angeles)

## Status and scope

This note closes the arbitrary-strength version of the dense pair relay.
Take a density-one population of disjoint partner pairs, put a complete
inter-pair background on the dense degree scale, and allow the normalized
partner strengths to have any limiting probability law.  Every discordant
pair, repaired pair, and externally produced child is retained in the exact
rare-colony process.

For every fixed fitness `r>1`, its uniformly averaged dB establishment
probability `S` satisfies

\[
                         \boxed{S\le p:=1-{1\over r}}.       \tag{1}
\]

Equality is possible only when the partner strength is zero almost surely.
Thus heterogeneous protection does not provide the positive-density relay
needed by the diagonal-to-two construction.  This is an establishment
theorem for the rare-colony limit, not a universal finite-graph fixation
theorem.  In particular, it does not cover nonregular external networks,
larger interacting cells, or a hierarchy in which colonies cease to be
rare before the local trace resolves.

## 1. Exact heterogeneous pair trace

Let `z>=0` be the normalized partner strength of a uniformly chosen pair
vertex and write

\[
 x={1\over1+z}\in(0,1],\qquad H=E x.             \tag{2}
\]

The result remains valid for weak limits that put mass at `x=0`.  Let `q_1`
and `q_2` be the extinction probabilities from a singleton and a doubleton
in a pair of type `x`.  External children have type law `x/H`.  Put

\[
 T=1-{E[xq_1]\over H},\qquad A=rHT.              \tag{3}
\]

A singleton dies at rate one, repairs its partner at rate

\[
 g_z={rz\over1+rz},                               \tag{4}
\]

and emits external children at rate `rH`.  A doubleton shrinks at rate
`2/(1+rz)` and emits children at rate `2rH`.  Direct first-event conditioning
therefore gives

\[
 {q_2\over q_1}={1\over1+A(1+rz)},\qquad
 q_1={1\over1+g_z+A-g_zq_2/q_1}.                 \tag{5}
\]

No independence between the two vertices of a pair is used in (5).

Set

\[
 t=1+rz={r-(r-1)x\over x},\quad
 B=A(A+2),\quad C=A(A+1),\quad
 y=r-(r-1)x,\quad D=x+By.                        \tag{6}
\]

The singleton survival `s=1-q_1` and its child-law-weighted contribution
`g=xs` are exactly

\[
 s_A(x)={C y\over D},\qquad
 g_A(x)={Cxy\over D}.                            \tag{7}
\]

The consistency equation (3) is simply

\[
                         E g_A(x)={A\over r}.     \tag{8}
\]

The desired uniform establishment probability is `S=E s_A(x)`.

## 2. The self-consistent parameter cannot exceed `r-1`

For a positive solution divide (8) by `A` and put

\[
 h_A(x)={g_A(x)\over A}
 ={(A+1)xy\over x+A(A+2)y}.                      \tag{9}
\]

At fixed `x`, direct differentiation gives

\[
 {\partial h_A\over\partial A}
 ={xy\{x-(A^2+2A+2)y\}\over
       \{x+A(A+2)y\}^2}<0,                       \tag{10}
\]

because `y>=x`.  At `A=r-1`, putting `q=1-x` gives the pointwise identity

\[
 h_{r-1}(x)-{1\over r}
 =-{q(r-1)(qr+1)\over x+(r^2-1)y}\le0.           \tag{11}
\]

Since (8) says `E h_A=1/r`, (10)--(11) imply

\[
                              0<A\le r-1.        \tag{12}
\]

If `A=r-1`, equality in (11) forces `x=1` almost surely.

## 3. Concave response envelope

The two response coordinates in (7) obey

\[
 s_A'(x)=-{Cr\over D^2}<0,                       \tag{13}
\]

\[
 g_A'(x)={CJ\over D^2},\qquad
 J=By^2-(r-1)x^2,qquad
 J'=-2(r-1)D<0.                                  \tag{14}
\]

Thus `g_A` either increases on the whole unit interval or increases to one
maximum and then decreases.  For a value of `g` having two preimages, the
smaller preimage has larger `s`, because `s=g/x`.  Consequently the upper
response envelope

\[
 \Phi_A(u)=\max\{s_A(x):g_A(x)=u\}               \tag{15}
\]

is parametrized by the increasing branch of `g_A`.  On that branch,

\[
 {d^2\Phi_A\over du^2}
 =-{2r(r-1)D^3\over C J^3}<0.                   \tag{16}
\]

Hence `Phi_A` is concave on the entire range of `g_A`.  Pointwise domination
and Jensen's inequality now give

\[
 S=E s_A(x)\le E\Phi_A(g_A(x))
       \le\Phi_A(Eg_A)=\Phi_A(A/r).              \tag{17}
\]

It remains only to locate the last value.  Put

\[
                         x_0={A\over r-1}\le1.   \tag{18}
\]

Writing `D_0=D(x_0)>0`, exact subtraction gives

\[
 g_A(x_0)-{A\over r}
 =-{A^2(r-1-A)^2\over r(r-1)D_0}\le0,           \tag{19}
\]

\[
 s_A(x_0)-p
 =-{A(r-1-A)^2\over rD_0}\le0.                 \tag{20}
\]

Also `g_A(1)=A/(A+1)>=A/r`.  Because (14) permits at most one turning
point, the increasing-branch solution `x_*` of `g_A(x_*)=A/r` satisfies
`x_*>=x_0`.  Equations (13), (17), and (20) yield

\[
 S\le\Phi_A(A/r)=s_A(x_*)\le s_A(x_0)\le p,     \tag{21}
\]

which proves (1).  If `A<r-1`, (20) is strict.  If `A=r-1`, Section 2
forces `x=1` almost surely.  Therefore nonzero pair protection on a set of
positive measure makes (1) strict.

## 4. Construction consequence

Arbitrary heterogeneity of partner strength cannot rescue the complete
external pair population.  A successful positive-density trigger must
change at least one structural hypothesis used here: it needs a nonregular
external child law, a cell with more than the singleton/doubleton trace, or
intercell interaction before the rare-colony trace has resolved.  Merely
mixing weak and strong protected pairs is now excluded exactly, rather than
only perturbatively.

## 5. Exact replay

`verify_dense_heterogeneous_pair_relay.py` reconstructs the trace equations,
all derivative and factor identities, the upper-envelope certificate, and
exact rational heterogeneous fixed points.  It does not use sampled fixation
probabilities as proof.
