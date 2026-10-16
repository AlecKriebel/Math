# Independent analytic verdict, frozen before prior assessments

Frozen: 2026-10-15 13:58 UTC. Candidate C4 revised SHA256 8da7cf366948e8d4fc63e3399cc4fe804ed786ea99b01479619efbdbacfedf3a. This memo was written after primary-body and C4/C1 inspection, but before reading the author clarification or Audits A/B/C1. It is not subsequently revised to agree with those assessments.

**PASS for the stochastic BK/Poisson/asymptotic mechanism, conditional on the finite primal/dual identity and primary-model flow-limit input.** No central stochastic gap remains in the revised candidate as inspected. This is an initial mechanism review, not whole-package acceptance or a novelty claim. The strongest verified implication is the canonical limit (T) from those identified inputs, using the independently checked chain theorem and product BK. No new central proof-search turn was used.

## Inputs and normalization

The external flow existence/L1 statement is an input from the primary problem, not proved anew. C1 gives V_n=c_L+c_B+2N-D_N with N=n-2. Hence E D_N/(2N) -> 1-v(1-q), after the bounded boundary correction and N/n -> 1. The exact planar separation identity itself remains a finite geometry dependency of this audit. Its algebra and source normalization were checked without reading the other independent family's findings.

Actual DZ PDF pages 1-2 define strictly increasing geometric chains, without requiring increasing sample indices; state L_n/sqrt(n) -> 2 in probability for uniform samples; and specialize the variational constant to one. Page 9, Theorem 2, gives (1/sqrt(n)) log P(L_n >= (2+c)sqrt(n)) -> -U_0(c), with U_0(c)>0 for c>0. Actual BK-author PDF pages 2-3 define disjoint certificate coordinates in {0,1}^n and give the product-distribution inequality in Theorem 1.1. The fixed-size Theorem 1.2 is unnecessary. Body hashes match the root retrieval receipt. These are theorem inputs; Bernoulli independence and boundary conventions are model assumptions.

## Count controlling both k and b

For each simple nonnegative-reward path, b<=k. Each coordinate of the ordered marked-edge starts, with endpoints appended, has negative variation at most b. C1's count applies to this class without a positive lower bound on k-b. A valid distinct-edge list has probability q^k. Invalid or repeated-edge lists may enlarge the numerical count but must not be assigned that probability. The revised argument respects this distinction.

The low-range base is 2 e^2 (3/2)^6 / 32^2 = 0.1643866545... < 1/4. The high-range base is at most 32 e^2 10^-6 6^2 = 0.0085121926... < 1/4. Summing 4*4^-k yields (16/3)*4^-r <=6*4^-r. A cycle has equally many forward and backward steps, so reward <=0. An optimal path may therefore be simple, and some monotone path has reward >=0. The exceptional-path event is controlled by K_N^+, rather than inferred incorrectly from D alone.

For theta<log 4, splitting D's exponential tail at ceil(32 sqrt(q)N) gives (27), with a constant depending only on theta. The displayed constant is conservative. Embed a W by H rectangle in a square of side max(W,H) and pad monotonically to its opposite corner; D_rect<=D_square under the coupling. This proves the weaker (28), including integer-translated rectangles outside Q_N.

## Sparse law, orientation, ties, topology and moments

There are E_q=2W_q H_q+W_q+H_q independent possible forward marks. At scale sqrt(q), the two orientations contribute rate two; boundary expectation q(W_q+H_q) vanishes. Expanding the Bernoulli Laplace functional gives the rate-two Poisson functional; the error is O(E_q q^2)=O(q). Multiplicities are retained before taking the limit.

For fixed M, the expected number of marked pairs whose starting x coordinates differ by at most M is bounded by a constant times q^2(W_q+1)(H_q+1)(2M+1)(H_q+1), with analogous orientation/boundary terms. This is O_M(sqrt(q)); the y bound is identical. It includes coincident horizontal/vertical starts. Z_q has bounded exponential moments, so P(Z_q>M) becomes uniformly small as M grows.

On Z_q<=M and coordinate separation greater than M in both coordinates, every nonnegative simple path has b<=k<=M. A decrease between ordered marked starts would require more than M negative steps. All collected starts therefore form a strict chain. Conversely such a chain can be visited including each marked edge: gaps greater than M>=1 accommodate each one-step orientation. Thus D equals strict-chain length on that event. For a finite configuration with no boundary points or coordinate ties, point count and strict coordinate order are locally constant under point-measure perturbation. Those conditions hold almost surely for the limit. This proves the distributional limit, rather than merely asserting that weak convergence preserves chain length.

Since 0<=D<=Z_q and E exp(a Z_q)<=exp(E_q q(exp(a)-1)), choosing a>theta gives uniform integrability of exp(theta D). Thus (29) follows, including moments. Separate positive x/y rescaling transforms the rate-two rectangle to a rate-one square of side sqrt(2wh), preserving order. Ties matter at finite q and are removed by a vanishing-probability argument, not ignored.

## Random counts, tails, and exponential moments

Couple all uniform samples with an infinite iid sequence independent of Z_s~Poisson(s^2). For n_+=ceil((1+delta)s^2), on Z_s<=n_+ the Poisson chain is bounded by L_{n_+}. Choose delta so (2+a/2)sqrt(1+delta)<2+a. A Poisson Chernoff bound is exp(-c_delta s^2), and DZ Theorem 2 gives P(Lambda_s >=(2+a)s)<=exp(-c_a s) after modifying constants. For convergence in probability also use n_-=floor((1-delta)s^2); on n_-<=Z_s<=n_+, sandwich between L_{n_-} and L_{n_+}. Let delta shrink after taking s large. This validates random-count Poissonization in both directions.

Factorial-moment counting gives expected increasing unordered k-tuples s^(2k)/(k!)^2 and hence (31). For k>=Ms, M>e, this is at most (e/M)^(2k). It proves uniform integrability of Lambda_s/s for s>=1: the far scaled first moment is bounded by C A rho^(A s), vanishing uniformly as A increases. The mean constant is consequently 2.

An explicit conversion to (30): fix eta>0, a=eta/4, M>10e, and a tail rate c_a>0. Choose 0<theta<min(log 4,1,c_a/(2M)). Split the exponential moment at t=(2+a)s and u=Ms. The lower part is <=exp(theta t). The middle part is <=C(s+1)exp(theta u-c_a s)<=C(s+1)exp(-c_a s/2), allowing harmless integer constants. Above u, exp(theta k)P(Lambda_s>=k)<=rho^k with rho=exp(theta)(e/M)^2<1, so its sum decreases exponentially in s. Absorb both errors in the gap between 2+a and 2+eta for large s. A single fixed-threshold tail would not suffice without the factorial far-tail control.

Choose eta small relative to epsilon, and use 2sqrt(wh)<=w+h for (32). The m+5 positive good shapes have minimum squared Poisson side 2(R/m)^2(m+5), which grows with R at fixed m. Thus one large fixed R covers every shape, then one small q gives (36) for all of them. The factor two absorbs convergence to finite positive moments. This q threshold is independent of N.

## Slicing, rounding, exceptional rectangles and entropy

First-hit levels are L,2L,... strictly below 2N, then 2N. Their number is J=ceil(2N/L). With j=0,...,J-1, all nonlast increments equal L and the last satisfies 0<tau<=L, including equality when L divides 2N. This resolves the candidate's harmless abbreviated indexing prose.

Let z=i_{j+1}-i_j. Subtracting rectangle endpoints gives W=(z+1)h+2a and H=tau+(1-z)h+2a. Hence W+H=tau+2h+4a exactly. A coordinate stays above its initial coordinate minus b and below its final coordinate plus b. The proposed rectangle contains these intervals. The endpoint displacements are >=-b; quantization remainders lie in [1,2h-1], so W,H>=2a-b+1>h, including the last short segment. Also -s-2<=z<=m+s+2. For s=0,tau=L, these yield precisely the asserted finite shape list, allowing unused shapes.

For nonlast bad segments, b>=h and a<=b+h<=2b. Their tau, 2h and 4a contributions total at most (m+2+8)sum b. The last segment costs <=L+6h+4b_last whether s=0 or positive. Combining them proves (41) with (m+10)B_N and no double charge. There are at most K+1 bad segments.

For fixed s-vector, possible endpoint records are at most product (m+5)(s_j+1)<=(m+5)^J exp(K). Nonnegative s-vectors with sum<=K number binom(J+K,K). At fixed q, h,L are fixed positive integers, so K/J ->16m sqrt(q). The entropy inequality log binom(J+K,K)<=J F(K/J) holds also at K=0. No microscopic endpoint factor log(1/q) is missing.

## Exact BK certificates despite overlapping rectangles

For a segment with positive reward r, fix only its originally marked forward edges to stay marked. Every original unmarked forward edge contributes at least zero in every completion; backward edges always cost one. Monotone padding in its rectangle adds nonnegative reward. Thus the padded walk has reward >=r in every completion. Removing cycles does not reduce reward. This is a certificate for {D_rect>=r} in the precise product-space definition. For r=0, D_rect>=0 is certain and the empty certificate works. Simple global paths never reuse an edge, so original segment certificates are pairwise disjoint; padding and rectangles need not be disjoint.

Choose one deterministic finite box covering all allowed skeleton rectangles before extending marks independently. An original skeleton realization forces disjoint occurrence in every extension, using only original marks. Thus the extended product measure bounds the original event; no conditioning on random rectangles or independence of overlapping fields is asserted.

Mutually disjoint certificates imply a left-iterated disjoint-occurrence event: the union of the first J-1 certificates certifies their iterated event and remains disjoint from the last certificate. These events are increasing. Iterated product BK yields the marginal product. Union over nonnegative integer reward vectors and the geometric tail identity give (44)-(45), including zero and negative segment rewards. There is no missing witness-list enumeration.

## Full error exponent, parameter order and lower constant

At fixed q,m,R: J/(2sqrt(q)N)->1/(sqrt(q)L), K/J->kappa=16m sqrt(q), and B_N/N->32sqrt(q). Target and baseline give -theta sqrt(2)Delta. The bad-size term is 512theta(m+10)sqrt(q). The remaining entropy equals [log(2(m+5)S_theta)+kappa(1+log C_theta)+F(kappa)]/(sqrt(q)L). This reproduces (47), with no missing order-one term.

Choose epsilon,m so Delta>0; then theta; then a sufficiently large fixed R for all shapes and the main entropy. Finally choose q small for (29), sqrt(q)L->R, kappa->0, F(kappa)->0 and the bad-size term. Every sufficiently small fixed q has a negative exponent; only then let N increase. R is independent of N. The complement of the backward-step event decreases by (25). Boundedness D_N/(2N)<=1 and (22) convert the tail to the claimed mean-density upper bound.

For the lower bound concatenate optimal paths in diagonal ell-squares. Adjacent squares share only one vertex, so rewards add on an admissible path. Expectations and the N-density limit at fixed q prove (51). For each fixed R>0, ell=floor(R/sqrt(q)) and exponential/first-moment convergence give the displayed liminf. Only after taking q small is R increased. The verified Poisson mean constant 2 then yields lower constant one. Both bounds prove (T), conditional on the stated finite identity and flow limit.

## Executed finite controls before this freeze

Assertions were active (`python3 -I -S -B`, no optimization). Independent controls exhaust 198 simple paths on Q_1,Q_2,Q_3 and 2,376 parameterized path cases, giving 4,854 segment rectangles: 114 negative endpoint displacements and 1,022 short final segments. All 4,096 configurations on Q_2 and 12 paths at four parameter choices give 442,368 segment certificates (264,960 positive; 18,816 negative segment rewards) and 47,744 nonnegative-path variation controls. Also checked: 581 separated mark sets in a 6 by 6 rectangle; all 8,000 ordered triples of increasing events on three coordinates at three rational q values, totaling 24,000 exact inequalities; and 30 coordinate-count parameter pairs. All passed. A row-tie example has reward 2 and strict-chain length 1, showing why separation is necessary. These are finite falsification controls, not an asymptotic theorem proved by computation.

The disk filled during the first memo-save attempt at approximately 13:58 UTC. No prior assessment was read in between. Only my already-inspected private rendered images and extracted BK text were removed; source PDFs remained untouched. This successful save is the analytic freeze.
