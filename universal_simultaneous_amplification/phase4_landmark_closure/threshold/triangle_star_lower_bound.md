# A singular-triangle clique-star proves \(R_{\rm sim}\ge 3/2\)

## Status

The construction and all finite symbolic calculations in this note are
**PROVED**.  The conclusion is the threshold lower bound

\[
R_{\rm sim}\ge \frac32.
\]

It is not a universal upper bound.  In particular, the failure of this one
family at and above \(3/2\) does not show that \(R_{\rm sim}=3/2\).

## 1. The graph family

For an integer \(N\ge2\), put

\[
c_N=N,\qquad M_N=N^2,\qquad
\delta_N=N^{-4},\qquad z_N=N^{-3},\qquad
\epsilon_N=2^{-2^{N^4}}.
\]

The graph \(T_N\) has one center set \(C\) of \(c_N\) vertices and
\(M_N\) disjoint three-vertex leaves \(L_j=\{A_j,B_j,C_j\}\).  Its edges
are as follows.

* Every two center vertices have edge weight \(z_N\).
* In leaf \(j\), the edge \(A_jC_j\) has weight \(1\), while
  \(A_jB_j\) and \(B_jC_j\) have weight \(\delta_N\).
* Every center vertex is joined to every vertex of every leaf with weight
  \(\epsilon_N\).
* There are no edges between distinct leaves.

Thus \(|V(T_N)|=N+3N^2\), all displayed weights are positive rational
numbers independent of fitness, and \(T_N\) is connected.

Schematic picture (each thin bundle is complete bipartite):

```text
                     A_j ===== C_j       (weight 1)
                       \       /
                     δ  \     /  δ
                         \   /
                          B_j
                           ⋮
                     ε-complete bundle
                           ⋮
                 [ clique C of size N ]
                    each edge weight z
```

## 2. Isolated-module quantities

For a connected weighted module \(F\), let

\[
\phi^U_{F,v}(q)
\]

be the probability that a fitness-\(q\) mutant initially at \(v\) fixes in
the isolated module under rule \(U\).  Write

\[
a_F^U(q)=\frac1{|F|}\sum_v\phi^U_{F,v}(q),\qquad
I_F=\sum_v\frac1{d_v},
\]

and, for dB,

\[
J_F(q)=\sum_v\frac{\phi^{\rm dB}_{F,v}(q)}{d_v}.
\]

For the leaf triangle \(L_\delta\), direct solution of its six transient
subset equations gives

\[
\lim_{\delta\downarrow0}
(\phi^{\rm Bd}_{A},\phi^{\rm Bd}_{B},\phi^{\rm Bd}_{C})=(0,1,0),
\]

\[
\lim_{\delta\downarrow0}
(\phi^{\rm dB}_{A},\phi^{\rm dB}_{B},\phi^{\rm dB}_{C})
=\left(\frac12,0,\frac12\right).
\]

Consequently, for every fixed \(q>0\),

\[
a_L^{\rm Bd}(q)\longrightarrow\frac13,qquad
a_L^{\rm dB}(q)\longrightarrow\frac13.
\tag{2.1}
\]

The inverse-degree quantities are

\[
I_L=\frac{1+5\delta}{2\delta(1+\delta)}
       \sim\frac1{2\delta},
\tag{2.2}
\]

and

\[
J_L(q)\longrightarrow\frac{q+2}{2}.
\tag{2.3}
\]

In particular, at relative fitnesses \(r\) and \(1/r\),

\[
J_L(r)\to\frac{r+2}{2},\qquad
J_L(1/r)\to\frac{2r+1}{2r},
\]

so the effective dB forward/reverse factor is

\[
r^2\frac{J_L(r)}{J_L(1/r)}
\longrightarrow \frac{r^3(r+2)}{2r+1}.
\tag{2.4}
\]

For the center clique, whose common internal weighted degree is
\((c-1)z\), symmetry gives

\[
I_C=\frac{c}{(c-1)z},\qquad
J_C(q)=\frac{c,a_C^{\rm dB}(q)}{(c-1)z}.
\tag{2.5}
\]

For either update rule and fixed \(r>1\), direct solution of the one-count
birth--death chain gives

\[
a_C^U(r)\longrightarrow 1-\frac1r,
\qquad
a_C^U(1/r)=O_r(\theta_r^c)
\quad\text{for some }0<\theta_r<1.
\tag{2.6}
\]

For Bd this is the usual geometric sum, derived from the constant down/up
ratio \(1/r\).  For dB the exact down/up ratio at mutant count \(i\) is

\[
\gamma_i(q)
=\frac{c-1+(q-1)i}{q\,[c-q+(q-1)i]}
=\frac1q\left(1+
 \frac{q-1}{c-q+(q-1)i}\right).
\tag{2.7}
\]

It converges to \(1/q\) uniformly in \(1\le i<c\).  The geometric-sum
formula for a one-dimensional absorbing chain proves the first limit in
(2.6); when \(q=1/r<1\), all \(\gamma_i(q)\) are eventually bounded below
by a fixed number greater than one, proving the exponential bound.

## 3. The rare-migration trace, derived from the update rules

First hold \(c,M,\delta,z\) fixed and let the common center--leaf weight
\(\epsilon\downarrow0\).  With probability tending to one, an invaded
module returns to a monomorphic state before another cross-module
replacement.  Conditioning on the first cross-module replacement therefore
gives a trace chain on

\[
(h,k)\in\{0,1\}\times\{0,\ldots,M\},
\]

where \(h\) records the center type and \(k\) the number of mutant leaves.
Failed invasions are trace self-loops.

Suppose first that \(h=0\) and one particular leaf is mutant.  Ignoring a
common positive factor, let \(A\) be the rate at which that leaf converts the
center and \(D\) the rate at which the resident center converts that leaf
back.  If \(h=1\), let \(B\) be the rate at which the mutant center converts
one particular resident leaf and \(C\) the rate at which that resident leaf
converts the center back.  Directly summing the cross-edge terms in the two
update rules gives

\[
\begin{array}{c|cccc}
 &A&D&B&C\\ \hline
{\rm Bd}
&c r I_L a_C^{\rm Bd}(r)
&3 I_C a_L^{\rm Bd}(1/r)
&3r I_C a_L^{\rm Bd}(r)
&c I_L a_C^{\rm Bd}(1/r)\\[2mm]
{\rm dB}
&3rJ_C(r)
&\dfrac{c}{r}J_L(1/r)
&crJ_L(r)
&\dfrac3rJ_C(1/r).
\end{array}
\tag{3.1}
\]

For example, in Bd, summing over source vertices produces the source factor
\(I_F\), while the target of a complete bipartite bundle is uniform.  In dB,
death at target \(v\) produces the factor \(1/d_v\); the reverse event has
relative invader fitness \(1/r\), which accounts for the displayed defense
factor.  Thus (3.1) is a direct consequence of the two definitions, not an
assumed coarse-graining.

Starting from one monomorphic mutant leaf and a resident center, consider the
specific favorable path on which the center converts before that leaf is
lost, and then all other leaves convert before the center reverts.  Its exact
probability in the trace chain is

\[
p_U=\frac{A_U}{A_U+D_U}
\left(\frac{B_U}{B_U+C_U}\right)^{M-1}.
\tag{3.2}
\]

This is a lower bound on eventual fixation in the trace chain.

## 4. Evaluation at the chosen scales

Let \(c=N,M=N^2,\delta=N^{-4},z=N^{-3}\).  Equations (2.1)--(2.6) and
(3.1) give

\[
\frac1{N^2}\frac{A_{\rm Bd}}{D_{\rm Bd}}
\longrightarrow \frac{r-1}{2},
\tag{4.1}
\]

\[
\frac1{N^2}\frac{A_{\rm dB}}{D_{\rm dB}}
\longrightarrow
\frac{6r^2(r-1)}{2r+1}.
\tag{4.2}
\]

Both limits are strictly positive for every fixed \(r>1\).  Moreover,

\[
M\frac{C_{\rm Bd}}{B_{\rm Bd}}
=O_r(N^4\theta_r^N)\longrightarrow0,
\qquad
M\frac{C_{\rm dB}}{B_{\rm dB}}
=O_r(N^4\theta_r^N)\longrightarrow0.
\tag{4.3}
\]

It follows from (3.2) that \(p_U\to1\) for both rules.

The proportion of vertices lying in leaves is

\[
\frac{3M}{3M+c}=\frac{3N^2}{3N^2+N}\longrightarrow1.
\]

Conditional on a uniformly selected leaf vertex, its isolated-module
establishment probability tends to \(1/3\) by (2.1).  Thus the rare-migration
fixation probability satisfies

\[
\rho_U(T_N,r)\longrightarrow\frac13,
\qquad U\in\{\mathrm{Bd},\mathrm{dB}\}.
\tag{4.4}
\]

For completeness, the matching upper bound follows because, before the
initial leaf first becomes monomorphic, the probability of a cross-module
event tends to zero.  If that leaf becomes resident, global extinction has
already occurred; initial center vertices have vanishing sampling mass.

### Explicit diagonal in \(\epsilon\)

The preceding trace derivation first sends \(\epsilon\) to zero at each fixed
\(N\).  The stated explicit choice

\[
\epsilon_N=2^{-2^{N^4}}
\]

implements the diagonal limit.  Here is a self-contained quantitative
justification.  On the compact fitness interval
\(K_N=[1+1/N,N]\), every transition entry is a rational function of
\(\epsilon\).  Cramer's rule, after writing determinants as sums of directed
forests, expresses each absorption probability as a ratio of polynomials in
\(\epsilon\) with nonnegative monomial weights.  There are at most

\[
Q_N=2^{N+3N^2}
\]

states.  After the lowest common power of \(\epsilon\) is removed, ratios of
nonzero coefficients are bounded by

\[
\exp\!\left(2^{O(N^2\log N)}\right).
\tag{4.5}
\]

Indeed, a forest uses fewer than \(Q_N\) transition factors; after inserting
\(\delta=N^{-4}\), \(z=N^{-3}\), and \(r\in K_N\), each coefficient factor
and its reciprocal are at most a fixed power of \(N\), and fewer than
\(Q_N^{Q_N}\) forests occur.  Positivity prevents cancellation of the first
nonzero coefficient.  Consequently the full-chain/trace-chain error is at
most (4.5) times \(O(\epsilon_N)\), which tends to zero because
\(2^{N^4}\) dominates \(2^{O(N^2\log N)}\).  Every fixed \(r>1\) lies in
\(K_N\) for all sufficiently large \(N\).  This proves (4.4) for the single
explicit graph family, with no fitness-dependent diagonal choice.

## 5. Strict comparison and the threshold lower bound

For either update rule on complete graphs of growing order, direct solution
of the mutant-count chain gives

\[
\rho_U(K_n,r)\longrightarrow1-\frac1r.
\tag{5.1}
\]

Fix \(1<r<3/2\).  Then

\[
\frac13-\left(1-\frac1r\right)=\frac{3-2r}{3r}>0.
\]

Equations (4.4) and (5.1) imply that for all sufficiently large \(N\),

\[
\rho_{\rm Bd}(T_N,r)>\rho_{\rm Bd}(K_{|T_N|},r),
\qquad
\rho_{\rm dB}(T_N,r)>\rho_{\rm dB}(K_{|T_N|},r).
\]

The family is independent of \(r\), so this proves
\(R_{\rm sim}\ge3/2\).

## 6. Sharp scale window inside this ansatz

The constants in the useful center-weight window can also be read off
exactly.  Suppose the reverse-center risk in (4.3) is negligible and write
\(x=A/D\).  The leading fixation probability is

\[
\frac13\frac{x}{1+x}.
\]

It exceeds \((r-1)/r\) exactly when

\[
r<\frac32,
\qquad
x>\frac{3(r-1)}{3-2r}.
\tag{6.1}
\]

Using the leading forms of (3.1), condition (6.1) becomes

\[
z>\frac{6\delta}{c(3-2r)}(1+o(1))
\quad\text{for Bd},
\tag{6.2}
\]

and

\[
z<\frac{2r^2(3-2r)}{c(2r+1)}(1+o(1))
\quad\text{for dB}.
\tag{6.3}
\]

The choice \(\delta=N^{-4},c=N,z=N^{-3}\) lies between these two bounds
for every fixed \(1<r<3/2\) once \(N\) is large.

## 7. Independent exact certificate

Run

```bash
python threshold/verify_triangle_star.py
```

from the `phase4_landmark_closure` directory.  The verifier constructs the
triangle subset chains directly from the update definitions, solves them
symbolically, checks the closed forms and all singular limits, verifies the
dB defense factor (2.4), and checks the macro comparison identity (6.1).
