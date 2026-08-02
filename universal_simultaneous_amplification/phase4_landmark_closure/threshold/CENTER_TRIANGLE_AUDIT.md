# Hostile independent audit of `CENTER_TRIANGLE_PROOF.md`

Audit date: 2026-08-01
Auditor track: threshold search (independent of the construction derivation)

## Verdict

**PROVED AFTER TWO LOCAL REPAIRS.**  I found no error in the construction,
the isolated fixation formulas, the successful trace rates, the scale
asymptotics, or the conclusion

\[
\rho_{\rm Bd}(G_N,r),\rho_{\rm dB}(G_N,r)\longrightarrow\frac13
\quad(r>1\text{ fixed}).
\]

I found one false sentence in the excursion-count discussion and two omitted
hypotheses in the stated rare-edge lemma.  All are repairable without
changing the graph, scales, or conclusion.  The corrected excursion bound is
still far below the chosen `N^10` cutoff.

## Itemized findings

### 1. Construction and connectivity — **PROVED**

The graph has `c=N` center vertices and `M=N^2` three-vertex modules, hence
`n=N+3N^2`.  The weights

\[
\delta=N^{-4},\quad z=N^{-3},\quad \varepsilon=N^{-N^3}
\]

are positive rational numbers independent of fitness.  Every module vertex
is connected to every center vertex, so the graph is connected.

### 2. Triangle subset chains — **PROVED / EXACTLY COMPUTED**

I independently rebuilt both six-transient-state chains from the update
definitions.  The exact averages (5)--(6), the reverse Bd sum, the dB
inverse-degree sums, and all limits (10)--(11) agree identically.

In particular, as `delta -> 0`, the three singleton vectors are

\[
(0,1,0)\quad\text{for Bd},\qquad
\left(\frac12,0,\frac12\right)\quad\text{for dB},
\]

and both uniform averages tend to `1/3`.  Also

\[
I_D(\delta,r)\to\frac{2r+1}{2r},\qquad
J_D(\delta,r)\to\frac{r+2}{2}.
\]

The construction certificate and the separately written threshold-track
certificate both pass.

### 3. Center clique formulas — **PROVED**

For dB at mutant count `i`, direct division of the down and up probabilities
gives

\[
\gamma_i(r)=
\frac{c-1+(r-1)i}{r[c-r+(r-1)i]}.
\]

Since the denominator factor at `i` is the numerator factor at `i-1`, the
product telescopes to (13).  Summing these products gives (14), including

\[
\bar Q_c^{\rm dB}/Q_c^{\rm dB}=r^{2-c}.
\]

The Bd formulas and reverse ratio are likewise exact.

### 4. Rare-trace rates (20), (22), (25), and (26) — **PROVED**

I recomputed every rate directly.

For Bd with one mutant module and a resident center, the favorable successful
rate is proportional to

\[
r c\varepsilon Q_c(r)
\sum_v(d_v+c\varepsilon)^{-1},
\]

and the adverse rate is proportional to

\[
\frac{c\varepsilon}{Z+3M\varepsilon}
\sum_v\beta_v(r).
\]

Their ratio is exactly the leading expression in (20).  This yields

\[
A_{B,N}\sim\frac{r-1}{2}\frac Z\delta
\sim\frac{r-1}{2}N^2.
\]

For dB, death at a center vertex gives the first line of (22), while death at
module vertex `v` gives the second.  The reverse invader fitness factor
`1/r` is present.  Hence

\[
A_{D,N}\sim
\frac{6r^2(r-1)}{2r+1}N^2.
\]

With a mutant center and a particular resident module, recomputation gives

\[
\frac{\text{bad}}{\text{good}}
=O_r(ZX\bar Q_c^{\rm Bd})=O_r(N^2r^{-N})
\]

for Bd and

\[
\frac{\text{bad}}{\text{good}}
=O_r(Z^{-1}\bar Q_c^{\rm dB})=O_r(N^2r^{2-N})
\]

for dB.  Multiplication by `M=N^2` still tends to zero.  Therefore the
specific direct sweep used as a lower bound succeeds with probability
`1-o(1)`.

### 5. Exact scale window (24) — **PROVED**

If `x` is the favorable/adverse successful-rate ratio in the first stage,
the leading fixation contribution is

\[
\frac13\frac{x}{1+x}.
\]

It exceeds `(r-1)/r` exactly when

\[
r<\frac32,qquad x>\frac{3(r-1)}{3-2r}.
\]

Substitution of the audited Bd and dB ratios gives exactly

\[
Z>\frac{6\delta}{3-2r},\qquad
Z<\frac{2r^2(3-2r)}{2r+1},
\]

respectively.

### 6. Rare-edge lemma statement — **GAP, LOCALLY REPAIRED**

The proof uses two hypotheses not stated in the lemma:

1. `epsilon <= b` (indeed it is enough that total outer weighted degree be
   controlled by a constant times the internal upper-degree bound);
2. every component has positive internal degree, so a singleton component
   with no internal edge is excluded.

Without these, the generic lower bound (16) need not follow from the stated
assumptions.  Both hypotheses hold overwhelmingly for the actual family:
all components have at least three vertices and
`epsilon=N^(-N^3) << a=N^-4 <= b=1`.

With these hypotheses inserted, the proof is valid.  A discordant internal
edge supplies a prescribed oriented type change with probability at least
`p=a/(C_r n^2b)`.  From every nonmonomorphic state a path of at most `s`
such changes reaches a monomorphic state.  Blocking the embedded internal
change chain into groups of `s` yields expected length at most `s p^-s`.
The outer/internal event ratio and denominator-perturbation coupling then
give (15).  At the construction scales,

\[
\log\eta_N=-N^3\log N+O_r(N\log N),
\]

so any polynomial number of excursions is coupled with error `o(1)`.

### 7. Excursion-count sentence — **ERROR, NONFATAL**

Section 6 says that the only small per-introduction success probability is
the dB center-to-module probability.  This is false if “outer excursions”
counts every type-changing outer introduction.  During the Bd sweep,
resident-module-to-center introductions are more frequent than the favorable
center-to-module introductions by order `N^2`.  The favorable direction
therefore occurs with probability only `Theta_r(N^-2)` per excursion.

The required polynomial bound nevertheless remains true.  Direct raw-rate
comparison gives the following lower bounds for the probability that one
outer excursion produces some successful macro change:

\[
\begin{array}{c|cc}
 &\text{module to center stage}&\text{center sweep stage}\\ \hline
\mathrm{Bd}&c_r&c_rN^{-2}\\
\mathrm{dB}&c_r\delta_N&c_r\delta_N.
\end{array}
\]

For dB, the `delta_N` factor is exactly the inverse-degree-biased chance that
the singular `B` seed fixes; for Bd in the sweep stage, the `N^-2` factor is
the raw direction imbalance just noted.  Thus the expected number of
excursions through all `M=N^2` conversions is `O_r(N^6)`.  Markov's inequality
gives

\[
\Pr\{L>N^{10}\}=O_r(N^{-4})=o(1).
\]

Replacing the disputed sentence by this calculation fully repairs the use of
the trace lemma.

### 8. Uniform initialization and the `1/3` limit — **PROVED AFTER REPAIRS**

The initial center mass is `O(N^-1)`.  From a leaf start, the repaired trace
bound makes an outer event before first internal absorption an `o(1)` event.
The isolated leaf fixes with probability `1/3+o(1)`.  Conditional on leaf
fixation, the two audited stages reach global fixation with probability
`1-o(1)`.

This proves the lower bound `rho_U >= 1/3-o(1)`.  It also proves the matching
upper bound: except on the vanishing early-outer-event event, an initial leaf
that does not fix internally has already lost the last mutant; initial-center
starts have vanishing mass.  Hence `rho_U <= 1/3+o(1)`.

The complete-graph limits are `(r-1)/r` for both rules, so strict simultaneous
amplification follows for each fixed `1<r<3/2` and sufficiently large `N`.

## Certificate execution

The following were run independently:

```text
PASS: verify_triangle_module.py (all exact identities and limits)
PASS: verify_center_triangle_lumping.py
      (all states for c=2,M=1 and c=2,M=2, both rules, exact Fractions)
PASS: threshold/verify_triangle_star.py (independent symbolic derivation)
PASS: Python compilation of all construction and threshold scripts
PASS: git diff --check
```

The quotient verifier initially failed because the machine's Python 3.9
lacks `int.bit_count`.  Replacing that call by `bin(mask).count("1")` is a
compatibility-only repair; after it, all exact checks passed.

## Addendum: audit of the `r=3/2` endpoint expansion

The subsequently added Section 8 was audited independently.

### 9. Error scale below `N^-2` — **PROVED**

The first-stage Markov tail is `O_r(N^-6)`, the full-sweep Markov tail is
`O_r(N^-4)`, the trace coupling contributes `N^10 eta_N`, and the reversal
union bound is `O_r(N^4 r^-N)`.  Every term is `o(N^-2)`.  The same
single-active-component estimate applies to the initial internal absorption,
including a center singleton.  Thus all untracked paths have probability
`o(N^-2)`.

The phrase “complement of the coupled direct path” in (32) should be read as
the complement caused by coupling, excursion-tail, or sweep-reversal errors.
The first-stage adverse conversion has probability `Theta(N^-2)` and is
separately retained exactly through `A/(1+A)` in the next display.

### 10. First-stage endpoint coefficients — **PROVED / EXACTLY COMPUTED**

At `r=3/2`, `delta=N^-4`, and total center degree
`Z=(N-1)N^-3`, the audited rate formulas give

\[
A_{B,N}=\frac14N^2(1+o(1)),\qquad
A_{D,N}=\frac{27}{16}N^2(1+o(1)).
\]

Since both module establishment probabilities equal `1/3+O(N^-4)`, this
implies

\[
p_{B,N}=\frac13-\frac{4}{3N^2}+o(N^{-2}),\qquad
p_{D,N}=\frac13-\frac{16}{81N^2}+o(N^{-2}).
\]

Only relative `1+o(1)` control of each odds ratio is needed: inversion turns
it into the stated absolute `o(N^-2)` remainder.  The symbolic certificate
recomputes both constants exactly after the substitution `t=1/N`.

### 11. Center starts and uniform averaging — **PROVED**

For a center singleton,

\[
q_{B,N}=\frac13+o(N^{-2}),\qquad
q_{D,N}=\frac13-\frac{1}{3N}+o(N^{-2}),
\]

from the exact clique formulas.  The center sampling mass is
`h_N=1/(3N+1)`.  Hence its dB correction contributes
`-1/(9N^2)` to the graph average and no order-`N^-2` Bd correction.  Therefore

\[
\rho_{B}(G_N,3/2)=\frac13-\frac{4}{3N^2}+o(N^{-2}),
\]

\[
\rho_{D}(G_N,3/2)=\frac13-\frac{25}{81N^2}+o(N^{-2}).
\]

For `n=N+3N^2`, the complete Bd baseline is `1/3+o(N^-2)`, while the
complete dB baseline is `1/3-1/(9N^2)+o(N^-2)`.  Subtraction gives exactly

\[
-\frac{4}{3N^2}+o(N^{-2})\quad\text{and}\quad
-\frac{16}{81N^2}+o(N^{-2}).
\]

Thus the endpoint suppression claim and the assertion that `(1,3/2)` is the
exact open amplification interval of this particular family are
**PROVED**.

### 12. Editorial consistency — **ERROR, TRIVIAL REPAIR**

After adding the endpoint theorem, the opening paragraph still said “No claim
is made at the endpoint `r=3/2`.”  This contradicts (2a) and Section 8 and
should be deleted or changed to say that the endpoint is explicitly
suppressed.  It has no mathematical effect.
