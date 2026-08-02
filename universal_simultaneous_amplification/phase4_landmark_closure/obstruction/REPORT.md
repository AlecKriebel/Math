# Phase 4 obstruction route: universal local tradeoffs and the bottleneck gap

Date: 2026-08-01 (America/Los_Angeles)

No literature search or external contact was used. The inherited fixed-graph,
support-degree, and finite-type results are treated as proved facts and are
not rederived here.

This report does **not** prove Alternative O. It proves several new universal
reductions and isolates the unresolved gap. The proved fixation controls are
local or exact drift identities; the branching statements concern only
separately defined abstract processes. A vanishing-weight modular cut can
retain an order-one relative bias not captured by the local controls.

## Retraction notice

An earlier version labelled the proposed genealogy domination in Section 4
as proved. It is false. The independently audited center--singular-triangle
family has `rho_dB(G_N,r)->1/3`, contradicting the claimed bound
`limsup rho_dB<=1-1/r` whenever `1<r<3/2`.

The error is joint, not marginal. In one replacement event, a birth of one
lineage is simultaneously the death of another lineage. Although each
lineage's marginal birth intensity has the displayed upper bound, those birth
events cannot be coupled to independent Poisson birth clocks while also
retaining independent exponential lifetimes. Filling a nearly closed module
with one ancestry makes the failure transparent: every descendant death is
paired with a descendant birth, so that ancestry can persist even when the
proposed independent branching envelope becomes extinct.

Equations for the separately defined abstract branching processes remain
valid algebra. They are not fixation bounds. Sections 2, 3, 5, 6, 7, and 8.1
do not use the invalid coupling and retain their stated status.

## 1. Notation

Let

$$
d_i=\sum_j w_{ij},\qquad
P_{ij}=\frac{w_{ij}}{d_i},\qquad
t_i=\sum_j P_{ji}.
\tag{1}
$$

Thus $P$ is row-stochastic and $t_i$ is its $i$th column sum (the
temperature of vertex $i$). In particular,

$$
\frac1n\sum_i t_i=1.
\tag{2}
$$

For dB put

$$
\lambda_i(r)=\sum_{j\ne i}
\frac{rP_{ji}}{1+(r-1)P_{ji}},
\qquad
c(G)=\frac1n\sum_{i,j}P_{ji}^2.
\tag{3}
$$

The quantity $c(G)$ is the average Simpson concentration of normalized
incoming influence. Unlike support degree, it does not count arbitrarily
small completion edges as full neighbors.

## 2. [PROVED] Exact singleton first-change tradeoff

### Theorem 2.1

Starting with the unique mutant at $i$, the probability of reaching two
mutants before extinction is exactly

$$
q_i^{\rm Bd}(r)=\frac{r}{r+t_i},
\qquad
q_i^{\rm dB}(r)=\frac{\lambda_i(r)}{1+\lambda_i(r)}.
\tag{4}
$$

Consequently, under uniform singleton initialization,

$$
\boxed{
\frac1n\sum_iq_i^{\rm Bd}(r)\ge\frac{r}{r+1}
\quad\text{and}\quad
\frac1n\sum_iq_i^{\rm dB}(r)\le\frac{r}{r+1}.}
\tag{5}
$$

The Bd excess has the exact representation

$$
\frac1n\sum_iq_i^{\rm Bd}(r)-\frac{r}{r+1}
=\frac{r}{(r+1)^2}\frac1n\sum_i
\frac{(t_i-1)^2}{r+t_i}.
\tag{6}
$$

For dB,

$$
\overline\lambda
=r-\frac{r(r-1)}n\sum_{i,j}
\frac{P_{ji}^2}{1+(r-1)P_{ji}}
\le r-(r-1)c(G),
\tag{7}
$$

and therefore

$$
\frac1n\sum_iq_i^{\rm dB}(r)
\le
\frac{r-(r-1)c(G)}{1+r-(r-1)c(G)}.
\tag{8}
$$

#### Proof

For Bd, while the state is the singleton $\{i\}$, an effective upward move
has transition mass $r/F$, where $F=n-1+r$. The effective downward mass is

$$
\frac1F\sum_j\frac{w_{ji}}{d_j}=\frac{t_i}{F}.
$$

Deleting self-loops proves the first formula in (4).

For dB, Poissonize so that each target dies at rate one. The initial mutant
dies at rate one. If $j\ne i$ dies, the mutant wins the vacancy with
probability

$$
\frac{rw_{ij}}{d_j+(r-1)w_{ij}}
=\frac{rP_{ji}}{1+(r-1)P_{ji}}.
$$

Its total birth rate is $\lambda_i(r)$, proving the second formula in (4).

The map $t\mapsto r/(r+t)$ is convex, while $x\mapsto x/(1+x)$ is concave.
Equation (2), the identities $\sum_iP_{ji}=1$, and

$$
\sum_i\frac{rP_{ji}}{1+(r-1)P_{ji}}\le r
$$

give (5). Subtracting the tangent at $t=1$ gives (6) exactly. Finally,

$$
r-\overline\lambda
=\frac{r(r-1)}n\sum_{i,j}
\frac{P_{ji}^2}{1+(r-1)P_{ji}}
\ge(r-1)c(G),
$$

and another use of concavity proves (8). ∎

This is a scale-invariant local tradeoff, but not yet a fixation tradeoff:
reaching two mutants is only a necessary establishment event.

## 3. [PROVED] Weight-sensitive structure forced by all-fitness dB amplification

### Theorem 3.1

Suppose $G_n$ dB-amplifies the complete graph eventually at every fixed
$r>1$. Then

$$
\boxed{c(G_n)\longrightarrow0}
\tag{9}
$$

and, for a uniformly sampled vertex $I_n$,

$$
\boxed{t_{I_n}\longrightarrow1\quad\text{in }L^1.}
\tag{10}
$$

Thus normalized influence must be locally diffuse, and its row and column
sums must agree asymptotically at a uniform vertex.

#### Proof of (9)

Fix $r>1$. Fixation must pass through two mutants, so Theorem 2.1 and dB
amplification imply

$$
\frac{1}{1+r-(r-1)c(G_n)}
\le \frac1n\sum_i\frac1{1+\lambda_i(r)}
<1-\rho_{\rm dB}(K_n,r).
\tag{11}
$$

The complete-graph extinction probability on the right tends to $1/r$.
Therefore

$$
\limsup_{n\to\infty}c(G_n)\le\frac1{r-1}.
\tag{12}
$$

This holds for every arbitrarily large *fixed* $r$. Sending $r$ to infinity
after taking the population limit proves (9); the two limits are not
exchanged.

#### Proof of (10)

Since $\lambda_i(r)\le rt_i$, the same first-change argument gives, for every
fixed $r>1$,

$$
\limsup_{n\to\infty}
\frac1n\sum_i\frac1{1+rt_i}\le\frac1r.
\tag{13}
$$

The empirical laws of $t_i$ are tight because they are nonnegative and have
mean one. Take any weakly convergent subsequence and call its limit $T$.
Bounded-continuous convergence in (13) gives

$$
E\frac1{1+rT}\le\frac1r
\qquad\text{for every fixed }r>1.
$$

Multiply by $r$ and use monotone convergence as $r\to\infty$. This gives
$E(1/T)\le1$, with $1/0=+\infty$. Truncation of the first moment gives
$ET\le1$, whereas Jensen gives

$$
E(1/T)\ge1/(ET)\ge1.
$$

Every equality condition is forced, so $T=1$ almost surely. Thus
$t_{I_n}\to1$ in probability. Since $Et_{I_n}=1$,

$$
E|t_{I_n}-1|=2E(1-t_{I_n})_+\longrightarrow0,
$$

which proves $L^1$ convergence. ∎

This closes the tiny-edge support-completion loophole at the local influence
level. It does not control the ratio across a cut whose total normalized
weight also tends to zero; Section 7 makes that limitation explicit.

## 4. [RETRACTED] Proposed total-genealogy bounds

Put

$$
h_r(z)=\frac{1+r-\sqrt{(1+r)^2-4rz}}{2r},
\qquad 0<z<1.
\tag{14}
$$

This is the smaller solution of

$$
h=\frac{z}{1+r(1-h)}.
\tag{15}
$$

### False claim 4.1 (retained for diagnosis)

The earlier version claimed that every connected undirected weighted graph of
order $n$ satisfies

$$
\boxed{
\rho_{\rm dB}(G,r)
\le\frac{1-h_r(z)}{1-z^n}}
\qquad(0<z<1).
\tag{16}
$$

Writing

$$
\eta(G)=\frac1n\sum_i|t_i-1|,
$$

and also

$$
\boxed{
\rho_{\rm Bd}(G,r)
\le\frac{1-h_r(z)+\eta(G)}{1-z^n}.}
\tag{17}
$$

The claimed consequences were, for every graph family and fixed $r>1$,

$$
\limsup_n\rho_{\rm dB}(G_n,r)\le1-\frac1r.
\tag{18}
$$

If the family satisfies the all-fixed-fitness dB-amplification hypothesis,
then Theorem 3.1 and (17) additionally give

$$
\limsup_n\rho_{\rm Bd}(G_n,r)\le1-\frac1r.
\tag{19}
$$

Since both complete-graph baselines tend to $1-1/r$, every hypothetical
asymptotically universal simultaneous amplifier must satisfy

$$
\boxed{
\rho_{\rm Bd}(G_n,r),\ \rho_{\rm dB}(G_n,r)
\longrightarrow1-\frac1r}
\tag{20}
$$

for every fixed $r>1$.  Statements (16)--(20) are false.

#### Invalid genealogical-domination step

Label a mutant lineage from the instant it is created until its vertex is
next replaced. Replacing a mutant by another mutant ends the old lineage and
creates a child lineage, so it is counted in the total genealogy even though
the mutant set does not change.

For dB, each lineage has a rate-one target-death lifetime. While a type-$i$
lineage is alive, its rate of producing a type-$j$ child is

$$
\frac{rw_{ij}}{d_j+(r-1)m_j(S)}\le rP_{ji}.
\tag{21}
$$

The attempted argument stopped the genealogy on first producing $n$ lineages
and revealed its family tree breadth first.  It then tried to attach fresh
independent Poisson birth envelopes to every lineage.  This is invalid.  A
child event of one lineage is simultaneously the target-death event of
another lineage.  The marginal intensity bound (21) does not make those
birth envelopes independent of all lineage lifetimes, so the claimed
injection into an independent multitype branching tree does not follow.

For Bd, give residents reproduction clocks of rate one and mutants clocks of
rate $r$. A type-$i$ mutant produces type-$j$ children at rate $rP_{ij}$.
Its vertex is targeted at total rate

$$
\sum_u f_uP_{ui}\ge\sum_uP_{ui}=t_i,
$$

so its lifetime is dominated by an exponential lifetime of rate $t_i$.
The same dependence invalidates the proposed Bd coupling.

Fixation does require at least $n$ total genealogical lineages, but without a
valid domination this gives no branching upper bound.

#### Valid PGF algebra for separately defined branching processes

For the proposed dB comparison branching process, let $g_i(z)=E_i z^T$, with
$z^\infty=0$, where $T$ is total progeny. Conditioning on the exponential
lifetime gives

$$
g_i(z)=\frac{z}{1+r(P^{\mathsf T}(1-g))_i}.
\tag{22}
$$

If $\bar g=n^{-1}\sum_i g_i$, column stationarity and convexity give

$$
\bar g\ge\frac{z}{1+r(1-\bar g)}.
$$

The larger root of the corresponding quadratic exceeds one for $z<1$, so
$\bar g\ge h_r(z)$.

For the proposed Bd comparison process, its PGFs $q_i$ satisfy

$$
q_i(z)=\frac{zt_i}{t_i+r(P(1-q))_i}.
\tag{23}
$$

Under the probability weights $\mu_i=t_i/n$, Jensen gives

$$
\bar q_\mu\ge\frac{z}{1+r(1-\bar q_\mu)},
\qquad
\bar q_\mu\ge h_r(z).
$$

Since $0\le q_i\le1$, the uniform average obeys
$\bar q\ge h_r(z)-\eta(G)$.

For a genuinely dominated tree one could finally use

$$
1-z^T\ge(1-z^n)\mathbf1_{\{T\ge n\}},
$$

but the missing domination means this proves none of (16)--(20) for fixation.

The earlier claimed finite-size consequence

$$
\rho_{\rm dB}(G,r)
\le1-\frac1r+O_r\!\left(\frac{\log n}{n}\right).
\tag{24}
$$

is therefore retracted.

For clarity, direct solution of the one-dimensional complete-graph chain
gives the exact baselines

$$
\rho_{\rm Bd}(K_n,r)
=\frac{1-r^{-1}}{1-r^{-n}},
\qquad
\rho_{\rm dB}(K_n,r)
=\frac{(1-r^{-1})(1-n^{-1})}{1-r^{1-n}}.
\tag{24a}
$$

Indeed, for dB the down/up ratio at mutant count $k$ is

$$
\gamma_k=\frac1r
\frac{n-1+(r-1)k}{n-r+(r-1)k},
$$

and its products telescope after writing
$x=(n-r)/(r-1)$:

$$
\prod_{j=1}^k\gamma_j
=r^{-k}\frac{x+k+1}{x+1}.
$$

Summing the standard birth--death absorption formula yields (24a).  Thus,
with $a=1-r^{-1}$,

$$
\rho_{\rm Bd}(K_n,r)=a+O_r(r^{-n}),
\qquad
\rho_{\rm dB}(K_n,r)=a-\frac an+O_r(r^{-n}).
\tag{24b}
$$

Equation (24b) records the exact baseline scale, but the retracted PGF method
does not bound fixation at any scale.  Within that failed method alone,
optimizing the formal right side of (16) would leave a logarithm: with
$z=e^{-x/n}$, the two formal errors are proportional to $e^{-x}$ and $x/n$.
This observation has no fixation consequence.

## 5. [PROVED FOR ABSTRACT BRANCHING PROCESSES] A survival tradeoff

Let $S$ be the uniform mean survival probability of the dB branching process
with birth $rP^{\mathsf T}$ and death one. Let $B$ be the uniform mean
survival probability of the Bd branching process with birth $rP$ and
type-$i$ death $t_i$. Put

$$
a=1-\frac1r,\qquad
\delta=a-S,\qquad
g=(B-a)_+.
$$

### Theorem 5.1

For every finite row-stochastic $P$ with positive column sums,

$$
\boxed{
S\le a,\qquad
\delta\ge
\frac{4a}{(2r+\sqrt r+1)^2}\,g^2.}
\tag{25}
$$

#### Proof

Write $s_i$ for dB branching survival. Its fixed-point equations are

$$
\frac{s_i}{1-s_i}=r(P^{\mathsf T}s)_i.
\tag{26}
$$

Uniform averaging gives

$$
E\frac{s}{1-s}=rS,
\tag{27}
$$

and Jensen yields $S\le a$. The exact tangent remainder at $S$ is

$$
E\frac{(s-S)^2}{1-s}=rS\delta(1-S),
\qquad
E\frac1{1-s}=1+rS.
\tag{28}
$$

Define $F(x)=x/[r(1-x)]$. Equation (26) is
$P^{\mathsf T}s=F(s)$, and

$$
F(s)-a=\frac{s-a}{1-s}.
\tag{29}
$$

Since $t=P^{\mathsf T}\mathbf1$ and $P^{\mathsf T}$ contracts normalized
$L^1$,

$$
aE|t-1|
\le E|F(s)-a|+E|s-a|.
\tag{30}
$$

Equations (28)--(29) and Cauchy--Schwarz give

$$
E|s-a|\le\sqrt{rS(1-S)\delta}+\delta,
\tag{31}
$$

$$
E|F(s)-a|
\le\sqrt{rS(1-S)(1+rS)\delta}+\delta(1+rS).
\tag{32}
$$

Now write $b_i$ for Bd branching survival. Its equations imply

$$
E\!\left[t\frac{b}{1-b}\right]=rE[tb].
$$

Jensen under the probability weights $t_i/n$ gives $E[tb]\le a$. Therefore

$$
g\le E[(1-t)b]\le\frac12E|t-1|.
\tag{33}
$$

Use $S(1-S)\le a$, $1+rS\le r$, and $\delta\le a$ in
(30)--(33). This yields

$$
g\le\frac{2r+\sqrt r+1}{2\sqrt a}\sqrt\delta,
$$

which is (25). ∎

Theorem 5.1 is a genuine quantitative tradeoff between the two separately
defined abstract branching processes. Because Section 4's domination is
false, it currently has no proved implication for fixation.

## 6. [PROVED FOR ABSTRACT BRANCHING PROCESSES] Sharper local perturbative tradeoff

Let $P_0$ be symmetric, doubly stochastic, and loopless. Consider an analytic
row-stochastic perturbation $P_\varepsilon$ arising from an undirected
weighting, and write

$$
t(\varepsilon)=\mathbf1+\varepsilon h+O(\varepsilon^2),
\qquad
\langle h,\mathbf1\rangle=0.
$$

Set

$$
x=a(rI-P_0)^{-1}h.
\tag{34}
$$

The matrix $rI-P_0$ is invertible for every $r>1$, without a mixing
spectral-gap assumption. Direct expansion of the two branching fixed-point
systems gives

$$
S(\varepsilon)
=a-\frac{r^2}{r-1}\langle x,x\rangle\varepsilon^2
+O(\varepsilon^3),
\tag{35}
$$

$$
B(\varepsilon)
=a-\frac{r}{r-1}\langle x,P_0x\rangle\varepsilon^2
+O(\varepsilon^3).
\tag{36}
$$

Here $\langle\cdot,\cdot\rangle$ is the uniform normalized inner product.
Thus a positive second-order Bd branching gain requires
$\langle x,P_0x\rangle<0$, and then

$$
\boxed{
\text{dB branching loss}\ \ge\
r\,\text{Bd branching gain}
\quad\text{at second order}.}
\tag{37}
$$

Indeed, the spectrum of $P_0$ lies in $[-1,1]$. Equation (35) follows from
the exact Jensen remainder in (28). For (36), if
$b=a+\varepsilon y+\varepsilon^2z+\cdots$, then $y=-x$, while

$$
E\!\left[t\left(\frac{b}{1-b}-rb\right)\right]=0
$$

gives

$$
\langle z,\mathbf1\rangle
=-\frac{r}{r-1}\langle y,P_0y\rangle.
$$

This is an abstract branching heterogeneity tradeoff in a full neighborhood
of a regular kernel. It is not a fixation theorem and still does not cover
singular weak-cut perturbations.

## 7. [PROVED FAILURE OF A LOCAL-TO-GLOBAL INFERENCE] Weak cuts retain order-one bias

For a mutant set $S$, put

$$
A(S)=\sum_{i\in S,j\notin S}P_{ij},
\qquad
B(S)=\sum_{i\in S,j\notin S}P_{ji}.
$$

Then

$$
\boxed{B(S)-A(S)=\sum_{i\in S}(t_i-1).}
\tag{38}
$$

The Bd down/up ratio at $S$ is $B(S)/(rA(S))$. Equation (38) shows why
Theorem 3.1 is insufficient: an $L^1$-small numerator can be comparable with
an even smaller cut.

For an explicit witness, take two $m$-vertex cliques $A,B$. Give every
internal $A$-edge weight $\alpha_A/(m-1)$, every internal $B$-edge weight
$\alpha_B/(m-1)$, and every cross edge weight
$\varepsilon_m/m^2>0$, where $0<\varepsilon_m\le1$. Then

$$
\eta(G_{2m})=O(\varepsilon_m/m),
\qquad
c(G_{2m})=O(1/m),
$$

but across the $A|B$ cut,

$$
\frac{B(A)}{A(A)}
\longrightarrow\frac{\alpha_A}{\alpha_B}.
\tag{39}
$$

The limiting relative cut bias is arbitrary although both local defects
vanish. This example is not claimed to amplify either rule. It proves that
no argument based only on $\eta(G)$ and $c(G)$ can close the theorem. A
successful obstruction must also control a hierarchy of vanishing cuts or
prove that their dB post-establishment effect has the wrong sign.

## 8. Hierarchical cut test and branching conjecture

### 8.1 [PROVED] Exact statewise cut-bias envelope

There is one further exact inequality relevant to arbitrary hierarchies.  For
a mutant set $S$, let $x=P\mathbf1_S$ and retain $A(S),B(S)$ from Section 7.
Deleting ineffective transitions gives

$$
R_{\rm Bd}(S)
:=\frac{T^+_{\rm Bd}(S)}{T^-_{\rm Bd}(S)}
=r\frac{A(S)}{B(S)},
\tag{40}
$$

whereas

$$
R_{\rm dB}(S)
=r\frac{\displaystyle\sum_{i\notin S}
 x_i/[1+(r-1)x_i]}
{\displaystyle\sum_{i\in S}
 (1-x_i)/[1+(r-1)x_i]}.
\tag{41}
$$

Since $1\le1+(r-1)x_i\le r$,

$$
\boxed{
R_{\rm dB}(S)\le r^2\frac{B(S)}{A(S)},
\qquad
R_{\rm Bd}(S)R_{\rm dB}(S)\le r^3.}
\tag{42}
$$

In particular, at least one rule has one-step forward bias at most
$r^{3/2}$.  This does **not** furnish a fixed-$r$ obstruction.  On a sharp
weak cut, $x_i\to1$ on the mutant side and $x_i\to0$ on the resident side,
so (42) is asymptotically sharp.  Choosing $A/B\sim\sqrt r$ makes both rules'
macro-level biases approach $r^{3/2}>r$.  Thus arbitrary hierarchical
families cannot be excluded by multiplying their cut-crossing biases.  The
remaining quantity that would need control is the uniform mass of initial
vertices whose descendants reach such an established module.

### 8.2 [NUMERICALLY OBSERVED, NOT USED] Branching level conjecture

Small multitype branching computations suggest

$$
\frac1n\sum_i
\Pr_i\{\text{hit population }K\text{ before zero}\}
\le\frac{1-r^{-1}}{1-r^{-K}}
\tag{43}
$$

for every column-stochastic birth kernel with death rate one. Random tests
covered up to four types and $K=6$. No proof was found. Even (43), by itself,
would be only a statement about the abstract branching process.  Without a
valid coupling it gives no fixation upper bound at all.  Mutant-to-mutant
replacement simultaneously terminates one lineage and creates another, so
the independent lifetime structure required by the linear branching process
is lost.  As Section 4 explains, this blocks even total-progeny domination,
not merely active-population domination.

Random full-chain searches found no fixed-$r$ universal inequality strong
enough to close that window. These computations are conjecture generation
only.

## 9. [PROVED] Coupling-free drift and occupation identities

Put

$$
\mathcal V=\sum_i d_i,
\qquad
H=\sum_i\frac1{d_i},
\qquad
D(S)=\sum_{i\in S}d_i,
\qquad
X(S)=\sum_{i\in S}\frac1{d_i}.
\tag{44}
$$

For $m_v(S)=\sum_{u\in S}w_{uv}$ and $x_v=m_v(S)/d_v$, define

$$
\Psi_D(S)=\sum_v
\frac{d_vx_v(1-x_v)}{1+(r-1)x_v},
\qquad
\Psi_B(S)=\sum_{u\in S,v\notin S}
\frac{w_{uv}}{d_ud_v}.
\tag{45}
$$

### Theorem 9.1

For every nonabsorbing state $S$,

$$
\boxed{
E_{\rm dB}[D(S_{t+1})-D(S_t)\mid S_t=S]
=\frac{r-1}{n}\Psi_D(S),}
\tag{46}
$$

and

$$
\boxed{
E_{\rm Bd}[X(S_{t+1})-X(S_t)\mid S_t=S]
=\frac{r-1}{n+(r-1)|S|}\Psi_B(S).}
\tag{47}
$$

Both drifts are nonnegative.  If $\tau$ is absorption time and expectation
starts from a uniformly sampled singleton, summing the stopped drifts gives
the exact fixation representations

$$
\boxed{
\rho_{\rm dB}(G,r)
=\frac1n+\frac{r-1}{n\mathcal V}
E_{\rm dB}\sum_{t<\tau}\Psi_D(S_t),}
\tag{48}
$$

$$
\boxed{
\rho_{\rm Bd}(G,r)
=\frac1n+\frac{r-1}{H}
E_{\rm Bd}\sum_{t<\tau}
\frac{\Psi_B(S_t)}{n+(r-1)|S_t|}.}
\tag{49}
$$

#### Proof

Under dB, conditional on target $v$, its new type is mutant with probability

$$
f_r(x_v)=\frac{rx_v}{1+(r-1)x_v}.
$$

Thus the expected degree-mass change is
$n^{-1}\sum_vd_v(f_r(x_v)-\mathbf1_{v\in S})$.  Undirectedness gives

$$
\sum_vd_vx_v
=\sum_v\sum_{u\in S}w_{uv}
=\sum_{u\in S}d_u=D(S).
$$

Using

$$
f_r(x)-x=\frac{(r-1)x(1-x)}{1+(r-1)x}
$$

proves (46).  For Bd, pair the two orientations of every cut edge
$uv$, with $u\in S$ and $v\notin S$.  Mutant reproduction along the edge
has probability $rw_{uv}/([n+(r-1)|S|]d_u)$ and increases $X$ by $1/d_v$;
the reverse resident event has probability
$w_{uv}/([n+(r-1)|S|]d_v)$ and decreases $X$ by $1/d_u$.  Their difference is

$$
\frac{r-1}{n+(r-1)|S|}\frac{w_{uv}}{d_ud_v},
$$

which proves (47).  At absorption, $D$ is $0$ or $\mathcal V$, and $X$ is
$0$ or $H$.  Their uniform-singleton initial means are respectively
$\mathcal V/n$ and $H/n$.  Optional summation of the bounded stopped
submartingales proves (48)--(49). ∎

These identities involve the actual replacement chains and no independent
lineage construction.  They reduce a universal tradeoff to comparison of two
different occupation measures of the nonnegative boundary functionals
$\Psi_D$ and $\Psi_B$.  No valid comparison between those occupation measures
is presently known; sharp weak cuts make their pointwise ratio singular.

## 10. [EXACT DIAGNOSTIC, NOT A LANDMARK OUTCOME] A dB inequality for weighted triangles

Let $L$ be an arbitrary triangle with positive edge weights and weighted
degrees $d_1,d_2,d_3$.  Write

$$
\alpha_D(s)=\frac13\sum_{i=1}^3\phi_i^{\rm dB}(L,s),
\qquad
H_L=\sum_{i=1}^3\frac1{d_i},
\qquad
I_D(s)=\sum_{i=1}^3\frac{\phi_i^{\rm dB}(L,s)}{d_i},
\tag{50}
$$

where $\phi_i^{\rm dB}(L,s)$ is dB fixation from a mutant initially at $i$.

### Diagnostic proposition 10.1

For every positively weighted triangle and every $r\ge3/2$,

$$
\boxed{
H_L\left[\alpha_D(r)-\left(1-\frac1r\right)\right]
\le \frac{I_D(1/r)}{r^2}.}
\tag{51}
$$

The threshold is sharp for this inequality.  For the singular family with
edge weights $(\varepsilon,1,\varepsilon)$,

$$
\lim_{\varepsilon\downarrow0}
\frac1{H_L}
\left\{
\frac{I_D(1/r)}{r^2}
-H_L\left[\alpha_D(r)-\left(1-\frac1r\right)\right]
\right\}
=\frac{2r-3}{3r}.
\tag{52}
$$

Hence (51) fails along positive weighted triangles for every $1<r<3/2$.

#### Exact proof certificate

Put edge weights $a,b,c>0$.  Build the six transient subset equations
directly from the dB rule, solve them over
$\mathbb Q(a,b,c,r)$, and denote the difference between the right and left
sides of (51) by $D(a,b,c,r)$.  Exact cancellation gives

$$
D(a,b,c,r)=\frac{N(a,b,c,r)}{Q(a,b,c,r)},
$$

where every coefficient of $Q$ is positive.  After writing
$r=3/2+u$, the polynomial

$$
N(a,b,c,3/2+u)
$$

has exactly 261 monomials in $a,b,c,u$, all with strictly positive rational
coefficients.  Therefore $D>0$ for $a,b,c>0$ and $u\ge0$, proving (51).
Direct symbolic limits give (52).  The independent verifier constructs the
chain rather than importing a declared fixation formula.

Inequality (51) is a genuine fixation result and uses no branching coupling,
but it concerns only three-vertex gadgets.  The mission explicitly excludes
further finite-triangle classification as a primary route, so this is
recorded only as a sharp diagnostic for the center--satellite mechanism.  It
is not an upper bound on $R_{\rm sim}$ and is not presented as a landmark
outcome.

## 11. [PROVED] Exact additive duals and stationary-set reductions

The invalid genealogy coupling in Section 4 tried to replace interacting
ancestries by independent particles.  There is nevertheless an exact
set-valued dual which keeps every coalescence and every joint update.  This
dual gives a second coupling-free formulation of the open obstruction.

Write a type configuration as a Boolean vector.  For Bd, multiplying all
transition probabilities at a state by the common positive factor
$n+(r-1)|S|$ does not change hitting probabilities.  The resulting
continuous-time process has, for every oriented edge $u\to v$,

* a neutral copying arrow at rate $P_{uv}$, sending the type at $u$ to $v$;
* a selective arrow at rate $(r-1)P_{uv}$, which changes $v$ to mutant if
  $u$ is mutant and otherwise does nothing.

The first Boolean map is copying and the second is the OR map
$y_v\leftarrow y_v\mathbin\vee y_u$.  Their exact backward actions on a
nonempty test set $A$ are respectively

$$
A\longmapsto (A\setminus\{v\})\cup\{u\},
\qquad
A\longmapsto A\cup\{u\},
\tag{53}
$$

when $v\in A$; if $v\notin A$, the test set is unchanged.

For dB let $K$ have the geometric law

$$
\Pr(K=k)=\frac1r\left(1-\frac1r\right)^{k-1},
\qquad k\ge1.
\tag{54}
$$

If $x$ is the mutant $P$-mass among the neighbors of the death vertex, then

$$
1-E(1-x)^K=\frac{rx}{1+(r-1)x}.
\tag{55}
$$

Thus a dB update can be generated exactly by sampling $K$ neighbors
independently from the row $P_{v\cdot}$ and setting the new type at $v$ to
the OR of their types.  Its backward action is

$$
A\longmapsto
(A\setminus\{v\})\cup\{U_1,\ldots,U_K\}
\quad (v\in A).
\tag{56}
$$

These are finite branching--coalescing *set chains*, not independent-family
branching processes.

### Theorem 11.1 (stationary dual representation)

For either rule $U$, let $\Pi_U^r$ be the unique limiting stationary law of
the corresponding dual started from a nonempty subset.  (For dB the full
test set is transient, because a death vertex cannot sample itself.)  Then,
for every mutant set $S$,

$$
\phi_U(S,r)=\Pr_{A\sim\Pi_U^r}(A\cap S\ne\varnothing).
\tag{57}
$$

Consequently,

$$
\boxed{
\rho_U(G,r)=\frac1nE_{\Pi_U^r}|A|.}
\tag{58}
$$

For either rule there is also the exact boundary identity

$$
\boxed{
\phi_i^{U}(G,1/r)=
\Pr_{A\sim\Pi_U^r}(A=\{i\}).}
\tag{59}
$$

#### Proof

Each map above satisfies the deterministic intersection duality

$$
\mathbf1\{\Phi(y)\cap A\ne\varnothing\}
=\mathbf1\{y\cap\Phi^*(A)\ne\varnothing\}.
$$

Composition through the graphical construction therefore gives the same
identity in expectation at every finite time.  The forward process absorbs
at the all-resident or all-mutant configuration.  Connectedness and the
positive probabilities of $K=1$ and $K=2$ give a unique recurrent class
reachable from every nonempty test set, so its law converges to $\Pi_U^r$.
Taking time to infinity proves (57), and averaging (57) over uniform
singletons proves (58).

For (59), type complementation gives
$\phi_i(G,1/r)=1-\phi(V\setminus\{i\},r)$.  By (57), the latter deficit is
the probability that the nonempty stationary dual set is contained in
$\{i\}$, which is exactly the singleton probability displayed in (59). ∎

Put

$$
h_r(x)=\frac{rx}{1+(r-1)x},\qquad
C(A)=\sum_{u,v\in A}P_{uv}.
$$

The exact stationary size balances are

$$
\boxed{
(r-1)E_{\Pi_{\rm Bd}^r}B(A)
=E_{\Pi_{\rm Bd}^r}C(A)
=E_{\Pi_{\rm Bd}^r}\{|A|-A(A)\},}
\tag{60}
$$

and

$$
\boxed{
E_{\Pi_{\rm dB}^r}|A|
=E_{\Pi_{\rm dB}^r}
\sum_{v\in A,u\notin A}h_r(P_{vu}).}
\tag{61}
$$

Indeed, a neutral Bd arrow coalesces two occupied dual sites precisely when
both endpoints lie in $A$, while a selective arrow increases the set size
precisely when its target is in $A$ and its source is outside.  For dB, an
update at $v\in A$ removes $v$, and an outside vertex $u$ is added with
probability $h_r(P_{vu})$.  Taking stationary expectations proves
(60)--(61).

Expanding

$$
h_r(x)=rx-
\frac{r(r-1)x^2}{1+(r-1)x}
$$

inside (61) gives a second exact form.  Define

$$
R_2(A)=\sum_{v\in A,u\notin A}
\frac{P_{vu}^2}{1+(r-1)P_{vu}}.
$$

Since the row cut equals $|A|-C(A)$,

$$
\boxed{
E_{\Pi_{\rm dB}^r}
\{C(A)+(r-1)R_2(A)\}
=\left(1-\frac1r\right)E_{\Pi_{\rm dB}^r}|A|.}
\tag{61a}
$$

Thus dB stationary density is exactly a sum of pairwise co-occupancy and a
nonnegative cut-collision remainder.  This identity is useful structurally,
but it does not by itself control the exact-level singleton masses needed
below.

For later use, put

$$
\ell_r(x)=E(x^K)=\frac{x}{r-(r-1)x},
$$

and denote the stationary probabilities of the singleton and doubleton sets
by $b_i,b_{ij}$ for the Bd dual and $q_i,q_{ij}$ for the dB dual.  Exact
stationarity at level one gives

$$
\boxed{
r t_i b_i=\sum_jP_{ij}(b_j+b_{ij}),
\qquad
q_i=\sum_j\ell_r(P_{ji})(q_j+q_{ij}).}
\tag{62}
$$

For example, the only ways for the dB dual to enter $\{i\}$ are from
$\{j\}$ or $\{i,j\}$, followed by an update at $j$ for which all $K$
samples equal $i$.  Summing the Bd equations, or directly balancing the
level-one and level-two size fluxes, gives

$$
\boxed{
(r-1)\sum_i t_i b_i
=\sum_{i<j}(P_{ij}+P_{ji})b_{ij}.}
\tag{63}
$$

Identity (59) turns the triangle diagnostic (51) into a stationary-set
inequality.  Its natural all-graph extension would be

$$
\sum_i\frac{\Pi_{\rm dB}^r(\{i\})}{d_i}
\ge r^2H\left\{\frac{E_{\Pi_{\rm dB}^r}|A|}{n}
-\left(1-\frac1r\right)\right\},
\tag{64}
$$

for $r\ge3/2$.  Equation (64) is **OPEN** beyond the diagnostic triangle
case.  The reduction is useful because it identifies the inverse-fitness
term as weighted stationary singleton mass, rather than as an unrelated
second fixation calculation.

There is an equally compact form of the full arbitrary-satellite product
inequality suggested by the rare-migration calculation.  Put

$$
s_B=\Pi_{\rm Bd}^r(|A|=1),
\qquad
s_D^{(h)}=\sum_i\frac{\Pi_{\rm dB}^r(\{i\})}{H d_i},
\qquad p=1-\frac1r.
$$

Then (58)--(59) turn that proposed inequality exactly into

$$
\boxed{
r^3n\,[\rho_{\rm Bd}(G,r)-p]_+
[\rho_{\rm dB}(G,r)-p]_+
\le s_Bs_D^{(h)}.}
\tag{65}
$$

This product inequality is **OPEN**.  Its dB factor alone is (64), whereas
the tempting separate Bd factor
$rn[\rho_{\rm Bd}-p]\le s_B$ is false (already on the unit-weight
three-vertex path at $r=3/2$).  Thus any proof of (65) must genuinely use the
joint Bd--dB structure rather than multiply two independent bounds.

Finally, grouping the Bd dual arrows which have common target $v$ gives an
exact local comparison mechanism.  Their incoming rate is $t_v$ and their
source law is

$$
Q_{vu}=\frac{P_{uv}}{t_v}.
\tag{66}
$$

At a combined rate $rt_v$, the occupied dual site is selectively retained
and a $Q_v$-neighbor added with probability $1-1/r$, or neutrally replaced
by a $Q_v$-neighbor with probability $1/r$.  If consecutive $v$-events are
grouped through their first neutral event while other targets are censored,
their net map is exactly the geometric burst (56), with kernel $Q$ rather
than $P$.  Interleaving events at other targets prevents this observation
from being a proved stochastic domination.  Establishing a valid censoring
or occupation comparison here would close the present duality gap; assuming
independent lineages would repeat the retracted error.

There is also an exact operator form of this bridge.  Let $L$ be the Bd dual
generator and let $\widehat L$ be obtained by reversing every underlying
graphical arrow before taking the set dual.  Thus an occupied $v$ in
$\widehat L$ samples $u$ from the row $P_{v\cdot}$, neutrally replacing $v$
by $u$ at rate one or selectively retaining $v$ and adding $u$ at rate
$r-1$.  On nonempty sets give the reference measure the unnormalized mass

$$
\mu(A)=(r-1)^{|A|}.
$$

Pairing each neutral coalescence with the reverse selective birth, and each
same-level swap with its reversed swap, gives all off-diagonal entries of the
weighted adjoint.  The exit-rate difference is the cut imbalance.  Hence

$$
\boxed{
L^{\dagger_\mu}
=\widehat L+r\{A(A)-B(A)\}I.}
\tag{67}
$$

This equality is entrywise and exact.  In particular, the only obstruction
to a product-reference adjoint is the already identified temperature
potential $A(A)-B(A)=-\sum_{i\in A}(t_i-1)$.

The geometric batching also has an exact resolvent form.  For a fixed target
$v$, let $S_v$ be the stochastic operator for one selective row-$P$ sample
(retain $v$ and add the sample), let $N_v$ be the operator for one neutral
row-$P$ sample (replace $v$ by the sample), and let $G_v$ be the full
geometric-burst operator.  Operators act on column test functions, so
chronological selective samples followed by the neutral sample give

$$
G_v=\frac1r\sum_{m\ge0}
\left(\frac{r-1}{r}S_v\right)^mN_v.
$$

Consequently,

$$
\boxed{
\left(I-\frac{r-1}{r}S_v\right)(G_v-I)
=\frac1r\{(N_v-I)+(r-1)(S_v-I)\}.}
\tag{68}
$$

The inverse on the left is positivity preserving.  Therefore any
targetwise sign certificate for the unbatched generator is inherited by the
dB burst.  No such certificate proving (64) or (65) is presently known:
the natural cardinality and inverse-degree potentials have local terms of
both signs, and summing over targets before applying the distinct resolvents
is not legitimate.  Equations (67)--(68) isolate that precise remaining
operator gap without introducing independent particles.

### 11.2 [EXACT FINITE DIAGNOSTIC, OPEN IN GENERAL] A normalized-transpose transform

For a symmetric weight matrix $W$ define another symmetric weighted graph by

$$
\mathcal T(W)_{ij}=\frac{W_{ij}}{d_i d_j}.
\tag{69}
$$

Its degree and transition kernel are exactly

$$
d_i^{\mathcal T}=\frac{t_i}{d_i},
\qquad
P^{\mathcal T}_{ij}=\frac{P_{ji}}{t_i}=Q_{ij}.
\tag{70}
$$

Thus $\mathcal T$ is the symmetric diagonal-scaling step whose Markov kernel
is the normalized transpose already arising in (66).  Exact finite tests
suggest the two cross-graph inequalities

$$
\rho_{\rm dB}(W,r)+\rho_{\rm Bd}(\mathcal T(W),r)
\le \rho_{\rm dB}(K_n,r)+\rho_{\rm Bd}(K_n,r),
\tag{71}
$$

$$
\rho_{\rm Bd}(W,r)+\rho_{\rm dB}(\mathcal T(W),r)
\le \rho_{\rm dB}(K_n,r)+\rho_{\rm Bd}(K_n,r).
\tag{72}
$$

Both (71) and (72) are **OPEN**.  They survived exact rational tests at
$r=3/2,2,3$ on every connected labelled support through four vertices under
three weight patterns and on twelve additional five-vertex graphs.  This is
828 exact comparisons, not a reduction theorem.  Even if proved, the two
inequalities would show only that $\mathcal T$ maps a simultaneous amplifier
to a simultaneous suppressor; they would not alone rule out the former.
Their possible asymptotic use is that inherited dB amplification forces
$t_i\to1$ in uniform $L^1$, while
$\mathcal T^2(W)_{ij}=W_{ij}/(t_i t_j)$.  Fixation is not uniformly
continuous under such a perturbation across arbitrarily weak cuts, so this
last observation is currently a route rather than a conclusion.

### 11.3 [PROVED REFORMULATION; OPEN INEQUALITY] Occupied-event rank reflection

Let $G_v(A,B)$ be the full geometric-burst kernel at target $v$, including
null bursts, and define the occupied-event chain

$$
T(A,B)=\frac1{|A|}\sum_{v\in A}G_v(A,B).
\tag{73}
$$

If $\Pi=\Pi_{\rm dB}^r$ and $m=E_\Pi|A|$, then

$$
\nu(A)=\frac{|A|\Pi(A)}m
\tag{74}
$$

is stationary for $T$.  This follows by restoring null target events in the
continuous-time stationary equation.  Thus, after putting $a=r-1$, the open
complementary-level conjecture is exactly

$$
\boxed{
\sum_{|A|=k}\frac{\nu(A)}{a^k}
\le
\sum_{|A|=n-k}\frac{\nu(A)}{a^{n-k}},
\qquad k>n/2.}
\tag{75}
$$

The factors $k$ and $n-k$ in the original formulation are precisely this
occupied-event Palm bias.

There is an exact complete-reference calculation behind (75).  Write
$N=n-1$, fix a target, and condition its burst union to have size $s$.  If
the input event mass is $|A|(n-|A|)a^{|A|}$, its tilted output rank
polynomial from this target is

$$
F_{s,a}(z)=a^{1-s}(1+a)^{s-1}z^s(1+z)^{N-s-1}
\{N+a(N-s)+sz\}.
\tag{76}
$$

At $r=2$, put $\ell(x)=x/(2-x)$ and, for a row $p$, define
$E_j(p)=\sum_{|L|=j}\ell(p_L)$ with $p_L=\sum_{i\in L}p_i$.  Exact
inclusion-exclusion gives the level-$l$ coefficient

$$
O_l(p)=\sum_{j=1}^l(-1)^{l-j}2^{j-1}(2N-j)
{N-j\choose l-j}E_j(p).
\tag{77}
$$

The uniform row makes $O_l=O_{n-l}$.  Convexity of $\ell$ proves
$O_l\le O_{n-l}$ universally for $n\le4$; from $n=5$ onward (77) has
alternating coefficients and ordinary Jensen convexity no longer closes the
sign.  Exact iterates suggest the stronger factorial-transform cone

$$
\sum_A\mu(A){n-|A|\choose j}
\ge\sum_A\mu(A){|A|\choose j},\qquad1\le j<n,
\tag{78}
$$

in addition to rank reflection.  Neither coarse cone, nor their
intersection, is invariant for arbitrary input measures.  Pointwise
complement comparison, Boolean stochastic domination, and universal
ultra-log-concavity are also false.  The full derivation and failed cone
tests are recorded in `RANK_REFLECTION.md`; no stationary reflection theorem
is claimed.

## 12. Verification

The file verify_obstruction_identities.py builds singleton and general-state
transitions directly from both update definitions using exact Fraction
arithmetic. It checks (4)--(8), including the exact mean-$\lambda$ deficit,
on 480 deterministic rational weighted graphs, and checks (40)--(42) and
(46)--(47) on all 39,360 of their nonabsorbing mutant sets. Its expected
output is:

    PASS: 480 exact weighted-graph and 39360 nonabsorbing-state checks

The abstract branching identities are analytic and are explicitly separated
from fixation. No floating-point output is used in any proved claim.

The file verify_triangle_db_threshold.py independently derives the full dB
chain on edge weights $a,b,c$, checks the 261-coefficient diagnostic
certificate (51), and checks sharpness (52). Its expected output is:

    PASS: arbitrary weighted-triangle dB threshold certificate (261 positive shifted coefficients)

The file verify_exact_duals.py independently builds the forward generators,
the additive Bd dual, and the geometric-union dB dual over exact rationals.
It solves both the fixation and stationary equations and checks the full-set
duality (57), not just its averaged consequence, together with (58)--(63)
and the collision form (61a).  It also checks (59) separately for both update
rules and verifies the weighted-adjoint and local-resolvent matrices
(67)--(68) entry by entry.  Finally, as a deliberately non-probative stress test, it evaluates
the open product (65) at $r=3/2$ on every connected labelled support through
four vertices under three exact edge-weight patterns, as well as additional
complete-support examples.  All comparisons use rational arithmetic; this
finite screen is evidence only and is not used as a universal claim.  Its
expected output is:

    PASS: 148 exact forward/dual stationary-chain checks
    PASS: open product inequality survived 145 exact rational small-graph tests at r=3/2 (...)

The discovery-only file test_sinkhorn_cross_conjecture.py checks (70)
entrywise and tests both open inequalities (71)--(72) over exact rationals.
Its expected output begins:

    PASS: both OPEN Sinkhorn cross inequalities survived 828 exact comparisons on 138 rational graphs

The file verify_rank_reflection_diagnostics.py checks (73)--(77), including
609 graph-independent exact conditional-rank identities.  It then checks
the open stationary reflection, the one-step reference reflection, and the
factorial transforms only on four listed rational graphs at $r=2$.  Its
expected output is:

    PASS: 609 exact conditional-rank formula checks
    PASS: OPEN stationary/one-step rank and factorial inequalities on 4 exact rational graphs at r=2

## 13. Status

- **PROVED:** exact singleton opposite-curvature tradeoff (Theorem 2.1).
- **PROVED:** every all-fixed-fitness dB amplifier is locally diffuse in
  normalized weight and has $t_i\to1$ in uniform $L^1$ (Theorem 3.1).
- **RETRACTED:** the universal genealogy bounds and every fixation consequence
  formerly attributed to Theorem 4.1.
- **PROVED FOR THE SEPARATELY DEFINED ABSTRACT PROCESSES:** global quadratic
  and local sharp second-order branching tradeoffs (Theorem 5.1 and Section
  6); no fixation consequence is claimed.
- **PROVED:** the coupling-free actual-chain drift and occupation identities
  (46)--(49).
- **PROVED:** the exact additive duals, stationary density and reverse
  singleton representations (57)--(59), and stationary size balances
  (60)--(63), including the collision expansion (61a).  These retain
  coalescence and do not use independent ancestry.
- **PROVED:** the weighted-adjoint and geometric-resolvent operator bridges
  (67)--(68); their remaining cut-potential and interleaving terms are not
  assumed to have a sign.
- **PROVED:** the occupied-event Palm reformulation (73)--(75) and the exact
  complete-reference rank formulas (76)--(77).
- **OPEN / EXACTLY TESTED FINITELY:** stationary complementary-level
  reflection (75) and its factorial-transform strengthening (78).
- **EXACT DIAGNOSTIC ONLY:** the threshold-sharp inverse-degree dB fixation
  inequality (51) for positive weighted triangles; this does not extend the
  inherited finite classification or bound $R_{\rm sim}$.
- **OPEN:** a global fixation comparison beyond singleton establishment and
  the exact drift or stationary-dual identities.
- **OPEN / EXACTLY TESTED FINITELY:** the two normalized-transpose cross
  inequalities (71)--(72); they are not an obstruction without a weak-cut
  continuity or reduction theorem.
- **OPEN:** singular mesoscopic or multiscale modular cuts.
- **OPEN:** Alternative O, Alternative U, and the exact value of
  $R_{\rm sim}$.

The valid obstruction route narrows any all-fixed-fitness dB-amplifying family
to a locally diffuse, asymptotically isothermal, bottleneck-sensitive regime.
It does **not** prove that fixation gains vanish, and it has not eliminated
  that regime.
