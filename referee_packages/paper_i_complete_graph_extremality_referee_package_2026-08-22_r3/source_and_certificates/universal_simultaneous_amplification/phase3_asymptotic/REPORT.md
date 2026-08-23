# Phase 3: the fixed-fitness / growing-population quantifier

Date: 2026-08-01 (America/Los_Angeles)

No literature search or external contact was used.  This report labels proved
claims, computational observations, falsified candidate routes, and open
claims separately.

## 0. Quantifier being studied

The finite-graph strong-selection theorem proves

\[
 \forall N\;\exists R_N\;\forall r>R_N:\quad
 \rho_{\rm dB}(G_N,r)<\rho_{\rm dB}(K_{|G_N|},r).
\]

It does **not** by itself rule out the logically weaker asymptotic property

\[
 \forall r>1\;\exists N_0(r)\;\forall N>N_0(r):\quad
 \rho_U(G_N,r)>\rho_U(K_{|G_N|},r)
\]

for both rules, because the thresholds \(R_N\) might diverge.  This report
attacks that remaining quantifier.

No full resolution was obtained.  Two broad candidate regimes are ruled out:

1. families for which a positive fraction of vertices retains bounded total
   support degree (with the subsequence/eventual distinction made below);
2. fixed irreducible-kernel, positive-proportion dense finite-type blow-ups
   with unequal limiting weighted degrees.

The broader collection of cases left open by these filters is described in
Section 6.

## 1. [PROVED] Fitness monotonicity for dB

For a mutant set \(S\), if vertex \(v\) dies, put

\[
 M_S(v)=\sum_{u\in S}w_{uv},\qquad
 R_S(v)=d_v-M_S(v).
\]

The probability that the replacement is mutant is

\[
 p_r(S,v)=\frac{rM_S(v)}{rM_S(v)+R_S(v)}.
\]

This is nondecreasing both in \(r\) and under inclusion of mutant sets.
Couple two processes by using the same dead vertex and the same uniform random
number to choose its new type.  If \(S\subseteq T\) and \(r\le r'\), the
inclusion is preserved after every coupled update.  Hence fixation probability
is nondecreasing in fitness, for every initial state and after uniform
averaging.

Combining monotonicity with the exact strong-selection limit gives the
finite-fitness upper bound

\[
 \boxed{
 \rho_{\rm dB}(G,r)
 \le 1-\frac1n\sum_{i=1}^n\frac1{s_i+1},}
\tag{1}
\]

where \(s_i\) is the degree of vertex \(i\) in the positive-weight support.
This bound is independent of the magnitudes of the positive weights.

## 2. [PROVED] A necessary support-degree condition

The complete-graph baseline is

\[
 \rho_{\rm dB}(K_n,r)=
 \frac{n-1}{n}\frac{1-r^{-1}}{1-r^{-(n-1)}}.
\tag{2}
\]

Define

\[
 a_n=\frac1n\sum_i\frac1{s_i+1}.
\]

If \(G_n\) dB-amplifies at fitness \(r\), (1) implies the necessary
inequality

\[
 a_n<1-\rho_{\rm dB}(K_n,r).
\tag{3}
\]

For fixed \(r>1\), the right side tends to \(1/r\).  Therefore:

**Proposition 2.1.**  Let \(n=|V(G_n)|\to\infty\).  If a graph family
dB-amplifies eventually at every fixed \(r>1\), then

\[
 \boxed{a_n\longrightarrow0.}
\tag{4}
\]

Indeed, for every fixed \(R>1\), eventual amplification at fitness \(R\)
gives

\[
 \limsup_{n\to\infty}a_n
 \le \lim_{n\to\infty}
 \left(1-\rho_{\rm dB}(K_n,R)\right)=\frac1R.
\]

This holds for arbitrarily large fixed \(R\), while \(a_n\ge0\), and hence
\(a_n\to0\).  Notice that the fitness is fixed before the population limit;
no fitness-uniform threshold is being used.
In particular, for each fixed integer \(K\),

\[
 \frac1n\#\{i:s_i\le K\}
 \le (K+1)a_n\longrightarrow0.
\tag{5}
\]

Thus the support degree must diverge in probability under a uniformly chosen
initial vertex.  Adding tiny positive edges can satisfy this support
condition, so it is necessary rather than sufficient.

### Consequences

**[PROVED FALSIFICATION: bounded-degree families.]**  Any uniformly
bounded-support-degree family fails the all-fixed-fitness dB requirement.  If
for some fixed \(K\),
\(\limsup_n n^{-1}\#\{i:s_i\le K\}>0\), choose a subsequence on which this
fraction is at least \(c>0\) and then a fixed \(r>(K+1)/c\); amplification
fails along that subsequence.  If the corresponding `liminf` is positive,
the same choice gives eventual suppression for all sufficiently large
\(n\), not merely failure on a subsequence.

**[PROVED FALSIFICATION: paths and bounded-support satellite gadgets.]**
Weighted paths have support degree at most two and therefore fail, regardless
of how their positive edge weights scale; in fact (1) proves eventual dB
suppression at every fixed \(r>3\).  Repeating a fixed gadget is covered only
when a positive fraction of its vertices retains bounded **total support
degree after the gadgets are connected**.  If typical gadget vertices receive
a diverging number of arbitrarily weak support-completion edges, Proposition
2.1 does not exclude the construction.

**[PROVED FALSIFICATION: windmills.]**  In a windmill of \(m\) triangles
sharing a hub, the hub support degree is \(2m\), while all \(2m\) leaves have
support degree two.  Its dB strong limit tends to \(2/3\).  For any fixed
\(r>3\), (2) tends to \(1-1/r>2/3\), so every choice of positive pair/spoke
weights is eventually dB-suppressing.

This rules the windmill out as a family that amplifies eventually at every
fixed fitness; more explicitly, it proves eventual dB suppression for every
fixed \(r>3\).  It does not assert suppression at each smaller fixed fitness.
The family is nevertheless an effective Bd amplifier in the numerical scan.

## 3. [PROVED] Dense finite-type dB establishment obstruction

This section treats a broad exactly equitable regime.  Fix a finite number
\(m\) of classes.  Suppose class sizes satisfy

\[
 \frac{n_a}{n}\longrightarrow q_a>0,\qquad \sum_aq_a=1,
\]

and every edge between classes \(a,b\) has symmetric weight
\(\omega_{ab}/n\), where the fixed nonnegative matrix \(\omega\) is
irreducible.  Thus the number of classes is fixed, every class has positive
limiting proportion, and the class-weight matrix is fixed after a common
normalization.  The factor \(1/n\) is only a normalization.  Put

\[
 \delta_a=\sum_bq_b\omega_{ab},
 \qquad
 A_{ab}=\frac{q_b\omega_{ab}}{\delta_b}.
\tag{6}
\]

### 3.1 Exact stopped generator and rare-mutant process

Poissonize the chain so that every vertex dies at rate one; this does not
change hitting probabilities.  Let \(x_a\) be the number of type-\(a\)
mutants, and define

\[
 d_b^{(n)}=\sum_c\frac{n_c-\mathbf 1_{c=b}}n\omega_{cb},
 \qquad
 m_b(x)=\sum_c\frac{x_c}{n}\omega_{cb}.
\tag{7}
\]

For a resident type-\(b\) target, the exact total rate of a type-\(b\) mutant
birth is

\[
 \lambda_{b,n}^+(x)
 =(n_b-x_b)\frac{r m_b(x)}
 {d_b^{(n)}+(r-1)m_b(x)}.
\tag{8}
\]

For a mutant type-\(b\) target, put
\(\widetilde m_b(x)=m_b(x)-\omega_{bb}/n\), subtracting the dead mutant
itself when it belongs to the same class.  The exact loss rate is

\[
 \lambda_{b,n}^-(x)
 =x_b\frac{d_b^{(n)}-\widetilde m_b(x)}
 {d_b^{(n)}+(r-1)\widetilde m_b(x)}.
\tag{9}
\]

Let

\[
 \eta_n=\max_a\left|\frac{n_a}{n}-q_a\right|.
\]

Irreducibility and \(q_a>0\) give
\(\delta_*:=\min_a\delta_a>0\).  Hence, uniformly on \(|x|\le K\),

\[
 \lambda_{b,n}^+(x)
 =r\sum_a x_aA_{ab}+O_K(\eta_n+n^{-1}),
 \qquad
 \lambda_{b,n}^-(x)=x_b+O_K(\eta_n+n^{-1}).
\tag{10}
\]

The constants may depend on the fixed \(r,K,q,\omega\).  The collision and
mutant-competition part is \(O_r(K^2/n)\), but the class-proportion error can
be larger unless the stronger rounding condition \(n_a=nq_a+O(1)\) is
imposed.  In particular, the total stopped-generator error is
\(O_K(\eta_n+n^{-1})=o_K(1)\), not generally \(O(K^2/n)\).

Equivalently, while the mutant count is fixed as \(n\to\infty\):

* a type-\(a\) mutant dies at rate \(1+o(1)\);
* it produces a type-\(b\) mutant at rate
  \(rA_{ab}+o(1)\).

The second statement follows directly: there are \(nq_b+o(n)\) possible
type-\(b\) deaths, the focal mutant contributes fitness-weighted mass
\(r\omega_{ab}/n\), and the competing resident mass tends to \(\delta_b\).

Thus the early process converges, after stopping at any fixed mutant
population size, to
a continuous-time multitype branching process with death rate one and birth
matrix \(rA\).

Let \(s_a\) be its survival probability from one type-\(a\) individual.  A
first-event equation gives, for the extinction probabilities
\(z_a=1-s_a\),

\[
 z_a=\frac{1+r\sum_bA_{ab}z_az_b}
 {1+r\sum_bA_{ab}},
\]

because a birth leaves the parent alive and adds one independent child.
Rearranging gives

\[
 s_a=r(1-s_a)(As)_a,
 \qquad
 1-s_a=\frac1{1+r(As)_a}.
\tag{11}
\]

The relevant initial average is \(\bar s=\sum_aq_as_a\).

### 3.2 Jensen obstruction

Symmetry of \(\omega\) gives the exact stationarity identity

\[
 \sum_aq_aA_{ab}=q_b.
\tag{12}
\]

The matrix \(A\) is irreducible.  Equation (12) supplies a strictly positive
left eigenvector \(q\) at eigenvalue one, so Perron--Frobenius gives
\(\rho(A)=1\).  The next-generation matrix of the branching process is
\(rA\), whose Perron root is \(r>1\).  It is therefore supercritical; by
irreducibility its survival vector has \(s_a>0\) in every coordinate.  This
also justifies the division by the positive average \(\bar s\) below.

Since \(x\mapsto(1+rx)^{-1}\) is strictly convex, (11)--(12) imply

\[
 1-\bar s
 =\sum_aq_a\frac1{1+r(As)_a}
 \ge \frac1{1+r\bar s}.
\]

For \(r>1\) and \(\bar s>0\), this is equivalent to

\[
 \boxed{\bar s\le1-\frac1r.}
\tag{13}
\]

This is a first-principles branching-process tradeoff; no fixation formula is
being assumed.

### 3.3 Stopped-generator hitting lemma and fixation upper bound

Fix an integer \(K\).  Stop both the finite count chain and the limiting
branching chain on \(|x|=0\) or \(|x|=K\).  For all sufficiently large \(n\),
their common interior state space

\[
 \mathcal X_K=\{x\in\mathbb Z_+^m:1\le |x|\le K-1\}
\]

is finite.  Equation (10) gives entrywise convergence of their killed
generators.  The limiting killed chain reaches one of the two boundaries
almost surely: on the finite band, death rates are positive and all rates are
bounded, so every fixed block of events has a uniformly positive probability
of containing enough consecutive deaths to hit zero.  Thus its interior
generator is invertible.  The finite Dirichlet systems for hitting \(K\)
before zero depend continuously on the generator entries, and their
solutions converge.  Since \(n_a/n\to q_a\), convergence also holds after
uniform-singleton initial averaging.

Fixation must pass through total count \(K\).  Therefore, for every fixed
\(K\),

\[
 \limsup_{n\to\infty}\rho_{\rm dB}(G_n,r)
 \le p_K,
\]

where \(p_K\) is the averaged branching probability of hitting \(K\).

The branching process is nonexplosive because its total rate is bounded by a
constant times its population size and hence is dominated by a linear pure
birth process.  An extinct path has finite maximum population.  A path that
survives while remaining forever below some \(K\) has probability zero by
the same finite-band absorption argument.  Consequently, reaching every
\(K\) is the survival event modulo a null set, so \(p_K\downarrow\bar s\).
Therefore

\[
 \boxed{
 \limsup_{n\to\infty}\rho_{\rm dB}(G_n,r)
 \le\bar s\le1-\frac1r.}
\tag{14}
\]

### 3.4 Strictness and the natural two-class family

Equality in Jensen requires \((As)_a\) to be constant.  Equation (11) then
makes \(s_a\) constant.  Since \(s_a>0\), equality first requires the row
sums to have one common value:

\[
 t_a:=\sum_bA_{ab}=t\quad\hbox{for every }a.
\tag{15}
\]

The common row-sum value is one, because

\[
 \sum_aq_at_a=\sum_{a,b}q_aA_{ab}=\sum_bq_b=1.
\tag{16}
\]

Thus \(t=1\).

Let

\[
 P_{ab}=\frac{q_b\omega_{ab}}{\delta_a}.
\]

This is irreducible and row-stochastic.  Condition (15) says that
\(1/\delta_a\) is \(P\)-harmonic.  The finite maximum principle forces it to
be constant.  Thus equality in (13) occurs exactly when all limiting weighted
degrees \(\delta_a\) are equal.

Conversely, if all \(\delta_a\) are equal, then every row sum of \(A\) is
one.  The total population in the branching process is then an ordinary
linear birth--death process with per-individual birth rate \(r\) and death
rate one, so its survival probability from every type is exactly
\(1-1/r\).  This proves the converse equality statement without assuming
uniqueness of an arbitrary algebraic solution of (11).

**Theorem 3.1.**  Every fixed-class, positive-proportion dense finite-type
family with a fixed irreducible limiting class kernel and unequal limiting
weighted degrees is eventually dB-suppressing at every fixed \(r>1\).  More
precisely, if

\[
 \gamma_r=1-\frac1r-\bar s>0,
\]

then (2) and (14) give

\[
 \liminf_{n\to\infty}
 \left(\rho_{\rm dB}(K_n,r)-\rho_{\rm dB}(G_n,r)\right)
 \ge\gamma_r>0.
\tag{17}
\]

Thus the comparison has a positive asymptotic gap in the precise sense of a
positive `liminf`; convergence of the graph fixation probabilities, and
hence existence of a limiting gap, has not been proved.

This includes the preferred two-equitable-class family when both class
proportions tend to positive constants and its nonzero orbit-weight ratios
tend, after common normalization, to a fixed irreducible kernel, unless its
two limiting weighted degrees agree.  It does not cover a vanishing class
proportion or a limiting reducible kernel, such as a cross-class weight ratio
tending to zero.

If the finite graphs are exactly weighted-regular, Bd ties the complete graph
for every fitness: across every mutant/resident cut, the embedded mutant-count
down/up ratio is exactly \(1/r\).  Hence the exactly regular equality case
cannot be a strict simultaneous amplifier either.

The delicate case left open here is asymptotic regularity without exact
finite-\(n\) regularity; its leading branching limit ties (13), and signs live
in lower-order corrections.

## 4. [COMPUTATIONAL OBSERVATIONS, NOT PROOFS]

The scripts in this directory use no external packages.

* `verify_lumping.py` enumerates the full subset chain for small instances
  with exact `Fraction` arithmetic.  It verifies strong lumpability for both
  rules into:
  * counts of mutants in two equitable classes;
  * hub type and counts of 0/1/2-mutant windmill pairs.
* `scan_lumpable.py` builds the quotient transitions directly and solves the
  holding-step-free absorbing equations by Gauss--Seidel iteration.

The documented scan (`python3 -u scan_lumpable.py --default-scan`) found:

```text
two_class n=40 r=1.1  Bd_delta=+0.002791296  dB_delta=-0.006024159
two_class n=40 r=2    Bd_delta=+0.006444028  dB_delta=-0.028145532
two_class n=40 r=10   Bd_delta=+0.000572067  dB_delta=-0.019270339

windmill n=41 r=1.1   Bd_delta=+0.033240174  dB_delta=-0.059414028
windmill n=41 r=2     Bd_delta=+0.073146286  dB_delta=-0.383198950
windmill n=41 r=10    Bd_delta=+0.009157227  dB_delta=-0.426701058
```

The two-class parameters in this table are equal class sizes and weights
`within A = 0.1`, `within B = cross = 1`.  The windmill pair and spoke weights
are all one.  These values support, but are not needed for, the proved class
obstructions.

The two-type branching fixed point with class fraction \(1/2\), limiting
degree ratio \(2\), and \(P_{12}=0.4\) gives:

```text
r=1.1  Bd excess +0.002043559   dB excess -0.008672528
r=2    Bd excess +0.003840600   dB excess -0.033414861
r=10   Bd excess +0.000289318   dB excess -0.015901953
```

This explicitly demonstrates the dense asymptotic tradeoff: degree
heterogeneity can improve Bd establishment while strict Jensen convexity
reduces dB establishment.

An additional scan of the complete-support family with two exceptional
vertices joined by a tiny edge (all other weights one) found a small positive
Bd excess and a negative dB excess for `n=10,20,40,80` and
`r=1.1,2,10`.  The dB deficit decays with `n`, illustrating the unresolved
lower-order, asymptotically regular regime.

## 5. Falsified or unsafe conjectures

### [UNSAFE INFERENCE] The finite strong-selection theorem is automatically uniform

This does not follow from the available expansion.  For complete support,
the negative \(1/r\) coefficient contains
terms \((d_i+d_j)/w_{ij}\).  An edge of weight \(\varepsilon_n\) can make the
coefficient grow like an inverse power of \(\varepsilon_n\), while the
remainder estimate is graph-dependent.  Thus rapidly vanishing weights can
push the regime controlled by the asymptotic expansion beyond every fixed
sampled fitness.  This does not prove that the actual crossover threshold
diverges, and it does not construct an amplifier; it shows only that swapping
the \(N\to\infty\) and \(r\to\infty\) limits requires a new uniform estimate.

### [FALSIFIED WITH A SUPPORT CAVEAT] A bounded-support satellite gadget can be repeated around a hub

The support-degree condition (5) rules the construction out as a family that
amplifies eventually at **every** fixed fitness only when a positive fraction
of vertices retains bounded total support degree after connection.  For
windmills it proves eventual suppression at every fixed \(r>3\), not at every
\(r>1\).  A repeated fixed internal gadget whose typical vertices acquire a
diverging number of tiny positive support-completion edges is outside this
argument.

### [FALSIFIED ELSEWHERE, RELEVANT HERE] dB is always weakly suppressing

The exact weighted path with edge weights `5,1,1,5` has
\(c_{\rm dB}=3/10+1/9310\).  Thus the present asymptotic obstructions cannot
be replaced by a finite-graph weak-selection maximization claim.

### [UNSUPPORTED] A cross-rule weak coefficient inequality

The exact criteria \(N_{\rm Bd}>n\), \(N_{\rm dB}>n\) remain useful, but no
universal inequality linking the two effective sizes was proved.  It should
not be used as an asymptotic obstruction.

## 6. Remaining cases and heuristic search directions

The proved filters impose only the following necessary requirements on a
positive family:

1. support degree tending to infinity for a uniformly chosen vertex;
2. it cannot be a fixed-class, positive-proportion dense blow-up with a fixed
   irreducible kernel and unequal limiting weighted degrees;
3. no exact weighted regularity, since that makes Bd tie;
4. in a leading-order dB tie regime, lower-order positive excess over the
   complete baseline is required, not merely a limiting tie at \(1-1/r\).

**[HEURISTIC DESIGN GUESS, NOT A PROVED NECESSITY.]**  Mesoscopic modules
whose size tends to infinity, with dominant internal edges and a growing
number of very weak support-completion edges, remain a plausible search
direction.  A next exact target would be a wreath-symmetric family of growing
cliques or growing paired modules, because module occupancy counts remain
lumpable.

The open class is broader than this non-diffuse guess.  It also contains
diffuse, asymptotically isothermal but not exactly regular perturbations whose
comparison is decided below the leading branching order.  It contains
finite-type boundary regimes excluded by the hypotheses of Theorem 3.1,
including vanishing class proportions and limiting reducible kernels.  The
proved results do not force a successful family to have any individually
macroscopic edge.

## 7. Status

**[OPEN]**  No explicit fitness-independent family simultaneously amplifying
both rules at every fixed finite \(r>1\) was found.

**[OPEN]**  No universal fixed-\(r\) obstruction covering diffuse
asymptotically isothermal perturbations, mesoscopic non-diffuse structures,
vanishing class proportions, or limiting reducible kernels was proved.

**[PROVED PROGRESS]**  Bounded-support-degree candidates (including repeated
gadgets only under the stated total-support caveat) and fixed-class,
positive-proportion, fixed irreducible-kernel dense candidates with unequal
limiting degrees are impossible.  These are partial obstructions, not an
exhaustive isolation of one remaining corridor.
