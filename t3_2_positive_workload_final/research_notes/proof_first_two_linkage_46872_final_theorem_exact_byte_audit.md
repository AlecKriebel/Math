# Exact-byte hostile audit of the final 46,872-pair theorem

**Independent proof-first audit, 2026-08-12 PDT.**  The immutable target is

~~~text
research_notes/proof_first_two_linkage_46872_final_theorem.md
SHA-256 dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde
206 lines / 7,865 bytes
~~~

The verdict is **STRICT PASS** at these exact bytes.  The proof is a
disjoint union of completed fixed-support-pair theorems.  It does not infer
recurrence from a finite computation, compose chart exits, switch
potentials along one trajectory, or enumerate orientations, rates,
populations, reaction histories, or communicating classes.

## 1. Exact support universe

For ten binary complexes, assign each complex to the first support, the
second support, or neither.  Requiring both ordered supports to have at
least two vertices gives the direct inclusion--exclusion count

\[
 3^{10}-2\bigl(2^{10}+10\,2^9\bigr)
 +(1+10+10+90)=46{,}872.                 \tag{1.1}
\]

The last four terms are respectively the cases in which both small
supports are empty, only the first is a singleton, only the second is a
singleton, or both are distinct singletons.  Thus (1.1) is the literal
ordered universe of disjoint nontrivial supports, not an orbit count.

The final union certificate and its test rehash as

~~~text
certificate 5b249ded4b54801f7eb5ab9ced943ed566216e1228c0e07f3e205b1eef319288
test        dd51ce074aa43bb4722d176ef4c85face956c924150681d5cae32f3b615c5e76
~~~

Its four byte-pinned source dependencies independently rehash to the
expected values.  The five focused union tests were rerun under a current
Python interpreter and all passed.

## 2. Exact five-way identity

The certificate proves pairwise disjointness, exhaustiveness, and the
literal identity

\[
 46{,}872=27{,}462+432+146+336+18{,}496.  \tag{2.1}
\]

The five canonical branch fingerprints are

~~~text
completed mixed orbit       1bf337cf143c6eb4cee5088827bb9e9b9cec704f01a1b1f57bde6aed856d2812
active-invariant orbit gap  5516d6071b2b9d07d50a11cbedfa6d891bf6310f1ad56fce34aac50967269397
strict positive invariant   d1fc7112f8a08605ef4dc33b664bce47c765e5c49b7496433e53a22bb62a087c
level-set residual          ea3d7b08d39c6f9cc4c5a15c9924a624a5ccb4a6a356724ecddea96aa18869ea
outside-mixed remainder     eb7db151e42eb9562b1a1d519ea7dad212df52c6df368ffa08edbf79410db4ad
~~~

Their union has fingerprint

~~~text
00446e17dca5ce6b75e86cdc755b5660d7c94b68fa4f3e6f028efa40d02c6c60
~~~

and the ordered branch manifest has fingerprint

~~~text
bd6ae54bff3aed8fc4fedb9255fe0b7377a28dc67404d6a5bea41c6aa4ac1bba.
~~~

The clean-room test also verifies the intermediate identities

\[
 27{,}894=27{,}462+432,
 \qquad
 18{,}978=146+336+18{,}496,               \tag{2.2}
\]

and the disjoint \(11{,}842+6{,}654\) split of the last branch.  The
certificate explicitly states that it makes no recurrence claim; its role
ends at the finite set identity.

## 3. Analytic branch pins and scopes

Every load-bearing target and audit cited by the final theorem was rehashed
from the current bytes:

~~~text
completed mixed orbit
  target a91e8c31f35312ef4b9063e8f5a48af534861145db2236e662ea6cc1eff8e30e
  audit  32eec768b2d8d701664f3ace2b1a7c04fd3790a4811eba5e05d56a8fa903e73b
  cert   57d8904dd86cd0bf626e344dbfd7b7f248b239cdeaace48489796058c6875f08
  test   e708c52f6cbc1bbc4dabf33f246d72379dff58c74cc97a38fdd8076ac3ae7d13

active-invariant orbit gap
  target 7edab78daabbf7e492851efe5326ccc228adfcb57f02cd5ff55eaa7056e034c8
  audit  1110efc0760ed8714fc4bf203739152820f6f9a18cbdc0e92716638a707140fd

level-set residual
  target 6e9ddcaccd03fe64b1c6a57cbaef052e984eaf7b7e2e87c4df52ca1240787a6c
  audit  35b18c365ce954594397b4c48ed55f7d11c847af37594f0fb354517434f76d72

outside-mixed remainder
  target e7b08be8b6ca3ff604f3975bdae18b526db532ea1168f25bf21170d8248b5106
  audit  192dfc3d79401c57416b582b45aeb0140f0c1ad3e0f90ab80acaae48e3b9a090
~~~

The mixed-orbit theorem first removes the 110 active-only invariant seeds,
then proves all 5,059 eligible seeds before taking their exact symmetry
orbit.  The 432 theorem is a seam-free population-Foster theorem.  The 146
branch is self-contained: a strictly positive invariant bounds every
coordinate on its fixed level set.  The 336 theorem is a completed
classwise physical-time Foster theorem.  The 18,496 wrapper is an exact
union of two standalone fixed-pair theorems and has a second independent
audit at SHA-256

~~~text
fb9c82f3b6a51c785e5800437c4d0fe0cd1cb9be298d683cd09edbf494f3d81f.
~~~

Accordingly, every member of every branch has an analytic theorem at its
literal support scope for arbitrary strong labelled orientations and
positive labelled rates.

## 4. Pairwise composition has no stochastic seam

Fix a physical network.  Its ordered pair of linkage supports is immutable.
The finite identity (2.1) assigns that pair once and for all to exactly one
completed theorem.  Therefore the final composition never compares branch
potentials and never interprets a descriptor exit as drift in another
chart.  This directly excludes the previously identified terminal-SCC,
current-target charging, and cross-potential interface failures.

The unordered nature of physical linkage classes creates no gap: the finite
universe contains both linkage orders, and every branch theorem is closed
under the ordering used by its exact selector.

## 5. From finite-set return to positive recurrence

Each analytic branch gives finite mean return to a finite subset \(K\) of
the fixed closed irreducible class \(\Gamma\).  Choose \(o\in K\).  For each
state of \(K\), irreducibility supplies a finite actual labelled path to
\(o\).  There are only finitely many such starts and paths, so the minimum
success probability is positive and all holding-time means on successful
prefixes are uniformly finite.

Stop an attempt at its first competing label.  Because \(K\), the path
menu, and the reaction set are finite and jumps are bounded, every failed
endpoint belongs to a finite set.  The branch return theorem has finite
mean return to \(K\) from each of those endpoints.  Uniformizing over this
finite set and retrying geometrically yields finite mean positive return to
\(o\).  A singleton closed class is immediate.  Thus every closed
irreducible class is positive recurrent.

## 6. Nonexplosion

Let \(N(x)=1+|x|_1\).  Since all targets are binary, a reaction with a
degree-two source cannot increase \(N\).  Every increasing channel has
source degree at most one, bounded jump size, and hence total positive
increment intensity at most \(C N(x)\) for a network-dependent constant
\(C\).

For the process stopped at level \(R\), Dynkin's formula and Gronwall give

\[
 \mathbb E_x N(X_{t\wedge\tau_R})\le N(x)e^{Ct}.       \tag{6.1}
\]

Therefore \(\Pr_x\{\tau_R\le t\}\le N(x)e^{Ct}/R\), up to the harmless
bounded overshoot convention, and population cannot escape in finite time.
Before \(\tau_R\), the population state lies in a finite set; all
mass-action hazards, including neutral quadratic hazards, are bounded
there.  Infinitely many neutral or decreasing firings therefore cannot
accumulate before population escape.  This proves nonexplosion of the
minimal CTMC.

## 7. Species and projection boundary

Networks with fewer than three species embed by zero-padding their complex
vectors, so the ten-complex universe remains exhaustive.  For the core
Theorem 1.1, distinct linkage classes already have disjoint supports.
Deleting zero-displacement labels does not change the population generator.

The extra fixed-class projection sentence is explicitly conditional: the
exact conjugacy must produce at most three dynamic species and exactly two
active projected linkage classes.  Collapsing duplicate projected vertices
preserves strong connectivity; strongly connected projected linkages that
share a vertex have strongly connected union; and parallel labels may be
aggregated by summing their positive rates.  Under the stated condition the
two surviving supports are disjoint, nontrivial members of the same exact
46,872-pair universe.  The final theorem makes no claim for a projection
with zero, one, or more than two active projected linkages.

## 8. Publication and exact-byte checks

The target was converted with Pandoc using
`markdown+tex_math_single_backslash` and compiled with Tectonic to a clean
letter render.  Every page was visually inspected.  The support table,
dotted-union arithmetic, dependency hashes, nonexplosion equations, and
final proof symbol render literally; no clipping or corrupt TeX token was
found.  A hidden-byte scan found no non-ASCII control or escape corruption.

Thus Theorem 1.1 receives **STRICT PASS** at target SHA-256

~~~text
dae2a58f170836427ffc053ff931c1909d64ac591d77b971591b0d5814526cde.
~~~
