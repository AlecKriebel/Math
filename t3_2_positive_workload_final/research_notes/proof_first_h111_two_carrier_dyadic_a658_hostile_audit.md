# Hostile audit of the homogeneous carrier/dyadic candidate at `a658899...`

**Independent proof-first audit, 2026-08-12 PDT.**  The exact target of this
audit is

~~~text
research_notes/proof_first_h111_two_carrier_dyadic_all_lower_supports_theorem.md
a65889914cf988c26301cea0fedd75951f4e9b68ecc71c0c252bbe505e9db192
~~~

The verdict on these bytes is **FAIL, repairable**.  The killed-carrier
ascent, dyadic band balance, wedge geometry, and (L)-independent workload
truncation pass.  The theorem statement omits a necessary rank hypothesis,
and its finite-establishment paragraph does not yet justify a uniform
all-clock trial.

## 1. Literal scope counterexample

The opening permits "any subset" of the optional dyadic vertices, hence the
empty subset.  Take


\[
             T=\{X+Y,2Z\},\qquad R=\{0,Y,Z\},
\]

with both labelled graphs strongly connected, arbitrary positive rates, and
initial population ((X,Y,Z)=(N,0,0)).  The top linkage has rank one and
preserves (S=2Y+Z).  The lower (Y,Z) immigration/transfer/death system is
independent of the frozen bulk coordinate (X=N) and has an (O(1))
positive recurrent scale.  Thus neither (H\le H_0/2) nor
(S\ge\varepsilon H) has a uniformly bounded mean hitting time as
(N\to\infty).  The asserted uniform base time (1.6) is false in this
literal scope.

The proof itself invokes rank two in Sections 2 and 3.  The repair is to
assume explicitly

\[
                    \operatorname{rank}\operatorname{span}(T-T)=2.
\]

For the dyadic support this forces at least one of (Y+Z,2Y); for the
two-carrier support it forces a vertex outside \(\{X+Y,X+Z\}\).

## 2. Missing uniform establishment argument

Lines 136--171 pass directly from a prescribed support path to
"finite-state geometric repetition."  That inference is not literal under
all clocks.  For example, an enabled slow (2Z) or other pure source can be
preempted with probability tending to one while an (O(H)) carrier remains
enabled.  Such a fast firing may be favorable, but it must be contracted or
charged; it cannot simply be called a fixed-probability deviation from a
slow prescribed word.

A sufficient repair is the following exact split.

1. If (X\in U) and \(\delta_X=0\), some (X\)-sourced lower transfer has
   rate at least (cX), every (X\)-sourced transfer raises the chosen
   transverse height, and all adverse lower/birth clocks have rate
   (O_K(1)) while (S<K).  Before wedge exit or (F), (X\ge cH).
   Therefore (K) favorable increments occur with a uniform trial
   probability and uniform mean time.  No slow top word is needed.
2. If (X\notin U), then (U=\{Y,Z\}).  On (S<K), quotient out only the
   (H)-fast carrier firings.  The remaining transverse states and phases
   form a finite chain.  Strong connectivity must be used to prove that it
   has no closed unsuccessful class.  In the dyadic lone-(Z) phase one
   must retain the (Z\to Y) alternative or a second tagged (Z) arrival;
   at (2Z), internal (2Z\leftrightarrow X+Y) moves are included in the
   finite contraction until a strict-height edge, structural exit, or reset
   occurs.  This gives the required uniform minorization and holding-time
   bound without suppressing any clock.

## 3. Parts that pass

The repaired two-carrier logarithmic time proof is correct.  The bounded
extension (f_r) agrees with \(\log S\) on the one-jump enlargement, so
Dynkin uses the full generator rather than a killed function.  From

\[
               \mathcal L f_r\ge cH\ge cr
\]

and a uniformly bounded endpoint oscillation one obtains
(\mathbb E t_r\le C/r) with the right sign.

The optional-support dyadic proof also passes.  Minimum-source rate
(\lambda_{\min}\ge cr^2) is exact on the band.  High-source,
(Y/Z)-sourced lower, death, and birth events have relative bad rate
(C(\varepsilon_0+r^{-1})).  The possibly order-(H) (X)-source transfers
are retained as good events.  On a no-exit prefix the height ledger gives
(g+c_*\le Cr+Ce); substitution into the two source-balance inequalities
leaves a fixed fraction of direct-cut opportunities.  The two adaptive
Chernoff bounds therefore prove (4.11), and the aggregate minimum clock gives
(\mathbb E t_r\le C/r).  No orientation or reaction history is enumerated.

Finally, the disjoint normalized wedge construction is sound: before (F),
the population is uniformly large, so a bounded jump leaving one sufficiently
small wedge cannot enter another.  The base stop \(\sigma_\infty\), followed
only afterwards by truncation at the (L)-th actual death, makes both mean
time and birth debt independent of (L).  The terminal priority
(F>D>I) resolves simultaneous labels correctly.

## 4. Disposition

Do not cite or freeze the target at `a658899...`.  A derivative which adds
the rank-two hypothesis and proves the two finite-establishment branches
above can inherit all later sections without changing their mathematics.
