# The equality \(BC\)-trigger trace

## 1. Network, question, and exact scope

Consider the weakly reversible bimolecular network

\[
 0\mathrel{\mathop{\rightleftarrows}^{\alpha}_{\beta}}B+C,
 \qquad
 B\xrightarrow{\lambda}A\xrightarrow{\mu}A+B
 \xrightarrow{\nu}2B\xrightarrow{\delta}B,             \tag{1.1}
\]

with all six rate constants positive and falling-factorial stochastic
mass-action propensities. Start at

\[
 x_N=(0,0,N).                                          \tag{1.2}
\]

The potentially dangerous history begins with \(0\to B+C\), then uses
\(B\to A\) before the fast \(B+C\to0\) return. The two events have rates
\(\lambda\) and \(\beta N\), respectively, so this trigger has probability
of order \(N^{-1}\). Conditional on that rare trigger, however, the
excursion lasts order \(N\) physical time and can change \(C\) by order
\(N\). Word counting by itself therefore does not determine the sign of
the return drift.

This note determines that sign. The conclusion is deliberately scoped.

> **Proposition 1.1 (stopped equality-trigger trace).** After the primary
> \(0\to B+C\) reaction, the probability of a \(B\to A\) trigger before
> return to \(A=B=0\) is
> \[
>  p_N={\lambda\over\beta N}
>      +{\lambda(\alpha-\beta-\lambda)\over\beta^2N^2}
>      +O(N^{-3}).                                      \tag{1.3}
> \]
> Conditional on the trigger, the stopped slow trace converges to the
> killed process in Proposition 3.1 below. Its terminal \(C\)-fraction is
> a random variable \(R\) satisfying
> \[
>  0<R<1\quad\hbox{almost surely}.                       \tag{1.4}
> \]
> Consequently, for every fixed \(p>0\), the leading triggered
> contribution is
> \[
>  {\lambda\over\beta}N^{p-1}
>       \{\mathbb E R^p-1\}<0.                          \tag{1.5}
> \]
> In particular the leading \(Q^2\) drift is strictly negative of order
> \(N\), and the leading factorial-entropy drift is strictly negative of
> order \(\log N\).

The convergence assertion is first proved with fixed slow-time and
population cutoffs. Removing those cutoffs uses the exponential return
tail of the limiting killed immigration--death chain and the positive-part
uniform-integrability estimates in Section 5. A finite-\(N\) path which
hits \(C\le \rho N\) before returning is already a macroscopic descent and
is stopped there. Thus no assertion that the unrestricted raw embedded
chain has already returned is hidden in Proposition 1.1.

This rules out a rate-tunable *leading* counterexample in (1.1). It does
not by itself prove recurrence of the full two-linkage network: the same
support pair has two-active failed descriptors, and those regions require
their own common-potential composition.

## 2. Exact identities and the pre-trigger expansion

Write the state as \((A,B,C)=(a,b,c)\), and define

\[
 Q=C-A-B.                                               \tag{2.1}
\]

The reaction increments of \(Q\) are

\[
\begin{array}{c|rrrrrr}
 \text{reaction}&0\to BC&BC\to0&B\to A&A\to AB&AB\to2B&2B\to B\\
 \hline
 \Delta Q&0&0&0&-1&0&+1.
\end{array}                                             \tag{2.2}
\]

Hence the following generator identity is exact, not averaged:

\[
 \mathcal LQ=-\mu A+\delta(B)_2.                        \tag{2.3}
\]

Since \(Q=C-A-B\), it also gives

\[
 \mathcal LC=-\mu A+\mathcal LA+\mathcal LB
                     +\delta(B)_2.                     \tag{2.4}
\]

At a return to \(A=B=0\), the changes of \(C\) and \(Q\) coincide. For
every integrable stopped base return \(\sigma\), therefore,

\[
 \mathbb E(C_\sigma-C_0)
 =\mathbb E\int_0^\sigma
       \{-\mu A_t+\delta(B_t)_2\}\,dt.                 \tag{2.5}
\]

This identity is a useful sign check: after a trigger, the negative
\(A\)-occupation is of order \(N\), whereas the \(B\ge2\) occupation is
lower order.

After the primary entry, the state is \((0,1,N+1)\). Let \(h_1(N)\) be
the probability that \(B\to A\) occurs before the next visit to
\(A=B=0\). A first-step expansion gives

\[
 h_1(N)={\lambda\over \beta(N+1)+\lambda+\alpha}
       +{\alpha\over \beta(N+1)+\lambda+\alpha}
          \left\{{2\lambda\over\beta N}+O(N^{-2})\right\}.
                                                               \tag{2.6}
\]

Expanding (2.6) proves (1.3). The only order-\(N^{-2}\) untriggered
history with positive base displacement is

\[
 (0,1,N+1)\xrightarrow{0\to BC}(0,2,N+2)
 \xrightarrow{2B\to B}(0,1,N+2)
 \xrightarrow{BC\to0}(0,0,N+1).                       \tag{2.7}
\]

Its exact probability is

\[
 {\alpha\over \beta(N+1)+\lambda+\alpha}
 {2\delta\over2\beta(N+2)+2\lambda+2\delta+\alpha}
 {\beta(N+2)\over\beta(N+2)+\lambda+\alpha},          \tag{2.8}
\]

and therefore

\[
 N^2\mathbb P\{C_{\rm return}=N+1,\text{ history }(2.7)\}
 \longrightarrow {\alpha\delta\over\beta^2}.          \tag{2.9}
\]

Every other untriggered positive history contains an additional slow
race against a \(BC\to0\) clock of order \(N\). Its total probability is
\(O(N^{-3})\). Thus (2.7) contributes only \(O(N^{p-3})\) to the drift
of \(C^p\), and cannot compete with (1.5).

Conditional on the trigger, the direct first-event history has probability
\(1-O(N^{-1})\). The post-trigger state is consequently

\[
 (A,B,C)=(1,0,N+1)+O_{\mathbb P}(1)                    \tag{2.10}
\]

in the discrete coordinates, with \(C/N\to1\). We do not replace the
entire conditional kernel by this state in total variation; the
\(O(N^{-1})\) exceptional entrance histories are retained as an endpoint
error. That distinction matters when a later survival exponent is less
than one.

## 3. The killed slow process

Put physical time \(t=N\tau\) and \(c_N(\tau)=C_{N\tau}/N\). When the
slow state is \(A=a\), a \(B\) customer is created at aggregate rate

\[
 \alpha+\mu a.                                         \tag{3.1}
\]

It is normally removed by \(BC\to0\) at rate \(\beta Nc\). Before that
removal it converts \(B\to A\) with probability
\(\lambda/(\beta Nc)+O(N^{-2})\), or fires \(AB\to2B\) with probability
\(\nu a/(\beta Nc)+O(N^{-2})\). Over \(N\,d\tau\) units of physical
time these rare marked customers have order-one counts. Ordinary
customers give the deterministic \(C\)-loss: an \(A\to AB\) customer
is normally removed by \(BC\to0\), decreasing \(C\) by one, while an
environmental \(0\to BC\) customer returns with zero net change.

The standard stopped martingale calculation gives the following limit.

> **Proposition 3.1 (killed PDMP).** Until \(A=0\), or until fixed
> cutoffs \(A=K\), \(c=\rho\), \(c=M\), and \(\tau=T\), the conditional
> trigger trace converges to
> \[
> \begin{aligned}
>  {dc\over d\tau}&=-\mu A,\\
>  q(a,a+1)&={\lambda(\alpha+\mu a)\over\beta c},\\
>  q(a,a-1)&={\nu a(\alpha+\mu a)\over\beta c},
> \end{aligned}                                        \tag{3.2}
> \]
> begun from \((A,c)=(1,1)\), with \(0\) absorbing.

One proof contracts each \(B\)-customer at its next \(B\)-free
regeneration. On \(c\in[\rho,M]\), its lifetime has every moment
bounded by \(C_rN^{-r}\). The aggregate customer intensity has
polynomial moments on every fixed stopped slow horizon. Customer
overlaps, \(2B\to B\) reactions, and all additional marked reactions
then have \(o(1)\) contribution to the scaled generator and its quadratic
variation. The uncontracted physical endpoint differs from the
contracted endpoint by a tight number of \(B\) molecules and \(O(1)\)
in \(C\). These estimates also justify the three stopped boundaries.

Now make the random time change

\[
 ds={\alpha+\mu A\over\beta c}\,d\tau.                 \tag{3.3}
\]

In \(s\)-time, \(A\) is the immigration--death chain killed at zero:

\[
 q(a,a+1)=\lambda,\qquad q(a,a-1)=\nu a,\qquad a\ge1.  \tag{3.4}
\]

Let

\[
 T_0=\inf\{s:A_s=0\}.                                  \tag{3.5}
\]

The exponential Lyapunov function \(e^{\theta a}\), followed by a
geometric trial from a fixed finite set, proves

\[
 \mathbb E_1 e^{\varepsilon T_0}<\infty                \tag{3.6}
\]

for some \(\varepsilon>0\). In particular \(T_0<\infty\) almost surely.
Equation (3.2) becomes

\[
 {d\log c\over ds}
 =-{\beta\mu A_s\over\alpha+\mu A_s}.                  \tag{3.7}
\]

Thus the limiting terminal fraction is

\[
 R=\exp\left\{-\beta\int_0^{T_0}
          {\mu A_s\over\alpha+\mu A_s}\,ds\right\}.    \tag{3.8}
\]

The integral in (3.8) is finite by (3.6), and is strictly positive
because the chain starts at \(A=1\). This proves \(0<R<1\) almost surely
for every positive rate vector. The rate \(\delta\) cannot change this
leading sign: it enters only through fast-queue overlap terms which vanish
from (3.2).

For reference, \(u_a(p)=\mathbb E_aR^p\) is the minimal bounded solution
of the Feynman--Kac equations

\[
 0=\lambda(u_{a+1}-u_a)+\nu a(u_{a-1}-u_a)
   -p{\beta\mu a\over\alpha+\mu a}u_a,\qquad u_0=1.    \tag{3.9}
\]

Equation (3.8), rather than a finite truncation of (3.9), proves the
strict inequality \(0<u_1(p)<1\).

## 4. Drift coefficients

Let an episode stop at the first of the contracted base return, a fixed
slow horizon, or one of the localization boundaries in Proposition 3.1.
For a bounded continuous test function \(f\), first let \(N\to\infty\),
then remove the fixed cutoffs. Sections 2--3 give

\[
 N\left\{\mathbb E f(C_{\rm end}/N)-f(1)\right\}
 \longrightarrow {\lambda\over\beta}
       \left\{\mathbb E f(R)-f(1)\right\}.             \tag{4.1}
\]

For \(f(r)=r^p\), the positive-part uniform integrability in Section 5
extends (4.1) to every fixed \(p>0\), giving

\[
 \mathbb E(C_{\rm end}^p-N^p)
 ={\lambda\over\beta}N^{p-1}
       \{\mathbb ER^p-1\}+o(N^{p-1}).                  \tag{4.2}
\]

In particular,

\[
 \mathbb E(Q_{\rm end}^2-Q_0^2)
 ={\lambda\over\beta}N\{\mathbb ER^2-1\}+O(1),         \tag{4.3}
\]

where the \(O(1)\) allows the bounded endpoint contraction and the
untriggered histories. The coefficient is strictly negative.

Let

\[
 h_\theta(n)=\log(n!)-n\log\theta.                     \tag{4.4}
\]

Stirling's formula, (1.3), and the fact that the conditional inactive
endpoint cost is tight give

\[
 \mathbb E\{h_\theta(C_{\rm end})-h_\theta(N)\}
 ={\lambda\over\beta}\{\mathbb ER-1\}\log N+O(1).
                                                               \tag{4.5}
\]

Thus the same physical block has direct negative factorial-entropy drift.
The strict sign is independent of all six positive rate choices.

## 5. Duration, endpoints, and debt marks

### 5.1 What is and is not uniform

Before the trigger, the fast \(BC\to0\) race has duration \(O(N^{-1})\).
The trigger occurs with probability \(O(N^{-1})\). Conditional on it,
the physical duration is \(O(N)\), and its duration divided by \(N\) has
all fixed moments after localization; this follows from (3.6) and

\[
 {d\tau\over ds}={\beta c\over\alpha+\mu A}
 \le {\beta M\over\alpha+\mu}                         \tag{5.1}
\]

before killing. Therefore the *unconditional mean* episode duration is
uniformly bounded. Higher raw duration moments are not uniformly
integrable: their natural scale is

\[
 \mathbb E\tau_N^q=O(N^{q-1}),\qquad q>1.              \tag{5.2}
\]

No stronger statement is used.

Only positive endpoint excursions require uniform integrability. On a
fixed slow horizon, pathwise

\[
 C_t\le N+1+Y_\alpha(t),                               \tag{5.3}
\]

where \(Y_\alpha\) is a rate-\(\alpha\) Poisson process. Together with
the exponential tail in (3.6), (5.3) gives uniform integrability of every
fixed positive power of \(C_{\rm end}/N\). The fresh-customer
construction gives polynomial endpoint bounds for \(A+B\). Decrements
of \(C\) need no positive-part UI; hitting \(C\le\rho N\) is itself the
desired descent. Taking \(K,M,T\to\infty\) and then \(\rho\downarrow0\)
therefore preserves the negative coefficients in (4.2)--(4.5).

### 5.2 Reflected debt is not lost

The primary \(0\to BC\) entry creates one unit each of \(B\)- and
\(C\)-debt. If \(B\to A\) wins the fast race, the \(B\)-debt is cleared
and one unit of \(A\)-debt is created, while the old \(C\)-debt remains.
Thus the trigger transfers part of the physical carrier into the \(A\)
coordinate; it does not make the old debt disappear. Each eventual
\(AB\to2B\) reaction clears an \(A\)-unit, and ordinary \(BC\to0\)
reactions clear \(B\)- and \(C\)-units. At a contracted return to
\(A=B=0\), the \(A\)- and \(B\)-debts are zero exactly. The primary old
\(C\)-unit is consumed by the first genuinely unpaired \(BC\to0\)
service.

Aggregate reflected \(C\)-debt created later need not be zero merely from
the inequality \(C\le N\): late arrivals can sit above a previous running
minimum. Such residual debt is retained and handed to the next physical
block. A localization stop likewise retains every outstanding mark. No
localization or contraction conditions away either a mark or its clocks.

This debt bookkeeping is compatible with (2.3): the only possible
positive correction to \(Q\) is the rare \(2B\to B\) overlap, while the
macroscopic \(A\)-occupation produces the strict negative term.

## 6. Verdict

The equality of the shortest upward and downward word depths does not
produce a physical C3 in (1.1). The complete leading kernel, not a
selected word, has a rate-independent stabilizing sign:

\[
 \mathbb ER^p-1<0\qquad(p>0).                          \tag{6.1}
\]

What is proved here is a local, all-reactions-retained stopped trace with
explicit endpoint and duration costs. A claim of recurrence for the
support pair still requires composition with its two-active regions and
the global common-potential return theorem. No such promotion is made in
this note.
