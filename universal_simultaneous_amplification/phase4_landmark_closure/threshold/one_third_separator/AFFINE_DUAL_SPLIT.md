# Exact affine dual split and its orientation obstruction

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Exact split

Fix `r=3/2` and put `a=r-1=1/2`.  Let `L` be the exact Bd
branching--coalescing dual, `C` the same unbatched dual with every underlying
arrow reversed, and `D` the exact geometric-burst dB dual.  Write

\[
 m_L=E_{\pi_L}|A|,\qquad m_C=E_{\pi_C}|A|,\qquad
 m_D=E_{\pi_D}|A|,
\]

and let `b,d` be the corresponding complete-graph means for `L,D`.  Define

\[
 x={m_L\over b},\qquad z={m_C\over b},\qquad y={m_D\over d}.
\]

Exact duality identifies `x,y` with the normalized Bd and dB fixation
probabilities.  The one-third endpoint excess has the taut but structurally
useful decomposition

\[
 \boxed{
 {x+2y\over3}-1
 =\left({x+2z\over3}-1\right)+{2\over3}(y-z).}       \tag{1}
\]

Thus the two inequalities

\[
             m_L+2m_C\le3b,                            \tag{2}
\]

and

\[
             {m_D\over d}\le {m_C\over b}             \tag{3}
\]

would separately imply the desired separator.  Equation (3) is the existing
normalized locked-target batching comparison.  The coefficient in (2) is
the same sharp `1:2` coefficient selected by the clique--pendant theorem.

The main result of this note is that (2) is **EXACTLY FALSE**.  Consequently
(1) is an exact decomposition, but not a separately signed proof.

## 2. Poisson--Dirichlet form of the orientation term

The failed orientation inequality nevertheless has a concise exact
graph-independent reduction.  The calculation is stated for general
`r=1+a`; specialize to `a=1/2` afterward.  Give nonempty sets reference mass

\[
                    \mu(A)\mathrel\propto a^{|A|}.
\]

The weighted-adjoint identities are

\[
 L^{\dagger_\mu}=C+V,\qquad C^{\dagger_\mu}=L-V,       \tag{4}
\]

where

\[
 V(A)=r\sum_{i\in A}q_i,\qquad
 q_i=1-\sum_jP_{ji}
     =\sum_jw_{ij}(d_i^{-1}-d_j^{-1}).                 \tag{5}
\]

Let `chi_L,chi_C` be the uniquely `mu`-mean-zero Poisson solutions

\[
 -L\chi_L=|A|-m_L,\qquad -C\chi_C=|A|-m_C.            \tag{6}
\]

Since `mu` has mean

\[
 b={na(1+a)^{n-1}\over(1+a)^n-1},
\]

take the `mu` inner product of (6) with the constant function.  Equations
(4) give directly

\[
 \langle V,\chi_L\rangle_\mu=m_L-b,\qquad
 \langle V,\chi_C\rangle_\mu=b-m_C.
\]

Therefore

\[
 \boxed{
 rb-am_L-m_C
 =\langle V,\chi_C-a\chi_L\rangle_\mu.}              \tag{7}
\]

At `a=1/2`, (2) is exactly the proposed sign of twice the right side of
(7).  If

\[
 Z_i=\langle {\bf1}_{\{i\in A\}},\chi_C-a\chi_L\rangle_\mu,
\]

undirected summation by parts turns (7) into the original-graph pairing

\[
 \boxed{
 rb-am_L-m_C
 =r\sum_{i<j}w_{ij}(d_i^{-1}-d_j^{-1})(Z_i-Z_j).}     \tag{8}
\]

This explains why the `1:2` orientation attempt is a global Dirichlet sign,
not a pointwise cut comparison.

## 3. Exact rational counterexample to the orientation sign

Take the connected six-cycle with positive integer edge weights

\[
\begin{array}{c|rrrrrr}
\text{edge}&01&12&23&34&45&50\\ \hline
\text{weight}&1&6{,}000{,}000{,}000&4{,}000{,}000&
5{,}000{,}000{,}000&20{,}000&7{,}000{,}000{,}000.
\end{array}                                             \tag{9}
\]

An independent exact 62-state solve, using the labelled link rates rather
than the dual stationary implementation, gives

\[
\begin{aligned}
 x&=0.97663793994876249307\ldots,\\
 z&=1.0155264975429422355\ldots,\\
 y&=0.96667603476243281645\ldots.
\end{aligned}                                           \tag{10}
\]

Every sign below is decided over the rationals:

\[
 {x+2z\over3}-1
 =0.00256364501154898805\ldots>0,                       \tag{11}
\]

so (2) and the Dirichlet sign in (8) fail.  But

\[
 y-z=-0.04885046278050941905\ldots<0,                   \tag{12}
\]

and the actual endpoint score remains

\[
 {x+2y\over3}-1
 =-0.03000333017545729134\ldots<0.                      \tag{13}
\]

Hence the batching loss more than cancels the wrong-signed orientation
term.  This graph does **not** violate the one-third separator and does not
simultaneously amplify at the endpoint.

## 4. Exact status

- **PROVED:** dual split (1).
- **PROVED:** Poisson and original-graph identities (7)--(8).
- **EXACTLY REFUTED:** the separate orientation inequality (2), by (9).
- **NUMERICALLY OBSERVED:** the normalized batching inequality (3) survives
  complete-support optimization through order six and every saved hostile
  witness tested here.
- **OPEN:** the combined sign in (1), hence the universal one-third
  separator.

The counterexample shows that a proof must retain cancellation between
orientation and batching.  Closing either term independently is not enough.
