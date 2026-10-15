# Independent audit of positive PCA tightness

## Verdict

**PASS: complete, correctly attributed negative resolution of the original Gaussian problem.** The audited candidate proves that the trace-one, entrywise-nonnegative semidefinite relaxation has value tending to 2 in probability and in expectation, whereas the nonnegative unit-vector optimum is at most sqrt(2) + o(1) with probability tending to one. Consequently, with probability tending to one, no SDP optimizer has rank one. Both conjectures in Afonso S. Bandeira's Open Problem 9.5 are disproved.

This is an independently checked reconstruction and application of an existing result of Bandeira, Kunisky and Wein, not a new mathematical discovery. No correction to the frozen candidate is required for this verdict. The stronger statement that the true optimum converges to sqrt(2) is correctly attributed to Montanari and Richard; its lower bound is not proved by the candidate and is unnecessary for the negative resolution.

Audited item: row 1760, problem 2800905, original assessed manuscript, exactly 11,969 bytes, SHA-256 `5251358434993a8021986f760f9a99710fededdd98d842bc9de14b1d2dd947e4`. The original file and the audit snapshot matched this pin. The conclusions below concern these exact bytes. The public edition is PROOF.md; EDITORIAL_CHANGES.json records its editorial-only differences and the corresponding presentation edit in this report.

## Original question and publication

Bandeira's notes dated October 10, 2016, printed pages 130–131, define the vector problem by x >= 0 and ||x||_2 = 1. Equations (103)–(104) impose X positive semidefinite, X entrywise nonnegative, and Tr(X) = 1. Open Problem 9.5 asks whether the expected SDP value is sqrt(2) + o(1) and whether its solution has rank one with high probability, for Gaussian Wigner entries normalized to variance 1/n. The preceding discussion describes independent Gaussian entries subject to symmetry. There is no planted signal in this question.

The author's November 28, 2015 blog entry identifies the same problem by number and subject. Replacing Tr(X) = 1 and entrywise nonnegativity by diagonal constraints X_ii = 1 changes the optimization problem. Adding a planted spike also changes the random model. The candidate's rejection of that alternative framing is justified. This audit addresses the actual unspiked problem.

Primary references:

- A. S. Bandeira, *Ten Lectures and Forty-Two Open Problems in the Mathematics of Data Science*, October 10, 2016, pp. 130–131, Open Problem 9.5: https://people.math.ethz.ch/~abandeira/TenLecturesFortyTwoProblems.pdf
- Original blog locator: https://afonsobandeira.wordpress.com/2015/11/28/10l42psbm/
- A. Bandeira, D. Kunisky and A. Wein, *Average-Case Integrality Gap for Non-Negative Principal Component Analysis*, PMLR 145, 153–171, publisher citation year 2022: https://proceedings.mlr.press/v145/bandeira22a.html
- Published PDF, Theorem 4, pp. 157–158: https://proceedings.mlr.press/v145/bandeira22a/bandeira22a.pdf
- Preprint version, Theorem 3, submitted December 3, 2020: https://arxiv.org/abs/2012.02243v1

The proceedings PDF's header and copyright use 2021, while the official publisher citation uses 2022. The candidate describes this discrepancy accurately. The published paper explicitly connects its result to Open Problem 9.5. Its projector-plus-all-ones witness is the construction used in the candidate.

## Normalization and the source error

The publisher PDF, printed page 154, visibly assigns variance 1/n to diagonal entries and 2/n to off-diagonal entries while calling this GOE. The same reversal occurs in the version-1 preprint. This is not a text-extraction artifact: the publisher page was rendered and visually inspected in this audit.

For the invariant normalization used by the proof, the correct assignments are Var(G_ii) = 2/n and Var(G_ij) = 1/n for i < j. The density on symmetric matrices is proportional to exp(-n Tr(G^2)/4), so orthogonal conjugation preserves the law. In particular the relevant eigenspace projectors are Haar distributed. In this normalization every deterministic unit vector u has Var(u^T G u) = 2/n.

The displayed reversed-variance model is not invariant: its quadratic-form variance at e_1 is 1/n, whereas at (e_1 + e_2)/sqrt(2) it is 5/(2n). For u = 1/sqrt(n), it is 4/n - 3/n^2. It therefore cannot literally support the Haar-eigenspace and 2/n variance claims used in the published proof. Equivalently, that reversed-variance model is sqrt(2) times invariant GOE up to an asymptotically negligible diagonal perturbation, so its spectral scale is 2 sqrt(2), not 2.

Calling the variance display a typo is a well-supported mathematical diagnosis from the surrounding statements and proof, not a verified author-issued erratum. No author confirmation was obtained. Crucially, the candidate does not need to assume such confirmation: it explicitly defines the correct invariant model, gives the argument in that model, and then proves the transfer to the original all-upper-triangular-variance-1/n model. The reconstruction is mathematically valid independently of how the publisher error is labeled.

## Detailed mathematical audit

Write K = {x in R^n: x >= 0, ||x||_2 = 1} and F = {X in R_sym^(n x n): X >= 0 entrywise, X positive semidefinite, Tr(X) = 1}. Let p(A) = max_K x^T A x and s(A) = max_F Tr(AX).

### Existence, stability, and rank one

K is closed and bounded and nonempty. F is closed and nonempty; its eigenvalues are nonnegative and sum to 1, whence ||X||_F <= 1. Thus both maxima exist. For symmetric D and positive semidefinite trace-one X, diagonalizing D gives Tr(DX) = sum_i lambda_i(D) (U^T X U)_ii, a convex combination of eigenvalues. Consequently |Tr(DX)| <= ||D||_op. This proves |s(A)-s(B)| <= ||A-B||_op, and the identical argument with X = xx^T proves this for p. It also proves p(A) <= s(A) <= lambda_max(A).

Every rank-one positive semidefinite trace-one matrix is xx^T with ||x||_2 = 1. If it is entrywise nonnegative, two nonzero coordinates cannot have opposite signs. Changing the global sign therefore places x in K. The converse is immediate. Since optima are attained, a rank-one SDP optimizer exists if and only if s(A) = p(A). This is an existence equivalence; no uniqueness assumption is used. A strict gap excludes every rank-one optimizer.

**Result: pass.**

### Gaussian comparison and concentration

Use independent standard Gaussian variables z_ij with G_ii = sqrt(2/n) z_ii and G_ij = G_ji = z_ij/sqrt(n), i < j. For A_x = x^T Gx, direct expansion yields

E[A_x A_y] = (2/n) (x^T y)^2,
E[(A_x-A_y)^2] = (4/n) (1-(x^T y)^2).

For B_x = (2/sqrt(n)) g^T x with a standard Gaussian vector g, the increment variance is (8/n)(1-x^T y). The difference between this quantity and the A increment variance is (4/n)(1-x^T y)^2 >= 0. Both processes are centered, continuous, and almost surely bounded on K and on the full unit sphere. Sudakov–Fernique therefore applies on either set.

On K, sup g^T x <= ||g_+||_2. Equality holds if g has a positive coordinate; the inequality remains true if all coordinates are negative. Jensen and E[(g_i)_+^2] = 1/2 give E p(G) <= sqrt(2). On the whole sphere the linear supremum is ||g||_2, giving E lambda_max(G) <= 2. The coefficient vector of x^T Gx as a functional of z has squared norm

(2/n) sum_i x_i^4 + (4/n) sum_(i<j) x_i^2 x_j^2 = 2/n.

The supremum of these linear functionals is sqrt(2/n)-Lipschitz. Gaussian concentration gives P(p(G) > sqrt(2)+t) <= 2 exp(-nt^2/4), and similarly P(lambda_max(G) > 2+t) <= 2 exp(-nt^2/4). No independence between maximizers and the matrix has been assumed.

The referenced forms of comparison and concentration are stated in Bandeira's notes, Theorems 5.10 and 4.7, printed pages 84 and 61. The notes prove a weaker concentration constant in their exposition but explicitly state the sharp inequality invoked here. Accepting the stated standard theorem, the candidate's constant is correct. In any event, the weaker displayed proof would suffice for the asymptotic conclusions.

All finite-n expectations exist, since these maxima are Lipschitz functions of a finite-dimensional Gaussian vector. Thus E s(G) <= 2 is justified without assuming that the SDP value is nonnegative.

**Result: pass.**

### Haar projector entry bound

Fix delta in (0,1) and set r = floor(delta n). For all sufficiently large n, 1 <= r < n. If P is the orthogonal projection onto a Haar r-dimensional subspace and u is a deterministic unit vector, then u^T P u has the law A_r/A_n, where A_k = sum_(i=1)^k Z_i^2 for independent standard Gaussians. This follows by rotating u and representing a uniform unit vector as Z/||Z||. Numerator and denominator in this representation need not be independent.

For A_k the moment-generating function is (1-2 theta)^(-k/2), theta < 1/2. The elementary logarithmic bounds for its centered logarithm are

log E exp(theta(A_k-k)) <= k theta^2/(1-2 theta), 0 < theta < 1/2,
log E exp(-theta(A_k-k)) <= k theta^2, theta > 0.

Chernoff optimization gives the candidate's upper threshold 2 sqrt(kt)+2t and lower threshold 2 sqrt(kt), each with failure probability at most exp(-t). When the lower threshold exceeds k, the lower event is empty. This verifies the stated tail bounds rather than relying on author software.

Take t = 6 log n and apply the bounds to A_r and A_n. Except on probability at most 4 n^(-6), A_n >= n/2 for large n and

|A_r/A_n-r/n| <= (2/n) (|A_r-r| + (r/n)|A_n-n|)
               <= C sqrt(log(n)/n).

The same absolute constant can be enlarged to absorb log(n)/n; a delta-dependent constant as claimed is harmless. For each i<j, set u_plus = (e_i+e_j)/sqrt(2), u_minus = (e_i-e_j)/sqrt(2). Polarization gives P_ij = (u_plus^T P u_plus-u_minus^T P u_minus)/2. There are n(n-1) such test vectors. A union bound has failure at most 4 n^(-4), yielding max_(i != j)|P_ij| <= C sqrt(log(n)/n). No independence of these tests is needed. Flooring r introduces no subsequence restriction.

**Result: pass.**

### Eigenspace distribution and feasible witness

G has the invariant density given above. The repeated-eigenvalue locus is the zero set of the nonzero discriminant polynomial, hence has Lebesgue measure zero. The top-r spectral projector is therefore almost surely defined and transforms equivariantly under orthogonal conjugation. Its distribution is the invariant probability measure on the Grassmannian, so the preceding projector bound applies. Independence of eigenvectors and eigenvalues is stronger than needed and is not invoked.

For fixed alpha, delta in (0,1), define X = (1-alpha)P/r + alpha 11^T/n. Both normalized summands are positive semidefinite with trace one. Thus X is positive semidefinite with trace one, and its diagonal is nonnegative. On the projector event its off-diagonal entries satisfy

X_ij >= alpha/n - ((1-alpha)/r) C sqrt(log(n)/n).

Since r/n tends to delta > 0, the error is O_delta(sqrt(log(n))/n^(3/2)), which is o(1/n). For every fixed alpha > 0 the entries are eventually nonnegative. This is the precise domination needed: entry bounds merely tending to zero before division by r would not alone be enough, but the candidate uses the stronger bound correctly.

The matrix is therefore feasible with probability tending to one. On that event,

s(G) >= (1-alpha) r^(-1) sum_(j=1)^r lambda_j(G) + alpha u^T Gu,

where eigenvalues are decreasing and u = 1/sqrt(n).

**Result: pass.**

### Semicircle input and limit order

The candidate invokes the global semicircle law only for a fixed interval, not for edge rigidity or a dimension-dependent shrinking interval. For G, the conditions in Benaych-Georges and Knowles, Definition 2.2, hold: independent upper-triangular centered entries, variance 1/n off the diagonal and O(1/n) on it, and bounded moments of sqrt(n)G_ij of every fixed order. Theorem 2.4 gives convergence of Stieltjes transforms in probability; Lemma 2.1 on page 8 converts this to weak convergence in probability of empirical spectral measures. The density is (1/(2 pi))sqrt(4-t^2) on [-2,2]. Source: https://arxiv.org/pdf/1601.04055v3.

For each fixed 0 < eta < 2, m_eta = integral_(2-eta)^2 (1/(2 pi))sqrt(4-t^2) dt is positive. The endpoints have zero mass, so the proportion of eigenvalues in that interval converges in probability to m_eta. This also follows by sandwiching its indicator with continuous bounded functions. Choose fixed 0 < delta < m_eta. With probability tending to one, at least floor(delta n) eigenvalues exceed 2-eta; therefore their leading-r average is at least 2-eta. Meanwhile u^T G u is centered Gaussian with variance 2/n, and tends to zero in probability.

Intersect the feasibility, spectral-count, and quadratic-form events using a union bound. No independence assumption is necessary. Given epsilon > 0, choose eta and alpha sufficiently small that (1-alpha)(2-eta) > 2-epsilon/2; then choose delta < m_eta. These parameters are held fixed while n tends to infinity. The lower bound s(G) >= 2-epsilon follows with probability tending to one. Together with the previous upper bound this proves s(G) -> 2 in probability. The choice of delta after alpha is not problematic; any fixed positive alpha dominates the off-diagonal correction for sufficiently large n.

**Result: pass.**

### Expectation convergence

Convergence in probability alone would not justify a statement about expectation. The candidate correctly supplies a separate argument. I/n is feasible, so s(G) >= T = Tr(G)/n. Since the n diagonal entries have variance 2/n, E T = 0 and E T^2 = 2/n^2.

For E_n = {s(G) >= 2-epsilon}, splitting the expectation and applying Cauchy–Schwarz gives

E s(G) >= (2-epsilon)P(E_n) + E[T 1_(E_n^c)]
       >= (2-epsilon)P(E_n) - sqrt(2)/n.

It is enough to use 0 < epsilon < 1, so no sign issue arises. There is no assertion that T is independent of E_n. Since P(E_n) -> 1, liminf E s(G) >= 2-epsilon. The upper bound E s(G) <= E lambda_max(G) <= 2 gives the desired expectation limit. The candidate neither needs nor silently assumes uniform integrability.

**Result: pass.**

### Transfer to the original Wigner normalization

Couple W and G by their common off-diagonal variables and W_ii = z_ii/sqrt(n), G_ii = sqrt(2)z_ii/sqrt(n). Each matrix has its required independent upper-triangular entries. Their difference is diagonal and

||W-G||_op = (sqrt(2)-1) max_i |z_ii|/sqrt(n).

Gaussian tails give P(max_i |z_ii| > a) <= 2n exp(-a^2/2), which tends to zero at every fixed positive multiple of sqrt(n). For expectation, exp(t max_i|z_i|) <= sum_i(exp(tz_i)+exp(-tz_i)); Jensen then gives E max_i|z_i| <= log(2n)/t + t/2. Setting t = sqrt(2 log(2n)) proves the candidate's bound. Thus the operator-norm perturbation tends to zero both in probability and in L1.

The deterministic Lipschitz inequalities now transfer s(G) -> 2 in probability and expectation to W. They also transfer the one-sided probabilistic bound on p(G), and even give limsup E p(W) <= sqrt(2). No eigenvector universality theorem for the noninvariant model W is required.

For any fixed t with 0 < t < (2-sqrt(2))/4, the events s(W) >= 2-t and p(W) <= sqrt(2)+t intersect with probability tending to one. On that intersection s(W) > p(W), excluding every rank-one optimizer by the proved equivalence. This is precisely the desired negative answer, with a stronger no-rank-one-optimizer conclusion than is needed to refute typical rank-one optimality.

**Result: pass.**

## The attributed true optimum limit

Montanari and Richard's *Non-negative Principal Component Analysis: Message Passing Algorithms and Sharp Asymptotics*, https://arxiv.org/abs/1406.4775, defines the symmetric noise with off-diagonal variance 1/n and diagonal variance 2/n. Its Theorem 2 and Definition 2.2 specialize correctly to the null model: take beta = 0 and, for the irrelevant spike direction, v_0 = 1/sqrt(n), whose scaled empirical distribution is the constant V = 1 with convergent second moment. Then T_V(0) = 0, G_V(0) = E[g g_+]/sqrt(E[g_+^2]) = 1/sqrt(2), and R_V^sym(0) = sqrt(2). The theorem yields p(G) -> sqrt(2) almost surely under its stated independent sequence convention. In particular convergence in probability follows and transfers to W by the diagonal estimate.

This audit checked the theorem statement, normalization, definitions, and this specialization. It did not independently audit the approximate-message-passing lower-bound proof. Therefore the known full true-optimum limit remains an explicitly attributed literature input. The audited candidate's self-contained comparison upper bound is sufficient for its resolution even without that input.

## Scope and limitations

The audit independently inspected the entire candidate, the original problem, the relevant published theorem and its complete proof, the named classical input statements and their hypotheses, and the Montanari–Richard null-model specialization. Fresh downloads of all six primary source files matched the screening captures byte for byte. Important formula pages were visually checked, including both original-problem pages and the publisher's variance definition and theorem/proof pages.

The proof is complete relative to the explicitly invoked standard Gaussian concentration, Sudakov–Fernique, and global semicircle theorems. This is not a formal proof-assistant verification or an independent reproof of those classical theorems. Basic facts about the invariant measure on the sphere and Grassmannian, Gaussian moment-generating functions, compactness, and the spectral theorem are also used. The elementary application steps and tail, rank, transfer, and expectation arguments were independently checked above.

The verdict does not cover the paper's low-degree hardness argument, finite-dimensional experiments, quantitative convergence-rate discussion, planted recovery thresholds, or arbitrary non-Gaussian Wigner universality. It gives no explicit finite-n cutoff. No author-provided code or existing verification program was executed; only auditor-written retrieval/integrity operations and standard PDF extraction/rendering tools were used. Hash validation establishes file identity, not mathematical truth. No queue, repository, branch, or pull request was changed by this audit.

**Final status: accepted as an existing published negative resolution, faithfully reconstructed for the exact original Gaussian model.**
