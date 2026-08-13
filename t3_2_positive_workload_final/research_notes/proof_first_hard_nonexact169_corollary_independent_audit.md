# Independent proof audit of the nonexact-169 corollary

**Verdict (2026-08-12 PDT): PASS in its stated physical-hard-menu scope.**
No orientation enumeration is used below.  The theorem, pair, and global
certification flags remain false.

The frozen inputs audited here are

```text
corollary  734f4cc3b0732b97c361100f2375c5b36a757da8926446c738dfdeef66130645
source     e34038585e738a42fce5a6587e578f28fe8b570c18c376e1394bf8e5791554a4
tests      219855ff45ee0647291fed0c4981d9cd433ca94ec8a40fd3887c8253f843ff61
base proof d53772170088cccbacc7a0911b6a71e05ad6cbe856fbaddf8858769d19805714
```

The phrase “uses only” in the corollary is read relative to the ambient
physical hard menu inherited from the base proof: (V) occurs only in
(C=V+I), the remaining complexes are in
({0,U,2U,I,2I,U+I}), the two displayed linkage supports carry fixed
strong digraphs with fixed positive rates, and the start is
(U=s^{p+o(1)},V=s^{q+o(1)},I=0).  The four listed premises are the only
additional support facts needed after those ambient hypotheses.  They would
not, by themselves, be axioms for an unrestricted reaction network.

## 1. The eight separated rows

Write (L_+) for the linkage containing (C).  In a separated row,

\[
 L_+\setminus\{C\}\subset\{0,U,2U\},\qquad
 L_-\subset\{I,2I,U+I\},
\]

and the maximal base (dU), (d\in\{1,2\}), lies in (L_+).  At an
(I=0) base only base sources are enabled.  If
(lambda_d(u)) is the aggregate rate of the non-null edges sourced at
(dU), strong connectivity gives

\[
 lambda_d(u)=k_d(u)_{\underline d},\qquad k_d>0,
\]

whereas the aggregate rate of all lower-degree base sources is at most
(C(1+u^{d-1})).  Consequently

\[
 \Pr\{\hbox{a lower-degree source fires first}\}
       =O(u^{-1})=O(s^{-p+o(1)}).                    \tag{1.1}
\]

On a (dU\to C) opening the state is
((u-d,v+1,1)).  The (C)-clock is at least (cv), while every other
enabled clock together is at most (C(1+u^d)).  Hence

\[
 \Pr\{\hbox{a non-}C\hbox{ insertion before the }C\hbox{ firing}\}
       =O(u^d/v)=O(s^{pd-q+o(1)})=O(s^{-1+o(1)}).     \tag{1.2}
\]

There is only one clean fast window in a separated row.  A clean
(C\to dU) firing is an exact return of the complete physical state.  Any
other clean outcome is a base (cU) with (c<d).  Moreover, exact returns
cannot trap the trace.  If (dU) has an edge to a base outside
({dU,C}), it is already a fixed-probability nonself outcome.  Otherwise
strong connectivity forces an edge from (C) to a base outside that set.
Because (L_+\ne\{dU,C\}), one of these alternatives holds.  Conditional
target probabilities are fixed positive rate ratios, so, for all large
(s), each visit to the original base has probability at least
(eta>0), independent of (s), of a clean nonself exit.  The number of
exact returns is therefore dominated by a geometric random variable with
all fixed moments.

This gives an explicit physical stopping rule: retain exact-return holding
times and restart after each exact return; stop at the first clean nonself
outcome, the first lower-degree initiation, or the first included non-(C)
insertion.  Equations (1.1)--(1.2), summed over the geometric number of
attempts, show that the last two exceptional alternatives have probability
(O(s^{-1+o(1)})).  Exact retries reset the physical population, and a
terminal attempt has only a bounded number of reactions.  Thus all
population increments are bounded and, for every fixed (r),

\[
 \mathbb E[(1+|\Delta U|+|\Delta V|+I)^r;
             \hbox{exceptional endpoint}]=O(s^{-1+o(1)}).     \tag{1.3}
\]

In particular, an (I\ge K\log s) boundary is never reached for large
(s); the carrier-tail part of the mixed proof is vacuous here.

At every regular endpoint (V) is unchanged, (I=0), and
(U'=U-d+c) for some (c<d).  For the corrected factorial potential,

\[
 \Delta G_\ell
   =\log((u-d+c)!)-\log(u!)+O_\ell(1)
   =-p(d-c)\log s+o(\log s).                         \tag{1.4}
\]

Thus the regular decrement is uniformly strict.  The exceptional endpoint
has (|\Delta G_\ell|=O(\log s)), so (1.3)--(1.4) imply

\[
 \mathbb E\Delta G_\ell\le-c\log s,qquad
 \mathbb E|\Delta G_\ell|^r=O(\log^r s).             \tag{1.5}
\]

The base holding rate is at least (cu^d), the open holding rate is at
least (cv), and the retry count has geometric moments.  A random-sum
estimate therefore gives every fixed physical-duration moment (indeed a
bound stronger than (O(1))).

## 2. The sixteen no-history rows

Here

\[
 L_+\setminus\{C\}\subset\{I,2I,U+I\},\qquad
 L_-\subset\{0,U,2U\},
\]

and (dU) lies in the base-only linkage (L_-).  The entire (L_+)
linkage is disabled at (I=0).  As before, the degree-(d) clock is
(k_d(u)_{\underline d}) and all lower-degree clocks total
(O(1+u^{d-1})), giving (1.1).  After physically null self labels are
discarded, every edge sourced at the unique maximal base (dU) has target
(cU) with (c<d); strong connectivity guarantees at least one such
edge.  Hence the first degree-(d) firing is already the regular direct
descent (1.4).  Stop at that firing or at the first lower-degree firing.
There is no carrier window, no dirty insertion, and no exact physical
retry.  The same calculations prove (1.3)--(1.5) and all fixed duration
moments.

## 3. Fourth-power lift

At either kind of start,

\[
 g:=G_\ell(X_0)=s^{q+o(1)}\log s,
\]

because (q>p).  With (H=\Delta G_\ell), (1.5) and the exact identity

\[
 (g+H)^4-g^4=4g^3H+6g^2H^2+4gH^3+H^4
\]

give

\[
 \mathbb E[(g+H)^4-g^4]
 \le -c g^3\log s+O(g^2\log^2s+g\log^3s+\log^4s)
 \le-c' g^3\log s.
\]

The (O(1)) mean duration is negligible on this scale.  Therefore the
stopped physical episodes in both additional categories satisfy the exact
claimed (W_\ell=G_\ell^4) inequality, with the same fixed correction
(\ell), along with all required increment and duration moments.  Their
regular endpoints are no-fast bases and so have the required
same-potential reclassification interface.

## 4. Finite replay and claim boundary

The finite replay passed all four tests.  It verifies only the inherited
complex universe, the nonexact split

\[
169=145+8+16,
\]

and (q-pd\ge1) (153 rows of gap one and 16 of gap two).  It is not used
for the orientation-uniform argument above.  The certificate deliberately
keeps `corollary_independently_audited`, `pair_recurrence_certified`, and
`global_t3_2_certified` false.  This audit validates the local analytic
corollary only; composition remains a separate gate.
