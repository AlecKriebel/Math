# Independent proof audit of the physical hard 188 composition

**Verdict (2026-08-12 PDT): STRICT PASS at the stated local physical
two-active scope.**  The theorem is a disjoint case composition of two
already audited analytic stopped-block theorems.  No orientation or history
space is enumerated, and no pair or global claim is promoted.

The frozen composition targets are

```text
note    fc9f1b9039fe1cf416c2d346799465c4a16c0c84e5cde85b6d1168d1355d89f4
source  9be690af29127013613d6d5f3d482943f51248d37da9d4af21c2b44cda1c0b65
tests   39f71e131532303015544de75023bc58b34803edf1c19891e964c69cacb727ac
```

All eight analytic input hashes recorded by the source match their current
bytes.  In particular, the exact-19 theorem and the nonexact-169 corollary
have strict independent PASS verdicts at the hashes frozen by the
composition.

## 1. The partition is exact and is the only finite input

Every hard row has a unique normalized relabelling

\[
 U=\text{lower-weight active species},\qquad
 V=\text{higher-weight active species},\qquad
 I=\text{inactive species},
\]

because its two positive descriptor weights are strictly ordered.  The
linkage containing $VI=V+I$ is the normalized proper linkage.  Define an
exact template to be one for which this linkage is precisely

\[
                         \{aU,VI\},\qquad a\in\{0,1,2\}.
\]

This predicate and its negation are disjoint by definition.  Applied to the
canonical physical hard table, they give 19 exact and 169 nonexact
templates.  Their union equals the complete set returned by the independent
407-incidence selector after normalization:

\[
188=19+169,
\]

with category split

\[
19\ \text{exact},\quad145\ \text{mixed},\quad
8\ \text{separated},\quad16\ \text{no-history}.
\]

The ratio histogram is

\[
(1,2):17,\qquad(1,3):154,\qquad(4,5):17.
\]

The 188 normalized templates represent all 407 physical incidences.  Their
multiplicity histogram is 17 templates used once, 147 used twice, and 24
used four times, so

\[
                     17+2(147)+4(24)=407.
\]

Coordinate relabelling and repeated use do not add an analytic hypothesis:
both input theorems are invariant under relabelling and quantify over the
actual fixed orientation and rate vector.  The executable checks only these
support identities, ratios, and frozen hashes; it does not infer a Markov
estimate from the finite table.

## 2. Exact-19 quantifiers and endpoint

The exact theorem assumes

\[
 U=s^{p+o(1)},\qquad V=s^{q+o(1)},\qquad I=0,
\]

the proper pair $\{aU,VI\}$, an arbitrary fixed strong orientation on both
linkages, arbitrary fixed positive rates, and an arbitrary fixed correction
$\ell$.  These are exactly the ambient hypotheses of the composition.
The nineteen finite premises supply $q-pa\ge1$, the allowed lower-complex
universe, and the exact entropy-maximizer alternatives.

The theorem retains the reversible carrier, every lower clock, and the
actual boundary-causing reaction.  In the eighteen singleton-maximizer
templates, the leading clean macro is strict.  In the unique two-source
equality template, the independently audited killed exponential Green
block supplies an integrable positive overshoot and a strict terminal cut;
no pathwise sign is imported.  At its physical stop,

\[
 \mathbb E\Delta G_\ell\le-c\log s,\qquad
 \mathbb E|\Delta G_\ell|^r=O(\log^rs),\qquad
 \mathbb E\sigma^r=s^{o(1)}
\]

for every fixed $r$.  The exact fourth-power expansion, including the raw
duration term, is already part of that audited theorem:

\[
 \mathbb E[W_\ell(X_\sigma)-W_\ell(X_0)+\sigma]
 \le-cG_\ell(X_0)^3\log s.                         \tag{2.1}
\]

Thus the composition neither re-proves nor weakens the exceptional-shell
overshoot obligation.

## 3. Nonexact-169 quantifiers and endpoint

The nonexact corollary has the same ambient physical hard menu, start,
orientation, rate, and arbitrary fixed-$\ell$ quantifiers.  Relative to
that ambient menu, the maximal base complex is $dU$, $d\in\{1,2\}$, and
all 169 rows obey

\[
                            q-pd\ge1.
\]

The 145 mixed rows use the audited one/two-window Schur macro.  The eight
separated rows use one clean carrier window and its geometric exact-return
inverse.  In the sixteen no-history rows, the $VI$ linkage is disabled on
$I=0$ and the first dominant nonself reaction in the base-only linkage is
an immediate base descent.  The independent corollary audit verifies that
these are analytic specializations, not conclusions drawn from their
category names.

Every exact retry retains its physical holding time.  A subdominant
initiator or dirty-window reaction is itself the included endpoint, and its
endpoint-weighted probability is $s^{-1+o(1)}$.  Regular separated and
no-history endpoints are actual no-fast bases; the mixed theorem likewise
returns the actual physical terminal population.  For every fixed $r$ the
needed increment and duration moments hold, and the audited corollary
already proves

\[
 \mathbb E[W_\ell(X_\sigma)-W_\ell(X_0)+\sigma]
 \le-cG_\ell(X_0)^3\log s.                         \tag{3.1}
\]

No historical debt hypothesis from the generalized one-active problem is
present or needed here: both active populations are macroscopic, and the
sixteen no-history rows descend directly in the base-only linkage.

## 4. Why the common-potential composition is literal

The composition selects one of (2.1) and (3.1) from the support predicate
at the initial descriptor.  It does not concatenate the two blocks, compare
two Lyapunov functions, or restart from an artificial state.  Both inputs
use the same physical state function

\[
 G_\ell=K_\ell+\sum_i\log(X_i!)+\ell\cdot X\ge1,
 \qquad W_\ell=G_\ell^4,
\]

for the same arbitrary fixed $\ell$.  Their terminal populations are
therefore immediately eligible for descriptor reclassification with no
endpoint conversion toll.  Constants may depend on the selected finite
template, strong orientation, rates, and $\ell$, as allowed by the local
theorem, but not on $s$.

The exact branch has $s^{o(1)}$ fixed duration moments and the nonexact
branch has bounded fixed duration moments.  “Arbitrary fixed duration
moments” in the composition means these inherited asymptotic bounds; it
does not assert a stronger uniform bound on the exact branch.  Both inputs
have already shown that their duration is lower order than the negative
fourth-power term.

Consequently every one of the 188 normalized physical templates, and hence
every one of the 407 physical hard incidences represented by them, has the
claimed raw physical stopped block for every strong orientation, every
fixed positive rate vector, and every fixed correction $\ell$.

## 5. Reproduction and claim boundary

The four composition tests and eighteen focused dependency tests pass.  The
composition reproduces

```text
rows     5295c9952f54069dc4337155aec8391fc09abc2b7e5aaf4b2650cf4036ae2ddc
payload  2152dcd4bbe64f08032ec576e126bc8213c3840b642fd15a2e7866a881e4ed0e
```

The frozen note has one non-load-bearing TeX typo in (3.1):
`\mathbb E_x\!left[` should read `\mathbb E_x\!\left[`.  This should be
repaired in the publication copy, but the surrounding display and theorem
unambiguously state the intended expectation and it does not affect the
strict analytic verdict.

The executable correctly leaves
`physical188_composition_independently_audited`,
`pair_recurrence_certified`, and `global_t3_2_certified` false.  This audit
certifies only the local physical-188 composition; changing a frozen flag
or promoting support pairs requires a separate composition step.
