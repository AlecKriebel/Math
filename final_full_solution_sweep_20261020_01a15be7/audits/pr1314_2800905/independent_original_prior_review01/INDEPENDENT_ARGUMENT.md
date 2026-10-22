# Independent argument for the exact original Gaussian model

Let p(A) maximize xᵀAx on the nonnegative unit sphere, and let s(A)
maximize Tr(AX) subject to X positive semidefinite, entrywise nonnegative,
and Tr(X)=1. The claim is s(W)→2 in probability and expectation, and
p(W)≤√2+o(1) with probability tending to one, when all independent upper
entries of the symmetric W are N(0,1/n).

The named standard inputs are Sudakov–Fernique in its increment-variance
form and Gaussian Lipschitz concentration, stated as Theorems5.10 and4.7
of [Bandeira's notes](https://people.math.ethz.ch/~abandeira/TenLecturesFortyTwoProblems.pdf),
and the global semicircle law, Definition2.2/Theorem2.4 with Lemma2.1 of
[Benaych-Georges–Knowles v3](https://arxiv.org/pdf/1601.04055v3).
These statements and hypotheses were inspected; their foundational proofs
are explicit imports. The following application steps are independently
verified. The all-ones/projector witness is credited to
[Bandeira–Kunisky–Wein](https://proceedings.mlr.press/v145/bandeira22a.html).

## Stability and rank

Both feasible sets are nonempty and compact. Positive semidefinite trace-one
matrices have nonnegative eigenvalues summing to one, hence bounded norm.
For every such X and symmetric D,

\[
 |\operatorname{Tr}(DX)|\le\|D\|_{op}.
\]

This follows by diagonalizing D and observing that the diagonal entries of
X in that basis are nonnegative and sum to one. Taking maxima gives
\(|s(A)-s(B)|,|p(A)-p(B)|\le\|A-B\|_{op}\), and
\(p(A)\le s(A)\le\lambda_{max}(A)\).
Their absolute values are bounded by ||A||op, hence by ||A||F, so all
expectations below are finite in the finite-dimensional Gaussian model.

A rank-one positive semidefinite trace-one X is xxᵀ with ||x||=1.
Entrywise nonnegativity forces all its nonzero coordinates to have one
common sign; a global sign change puts x in the original feasible set.
Thus a rank-one SDP optimizer exists exactly when s(A)=p(A). A strict
gap excludes every such optimizer, regardless of uniqueness.

## Invariant Gaussian comparison

First use G with diagonal variance2/n and off-diagonal variance1/n, all
upper entries independent. Its density is proportional to
\(\exp[-n\operatorname{Tr}(G^2)/4]\), so it is orthogonally invariant.
For unit x,y, let A_x=xᵀGx and t=xᵀy. Direct expansion yields

\[
 \mathbb E A_xA_y=2t^2/n,\qquad
 \mathbb E(A_x-A_y)^2=4(1-t^2)/n.
\]

For a standard Gaussian vector g, B_x=2gᵀx/√n has increment variance
8(1−t)/n. Subtracting the A increment gives 4(1−t)²/n≥0. These centered
Gaussian processes are continuous on the same compact sets. The comparison
theorem therefore implies

\[
 \mathbb E p(G)\le 2\mathbb E\|g_+\|/\sqrt n\le\sqrt2,
 \qquad \mathbb E\lambda_{max}(G)\le2.
\]

The bound on the linear positive-sphere supremum is an inequality, also
valid if every coordinate of g is negative. It is not asserted equal to
||g_+|| in that case. Jensen and E||g_+||²=n/2 give the first estimate.

Parameterize G by independent standard z_ij, with diagonal coefficient
√(2/n) and upper off-diagonal coefficient1/√n. For any unit x, the squared
coefficient norm of xᵀGx is

\[
 \frac2n\sum_i x_i^4+\frac4n\sum_{i<j}x_i^2x_j^2=2/n.
\]

Suprema of these linear functionals are √(2/n)-Lipschitz. Concentration
gives upper tails at most 2exp(−nt²/4) above √2+t for p(G), and above
2+t for λmax(G). Hence s(G)≤2+o(1) with high probability and Es(G)≤2.
Taking, for example, t=n^(−1/4) makes the one-sided o(1) statement precise.

## Haar projector estimate and feasibility

Fix δ∈(0,1), and r=⌊δn⌋; eventually 1≤r<n. For the projector P onto a
Haar r-plane and a fixed unit vector u, uᵀPu has distribution A_r/A_n,
where A_k is a sum of k independent squared standard Gaussians in a common
sequence. This ratio representation does not assert independence of its
numerator and denominator.

The chi-square moment generating function gives, for t>0,

\[
 \Pr(A_k-k\ge2\sqrt{kt}+2t)\le e^{-t},\qquad
 \Pr(k-A_k\ge2\sqrt{kt})\le e^{-t}.
\]

For completeness, the centered log-mgf is at most kθ²/(1−2θ) for
0<θ<1/2, because −log(1−u)−u≤u²/[2(1−u)]. For the negative parameter
it is at most kθ², using −log(1+u)+u≤u²/2. Markov's inequality with
θ=√t/(√k+2√t), respectively θ=√(t/k), yields the displayed bounds.

Set t=6log n, apply these bounds to A_r,A_n, and use A_n≥n/2 on the
resulting event, for large n. Then

\[
 |A_r/A_n-r/n|\le\frac2n\bigl(|A_r-r|+(r/n)|A_n-n|\bigr)
                  =O(\sqrt{\log n/n}).
\]

The failure probability for a fixed u is at most4n^(−6). Apply this to
(e_i±e_j)/√2 and polarize. A union bound over n(n−1) vectors gives
max_{i≠j}|P_ij|≤C√(log n/n) with failure O(n^(−4)). No independence of
the different vector tests is required.

G has simple spectrum almost surely: the discriminant is a nonzero
polynomial and the Gaussian law has a density. Orthogonal invariance makes
its top-r eigenspace Haar distributed. Let P now denote its projector and,
for fixed α∈(0,1), set

\[
 X=(1-α)P/r+α\mathbf1\mathbf1^T/n.
\]

It is positive semidefinite with trace one. Its diagonal is nonnegative;
off the diagonal it is at least
α/n−(1−α)C√(log n/n)/r. For fixed α,δ, this equals α/n−o(1/n)>0
eventually. Thus X is feasible with probability tending to one. A rank-r
projector alone, or a correction by I/n, need not have this property.

## Spectral edge and expectation

The invariant G satisfies the semicircle theorem's independence, centering,
off-diagonal variance1/n, diagonal O(1/n) variance, and uniform moment
hypotheses. For each fixed η∈(0,2), the semicircle mass m_η in (2−η,2)
is positive. Weak convergence in probability gives that eigenvalue-count
fraction tending to m_η, since the endpoints have zero limiting mass.
Choose fixed 0<δ<m_η. With high probability the leading r eigenvalues
are all greater than2−η. Also q=1ᵀG1/n is N(0,2/n), hence tends to zero
in probability. On intersecting these events and the feasibility event,

\[
 s(G)\ge(1-α)r^{-1}\sum_{j=1}^r\lambda_j(G)+αq
        \ge(1-α)(2-η)+o_P(1).
\]

Given ε>0, first choose sufficiently small fixed η and α, then δ<m_η,
and only then send n→∞. No shrinking interval, edge rigidity, or joint
independence is being assumed. This lower bound and the comparison upper
bound prove s(G)→2 in probability.

Expectation needs an additional argument. I/n is feasible, so s(G)≥T,
where T=Tr(G)/n has mean zero and second moment2/n². For
E_n={s(G)≥2−ε}, with 0<ε<1, Cauchy–Schwarz gives

\[
 \mathbb E s(G)\ge(2-ε)\Pr(E_n)+\mathbb E[T1_{E_n^c}]
                 \ge(2-ε)\Pr(E_n)-\sqrt2/n.
\]

Therefore liminf Es(G)≥2−ε; Es(G)≤2 supplies the limit2. This does not
infer convergence of expectation merely from convergence in probability.

## Exact diagonal transfer and the original answer

Using the same upper standard Gaussians, put W_ii=z_ii/√n and
G_ii=√2 z_ii/√n, with identical off-diagonal entries. Then

\[
 \|W-G\|_{op}=(\sqrt2-1)\max_i|z_{ii}|/\sqrt n.
\]

The Gaussian union bound gives convergence to zero in probability. The
bound E max_i|z_i|≤√(2log(2n)) follows from the exponential-moment bound
E exp(t max_i|z_i|)≤2n exp(t²/2), Jensen, and optimization over t>0.
Thus the perturbation also tends to zero in L1. The deterministic
Lipschitz bounds transfer the SDP probability and expectation limits, and
the true-optimum upper bound, to the original W. With probability tending
to one there is a strict positive gap between2+o(1) and at most√2+o(1).
Consequently no rank-one SDP optimizer exists there. Both original
conjectures are false. The full limit p(W)→√2 is unnecessary and is not
independently asserted as a proved lower bound in this audit.

## The published variance display

The actual published p.154 and v1 PDF2 assign diagonal variance1/n and
off-diagonal variance2/n. In that displayed ensemble H, the variance of
e_1ᵀHe_1 is1/n but that of ((e_1+e_2)/√2)ᵀH((e_1+e_2)/√2) is5/(2n).
Thus that literal model is not invariant. It is √2 G plus a diagonal
operator-norm perturbation tending to zero. The same Lipschitz argument
therefore gives s(H)→2√2, rather than2. The literal variance sentence
cannot be used unchanged to invoke the theorem's claimed normalization.

The intended standard convention is identified mathematically by the
Haar-projector argument and its stated quadratic-form variance2/n. Calling
the reversal a typographical slip is a supported diagnosis, not an
author-confirmed erratum. The explicit reconstruction above establishes
the needed normalization and original-model transfer without assuming
such confirmation. No quantitative shrinking-parameter remark in the
published paper is needed or certified here.
