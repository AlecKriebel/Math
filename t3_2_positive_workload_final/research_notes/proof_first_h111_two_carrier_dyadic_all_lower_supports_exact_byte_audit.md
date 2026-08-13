# Exact-byte audit: carrier/dyadic activation

**Independent audit date:** 2026-08-12 PDT.

## 1. Frozen target and verdict

The immutable target is

~~~text
research_notes/proof_first_h111_two_carrier_dyadic_all_lower_supports_theorem.md
SHA-256 f4d8cc40ccea1c6d9e0df9302f75c8cc1d58dd7c89669fd19ad48fc4bca735b0
499 lines / 20,690 bytes
~~~

> **STRICT PASS.** The target proves the stated all-clock
> activation-or-direct-death ledger for every rank-two two-carrier or dyadic
> homogeneous support, every allowed lower unary support, every strong
> labelled orientation, and every fixed positive rate vector. The mean
> physical time and birth debt are uniform in the initial population and in
> the later death threshold \(L\).

This verdict is analytic. No reaction orientation, rate vector, population
box, or stochastic history was enumerated. The finite support identity
\(360=168+144+48\) is a separate geometry certificate and supplies no
probability estimate.

## 2. Repaired scope and rejected rank-one witness

The earlier candidate incorrectly allowed the optional dyadic high set to be
empty. The target now assumes

\[
                    \dim\operatorname{span}(T-T)=2.                 \tag{2.1}
\]

This is necessary. Without it, the literal support

\[
                 T=\{X+Y,2Z\},\qquad R=\{0,Y,Z\}
\]

at initial population \((N,0,0)\) is a counterexample to uniform activation:
the upper linkage has rank one and preserves \(2Y+Z\), while the lower
transverse process has an \(O(1)\) recurrent scale independent of \(N\).
The target excludes this support. In the dyadic kernel, (2.1) forces at least
one of \(Y+Z,2Y\); in the two-carrier kernel it forces a vertex outside
\(\{X+Y,X+Z\}\). These are exactly the graph facts used in the proof.

## 3. Workload ledger, wedges, and debt independent of \(L\)

The physical workload identity is exact:

\[
                 H(X_t)-H(X_0)=B_t-D_t.                            \tag{3.1}
\]

Top reactions and nonzero lower transfers preserve total population. Only
constant-source births and labelled unary-to-zero deaths occur in (3.1).
The normalized transverse heights vanish at distinct pure vertices, so small
wedge closures are disjoint. Bounded reaction vectors then ensure that,
outside a finite set, a physical wedge exit lands in the common activated
region rather than another wedge.

The proof first constructs \(\sigma_\infty\), stopped only at fractional
workload return or wedge exit, with

\[
       \sup_x\mathbb E_x\sigma_\infty<\infty,
       \qquad
       \sup_x\mathbb E_xB_{\sigma_\infty}<\infty.                  \tag{3.2}
\]

Every direct-death clock remains live. Only afterward does the theorem set
\(\sigma_{x,L}=\sigma_\infty\wedge\rho_L\), where \(\rho_L\) is the actual
\(L\)-th direct death. Monotonicity preserves (3.2), so its constant is
independent of \(L\). Endpoint priority \(F>D>I\) makes classifications
disjoint. There is no circular choice of \(L\) against an \(L\)-dependent
activation debt.

If \(X\to0\) has positive coefficient, the exact drift
\(\mathcal LH\le\beta-cH\) proves (3.2) before wedge exit or fractional
return. Otherwise every \(X\)-sourced lower arrow is a favorable transfer to
\(Y\) or \(Z\), while adverse lower intensity is only \(O(1+Y+Z)\).

## 4. Literal finite establishment

### 4.1 Two carriers

At \(S=0\), either an \(X\)-sourced lower transfer seeds transverse mass at
rate \(cX\), or \(U=\{Y,Z\}\) and a constant-source lower birth seeds it at a
fixed positive rate. For \(0<S<K\), the killed-resolvent estimate and exact
lower signs give

\[
                       \mathcal LS\ge cH_0S,
              \qquad \Gamma S\le CH_0S.                            \tag{4.1}
\]

All clocks remain in this generator. A small \(e^{-\theta S}\) is therefore a
supermartingale until \(S=0\), \(S\ge K\), fractional return, or wedge exit.
Every nonzero integer population has \(S\ge s_*>0\), yielding a uniform
success probability. Stopped Dynkin applied to bounded \(S\), with
\(H\ge H_0/2\), gives \(O(H_0^{-1})\) mean seeded-trial time. Geometric
reseeding gives uniform mean time and birth count. This is an all-clock
renewal, not a prescribed slow word.

### 4.2 Dyadic kernel with \(X\in U\)

Every \(X\)-sourced lower event raises \(S=2Y+Z\), at aggregate favorable
rate at least \(cX\ge cH_0\). While \(S<K\), every clock that can lower \(S\)
is sourced in the bounded \((Y,Z)\) phase and has aggregate rate \(O_K(1)\).
Neutral minimum-source firings remain live but only time-change the race.
Thus \(K\) favorable events precede an adverse reset with fixed positive
probability and \(O(H_0^{-1})\) mean time.

### 4.3 Dyadic kernel with \(U=\{Y,Z\}\)

The phase \(S<K\) is finite after contracting only the order-\(H\) firings
sourced at \(B=X+Y\). From zero, a lower birth creates \(Y\) or a lone \(Z\).
A lone \(Z\) reaches \(Y\), receives a second seed, or is lost and restarts.
At \(Z\ge2\), source \(A=2Z\) has a fixed positive clock. An internal
\(A\to B\) firing is followed by the fast \(B\) clock; internal
\(A\leftrightarrow B\) moves preserve height.

The set \(\{A,B\}\) is not closed in the strong upper graph because of
(2.1). Hence one source has a strict outgoing label with fixed positive
same-source conditional probability. Every finite phase reaches a strict
height increment, a favorable terminal, or a reset with a uniform
minorization and bounded mean. Forbidding finitely many adverse height losses
concatenates at most \(K\) strict increments with fixed positive probability.
Geometric repetition closes the lone-\(Z\) resistance-two phase and the
neutral \(A\leftrightarrow B\) loop without suppressing a fast clock.

## 5. Two-carrier multiplicative ascent

Killing the strong top graph on leaving the carrier set gives a transient
two-state subgenerator \(Q\). With \(g=(-Q)^{-1}{\bf1}\) and

\[
                 S=(1-\epsilon g_Y)Y+(1-\epsilon g_Z)Z,
\]

exact falling-factorial algebra gives

\[
                   \mathcal L_TS\ge cXS-CS^2.                       \tag{5.1}
\]

Together with the lower signs, on \(K\le S<\varepsilon_0H\),

\[
                  \mathcal LS\ge cHS,
             \qquad \Gamma S\le C'HS.                              \tag{5.2}
\]

The exponential test gives an \(e^{-cr}\) lower-band probability at scale
\(r\). The time estimate uses a bounded \(f_r\) equal to \(\log S\) on the
entire one-jump enlargement of the open band. Thus it uses the full generator,
not a killed logarithm, and

\[
                  \mathcal Lf_r\ge cH\ge cr.                        \tag{5.3}
\]

The stopped endpoint oscillation of \(f_r\) is bounded, so Dynkin has the
correct sign and gives \(\mathbb Et_r\le C/r\). Summing doubling bands gives
finite error and finite mean time.

## 6. Dyadic source balance with all lower supports

In a band \(r/2<S<2r\le2\varepsilon_0H\), the aggregate minimum-source rate
satisfies

\[
  \lambda_{\min}=a_AZ(Z-1)+a_BXY\ge cr^2.                           \tag{6.1}
\]

Optional high-source events, \(Y/Z\)-sourced lower events, direct deaths, and
births have relative bad probability \(C(\varepsilon_0+r^{-1})\). Potentially
order-\(H\) \(X\)-sourced lower events remain live and are counted separately
as favorable height increments.

On every no-exit prefix, the exact height ledger gives

\[
                              g+c_*\le Cr+Ce.                        \tag{6.2}
\]

The two population balances show that, after an \(O(r+e+g)\) debit, a fixed
fraction of minimum-source firings occur at a source with a strict outgoing
label. Substituting (6.2) absorbs the live \(X\)-source count \(g\) into
\(O(r+e)\). Same-source label ratios are fixed. Adaptive Chernoff bounds
control bad events and strict-label successes. Hence a prefix of \(L_0r\)
reactions exits upward except with probability \(Ce^{-cr}\); a lower exit
also requires \(cr\) bad reward and has the same bound.

The expected reaction count is \(O(r)\). Equation (6.1) bounds each
conditional mean holding time by \(C/r^2\), so \(\mathbb Et_r\le C/r\). This
covers every optional high subset and every two- or three-unary lower support.
It neither inspects an orientation list nor assumes a pointwise strict-cut
clock.

## 7. Stopping-time rigor and final disposition

Establishment and band blocks concatenate at actual endpoints. Zero-length
classifier handoffs are merged rather than counted as episodes. Binary mass
action is nonexplosive because \(H_t\le H_0+N_t\) for the constant-rate birth
process \(N\); within a population level there are finitely many states and
bounded total hazards. Localization and monotone convergence justify the
stopped Dynkin and compensator identities. In particular,

\[
              \mathbb EB_{\sigma_\infty}
                  =\beta_0\mathbb E\sigma_\infty<\infty.            \tag{7.1}
\]

The target proves exactly its advertised activation-or-ledger interface. It
does not append the deterministic activated-shell service window, nor infer a
stochastic theorem from the finite \(168+144\) support count. Within that
scope, no mathematical gap or counterexample remains.

**Frozen verdict: STRICT PASS.**
