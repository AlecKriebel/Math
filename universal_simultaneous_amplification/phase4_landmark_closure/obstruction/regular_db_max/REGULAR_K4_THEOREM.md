# Exact regular-order-four dB maximizer theorem

## Theorem

Let `G` be a finite connected undirected weighted regular graph on four
vertices, with zero self-weights and nonnegative edge weights.  At mutant
fitness two,

\[
 \rho_{\rm dB}(G,2)\le \rho_{\rm dB}(K_4,2)={3\over7}.
\]

Equality holds if and only if all six edge weights of `G` are equal.

## Proof

Scale the common weighted degree to one.  If `ij` and `kl` are opposite
edges, the degree sum at `i,j` is twice `w_ij` plus the four cross-edge
weights; the degree sum at `k,l` is twice `w_kl` plus the same cross-edge
weights.  Regularity gives `w_ij=w_kl`.  After relabelling,

\[
 P=\begin{pmatrix}
 0&a&b&c\\ a&0&c&b\\ b&c&0&a\\ c&b&a&0
 \end{pmatrix},\qquad a+b+c=1.                         \tag{1}
\]

For a mutant pair joined by an edge of weight `x`, direct death--birth
updating gives the upward probability at the next type-changing event

\[
 q_x={2(1+x)\over4+x}.                                 \tag{2}
\]

Let `f_1,f_3` be the common fixation values from a singleton and a triple,
and put `f_{2,x}=q_xf_3+(1-q_x)f_1`.  The type-changing rate from a singleton
to its `x`-pair is `2x/(1+x)`; the complementary rate from a triple to its
`x`-pair is `x/(2-x)`.  Substitution into the singleton and triple harmonic
equations yields

\[
 f_1={4A\over4+5A},\qquad
 A=\sum_{x\in\{a,b,c\}}{4x\over4+x}.                  \tag{3}
\]

The following identity uses only `a+b+c=1`:

\[
 A={12\over13}-{16\over169}
 \sum_{x\in\{a,b,c\}}{(3x-1)^2\over4+x}.             \tag{4}
\]

The right side of (3) is strictly increasing in `A`.  Equations (3)--(4)
therefore give

\[
 {3\over7}-\rho_{\rm dB}(G,2)
 ={16\over91(4+5A)}
 \sum_{x\in\{a,b,c\}}{(3x-1)^2\over4+x}\ge0.        \tag{5}
\]

Equality in (5) requires `a=b=c=1/3`, and this condition is sufficient.  The
derivation is rational on the closed simplex.  When some edge weights vanish,
continuity gives the same formula; connectedness excludes only the degenerate
case with a single positive opposite-edge pair and ensures the absorbing
solution is unique.  This proves the theorem.  QED.

## Exact certificate

`verify_regular_k4.py` independently constructs all fourteen labelled
transient equations from the death--birth definition, substitutes the values
in (2)--(3), checks every harmonic equation over the rational-function field,
and verifies identities (4)--(5).
