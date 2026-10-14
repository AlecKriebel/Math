# Independent acceptance of isolated-block tails and the fixed-fraction corollary

Shared PASS3, 14 October 2026.

## Verdict and pins

**Accepted:** the finite marked-block count, its uniform-in-location exponential consequence for every fixed K, and the stated fixed-fraction bound for the largest cell.

- `pass3_kernel_feasibility/ISOLATED_BLOCK_TAIL.md`: 5854 bytes, SHA-256 `f61fde65b505d884a7bf9f9432edf5d937f5009a8168246f67052484890d7fdd`.
- `pass3_kernel_feasibility/LARGEST_CELL_FRACTION_COROLLARY.md`: 855 bytes, SHA-256 `902f69a9507145701bc15686c15152c6cb4423e678cb99f5d2d25c51d1fa016a`.

No mathematical correction is needed. The finite path-cut argument is also independently accepted in `pass3_bijection_audit/ISOLATED_BLOCK_STRUCTURAL_ACCEPTANCE.md`, SHA-256 `937e56392b99c2f4a8d469d1ffb65ab0b81d0c930d2cc62728e84cc2a7cb3b16`, with receipt SHA-256 `8fec619a832024195d248e660e47bc6d7c5a7987d6c8c7a480d797ecea06b76b`.

## 1. The finite law keeps all completion factors

Cutting the exact normalized canonical path before and after a marked block leaves three valid path pieces. For exterior sizes p and q and marked mass m, their full states and internal shuffles are counted by a_p, a_q and b_(m,K), respectively. The homogeneous kernel makes even-starting fragments valid normalized paths too; no parity multiplicity is missing.

The location of the mark is encoded by the prefix path. Two different marked positions therefore cannot collapse into the same three-piece data. Empty exteriors are included with a_0=1 and no boundary edge. Neither exterior is replaced by an assumed uniform conditional residual.

If the two adjacent exterior cells have sizes l and r, their two missing edge shuffles have at most

    binom(m+l,l) binom(m+r,r)

possibilities. The first and last cell inside the block can each be enlarged to size m for this upper bound, including the one-cell case in which they coincide. Missing exteriors give l=0 or r=0 and the correct factor one.

For k=l+r, the negative-binomial convolution is

    sum_(j=0)^k binom(m+j,j)binom(m+k-j,k-j)
      = binom(2m+k+1,k).

The actual product is one term in that positive sum. The right side increases with k, so k<=floor(delta m) gives the claimed uniform edge bound. Discarding the boundary restriction only after applying this bound is valid. Summing all p+q=n-m gives n-m+1 terms, each with a_p a_q<=a_(n-m) by skew closure. This proves the displayed finite bound without an extra uncounted location or allocation factor.

## 2. Uniform large-mass probability estimate

For fixed K, the earlier fixed-prefix theorem gives the strict canonical-cell growth gap g_K<lambda. This is specifically the at-most-K canonical-cell class, not all permutations admitting an arbitrary K-cell gridding. Its one-cell case is Catalan-enumerated, so g_1=4 and the strict gap also gives lambda>4.

Use the actual full denominator a_n. The inequalities a_(n-m)<=lambda^(n-m) and log a_n=n log lambda+o(n) retain the necessary normalization. The limsup defining g_K gives, for every fixed positive error, an upper bound on b_(m,K) valid for all sufficiently large m. Therefore it is uniform on epsilon n<=m<=n. A convergent sequence or an asymptotic constant for b_(m,K) is not required.

For fixed delta>0, Stirling's bound, including the floor and the added one, gives

    log binom(2m+floor(delta m)+1,floor(delta m))
      = m Phi(delta)+O(log(m+1)).

For delta=0 the coefficient equals one and Phi(0)=0. Thus the stated estimate also holds at that endpoint. Both errors are uniform over the relevant mass interval. The exterior-size factor and summation over at most n values of m are polynomial and disappear at logarithmic rate.

Under Phi(delta)<log(lambda/g_K), the resulting rate is at most

    -epsilon[log(lambda/g_K)-Phi(delta)]<0.

This proves the existence-event estimate at every staircase location simultaneously. The argument does not hide an error depending on a growing cell index. It does, however, fix K before taking n to infinity; no uniform statement for K growing with n follows.

## 3. Fixed-fraction largest-cell corollary

Choose a fixed delta>0 with Phi(delta)<log(lambda/4), possible because lambda>4 and Phi(delta) tends to zero at zero. Set c=1/(1+delta)<1. If any cell has mass m>=cn, the sum of its two neighboring masses is at most all exterior mass n-m, which is at most delta m. Thus the isolated-single-cell event contains the largest-cell event at this threshold.

Applying the accepted K=1 estimate with epsilon=c gives exactly the displayed strictly negative rate. The endpoint inclusion m>=cn is correct; integer rounding can only strengthen the needed inequality.

The corollary proves existence of some fixed c<1 with an exponential upper tail beyond c n. It does not prove that every positive c works, that maxcell/n tends to zero, or that a permuton limit exists. It also does not make largest-cell sublinearity a necessary condition for anti-diagonal convergence.

## 4. Finite checks and remaining scope

The supplied isolated-block checker reports360 finite inequalities and159069 marked objects through size8, with block lengths1–3. Its normal, -O and -OO JSON reports are mathematically identical. I compared the reports; these supplied runs are not claimed as independent audit reruns. They are regression evidence, while the all-size proof is the path-cut and growth argument audited above.

The result excludes isolated fixed-width macroscopic blocks, including at escaping indices. It leaves profiles with significant neighboring mass, blocks with unbounded cell-count, and potentially collapsing growth gaps as K increases. It does not prove the target anti-diagonal limit for uniform1324 or the universal fixed-alpha diagonal theorem.
