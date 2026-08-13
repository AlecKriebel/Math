# Independent exact-byte hostile audit: homogeneous carrier/dyadic macro

**Audit date:** 2026-08-12 PDT.

## 1. Immutable target and strict verdict

This audit pins exactly

~~~text
research_notes/proof_first_h111_two_carrier_dyadic_all_lower_supports_theorem.md
SHA-256 f4d8cc40ccea1c6d9e0df9302f75c8cc1d58dd7c89669fd19ad48fc4bca735b0
499 lines / 20,690 bytes
~~~

The target remained unchanged throughout this replay.

> **STRICT PASS.**  For its literal rank-two two-carrier and dyadic support
> families, the target proves an all-clock stopping macro with uniformly
> bounded expected physical duration and birth debt, independent of the
> subsequently chosen direct-death threshold (L).  It covers every allowed
> two- or three-unary lower support, arbitrary strongly connected labelled
> orientations, and arbitrary fixed positive rates.  No orientation, rate,
> population box, or stochastic history is enumerated.

This is an activation-or-ledger theorem.  It does not itself prove the
separate activated-shell service theorem or the finite support identity
(360=168+144+48).

## 2. Exact support scope and the rank-one obstruction

After relabelling the dead pure vertex as (X), the target assumes


\[
  2X\notin T,\qquad \dim\operatorname{span}(T-T)=2.                 \tag{2.1}
\]

The two-carrier case contains (X+Y,X+Z), and (2.1) forces at least one
additional vertex.  The dyadic case is exactly

\[
 T=\{X+Y,2Z\}\cup Q,
 \qquad\varnothing\ne Q\subseteq\{Y+Z,2Y\}.                       \tag{2.2}
\]

The nonempty condition is necessary.  With
(T=\{X+Y,2Z\}), (R=\{0,Y,Z\}), and initial population
((N,0,0)), the rank-one top linkage preserves (2Y+Z), leaves (X)
frozen, and gives no population-uniform activation estimate.  The frozen
target explicitly excludes this witness and uses rank two precisely where
the carrier set or the dyadic pair must have a strict upper exit.

## 3. Workload identity, disjoint endpoints, and (L)-independent debt

For (H=X+Y+Z), every top reaction and every nonzero unary transfer is
(H)-neutral.  Hence the pathwise identity

\[
                         H_t-H_0=B_t-D_t                             \tag{3.1}
\]

is exact.  Small normalized transverse wedges about distinct dead pure
vertices have disjoint compact closures.  Since every reaction displacement
is bounded, the first physical exit from the (X)-wedge lands in the common
activated complement outside one finite population set.

The proof first constructs a base time \(\sigma_\infty\), stopped only at
fractional workload return or wedge exit, with

\[
 \sup_x\mathbb E_x\sigma_\infty<\infty,
 \qquad
 \sup_x\mathbb E_xB_{\sigma_\infty}<\infty.                       \tag{3.2}
\]

Every direct-death clock is live in this construction.  Only afterward does
it put \(\sigma_{x,L}=\sigma_\infty\wedge\rho_L\), where \(\rho_L\) is
the actual (L)-th direct death.  Therefore the constants in (3.2) are
independent of (L).  The endpoint priority (F>D>I) makes fractional
return, (L)-death, and activated exit disjoint even when one physical jump
has more than one property.

If (X\to0) is present, \({\cal L}H\le\beta-cH\) until the favorable
stop proves (3.2) directly.  Otherwise every (X)-sourced lower event is a
transfer to (Y) or (Z) and has favorable transverse sign.  Thus no
order-(H) lower clock is hidden in a bounded perturbation.

## 4. Literal finite establishment

### 4.1 Two carriers

The killed two-state carrier graph supplies the positive transverse height
\(S=v_Y Y+v_Z Z\).  At \(S=0\), either a favorable \(X\)-source transfer
seeds at rate \(cX\), or the lower support is \(\{0,Y,Z\}\) and a
zero-source birth seeds at fixed positive rate.  On the fixed phase
\(0<S<K\), with
every clock retained,

\[
                    {\cal L}S\ge cH_0S,
             \qquad \Gamma S\le CH_0S.                             \tag{4.1}
\]

A small exponential test bounds the return-to-zero probability away from
one.  Stopped Dynkin for bounded \(S\) gives \(O(H_0^{-1})\) expected trial
time.  Geometric reseeding therefore has bounded mean duration and birth
count; it is not a conditioned slow reaction word.

### 4.2 Dyadic support with \(X\) in the lower linkage

Every \(X\)-sourced lower event raises \(S=2Y+Z\), at aggregate rate at
least \(cX\).  On \(S<K\), all height-lowering clocks have bounded aggregate
rate.  Fast height-neutral top firings remain active but do not alter the
good-versus-adverse race.  A fixed number of favorable \(X\)-source events
therefore establishes \(S\ge K\) with uniform positive probability and
\(O(H_0^{-1})\) expected physical time.

### 4.3 Dyadic support with lower set \(\{Y,Z\}\)

The transverse phase below \(K\) is finite after contracting only the
order-\(H\) events from \(B=X+Y\).  A \(B\to A=2Z\) event is height-neutral
and consumes a \(Y\), so at most \(K\) consecutive contracted neutral events
occur before strict progress or \(Y=0\).  At the zero phase a lower birth
seeds \(Y\) or a lone \(Z\); a lone \(Z\) can be lost and restart, move to
\(Y\), or receive the second \(Z\) required to enable \(A\).

Once \(A\) is enabled, the internal pair \(\{A,B\}\) cannot be closed in
the strong top graph because \(Q\ne\varnothing\).  A strict outgoing label
therefore exists at \(A\) or \(B\), with fixed positive same-source label
probability.  The resulting finite quotient has no closed unsuccessful
class.  Finite minorization followed by geometric renewal yields the stated
mean establishment bounds without assuming a population-dependent slow
word.

## 5. Two-carrier multiplicative ascent and the repaired time sign

Killing the top graph when it leaves the two carrier sources gives a
transient subgenerator \(Q\).  With

\[
 g=(-Q)^{-1}{\bf1},\qquad
 S=(1-\epsilon g_Y)Y+(1-\epsilon g_Z)Z,                         \tag{5.1}
\]

the exact source rewards give

\[
 {\cal L}_TS\ge cXS-CS^2.                                      \tag{5.2}
\]

All \(X\)-source lower transfers are favorable, while the remaining lower
drift and variance are absorbed once \(K\le S<\varepsilon_0H\).  Therefore

\[
                 {\cal L}S\ge cHS,
             \qquad\Gamma S\le C'HS.                            \tag{5.3}
\]

The exponential test makes a downward band exit exponentially unlikely.
The load-bearing time estimate has the correct sign: the proof uses a
bounded full-process function \(f_r\) equal to \(\log S\) on the band and
its complete one-jump enlargement.  Thus before stopping

\[
             {\cal L}f_r={\cal L}\log S\ge cH\ge cr.              \tag{5.4}
\]

The stopped endpoint oscillation of \(f_r\) is bounded, so Dynkin gives
\(\mathbb Et_r\le C/r\).  No invalid killed-logarithm or cemetery-value sign
is used.  Both the error probabilities and times are summable over doubling
bands.

## 6. Dyadic source balance with live bulk lower clocks

In a band \(r/2<S<2r\le2\varepsilon_0H\), the two minimum-height source
rates satisfy

\[
 \lambda_{\min}=a_AZ(Z-1)+a_BXY\ge cr^2.                         \tag{6.1}
\]

Optional high-source events, (Y/Z)-source lower events, deaths, and births
have relative probability at most \(C(\varepsilon_0+r^{-1})\).  Potentially
order-\(H\) \(X\)-source lower events are not put in that error; they are
counted as favorable events \(g\).

On a prefix that stays in the band, bounded height variation gives the exact
ledger

\[
                              g+c_*\le Cr+Ce.                       \tag{6.2}
\]

If one minimum source lacks a strict outgoing cut, its repeated firings
consume its transverse reactant, and the other source must have a strict cut
by strong connectivity and (2.2).  The two source balances imply that,
after an \(O(r+e+g)\) debit, a fixed fraction of minimum-source firings occur
at a direct-cut source.  Substituting (6.2) reduces this debit to \(O(r+e)\).
At each such source, a strict label has a fixed conditional probability.

Two adaptive Chernoff estimates now show that a prefix of \(L_0r\) actual
reactions exits upward except with probability \(Ce^{-cr}\); a lower exit
would require \(cr\) adverse height loss and has the same bound.  The expected
reaction count is \(O(r)\), while (6.1) makes each conditional holding time
at most \(C/r^2\), so again \(\mathbb Et_r\le C/r\).  This argument keeps
direct deaths and all bulk (X)-source clocks active.

## 7. Stopping times, nonexplosion, and exact handoff

Every establishment and band block stops at an actual physical endpoint.
Zero-length classifier handoffs are concatenated and are not counted as
episodes.  Since top reactions and nonzero unary transfers preserve (H),
pathwise

\[
                             H_t\le H_0+N_t,                       \tag{7.1}
\]

where (N_t) is the constant-rate birth Poisson process.  Population and
all binary hazards are consequently bounded on each finite physical-time
interval, proving nonexplosion.  Localization, stopped Dynkin, and the birth
compensator are therefore legitimate, and

\[
       \mathbb EB_{\sigma_\infty}
          =\beta_0\mathbb E\sigma_\infty\le C.                     \tag{7.2}
\]

The theorem provides exactly the activation-or-death ledger required by the
later workload-only Foster composition.  An \(F\)-endpoint has
\(D-B\ge H_0/2\); a \(D\)-endpoint has \(D\ge L\); an \(I\)-endpoint lies in
the common activated region.  Because the expected birth debt is independent
of \(L\), the composition may choose \(L>C\) afterward.  No additional
recurrence or service claim is silently imported.

## 8. Reproduction and render

The target SHA-256, line count, byte count, and visible control-byte scan
were independently replayed.  Pandoc and Tectonic produced clean
letter-paper PDFs for both target and audit.  Every page was rasterized and
visually inspected for clipping, overlap, malformed equations, broken code
blocks, and missing glyphs.  No mathematical, exact-byte, or rendering
obstruction remains.

> **FROZEN VERDICT: STRICT PASS.**
