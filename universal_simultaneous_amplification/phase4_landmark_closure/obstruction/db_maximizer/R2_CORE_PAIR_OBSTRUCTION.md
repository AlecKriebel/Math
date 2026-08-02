# An exact `r=2` obstruction for singular clique windmills

Status: **PROVED FOR THE FAMILY BELOW.**  This is not a universal dB
maximizer theorem.

## 1. Family

Fix `c>=3`, `q>=1`, and satellite sizes `m_j>=2`.  Let `G_epsilon` consist
of:

- a core `C=K_c`, with every core edge of weight one;
- `q` disjoint satellite cliques `B_j=K_(m_j)`, whose internal edges have
  arbitrary fixed weight `a_j>0`;
- every edge from `C` to `B_j`, with common weight `epsilon*b_j`, where
  `b_j>0`;
- no edges between distinct satellites.

Thus `n=c+sum_j m_j`.  All graphs are connected for `epsilon>0`.  The sizes,
internal weights, and relative attachment scales may be heterogeneous, but
are held fixed as `epsilon` tends to zero.

## 2. Theorem

At fitness `r=2`,

\[
 \limsup_{\epsilon\downarrow0}\rho_{\rm dB}(G_\epsilon,2)
 \le {n-1\over2n}
 < \rho_{\rm dB}(K_n,2).
\]

Consequently every fixed choice of `c,q,m_j,a_j,b_j` is dB-suppressing for
all sufficiently small positive `epsilon`.

This rules out the most dangerous numerical regime found in the `r=2`
search: a growing clique core weakly coupled to arbitrarily heterogeneous,
internally fast clique satellites.  It also explains why double-precision
solves appeared to cross zero: the family can approach `(n-1)/(2n)` very
closely, but the complete graph lies strictly above that value.

## 3. Separation reduction

As `epsilon` tends to zero, each component reaches internal absorption before
the next cross-component change with probability tending to one.  Here is a
finite-state justification.  When a component is polymorphic, its internal
absorption time has a finite expectation independent of `epsilon`, while at
each update the probability of a cross-component replacement is `O(epsilon)`.
Truncating the absorption time and applying a union bound shows that a cross
replacement occurs before internal absorption with probability `o(1)`.  The
same argument applies after each rare introduction.  Failed introductions
return to the same internally homogeneous macrostate.  Thus the first
macrostate-changing event is a race among introduction rates, multiplied by
the exact within-component establishment probabilities below; every displayed
first-event probability has error `o(1)`.  All constants are uniform over the
finitely many states because the parameters are fixed.

For `k>=2`, put

\[
 T_k=2^{k-2},\qquad
 \alpha_k=\rho_{\rm dB}(K_k,2)
 ={(k-1)T_k\over k(2T_k-1)},\qquad
 \beta_k=\rho_{\rm dB}(K_k,1/2)
 ={k-1\over k(2T_k-1)}={\alpha_k\over T_k}.
\]

These formulas follow by solving the one-dimensional complete-graph chain
directly.  Write

\[
 A_k=k\alpha_k={(k-1)T_k\over2T_k-1},\qquad
 d_k={A_k\over2T_k}={k-1\over2(2T_k-1)},\qquad
 s_k={k\over2}-A_k={2T_k-k\over2(2T_k-1)}={1\over2}-d_k.
\]

Let `T=T_c` and `A=A_c`.  Suppressing the common update-rate factor `1/n`,
the leading effective rates involving satellite `j` are

| homogeneous state | favorable macro change | adverse macro change |
|---|---:|---:|
| `B_j` mutant, `C` resident | `2*c*m_j*epsilon*b_j*alpha_c/(c-1)` | `c*m_j*epsilon*b_j*beta_(m_j)/(2*a_j*(m_j-1))` |
| `C` mutant, `B_j` resident | `2*c*m_j*epsilon*b_j*alpha_(m_j)/(a_j*(m_j-1))` | `c*m_j*epsilon*b_j*beta_c/(2*(c-1))` |

For example, the first favorable rate is the rate at which one of the `c`
core vertices is replaced from the `m_j`-vertex mutant satellite, multiplied
by the probability `alpha_c` that this introduction fixes in the core.  The
other three entries follow in the same way.  Define the favorable-to-adverse
odds from a mutant satellite by

\[
 z_j={4a_j(m_j-1)\alpha_c\over(c-1)\beta_{m_j}},\qquad
 y_j={z_j\over16T_cT_{m_j}}.
\]

The two directional odds have the exact product

\[
 z_j\,{4(c-1)\alpha_{m_j}\over
              a_j(m_j-1)\beta_c}
 =16T_cT_{m_j}.
\]

It follows that a fixed mutant satellite establishes in the resident core
before being lost with limiting probability

\[
 p_{0,j}={z_j\over1+z_j}.
\]

Starting instead with a mutant core and resident satellites, put

\[
 \omega_j=m_jb_j,\qquad
 y_H={\sum_j\omega_j\over\sum_j\omega_j/y_j}.
\]

The adverse core-loss rates are proportional to `omega_j`; the corresponding
favorable-to-adverse odds are `1/y_j`.  Therefore the probability that some
satellite becomes mutant before the core is lost is

\[
 p_1={1\over1+y_H}.
\]

A uniformly placed singleton in component `K_k` reaches its all-mutant local
state with probability `alpha_k`, contributing total initial mass `A_k`.
Global fixation then requires the first favorable macro event counted by
`p_1` or `p_{0,j}`.  Dropping every later failure can only increase fixation
probability, so

\[
 \limsup_{\epsilon\downarrow0}n\rho_{\rm dB}(G_\epsilon,2)
 \le A p_1+\sum_{j=1}^q A_{m_j}p_{0,j}.
\tag{1}
\]

## 4. The scalar scale-tradeoff lemma

For every `c>=3`, `m>=2`, and `y>0`,

\[
 {A_cy\over1+y}
 +{A_m\over1+16T_cT_my}
 \ge d_c-s_m.
\tag{2}
\]

Only four regimes require proof.  The sequence `d_k` is strictly decreasing,
so `d_c<=d_3=1/3`, while `s_m=1/2-d_m` is strictly increasing.  Hence the
right side of (2) is nonpositive, and the result is immediate, for `m>=5`,
for `m=4,c>=4`, and for `m=3,c>=5`.

For `m=2`, put `x=2T_cy`.  Then (2) is exactly

\[
 {A_c x\over2T_c+x}+{1\over8x+1}\ge {A_c\over2T_c}.
\tag{3}
\]

Since `c-1<=T_c`,

\[
 A_c\le {T_c^2\over2T_c-1}.
\]

For `x>=2T_c/(2T_c-1)`, the first term in (3) suffices.  Below this
threshold, clearing positive denominators reduces (3) to

\[
 F_T(x)=2(2T-1)(2T+x)
 -T(8x+1)\{2T-(2T-1)x\}>0.
\]

This convex quadratic has unrestricted minimum

\[
 {188T^4-364T^3+63T^2+12T-4\over32T(2T-1)}.
\]

Writing `T=2+u`, the numerator becomes

\[
 188u^4+1140u^3+2391u^2+1912u+368>0.
\]

The only remaining pairs `(c,m)` are `(3,3)`, `(4,3)`, and `(3,4)`.  After
putting (2) over its positive common denominator and removing a positive
constant factor, its numerator is respectively

\[
 64y^2-7y+1,\qquad
 4480y^2-65y+27,\qquad
 3456y^2-65y+35.
\]

Their discriminants are `-207`, `-479615`, and `-479615`.  Thus all three
quadratics are strictly positive, proving (2).

## 5. Closing the global budget

A weighted harmonic mean is at least the smallest entry, so choose `j` with
`y_j<=y_H`.  The total loss from the right side of (1), relative to allowing
every locally fixed component to succeed, is at least

\[
 A{y_H\over1+y_H}
 +{A_{m_j}\over1+z_j}
 \ge A{y_H\over1+y_H}
 +{A_{m_j}\over1+16T_cT_{m_j}y_H}
 \ge d_c-s_{m_j}.
\]

Since every `s_k>=0`, this is at least
`d_c-sum_j s_(m_j)`.  On the other hand,

\[
 A_c+\sum_jA_{m_j}-{n-1\over2}
 =d_c-\sum_js_{m_j}.
\]

Subtracting the loss proves from (1) that

\[
 \limsup_{\epsilon\downarrow0}n\rho_{\rm dB}(G_\epsilon,2)
 \le {n-1\over2}.
\]

Finally, direct solution of the complete-graph chain gives

\[
 \rho_{\rm dB}(K_n,2)
 ={n-1\over2n}\,{1\over1-2^{-(n-1)}}
 >{n-1\over2n}.
\]

## 6. Exact audit of the closest numerical false positive

The pair-satellite search case `c=60`, `q=3`, `a_j=10^10`, `b_j=1`, and
`epsilon=10^-8` appeared positive in double precision.  Exact rational
solution of its 608 transient orbit equations gives

\[
 \rho_{\rm dB}(G,2)-\rho_{\rm dB}(K_{66},2)
 =-3.7632440265\ldots\times10^{-10}<0.
\]

`verify_r2_core_pair_obstruction.py` checks the general scalar polynomial
certificate and this exact absorbing solve.

## 7. Boundary of the result

This theorem excludes a broad singular architecture, including arbitrary
fixed clique-satellite sizes, internal weights, and attachment scales.  It
does **not** prove that `K_n` maximizes dB fixation at `r=2` among all connected
weighted graphs.  Non-clique satellites, multiple non-clique cores, nested
modules, or scales and component sizes that change jointly with `epsilon`
remain outside the theorem.
