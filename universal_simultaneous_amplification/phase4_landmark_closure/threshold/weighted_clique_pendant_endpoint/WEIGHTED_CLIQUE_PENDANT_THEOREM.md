# A uniform weighted clique--pendant obstruction at the endpoint

## 1. Graph class and result

Fix `r>1`.  Let `G(c;w_1,...,w_m)` have a hub `H`, `c` ordinary vertices,
and `m` pendant leaves.  The hub and ordinary vertices induce the unit
clique `K_{c+1}`.  Leaf `ell` is joined only to `H`, with arbitrary weight
`w_ell>0`.  Thus the result below includes common-weight and finitely many
weight-class variants, with weights allowed to depend arbitrarily on
`c,m`.

Put `n=c+m+1` and `p=1-1/r`.

**Theorem.**  There are constants `c_0(r)` and `A_r<infinity`, independent
of `m` and of all pendant weights, such that, for `c>=c_0(r)`,

\[
 {\rho_{dB}(G(c;w_1,\ldots,w_m),r)\over\rho_{dB}(K_n,r)}
 \le {c\over c+m}+{A_r\over c+m}.                         \tag{1}
\]

Consequently, every sequence in this graph class with `m->infinity` is
eventually dB-suppressing at the fixed fitness `r`, irrespective of every
weight-scaling regime.  In particular, it cannot be an endpoint
simultaneous-amplifier family.  Any still-viable growing family in this
class must have a bounded number of pendants.

At `r=3/2` one may take `c_0=13` and, nonoptimally, `A_{3/2}=1630`.

This is a class theorem, not the universal endpoint obstruction.  It leaves
open sequences with bounded `m`, for which both normalized probabilities
approach one and the sign is a lower-order question.

## 2. Exact lumped transitions for a common weight

For discovery and finite verification, first take `w_ell=w`.  A lumped
state is `(h,i,j)`, where `h` is the hub type and `i,j` are the mutant
ordinary and leaf counts.  The action of `S_c x S_m` is transitive on every
fibre and commutes with both update rules, proving strong lumpability.

Let

\[
 F=n+(r-1)(h+i+j),\qquad D_H=c+mw.
\]

The six Bd changing probabilities are

\[
\begin{array}{ll}
i\to i+1:&\displaystyle {r(c-i)\over F}
                 \left({h\over D_H}+{i\over c}\right),\\[3pt]
i\to i-1:&\displaystyle {i\over F}
                 \left({1-h\over D_H}+{c-i\over c}\right),\\[3pt]
0\to1\text{ at }H:&\displaystyle {r\over F}\left({i\over c}+j\right),\\[3pt]
1\to0\text{ at }H:&\displaystyle {1\over F}
                 \left({c-i\over c}+m-j\right),\\[3pt]
j\to j+1:&\displaystyle {rhw(m-j)\over D_HF},\\[3pt]
j\to j-1:&\displaystyle {(1-h)wj\over D_HF}.
\end{array}                                                   \tag{2}
\]

For dB, put

\[
 M_H=i+wj,\qquad R_H=c-i+w(m-j).
\]

The hub changes from resident to mutant with probability

\[
 {1\over n}{rM_H\over rM_H+R_H},                            \tag{3}
\]

and from mutant to resident with the same denominator and numerator `R_H`.
The ordinary-vertex transitions are

\[
\begin{array}{ll}
i\to i+1:&\displaystyle {c-i\over n}
 {r(h+i)\over c+(r-1)(h+i)},\\[3pt]
i\to i-1:&\displaystyle {i\over n}
 {c-i+1-h\over c+(r-1)(i-1+h)}.
\end{array}                                                   \tag{4}
\]

Finally, `j->j+1` has probability `h(m-j)/n`, and `j->j-1` has probability
`(1-h)j/n`.  The weight cancels because a dying leaf has only one
competitor.  Equations (2)--(4) come directly from parent--target pairs and
are independently checked from labelled transition rows.

## 3. A uniform bound from an ordinary singleton

Start dB from one mutant ordinary vertex.  Until either the hub activates
or the mutant ordinary count reaches zero, all leaves remain resident.  If
there are `i` mutant ordinary vertices, multiply all probabilities by `n`
and write the three relevant rates as

\[
\begin{aligned}
 b_i&={(c-i)ri\over c+(r-1)i}, &&(i\to i+1),\\
 d_i&={i(c-i+1)\over c+(r-1)(i-1)}, &&(i\to i-1),\\
 a_i&={ri\over c+W+(r-1)i}, &&(H:0\to1),                  \tag{5}
\end{aligned}
\]

where `W=sum_ell w_ell`.  Conditional on no hub activation, the embedded
ordinary-count walk has up/down ratio

\[
 q_i={b_i\over d_i}
 =r{c-i\over c-i+1}
 {c+(r-1)(i-1)\over c+(r-1)i}.                              \tag{6}
\]

Fix any `s,z` with `1<z<s<r`, and stop at `0` or
`k=floor(c/2)`.  Uniformly for `1<=i<k`, once `c` is sufficiently large,

\[
             s\le q_i\le r,
 \qquad {a_i\over a_i+b_i+d_i}\le {a_i\over d_i}
             \le {r(r+1)\over c}.                          \tag{7}
\]

Couple the process to the walk `X` which simply omits hub-activation marks.
The chance that `X` hits `k` is at most the constant-r gambler's-ruin value

\[
                 {p\over1-r^{-k}}.                         \tag{8}
\]

Only a mark on a path which otherwise hits zero can add to (8).  From level
`i`, the latter event has probability at most `s^{-i}`.  To bound its total
occupation, set

\[
 \gamma={s/z+z\over s+1}<1,\qquad
 V(i)={z^{-i}\over1-\gamma}.
\]

Since the up probability is at least `s/(s+1)` and `V` is decreasing,

\[
 V(i)-\mathbb E_iV(X_1)\ge z^{-i}\ge s^{-i}.
\]

Stopping and summing therefore gives

\[
 \mathbb E_1\sum_{t<T}s^{-X_t}
 \le {z^{-1}\over1-\gamma}=:D_s.                           \tag{9}
\]

A union bound over the coupled marks, conditioned on the future zero hit,
now yields the uniform singleton bound

\[
 u_C\le {p\over1-r^{-k}}+{r(r+1)D_s\over c}.               \tag{10}
\]

The argument grants fixation after a hub activation or after hitting `k`,
so it is an upper bound and uses no post-establishment assumption.

## 4. All leaf singleton starts together cost at most a constant

Start instead from leaf `ell`.  Before either its death or hub activation,
there are no other type-changing events.  Writing `D=c+sum_z w_z`, the
exact probability that activation occurs first is

\[
 {rw_\ell\over D+(2r-1)w_\ell}\le {rw_\ell\over D}.        \tag{11}
\]

Even granting certain fixation after activation gives

\[
                  \sum_{\ell=1}^m u_{L_\ell}\le r.         \tag{12}
\]

This is why neither extreme weights nor multiple pendant-weight classes
evade the obstruction.

## 5. Uniform initialization and complete-graph comparison

Granting fixation from an initial mutant hub and using (10)--(12),

\[
 \rho_{dB}(G,r)\le {1\over n}
 \left\{{cp\over1-r^{-k}}+r(r+1)D_s+1+r\right\}.           \tag{13}
\]

The exact loopless complete-graph baseline is

\[
 \rho_{dB}(K_n,r)={n-1\over n}{p\over1-r^{-(n-1)}}.        \tag{14}
\]

Dividing (13) by (14), dropping the factor `1-r^{-(n-1)}`, and absorbing
the bounded quantity

\[
 \sup_{c\ge c_0}{c r^{-\lfloor c/2\rfloor}
                 \over1-r^{-\lfloor c/2\rfloor}}
\]

into a constant proves (1).

This also proves the stated consequence without an implicit assumption that
`c->infinity`.  Along subsequences with `c>=c_0`, the right side of (1) is
strictly below one once `m>A_r`.  If instead `c<c_0` while `m->infinity`,
granting fixation to all `c+1` core starts and using (12) gives

\[
                 \rho_{dB}(G,r)\le {c+1+r\over n}\to0,
\]

whereas the complete-graph baseline tends to `p>0`.

For the explicit endpoint constants, take `s=5/4,z=9/8`.  If `c>=13`,
the two factors multiplying `r=3/2` in (6) have product at least

\[
 {2c-1\over2(c+2)}\ge {5\over6}.
\]

Moreover `D_s=144`, so `r(r+1)D_s=540`.  The remaining exponential term is
bounded by `2`: writing `k=floor(c/2)>=6`, its upper envelope is
`(2k+1)(2/3)^k/(1-(2/3)^k)`, which is below `2` at `k=6` and decreases
thereafter.  Inserting `p=1/3` gives the advertised safe choice
`A_{3/2}=1630`.

## 6. Exact status

- **PROVED:** exact common-weight lumping and transitions.
- **PROVED:** the arbitrary-weight dB bound (1), uniformly over all positive
  pendant weights and all `m`.
- **PROVED:** every such family with `m->infinity` is eventually
  dB-suppressing at every fixed `r>1`.
- **NUMERICALLY OBSERVED:** optimizing both the endpoint simultaneous minimum
  and `(x+2y)/3` over common weights through the recorded finite search found
  no violation; the closest cases have one pendant and approach one from
  below.
- **OPEN WITHIN THIS CLASS:** the all-scaling sign for bounded `m`.
- **OPEN UNIVERSALLY:** the endpoint no-simultaneous-amplification theorem.
