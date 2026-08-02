# Phase 4 obstruction route: universal local tradeoffs and the bottleneck gap

Date: 2026-08-01 (America/Los_Angeles)

No literature search or external contact was used. The inherited fixed-graph,
support-degree, and finite-type results are treated as proved facts and are
not rederived here.

This report does **not** prove Alternative O. It proves several new universal
reductions and isolates the unresolved gap. All proved controls are local,
branching-level, or leading-order. A vanishing-weight modular cut can retain
an order-one relative bias, and strict fixation amplification may live below
the controlled leading order.

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

## 4. [PROVED] Universal total-genealogy bounds

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

### Theorem 4.1

For every connected undirected weighted graph of order $n$,

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

one also has

$$
\boxed{
\rho_{\rm Bd}(G,r)
\le\frac{1-h_r(z)+\eta(G)}{1-z^n}.}
\tag{17}
$$

Consequently, for every graph family and fixed $r>1$,

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

for every fixed $r>1$. Both strict gains must vanish.

#### Genealogical domination

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

Poisson thinning therefore embeds the actual genealogical tree in a
multitype linear branching tree with death rate one and birth matrix
$rP^{\mathsf T}$.

For Bd, give residents reproduction clocks of rate one and mutants clocks of
rate $r$. A type-$i$ mutant produces type-$j$ children at rate $rP_{ij}$.
Its vertex is targeted at total rate

$$
\sum_u f_uP_{ui}\ge\sum_uP_{ui}=t_i,
$$

so its lifetime is dominated by an exponential lifetime of rate $t_i$.
The total genealogy is therefore dominated by the branching process with
birth matrix $rP$ and type-$i$ death rate $t_i$.

In either update rule, fixation requires at least $n$ total genealogical
lineages.

#### PGF proof

For the dB-dominating branching process, let $g_i(z)=E_i z^T$, with
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

For the Bd-dominating process, its PGFs $q_i$ satisfy

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

Finally,

$$
1-z^T\ge(1-z^n)\mathbf1_{\{T\ge n\}},
$$

which proves (16)--(17). Taking $z_n=e^{-n^{-1/2}}$ proves
(18)--(20). ∎

The explicit finite-size choice $z=n^{-1/n}$ gives

$$
\rho_{\rm dB}(G,r)
\le1-\frac1r+O_r\!\left(\frac{\log n}{n}\right).
\tag{24}
$$

Thus no dB family can have a positive limiting additive amplification gap.
The error in (24) remains larger than the complete dB baseline's $O(1/n)$
deficit, so (24) is not Alternative O.

## 5. [PROVED] A nonperturbative branching-survival tradeoff

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

Theorem 5.1 is a genuine quantitative Bd--dB tradeoff, but it concerns the
dominating rare-mutant branching processes. The quadratic bound is too weak
to settle fixation signs at scale $1/n$.

## 6. [PROVED] Sharper local perturbative tradeoff

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

This is the requested heterogeneity tradeoff in a full neighborhood of a
regular kernel. It still does not cover singular weak-cut perturbations.

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

## 8. [NUMERICALLY OBSERVED, NOT USED]

Small multitype branching computations suggest

$$
\frac1n\sum_i
\Pr_i\{\text{hit population }K\text{ before zero}\}
\le\frac{1-r^{-1}}{1-r^{-K}}
\tag{40}
$$

for every column-stochastic birth kernel with death rate one. Random tests
covered up to four types and $K=6$. No proof was found. Even (40), by itself,
would upper-bound dB fixation by the Bd complete baseline rather than the
smaller dB baseline, leaving an $O(1/n)$ window.

Random full-chain searches found no fixed-$r$ universal inequality strong
enough to close that window. These computations are conjecture generation
only.

## 9. Verification

The file verify_obstruction_identities.py builds the singleton transitions
directly from both update definitions using exact Fraction arithmetic. It
checks (4)--(8), including the exact mean-$\lambda$ deficit, on 480
deterministic rational weighted graphs. Its expected output is:

    PASS: 480 exact weighted-graph identity checks

The branching and asymptotic proofs above are analytic; no floating-point
output is used in them.

## 10. Status

- **PROVED:** exact singleton opposite-curvature tradeoff (Theorem 2.1).
- **PROVED:** every all-fixed-fitness dB amplifier is locally diffuse in
  normalized weight and has $t_i\to1$ in uniform $L^1$ (Theorem 3.1).
- **PROVED:** universal genealogy bounds and convergence of both fixation
  probabilities to $1-1/r$ for every hypothetical positive family
  (Theorem 4.1).
- **PROVED:** global quadratic and local sharp second-order tradeoffs between
  Bd and dB branching establishment (Theorem 5.1 and Section 6).
- **OPEN:** control of fixation after establishment at the decisive $1/n$
  scale.
- **OPEN:** singular mesoscopic or multiscale modular cuts.
- **OPEN:** Alternative O, Alternative U, and the exact value of
  $R_{\rm sim}$.

The obstruction route has narrowed every positive family to a vanishing-gain,
locally diffuse, asymptotically isothermal, bottleneck-sensitive regime. It
has not eliminated that regime.

