# Search beyond the `3/2` construction threshold

Date: 2026-08-02 (America/Los_Angeles)

No literature search or external contact was used.  This report separates
exact derivations from numerical reconnaissance.  It does **not** claim an
improved lower bound beyond `R_sim>=3/2`.

## 1. Outcome

No global construction beyond `3/2` survived the center-load and reverse-
establishment checks in this track.

Two exact findings sharpen the search:

1. A natural four-vertex singular module is dB-establishing above `3/2`, up
   to the unique real root `1.543689...` of

   \[
     r^3-2r^2+2r-2=0,
   \]

   but its Bd and dB center-degree windows are disjoint for every `r>1` by
   the transparent identity

   \[
     Z_{\rm upper}-Z_{\rm lower}
       =-(r-1)^2(r^2+1)<0.
   \]

2. The rational triangle with edge weights `(3,3,2)` has a distinguished
   vertex whose fixation probability exceeds the infinite-complete baseline
   under both rules at `r=31/20`.  This is an exact simultaneous **rooted
   portal**, not a uniformly initialized population construction.  Every
   tested handoff architecture multiplied its advantage by a subunit transfer
   probability or imposed a compensating resident load on the large core.

The general early-migration branching derivative was derived exactly.  Broad
optimization over three-, four-, and five-vertex weighted colonies found no
positive coefficient at `r=1.55`.  This is numerical evidence only, not an
obstruction theorem.

## 2. Exact four-vertex two-edge module

Take two unit-weight edges and join their endpoint sets by edges of weight
`epsilon`, then let `epsilon -> 0`.  Internal resolution of the initial pair
occurs before a cross-pair event.  From one mutant in a pair, the pair fixes
with probability `r/(r+1)` under Bd and `1/2` under dB.  Once one pair is
mutant and the other resident, direct successful-rate division gives macro
fitness `r^2` under both update rules.  Hence the uniform singleton limits are

\[
 \alpha_B=\frac{r^3}{(r+1)(r^2+1)},\qquad
 \alpha_D=\frac{r^2}{2(r^2+1)}.                 \tag{1}
\]

The corresponding reverse singleton probabilities at each vertex are

\[
 \beta_B=\frac1{(r+1)(r^2+1)},\qquad
 \beta_D=\frac1{2(r^2+1)}.                     \tag{2}
\]

Writing `p=(r-1)/r`, exact subtraction gives

\[
 \alpha_B-p=\frac1{r(r+1)(r^2+1)}>0,           \tag{3}
\]

\[
 \alpha_D-p=
 -\frac{r^3-2r^2+2r-2}{2r(r^2+1)}.             \tag{4}
\]

The cubic in (4) is strictly increasing because
`3r^2-4r+2>0`.  It is negative at `r=3/2` and positive at
`r=31/20`, giving the unique threshold `1.543689...`.

Now weakly join many copies to a growing clique center with total internal
weighted degree `Z`, exactly as in the proved triangle construction.  A
mutant module must seed the center before a resident center erases it.  The
large-center successful odds are

\[
 A_B=Z(r-1)(r+1)(r^2+1),\qquad
 A_D=\frac{2r(r-1)(r^2+1)}Z.                   \tag{5}
\]

The contribution `alpha_U A_U/(1+A_U)` exceeds `p` precisely when

\[
 Z>1\quad\text{for Bd},                         \tag{6}
\]

and, whenever (4) is positive,

\[
 Z< -r(r^3-2r^2+2r-2)\quad\text{for dB}.       \tag{7}
\]

But the right side of (7) minus one is exactly

\[
 -(r-1)^2(r^2+1),                               \tag{8}
\]

so (6)--(7) never overlap.  This is a proved no-go for the equal-pair
singular module in the separated clique-center architecture, despite its
apparently favorable dB establishment interval beyond `3/2`.

## 3. Exact rooted portal

Let a triangle have weights

\[
 w_{01}=w_{12}=3,\qquad w_{02}=2,
\]

and start the mutant at vertex `1`.  Solving all six transient equations
directly gives

\[
 f^{B}_1(r)=
 \frac{5r^2(12r^2+20r+9)}
 {60r^4+172r^3+233r^2+172r+60},                 \tag{9}
\]

\[
 f^{D}_1(r)=
 \frac{3r(2r^2+8r+3)}
 {(r+1)(9r^2+34r+9)}.                           \tag{10}
\]

At `r=31/20`, both comparisons are positive exactly:

\[
 f^{B}_1-p=\frac{40209028}{464555925}>0,
 \qquad
 f^{D}_1-p=\frac{1534279}{17564383}>0.          \tag{11}
\]

Thus a common root can be locally favorable well beyond `3/2`.  This rules
out the simplistic explanation that Bd-good and dB-good entry vertices must
always be disjoint.  It does not solve uniform initialization: a large core
must still be reached and retained.

## 4. Early migration and the unavoidable center load

Let a finite module `H` have internal degrees `d_i`.  Give module vertex `i`
total edge weight `h_i` to a clique center whose **actual** total degree is
`D`.  Let `s_i^U(p)` be the probability that the exact finite module colony,
started at `i`, emits at least one nonextinct center lineage, when a center
lineage survives with probability `p=1-1/r`.  Center-to-module replacements
are included in this killed chain; no internal-resolution assumption is made.

If `M/c=mu -> 0`, differentiating the coupled center/colony branching PGF at
`mu=0` gives

\[
 \rho_U^{\rm branch}=p+\mu C_U+O(\mu^2),        \tag{12}
\]

where

\[
 C_B=\sum_i s_i^B-|H|p+
 \frac{\sum_i(h_i/D)s_i^B-p\sum_i h_i/(d_i+h_i)}{r-1}, \tag{13}
\]

\[
 C_D=\sum_i s_i^D-|H|p+
 \frac{\sum_i h_i s_i^D/(d_i+h_i)-p\sum_i h_i/D}{r-1}. \tag{14}
\]

Equations (13)--(14) follow by direct implicit differentiation of the center
extinction equation.  They expose the load missed by a one-active-module
calculation: by the handshake identity, `M sum(h_i)/c` contributes to every
center degree.  Large local escape rates cannot be installed on a positive
mass of modules without altering center establishment at the same order.

`search_branching_derivative.py` evaluates (13)--(14) for the singular
triangle.  `search_general_colony_derivative.py` builds the full subset chain
for arbitrary weighted modules and evaluates the same coefficients.  At
`r=1.55`, extensive floating-point optimization gave negative best scores for
orders three through five.  These searches are **NUMERICALLY OBSERVED** and
not a proof of `C_B<=0` or `C_D<=0`.  Since the coefficients add across rare
satellite types, the convex tradeoff frontier of Bd-special and dB-special
colonies was also optimized; no tested mixture entered the positive quadrant.

## 5. Other numerical reconnaissance

- Direct optimization of separated weighted modules of orders four and five
  found no nonempty clique-center window at `r=1.51` or `1.55`.
- A finite portal feeding a large clique was optimized over its internal
  weights, entry attachment, handoff attachment, and center degree.  At
  `r=1.55`, the best balanced composite rooted probability was about `0.3313`,
  below `p=0.35484`.
- Repeated-module cliques, recursive stars, and weighted-star cores all lost
  the portal gain in the first reverse-establishment or handoff factor.
- Allowing the external entry distribution and the weak interportal
  attachment distribution to differ did not repair this: optimized rooted
  weak cliques of portal modules of orders three through five reached only
  about `0.325` under both rules at `r=1.55`, below `p=0.35484`.
- A local early-escape calculation that ignored resident-satellite load gave
  a false positive near `0.44375` under both rules at `r=1.55`.  Substitution
  into the load-aware PGF made dB strictly worse than baseline.  This is a
  useful diagnostic against future false constructions.
- Mixtures of a Bd-special and a dB-special colony were tested through their
  opposing gain/loss ratios.  For module orders two through five, the product
  of the best two ratios stayed below one at `r=1.50`, `1.51`, and `1.55`.
  The ratios increased with module order, so this is not a reduction theorem.

## 6. Reproducibility and status

- `verify_higher_threshold_identities.py`: exact symbolic certificate for
  (1)--(11), rebuilding the rooted triangle chain from the update rules;
- `verify_branching_derivative.py`: independent finite-difference check of
  (13)--(14) against the full coupled center/colony PGF;
- `search_weighted_modules.py`: separated-module optimization;
- `search_rooted_portal.py`: rooted-entry optimization;
- `search_nested_core.py`: portal-to-clique handoff optimization;
- `search_repeated_modules.py`: weak complete coupling of repeated modules;
- `search_rooted_repeated_core.py`: separately optimized rooted entry and
  interportal attachment laws for a large weak clique of portal modules;
- `search_early_escape.py`: exact seven-state local killed chain;
- `search_branching_satellites.py`: full center/colony PGF;
- `search_branching_derivative.py`: exact formulas (13)--(14) for triangles;
- `search_general_colony_derivative.py`: arbitrary finite-module version.

**PROVED:** the two-edge separated-module no-go and the rational rooted portal
formulas.
**EXACTLY DERIVED:** the rare-satellite branching coefficients (13)--(14).
**NUMERICALLY OBSERVED:** no higher-threshold candidate in the searched
architectures.
**OPEN:** whether any construction exceeds `3/2`, and whether (13)--(14) obey
a universal cross-rule obstruction at `r>=3/2`.
