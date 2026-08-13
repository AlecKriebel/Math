# Finite-fitness continuation of the exact weak theta atom

Date: 2026-08-13 (America/Los_Angeles)

No literature search, architecture scan, or external communication was used.

## Status

**PROVED:** the 23-vertex, seven-arm theta graph with endpoint weights
`103/500` strictly amplifies both Bd and dB at the explicit fitness

\[
                              r={1001\over1000}.             \tag{1}
\]

The proof uses two exact rational Bellman subsolutions on the full
`13,728`-state symmetry quotient.  Floating sparse solves only propose the
subsolutions; every transition inequality and both final comparison signs
are checked over `QQ`.

**PROVED:** in the two-parameter plane `(epsilon,x)`, the Bd and dB zero
sets emanating from the two exact weak-selection endpoints are analytic
curves.  Because their neutral endpoints are separated, there is a genuine
open wedge of simultaneous amplification for `epsilon=r-1>0`.  Thus the
weak interval does not collapse immediately at finite fitness.

This is a finite-graph theorem.  It does not by itself raise the asymptotic
universal threshold `R_sim`; doing that requires a composition theorem that
repeats the atom without losing its two positive coordinates.

## 1. The exact first Taylor terms

Let `G_x` be the two-hub graph with seven internally disjoint length-four
paths, internal edge weights one, and hub-adjacent weights `x>0`.  Put

\[
 \mathcal G_U(\epsilon,x)
 ={\rho_U(G_x,1+\epsilon)\over\rho_U(K_{23},1+\epsilon)}-1.
                                                                    \tag{2}
\]

Every finite absorbing system is rational in `(epsilon,x)` on the positive
domain and analytic at `epsilon=0`.  The exact neutral pair calculation in
`EXACT_WEAK_SIMULTANEOUS_THETA.md` gives

\[
 \mathcal G_{Bd}(\epsilon,x)
  =\epsilon A_B(x)+O(\epsilon^2),                          \tag{3}
\]

\[
 A_B(x)={P_B(x)\over(49x^2+249x+4)Q_B(x)},                \tag{4}
\]

where

\[
\begin{aligned}
 P_B(x)={}&180018405x^7+2975072149x^6+13161584556x^5\\
 &+17094630950x^4+2810292145x^3-858773619x^2\\
 &-105248866x-1878120,                                    \tag{5}
\end{aligned}
\]

\[
 Q_B(x)=1786365x^5+15512608x^4+34819480x^3
        +14633270x^2+1659563x+52170,                       \tag{6}
\]

and

\[
 \mathcal G_{dB}(\epsilon,x)
  =\epsilon A_D(x)+O(\epsilon^2),                          \tag{7}
\]

\[
 A_D(x)=-{9576x^2+2473x-924\over2(672x^2+743x+252)}.      \tag{8}
\]

At the frozen rational weight `x=103/500`, these leading coefficients are

\[
 A_B={240476727804846875792249
      \over40280910072408620757517633}>0,                 \tag{9}
\]

\[
 A_D={512179\over54196874}>0.                              \tag{10}
\]

They are approximately `0.00596999242005` and `0.00945034209907`.

The deterministic quotient Taylor solver differentiates the full first-step
system through cubic order.  It gives the following diagnostic expansions
at `x=103/500`:

\[
 \mathcal G_{Bd}=0.00596999242\,\epsilon
                 +0.03888813\,\epsilon^2
                 +0.00353\,\epsilon^3+O(\epsilon^4),       \tag{11}
\]

\[
 \mathcal G_{dB}=0.00945034210\,\epsilon
                 -1.572125\,\epsilon^2
                 +1.21058\,\epsilon^3+O(\epsilon^4).       \tag{12}
\]

Only the first coefficients in (9)--(10) are used as exact theorem data.
The higher displayed decimals are a high-accuracy quotient diagnostic.  In
particular, (12) correctly predicts that this fixed atom loses its dB gain
on the scale `epsilon approximately 0.006`; it is not a path to the hybrid
endpoint by itself.

## 2. Analytic overlap curves

Let `alpha_B` be the unique positive root of `P_B`, and let

\[
 \alpha_D={-2473+5\sqrt{1660345}\over19152}.              \tag{13}
\]

Exact signs give

\[
          \alpha_B<{103\over500}<\alpha_D.                \tag{14}
\]

Moreover, `gcd(P_B,P_B')=1`, so `alpha_B` is simple; the quadratic root
`alpha_D` is also simple.  Since every denominator in (4) and (8) is
positive, the derivatives satisfy

\[
                         A_B'(\alpha_B)>0,
 \qquad A_D'(\alpha_D)<0.                                 \tag{15}
\]

Define the analytic continuations

\[
 F_U(\epsilon,x)=
 \begin{cases}
   \mathcal G_U(\epsilon,x)/\epsilon,&\epsilon\ne0,\\
   A_U(x),&\epsilon=0.
 \end{cases}                                               \tag{16}
\]

The analytic implicit-function theorem applied at `(0,alpha_B)` and
`(0,alpha_D)` produces unique analytic zero curves

\[
 F_{Bd}(\epsilon,x_B(\epsilon))=0,
 \qquad
 F_{dB}(\epsilon,x_D(\epsilon))=0,                         \tag{17}
\]

with `x_B(0)=alpha_B` and `x_D(0)=alpha_D`.  By (14) and continuity,

\[
                         x_B(\epsilon)<x_D(\epsilon)        \tag{18}
\]

for all sufficiently small positive `epsilon`.  For those fitnesses, every
`x` strictly between the curves is a finite simultaneous amplifier.  This
is the exact noncollapse theorem.  It supplies an abstract positive
`epsilon_0`; the next section gives a separate explicit rational checkpoint.

## 3. Exact checkpoint at `r=1001/1000`

The full quotient state is

\[
 (h_L,h_R;n_{000},n_{001},\ldots,n_{111}),
 \qquad \sum_\eta n_\eta=7.                               \tag{19}
\]

There are

\[
                         4{14\choose7}=13728               \tag{20}
\]

states, of which `13726` are transient.  The verifier constructs both
first-step systems directly from the update definitions at (1) and
`x=103/500`.

For a transient embedded chain with committor `h`, a rational vector `u`
obeying

\[
             u_i\le p_{iF}+\sum_{j\ transient}Q_{ij}u_j   \tag{21}
\]

at every state is a subsolution, hence `u<=h` by absorption and monotone
iteration.  The verifier constructs a rational `u` on the common grid
`10^-16` and checks (21) exactly.

To make the inequalities robust, it mixes a numerical committor proposal
with a strict analytic subsolution.  For Bd the neutral reproductive-value
martingale `v_B` is already strict at every transient state when `r>1`.  For
dB there are two checkerboard states with zero one-step drift, so the strict
subsolution is

\[
                              w_D={v_D+T_Dv_D\over2}.       \tag{22}
\]

Indeed,

\[
             T_Dw_D-w_D={T_D^2v_D-v_D\over2}>0            \tag{23}
\]

at every transient state.  Both signs are verified over `QQ`.  A mixing
weight `10^-6` leaves the desired uniform-start gap essentially unchanged
while providing a rational slack margin against rounding.

The final exact subsolution averages exceed the complete references by

\[
 \rho_{Bd}(G,1001/1000)-\rho_{Bd}(K_{23},1001/1000)
 >2.63658\times10^{-7},                                   \tag{24}
\]

\[
 \rho_{dB}(G,1001/1000)-\rho_{dB}(K_{23},1001/1000)
 >3.45738\times10^{-7}.                                   \tag{25}
\]

The decimals in (24)--(25) only abbreviate positive rational numbers printed
in full by the replay.  The minimum exact Bellman slacks are respectively
about `6.23e-13` and `4.34e-13`.  Therefore (24)--(25) are rigorous lower
bounds, not residual-based floating comparisons.

## 4. Fixed-weight finite-fitness behavior

The sparse quotient solver, with residuals below `6e-14`, gives the following
orientation for `x=103/500`:

\[
\begin{array}{c|cc}
 r&\mathcal G_{Bd}&\mathcal G_{dB}\\ \hline
 1.001&+6.01\,10^{-6}&+7.88\,10^{-6}\\
 1.002&+1.21\,10^{-5}&+1.26\,10^{-5}\\
 1.005&+3.08\,10^{-5}&+8.11\,10^{-6}\\
 1.006&+3.72\,10^{-5}&+3.88\,10^{-7}\\
 1.0065&+4.36\,10^{-5}&-4.63\,10^{-6}.
\end{array}                                                \tag{26}
\]

These rows are diagnostic except for (1), which has the exact certificate
above.  They show that the fixed atom has a genuine but narrow fitness
window and that dB is the losing coordinate.

## 5. BDM diagnostic at the hybrid endpoint

At `r=R_hyb`, the same quotient solver gives

\[
 b=\rho_{Bd}(G,R)=0.3362368954\ldots,\qquad
 a={\rho_{dB}(G,R)\over R-1}=0.5646219105\ldots.           \tag{27}
\]

Thus `a+b=0.900858806<1`.  The Hellinger side of the bounded
dual-moment inequality is on its zero branch:

\[
 R(R-1)^2
 \left[\sqrt{ab}-\sqrt{(1-a)(1-b)}\right]_+^2=0.          \tag{28}
\]

Every portal law has `q_Bq_D>0`, so this exact weak atom satisfies BDM
strictly but vacuously at `R_hyb`.  It is therefore consistent with the
proposed local upper lemma.  The diagnostic margin `1-a-b approximately
0.0991` is far larger than the numerical residual, although (27) is not
promoted here to an exact algebraic certificate.

## 6. Replays and remaining construction question

Run

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
lower_global_tradeoff/verify_theta_r1001_checkpoint.py
```

for the exact theorem at (1), and

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -B \
  universal_simultaneous_amplification/phase5_exact_threshold/\
lower_global_tradeoff/audit_theta_full_fitness.py --x 0.206 --r 1.002 --series
```

for the full quotient and Taylor diagnostic.

The strongest theorem currently warranted is finite: one fixed graph is a
strict simultaneous amplifier at the explicit fitness (1).  To turn it into
a lower bound for `R_sim`, one must prove that a growing connected
composition of these atoms retains a positive pair of response curves on a
common interval.  The exact module--trace Schur theorem identifies the data
that such a composition must preserve, but no nonlinear finite-fitness
composition law is yet proved.

