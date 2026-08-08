# The stationary entropy-reflection reduction at dB fitness two

Date: 2026-08-02 (America/Los_Angeles)

## Status

The identities in Sections 1--3 are **PROVED** for every loopless
row-stochastic kernel.  They reduce the stationary-dual half-density problem
at fitness two to the single Shannon-information inequality

\[
 H(C\mid B)\ge I(V;B).                                      \tag{1}
\]

Here `V` is the uniformly chosen update target, `B` is the stationary output,
and `C` records whether the target was occupied before the update.  Inequality
(1) remains **OPEN**.  If true, it proves

\[
 E_\Pi |B|\le n/2
 \quad\hbox{and hence}\quad
 \rho_{\rm dB}(G,2)\le 1/2.                                \tag{2}
\]

The reduction exposes a precise cross-density reflection term.  It also
shows why two tempting entropy proofs do not close: the integrand of (1) has
both signs even for the complete graph, and the effective-update channel can
strictly *decrease* entropy on a positive regular weighted `K_4`.  Both
failures are certified exactly below.

Natural logarithms are used throughout.

## 1. The stationary target experiment

Let `Pi` be stationary for the uniform-target geometric-union dual at
fitness two.  Draw

\[
 A\sim\Pi,\qquad V\sim {\rm Unif}(\{1,\ldots,n\}),
 \qquad B\sim K_V(A),                                      \tag{3}
\]

where `A` and `V` are independent.  Put

\[
 C=1_{\{V\in A\}}.                                        \tag{4}
\]

Thus `C=0` is a null update and then `B=A`; if `C=1`, the target is
deleted and replaced by a fair-geometric union of independent samples from
row `P_V`.  Stationarity gives `B~Pi`, and every `V`-output omits `V`.

For a fixed target `v`, let

\[
 \mu_v=\Pi K_v,\qquad
 R_v(B)=\Pi(B)1_{\{v\notin B\}},\qquad
 \nu_v=\mu_v-R_v.                                         \tag{5}
\]

The measure `nu_v` is exactly the effective incoming mass.  If `v` is a
hole of `B`, define

\[
 e_v(B)={\nu_v(B)\over\Pi(B)}.                            \tag{6}
\]

Stationarity and target exclusion imply, pointwise for `k=|B|` and
`h=n-k`,

\[
 \sum_{v\notin B}e_v(B)=k.                                \tag{7}
\]

Consequently

\[
 \Pr(V=v\mid B)={1+e_v(B)\over n}\quad(v\notin B),        \tag{8}
\]

and

\[
 \Pr(C=1\mid B)={k\over n}.                               \tag{9}
\]

Write `tau_B` for the posterior distribution in (8), supported on the
`h` holes.  Since `A` and `B` have the same law, (9) gives the exact identity

\[
 M:=E_\Pi h_2(|A|/n)=E_\Pi h_2(|B|/n)=H(C\mid B),          \tag{10}
\]

where `h_2(x)=-x log x-(1-x)log(1-x)`.

## 2. Exact entropy reflection

The target information is

\[
 I(V;B)=\log n-E_\Pi H(\tau_B).                            \tag{11}
\]

Combining (10)--(11), state by state, gives

\[
 \boxed{
 M-I(V;B)
 =E_\Pi\left[
 H(\tau_B)-{k\over n}\log k-{h\over n}\log h
 \right].}                                                \tag{12}
\]

Equivalently, because
`D(tau_B || Unif(B^c))=log h-H(tau_B)`,

\[
 \boxed{
 M-I(V;B)
 =E_\Pi\left[
 {k\over n}\log{h\over k}
 -D\!\left(\tau_B\middle\|{\rm Unif}(B^c)\right)
 \right].}                                                \tag{13}
\]

Thus the missing theorem is a genuine reflection inequality: low-density
states must compensate both the negative logarithmic contribution of
high-density states and the posterior nonuniformity within the holes.

### 2.1 Why (1) proves half density

Let `x=E|B|/n`.  Since `tau_B` is supported on `h=n-|B|` points,

\[
 I(V;B)
 \ge \log n-E\log h
 \ge -\log(1-x).                                          \tag{14}
\]

Concavity of binary entropy gives

\[
 M\le h_2(x).                                             \tag{15}
\]

If (1) holds, then (14)--(15) imply

\[
 -\log(1-x)\le h_2(x).
\]

After cancellation this is

\[
 x\log{1-x\over x}\ge0,
\]

so `x<=1/2`.  The duality identity
`rho_dB(G,2)=E|B|/n` then proves (2).

### 2.2 Complete-graph equality is cross-level, not pointwise

For the complete kernel,

\[
 \Pi_K(B)={|B^c|\over n(2^{n-1}-1)},                      \tag{16}
\]

and label symmetry makes `tau_B` uniform on `B^c`.  Hence the divergence in
(13) vanishes.  The remaining sum is zero by pairing levels `k` and `n-k`:

\[
 \sum_{k=1}^{n-1}{\binom nk k(n-k)\over
 n^2(2^{n-1}-1)}\log{n-k\over k}=0.                       \tag{17}
\]

Therefore `M=I(V;B)` on every complete graph at fitness two.  But the
integrand is not nonnegative: on a complete `K_4` state of size three it is

\[
 {3\over4}\log{1\over3}<0.                                \tag{18}
\]

Any proof must retain cross-level cancellation.

## 3. Exact active-channel decomposition

Put `p_v=Pr(v in A)`.  Conditional on an effective target `v`, define

\[
 S_v={\cal L}(A\setminus\{v\}\mid v\in A),\qquad
 N_v={\cal L}(B\mid V=v,C=1).                             \tag{19}
\]

The first law is the deleted active source and the second is its effective
output.  Both are probability laws on subsets omitting `v`.

There is an exact decomposition

\[
 \boxed{
 M-I(V;B)
 = I(C;V\mid B)
 +{1\over n}\sum_v p_v\{H(N_v)-H(S_v)\}.}                \tag{20}
\]

To prove it, map `(A,V)` bijectively to `(C,V,D)`, where `D=A` on a null
update and `D=A\setminus{V}` on an effective update.  The null parts of
`(C,V,D)` and `(C,V,B)` agree exactly.  On the effective part their entropy
difference is the second term of (20).  Also

\[
 H(C,V,B)-H(C,V,D)=H(C\mid B,V)-I(V;B).
\]

Finally `M=H(C|B)` by (10), so adding
`I(C;V|B)=H(C|B)-H(C|B,V)` proves (20).

The first term in (20) is nonnegative.  It is tempting to claim that the
second is also nonnegative.  That claim is **EXACTLY FALSE**.

### 3.1 Exact regular `K_4` counterexample to active entropy expansion

On vertices `0,1,2,3`, give the four cycle edges

\[
 01,12,23,30
\]

weight `4`, and the two diagonals `02,13` weight `1`.  This is a connected,
positive-support, regular weighted graph of weighted degree nine.

Every vertex has

\[
 p_v={168\over395}.                                       \tag{21}
\]

Up to relabeling, the probability multisets of `S_v` and `N_v` are

\[
\begin{aligned}
 S_v:&\quad
 \left\{{1\over4},{43\over168},
 2\times{13\over96},3\times{25\over336}\right\},\\
 N_v:&\quad
 \left\{2\times{37\over336},{5\over168},
 2\times{13\over96},{43\over168},{25\over112}\right\}.
\end{aligned}                                             \tag{22}
\]

Exact prime collection yields

\[
 H(N_v)-H(S_v)
 ={1\over336}\log
 {2^{158}3^9 7^{84}\over5^{10}37^{74}}<0.                \tag{23}
\]

The strict sign is an integer comparison, checked independently by the
verifier.  Hence the active contribution in (20) is

\[
 {1\over790}\log
 {2^{158}3^9 7^{84}\over5^{10}37^{74}}<0.                \tag{24}
\]

For this graph the full gap `M-I(V;B)` is nevertheless strictly positive:
`I(C;V|B)` more than compensates (24).  Thus (20) is a useful exact split,
but neither summand has the desired sign separately.

## 4. Relation to the order-two route

The same posterior experiment gives

\[
 I_2(V;B)
 =1+{E|B|\over n}
 +{1\over n}E\sum_{v\notin B}e_v(B)^2.                    \tag{25}
\]

The sharp conjecture `I_2(V;B)<=2` would also prove half density.  The
fair-geometric midpoint resolvent gives exact linear identities for the
effective measures, but fixed-reference `L^2` contraction and revealing the
effective/null flag both have exact counterexamples; see
`chi_square_channel/RESOLVENT_IDENTITIES.md`.  The Shannon formula (13) and
the chi-square formula (25) therefore share the same unresolved feature:
the null/effective and low/high-density cancellations must be kept before a
convex functional is applied.

Three further standard Shannon routes also fail exactly.  The normalized
Cayley reverse channel reverses every labelled fair-geometric path with the
same probability, so its path-space entropy production is identically zero
rather than (13).  The output experiment is not a Blackwell garbling of the
membership experiment: on the unweighted three-path, target-row total
variation increases from `7/9` to `5/6`.  Finally, full convex-order
comparison of the two likelihood ratios fails on the `(7,1,1)` triangle,
where the stop-loss difference at threshold `3/2` is `-8/327`.  These exact
certificates are proved and checked in
`chi_square_channel/SHANNON_REFLECTION.md`.

## 5. Verification and current boundary

Run

```text
python3 verify_entropy_reflection.py
python3 chi_square_channel/verify_resolvent_identities.py
python3 chi_square_channel/verify_shannon_routes.py
```

Both scripts use exact rational arithmetic for the Markov chain.  The first
represents every entropy expression as a rational linear combination of
prime logarithms, so all identities and asserted strict signs are checked by
integer arithmetic rather than floating point.

The present classification is:

- **PROVED:** posterior formulas (7)--(9), reflection identities (12)--(13),
  the implication (1) `=>` half density, decomposition (20), and complete
  equality (17).
- **EXACTLY COMPUTED:** the regular weighted `K_4` counterexample
  (21)--(24) to separate active entropy expansion; zero entropy production
  of the exact Cayley path reversal; the path total-variation obstruction;
  and the triangle convex-order obstruction.
- **NUMERICALLY OBSERVED:** random and continuous searches over reversible
  and directed kernels through six vertices found no negative value of
  `M-I(V;B)`.
- **OPEN:** the universal entropy-reflection inequality (1), the sharp
  chi-square bound `I_2<=2`, and therefore the all-graph half-density ceiling.
