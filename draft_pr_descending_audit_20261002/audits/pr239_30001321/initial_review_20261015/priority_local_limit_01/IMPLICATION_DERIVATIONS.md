# Exact implications and missing quantitative steps

This file contains original deductions for the audit, not claims that these deductions are stated in the cited papers.

## 1. The parity issue is exactly removable

At time t the target walk X_t is supported on x≡t (mod 2). Set

    Y_t=(X_t+t)/2,   p̃_(t,y)=p_(t,2y−t).

Then Y moves by 1 with probability p̃_(t,y) and by 0 otherwise. The map (t,y)↦(t,2y−t) is injective, so all the p̃ coordinates are iid with the identical original scalar law. In particular q=E p is in (0,1); the annealed increment law is (1−q)δ_0+qδ_1 and has span one. The bounded-step and nondegeneracy hypotheses in the RAP and JRS papers hold. This removes a superficial periodicity objection to using their results, without adding ellipticity. Extending p̃ to all integer times by independent copies also does not change any target finite-time distribution.

At terminal time N an original real interval [a+jM,a+(j+1)M) corresponds exactly to the Y interval [(a+N+jM)/2,(a+N+(j+1)M)/2), intersected with Z. Thus equal real lengths M become equal real lengths M/2. If original cells are M consecutive integers and M is odd, the Y cell counts alternate between floor(M/2) and ceil(M/2). This bounded discrepancy matters if a source insists on an exactly integer cell length; it is harmless for the variance/truncation argument below because its only geometric input is a lower bound proportional to M on nonempty cell lengths. One must not silently identify odd-M partitions with equal-integer partitions.

## 2. What the JRS density covariance implies

For the transformed model let a=q(1−q), δ=E[p(1−p)] and σ²=Var(p)=a−δ. In JRS notation,

    φ_ω(θ)=1−p+p e^(iθ),
    λ(θ)=E|φ_ω(θ)|²=1−2δ(1−cosθ),
    λ̄(θ)=|E φ_ω(θ)|²=1−2a(1−cosθ).

Their β integral is consequently β=δ/a, including the continuous extension at θ=0. Their density f has

    Ef=1,  Var f=β^(-1)−1=σ²/δ,
    Cov(f(T_(x,0)ω),f(T_(y,0)ω))=0  for x≠y.

Write c=σ²/δ. At every fixed time N the stationary field F_(N,y)=f(T_(y,N)ω) has those same moments. Its coordinates are *uncorrelated*; the results do not assert that they are independent.

Let b_N(y)=P(Binomial(N,q)=y). Define the weighted random measure

    ν_N(y)=b_N(y) F_(N,y).

This measure is nonnegative but need not have total mass exactly 1. For every cell J,

    E|ν_N(J)−b_N(J)| ≤ sqrt(c Σ_(y∈J) b_N(y)²).

Fix R≥1. Cells meeting [qN−R√N,qN+R√N] number at most 4R√N/M+3, uniformly in alignment after the parity shear. Since max b_N≤C/√N and Σ b_N²≤C/√N, Cauchy–Schwarz gives

    E Σ_(central J)|ν_N(J)−b_N(J)|
      ≤ C sqrt(R/M+N^(−1/2)).

For the other cells, all their sites lie outside the window and

    E|ν_N(J)−b_N(J)|≤Eν_N(J)+b_N(J)=2b_N(J).

The annealed variance bound gives their sum at most C/R². Therefore

    E ||ν_N(coarse)−b_N(coarse)||_1
      ≤ C sqrt(R/M+N^(−1/2)) + C/R².                    (J)

If c=0 the left side is zero. For every diverging M_N, first fix R and send N→∞, then send R→∞: the left side tends to zero, uniformly over deterministic alignments. Markov only gives the same vanishing bound divided by ε, which need not beat any power of N when M_N diverges slowly.

Crucial exact gap: ν_N is a stationary-density ansatz. JRS Proposition 3.1 and Theorems 1.1/1.2 do not identify the single-origin law μ_N with ν_N or state a quantitative local limit for μ_N−ν_N. Formula (J) alone is not even an all-scale expectation theorem for μ_N. A separate weighted local limit with an appropriate globally summed error would establish that expectation conclusion; the superpolynomial probability conclusion would still need more information.

## 3. Why pointwise L2 local-limit errors are insufficient by direct summation

Suppose, hypothetically in the discrete target model, a weighted approximation r_N(y)=μ_N(y)−b_N(y)F_(N,y) were available with

    sup_y E|r_N(y)|² ≤ C N^(−1−η),   η>0.

The central window has O(R√N) sites. Thus

    E Σ_(central sites)|r_N(y)| ≤ C R N^(−η/2).

Combined with positivity, Ef=1 and annealed tails, this yields a coarse-L1 expectation bound C R N^(−η/2)+C/R² plus (J). It gives no all-K tail estimate. Markov applied to the central residual gives a fixed polynomial exponent η/2. To control the whole residual one must also choose R: with only the displayed C/R² tail bound, taking R=N^(η/6) gives O(N^(−η/3)); the exact binomial exponential tail permits R proportional to √log N and retains N^(−η/2) up to logarithms. None of these direct deductions gives arbitrary polynomial powers. The stationary average term may vanish only with M_N. The source assumptions might of course imply stronger statements by an additional proof, but they cannot be promoted by this direct implication.

The continuum Dunlap–Gu d=1 bound has η=1/3 and an extra log N before taking a square root. Even after supposing it were a discrete theorem and after giving it the strongest natural central-window interpretation, direct integration produces only C R N^(−1/6)√log N. This deliberately favorable hypothetical comparison does not yield N^(−K) for every K.

The continuum covariance bound |Cov(U(x),U(y))|≤C/(1+|x−y|) likewise implies a variance O(M log(2+M)) for its unweighted integral over an M interval. That supports spatial averaging as M→∞, with a logarithm, but supplies no all-order environmental concentration.

## 4. Almost sure convergence is not a rate

An abstract sequence Z_N=1_(A_N), with P(A_N)=N^(−2), converges to 0 almost surely by the first Borel–Cantelli lemma, because ΣN^(−2)<∞. Yet P(Z_N>1/2)=N^(−2), which is not O(N^(−3)). This does not model an iid RWRE and is not a counterexample to PR239. It proves the logical nonimplication from a qualitative almost-sure conclusion to the requested superpolynomial environmental tail.

The adversary's stronger binomial modulation example additionally preserves a binomial annealed marginal and the favorable L2 exponent. It has the same limited purpose: it tests a proposed theorem-to-theorem inference, not the iid walk itself.

## 5. Mean fluctuations and single-site correctors do not disprove coarse smoothing

The credited N^(1/4) quenched-mean fluctuations are smaller than the width √N of the endpoint law. For a smooth Gaussian density g_N with variance proportional to N,

    ||g_N(·−h)−g_N||_1 ≤ |h| ||g_N'||_1 = C |h|/√N.

A shift h of order N^(1/4) therefore has total variation of order N^(−1/4), which vanishes even before coarse graining. This example explains why the quenched-mean fluctuation scale does not itself generate a fixed-ε tail lower bound.

Likewise, a persistent order-one local density factor F_(N,y) is compatible with coarse convergence through (J). The word 'local' in a weighted local-limit theorem describes fluctuations that the target intentionally averages. It does not settle their simultaneous concentration over the many terminal cells.

## 6. Exact missing bridge for a full older-result implication

A verified earlier implication needs an estimate on the *whole* coarse discrepancy at a fixed ε, with an environmental failure probability smaller than every N power and with no lower rate on M_N. Sufficient routes could include:

1. a directly stated full coarse-L1 concentration theorem for merely elliptic iid scalar laws;
2. weighted-LLT residuals with arbitrary high moment decay plus quantitative concentration of all weighted stationary blocks at any diverging scale;
3. an already published final-segment concentration/decoupling theorem that converts a small conditional mean at arbitrary target scales to the required tail while keeping a polynomial number of independent input blocks.

Merely asserting that the invariant density is mixing, that equilibrium is unique, or that its covariance vanishes at distinct sites supplies none of these. A route relying on such an unstated bridge is marked blocked at that bridge; it is not reopened by renaming it a local-limit argument.


## 7. Finite-valued approximation needs uniform control

Suppose p and p' are placed on a common environment probability space with |p_(t,x)−p'_(t,x)|≤h at every site. Maximal transition coupling while the walks coincide shows that their paths disagree by time N with conditional probability at most Nh. Therefore their endpoint L1 distance, and any coarse endpoint L1 distance, is at most 2Nh. The same deterministic estimate applies to their annealed endpoint laws. The two coarse discrepancies consequently differ by at most 4Nh.

A finite-valued quantization with fixed h therefore does not transfer an asymptotic theorem to the original arbitrary law for all large N. Choosing h_N=o(1/N) changes the approximating law with N. A theorem with constants and a large-N threshold depending on each fixed law cannot be substituted along that triangular array without additional uniformity. No such transfer is asserted here. This is a general quantifier check, not a claim about an unread original paper's full hypotheses.

## 8. Balanced or symmetric models do not contain the generic target

For a one-dimensional nearest-neighbor continuous-time generator obtained by multiplying the target transition probabilities by any positive site clock c_(t,x), the local drift is c_(t,x)(2p_(t,x)−1). It is balanced only if p_(t,x)=1/2. For constant clocks c, subtracting the annealed velocity gives 2c(p_(t,x)−q), still random for a nonconstant law. For arbitrary fixed deterministic clocks, subtracting one deterministic velocity v gives c_(t,x)(2p_(t,x)−1)−v, which likewise cannot vanish almost surely for a nonconstant iid scalar law. A deterministic change of moving frame does not establish pointwise balance.

Similarly, symmetric conductances would require a right-edge rate at x to equal the reverse-edge rate at x+1. Independent scalar p values impose no identity c_(t,x)p_(t,x)=c_(t,x+1)(1−p_(t,x+1)) with fixed deterministic clocks. One can sometimes construct random reversible weights in a static setting, but that is an additional transformation whose time dependence and invariant-density effect must be proved. A symmetric-conductance LLT cannot simply be relabeled as the target result.
