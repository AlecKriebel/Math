# Embedded labelled reaction-count Green theorem

## 1. Setup

Let `(Z_n)_{n>=0}` be the population embedded chain on one infinite closed
irreducible class `Gamma`.  The next labelled channel is denoted `E_{n+1}`;
conditional on `Z_n=x`,

\[
 P(E_{n+1}=e\mid Z_n=x)
 =\frac{\kappa_e(x)_{y_e}}{\Lambda(x)}.
\]

The channel mark is physical: equal population displacements with different
sources or targets remain different channels.

Fix `o in Gamma`.  Choose an increasing finite exhaustion `D_M` such that
`o in D_M` and every fixed finite path is contained in `D_M` for all large
`M`.  Put

\[
 T_o^+=\inf\{n\ge1:Z_n=o\},\qquad
 \sigma_M=\inf\{n\ge0:Z_n\notin D_M\},
\]

and

\[
 \tau_M=T_o^+\wedge\sigma_M,\qquad t_M=E_o\tau_M.
\]

## 2. Divergence of the killed mean

If `E_o T_o^+=infinity`, then

\[
 \tau_M\uparrow T_o^+
\]

pathwise.  Indeed, every finite initial segment of a discrete sample path
uses finitely many states and hence lies in all sufficiently large `D_M`.
Monotone convergence gives

\[
 t_M\longrightarrow\infty.                     \tag{2.1}
\]

Define the normalized labelled transition-count occupation

\[
 \nu_M(x,e)=\frac1{t_M}
 E_o\sum_{n<\tau_M}
 1\{Z_n=x,E_{n+1}=e\}.                         \tag{2.2}
\]

It is nonnegative and

\[
 \sum_{x,e}\nu_M(x,e)=1.                       \tag{2.3}
\]

No physical-time channel intensity is used in this normalization.

## 3. Escape from finite sets

Let `K subset Gamma` be finite.  For each `x in K`, irreducibility supplies a
simple positive-probability embedded path

\[
 x=x_0,x_1,\ldots,x_l=o
\]

which does not revisit `x` after time zero.  Let `delta_x>0` be the product
of its labelled transition probabilities.  For all sufficiently large `M`
the path lies inside `D_M`.

Every visit to `x` before `tau_M` therefore has conditional probability at
least `delta_x` of being followed by a hit of `o` before the next return to
`x`.  The number of visits to `x` before `tau_M` is stochastically dominated
by a geometric random variable with mean `1/delta_x`, apart from the single
initial visit when `x=o`.  Hence

\[
 \sup_M E_o\sum_{n<\tau_M}1\{Z_n=x\}<\infty.    \tag{3.1}
\]

Summing over `K` and using (2.1),

\[
 \sum_{x\in K,e}\nu_M(x,e)\longrightarrow0.    \tag{3.2}
\]

Thus the normalized transition occupation escapes every finite set of
population states.

## 4. Exact balance identities

For any bounded `f:Gamma->R`, pathwise telescoping gives

\[
 \sum_{n<\tau_M}[f(Z_{n+1})-f(Z_n)]
 =f(Z_{\tau_M})-f(o).
\]

Taking expectations and dividing by `t_M`,

\[
 \sum_{x,e}\nu_M(x,e)
 [f(x+\zeta_e)-f(x)]
 =\frac{E_o[f(Z_{\tau_M})-f(o)]}{t_M}.          \tag{4.1}
\]

The right side tends to zero for bounded `f`.  In particular, finite
partitions of state/phase space inherit exact asymptotic flow balance.

For a physical linear workload `h`, define

\[
 q_M=\frac{E_o[Z_{\tau_M}-o]}{t_M}.
\]

Then the same pathwise identity, now justified directly rather than by a
bounded-test limit, gives

\[
 \sum_{x,e}\nu_M(x,e)h\cdot\zeta_e=h\cdot q_M. \tag{4.2}
\]

Every bimolecular reaction changes each coordinate by at most two.  Hence
pathwise

\[
 \|Z_{\tau_M}-o\|_\infty\le2\tau_M,
\]

so `(q_M)` is bounded.  Moreover `Z_{\tau_M,i}>=0`, and therefore

\[
 q_{M,i}\ge-\frac{o_i}{t_M}.
\]

After subsequence extraction,

\[
 q_M\to q\in\mathbb R^3_{\ge0}.                \tag{4.3}
\]

Consequently `h\cdot q>=0` for every nonnegative workload `h`.

## 5. Compactified nonzero occupation

Although the measures in (2.2) lose mass on the countable state space, they
remain probability measures after pushforward to the compactification used
in `terminal_chart_localization.md`.  Every weak limit has total mass one,
and (3.2) places it entirely on the boundary at infinity.  The limiting
object is therefore nonzero.

## 6. Source-layer traces

Reaction-count normalization may be dominated by a faster neutral layer.
The proof never concludes that a slower changing layer has positive mass in
`nu_M` merely because it exists graphically.

Inside a fixed finite workload shell, collapse a closed faster neutral class
by its exact finite Green matrix and observe the trace at the first event in
the next source layer or at a declared chart exit.  If the expected number
of such events diverges, normalize their exact counts and repeat (4.1).  If
it does not diverge, the normalized flux of that layer is zero and the layer
is deleted.  Because the source flag has finite length, this elimination
terminates.  At the first occupied changing trace layer, its normalized
transition occupation is nonzero by construction.

This qualification is essential: raw embedded counts alone need not assign
positive limiting mass to a slower source layer when faster neutral reaction
rates diverge.

## 7. CTMC interface

At every nonabsorbing population state, at least one channel is enabled.
Every enabled falling factorial is a positive integer, so

\[
 \Lambda(x)\ge\kappa_{\min}>0.                 \tag{7.1}
\]

If a positive embedded return uses `N` jumps, the conditional expected
physical duration is at most `N/kappa_min`.  Thus finite expected embedded
return count implies finite expected physical return time.

Nonexplosion is proved separately in `global_return_closure.md`; it is not
inferred from (7.1).

## 8. Lexicographic reaction-count normalization lemma

Let the complete source flag be `E_1 >> ... >> E_r`.  For a killed path let

\[
 C_k(M)=E_o\#\{n<\tau_M:y_{E_{n+1}}\in E_k\}.
\]

Suppose all layers before `k` have been eliminated as complete-workload
neutral.  Then exactly one of the following holds.

1. `C_k(M)` is bounded.  Since jumps are bounded, layer `k` has bounded total
   workload displacement and is irrelevant to an escaping endpoint.
2. `C_k(M)->infinity`.  Normalize the labelled counts in layer `k` by
   `C_k(M)`.  Finite-shell Green elimination of faster neutral motion gives a
   nonzero probability trace occupation satisfying exact phase balance.
3. Positive normalized flux leaves the current shell/support chart during
   faster elimination; this is a retained structural exit.

If the endpoint workload escapes, not every workload-changing layer can have
bounded count.  Select the first changing layer with diverging count.  All
faster layers are neutral by construction, and every slower layer is absent
from this normalization.  This is the precise meaning of "the first occupied
changing layer carries positive normalized flux."

The lemma prevents an invalid deletion of a rare stabilizing linkage.  A
linkage may vanish under raw jump-count normalization yet reappear at the
next slower trace.  The hierarchy terminates after at most the number of
enabled source layers.
