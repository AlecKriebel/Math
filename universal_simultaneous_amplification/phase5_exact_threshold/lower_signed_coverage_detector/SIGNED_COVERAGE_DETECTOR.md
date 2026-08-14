# Signed coverage detectors: an exact baseline obstruction and an abstract surrogate

Date: 2026-08-13 (America/Los_Angeles)

No graph search, literature search, or external communication was used.

## 1. Status

Let `J` have the geometric-zero law

\[
 \Pr(J=j)={1\over r}\left({r-1\over r}\right)^j,
 \qquad j\geq0,
\tag{1}
\]

and let an anchored locked batch output

\[
                    B=\{U_0,U_1,\ldots,U_J\},
\tag{2}
\]

where the `U_j` are iid with row law `p`.  Write `a=r-1` and

\[
                  g(B)=|B|-\mathbf 1_{\{B\ne\varnothing\}}.
\tag{3}
\]

There are three exact conclusions.

1. The detector has the desired diffuse expectation:

   \[
   \boxed{
   E g(B)=a\sum_u{p_u(1-p_u)\over1+a p_u}
   =a-ar\sum_u{p_u^2\over1+a p_u}.}
   \tag{4}
   \]

   For uniform fan-out on `m` labels this is

   \[
                       \boxed{\Gamma_{r,m}
                       ={a(m-1)\over m+a}.}
   \tag{5}
   \]

   Thus `Gamma_(r,m) -> r-1`, with a depth-`L` relative collision
   error at most `Lr/(m+a)` in the formal independent-stage product.

2. Exact `g`, and every nonzero affine normalization preserving its zero
   on singletons, is **not** a common-coefficient signed difference of
   normalized coverage harmonics.  Its unique signed coverage measure has
   positive mass `m` and negative mass `1`.  Allowing an unmatched positive
   baseline forces coefficient `m-1`; this cost is sharp and is larger than
   the uniform-batch signal by the exact factor

   \[
                         \boxed{{m+a\over a}.}
   \tag{6}
   \]

   Hence the literal diffuse `g` router fails the response-scale
   uniform-start/baseline test.

3. The coverage cone does admit a different, baseline-free, bounded-cost
   signed detector.  Its exact one-stage multiplier is derived in Section
   5.  This is only an **abstract randomized coverage test**, not yet a
   physical undirected fixation/hitting module.  In fact, its two canonical
   representing laws cannot be invariant ancestral laws of any finite
   connected dB fixation chain.  An augmented stopped-module realization
   would need a new killed-dual construction and a common-control response
   identity under both update rules.

Consequently the exact `g` proposal is closed, but signed terminal
observables as a class are not closed.

## 2. Exact geometric-union expectation

For a fixed label `u`,

\[
 E(1-p_u)^{J+1}
 ={1-p_u\over1+a p_u}.
\tag{7}
\]

Therefore

\[
 \Pr(u\in B)={r p_u\over1+a p_u},
\tag{8}
\]

and summing (8), then subtracting one, proves the first expression in
(4).  The second follows from

\[
 {r p\over1+a p}-p={a p(1-p)\over1+a p}
\tag{9}
\]

and

\[
 1-\sum_u{p_u(1-p_u)\over1+a p_u}
 =r\sum_u{p_u^2\over1+a p_u}.
\tag{10}
\]

In particular, with `eta=sum_u p_u^2` and `p_*=max_u p_u`,

\[
 {ar\eta\over1+a p_*}
 \le a-Eg(B)\le ar\eta.
\tag{11}
\]

For `p_u=1/m`, (4) reduces to (5), and

\[
 {\Gamma_{r,m}\over a}=1-{r\over m+a}.
\tag{12}
\]

If independent locked stages reinitialize the same signed scalar channel,
the formal projective multiplier is `Gamma_(r,m)^L`.  Hence

\[
 0\le1-\left({\Gamma_{r,m}\over a}\right)^L
 \le {Lr\over m+a}.
\tag{13}
\]

This is a scalar history calculation only.  It does not assert that a
finite graph composes the signed observable.

For completeness, if the anchor `U_0` is omitted and `B` is the union of
the `J` selective samples alone, then

\[
 \boxed{
 E g(B)=a^2\left\{{1\over r}
       -\sum_u{p_u^2\over1+a p_u}\right\}.}
\tag{14}
\]

For uniform fan-out this is

\[
                  {a^2(m-1)\over r(m+a)}.
\tag{15}
\]

Thus the anchored and unanchored conventions differ by a full adverse
factor; (4), not (14), is the convention matching the locked batch in (2).

## 3. Unique signed coverage measure

For every nonempty `Z subseteq V`, put

\[
                 c_Z(B)=\mathbf1_{\{Z\cap B\ne\varnothing\}}.
\tag{16}
\]

The functions `c_Z` form a basis of the functions on nonempty subsets.
Indeed, if `sum_Z sigma_Z c_Z(B)=0` for every nonempty `B`, evaluation at
`B=V` first gives `sum_Z sigma_Z=0`.  Evaluation at `B=V\setminus C` for
every proper `C subset V` then gives `sum_(Z subseteq C) sigma_Z=0`;
Boolean-lattice inversion, followed once more by the total-mass identity,
forces every `sigma_Z=0`.

The identity

\[
                 \boxed{g=\sum_{u\in V}c_{\{u\}}-c_V}
\tag{17}
\]

is therefore the unique signed coverage representation of `g`.  Its
Jordan masses are

\[
                  \|\sigma_g^+\|=m,
                  \qquad \|\sigma_g^-\|=1.
\tag{18}
\]

A normalized coverage harmonic has the form

\[
 h_\mu(B)=\sum_Z\mu_Zc_Z(B),
 \qquad \mu_Z\ge0,\quad\sum_Z\mu_Z=1,
\tag{19}
\]

and consequently satisfies `h_mu(V)=1`.  Every common-coefficient signed
module sum

\[
 D(B)=\sum_jd_j\{h_{\mu_j}(B)-h_{\nu_j}(B)\},
 \qquad d_j\ge0,
\tag{20}
\]

has `D(V)=0`.  Since `g(V)=m-1`, no nonzero multiple of `g` can equal (20).
More generally, an affine function `alpha g+beta` on the full Boolean cube
can equal (20) only trivially: evaluation at the empty set gives `beta=0`,
and evaluation at `V` then gives `alpha=0`.

Suppose one permits one unmatched normalized coverage baseline:

\[
                       \alpha g=\beta h_0+D,
                       \qquad \alpha>0.
\tag{21}
\]

Evaluation at `V` forces, without an inequality or approximation,

\[
                         \boxed{\beta=\alpha(m-1).}
\tag{22}
\]

This lower bound is sharp.  With

\[
 h_{\rm one}(B)={|B|\over m},
 \qquad h_{\rm all}(B)=\mathbf1_{\{B\ne\varnothing\}},
\tag{23}
\]

one has

\[
 \boxed{
 \alpha g=\alpha(m-1)h_{\rm one}
           +\alpha(h_{\rm one}-h_{\rm all}).}
\tag{24}
\]

The residual common signed coefficient in (24) is also minimal: the unique
measure (17) has negative mass `alpha` at `V`, so any positive-minus-positive
decomposition of the zero-total residual needs common mass at least
`alpha`.

Under uniform fan-out, the ratio of the forced baseline coefficient (22)
to the actual signed signal is

\[
 {\alpha(m-1)\over\alpha\Gamma_{r,m}}
 ={m+a\over a},
\tag{25}
\]

which diverges linearly.  Scaling `g` by `1/(m-1)` merely changes both
numerator and denominator: the normalized detector has expectation
`a/(m+a)`, while its unmatched baseline coefficient remains one.  Thus
normalization cannot repair the response-scale initialization cost.

## 4. A common-difference surrogate

The endpoint obstruction in Section 3 applies to exact `g`; it does not
exclude a detector that returns to zero on macroscopic sets which the
geometric batch almost never visits.

Fix `1<s<m`.  Let `mu_s` be the uniform law on all `s`-subsets of `V`, let
`mu_1` be the uniform singleton law, and put

\[
 \lambda={s-1\over m-1},
 \qquad \nu_s=\lambda\delta_V+(1-\lambda)\mu_1.
\tag{26}
\]

Both laws have the same one-label marginal `s/m`.  Define

\[
 \boxed{
 f_{m,s}(B)={m\over s}
       \{h_{\mu_s}(B)-h_{\nu_s}(B)\}.}
\tag{27}
\]

This is a common-coefficient difference with coefficient `m/s`, and

\[
                         f_{m,s}(\{u\})=0.
\tag{28}
\]

It is also nonnegative.  If `|B|=k`, then

\[
 h_{\mu_s}(B)=1-{(m-s)_k\over(m)_k},
 \qquad
 h_{\nu_s}(B)=\lambda+(1-\lambda){k\over m}.
\tag{29}
\]

Here `(x)_k` denotes the falling factorial.  If `k>m-s`, the first ratio in
(29) is zero and the desired inequality is immediate.  Otherwise, after
cancelling the first factor, the inequality is

\[
 \prod_{j=1}^{k-1}{m-s-j\over m-j}
 \le\prod_{j=1}^{k-1}{m-j-1\over m-j}
 ={m-k\over m-1},
\tag{30}
\]

which holds factor by factor.  It is strict for `1<s<m` and
`2<=k<=m-1`.  Thus

\[
 f_{m,s}(B)
 \begin{cases}
 =0,&|B|=0,1,m,\\
 >0,&2\le|B|\le m-1.
 \end{cases}
\tag{31}

In particular, `f_(m,s)` is not itself a coverage harmonic: a nonnegative
monotone harmonic which vanishes at `V` must vanish everywhere.

For fixed `k`, if `s/m -> q in (0,1)`, then

\[
 f_{m,s}(B)\longrightarrow
 {1-(1-q)^k-q\over q}.
\tag{32}

Sending `q downarrow0` recovers `k-1`, but the common coefficient `m/s`
then diverges like `1/q`.  This is the bounded-set version of the exact
baseline/cost obstruction.

## 5. Exact surrogate multiplier

For a deterministic ancestral set of relative size `x=|Z|/m`, the anchored
uniform batch obeys

\[
 E c_Z(B)=1-E(1-x)^{J+1}
 ={rx\over1+a x}=: \phi_r(x).
\tag{33}
\]

Using (26)--(27) and simplifying gives

\[
 \begin{aligned}
 \Theta_{r,m,s}
 &:=E f_{m,s}(B)\\
 &={m\over s}\left\{
   \phi_r(s/m)-\lambda\phi_r(1)
   -(1-\lambda)\phi_r(1/m)\right\}\\
 &=\boxed{
 {a m(s-1)(m-s)\over s(m+a)(m+a s)}.}
 \end{aligned}
\tag{34}
\]

Two regimes are exact consequences.

If `s/m -> q in (0,1)`, then the common coefficient stays bounded and

\[
 \boxed{
 \Theta_{r,m,s}\longrightarrow
 {a(1-q)\over1+a q}<a.}
\tag{35}
\]

If `s -> infinity` and `s/m -> 0`, then

\[
                         \Theta_{r,m,s}\longrightarrow a,
 \qquad {m\over s}\longrightarrow\infty.
\tag{36}
\]

Thus exact recovery of the labelled multiplier again requires divergent
coefficient cost, but a fixed-density signed surrogate has bounded cost and
an even smaller adverse multiplier.  Conditional on independent ordered
handoff and an actual common-control module realization, `L` stages would
give projective factor `Theta_(r,m,s)^L`.

Equation (35) is deliberately not advertised as a graph construction.  At
`r=2` it would give `(1-q)/(1+q)<1`; if it composed physically with no other
term, it would suppress the adverse channel even at the proposed endpoint.
That makes the missing physical sign and normalization audit essential.

## 6. Why the surrogate is not yet physical

The coverage theorem is one-way.  A physical dB fixation harmonic has a
unique representing law which is invariant for the exact geometric-OR
ancestral dual.  An arbitrary probability law on nonempty sets defines an
abstract randomized coverage test, but need not be such an invariant law.

For `m>=3`, neither canonical law in (26) is the invariant ancestral law of
any finite connected loopless dB graph on `V`, at any `r>1`.

For `mu_s`, first suppose `s>=2`.  Some `s`-set `A` in its support contains
an edge `{u,v}`.  When the dual target is `v`, the event `K=1` and parent
`u` has positive probability, and sends

\[
                       A\longmapsto A\setminus\{v\},
\tag{37}
\]

of rank `s-1`.  A law supported only at rank `s` cannot be invariant.  If
`s=1`, connectedness supplies a vertex of degree at least two.  From its
singleton, the positive-probability event `K=2` with two distinct parents
produces rank two.  Finally, `delta_V` is not invariant because `K=1`
always sends `V` to an `(m-1)`-set.  Since `nu_s` has positive mass at `V`
when `s>1`, and equals `mu_1` when `s=1`, it is not invariant either.

This proves an exact obstruction for full fixation harmonics on the same
source set.  A natural attempt to evade stationarity is worth separating
carefully from physical forward dynamics.

### 6.1 Exact selector stopping law

On the complete loopless reservoir `K_m`, the geometric-OR dual is
irreducible on the proper nonempty subsets.  From a set of rank at least
two, repeated `K=1` samples from another current ancestor reach a singleton.
From a singleton `{v}`, first move to a label outside a prescribed proper
set `C`, if necessary, and then sample with distinct support exactly `C`.
Every step has positive probability.

Consequently, if the dual starts from a uniform singleton and

\[
                 \tau_s=\inf\{t:|A_t|=s\},
                 \qquad1\le s\le m-1,
\tag{38}
\]

then `tau_s` is finite almost surely.  Permutation equivariance proves

\[
                         A_{\tau_s}\sim\mu_s.
\tag{39}
\]

This is an exact stopped-dual realization of the first law in (26).

There is a sharp loopless obstruction at full rank.  Whenever an ancestor
`v` is updated, it is removed and every sampled parent differs from `v`.
Thus a proper ancestral set can never jump to `V`; full rank is unreachable
after the dual has entered the proper-set class.

One external selector vertex `x` evades that narrow obstruction.  On
`K_(m+1)` with source interface `V` and selector `x`, the set `V` is a
proper ancestral state.  Irreducibility and symmetry imply that, starting
from `{x}`, first hitting a source-only `s`-set is uniform, and first hitting
the source set `V` occurs almost surely.  Hence both `mu_s` and `delta_V`
are exact **ancestral exit laws** with one formal selector root.

### 6.2 Why dual stopping is not a forward harmonic

The last statement does not produce an ordinary terminal committor.  Let

\[
                         H(B,A)=\mathbf1_{\{B\cap A\ne\varnothing\}}
\tag{40}
\]

be the duality kernel, and let `L_X,L_A` be the forward and ancestral
generators.  Generator duality says

\[
                       L_XH(\,·\,,A)=L_AH(B,\,·\,).
\tag{41}
\]

For a coverage law `mu`, therefore,

\[
 L_Xh_\mu(B)=\int L_AH(B,A)\,d\mu(A).
\tag{42}
\]

An invariant ancestral law makes (42) vanish and yields the fixation
harmonic.  A rank-hitting exit law does not.  More sharply, on the same
source set, if the right side of (42) vanished for every `B`, uniqueness of
the coverage transform from Section 3 would imply `mu L_A=0`; the rank-leak
argument above proves this is false for `mu_s` and `nu_s`.

The stopping surface in (38) is a nonlocal surface in **ancestral
configuration space**.  It is not a spatial terminal of the ordinary
one-bit forward Moran graph.  The ancestral process can replace one
particle by many particles in one mark and is not a second copy of the
forward mutant process.  A physical implementation would need an
additional state which stores the ancestral particles and detects their
source rank.  The one selector vertex in the stopped-law proof supplies
neither operation.

Thus the selector construction proves that there is no probability-law
obstruction to (27), but it remains an external randomized coverage test.
It gives no bounded-vertex forward controller and no uniform-start audit
for such a controller.

### 6.3 Complete-harmonic chord audit

Another useful common-difference bump starts from

\[
 H_m(k)={1-r^{-k}\over1-r^{-m}}.
\tag{43}
\]

This is the genuine complete-graph **Bd** fixation harmonic.  Its chord
through ranks one and `m`,

\[
 L_m(k)=H_m(1)+{k-1\over m-1}\{1-H_m(1)\},
\tag{44}
\]

is exactly the coverage harmonic of

\[
 {mH_m(1)-1\over m-1}\,\delta_V
 +{m\{1-H_m(1)\}\over m-1}\,\mu_1.
\tag{45}
\]

Concavity makes `H_m-L_m` zero at ranks one and `m` and positive between
them.  On the anchored geometric batch, its limiting mean is indeed

\[
 \begin{aligned}
 \lim_{m\to\infty}E\{H_m(|B|)-L_m(|B|)\}
 &= {1\over r}-E r^{-(J+1)}\\
 &=\boxed{{a^2\over r(1+ra)}}.
 \end{aligned}
\tag{46}
\]

However, (43) is not the finite complete-graph dB harmonic.  For dB, the
successive harmonic-increment ratio is

\[
 {T_k^-\over T_k^+}
 ={m-1+ak\over r\{m-1+a(k-1)\}}
 ={1\over r}+{a\over r\{m-1+a(k-1)\}},
\tag{47}
\]

not `1/r`.  The two agree only in the fixed-rank large-`m` limit.  A global
dB process cannot run a dB locked batch followed by a Bd terminal update
rule.

One may replace (43) by the genuine finite dB complete harmonic; its
increments are decreasing for `m>=3`, so subtracting its chord again gives
an abstract positive bump and has the same fixed-rank limit (46).  But the
chord's law still contains positive `delta_V` mass and is not an invariant
dB ancestral law.  The construction is therefore a genuine-plus-external-
control decomposition, not a physical common-control module.

### 6.4 Remaining physical obligations

To turn either signed bump into a physical terminal module one must still
provide:

1. a finite undirected killed-dual/Dirichlet realization of both laws (or
   suitable approximations) using the same source interface;
2. a common physical coefficient which makes the second harmonic removed
   baseline/control mass, not a negative population of terminal starts;
3. the same replacement identity under Bd and dB updating;
4. auxiliary-selector, reverse-interface, and uniform-start contributions
   which are little-oh of the signed response.

Without item 2, a graph containing the two terminal populations adds their
nonnegative fixation probabilities; it does not subtract them.  The
difference in (27) exists only between a proposed module and a control or
reference module.  Coverage algebra alone supplies no such common-control
identity.

Accordingly there is no unconditional physical response-composition lemma
here.  What is proved is sharper: literal `g` has a decisive common-measure
baseline obstruction, while the smallest coverage-level escape has been
isolated together with the exact additional physical obligations.

## 7. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_signed_coverage_detector.py
```

The replay checks (4)--(5), (14)--(15), the unique explicit signed
representation, pointwise positivity of the surrogate on a finite exact
grid, and the factorization (34).
