# The bounded-core trace for the nested-entry obstruction

## 1. Statement and scope

Consider the exact network

\[
 0\mathrel{\mathop{\rightleftarrows}^{\alpha}_{\beta}}AC,
 \qquad
 BC\xrightarrow{\kappa_1}AB\xrightarrow{\kappa_2}2B
 \xrightarrow{\kappa_3}2A\xrightarrow{\kappa_4}BC,     \tag{1.1}
\]

with all six rates positive and falling-factorial stochastic mass-action
propensities. Write \(S=A+B+C\), and start from

\[
 z_N=(0,0,N).                                          \tag{1.2}
\]

The uniform old-debt service block is false, as proved in
*one_active_nested_entry_obstruction.md*. This note analyzes the correct
rare-event scale.

Fix \(T>0\), an integer \(K\ge3\), and \(\rho\in(0,1)\). Define one
base-to-core trial as follows.

1. Wait for the first \(0\to AC\) reaction.
2. Until either \(A=0\) or \(2A\to BC\) fires, retain the full chain.
   Before that firing \(B=0\), so no other reaction in the second linkage
   is enabled.
3. If \(A=0\), stop. If \(2A\to BC\) fires, continue the full chain until
   \[
    \theta_N=T\wedge\inf\{t:B_t\in\{0,K\}\}
              \wedge\inf\{t:S_t\le\rho N\}.           \tag{1.3}
   \]

Let \(\tau_N\) be the complete trial and let \(\mathsf A_N\) denote the
activation event in step 2.

> **Proposition 1.1 (base-to-bounded-core trace).** For every
> positive rate vector,
> \[
> \begin{aligned}
> {\mathbb P}_{z_N}(\mathsf A_N)
>   &={\gamma\over N^2}+O(N^{-3}),
>   &\gamma&={\alpha\kappa_4\over\beta^2}>0,           \tag{1.4}\\
> \sup_N{\mathbb E}_{z_N}\tau_N^p&<\infty
>   &&(p<\infty).                                      \tag{1.5}
> \end{aligned}
> \]
> Conditional on \(\mathsf A_N\),
> \[
> {C_{\tau_N}\over N}\Longrightarrow R,\qquad
> {S_{\tau_N}\over N}\Longrightarrow R,               \tag{1.6}
> \]
> with uniform integrability of every fixed power. Here \(R\in[0,1]\) and
> \[
> m_j={\mathbb E}R^j<1\qquad(j>0).                    \tag{1.7}
> \]
> Consequently,
> \[
> \begin{aligned}
> {\mathbb E}(C_{\tau_N}-N)
>   &=-{\gamma(1-m_1)\over N}+o(N^{-1}),\\
> {\mathbb E}(C_{\tau_N}-N)^2
>   &=\gamma\,{\mathbb E}(1-R)^2+o(1),\\
> {\mathbb E}(C_{\tau_N}^2-N^2)
>   &=\gamma(m_2-1)+o(1)<-\delta                      \tag{1.8}
> \end{aligned}
> \]
> for some \(\delta>0\) and all sufficiently large \(N\).

Thus every positive rational rate vector has strictly negative leading
quadratic trace drift. The displayed network is not a physical C3
counterexample. The stopped-network proposition, including its
finite-state averaging step, has received an independent adversarial check.
It is a local trace theorem, not a global recurrence claim.

## 2. Exact activation asymptotics

Before activation, \(B=0\) and

\[
 C-A=N.                                                \tag{2.1}
\]

The preactivation population is therefore the one-dimensional chain
\(a=A\) with rates

\[
\begin{array}{rcl}
 a\to a+1&:&\alpha,\\
 a\to a-1&:&\beta a(N+a),\\
 a\to\dagger&:&\kappa_4a(a-1).
\end{array}                                            \tag{2.2}
\]

The trial enters (2.2) at \(a=1\). The leading successful path is
\[
 1\xrightarrow{\alpha}2\xrightarrow{2\kappa_4}\dagger.
\]
Its probability is

\[
 {\alpha\over\alpha+\beta(N+1)}
 {2\kappa_4\over
   \alpha+2\beta(N+2)+2\kappa_4}
 ={\alpha\kappa_4\over\beta^2N^2}+O(N^{-3}).           \tag{2.3}
\]

Every other successful path contains at least one additional upward race
against a death rate bounded below by \(\beta N\), or returns from
\(a=2\) to \(a=1\) before trying again. A geometric first-step expansion
therefore makes their total contribution \(O(N^{-3})\). This proves
(1.4). It also shows that, conditional on activation, the firing state has
\(A=2\) with probability \(1-O(N^{-1})\). Immediately after activation,

\[
 (A,B,C)=(0,1,N+3)+o_{\mathbb P}(1),\qquad S=N+4+o_{\mathbb P}(1).
                                                               \tag{2.4}
\]

The un-killed immigration--death chain obtained by deleting
\(a\to\dagger\) dominates the preactivation duration. Its death rate is at
least \(\beta Na\), so the time to \(0\), begun at \(1\), has all moments
bounded by constants times \(N^{-p}\). Adding the initial
\({\rm Exp}(\alpha)\) wait and the bounded postactivation horizon proves
(1.5).

## 3. The stopped averaged phase

Put

\[
 r={\kappa_1\over\beta},\qquad
 \lambda=\kappa_2r+\kappa_4r^2.                       \tag{3.1}
\]

On the stopped region in (1.3), \(1\le B\le K-1\) and either
\(S\ge\rho N\) or the trial has already stopped. Conditional on fixed
\(B=b\) and \(C\), the \(C\)-accelerated part of the \(A\)-generator is

\[
 C Q_bf(a)=C\left[
 \kappa_1b\{f(a+1)-f(a)\}
 +\beta a\{f(a-1)-f(a)\}\right].                      \tag{3.2}
\]

The invariant law of \(Q_b\) is \({\rm Pois}(rb)\). Here is a uniform
moment argument which also covers the corner \(C=0,A\asymp N\). Use the
random clock

\[
 u(t)=\int_0^t C_s\,ds.                                \tag{3.3}
\]

On that clock, the two fast reactions \(BC\to AB\) and \(AC\to0\)
make \(A\) an immigration--death chain whose immigration rate is at most
\(\kappa_1K\) and whose per-particle death rate is \(\beta\). Its
exponential moments are bounded uniformly for every clock value
\(u\ge0\). The only other reactions which increase \(A\) are
\(0\to AC\), at rate \(\alpha\), and \(2B\to2A\), by two at rate at most
\(\kappa_3K(K-1)\). Their count up to \(T\) is dominated by a fixed-rate
compound Poisson variable. The channels \(AB\to2B\) and \(2A\to BC\)
only decrease \(A\). Hence, by the graphical construction, \(A\) is
dominated by the time-changed immigration--death population plus that
compound Poisson variable. In particular, for small enough \(\vartheta>0\),

\[
 \sup_N\sup_{t\le T}
 {\mathbb E}\exp\{\vartheta A_{t\wedge\theta_N}\}<\infty. \tag{3.4}
\]

Equivalently, the exponential-generator calculation has a negative
\(-\beta AC\) term when \(C>0,A\) is large and a negative
\(-\kappa_4(A)_2\) term when \(C\) is small; the only positive additions
in the latter region have the bounded rates just displayed. Thus, for
every fixed \(p\), the fixed-time and occupation bounds are

\[
 \sup_N\sup_{t\le T}{\mathbb E}(1+A_{t\wedge\theta_N})^p
 +\sup_N{\mathbb E}\int_0^{\theta_N}(1+A_t)^p\,dt
 <\infty.                                             \tag{3.5}
\]

No expected path-supremum estimate is asserted or used. Equation (3.5)
implies \(A/N\to0\) in occupation and at each stopped endpoint. Hence
\(C/N-S/N\to0\).

The polynomial space of degree at most two is invariant under \(Q_b\).
Solve its Poisson equations for \(a-rb\) and
\((a)_2-r^2b^2\). Since the physical fast clock is \(C\), use the
state-dependent correctors \(\chi_b(A)/(C\vee1)\). A fast reaction changes
\(C\) by one, so expanding the denominator leaves an \(O(C^{-1})\)
occupation error; a slow \(B\)-jump changes \(b\), but \(b<K\) and the
corresponding corrector jump is again \(O(C^{-1})\). Stopped Dynkin and
(3.5) give

\[
\begin{aligned}
 \int_0^{\theta_N}(A_t-rB_t)\,dt&\longrightarrow0,\\
 \int_0^{\theta_N}\{(A_t)_2-r^2B_t^2\}\,dt
   &\longrightarrow0
\end{aligned}                                         \tag{3.6}
\]

in \(L^1\). The lower bound \(S\ge\rho N\), together with (3.5), makes
\(C\) order \(N\) outside an event of vanishing probability, so the
Poisson-equation boundary terms are uniform. If that lower bound fails,
the trial has already stopped at the desired macroscopic descent.

It follows from the martingale problem that \(B\), stopped on
\(\{0,K\}\), converges to the finite-state chain

\[
\begin{array}{rcl}
 b\to b+1&\text{ at rate }&\lambda b^2,\\
 b\to b-2&\text{ at rate }&\kappa_3b(b-1).
\end{array}                                            \tag{3.7}
\]

This finite stopping is essential: it avoids making any claim about an
explosive unbounded quadratic averaged phase.

The stopped martingale problem converges jointly with \(S/N\). Hitting
\(\{0,K\}\) is a jump boundary of a finite-state chain, hitting
\(\rho\) is a continuous boundary for \(S/N\), and a finite-state jump
occurs at the deterministic time \(T\) with probability zero. The
continuous-mapping theorem therefore gives endpoint, not merely
pre-stopping, convergence at all three boundaries.

## 4. The macroscopic loss

Only the first linkage changes total population:

\[
 S_t=S_0+2N_\alpha(t)-2N_\beta(t),                    \tag{4.1}
\]

where \(N_\alpha\) has intensity \(\alpha\) and \(N_\beta\) has intensity
\(\beta A_tC_t\). Divide by \(N\). The birth term vanishes uniformly on the
fixed horizon. The stopped death martingale has quadratic variation
\[
 {4\over N^2}{\mathbb E}N_\beta(\theta_N)=O(N^{-1}).
\]
Using (3.6), \(C/N-S/N\to0\), and (4.1), the joint limit is

\[
 R(t)=\exp\left\{-2\kappa_1\int_0^tB(s)\,ds\right\},   \tag{4.2}
\]

stopped at \(T\), \(B\in\{0,K\}\), or \(R=\rho\). This proves (1.6).

The limiting stop is strictly positive almost surely. Since \(B(0)=1\),
\(\int_0^\theta B(s)\,ds>0\) almost surely, and therefore
\[
 0\le R<1\quad\hbox{almost surely}.                   \tag{4.3}
\]
This gives (1.7).

For uniform integrability, before the postactivation stop,
\[
 S_t\le S_0+2N_\alpha(T).                              \tag{4.4}
\]
The conditional preactivation excess has a geometric \(O(N^{-1})\) tail
by (2.2), and \(N_\alpha(T)\) is Poisson. Thus
\((S_{\tau_N}/N)^p\) is uniformly integrable for every fixed \(p\).
Because \(A+B=O_{\mathbb P}(1)\) at the stopped endpoint, the same is true
with \(C\) in place of \(S\).

On \(\mathsf A_N^c\), the endpoint is exactly \(z_N\). Combine
(1.4), (1.6), and uniform integrability:

\[
\begin{aligned}
 {\mathbb E}(C_{\tau_N}-N)
 &=\left({\gamma\over N^2}+O(N^{-3})\right)
   \{N(m_1-1)+o(N)\},\\
 {\mathbb E}(C_{\tau_N}-N)^2
 &=\left({\gamma\over N^2}+O(N^{-3})\right)
   \{N^2{\mathbb E}(1-R)^2+o(N^2)\},\\
 {\mathbb E}(C_{\tau_N}^2-N^2)
 &=\left({\gamma\over N^2}+O(N^{-3})\right)
   \{N^2(m_2-1)+o(N^2)\}.
\end{aligned}                                         \tag{4.5}
\]

These are exactly (1.8). In particular the Lamperti combination equals

\[
 2N\,{\mathbb E}(C_{\tau_N}-N)
 +{\mathbb E}(C_{\tau_N}-N)^2
 \longrightarrow
 \gamma\,{\mathbb E}(-2Y+Y^2)<0,\quad Y=1-R.          \tag{4.6}
\]

The strict sign uses only positivity of the six rates. There is no
rate-orientation choice inside (1.1)--(1.2) that reverses it.

## 5. Certification boundary

The exact activation calculation, the stopped finite \(B\)-phase, the
uniform averaging, all three endpoint boundaries, and the quadratic sign
have passed independent audit. Accordingly the stopped-network analytic
flag is true. The deliberately narrower global claims remain false:

- Proposition 1.1 is not included in any pair count;
- no global one-active promotion is claimed; and
- no invariant probability for (1.1) is inferred from this local episode
  alone.

Even after Proposition 1.1 passes, extending it to all mixed supports will
require an exact rare-contest exponent and a support-uniform higher-power
endpoint theorem.
