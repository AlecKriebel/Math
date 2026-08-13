# Independent exact-byte audit of the final T3-2 global theorem

**Independent hostile proof-first audit, 2026-08-12 PDT.**  The immutable
target is

~~~text
research_notes/proof_first_t3_2_global_theorem.md
SHA-256 781d2520cbb3ad30e1749814f620d49d4c503c5c341ccd1add39a5fec31e2b7f
164 lines / 6,898 bytes
~~~

The verdict is **STRICT PASS** at these exact bytes.  The fixed-class
projection is an exact generator conjugacy, and its image is routed once and
for all into a completed zero-, one-, or two-active-linkage theorem.  No
trajectory switches among theorem potentials.

## 1. Exact fixed-class projection

Fix a closed irreducible class $\Gamma$.  Let $L$ be an original active
linkage, choose a source $y_0$ enabled at $x\in\Gamma$, and put
$r=x-y_0\ge0$.  For every directed path

\[
 y_0\longrightarrow y_1\longrightarrow\cdots\longrightarrow y_k,
 \tag{1.1}
\]

the literal population path is $r+y_0,r+y_1,\ldots,r+y_k$.  Every target
creates the next source, and closure keeps each reached state in $\Gamma$.
If coordinate $i$ is constant on $\Gamma$, then

\[
 m_i=r_i+(y_j)_i \qquad(0\le j\le k).                \tag{1.2}
\]

Strong connectivity therefore makes the $i$-stoichiometry common to every
complex in $L$.  The deleted-coordinate propensity factor

\[
             \prod_{i\ \mathrm{constant}}(m_i)_{y_i} \tag{1.3}
\]

is positive and constant, so absorbing it into the corresponding labelled
rate gives exactly the projected stochastic mass-action propensity.

This also closes the possible zero-displacement seam.  Projection is
injective on each active linkage support: two complexes with the same
dynamic projection already have the same constant coordinates by (1.2),
and hence are the same original complex.  Thus no nontrivial reaction of an
active linkage collapses to zero displacement.  Any explicitly retained
zero-displacement label is generator-inert and may be deleted without
changing the chain.

A linkage with no source enabled anywhere on $\Gamma$ has zero propensity
there and contributes no transition.  If projected active linkages share a
vertex, their union is strongly connected: route to the shared vertex in
one component and away from it in the other, and use the reverse strong
paths for the return.  Retaining parallel labels, or equivalently summing
their effective positive rates, preserves every transition rate.

Let $\pi$ delete the constant coordinates.  It is one-to-one on $\Gamma$
and onto its image $\Gamma'=\pi(\Gamma)$.  The preceding rate identity
intertwines the two generators.  It also makes $\Gamma'$ closed and
irreducible, because every original transition projects and every projected
transition from $\Gamma'$ lifts uniquely.  Hence the chains restricted to
$\Gamma$ and $\Gamma'$ have identical holding-time and jump laws under
$\pi$.

Deleting coordinates cannot increase dynamic species, while deleting and
merging linkages cannot increase active linkage count.  The reduced
complexes remain binary.  This proves every assertion of Lemma 2.1,
including the exact interface needed by the analytic inputs.

## 2. Exact routing to completed pair theorems

The one-linkage target and audit rehash as

~~~text
target b7306d448d0556beff1879796c1b399ed7786fdca086d8fd9125b0832d090563
audit  bebda68bb91bb5b22bcf4ee5d1eaf7920accde02a82210b6ffbacd9e57d6ee35
~~~

They prove nonexplosion and classwise positive recurrence for every reduced
binary network having at most three dynamic species and exactly one active
strong linkage, with arbitrary positive labelled rates.  The theorem itself
includes the same exact projection interface, so applying it to the already
reduced image introduces no new assumption.

The two-linkage target and audit rehash as

~~~text
target dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde
audit  a4f50dcbc2235766524ddb7000a264ec88bf04f8841b3ce9b8d4689c800ba619
~~~

They cover every ordered pair of disjoint nontrivial binary supports on at
most three species, for arbitrary strong labelled orientations and positive
rates.  The projected linkages satisfy this literal scope: each is strong,
projection is injective within it, and all projected collisions between
different linkages were merged before the active count was taken.

If the reduced active linkage count is zero, no transition changes a state
of $\Gamma'$.  Irreducibility makes $\Gamma'$ a singleton.  Counts one and
two invoke the respective completed theorem above.  These three alternatives
are exhaustive under the stated intrinsic hypothesis.  Since the count is a
fixed-class structural datum, it does not change along a stochastic path;
the one- and two-linkage Lyapunov functions are never compared.

## 3. Nonexplosion

Let $N(x)=1+|x|_1$.  A degree-two source cannot increase total population
because every target is binary.  Every population-increasing channel
therefore has source degree at most one and bounded jump size.  Finiteness of
the reaction set gives

\[
 \sum_{y\to z}\lambda_{y\to z}(x)(|z|-|y|)^+
       \le C N(x).                                    \tag{3.1}
\]

At $\tau_R=\inf\{t:N(X_t)\ge R\}$, Dynkin's formula and Gronwall yield

\[
 \mathbb E_xN(X_{t\wedge\tau_R})\le N(x)e^{Ct},
 \qquad
 \mathbb P_x(\tau_R\le t)\le\frac{N(x)e^{Ct}}R.      \tag{3.2}
\]

The second bound tends to zero with $R$.  Within each bounded-population
sublevel the state space is finite and the full mass-action hazard is
bounded, so neutral quadratic reactions cannot accumulate there.  Explosion
would require either such bounded accumulation or population escape; both
are excluded.  This proves nonexplosion of the original minimal chain,
including the more intrinsic version with additional inactive or merging
original linkages.

## 4. Transport of recurrence and theorem scope

Positive recurrence is invariant under the bijective CTMC conjugacy
$\pi:\Gamma\to\Gamma'$.  Thus the finite mean return supplied by the
appropriate reduced theorem transports to every original state of
$\Gamma$.  For the original T3-2 hypothesis, at most three species and at
most two weakly reversible linkage classes automatically reduce to at most
three dynamic species and at most two active projected linkage classes.

Conversely, the proof only uses those two reduced counts.  It therefore
justifies the target's stronger intrinsic formulation for a chosen closed
class even when the unreduced network has additional constant coordinates,
inactive linkages, or projected linkages that merge.  It makes no claim
beyond binary complexes, three dynamic species, or two active projected
linkages.

## 5. Publication checks

The exact target was independently converted with Pandoc's single-backslash
TeX-math reader and compiled with Tectonic.  The result is a clean
three-page letter-size PDF with zero compiler or layout diagnostics.  All
pages were visually inspected: Theorem 1.1, the path-lifting calculation,
the constant-factor display, both Foster displays, and all dependency hashes
are legible and unclipped.  Text and hidden-byte scans found no corruption;
the exact target SHA above receives **STRICT PASS**.
