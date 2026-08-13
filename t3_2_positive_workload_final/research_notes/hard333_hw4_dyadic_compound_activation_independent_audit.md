# Independent audit of the dyadic compound-activation route

**Audit date:** 2026-08-11 (America/Los_Angeles)  
**Audited candidate payload:**
`57608cbc0912802e526b5555631ffcfcaacd8eba2c26852439971babf5ea4aa7`  
**Scope:** the exact four hard \(H_w\) pairs selected by
`hard333_pair_composition.hw_switch_pairs()`.

## 1. Strict verdict

The candidate is **PASS**, strictly for the local common-factorial stopped
episode on the exact hard \(H_w\) four.  The exact support relabeling, the
height coordinate, the enumeration of all 1,606 strong digraphs, the
event-skeleton ascent, deterministic service, and common endpoint all pass.
No orientation or positive rate vector was found which contradicts compound
activation.

The preceding payload
`11a9c09fcb9ad032aaebfad1d707d038480777dd9f1b5c7a2e4b87c013dcc04d`
failed as written because it asserted a Green-corrector estimate.  The
audited payload replaces that estimate by the embedded reaction-event
skeleton, exact pathwise balance between the two minimum-height sources, and
adaptive Chernoff bounds proved below.  It also contains the audited
finite-establishment restart and the conditional \(B-D_{\rm win}\)
exponential comparator.

This local pass does not by itself certify the four pair-recurrence rows or
global T3-2.  Those flags remain false pending pair composition and global
verification.

## 2. Exact common parametrization

Write

\[
 A=2P,\qquad B=XU,\qquad H_1=PU,\qquad H_2=2U,
 \qquad R=P+2U.                                      \tag{2.1}
\]

For resistance two, \((P,U)=(C,Y)\); for resistance one,
\((P,U)=(Y,C)\).  The complex heights are

\[
 h(A)=h(B)=2,\qquad h(H_1)=3,\qquad h(H_2)=4.         \tag{2.2}
\]

Consequently every reaction sourced at \(A\) or \(B\) is either a
zero-height reaction between \(A,B\), or a strict cut of reward one or two.
Every reaction sourced at \(H_1,H_2\) changes \(R\) by at most two in
absolute value.  A physical death changes \(R\) by minus one in resistance
two and minus two in resistance one; a physical birth is favorable.

The exhaustive mask replay gives the following direct-cut/zero-edge profile.
Here `direct A` means an edge from \(A\) to \(H_1\) or \(H_2\), and similarly
for \(B\).

\[
\begin{array}{c|c}
\text{profile}&\text{strong digraphs}\\ \hline
\text{both minimum nodes direct}&1234\\
\text{only }A\text{ direct}&186\\
\text{only }B\text{ direct}&186.
\end{array}                                           \tag{2.3}
\]

In every only-\(A\)-direct graph, \(B\to A\) is present.  In every
only-\(B\)-direct graph, \(A\to B\) is present.  This is also immediate from
strong connectivity: a minimum node without a direct cut has only the other
minimum node available as its first step out.

Splitting further according to the optional reverse zero edge gives the
exact histogram

\[
\begin{array}{c|c|c|c|r}
d_A&d_B&A\to B&B\to A&\#\\ \hline
0&1&1&0&84\\
0&1&1&1&102\\
1&0&0&1&84\\
1&0&1&1&102\\
1&1&0&0&228\\
1&1&0&1&308\\
1&1&1&0&308\\
1&1&1&1&390.
\end{array}                                           \tag{2.4}
\]

These counts sum to 1,606 and reproduce the candidate's
\((1,1):1234,(1,2):372\) minimum-cut profile.

## 3. Uniform propensity comparison in a dyadic band

Fix one strong orientation and its positive rate constants.  All constants
below may depend on this fixed data.  Let \(N=X+P+U\) be the current total
population.  Stop upon leaving

\[
 {r\over2}<R<2r,\qquad R\le\varepsilon N,\qquad r\ge K.              \tag{3.1}
\]

Let \(a_A,a_B>0\) be the sums of outgoing rate constants from \(A,B\).
The aggregate minimum-source propensity is

\[
 \lambda_{\min}
 =a_A P(P-1)+a_B XU.                                  \tag{3.2}
\]

Since \(X=N-P-U\ge N-R\ge(1-\varepsilon)N\), a split according to
\(P\ge R/2\) or \(P<R/2\) gives

\[
 \lambda_{\min}\ge c\{P(P-1)+NU\}\ge c r^2.         \tag{3.3}
\]

Let `bad` consist of all top reactions sourced at \(H_1,H_2\), together
with the physical death.  Let `exceptional` additionally include the
physical birth.  Uniformly in (3.1),

\[
 \lambda_{\rm high}\le C U R,
 \qquad \lambda_{\rm death}\le CR,
 \qquad \lambda_{\rm birth}=O(1).                    \tag{3.4}
\]

If \(U>0\), the \(XU\) term in (3.2) bounds
\(UR/\lambda_{\min}\) by \(C R/N\le C\varepsilon\).
If \(U=0\), the high-source propensity vanishes.  The two cases
\(P\ge R/2\) and \(P<R/2\) similarly bound the death term.  Thus

\[
 {\lambda_{\rm exceptional}\over\lambda_{\min}}
 \le q_{\varepsilon,K}:=C(\varepsilon+K^{-1}),        \tag{3.5}
\]

and the same inequality holds with `bad` in place of `exceptional`.
This comparison retains every reaction.  It is a comparison with the
aggregate minimum clock, not with a currently available cut clock.

At successive reaction times before the stop, the indicator of an
exceptional reaction is therefore adaptively dominated by a Bernoulli
variable of parameter \(q_{\varepsilon,K}\).  The usual conditional
exponential-supermartingale proof gives, for every deterministic \(M\),

\[
 \Pr\{E_M\ge t\}
 \le \inf_{\theta>0}
  \exp\{-\theta t+M\log(1+q_{\varepsilon,K}(e^\theta-1))\}.          \tag{3.6}
\]

## 4. Exact source-balance lemma

Consider any finite reaction prefix which stays in (3.1).  Write
\(m_A,m_B\) for the numbers of reactions sourced at \(A,B\), and \(e\) for
the number of exceptional reactions.  Each exceptional reaction changes
\(P,U\) by at most two.

If \(B\) has no direct cut, every \(B\)-reaction is \(B\to A\), hence lowers
\(U\) by exactly one.  An \(A\)-reaction raises \(U\) by at most two.
Nonnegativity of \(U\) gives the pathwise inequality

\[
 m_B\le U_0+2m_A+2e\le2r+2m_A+2e,
 \qquad
 m_A\ge{m_A+m_B-2r-2e\over3}.                        \tag{4.1}
\]

If \(A\) has no direct cut, every \(A\)-reaction is \(A\to B\), hence lowers
\(P\) by exactly two.  A \(B\)-reaction raises \(P\) by at most two.
Nonnegativity of \(P\) gives

\[
 2m_A\le P_0+2m_B+2e\le2r+2m_B+2e,
 \qquad
 m_B\ge{m_A+m_B-r-e\over2}.                          \tag{4.2}
\]

If both nodes have direct cuts, every minimum-source firing is already a
firing of a direct source.  Equations (4.1)--(4.2) show in the other two
cases that, after an \(O(r+e)\) initial debit, a fixed fraction of all
minimum-source firings come from the direct node.  This remains true when
high-source targets repeatedly recreate a carrier-rich configuration,
because each such recreation is charged to \(e\) in the exact population
balance.

Conditional on a firing from a fixed minimum source, its destination is
chosen with probabilities equal to its outgoing rate constants divided by
their sum.  These probabilities do not depend on the population.  Hence a
direct source has a fixed strict-cut probability \(q_*>0\).  The strict-cut
indicators at successive direct-source firings have the standard adaptive
Bernoulli lower-tail bound

\[
 \Pr\{D_d\le q_*d/2\}\le e^{-c_*d}.                  \tag{4.3}
\]

No independence of reaction times, and no pointwise lower bound on the cut
clock, is used.

## 5. Dyadic exit and duration

Start with \(R_0=r+O(1)\), and stop when \(R\le r/2\), \(R\ge2r\), or
\(R>\varepsilon N\) (the last event is activation and is favorable).  Choose
\(L<\infty\), depending only on the fixed orientation and rates, so large
that (4.1)--(4.3) give at least \(4r\) strict cuts among \(Lr\) reactions
whenever the exceptional count is at most \(r\), except with probability
\(Ce^{-cr}\).  Then choose \(\varepsilon\) small and \(K\) large so that
\(Lq_{\varepsilon,K}\) is smaller than a fixed sufficiently small constant.
Equation (3.6) gives

\[
 \Pr\{E_{Lr}>r\}\le Ce^{-cr}.                        \tag{5.1}
\]

Before the lower boundary can be hit from \(R_0=r+O(1)\), at least
\(r/5\) bad reactions must occur, because all minimum-source reactions and
births are nonnegative in \(R\), while one bad reaction lowers \(R\) by at
most two.  Thus

\[
 \Pr\{R\le r/2\text{ before the upper/activation exit}\}
 \le Ce^{-cr}.                                       \tag{5.2}
\]

On the complementary event, the strict cuts contribute at least \(4r\)
to \(R\), while all bad reactions contribute at worst \(-2r\).  The upper
or activation exit must therefore occur by reaction \(Lr\).  The same
argument, restarted after a rare nonexit prefix, gives an exponential tail
for the number \(J_r\) of reactions before exit:

\[
 \Pr\{J_r>kLr\}\le C e^{-c(r+k)}
 \quad\text{(and a stronger geometric-in-\(k\) version is available).}       \tag{5.3}
\]

While the process remains in the band, (3.3) makes each holding time
stochastically no larger than an exponential variable of rate \(cr^2\).
Combining this domination with (5.3) yields, for a possibly smaller
constant \(c>0\),

\[
 \mathbb E e^{crS_r}\le C,
 \qquad \mathbb E S_r^p\le C_p r^{-p}.               \tag{5.4}
\]

This also resolves the carrier-rich timing objection.  The proof never
waits for \(U\) to drain to zero.  Even if one isolates the one-way initial
layer, only a fixed fractional conversion is needed, whose mean time is
\(O_\varepsilon(n^{-1})\).  More directly, (3.3) shows that the aggregate
minimum clock remains of order at least \(r^2\) throughout the layer.

Equations (5.2)--(5.4) are exactly the dyadic ascent and duration estimates
needed for summation over \(K,2K,4K,\ldots\).  They do not require a Green
corrector.

## 6. Downstream audit

### 6.1 Fixed-\(K\) establishment: pass with a wording repair

At fixed transverse counts, every enabled \(XU\)-source clock is order
\(N\), while all pure-source, high-source, birth, and death clocks are
\(O_K(1)\).  Every fast \(XU\) reaction is zero-height or favorable.  If
\(XU\) has no direct cut, its only outgoing reaction is the zero edge to
\(2P\); after contraction, the pure source has a fixed positive direct-cut
branch.  If \(XU\) has a direct cut, that branch itself has fixed positive
probability.  Thus the contracted finite chain has no closed unsuccessful
class, and prescribing finitely many favorable branches reaches \(R\ge K\)
with a positive probability uniform for large \(N\).  The canonical proof
should explicitly list the high-source clocks among the finitely many slow
competitors.

The resistance-one seed and the two successive resistance-two seeds have
uniform positive trial probabilities.  Concatenating the fixed-\(K\) phase
with the dyadic estimates gives a compound-geometric exponential birth
tail and an exponential activation-duration moment.  The constant-rate
birth count at a stopping time is controlled by its counting-process
exponential martingale; it must not be called conditionally Poisson.

### 6.2 Deterministic service: pass

For both exact supports, the largest invariant subset of \(C=0\) is the
dormant \(X\)-vertex.  At any other boundary point at least one complex is
enabled; strong connectivity supplies a first edge whose target introduces
the missing species.  Iterating this observation puts the top ODE in the
relative interior.  The activated compact shell \(R\ge\varepsilon N\) is
separated from the dormant vertex.  The single-linkage weakly-reversible
permanence theorem then makes the service integral infinite for every
activated trajectory.  Continuity, monotonicity in the fluid horizon, and
compactness give one uniform finite horizon for any fixed required service
integral.

Uniform density-dependent convergence on this fixed horizon is valid even
for lattice initial conditions approaching the boundary.  The death
compensator has the required uniform mean, and its integrated intensity is
uniformly bounded above on a fixed horizon, giving all exponential moments.
Lower births and deaths remain in the chain and are lower order in the
density limit.

### 6.3 Negative macroincrement: pass after one necessary clarification

Negative conditional mean plus a bound on \(Z^+\) does **not**, by itself,
imply a contracting exponential moment.  The valid argument uses the
particular construction.  Let \(B\) be all episode births and let
\(D_0\) be only the deaths in the fixed service window.  Ignore the favorable
preactivation deaths.  Pathwise,

\[
 Z\le \widetilde Z:=B-D_0.                            \tag{6.1}
\]

The activation result gives a uniform exponential moment for \(B\), and
the fixed service window gives one for \(D_0\).  Choose its mean so that
\(\mathbb E(\widetilde Z\mid\mathcal F_0)\le-a\).  Uniform Taylor control
then gives, for some fixed \(\theta,c>0\),

\[
 \mathbb E(e^{\theta Z}\mid\mathcal F_0)
 \le\mathbb E(e^{\theta\widetilde Z}\mid\mathcal F_0)
 \le1-c\theta.                                       \tag{6.2}
\]

This is the exponential supermartingale actually used in the fractional
return.  It yields the exponentially unlikely upper exit, an exponential
tail for the episode count beyond order \(N_0\), all fixed episode-count
moments, and a uniform exponential positive overshoot.  Combining the tail
of the episode count with the conditional duration moments gives
\(\mathbb E\tau^p=O(N_0^p)\) for the required fixed integer \(p>8\).

### 6.4 Common factorial endpoint: pass

The multinomial bound

\[
 \log(N!)-N\log3\le\sum_i\log(x_i!)\le\log(N!)       \tag{6.3}
\]

and the fixed \(O(N)\) linear shift imply that, for any fixed sufficiently
small \(\rho<1\), a lower endpoint \(N_\tau\le\rho N_0\) has

\[
 W_\ell(X_\tau)-W_\ell(x)
 \le-c(N_0\log N_0)^4.                               \tag{6.4}
\]

At the upper endpoint, the crossing jump is positive and its overshoot has
a uniform exponential moment.  Hölder's inequality combines that moment
with the \(e^{-cN_0}\) upper-exit probability, making its expected
factorial cost negligible.  The \(O(N_0^p)\) duration is also negligible
on the fourth-power factorial scale.  This uses the same shifted physical
factorial potential as the other branches.

## 7. Frozen replay and certification boundary

The audited canonical bytes are

~~~text
note    df392304c5c0b5476584175c4601fd2e3d7f80e41154ae03c7ab1bd9de54b518
source  bbe1bd66769c14c88930bb28a3402abba980b6d0422ce2201c83c1ea28be6a8f
test    cf273a011d38b26f455b6490ba52d43dfde2962e34a749094f2cea0ba59ebb54
~~~

The exact finite geometry and the event-skeleton replacement in Sections
3--5 pass this hostile replay, including arbitrary positive rates, both
one-way zero-edge cases, repeated high-source recreation of the carrier-rich
phase, lower clocks, dyadic duration, and boundary overshoots.  The canonical
payload also states the finite-establishment competitor/restart argument and
the exponential-comparator argument (6.1)--(6.2) explicitly.  The canonical
and independent focused suites pass, Python compilation succeeds, and the
canonical note renders as a nine-page PDF.

This is a bounded local proof audit, not a pair/global recurrence promotion.
No exact T3-2 counterexample is supplied by this audit.
