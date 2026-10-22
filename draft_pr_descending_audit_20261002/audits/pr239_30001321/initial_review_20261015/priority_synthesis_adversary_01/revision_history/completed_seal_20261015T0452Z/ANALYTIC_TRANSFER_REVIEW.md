# Independent analytic review of the two new audit bridges

2026-10-15 UTC. These are deductions checked for this synthesis audit. They do
not assign an earlier date to a newly written argument. Input hashes are in
`INPUT_PINS.json`.

## 1. Quantitative TURN_2 input

Fix one scalar iid law, and put

\[
\gamma=5/16,\quad\beta=9/32,\quad\eta=1/64,\quad b=1/128.
\]

The occupation estimate in TURN_2 is explicit for **every** integer moment
order, with the same constant in `k! C^k L^(k/2)`. Thus choose, for example,
`k=floor(log n)`. Markov's bound at `n^eta sqrt(L)` has logarithm at most

\[
k\log k+O(k)-\eta k\log n\le-c(\log n)^2
\]

for large n. A union over the `O(log n)` deterministic dyadic blocks keeps
this form. The bridge file's larger choice `k` proportional to `log^2 n`
also works: its leading negative term is of order `log^3 n`. Constants do
not secretly depend on k beyond the displayed factorial/exponential factor.

For terminal sign tests, insert a threshold `u=c_0 n^(-b)` into the actual
Freedman denominator, retaining its increment term. The predictable variance
is at most `C n^(eta-beta) log n`; the increment times u is smaller. Hence
the exponent is at least

\[
c n^{\beta-\eta-2b}/\log n=c n^{1/4}/\log n.
\]

The sign entropy is `O(n^(1/2-gamma) log n)=O(n^(3/16) log n)`, so it is
absorbed. The overlap event is charged once, outside this union. The
annealed central-window tail and the quenched last-segment displacement
have expectation `exp[-c log^2 n]`; division by the shrinking threshold
costs only `n^b`, which is absorbed by reducing c.

For the boundary test, its mean is at most

`C n^(beta-gamma)+C n^(beta-1/2)=O(n^(-1/32))`,

which is `o(n^(-b))`. The variance part of the concentration exponent is

\[
2\beta-1/2-\eta-2b=1/32>0.
\]

Its increment term is again smaller. All necessary constants are uniform
over deterministic alignment and over lengths `H>=n^gamma`. Taking a
sufficiently small fixed c_0 in the finitely many threshold allocations
therefore proves

\[
\mathbb P(L^z_{n,H}>n^{-b})\le C\exp[-c(\log n)^2].\tag{H}
\]

Stationarity gives the same bound at each fixed starting space-time point
z. This is a probability bound uniform in z, not a claim that one event
works simultaneously for infinitely many z. The later finite union over
sites supplies the simultaneous event actually needed.

## 2. The multiscale recurrence

Let `rho=7/8`. For `M<N^gamma`, take decreasing integer segment times
`n_j` comparable to `N^(rho^j)`, stopping at the first r with
`n_r^gamma<=M`. Restrict M initially to exceed a fixed large constant, so
all segment times are above the input threshold. The initial time
`t_0=N-sum_j n_j` is at least `N/2` eventually. Its cell length
`h_0=ceil(N^gamma)` is above `t_0^gamma`, so (H) initializes the recurrence.

At stage j, the old cell length is
`h=h_(j-1)<=C n_j^(gamma/rho)`. All measures have the same parity at the
old time. The annealed same-parity smoothing error within a cell is

\[
C h/\sqrt{n_j}\le Cn_j^{-d},\qquad
d=1/2-\gamma/\rho=1/7.
\]

Call a cell bad if (H) fails for any reachable-parity starting site in
it, for that segment and the next deterministic partition. It has at most
`h+1` sites. Thus its bad probability is at most
`p_n=C exp[-c_1 log^2 n]`, after absorbing its polynomial site count.

The crucial replacement is **deterministic annealed cell masses, random
quenched conditional laws within cells**. Contraction charges the previous
coarse discrepancy exactly. It also makes the bad-cell weights
`w_J=alpha_(t_(j-1))(J)` deterministic; no random old mass is inserted into
the concentration calculation. In a zero quenched-mass cell choose any
same-parity old site in that cell; if its annealed mass is also zero its
choice is irrelevant. An annealed-positive cell has such a reachable site.

Triangle inequality and annealed smoothing give

\[
\lambda_j\le\lambda_{j-1}+n_j^{-b}+2 B_j+C n_j^{-d},\qquad
B_j=\sum_Jw_J1_{\{J\text{ bad}\}}.\tag{R}
\]

This uses independence of fresh time layers for the exact annealed
semigroup identity. It does not require different starting kernels to be
independent.

## 3. Failure probabilities stay on the N scale

For `n_j>N^(1/4)`, the union over at most `O(N)` old cells and
`O(log log N)` stages costs at most `C exp[-c_2 log^2 N]`. No bad cell
occurs at these stages outside that event.

For `n=n_j<=N^(1/4)`, a bad-cell event depends on the segment's finite
space-time cone. Deterministic old cells can be colored with
`D<=C(1+n/h)` colors so that cones in each color are disjoint. All old
times are at least `N/2`, and binomial spread gives

\[
\max_Jw_J\le Ch/\sqrt N,\qquad
D\sum_Jw_J^2\le C(n+h)/\sqrt N\le Cn/\sqrt N.
\]

The last inequality uses `h<=C n^(gamma/rho)` with `gamma/rho<1/2`;
it is valid uniformly above the fixed segment threshold. Hölder across
colors and Hoeffding within each independent color give

\[
\mathbb P(B_j>p_n+t)\le\exp[-c t^2\sqrt N/n].\tag{C}
\]

Take `t=n^(-b)` here; `b=1/128<1/8`. Then `p_n<=n^(-b)` eventually,
and the exponent is at least

\[
cN^{1/2-(1+2b)/4}=cN^{63/256}.
\]

Union over stages is harmless. Independence between stages is neither
claimed nor needed. A terminal-scale union bound alone would instead have
given a tail in M, which is insufficient at `M=log log N`; this argument
avoids exactly that error.

The inverse powers in (R) sum to `C n_r^(-b)`, uniformly in the number
of stages: their logarithms increase geometrically when the stages are
read backward. The stopping rule and `n_r` comparable to
`n_(r-1)^rho` give `n_r>=cM^(rho/gamma)`. Thus

\[
\mathbb P\left(L_{N,M}>CM^{-7/320}+CN^{-1/128}\right)
\le C\exp[-c'(\log N)^2].\tag{Q}
\]

For `M>=N^gamma`, (H) proves the stronger bound directly. Rounding changes
only constants, once M is above a fixed threshold. The proof can use
real target intervals as well: their terminal stage only requires (H) for
that interval geometry, and TURN_2's real periodic boundary majorants and
cell counting extend directly with additive one-site errors. The integer
version of the bridge alone already proves the requested numerical rate;
the frozen candidate separately proves the real-length extension.

For every fixed epsilon and every deterministic `M_N->infinity`, (Q)'s
deterministic error is eventually smaller than epsilon. The failure tail
beats every fixed inverse power of N. There is no hidden lower growth
rate for M_N and no uniformity over laws approaching arrows.

One expository refinement identified during this review was accepted:
the **generic** bridge proof introduces `b_1<=min(b,1/8)`, so its readily
quotable sufficient range is `a<=min(b,1/8,d)`. The repaired statement now
exposes that cap and explicitly chooses `b_1>=a`. I checked its complete
diff and both the preserved original and new public seals. The particular
rate in (Q) is unaffected. `FINAL_RESEAL_CHECK.json` records the hashes.

## 4. Uniform quasi-locality really concentrates the stationary factor

Suppose an iid field has a finite alphabet and a real finite functional
Phi, defined on a full-measure domain, has uniform cylinder oscillations
tending to zero. Fix a radius whose oscillation is at most one. There
are finitely many nonempty cylinder classes, and finitely many finite
representative values. Every Phi value is within one of its class's
representative. Thus Phi is essentially bounded. This conclusion would
be false for mere L2 approximation; it uses **uniform** oscillation.

For each fixed delta, choosing a fixed larger radius produces a bounded
cylinder function `Psi_R` of expectation one with
`||Phi-Psi_R||_infinity<=2delta`. There is a common full-measure domain
for all countably many shifts. Let `b_N` be the binomial weights in the
sheared coordinate and

\[
H_N(\Psi)=\sum_I\left|\sum_{x\in I}b_N(x)
                       (\Psi(T_{x,N}\eta)-1)\right|.
\]

Finite-range covariance and Cauchy-Schwarz on the cells meeting a
central window of radius `A sqrt(N)` give

\[
\mathbb EH_N(\Psi_R)\le C_R\sqrt{A/M+N^{-1/2}}
                         +C(B_R+1)/A^2.
\]

For tails this uses absolute boundedness, not positivity of the recentered
approximant. Fix A, let N and M_N grow, then increase A. Hence the
expectation vanishes for every divergence rate and deterministic alignment.

Changing one independent field coordinate z changes H_N by at most
`C_R sum_(|x-z_space|<=R)b_N(x)`. Only a fixed number of time layers
occurs. Summing these actual squared weights and applying the discrete
convolution inequality yields

\[
\sum_zc_z^2\le C_R\sum_x b_N(x)^2\le C_R/\sqrt N.
\]

Bounded differences therefore gives a fixed-epsilon failure probability
`exp[-c_(epsilon) sqrt(N)]` after choosing delta and then R depending
only on epsilon. No quantitative rate of quasi-locality is needed.
The positive stationary-factor claim in `QUASILOCAL_SOURCE_BRIDGE.md`
passes this independent check.

This does not control a separate local-limit residual. A qualitative
almost-sure or L2 residual can have fixed polynomial failure probability.
For instance `1_(A_N)` with `P(A_N)=N^(-2)` tends to zero almost surely
but fails every-K concentration. Nor can a theorem for each fixed finite
alphabet automatically be substituted along approximations changing with
N when its constants and onset depend on that alphabet or law.

## 5. The density-identification caution passes

For a fixed two-atom iid law on `{r,1-r}`, both atoms positive and
`0<r<1/2`, enforce inward drift toward the edge `{0,1}` on a finite
backward cone. This event has positive probability. For its deterministic
comparison kernel P, put `d=1-2r`, `rho=r/(1-r)` and
`pi_0=pi_1=(1-rho)/2`. Direct column sums and reversibility give

\[
u_T(0)=1+d\sum_{s<T}[P^s(0,0)+P^s(1,0)],\qquad
P^{2n}(0,0)\ge\pi_0.
\]

Consequently `u_T(0)>=1+d pi_0 ceil(T/2)`. Under the exact shear, all
other-parity starting sites have zero endpoint-zero transition probability;
the column sum is exactly the JRS finite-past martingale `f_T`. JRS's
L2 convergence implies `f_T=E[f|last T layers]`. If f were essentially
bounded, every f_T would have the same bound, contradicting the positive
finite-cone events. Therefore f is unbounded for this fixed finite-state
uniformly elliptic law.

A literal uniformly quasi-local finite-alphabet Phi is bounded and cannot
equal this f, even in distribution. The caution is valid. It does **not**
identify the unread BMP object with JRS f and does not refute BMP. Precise
BMP assumptions, functional definition, residual, and object identification
remain source questions.

## 6. Dating conclusion

The analytic transfer is complete for the stated numerical parameters, and
the quasi-local positive implication is valid. Neither new audit derivation
can be assigned the date of its oldest ingredient. BRAS's dated Green
estimate supplies the conditional occupation moments by first hitting and
ordered-time expansion; elementary concentration supplies the rest of (H)
through the argument explicitly checked above. That proves a route today.
It does not show that a source previously stated the scalar quantitative
comparison or a model-general theorem which makes this route an earlier
published corollary. Conversely, lack of such an authenticated source is
not proof that the scalar application is novel.
