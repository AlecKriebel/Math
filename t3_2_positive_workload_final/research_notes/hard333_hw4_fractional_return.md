# A fractional-population common-(W) candidate for the four hard (H_w) switches

## 1. Scope and status

This note gives a candidate stopped theorem for the four rank-two
(H_w)-switch pairs inside the hard 333 family.  It avoids the impossible
direct scalar

\[
             W_\ell+\eta(1+A+B+C)^q                 \tag{1.1}
\]

identified in *hard333_switch_16_scalar_obstruction.md*.  Instead, it repeats
a full-chain activation/service macroepisode until total population drops by
a fixed fraction.  That contraction forces a large decrease of the same
factorial fourth power (W_\ell), irrespective of how the top linkage has
redistributed the population.

The argument has not received independent analytic replay.  All executable
analytic, pair-recurrence, and global flags remain false.  The exact
four-pair fingerprint is

```text
4b24d4d3437351daf8e1d9b0e84e3d38e5e77147141a44fd9b68f6e1bba68716
```

If this candidate eventually passes audit, the unresolved switch family
would shrink claim-neutrally from sixteen to the exact twelve (H_b) pairs.

## 2. Exact geometry

Every pair has lower linkage (0\rightleftarrows C), and its other linkage
is one of

\[
\begin{array}{c|c|c|c}
T&\text{sources on }C=0&\text{dormant vertex}&\text{seed resistance}\\ \hline
\{2A,2C,AB,AC\}&\{2A,AB\}&B&2\\
\{2A,2C,AC,BC\}&\{2A\}&B&1\\
\{2B,2C,AB,BC\}&\{2B,AB\}&A&2\\
\{2B,2C,AC,BC\}&\{2B\}&A&1.
\end{array}                                             \tag{2.1}
\]

Each (T) is homogeneous of molecularity two and has stoichiometric rank
two.  Hence

\[
                  n=A+B+C,qquad \mathcal L_Tn=0         \tag{2.2}
\]

for every strong orientation and every positive rate vector.  There is one
all-active failed descriptor, with workload ((1,1,1)), on each pair.

The service-zero face has exactly one invariant vertex.  For example, in
the first row, if (A,B>0), strong connectivity supplies a cut edge from
({2A,AB}) to a (C)-containing complex.  At the pure (A)-vertex,
(2A) is enabled and the trajectory either creates (C) immediately or
creates (B), after which the cut applies.  The pure (B)-vertex is
dormant because (2B) is absent.  The other rows are identical or obtained
by swapping (A,B).

In the resistance-one rows, the physical (0\to C) seed immediately
enables the carrier (BC) or (AC).  In the resistance-two rows, one seed
does not enable a top source, but two seeds enable (2C).  Every outgoing
edge from (2C) creates the missing nonservice species, after which the
carrier (AB) has order-(n) propensity.

## 3. One activation/service macroepisode

Fix one pair, orientation, and rate vector.  Constants below may depend on
those fixed data, but not on population size.

### 3.1 Activation near the dormant vertex

Write (X) for the dormant species and (R) for a positive linear form in
the two transverse species.  Once a carrier is present, the same killed
carrier construction used for the final-seven activation theorem gives

\[
       \mathcal L_TR\ge cXR-KR^2,qquad
       \Gamma R\le CnR.                                \tag{3.1}
\]

For sufficiently small fixed (arepsilon>0), throughout
(0<R\le\varepsilon n),

\[
                    \mathcal LR\ge c_1nR.               \tag{3.2}
\]

The resistance-one rows start (3.2) after one (0\to C) seed.  In a
resistance-two row, the finite birth--death race on (C=0,1,2), followed by
the first (2C)-firing, has a fixed positive success probability.  Failure
returns to the dormant vertex or incurs a favorable (C\to0) death.  Thus
the number (K) of physical births used before a carrier ascent has a
uniform exponential moment.

Applying the exponential supermartingale to (e^{-\theta R}), and the
logarithmic drift estimate to (log R) away from a fixed finite transverse
set, yields a fixed success probability for reaching
(R\ge\varepsilon n).  Failed carrier attempts have physical duration
(O(\log n/n)); dormant waiting times are exponential with the fixed lower
birth rate.  Consequently, for some (	heta_0>0),

\[
 \sup_{n\ge n_0}\mathbb E e^{\theta_0K}<\infty,
 \qquad
 \sup_{n\ge n_0}\mathbb E\sigma_{\rm act}^m<\infty
 \quad(m\ge1).                                         \tag{3.3}
\]

No top, birth, or death clock is deleted.

### 3.2 Uniform service from the activation shell

Normalize the top ODE to the unit simplex.  If
(int_0^\infty C(t)\,dt<\infty), uniform continuity gives (C(t)\to0).
The omega-limit is then contained in the largest invariant subset of
(C=0), which Section 2 identifies as the unique dormant vertex.  The
fluid form of (3.1) repels every nontrivial trajectory from that vertex.
Therefore

\[
                       \int_0^\infty C(t)\,dt=\infty    \tag{3.4}
\]

for every trajectory started on the compact normalized activation shell.
Continuity and compactness imply that, for every prescribed (M), one can
choose finite (T(M)) with

\[
       \inf_{z\in\mathcal A}\int_0^{T(M)} C_z(t)\,dt>M. \tag{3.5}
\]

Run the full stochastic chain for physical time (T/n).  The top density
process converges uniformly to the ODE over this fixed fluid horizon.  The
lower birth has (O(n^{-1})) expected firings, while the number (D) of
(C\to0) deaths has compensator

\[
             \kappa_{C0}\int_0^T Z_{n,C}(t)\,dt.        \tag{3.6}
\]

Counting-process exponential martingales give uniform exponential moments
for the service-window birth and death counts.  Choosing (M) after the
activation law makes

\[
  \mathbb E\{K+B_{\rm win}-D\}\le-a<0,
  \qquad
  \sup_n\mathbb E e^{\theta_1(K+B_{\rm win}-D)^+}<\infty              \tag{3.7}
\]

for fixed (a,	heta_1>0).  Preactivation deaths are retained in the
physical chain and only improve the population upper bound.

Thus one macroepisode, from any sufficiently large state, has population
increment (Z), duration (S), and constants independent of its starting
population such that

\[
 \mathbb E(Z\mid\mathcal F_0)\le-a,
 \quad
 \mathbb E e^{\theta Z^+}\le C,
 \quad
 \mathbb E S^m\le C_m\quad(m\ge1).                    \tag{3.8}
\]

Away from the dormant wedge, the activation part is omitted and the same
compact service argument begins immediately.

## 4. Repetition to a fractional contraction

Fix (0<\rho<1), let (n_0=n(x)), and concatenate the macroepisode from
Section 3 at its successive strong-Markov endpoints.  Stop at the first
macroendpoint (J) with

\[
                     n_J\le\rho n_0
                     \quad\hbox{or}\quad
                     n_J\ge2n_0.                       \tag{4.1}
\]

Uniform exponential integrability and the strict conditional mean in
(3.8) give a sufficiently small (gamma>0) for which

\[
       \mathbb E(e^{\gamma Z}\mid\mathcal F)\le1-c\gamma.             \tag{4.2}
\]

The exponential supermartingale and optional stopping yield

\[
       \mathbb P(n_J\ge2n_0)\le C e^{-c(1-\rho)n_0}.    \tag{4.3}
\]

The ordinary negative-drift stopped-sum estimate gives

\[
       \mathbb EJ\le Cn_0,qquad
       \mathbb EJ^m\le C_m(1+n_0)^m.                  \tag{4.4}
\]

Combining (3.8) and (4.4) gives, for every fixed (m),

\[
       \mathbb E\tau^m\le C_m(1+n_0)^m,               \tag{4.5}
\]

and the upward overshoot at (2n_0) retains an exponential moment.  In
particular one may choose (m>8).

## 5. The common factorial endpoint

Fix an arbitrary vector (ell\in\mathbb R^3), and choose (K_\ell) so
that

\[
 F_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\cdot x\ge1,
 \qquad W_\ell=F_\ell^4.                              \tag{5.1}
\]

For every state of total population (n),

\[
       \log(n!)-n\log3
       \le\sum_i\log(x_i!)\le\log(n!).                \tag{5.2}
\]

On the contraction event in (4.1), Stirling's bounds and (5.2) give,
uniformly over both endpoint allocations,

\[
 F_\ell(X_\tau)-F_\ell(x)
 \le \log((\rho n_0+O(1))!)-\log(n_0!)+O(n_0)
 \le-c_\rho n_0\log n_0.                             \tag{5.3}
\]

Since (F_\ell(x)=\Theta(n_0\log n_0)),

\[
       W_\ell(X_\tau)-W_\ell(x)
       \le-c(n_0\log n_0)^4.                          \tag{5.4}
\]

The exponentially unlikely upper exit in (4.3), including its random
overshoot, contributes (o(1)) after any polynomial endpoint weight.
Equation (4.5) is lower order than (5.4).  Hence the proposed full stopped
inequality is

\[
 \mathbb E_x\!left[
    W_\ell(X_\tau)-W_\ell(x)+\tau
 \right]
 \le-c(n_0\log n_0)^4                                \tag{5.5}
\]

outside a finite set.

This uses one common physical potential and never pays a switch from
(W_\ell) to (H^q).  If (3.1)--(5.5) survive independent replay, the
random-time Foster theorem would prove positive recurrence on every closed
irreducible class for all four pairs.

## 6. Independent audit gate

Before any flag changes, an independent audit must verify:

1. the resistance-two (C=0,1,2) regenerative trial with every lower clock
   retained;
2. the carrier ascent and exponential seed-count estimate for every strong
   top orientation;
3. the largest-invariant-set and uniform integrated-service arguments;
4. the lattice-uniform density limit and counting-process exponential
   moments;
5. the conditional moment generating function in (4.2), including starts
   after random overshoots;
6. the (m>8) random-sum duration and endpoint estimates; and
7. the factorial envelope on both stopping branches.

Until that replay succeeds, the candidate changes no certified count.

## 7. Reproduction

```text
PYTHONPATH=src python3 -B src/hard333_hw4_fractional_return.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_hard333_hw4_fractional_return.py -v
```

The executable freezes the four supports, the (2+2) activation-resistance
split, the exact dormant vertices, the service-zero sources, and the
claim-neutral twelve-pair remainder.
