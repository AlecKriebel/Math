# Remaining fast-phase corrector gate

## 1. First exact unresolved arbitrary pairing

After closing the exact \(\{C,A+C,B+C\}\) seam, the first unresolved
shielded/available pairing is

\[
 L_0=\{B,2A,B+C\},\qquad
 L_1=\{0,A,C\},\qquad h=(1,2,0).
\tag{1.1}
\]

The first linkage is shielded and preserves

\[
 q=A+2B.
\tag{1.2}
\]

The second linkage is available. Each linkage separately has deficiency
zero, but their union has six complexes, two linkage classes, stoichiometric
rank three, and deficiency one. Therefore the isolated product-form laws do
not combine into a stationary law for the full network.

The minimal partner \(\{0,A\}\) gives a full deficiency-zero system. Adding
the complex \(C\) raises the deficiency, so recurrence of the minimal
subnetwork cannot be transferred by discarding the extra reactions.

## 2. Exact failure of the current one-step factorial argument

Give \(L_0\) the directed cycle

\[
 B\mathop{\longrightarrow}^{1}B+C
 \mathop{\longrightarrow}^{2}2A
 \mathop{\longrightarrow}^{1}B
\tag{2.1}
\]

and give \(L_1\) the directed cycle

\[
 0\longrightarrow A\longrightarrow C\longrightarrow0.
\tag{2.2}
\]

A complex-balanced vector for (2.1) is

\[
 \theta_A=\theta_B=1,\qquad \theta_C=\tfrac12.
\]

For the tilted factorial potential

\[
 F_\theta(x)=\sum_i\log(x_i!)-\sum_i x_i\log\theta_i,
\]

evaluate the generator at \(x_n=(n,n^2,0)\). The reaction
\(B\to B+C\) contributes exactly

\[
 n^2\log2.
\]

The enabled reaction \(2A\to B\) contributes only \(O(n)\), and
\(B+C\to2A\) is disabled. The available linkage contributes at worst
\(-O(n\log n)\). Consequently

\[
 \mathcal L F_\theta(x_n)=n^2\log2-O(n\log n)>0
\]

for all sufficiently large \(n\). Thus complex-balancing the fast linkage
and asking the slower linkage to dominate its one-step factorial drift is
false even in the first residual support.

This is an obstruction to that proof, not a transient or null-recurrent
reaction network.

## 3. Why averaging remains plausible

On a fixed \(q=N\) shell, the isolated \(L_0\) process has the summable
deficiency-zero law

\[
 \pi_N(a,b,c)\ \propto\
 \frac{\theta_A^a}{a!}
 \frac{\theta_B^b}{b!}
 \frac{\theta_C^c}{c!}
 \mathbf 1_{\{a+2b=N\}}.
\tag{3.1}
\]

Under this law, \(C\) is Poisson and independent of \((A,B)\), while the
typical scale of \(A\) is \(\Theta(\sqrt N)\). Strong connectivity of
\(L_1\) forces an outgoing edge from \(A\) to \(0\) or \(C\), so its
stationary averaged \(q\)-drift is negative of order \(\sqrt N\); positive
\(q\)-events sourced at \(0\) or \(C\) have only bounded stationary mean.

What is missing is a uniform passage from this stationary average to the
actual coupled process started at an arbitrary point of the shell.

There is also an exact transient scalar behind the same square-root scale.
Aggregate the \(L_0\) rates as

\[
\begin{array}{c|cccccc}
\text{edge}&B\to2A&B\to B+C&2A\to B&2A\to B+C&B+C\to B&B+C\to2A\\
\hline
\text{rate constant}&x&y&s&r&t&v
\end{array}
\]

and put \(d=t+v\),

\[
 \alpha=x+\frac{vy}{d}>0,
 \qquad
 \beta=2\left(s+\frac{rt}{d}\right)>0,
 \qquad
 Z=A+\frac{2v}{d}C.
\]

A direct generator calculation gives

\[
 \mathcal L_0 Z=2\alpha B-\beta(A)_2.
\tag{3.2}
\]

Since \(2B=N-A\), the scaling \(A=\sqrt N\,z\) on accelerated time
\(\tau=\sqrt N\,t\) formally yields the Riccati equation

\[
 \frac{dz}{d\tau}=\alpha-\beta z^2,
\tag{3.3}
\]

with a strictly positive stable root. This identifies the right transient
mechanism, but (3.2) alone does not supply the required shell-uniform
stopping-time or endpoint estimates.

## 4. Exact missing theorem

Prove a shell-uniform killed-resolvent or Poisson-corrector estimate for the
fast \(L_0\) process such that:

1. the correction reduces its positive \(O(B)\) transient factorial drift
   to \(O(A)\), or makes it nonpositive;
2. the correction has endpoint moments sufficient for every \(L_1\) jump;
3. its \(L_1\)-generator error is \(o(\sqrt q)\) in the averaging region;
4. large \(C\), atypically small \(A\), and transitions between \(q\)-shells
   are controlled uniformly; and
5. the resulting global potential is proper and gives a physical-time
   Foster inequality outside a finite set.

Equivalently, construct an unconditioned strong-Markov episode whose
expected \(q\)-change plus physical duration is uniformly negative after
charging every positive \(L_1\) event and every fast \(L_0\) excursion.

The finite atlas records (1.1)--(1.2) but contains none of these resolvent
or corrector estimates.

### A second tempting shortcut also fails

The proper linear workload

\[
 H=q+C=A+2B+C
\]

does not admit a uniform one-arrival/next-service debt margin. Take unit-rate
cycles

\[
 B\to2A\to B+C\to B,\qquad
 0\to C\to A\to0.
\]

Starting from \(x_n=(n,0,0)\), the positive reaction
\(2A\to B+C\) produces \(y_n=(n-2,1,1)\). At that actual target, the
positive and negative \(H\)-hazards are

\[
 P_n=(n-2)(n-3)+1,\qquad S_n=(n-2)+1.
\]

Thus the next \(H\)-changing event is positive with probability tending to
one and \(\mathcal LH(y_n)=n^2-6n+8\). Any successful episode must contract
the whole fast busy period, not treat each positive target as one service
trial.

### What the fast equilibrium does certify

Let \(\tau_B,\tau_{2A},\tau_{BC}>0\) be the directed matrix-tree weights of
the \(L_0\) complex graph. One complex-balanced vector is

\[
 \theta_B=\tau_B,\qquad
 \theta_A=\sqrt{\tau_{2A}},\qquad
 \theta_C=\tau_{BC}/\tau_B.
\]

Under (3.1), write \(m_N=\mathbb E_{\pi_N}A\) and
\(k=\theta_A^2/(2\theta_B)\). Exact factorial-moment and log-concavity
calculations give

\[
 \mathbb E_{\pi_N}(A)_2=k(N-m_N),\qquad
 \operatorname{Var}_{\pi_N}A\le2m_N,
\]

and therefore

\[
 m_N\ge
 \frac{\sqrt{(1+k)^2+4kN}-(1+k)}2
 =\Theta(\sqrt N).
\]

For arbitrary strongly connected \(L_1\),

\[
 \mathcal L_1q=\kappa_{0A}+\kappa_{CA}C
  -(\kappa_{A0}+\kappa_{AC})A,
\]

so its \(\pi_N\)-average is at most \(-c\sqrt N\) eventually. This rules
out a critical or null *averaged* level chain, but it is not a pointwise
killed-resolvent estimate from arbitrary initial phases.

An additive-symmetrization/path comparison also gives an \(L^2(\pi_N)\)
spectral gap of order at least \(\sqrt N\). The resulting centered Poisson
solution has useful stationary \(L^2\) and energy bounds, but those bounds do
not control its weighted jump gradients from a point mass with very large
\(C\). A state such as \((A,B,C)=(N,0,N^4)\) can undergo a \(C\to A\)
shell increase before the fast phase mixes with probability tending to one.

For the large-\(C\) region, the weighted proper workload

\[
 H_\rho=q+\rho C
\]

is promising. Choosing

\[
 \frac{\kappa_{CA}}{\kappa_{CA}+\kappa_{C0}}
 <\rho<
 1+\frac{\kappa_{A0}}{\kappa_{AC}}
\]

with the natural interpretation for missing edges makes the coefficients of
both \(A\) and \(C\) in \(\mathcal L_1H_\rho\) strictly negative. The open
problem is a uniform transient lemma joining that large-\(C\) region to the
\(\sqrt q\)-scale averaged descent region.

## 5. Other unresolved families

The second positive-invariant deficiency-one shielded support is

\[
 \{A,B,A+C,B+C\}.
\]

Its nine minimal available partners are \(\{u,q\}\), where

\[
 u\in\{0,C,2C\},\qquad q\in\{2A,2B,A+B\}.
\]

The four signed supports

\[
 \{0,A,B+C\},\quad \{0,2A,B+C\},\quad
 \{A,2A,B+C\},\quad \{0,A,2A,B+C\}
\]

and their \(A\leftrightarrow B\) images also remain unresolved. Their
invariant \(B-C\) is not proper.
