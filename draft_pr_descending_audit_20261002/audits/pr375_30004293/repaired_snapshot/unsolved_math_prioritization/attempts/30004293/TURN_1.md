# Turn 1: almost-sure amplification and deterministic exponent bounds

## Scope and outcome

The author target is the explicitly labeled finite-prefix interpretation

    M(D)=max_x #{B subset A intersect [1,D]: sum B=x},

for independent P(i in A)=1/i. The original OWR wording omits a cutoff in its model display; SOURCE_SCOPE.md and LITERAL_COROLLARY.md keep that literal issue separate. This turn does not determine the sharp growth of M(D).

It proves three useful facts:

1. The credited annular threshold bounds amplify to an **almost-sure** lower bound on the prefix exponent, not just convergence in probability.
2. The liminf and limsup of log M(D)/log log D are deterministic extended constants, by finite-modification invariance and the zero-one law. No equality of the two is proved.
3. Element-prefix and sum-prefix cutoffs have the same leading log-log exponent behavior, with precise deterministic comparisons.

The main lower bound is

    liminf_{D->infinity} log M(D)/log log D >= zeta_* >= eta
    almost surely,                                         (1)

where eta≈0.3533227727 is the credited Ford–Green–Koukoulopoulos constant and

    zeta_*=sup_{k>=2} log k / log(1/beta_k).

The beta_k are the source annular thresholds. We also show that zeta_* equals their limsup version used in the primary paper. The exact value of this exponent and any matching upper prefix bound remain unproved here. No recent Mao–Song preprint claim is needed as an input.

## 1. Definitions and a crude endpoint guard

For a finite set B of positive integers put r_B(x)=#{C subset B:sum C=x} and m(B)=max_x r_B(x). Representations are subsets, not ordered sums. Let beta_k be the supremum of c<1 such that

    P(m(A intersect (D^c,D])>=k)->1 as D->infinity.            (2)

For positive c the half-open interval has the same threshold as the source's closed one: the possible differing endpoint is selected with probability at most D^{-c}, tending to zero. This convention makes adjacent annuli disjoint.

The property in (2) is downward closed in c. Thus every 0<c<beta_k satisfies (2), without requiring the supremum to be attained. The published positive lower bounds imply beta_k>0 for every fixed k; this is a credited input, not reproved by a finite computation.

For clarity, beta_k<1 can also be guarded without any sharp published upper bound. We prove the crude estimate beta_k<=2/3 for all k>=2. Fix 0<c<1, write L=D^c, and I=(L,D] intersect N. If A intersect I has two distinct equal subset sums, cancel their common elements and choose the largest element m in their symmetric difference. Reversing the signs if necessary expresses

    m=sum_{b in B} epsilon_b b,   epsilon_b in {-1,1},

with B subset I, m not in B, and m>max B. For every B and sign choice, at most one m is determined. Dropping all restrictions other than m>=L gives the union bound

    P(m(A intersect I)>=2)
       <= L^{-1} sum_{B subset I} 2^{|B|} product_{b in B} b^{-1}
       = L^{-1} product_{i in I}(1+2/i)
       <= C D^{2-3c}.                                      (3)

Independence is used only for distinct B union {m}; terms not meeting that condition are discarded before the upper bound. The last estimate follows from log(1+2/i)<=2/i and the harmonic-sum bound log(D/L)+O(1/L). If c>2/3 the right side tends to zero, proving beta_2<=2/3. The event for k>=2 implies the two-sum event, so beta_k<=beta_2. This is merely a coarse guard, not a claimed best threshold.

## 2. A deterministic tensor observation

If B_1,...,B_n are pairwise disjoint finite sets of positive integers, and in B_j there are k_j distinct subsets with one common sum s_j, then their unions give product_j k_j distinct subsets of the union with common sum sum_j s_j. Distinctness follows by intersecting a union with each disjoint B_j. Therefore

    m(union_j B_j)>=product_j m(B_j).                       (4)

This is a lower bound only. Equality or a reverse multiplicative inequality is not claimed, because collisions can combine different component sums. The tensor device is classical and explicitly used in FGK Lemma2.1; the almost-sure deployment below is spelled out separately.

## 3. Fixed disjoint annuli give the almost-sure lower bound

Fix k>=2 and 0<c<beta_k. Define real endpoints

    D_j=exp(c^{-j}),   j=0,1,2,...,

so D_j^c=D_{j-1}. Let X_j be the indicator of the event that A intersect (D_{j-1},D_j] has at least k equal subset sums. The X_j are independent, because the integer annuli are disjoint. By (2), P(X_j=1)->1.

Here is an elementary strong-law argument that requires no rate of this convergence. Put S_n=sum_{j=1}^n X_j. Independence gives Var S_n<=n/4, while E S_n/n->1 by Cesaro averaging. For every epsilon>0, Chebyshev gives

    P(|S_{m^2}-E S_{m^2}|>epsilon m^2)<=1/(4 epsilon^2 m^2).

These probabilities are summable. Borel–Cantelli, first for rational epsilon>0, yields S_{m^2}/m^2->1 almost surely. Since S_n is nondecreasing and m^2<=n<(m+1)^2, squeezing between the two neighboring squares gives S_n/n->1 almost surely.

On every successful annulus choose k equal-sum subsets. Applying (4) to all successful annuli up to n gives

    M(D_n)>=k^{S_n}.

If D_n<=D<D_{n+1}, monotonicity of M and log log D<=(n+1)log(1/c) imply

    log M(D)/log log D
       >= (S_n/(n+1)) log k/log(1/c).

Thus, almost surely,

    liminf_{D->infinity} log M(D)/log log D
       >= log k/log(1/c).                                  (5)

Take a countable intersection over k and rational c with 0<c<beta_k, and let c increase to beta_k. This proves the first inequality of (1), even if zeta_* is interpreted as an extended real number. The published FGK lower bound supplies zeta_*>=eta. This argument does not convert arbitrary convergence-in-probability statements into almost-sure ones: it uses an explicit independent disjoint-block construction and monotonicity.

## 4. Supremum versus the source limsup exponent

For every integer r>=1,

    beta_{k^r} >= beta_k^r.                                (6)

Indeed, fix c<beta_k positive and split (D^{c^r},D] into the r disjoint annuli (D^{c^j},D^{c^{j-1}}], j=1,...,r. Each has k equal sums with probability tending to one as D tends to infinity. A finite union bound and (4) give k^r equal sums in their union with probability tending to one. Hence beta_{k^r}>=c^r; let c increase to beta_k.

It follows from (6) that along the sequence k^r,

    log(k^r)/log(1/beta_{k^r}) >= log k/log(1/beta_k).

Therefore the limsup over all integers k tending to infinity is at least every fixed-k ratio. The reverse inequality with their supremum is tautological. Consequently

    zeta_*=limsup_{k->infinity} log k/log(1/beta_k)=zeta_+.

This uses a fixed-r amplification before taking the parameter D to infinity; no unproved estimate uniform in growing k or r is inserted. It identifies the two variational expressions, not their numerical value or a matching prefix upper bound.

## 5. Tail determinism and what it does not imply

Adding one positive integer a to a finite set B gives

    r_{B union {a}}(x)=r_B(x)+r_B(x-a)

when a is absent from B. Thus

    m(B)<=m(B union {a})<=2m(B).                            (7)

If two infinite sets A,A' differ in at most q entries, (7) gives, for every D,

    |log M_A(D)-log M_{A'}(D)|<=q log 2.                    (8)

The normalized liminf and limsup are consequently unchanged by every finite modification. They are measurable functions of the independent Bernoulli sequence and belong to its tail sigma field: for each fixed N, replace the first N indicators by zeros in their definition and use (8). Kolmogorov's zero-one law then makes both extended random variables deterministic, say theta_- and theta_+. In particular theta_->=zeta_+ almost surely, and theta_+>=theta_-.

This is not a proof that theta_-=theta_+, that either is finite, or that the normalized sequence converges in probability. Almost-sure upper/lower limits and a possible convergence-in-probability limit must not be conflated. If a finite convergence-in-probability limit is established by some future argument, the same finite-modification observation forces that random limit to be a deterministic constant; it does not establish its existence here.

## 6. Element cutoff versus sum cutoff

Let

    L(X)=max_{0<=x<=X} r_A(x).

All subsets representing x<=X use only elements <=X, so L(X)<=M(X). Conversely, all subsets of [1,D] have sum at most D(D+1)/2, giving M(D)<=L(D(D+1)/2). In particular, for sufficiently large integer X,

    M(floor(sqrt X))<=L(X)<=M(X),
    L(D)<=M(D)<=L(D^2).                                    (9)

The first lower bound uses floor(sqrt X)(floor(sqrt X)+1)/2<=X. Since log log(X^a)/log log X->1 for each fixed a>0, monotonicity and (9) show that M and L have the same normalized liminf and limsup, and that convergence of either normalized sequence in probability to a finite constant implies convergence of the other to the same constant. These assertions concern the leading log-log scale only. The exact maxima, lower-order terms and their distributions are not equated.

## Remaining quantitative gap

The turn upgrades the credited prefix lower-growth mechanism to an almost-sure statement and fixes the deterministic tail/normalization structure. It gives no upper bound of the form M(D)<=(log D)^{eta+o(1)}, no numerical evaluation of zeta_+, and no proof of a limiting exponent. Those are the remaining objectives. The literal unbounded-supremum correction was source bookkeeping, not the substantive result counted here.

The exact checker validates finite subset identities, modification bounds, product constructions and the collision union bound on small windows. The infinite probabilistic argument is the proof above; finite checks are supplementary.
