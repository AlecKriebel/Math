# The scaled endpoint-versus-first-orbit five-ground reduction

Date: 2026-08-13 (America/Los_Angeles)

No graph search, kernel search, or external communication was used.

## 1. Status

**EXACT CONDITIONAL REDUCTION, NOT A PROOF OF THE ENDPOINT INEQUALITY.**
Let `3/2 <= r <= 151/100`, put `c=r-1`, and define

\[
                     {\cal F}_r(y)={rRy\over1+rRy}.       \tag{1}
\]

The still-open lower half of the scaled sandwich is

\[
                    \boxed{\quad E_p s\leq E_p{\cal F}_r(cq).\quad} \tag{2}
\]

This note proves three structural statements about (2).

1. Its target density has an exact resolvent representation using the five
   positive grounds `{1,a,b,v=as,w=acq}`.
2. The complete cone obtained by summing all ten pairwise cut-Picone
   inequalities has an exact finite Farkas alternative.  Consequently (2)
   is reduced to one sharply specified linked-order statement.
3. The tempting potential-only proof using just the `(w,v)` order is
   impossible as an unconditional pointwise certificate: even on the exact
   local potential surface, its correction can vanish while the target
   density is negative.

The third statement is only an obstruction to the single-order route.  It
does not refute the ten-order five-ground cone, and none of the statements in
this note proves or refutes (2).

## 2. Adjoint endpoint setup and corrected scaling

Let `P` be finite, row stochastic, and self-adjoint in `L^2(pi)`.  Let
`a>0`, normalize `E_pi a=1`, and put

\[
 p=\pi a,\qquad R=D_a^{-1}PD_a,\qquad t={Pa\over a}.       \tag{3}
\]

Suppose the positive endpoint solutions obey

\[
 tb=r(1-b)Pb,\qquad s=r(1-s)Rs.                            \tag{4}
\]

Write

\[
 q=1-b,\qquad h=1-s,\qquad X=cq,\qquad
 h_1={1\over1+rRX}.                                       \tag{5}
\]

The factor `c` in `X=cq` is essential.  At the homogeneous endpoint
`q=1/r`, it gives

\[
 {\cal F}_r(X)={c\over r}=s,
\]

whereas the unscaled input is not baseline matched when `r<2`.

Divide the second equation in (4) by `h` to obtain

\[
                         {1\over h}=1+r(t-Rh).             \tag{6}
\]

Since `1/h_1=1+rRX`, subtraction gives the pointwise identity

\[
\boxed{
 h-h_1=rhh_1\{R(h+X)-t\}
      =rhh_1R(X-s).}                                      \tag{7}
\]

Therefore the gap in (2) is exactly

\[
 E_p{\cal F}_r(X)-E_ps
  =E_p(h-h_1)
  =rE_p\{hh_1R(X-s)\}.                                   \tag{8}
\]

Equation (8) is a resolvent reduction, not a sign argument: `R` need not
preserve the weighted average after multiplication by `hh_1`.

## 3. The five positive grounds

Put

\[
                         v=as,\qquad w=aX=acq.              \tag{9}
\]

The five grounds and their exact node potentials `V_f=(Pf)/f` are

\[
\begin{array}{c|ccccc}
f&1&a&b&v=as&w=aX\\ \hline
V_f&1&t&t/(rq)&1/(rh)&RX/X=Rq/q.
\end{array}                                                \tag{10}
\]

Here scalar multiplication by `c` does not change the potential of `w`.
In particular,

\[
 1-h_1=rXV_w h_1,\qquad 1-h=rhV_v.                         \tag{11}
\]

The target node density is

\[
 e_i=a_i(h_i-h_{1,i})
    =a_i r h_i h_{1,i}(X_iV_{w,i}-s_iV_{v,i}).             \tag{12}
\]

It also admits the exact local separation

\[
\boxed{
 {e\over a}
 ={h\over h+X}(X-s)
  +{rXhh_1\over h+X}(V_w-V_v).}                           \tag{13}
\]

Thus the only new ground needed by the corrected scaling is still `w`; the
linked ratios and potentials, rather than a new endpoint equation, carry
the remaining information.

## 4. Complete ten-order Picone certificate

For positive grounds `f,g`, define

\[
 z_i^{fg}={g_i\over f_i},\qquad
 d_i^{fg}=f_ig_i(V_{g,i}-V_{f,i}).                         \tag{14}
\]

The cut-Picone identity says that for every increasing function `psi_fg`
on the finite ratio set,

\[
                    \sum_i\pi_i d_i^{fg}\psi_{fg}(z_i^{fg})\leq0. \tag{15}
\]

Indeed, with symmetric conductances `kappa_ij=pi_iP_ij`, its left side is

\[
 {1\over2}\sum_{ij}\kappa_{ij}f_if_j
 (z_j^{fg}-z_i^{fg})
 \{\psi_{fg}(z_i^{fg})-\psi_{fg}(z_j^{fg})\},              \tag{15a}
\]

which is nonpositive term by term.

Take one orientation of every unordered pair in

\[
                         {\cal G}=\{1,a,b,v,w\}.            \tag{16}
\]

There are ten pairs.  Hence the following is immediate.

**Complete five-ground certificate.**  If increasing functions `psi_fg`
exist such that

\[
 e_i+\sum_{\{f,g\}\subset{\cal G}}
        d_i^{fg}\psi_{fg}(z_i^{fg})\geq0
 \qquad\hbox{for every }i,                                \tag{17}
\]

then (2) holds.

Indeed, multiply (17) by `pi_i`, sum, and apply (15) to every correction.
This is the complete certificate obtainable by taking arbitrary
nonnegative sums of the ten pairwise cut-Picone inequalities of the five
known grounds.

The data are not ten independent scalar orders.  For any three grounds,

\[
 z^{fk}=z^{fg}z^{gk},\qquad
 d^{fk}={k\over g}d^{fg}+{f\over g}d^{gk},                 \tag{18}
\]

and, specifically,

\[
 {w\over a}=X,\qquad {v\over a}=s,\qquad {v\over w}={s\over X}. \tag{19}
\]

Any proof must retain these simultaneous linkages.

## 5. Exact theorem of alternatives

For a nonnegative node vector `lambda` and a pair `fg`, define each lower
prefix

\[
 L_{fg}(z)=\sum_{i:z_i^{fg}\leq z}\lambda_i d_i^{fg}.       \tag{20}
\]

Exactly one of the following alternatives holds:

1. the ten increasing label potentials in (17) exist;
2. there is a nonzero `lambda>=0` such that, for every pair `fg`,

   \[
   \sum_i\lambda_i d_i^{fg}=0,\qquad
   L_{fg}(z)\geq0\quad\hbox{at every proper ratio cut},     \tag{21}
   \]

   while

   \[
                              \sum_i\lambda_i e_i<0.        \tag{22}
   \]

This is finite-dimensional Farkas elimination.  Give one variable to each
distinct ratio level in every order, impose consecutive monotonicity, and
dualize the node inequalities (17).  Eliminating the nonnegative dual flows
on consecutive order edges gives exactly the prefix conditions (21), and
the prefix values conversely reconstruct those flows.

For the physical measure `lambda=pi`, (21) follows automatically from the
cut-Picone identity.  The exact theorem that would close this route is
therefore:

> Every nonnegative measure obeying all ten simultaneous linked ground
> orders (21), for data arising from (3)--(5), has nonnegative `e`-average.

This statement is neither proved nor refuted here.  A dual vector satisfying
(21)--(22) would refute only this complete pairwise-Picone certificate cone;
it would not necessarily be a physical reversible kernel and would not by
itself refute (2).

There is also an exact reason why the ten total-order equations cannot close
the theorem merely by identifying `lambda` with the physical measure.  Form
the `10 by n` matrix whose rows are the ten vectors `d^{fg}`.  For `n>=12`,
its nullspace has dimension at least two and contains `pi`.  Hence it contains
a vector `u` not proportional to `pi`.  If all physical proper prefix sums
in (21) are strict, then for every sufficiently small signed `epsilon`,

\[
                            \lambda=\pi+\epsilon u          \tag{22a}
\]

remains positive and preserves all ten total equations and all ten families
of prefix inequalities.  Thus a full-cone proof must use the specific target
`e`, not uniqueness of the simultaneous cut measure.  This dimension
observation does not produce (22), so it is not a refutation of the full
cone.

## 6. Exact obstruction to a potential-only single `(w,v)` order

For the orientation `(w,v)`, the signed potential correction is

\[
 d^{wv}=wv(V_v-V_w)=a^2Xs(V_v-V_w),                       \tag{23}
\]

and its ratio label is

\[
                              {v\over w}={s\over X}.        \tag{24}
\]

A pointwise proof using only the local `(w,v)` potential data, with no other
ground or endpoint constraint, would require an increasing function `psi`
such that

\[
                         e+d^{wv}\psi(s/X)\geq0             \tag{25}
\]

throughout the exact positive potential surface (11).

Such an unconditional potential-only certificate is impossible.  Choose any

\[
                         0<X<s<1                             \tag{26}
\]

and set

\[
 V_v=V_w={1\over r(1-s)},\qquad
 h_1={1\over1+rXV_w}={1-s\over1-s+X}.                     \tag{27}
\]

Then both identities (11) hold, but

\[
 d^{wv}=0,
 \qquad
 {e\over a}=h-h_1
 ={(1-s)(X-s)\over1-s+X}<0.                               \tag{28}
\]

Thus (25) fails independently of the choice of `psi`, even if monotonicity
is dropped.  This does not assert that the displayed one-node data alone are
a complete physical endpoint kernel; that would require all the other linked
grounds.  For a fully rational specialization of the local potential surface
valid on the whole fitness interval, take

\[
 X={c\over4},\qquad s={c\over2},\qquad
 V_v=V_w={1\over r(1-c/2)}.                               \tag{29}
\]

Its target is exactly

\[
                         {e\over a}
 =-{c(3-r)\over2(5-r)}<0
 \qquad\left({3\over2}\leq r\leq{151\over100}\right).     \tag{29a}
\]

This obstruction is intentionally local: the remaining eight grounds and
nine orders may exclude or compensate the bad node after global summation.
It proves that (13) cannot be closed by silently replacing the target with
the `(w,v)` Picone term, not that the complete five-ground route fails.

## 7. Relation to the proved upper sandwich

The separate scaled first-orbit theorem proves

\[
                    E_p{\cal F}_r(cq)\leq cE_pq             \tag{30}
\]

uniformly on `3/2<=r<=151/100`.  Combining it with (2) would give

\[
                         E_ps\leq cE_pq,
\]

the desired diffuse support inequality at `R_hyb`.  The work here isolates
the entire remaining endpoint obligation without claiming that its
ten-order sign consequence is automatic.
