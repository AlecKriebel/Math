# Tightness of the data-point k-median LP: scoped results and exact controls

**Record 2800903 / AMR-027-0903. Original joint random-model question unresolved.**

This note proves limited statements for the precise data-point LP: an explicit planar fractional gap; exact tightness on a line; a nonvanishing failure lower bound as dimension alone grows with six points; near-unit *value ratio* when Gaussian dimension dominates log sample size; and robust gap configurations for arbitrarily large finite sample sizes. None supplies the unresolved joint large-sample/high-dimensional failure probability. No novelty or peer-review claim is made.

## 1. Target and conventions

Let P=(p_0,...,p_{n-1}) be n labelled points in Euclidean space R^d, and let 1 <= k <= n. Clients and allowed centers are the same data points. Write d_ij=||p_i-p_j||_2, without squaring. The source's relaxation is

\[
 L(P,k)=\min_{x,y}\sum_{i,j}d_{ij}x_{ij},\qquad
 \sum_i x_{ij}=1,\quad 0\le x_{ij}\le y_i\le1,\quad\sum_i y_i=k.
 \tag{1}
\]

The integral optimum is

\[
 I(P,k)=\min_{S\subseteq[n],\ |S|=k}\sum_j\min_{i\in S}d_{ij}.
 \tag{2}
\]

Each selected center can be assigned to itself. Tightness means L=I, equivalently existence of an integral optimum, since (1) is compact. It does not mean that every optimum is integral or unique. A fractional optimum returned by a solver is insufficient to prove L<I. Our negative certificates explicitly place a feasible fractional value below every integral value.

Bandeira's [Problem 9.3](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-of-data-science-fall-2015/29dc319cb9f8992c5b4b46b917ecd86d_MIT18_S096F15_Open9.3.pdf), pp.1–2, asks for tightness under natural unplanted models, mentioning independent Gaussian points. It does not specify a growth regime. The earlier [Mixon/Ward Problem 6](https://dustingmixon.wordpress.com/2015/08/25/applied-harmonic-analysis-and-sparse-approximation/) is more precise about the law: A is uniform on the unit Frobenius sphere in R^{d x n}; it asks whether failure probability vanishes as d and n increase, without prescribing their relation or k's dependence on them.

If G has independent standard normal entries, G/||G||_F is uniform on this sphere, by rotation invariance of the Gaussian density. Distances, I, and L all scale by the same positive scalar. Thus the sphere and independent-standard-Gaussian-column models have identical tightness events. We denote their common failure probability by p_{d,n,k}. Fixed-n dimension limits, fixed-d sample limits, joint limits, and uniformity over k are different assertions. The title's k-median is the data-point/medoid problem, not a continuous-center geometric-median problem.

For comparison with sources omitting y_i<=1: column sums imply x_ij<=1. Replacing y by min(y,1) preserves x<=y, and unused opening mass can be redistributed up to 1 at other points to restore sum y=k because k<=n. This changes no objective. Hence dropping upper bounds gives the same optimal *value*. We do not transfer uniqueness claims without checking them separately.

## 2. Approach 1: an exact six-point Euclidean gap

Use k=2 and

\[
(p_0,p_1,p_2,p_3,p_4,p_5)=((9,9),(-3,0),(6,3),(7,-4),(2,10),(8,0)).
\]

The exact squared-distance matrix is

\[
M=\begin{pmatrix}
0&225&45&173&50&82\\
225&0&90&116&125&121\\
45&90&0&50&65&13\\
173&116&50&0&221&17\\
50&125&65&221&0&136\\
82&121&13&17&136&0
\end{pmatrix}.
\tag{3}
\]

Set y=(0,1/2,1/2,0,1/2,1/2). For clients j=0,...,5, assign weight 1/2 to each of the following two facilities:

\[
(2,4),\ (1,2),\ (2,5),\ (2,5),\ (2,4),\ (2,5).
\tag{4}
\]

The assignment columns sum to one and respect y; sum y=2. Its cost is

\[
F=\tfrac12(\sqrt{45}+2\sqrt{50}+\sqrt{90}+2\sqrt{13}+\sqrt{17}+\sqrt{65}).
\tag{5}
\]

The best integral centers are {1,2}, with cost

\[
I=\sqrt{45}+\sqrt{50}+\sqrt{65}+\sqrt{13}.
\tag{6}
\]

Here is a complete finite certificate for the minimum assertion, using lower bounds with denominator 10^6. The center pairs in lexicographic order and corresponding lower numerators are

| S | 10^6 times a rigorous lower bound for its cost |
|---|---:|
| 0,1 | 33604984 |
| 0,2 | 27234517 |
| 0,3 | 28672704 |
| 0,4 | 40096873 |
| 0,5 | 25799723 |
| 1,2 | 25447078 |
| 1,3 | 35527457 |
| 1,4 | 36903653 |
| 1,5 | 27964380 |
| 2,3 | 27862843 |
| 2,4 | 26871653 |
| 2,5 | 28380397 |
| 3,4 | 29035568 |
| 3,5 | 35093168 |
| 4,5 | 25799723 |

For each squared distance m, let a_m=floor(sqrt(10^12 m)), computed by integer square root. Then a_m/10^6 <= sqrt(m) <= (a_m+1)/10^6, with equality on both endpoints replaced by a_m/10^6 when exact. For each pair, selecting the smaller *squared* distance gives its nearest facility exactly. Summing the corresponding radical lower bounds gives the table. The upper bound for {1,2} is 25.447082, smaller than every other pair's lower bound. This proves (6). The verifier checks the integers by squaring, rather than trusting floating-point roots.

The exact certificate gives

\[
24.8668165\le F\le24.8668205,\quad
25.447078\le I\le25.447082,\quad
I-F\ge\frac{232103}{400000}>\frac{29}{50}.
\tag{7}
\]

Consequently L<=F<I. We **do not claim F=L**. The observed solver optimum is not used in any proof.

If each point is moved by at most epsilon, each pair distance changes by at most 2 epsilon. Every feasible assignment has total mass n, so its value changes by at most 2n epsilon; the integral minimum satisfies the same bound. Keeping (4) as a fixed fractional witness, its gap below I decreases by at most 4n epsilon. For epsilon=1/100 and n=6, (7) leaves a gap greater than 17/50. Thus an open neighborhood of this configuration is non-tight. Every independent point law assigning positive mass to each of these six neighborhoods, including a nondegenerate Gaussian in any d>=2 after embedding the points, has positive failure probability for n=6,k=2. This does not give a lower bound uniform in dimension or sample size.

## 3. Approach 2: exact rounding on a line

**Theorem.** If all facilities and clients lie on a line, (1) has an integral optimum for every n and k. In particular p_{1,n,k}=0.

This is a known special case; see Hajiaghayi–Hu–Li–Li–Saha, [Lemma 3.1](https://cse.buffalo.edu/~shil/papers/FTKM-SODA2014.pdf), which treats the more general fault-tolerant version. The following is a self-contained proof for (1).

Order the facilities along the line, breaking location ties by label. For a feasible y define s_0=0 and s_i=sum_{h<i}y_h, so facility i corresponds to the half-open interval [s_i,s_i+y_i) within [0,k). Choose U uniformly from [0,1), and open facility i precisely when this interval contains some U+t with integer t=0,...,k-1. Except on finitely many null phases, each interval contains at most one of these points because y_i<=1; each of the k phase points is in exactly one interval. Therefore exactly k distinct facilities are opened.

Any consecutive block of facilities corresponds to a single interval of length ell=sum_{i in block}y_i. The probability that it contains a phase point is min(1,ell): for ell<1 the interval's projection modulo one has Lebesgue measure ell, and for ell>=1 it contains a point of every translate of the integer lattice. Hence the probability that the block is missed is (1-ell)_+.

For a client j and radius r>=0, its ball of facilities B_j(r)={i:d_ij<=r} is a consecutive block. If R_j is the distance to the closest opened facility,

\[
\mathbb P(R_j>r)=(1-y(B_j(r)))_+.
\]

For any feasible assignment column x_{.j}, its mass outside B_j(r) is at least this quantity. Integrating the elementary identity a=integral_0^infinity 1_{a>r} dr gives

\[
\mathbb E R_j=\int_0^\infty(1-y(B_j(r)))_+dr
\le\sum_i d_{ij}x_{ij}.
\]

Summing over j, the expected rounded integral cost is at most the fractional value. Some phase therefore gives an integral cost no larger than that value. Apply this to an optimal fractional point; the reverse inequality L<=I is automatic. This establishes exact tightness, without implying integrality of the entire feasible polytope. The same proof allows arbitrary nonnegative client weights and separately located line facilities.

## 4. Approach 3: dimension alone does not eliminate failure

**Theorem.** For six independent standard Gaussian points in R^d and k=2,

\[
\liminf_{d\to\infty} p_{d,6,2}>0.
\tag{8}
\]

This is a fixed-six-point statement, not a joint n,d result.

Let D^{(d)}_{ij}=||g_i-g_j||, with each g_i standard Gaussian in R^d. For i<j set H^{(d)}_{ij}=D^{(d)}_{ij}-sqrt(2d), and complete it symmetrically with zero diagonal. The 15-dimensional vector H^{(d)} converges in distribution to

\[
 Z_{ij}=\frac{V_i+V_j-2W_{ij}}{2\sqrt2},
\tag{9}
\]

where V_0,...,V_5 are independent N(0,2), the W_{ij} are independent N(0,1), and the two families are independent.

For completeness, let g_{it} be the coordinates. The vectors consisting of (g_{it}^2-1)_i and (g_{it}g_{jt})_{i<j} are independent over t, centered, and have diagonal covariance: variance 2 in the first coordinates and 1 in the second. Mixed covariances vanish by odd Gaussian moments and independence. The finite-dimensional central limit theorem applied to their sums divided by sqrt(d) gives the V,W limit. Also

\[
\frac{(D^{(d)}_{ij})^2-2d}{\sqrt d}
=\frac{\sum_t(g_{it}^2-1)+\sum_t(g_{jt}^2-1)-2\sum_tg_{it}g_{jt}}{\sqrt d}.
\]

Dividing this expression by (D^{(d)}_{ij}+sqrt(2d))/sqrt(d), which converges in probability to 2sqrt(2), proves (9). The only probabilistic limit theorems used are the usual finite-dimensional central limit theorem, law of large numbers, and continuous mapping/Slutsky theorem. No growing-dimensional CLT is invoked. In particular Var Z_{ij}=1; shared-endpoint covariance is 1/4; disjoint-edge covariance is zero. The independent W terms imply positive-definite covariance and positive density everywhere in R^{15}.

Let x* be (4), and for any symmetric off-diagonal cost array H put

\[
\Psi(H)=\min_{|S|=2}\sum_{j\notin S}\min_{i\in S}H_{ij}
-\sum_{i\ne j}H_{ij}x^*_{ij}.
\]

Both terms have total off-diagonal mass 4, so Psi is 8-Lipschitz in the maximum norm. Let C be the Euclidean distance array of (3), and define H*_{ij}=C_{ij}/10-1 for i!=j. Adding a common constant to all off-diagonal entries changes both terms equally, while positive scaling scales their difference. Thus Psi(H*)=(I-F)/10>29/500.

The open box B={H:max_{i<j}|H_ij-H*_ij|<1/1000} satisfies Psi(H)>29/500-8/1000=1/20. Since Z has full support, q=P(Z in B)>0. For every realization of the Gaussian distances, both the integral optimum and the fixed witness have off-diagonal mass 4 after each selected center is assigned to itself; hence

\[
 I(D^{(d)},2)-F(D^{(d)})=\Psi(H^{(d)}).
\]

The right side being positive implies LP failure. Portmanteau's theorem for the open box now gives liminf p_{d,6,2}>=q>0. Positive rescaling transfers the conclusion to the Frobenius-sphere law. No numerical estimate of q, let alone a practically large failure probability, is asserted.

## 5. Approach 4: concentration controls the value ratio, not exact integrality

**Deterministic bound.** Suppose 0<a<=d_ij<=b whenever i!=j and k<n. For every fractional feasible point,

\[
\sum_{i,j}d_{ij}x_{ij}\ge a\sum_{i\ne j}x_{ij}
=a\bigl(n-\sum_jx_{jj}\bigr)\ge a(n-k).
\]

The last step uses x_jj<=y_j and sum y=k. Any k selected centers, self-assigned and with all other clients assigned arbitrarily among them, have cost at most b(n-k). Therefore

\[
1\le I/L\le b/a.
\tag{10}
\]

When k=n both optima are zero, so a ratio is unnecessary.

**Gaussian consequence.** For independent standard Gaussian points and 0<epsilon<1,

\[
\mathbb P\left(\text{for all }1\le k<n:\
1\le I(P,k)/L(P,k)\le\sqrt{\frac{1+\epsilon}{1-\epsilon}}\right)
\ge1-n(n-1)e^{-d\epsilon^2/8}.
\tag{11}
\]

A negative lower bound on the right is simply vacuous. To prove (11), for every pair D_ij^2/2 has a chi-square law with d degrees of freedom. If X has this law, its moment generating function is E exp(tX)=(1-2t)^{-d/2}, t<1/2, obtained by the one-dimensional Gaussian integral and independence. Chernoff optimization gives

\[
\mathbb P(X\ge d(1+\epsilon))\le
\exp[-d(\epsilon-\log(1+\epsilon))/2],
\]

\[
\mathbb P(X\le d(1-\epsilon))\le
\exp[-d(-\epsilon-\log(1-\epsilon))/2].
\]

For 0<epsilon<1, differentiating shows epsilon-log(1+epsilon)>=epsilon^2/4 and -epsilon-log(1-epsilon)>=epsilon^2/2. Thus the two-sided probability is at most 2 exp(-d epsilon^2/8). A union bound over n(n-1)/2 pairs, without requiring independent distances, puts all distances in [sqrt(2d(1-epsilon)),sqrt(2d(1+epsilon))]. Apply (10) simultaneously for every k.

In particular, if d tends to infinity and log(n+1)=o(d), set epsilon=(log(n+1)/d)^{1/4}. Then epsilon tends to zero and the exceptional probability in (11) tends to zero: its logarithm is at most 2log n - sqrt(d log(n+1))/8, which tends to minus infinity. Hence the maximal ratio over 1<=k<n converges to 1 in probability. This also holds for fixed n as d increases. It is fully compatible with (8): a positive chance of a strict but relatively tiny gap need not disappear. A proof that I/L approaches one cannot be promoted to a proof that I=L with high probability. No approximation-algorithm ratio is used.

## 6. Approach 5: sample replication and its asymptotic limitation

**Theorem.** For every integer r>=1 and every finite d>=2, p_{d,6r,2}>0. More generally the same holds for any independent identical point law with full support in R^d.

Start with r labelled copies of each of the six planar points in (3), embedded in R^d. Allowing coincident labels here is a temporary construction, not a claim that a Gaussian sample has coincidences. For two chosen facility labels, if their base locations differ, their cost is exactly r times the corresponding two-location cost. If their locations coincide, the cost is r times a one-location cost, which is at least rI because adding a second distinct center cannot increase cost. Thus the integral optimum of the duplicated configuration equals rI.

For a fractional witness use a single representative facility for each of base labels 1,2,4,5, each with opening 1/2. Each copy of client j uses the assignment in (4) to those representative facilities. All other facilities have opening zero. This is feasible and has cost rF, so the gap is greater than 29r/50.

Move each of the 6r points independently by less than 1/100. The objective perturbation argument from Approach 1 gives a decrease of at most 4(6r)/100 in the integral-minus-witness gap, leaving more than 17r/50. This holds uniformly across all choices of the perturbations, including ones making every point distinct. The event that the first r independent samples fall in the first point's neighborhood, the next r in the second, and so forth has probability

\[
\prod_{i=0}^5\mu(B(p_i,1/100))^r>0.
\tag{12}
\]

For a nondegenerate Gaussian the sample is distinct almost surely. Normalization again transfers the assertion to the uniform Frobenius sphere.

This route rules out almost-sure exactness at these finite sizes. It does not rule out failure probability tending to zero. Indeed the explicit event in (12) is exponentially small in r for the disjoint neighborhoods used here, and its mass also depends on d. Inferring a uniform lower bound or a joint asymptotic counterexample from (12) would be invalid. Replication creates a *rare event inside* the single Gaussian law; it does not replace that law by a planted mixture.

## 7. What remains and proof dependencies

The unresolved target is a quantitatively specified regime for p_{d,n,k} as both n and d grow, or as n grows in a fixed dimension >=2, including how k scales. We have no upper or lower failure-probability bound in those regimes that settles the source question. The statements proved here require neither a planted partition nor a separated-mixture assumption on the Gaussian law.

Approach 1 is an exact finite Euclidean certificate and a robustness proof. Approach 2 is a standard interval-coupling proof. Approach 3 uses a fixed-dimensional central limit theorem, LLN, Slutsky, and the open-set form of Portmanteau, with its covariance and witness comparison proved explicitly. Approach 4 uses only Gaussian integrals, Chernoff's inequality and a union bound. Approach 5 is a deterministic replication and positive-support argument. None depends on the disputed arbitrary-disjoint-ball theorem. Neither the k-means SDP nor a continuous-center problem is analyzed.

The standard-library script `verify.py` independently reconstructs squared distances, rational radical enclosures, all 15 center pairs, fractional feasibility, a covariance LDL decomposition, and exhaustive finite interval-rounding controls. Its output is `verification.json`. It is a certificate checker for the finite claims; the universal rounding and probability statements are established by the written arguments, not by simulations. No third-party source text, source PDFs, or external datasets are included in this packet.
