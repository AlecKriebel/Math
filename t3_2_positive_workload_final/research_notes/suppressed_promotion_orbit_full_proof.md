# The suppressed four-pair promotion orbit

## 1. Exact scope and claim boundary

Up to the four species relabellings present in the ordered residual table,
consider

\[
 L_*=\{U,I+V\},\qquad L_-=\{0,I,2I,I+U\}.              \tag{1.1}
\]

The first linkage is reversible, and the second is given an arbitrary
strongly connected directed graph and arbitrary positive present rates. The
exact finite certificate finds four positive-invariant support pairs in this
orbit, with no overlap with any previously certified branch. Across those
four pairs there are exactly 28 affine-feasible failed incidences:

\[
\begin{array}{c|c|c}
(w_I,w_U,w_V)&\text{incidences}&\text{whole top}\\ \hline
(0,0,1)&12&\text{no}\\
(0,1,1)&4&\text{yes}\\
(0,1,2)&4&\text{no}\\
(0,1,3)&4&\text{no}\\
(0,4,5)&4&\text{no}.
\end{array}                                            \tag{1.2}
\]

The twelve one-active rows have fixed caps
\((I,U)=(0,0),(0,1),(0,2)\), once per support pair.

Throughout, a profile means an **exact D-tier** profile, not merely a
normalized logarithmic weight.  Thus, in the \((0,1,2)\) profile,
\(M^2/D\) stays in a compact subset of \((0,\infty)\).  If a subpower
factor makes this ratio tend to zero or infinity, the sequence refines the
D-tier and falls respectively into the \((0,1,3)\) or \((0,4,5)\)
profile.  This three-way split is load-bearing below.

This note proves recurrence for the exact four-pair orbit. Two independent
audits replayed the analytic stopping argument, exact selector, and
pair-level composition. No broader promotion family is claimed.

## 2. One potential and one exact shell invariant

Write the rates of \(U\to I+V\) and \(I+V\to U\) as
\(\alpha,\mu>0\). Choose a fixed vector \(\ell\) satisfying

\[
 \ell_I+\ell_V-\ell_U=\log(\mu/\alpha),                 \tag{2.1}
\]

and put

\[
 {\cal F}_\ell(x)=\log(I!)+\log(U!)+\log(V!)+\ell\cdot x.
\tag{2.2}
\]

After adding a constant, this is nonnegative and proper. The affine
correction (2.1) is the detailed-balance correction for \(L_*\), and it
does not alter any strict D-tier logarithmic gap.

The top linkage preserves

\[
 Q=U+2V-I.                                             \tag{2.3}
\]

The four lower complexes have \(Q\)-levels

\[
 q(0)=q(I+U)=0,\qquad q(I)=-1,\qquad q(2I)=-2.         \tag{2.4}
\]

Thus the apparently bad \(0\leftrightarrow I+U\) resets are exactly
\(Q\)-neutral. Every edge from
\({\mathsf N}:=\{0,I+U\}\) to
\({\mathsf D}:=\{I,2I\}\) strictly lowers \(Q\). Strong connectivity of
\(L_-\) guarantees at least one edge across this cut.

Start a top excursion from the core state

\[
 (I,U,V)=(0,M,D).                                      \tag{2.5}
\]

If one lower reaction fires during the excursion and all remaining
inactive molecules are then cleared by \(I+V\to U\), its exact core
endpoint and factorial reward are as follows:

\[
\begin{array}{c|c|c}
\text{lower edge}&(U_{\rm end},V_{\rm end})
 &\Delta{\cal F}_\ell\\ \hline
0\to I&(M+1,D-1)&
 \log\frac{M+1}{D}+\ell_U-\ell_V\\[2mm]
0\to2I&(M+2,D-2)&
 \log\frac{(M+1)(M+2)}{D(D-1)}
       +2(\ell_U-\ell_V)\\[2mm]
0\to I+U&(M+2,D-1)&
 \log\frac{(M+1)(M+2)}D+2\ell_U-\ell_V\\[2mm]
I+U\to0&(M-2,D+1)&
 \log\frac{D+1}{M(M-1)}+\ell_V-2\ell_U\\[2mm]
I+U\to I&(M-1,D)&-\log M-\ell_U\\[1mm]
I+U\to2I&(M,D-1)&-\log D-\ell_V .
\end{array}                                            \tag{2.6}
\]

These identities do not assume that the lower clock fires at \(I=1\).
Before that clock, the top shell has

\[
 U=M-I,\qquad V=D+I.                                   \tag{2.7}
\]

Substitution shows that clearing the remaining \(I\)'s gives exactly
(2.6), independently of the transient value of \(I\). The first two and
last two rows lower \(Q\); the middle reset pair preserves it.

## 3. The transient killed-shell occupation lemma

The only genuinely averaged flag is \((w_I,w_U,w_V)=(0,1,2)\); the same
estimate also repairs the originally suppressed \((0,4,5)\) flag.

> **Lemma 3.1 (top-shell occupation).** Suppose
> \(M,D\to\infty\), \(D/M\to\infty\), and
> \(R:=M^2/D\ge r_0>0\). Run only \(L_*\) from (2.5), and set
>
> \[
> h={T\over R}={TD\over M^2},\qquad
> J_h=\int_0^h I_t(M-I_t)\,dt.                         \tag{3.1}
> \]
>
> Then, for each fixed \(T>0\),
>
> \[
> J_h\longrightarrow{\alpha T\over\mu}
> \quad\text{in }L^1,\qquad
> {\mathbb E}\int_0^h\{I_t+(I_t)_2\}\,dt=O(M^{-1}).
> \tag{3.2}
> \]
>
> The transient \(I\)-population at a timeout or at a clock biased by
> \(I_t(M-I_t)\) has uniform exponential moments (the claim concerns
> shell excess, not the full \(U,V\) populations).

### Proof

On the top shell, \(I\) is the birth--death chain

\[
 i\longrightarrow i+1\ \text{ at rate }\alpha(M-i),
 \qquad
 i\longrightarrow i-1\ \text{ at rate }\mu i(D+i).
\tag{3.3}
\]

It is stochastically dominated by immigration--death with immigration
\(\alpha M\) and per-particle death \(\mu D\). Starting from zero, the
dominating law is Poisson with mean at most
\(\alpha M/(\mu D)\). Hence, for every fixed \(p\ge1\),

\[
 \sup_{t\ge0}{\mathbb E}I_t^p\le C_p{M\over D},
 \qquad
 {\mathbb E}\int_0^h I_t^p\,dt\le {C_{p,T}\over M}.
\tag{3.4}
\]

Let \({\cal M}_t\) be the martingale in the coordinate equation for \(I\).
At time \(h\),

\[
 \mu D\int_0^h I_t\,dt
 =\alpha Mh-\alpha\int_0^h I_t\,dt
  -\mu\int_0^h I_t^2\,dt+{\cal M}_h-I_h.              \tag{3.5}
\]

Multiplying by \(M/(\mu D)\) and subtracting
\(\int_0^h I_t^2dt\) gives

\[
\begin{split}
 J_h={\alpha M^2h\over\mu D}
 &-{\alpha M\over\mu D}\int_0^h I_t\,dt
  -\left(1+{M\over D}\right)\int_0^h I_t^2\,dt\\
 &+{M\over\mu D}({\cal M}_h-I_h).                     \tag{3.6}
\end{split}
\]

The first term is \(\alpha T/\mu\). Equations (3.4) make all deterministic
errors \(o_{L^1}(1)\). Moreover

\[
 {\mathbb E}\langle{\cal M}\rangle_h
 \le 2\alpha Mh=O(D/M),
\tag{3.7}
\]

so the martingale term in (3.6) has variance \(O(M/D)=o(1)\).
This proves (3.2). The same Poisson domination, followed by compensation
with a slightly smaller exponential parameter, gives the timeout and
size-biased endpoint assertion. \(\square\)

Let \(\Lambda_0\) be the aggregate rate of \(0\)-source lower edges,
\(\Lambda_U\) the aggregate coefficient of \(I+U\)-source edges, and
\(\Lambda_D\) the remaining \(I\)- and \(2I\)-source propensity. Conditional
on the top path,

\[
 \int_0^h\Lambda_U(t)\,dt=\kappa_UJ_h,\qquad
 {\mathbb E}\int_0^h\Lambda_D(t)\,dt=O(M^{-1}).
\tag{3.8}
\]

Thus the killed shell retains every lower clock: no reaction is deleted.

## 4. Physical cleanup and endpoint cost

> **Lemma 4.1 (return to the core).** Under the hypotheses of Lemma 3.1,
> after one bounded lower jump the chain reaches \(I=0\) by physical
> \(I+V\to U\) reactions before any further lower reaction, outside an
> event of probability \(o(1)\). The cleanup duration has every fixed
> scaled moment, and the exceptional positive factorial cost is uniformly
> integrable.

Indeed, while \(I\ge1\), the clearing rate is at least \(cDI\), whereas
the aggregate \(I+U\)-source rate is at most \(CMI\), and the
\(0,I,2I\)-source rates are at most \(C(1+I^2)\). Poisson domination from
Lemma 3.1 gives a geometric number of clearing steps and therefore

\[
 {\mathbb P}\{\text{lower interference during cleanup}\}
 \le C{M\over D}+{C\over D}=o(1).                     \tag{4.1}
\]

At an \(I+U\)-biased endpoint, the compensation estimate

\[
 {\mathbb E}\int_0^h e^{\theta I_t}
 I_t(M-I_t)\,dt\le C_T                               \tag{4.2}
\]

holds for a sufficiently small \(\theta>0\). For \(I\)- and \(2I\)-source
interference, (3.4) gives probability \(O(M^{-1})\); multiplying its
factorial cost by \(\log(M+D)\) still gives \(o(1)\) in every profile in
(1.2). These estimates prove the claimed endpoint uniform integrability.

## 5. Every failed flag

### 5.1 The twelve one-active rows

Here \(D=V\to\infty\), while \(M=U\in\{0,1,2\}\) and \(I=0\).
Strong connectivity gives a positive aggregate \(0\)-source rate. Retain
all clocks and stop at the first lower reaction, then append physical top
cleanup.  The desired event is that this first reaction has source \(0\).
Top excursions make the expected aggregate hazard of all nonzero-source
lower interruptions only \(O(D^{-1})\).  Every such bounded interruption
has positive reward at most \(O(\log D)\); in particular, the only row of
(2.6) with possibly positive reward is \(I+U\to0\).  Their total expected
positive contribution is therefore \(O(D^{-1}\log D)=o(1)\).
Whatever the \(0\)-source target, the exact table (2.6) gives

\[
 \Delta{\cal F}_\ell\le-\log D+O(1).                  \tag{5.1}
\]

Here the cleanup estimate is elementary and does not use the
\(M,D\to\infty\), \(R\ge r_0\) hypotheses of Lemma 4.1.  Immediately after
the bounded target, \(I\le4\) and \(U=O(1)\).  Each present \(I\) has top
death rate at least \(cD\), whereas all top births and all lower competitors
together have rate \(O(1+I^2)\).  Thus cleanup precedes interference with
probability \(1-O(D^{-1})\), its duration has moments \(O(D^{-m})\), and
the exceptional positive factorial contribution is
\(O(D^{-1}\log D)=o(1)\).  The initial wait has fixed exponential moments,
and the cleaned active endpoint changes by only \(O(1)\).

### 5.2 The whole-top profile \((0,1,1)\)

Now \(M\asymp D\asymp N\), and \(R=M^2/D\asymp N\). From the core, the
first top birth occurs before a \(0\)-source edge with probability
\(1-O(N^{-1})\). Starting at \(I=1\), run until either \(I\) returns to zero
or a lower reaction fires; an \(I+U\)-source edge is the successful lower
event, while every other lower event is retained as an exceptional
endpoint. All top rates and the \(I+U\)-source rate are of order \(N\), so

\[
 {\mathbb P}\{I+U\text{-source edge before }I=0\}\ge p>0,
 \qquad {\mathbb E}\tau^m=O(N^{-m}).                  \tag{5.2}
\]

This follows already by requiring the very next reaction to be an
\(I+U\)-source edge; additional top excursions only increase the success
probability. The rescaled birth--death chain has uniform exponential
moments for the transient \(I\) population (equivalently, for the excesses
of \(U,V\) relative to the shell parameters \(M,D\)); no uniform moment is
claimed for the full active populations.  Stop **at** the successful
\(I+U\)-source reaction;
no top-only cleanup is imposed in this equal-depth regime, because further
\(I+U\) clocks would be of the same order.  At a pre-jump state on the top
shell,

\[
 {\cal F}_\ell(i,M-i,D+i)-{\cal F}_\ell(0,M,D)
 =O\{1+i\log(i+1)\},                                  \tag{5.3}
\]

uniformly for \(M/D\) in a compact positive interval.  The exponential
endpoint bound therefore makes the expected top-shell cost \(O(1)\).
Each possible \(I+U\)-target has direct jump reward
\(-\log N+O\{1+\log(i+1)\}\).  Consequently

\[
 {\mathbb E}\Delta{\cal F}_\ell\le-p\log N+O(1).      \tag{5.4}
\]

A failed excursion returns to the exact starting core and costs zero.
Other lower sources have order one during an \(O(N^{-1})\) attempt and
contribute \(o(1)\).

### 5.3 The balanced killed shell \((0,1,2)\)

Here \(M\asymp N\), \(D\asymp N^2\), and
\(R=M^2/D\) stays in a compact subset of \((0,\infty)\). Put

\[
 a_0=\sum_{z\in{\mathsf D}}\kappa_{0z},\qquad
 a_U=\sum_{z\in{\mathsf D}}\kappa_{I+U,z}.             \tag{5.5}
\]

Strong connectivity implies \(a_0+a_U>0\). In the Lemma 3.1 window, the
cumulative service hazard is

\[
 A_{\rm s}(h)=a_0h+a_UJ_h.                             \tag{5.6}
\]

It is bounded below with positive probability, while the total
\({\mathsf N}\)-source cumulative hazard is bounded above with probability
arbitrarily close to one. Conditional Poisson clock calculus therefore
gives

\[
 {\mathbb P}\{\text{the first lower event is an }
 {\mathsf N}\to{\mathsf D}\text{ service}\}\ge p>0.    \tag{5.7}
\]

Explicitly, choose constants \(a,B>0\) for which
\({\mathbb P}\{A_{\rm s}(h)\ge a,\ A_{\rm all}(h)\le B\}\ge c>0\).
Conditional on the top path, the first-service probability is
\(\int_0^h e^{-A_{\rm all}(t)}dA_{\rm s}(t)\), hence it is at least
\(e^{-B}a\) on this event.  This proves (5.7) without an independence
assumption.

The \(I\)- and \(2I\)-source event probability is \(o(1)\) by (3.8).
Neutral \(0\leftrightarrow I+U\) endpoints preserve \(Q\) and have
\(O(1)\) factorial reward because \(R\asymp1\). Every service endpoint
satisfies, by (2.6),

\[
 \Delta{\cal F}_\ell\le-\log N+O(1).                  \tag{5.8}
\]

Thus one all-reactions-retained block has expected drift tending to
\(-\infty\), fixed physical duration, and uniform endpoint moments.

### 5.4 The source-dominant profile \((0,1,3)\)

Here \(R=M^2/D\to0\) and \(D/M\to\infty\). Wait for the first
lower reaction and append physical top cleanup; the desired first clock is
the independent aggregate \(0\)-source clock \(S\). Poisson domination
gives

\[
 {\mathbb E}\int_0^S I_t(M-I_t)\,dt\le C R=o(1)       \tag{5.9}
\]

for the independent exponential \(0\)-clock \(S\). Hence a lower
\(I+U\)-source edge intervenes with probability \(O(R)\). Every
\(0\)-target is favorable:

\[
 0\to I+U:\quad \Delta{\cal F}_\ell=\log R+O(1),
\qquad
 0\to{\mathsf D}:\quad
 \Delta{\cal F}_\ell\le-\log(D/M)+O(1).                \tag{5.10}
\]

The only potentially positive interruption is \(I+U\to0\), with cost
\(\log(1/R)+O(1)\); its expected contribution is
\(O(R\log(1/R))=o(1)\). Therefore the expected factorial drift tends to
\(-\infty\).

### 5.5 The originally suppressed profile \((0,4,5)\)

Now \(R=M^2/D\to\infty\). Use the short window \(h=T/R\) of Lemma 3.1.
The \(I+U\)-source cumulative hazard converges to a positive constant,
whereas the \(0\)-source hazard is \(O(R^{-1})\) and the
\(I,2I\)-source hazard is \(o(1)\). Thus, for some \(p>0\),

\[
 {\mathbb P}\{\text{an }I+U\text{-source edge fires by }h\}\ge p. \tag{5.11}
\]

All of its possible targets are favorable:

\[
\begin{array}{c|c}
\text{target}&\Delta{\cal F}_\ell\\ \hline
0&-\log R+O(1)\\
I&-\log M+O(1)\\
2I&-\log D+O(1).
\end{array}                                            \tag{5.12}
\]

Timeout followed by cleanup returns to the exact core and costs zero.
Equations (3.8), (4.1), and (5.11)--(5.12) give expected factorial drift
tending to \(-\infty\), duration \(O(R^{-1})\), and uniform scaled endpoint
moments.

## 6. Exact pair theorem

> **Theorem 6.1.** For either ordering of any support pair in the
> exact four-pair orbit (1.1), give both linkages arbitrary strongly
> connected directed graphs and arbitrary positive present rates. Then
> every closed irreducible population class is positive recurrent.

Fix one closed irreducible class \(\Gamma\). The finite certificate proves
that every affine-feasible failed descriptor is one of the profiles in
(1.2). Sections 5.1--5.5 give a physical stopping episode for all of them,
using the single proper potential (2.2). Every other realizable descriptor
passes the ordinary source-tier criterion, and the fixed affine correction
\(\ell\) preserves its strict logarithmic exit.

If the required drift and endpoint bounds failed outside every finite subset
of \(\Gamma\), a divergent bad sequence would have a subsequence realizing
one of the finitely certified descriptors, contradicting the corresponding
estimate above. The common-potential physical-time gluing theorem therefore
gives finite mean hitting of one finite subset of \(\Gamma\).

Nonexplosion is immediate: every reaction which increases total population
has source molecularity at most one, so the positive total-population drift
is bounded by \(C(1+|x|)\). Local finiteness and finite mean return from the
finite target give positive recurrence.

The exact four pairs are positive-invariant and disjoint from all prior
ordered branches. The two independent audits certify the disjoint
arithmetic

\[
 (1839,187)\longmapsto(1835,187).                      \tag{6.1}
\]

Global T3-2 remains uncertified.

## 7. Independent-audit record

Both independent replays checked:

1. the exact macro endpoints and rewards in (2.6), including transient
   \(I>1\);
2. the martingale identity (3.6), its uniform error bounds, and size-biased
   exponential moments;
3. physical cleanup with every lower clock retained;
4. the cut-hazard lower bound (5.7) for every strong orientation;
5. propensity-times-log uniform integrability in the \(R\to0\) and
   \(R\to\infty\) regimes;
6. the common-\({\cal F}_\ell\) passing-cone composition and exact
   four-pair disjointness.

All six obligations passed. One review is recorded in
`research_notes/suppressed_promotion_orbit_independent_audit.md`; the second
independently replayed the current theorem and executable selector. The
analytic and exact pair-level flags are true only for these four pairs; the
global flag remains false.
