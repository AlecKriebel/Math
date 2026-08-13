# Independent audit of the repaired normalized-phase terminal theorem

**Hostile proof audit, 2026-08-12 PDT.**  The immutable target of this
audit is

`proof_first_separated_normalized_phase_marked_terminal_repair.md`

at SHA-256

`149c2edd9a8427a442a66e4f99c026be96313bfc4e5072f96d0aa380502ffa77`.

The target was not edited during this audit.  No support, orientation,
reaction word, or population range was enumerated.

**Verdict: STRICT PASS.**  Under the hypotheses stated in Section 1 of
the target, the three boxed estimates (3.4), (4.1), and (5.5) follow from
the cited clean-base and open-phase inputs.  The direct-base first mark,
the terminal priority, the completed-base guard, the case (p=0), and an
open crossing which lands directly at (C=0) are all accounted for.
Duration and the fourth-power lift are, as stated, outside this verdict.

## 1. The stopping partition is exact

Give the open boundary (B_O) first priority.  Among paths which have not
hit (B_O), give a clean return with (k\ge1) the label (S), and a
return following a first lower-sourced open reaction the label (E).
Only a continuing, unmarked clean return with (k=0) is tested against
the base guard (B_0).  These rules make

\[
                         B_O,\quad B_0,\quad S,\quad E       \tag{1.1}
\]

disjoint physical terminal events.  In particular, a long service or
marked genealogy is never relabelled by the narrower base guard.

Let (Q) retain the physical clean prefix and kill on the four terminal
labels.  Restrict the first-mark operator to causing reactions which do
not cross (B_O), and split it into (R_B), which itself lands at a
base, and (R_O), which remains open.  Let (K_{OO}) be the full
post-mark physical open kernel, killed at its next base or (B_O), and
let (T_{OE}) be its exit to a base without an earlier boundary hit.
Then the (E)-kernel is exactly

\[
       (I-Q)^{-1}\{R_B+R_O(I-K_{OO})^{-1}T_{OE}\}.           \tag{1.2}
\]

There is no continuation after the base endpoint in (1.2).  A mark which
crosses (B_O), and the complementary post-mark exit
(R_O(I-K_{OO})^{-1}T_{O\partial}), belong to (B_O).  Thus (1.2)
neither omits a direct return such as (C\to0), nor counts a
boundary-causing mark as (E).  This repairs the two possible failures of
the unqualified expression (R(I-K_{OO})^{-1}).

## 2. Normalization and the marked transform

At an open phase (s), the target uses

\[
 V_\theta(x,s)=e^{\theta G_\ell(x)}
       \left\{\frac{M_x(dB)}{M_x(s)}\right\}^{\theta}.       \tag{2.1}
\]

Multiplying the audited phase weight by (M_x(dB)^\theta) changes a
one-reaction ratio by a bounded constant because a binary reaction changes
(B) by at most two.  The audited phase table therefore gives

\[
 \frac{\lambda_{yz}(x)}{\lambda_{\rm tot}(x)}
 \frac{V_\theta(x+z-y,s')}{V_\theta(x,s)}
 \le
 \begin{cases}
 Cr_y^{1-\theta}r_s^\theta,&y\ne q,\\
 Cr_s^\theta,&y=q.
 \end{cases}                                                \tag{2.2}
\]

The pre-boundary ratios satisfy (r_y\le C\bar\delta).  Hence a first
lower-sourced mark costs (C\bar\delta^{1-\theta}).  After it, a lower
phase has row norm (O(\bar\delta^\theta)); a (q)-phase has only one
free (q)-exit, which sets a lower phase.  Pairing steps yields

\[
 \|K_{OO}^2\|_{V_\theta}\le C\bar\delta^\eta,
 \qquad \|(I-K_{OO})^{-1}\|_{V_\theta}\le C.               \tag{2.3}
\]

The exit row has bounded corrected norm.  Combining (1.2), (2.2),
(2.3), and the clean-prefix Green bound gives corrected mass
(C\bar\delta^{1-\theta}).  At both the entrance and every (E)-endpoint
(C=0), and the weight (2.1) is defined to be exactly (e^{\theta G_\ell}).
Thus no terminal divisor or unweighted spectator moment occurs, and

\[
 \mathbb E_x[e^{\theta\Delta G_\ell};E]
 \le C\bar\delta^{1-\theta}
 \le Ce^{-\eta h/2}.                                       \tag{2.4}
\]

This also proves (2.4) for the (R_B) term without inserting a fictitious
open continuation.

## 3. The clean-service factor is genuinely raw

The phase table alone would not prove the asserted gap at a service
endpoint; the completed-return ledger is essential.  For a clean macro
sourced at (cB), it gives

\[
                    B_\tau-b\le pk+(d-c),\qquad k\ge1.      \tag{3.1}
\]

The base source probability contributes
(C(1+b)^{c-d}).  Split a possible positive spectator displacement into
the first (d-c) molecules and the at most (pk) service-associated
molecules.  The first part, together with the source probability, costs at
most

\[
                         C(1+b)^{-(1-\theta)(d-c)}\le C.     \tag{3.2}
\]

For the remaining part, the active factorial quotient supplies
((a)_{\underline{k}}^{-\theta}), while before the included boundary
((1+B)^p\le Cc_0\bar\delta a).  Taking (c_0) sufficiently small to
absorb the fixed linear-correction constants gives

\[
 (a)_{\underline{k}}^{-\theta}(1+B)^{\theta pk}
                       \le C\bar\delta^{\theta k}.           \tag{3.3}
\]

For (p=0), there is no spectator factor and the active factorial loss is
stronger than (3.3).  Equations (3.1)--(3.3) are precisely the audited
completed-service marked estimate, now used at a weight which is raw at
the base endpoint.  Summing the bounded clean Green and taking (k\ge1)
therefore gives

\[
 \mathbb E_x[e^{\theta\Delta G_\ell};S]
       \le C\bar\delta^\theta\le Ce^{-\eta h/2}.             \tag{3.4}
\]

Thus the target does not rely merely on the informal phrase “one nonfree
(q)-step”; its explicit ledger import supplies the load-bearing raw
factor.

## 4. Completed-base guard upcrossing

Assume (p\ge1), and write

\[
 R_a=\left(\frac{c_0}{2}\bar\delta a\right)^{1/p}.          \tag{4.1}
\]

At the entrance, (b^p\le\epsilon a), whereas
(R_a^p=(c_0/2)\epsilon^{1/2}a).  Consequently
(b/R_a\to0).  After literal self-returns have been contracted, every
continuing clean (k=0) return changes (B) by at most two.  Reaching
(B_0) hence requires at least (cR_a\ge cL) contracted returns.

For the same raw exponent, a maximal-degree nonself return decreases
(B) and costs (O((1+B)^{-\theta})).  An upward return from degree
(c<d) has bounded rise at most (d-c), while its source probability
times raw factorial ratio is

\[
                       O((1+B)^{-(1-\theta)(d-c)}).          \tag{4.2}
\]

The literal-return diagonal inverse is uniformly bounded by the strong
cut.  The finite compact killed kernel is absorbed by the bounded clean
Green corrector.  Thus, for a weight \(\widehat V\asymp e^{\theta G_\ell}\),
the contracted continuing kernel satisfies

\[
                         Q_0\widehat V\le\rho\widehat V,
                         \qquad \rho<1.                     \tag{4.3}
\]

The terminal guard-return row has bounded same-exponent norm by the same
ledger.  Summing it after at least (cL) continuing returns, and using
the two-sided bounded comparison between \(\widehat V\) and the raw
weight, proves

\[
 \mathbb E_x[e^{\theta\Delta G_\ell};B_0]
                         \le C\rho^{cL}.                    \tag{4.4}
\]

This argument permits arbitrary lower-degree upward moves; bounded jumps
plus the global corrected contraction, rather than monotonicity of every
return, produce (4.4).

## 5. Open-boundary paths, including a base landing

Every opening occurs below half the spectator threshold.  A base launch
changes each coordinate by at most two.  Therefore a path to the spectator
part of (B_O) needs (\Omega((\bar\delta a)^{1/p})) open reactions.
The carrier and active parts respectively need
(\Omega(\bar\delta a)) and (\Omega(a)) reactions.  In all cases the
number is at least (cL).

The first and terminal rows have bounded corrected norm.  Pairing the
interior reactions by (2.3) therefore gives

\[
 \mathbb E_x\!\left[
       \frac{V_\theta(X_\tau,s_\tau)}{V_\theta(x)};B_O
                    \right]
       \le C(C\bar\delta^\eta)^{cL/2}.                      \tag{5.1}
\]

This argument uses the localized pre-jump state and includes the causing
reaction.  In particular, if a (q\to2B) reaction lands at (C=0) and
crosses the spectator guard, its pre-jump history has already traversed
the required distance.  It is labelled (B_O), not service, mark, or
literal return.  At its base endpoint the normalized-to-raw ratio is one.

At an open crossing endpoint all dynamic coordinates are (O(a)), and

\[
 \frac{e^{\theta G_\ell(X_\tau)}}
      {V_\theta(X_\tau,s_\tau)}
       =\left\{\frac{M_{X_\tau}(s_\tau)}
                        {M_{X_\tau}(dB)}\right\}^{\theta}
       \le Ca^{2\theta}.                                    \tag{5.2}
\]

When (p=0), no complex contains (B); it is constant on the fixed
irreducible class and contributes only a class-dependent constant.  Hence
every fixed polynomial endpoint mark costs a fixed power of (a).
Finally

\[
 \bar\delta a\ge a^{1/2},\qquad
 (\bar\delta a)^{1/p}\ge a^{1/(2p)},
 \qquad L\ge ca^{1/4}.                                     \tag{5.3}
\]

The stretched-exponential bounds (4.4), (5.1) absorb (5.2) and every
fixed polynomial.  Thus, for every fixed (N),

\[
 \mathbb E_x[e^{\theta\Delta G_\ell}P(X_\tau);B]
                         \le C_{N,P}a^{-N}.                 \tag{5.4}
\]

## 6. Scope of certification

The assumptions that an enabled cofactor-free source exists and that
({\cal P}\ne\varnothing) put the target in its stated physical
active-loss branch.  They also make (d) well-defined.  The complementary
fixed-class frozen and (A-C)-invariant alternatives are not silently
claimed here.  Likewise this audit certifies no duration estimate and no
fourth-power Foster lift.

Within that exact scope, no counterexample or unproved endpoint conversion
remains.  The target's raw marked-return, raw service, and polynomially
weighted included-boundary estimates are valid.
