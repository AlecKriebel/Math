# Independent audit of the v2.0.2 stopped-time repair

**Checkpoint:** 2026-08-22 14:24 PDT

**Assigned-scope completion:** **100%**

**Scope verdict:** **The prior Lemma 9 defect is correctly repaired. No actionable mathematical issue remains in the revised stopped-time argument or its downstream uses.**

## Scope and evidence boundary

I independently compared the revised manuscript with the frozen v2.0.1
manuscript, re-derived the repair from the displayed Bd generator, traced every
direct and indirect downstream use, and tested the boundary states and
conditional stopping arguments. I treated
`REFEREE_RESPONSE_2026-08-22.md` as a list of claims, not as evidence.

The load-bearing revised source is
`delivered_copy/source_and_certificates/universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold/main.tex`.
The relevant rendered text is on PDF pages 10--12. The old source used for the
comparison is the byte-frozen v2.0.1 `main.tex` in the earlier audit's
`delivered_copy`.

The source diff changes the mathematical text only in the Lemma 9 repair and
its immediately adjacent descriptions (revised lines 680--935). The response
functions, threshold algebra, graph diagonal, and theorem quantifier proof are
unchanged. The remaining diff at revised lines 1515--1521 concerns reproducibility
disclosures and the tag URL, not mathematics.

## 1. The old failure is genuinely removed

The old equations (25)--(26), v2.0.1 lines 728--755, used the next pendant
change and `tau_{ell=m}` without stopping at core escape. They could therefore
equal infinity on the positive-probability event of extinction before the
target. An independent exact-rational finite-chain calculation directly
reproduced this mechanism: for a Bd clique--pendant chain with `c=4`, `m=2`,
`r=3/2`, started from `(h,i,ell)=(0,3,0)`,

```
P(hit (h,ell)=(1,m) before extinction) = 0.629017511778...
P(extinction first)                    = 0.370982488222...
```

Thus the corresponding *unstopped* target-hitting time is infinite with
positive probability.

The revised proof instead defines

\[
 \tau_\uparrow=\inf\{s:R_s\ge 2\delta c\},\qquad
 \Sigma=\inf\{s:(h_s,\ell_s)=(1,m)\ \hbox{or}\ R_s\ge2\delta c\}.
\]

This occurs at revised lines 680--681 and 788--794, PDF pages 10--11,
equation (26). Core escape is now an absorbing stopped outcome everywhere it
must be: the committor, the trace, the calendar-time estimate, equation (26),
and the regeneration block all use the same boundary.

## 2. Stopped committor and adapted interruptions

**Anchors:** revised lines 681--729, PDF page 10, equation (24).

For fixed `ell`, let `(p_0,p_1)` be the worst-rate two-hub-phase committor,
with leaf-up value one, leaf-down value zero, and upper-strip exit value one.
The displayed formulas are

\[
 p_0=\frac{H_+U}{H_+U+V(H_-+U)},\qquad
 p_1=\frac{U(H_++V)}{H_+U+V(H_-+U)}.
\]

Both increase with `H_+` and `U` and decrease with `H_-`. More directly, for
the fixed worst-rate function, the actual generator is nonnegative:

- in hub phase zero, `p_1-p_0 >= 0`, so replacing the worst activation rate by
  the larger actual rate can only increase the generator;
- in hub phase one, `1-p_1 >= 0` and `p_0-p_1 <= 0`, so increasing the gain
  rate and decreasing the deactivation rate can only increase the generator;
- core jumps inside the strip leave the function unchanged;
- a core jump through the upper boundary contributes `rate*(1-p_h) >= 0`.

The function is bounded. The next pendant outcome or exit is almost surely
finite: at each hub phase the phase-ending intensity has a positive lower
bound, and every one or two phases has positive probability of a pendant
outcome or exit. Therefore bounded optional stopping applies without using the
later mean-time conclusion. This avoids circularity and permits an arbitrary
adapted sequence of core jumps.

For `1 <= ell < m`, the smaller of the two phase odds is the phase-zero odds,

\[
 \frac{\underline H_+\underline U}
      {\overline H_-V}\frac1{1+\underline U/\overline H_-}.
\]

Writing `a=m-ell >= 1`, the non-vanishing part of its uniform bound follows
exactly from

\[
 (1+2\delta)(\ell+1-2\delta)a-\ell(a+2\delta)
 =a(1-4\delta^2)+2\delta\ell(a-1)\ge0.
\]

Also `underline U/overline H_- = O(C^{-1})` uniformly. Hence equation (24)
does give fixed compact-uniform odds `beta>1`, as claimed.

## 3. Discrete stopped trace, including `ell=0`

**Anchors:** revised lines 731--753, PDF page 10.

The revised trace maps upper exit to terminal level `m`. Before its stopping
index `N`, every outcome is a one-level up move, a one-level down move, or an
exit jump of size at least one toward `m`. For `1 <= ell < m`, the favorable
outcome probability is at least `beta/(1+beta)`. At `ell=0`, a down move is
impossible, so the conditional increment is at least one. Therefore, with
`epsilon=(beta-1)/(beta+1)`,

\[
 \widehat\ell_{j\wedge N}-\epsilon(j\wedge N)
\]

is a bounded-above stopped submartingale. Optional stopping at `N wedge k`
and monotone convergence give `E N <= m/epsilon`. This is valid for the
adapted, non-Markov pendant trace; it uses conditional drift, not independence.

The added `ell=0` sentence is essential and correct. In a resident-hub phase
the loss rate is zero, but activation has a compact-uniform positive intensity.
After activation, the mutant-hub gain-or-exit estimate applies. Thus grouping
at most two hub phases preserves the required geometric comparison.

## 4. Calendar-time estimate and equation (25)

**Anchors:** revised lines 755--782, PDF page 11, equation (25).

Before upper exit:

- in an `h=0` phase, activation plus loss has intensity bounded below by a
  positive constant because `i/c > 1-2 delta`;
- in an `h=1`, `ell<m` phase, deactivation plus gain has intensity at least
  `m-ell >= 1`;
- for `1 <= ell < m`, loss-or-exit before activation has probability
  `Omega(C^{-1})`;
- for `0 <= ell < m`, gain-or-exit before deactivation has probability
  `Omega(C^{-1})`.

Core events may change the competing rates, but throughout the stopped strip
the same pointwise upper and lower hazard bounds hold. They neither reset nor
pause the phase-ending compensators. In every group of at most two phases,
the conditional probability of termination by a pendant change or exit is at
least `c_0/C`, while each phase has uniformly bounded conditional mean
duration. The geometric-tail argument therefore gives, conditional on the
entire past,

\[
 E(\sigma_{j+1}-\sigma_j\mid\mathcal F_{\sigma_j})\le K_0C.
\]

Tonelli's theorem and the stopped conditional estimate justify the random
sum explicitly:

\[
 E\xi
 =\sum_{j\ge0}E[1_{\{j<N\}}(\sigma_{j+1}-\sigma_j)]
 \le K_0C\sum_{j\ge0}P(j<N)
 =K_0C\,EN=O(Cm).
\]

Thus revised equation (25) is finite and is exactly the stopped estimate
needed later.

## 5. Boundary `(h,ell)=(0,m)` and equation (26)

**Anchors:** revised lines 782--795, PDF page 11, equation (26).

This state is not covered by first hitting `ell=m`, so it must be handled
separately. The revision does so correctly. Starting from `(0,m)`, the first
activation, pendant loss, or upper exit has bounded mean time. Uniformly in
`R<2 delta c`,

\[
 \Pr(\hbox{loss first})
 \le \frac{m/(c+m)}{r_-(1-2\delta+m)+m/(c+m)}=O(C^{-1}).
\]

Activation reaches `(1,m)`, and exit is the other terminal event. After the
rare loss, the stopped trace starts from `(0,m-1)` and has mean `O(Cm)`.
Therefore its contribution is only `O(m)`, and the stated weaker uniform
bound `E Sigma=O(Cm)` follows. If `ell` reaches `m` from below, that last event
is a pendant gain and hence the hub is automatically mutant, so there is no
missing resident-hub case. The `(1,m)` starting state has `Sigma=0`.

## 6. Downstream propagation and noncircularity

| Use | Anchor | Audit result |
|---|---|---|
| One-block synchronization and cleanup | revised lines 797--825; PDF page 11, equations (26)--(27) | From `E Sigma=O(Cm)` and `m=o(C)`, `P(Sigma>C^2)=O(m/C)=o(1)`. Independently, core confinement bounds exit by time `C^2` by `O(C^3 e^{-gamma C})`. Their union gives high-probability nonexceptional synchronization before cleanup. |
| Regeneration start | revised lines 837--865; PDF page 12 | Every `S_j` has `R<=delta c`; strong Markov plus the uniform statewise equation (26) gives `E(Sigma_j-S_j | F_{S_j})<=KCm`. Exit is terminal and charged, exactly as equation (26) requires. |
| Block success, escape, duration | revised lines 866--898; PDF page 12, equations (28)--(30) | The stopped synchronization mean supplies the duration bound; the separately proved core confinement supplies the escape bound. No independence between blocks is assumed. |
| Center estimate | revised lines 1161--1179; PDF page 16 | Lemma 9 now yields polynomial-time completion failure `o(q/C)` after choosing `B_0>3/4`; the scale and compact-uniform constants are unchanged. |
| Gate and response functions | revised lines 1206--1329; PDF pages 16--18 | They use Proposition 6 only through its now-supported asymptotic center estimates. No stronger unstopped hitting-time statement is used. |
| Final pointwise fitness diagonal | revised lines 1388--1397; PDF page 18 | The repair is uniform on each fixed compact fitness interval, exactly the uniformity needed before fixing `r`. The graph remains chosen before `r`; the theorem's quantifier order is unchanged. |

There is no circular use of core confinement. Lemma 8 proves confinement
first and uniformly in hub and pendant coordinates. Lemma 9 establishes the
*stopped* synchronization expectation using only pointwise strip rates. Only
after that does it invoke Lemma 8 to show that the terminal exit alternative
is exponentially unlikely over the polynomial block horizon.

## 7. Independent finite-chain corroboration

`independent_checks/math_repair_v202_check.py` imports no manuscript or
certificate code. It constructs the Bd chain directly from the six displayed
rates and solves the relevant finite linear systems with exact rational
Gaussian elimination. Its logged run exited zero. Across three independent
high-core strips it found:

- every stopped mean finite;
- maximum stopped means divided by `(C m)` equal to approximately `0.134`,
  `0.120`, and `0.090`;
- at `ell=0`, every up-or-exit probability exactly one;
- for every tested `1 <= ell < m`, the exact committor odds exceeded both one
  and the manuscript's worst-rate lower bound;
- the old unstopped target had positive extinction-before-target probability.

This computation is corroborative only; the asymptotic conclusion above rests
on the analytic conditional-hazard and stopping argument.

## 8. Search for newly introduced inconsistencies

I found none. In particular:

- `tau_up` is defined once and used consistently in the later dB display;
- strict `R<2 delta c` in equation (26) matches the target boundary and is
  sufficient because every regeneration begins at `R<=delta c`;
- exit cannot occur simultaneously with a pendant event in the finite
  continuous-time chain, so the terminal-level convention is unambiguous;
- the `ell=0`, `(0,m)`, and `(1,m)` boundary states are all covered;
- all compact-uniform constants depend only on the preselected fitness compact;
- the repair does not change any response coefficient, threshold identity, or
  final quantifier transfer.

## Conclusion

The revised equations (25)--(26) now state the correct stopped quantities,
the proof establishes them with valid adapted conditional estimates, and every
downstream use requires exactly this stopped form plus the independently proved
core-confinement bound. The adjacent `ell=0` issue and the separate `(0,m)`
boundary are both handled correctly. **Within the assigned mathematical scope,
the manuscript is ready for submission.**
