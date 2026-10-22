# Independent adversarial audit: nonnegative corner weights

Date: 2026-10-20 UTC.

## Verdict

**PASS for the precise statement with each fixed real a >= 0.** I found no mathematical gap in the Perron–Frobenius, confinement, endpoint-grouping, mirror, padding, injection, exponent, or ordinary-root-limit arguments. In particular, the endpoint a=0 is covered without a limiting argument and without introducing a forbidden corner.

The result establishes

    lim_{m -> infinity} Q_m(a)^(1/m) = (2 + sqrt(2+2a))^2

and the corresponding half-length radius, for the exact linear NW/ES statistic and the exact origin-returning nonnegative-quadrant model in the source gate. It is a partial resolution of the recovered full-range question, not a resolution for all a >= -1. No conclusion for -1 < a < 0, no coefficient asymptotic, and no novelty certification follows from this audit.

No correction is required for the theorem as written. Two optional exposition improvements are listed below.

## Audited inputs and source match

- `ATTEMPT_1.md`, SHA-256 `6781240b940f5851570a50f36974f71c7cfedddbe6d774125ef65ace92b04a17`.
- Source/status gate, SHA-256 `de6f8a2ec91be2a673292daacf75183e48b6853c6773ffde56e598137c93f5a1`.

I also checked the locally available Albert–Bousquet-Mélou v3 extraction at the model definition, Conjecture 11, and Proposition 17. The half-length variable, ordered NW/ES statistic, and formula agree. The attempt does not substitute arbitrary-endpoint paths for loops: arbitrary endpoints are an intermediate construction, subsequently closed by pairing paths with the same endpoint. Boundary visits, repeated vertices, and intermediate returns remain allowed.

Public reference: Michael Albert and Mireille Bousquet-Mélou, *Permutations sortable by two stacks in parallel and quarter plane walks*, European Journal of Combinatorics 43 (2015), 131–164, Conjecture 11 and Proposition 17. https://arxiv.org/abs/1312.4487 ; https://doi.org/10.1016/j.ejc.2014.08.024 . This audit is not a new literature-status search.

## 1. Transfer matrix and probability law

In state order E,N,W,S the matrix is exactly

    [1  1  1  a]
    [1  1  a  1]
    [1  1  1  1]
    [1  1  1  1].

With s=sqrt((1+a)/2), the identity 1+a=2s^2 gives the displayed right and left eigenvectors directly. Both have strictly positive entries even at a=0. At that endpoint, for every i,j at most two of the four intermediate states k are excluded from a positive product M_ik M_kj, so M^2_ij>0. This verifies primitivity rather than assuming positivity at a=0.

The eigenvalue lambda=2+2s is the Perron eigenvalue. The stated characteristic polynomial z^2(z^2-4z+2-2a) is also correct, although unnecessary.

The Doob transform is stochastic. Its stationary distribution is uniform because the coordinatewise product of the left and right eigenvectors is constant. Consequently each coordinate of the direction vector has zero stationary mean. No unsupported inference from the unweighted random walk enters here.

Telescoping transition probabilities gives the claimed path probability, with lambda raised to n-1 rather than n. The conversion to lambda^n merely absorbs the fixed factor 1/lambda. Explicit admissible constants are

    c_a = (4/lambda) min(r)/max(r),
    C_a = (4/lambda) max(r)/min(r).

These are finite and positive for every fixed a>=0. Zero-weight words have zero chain probability, so the comparison remains valid at a=0. No uniformity as a varies is required or claimed.

## 2. Poisson equation and whole-path confinement

For an irreducible finite stochastic matrix, the nullspace of I-P consists of constants, and its range is the stationary-mean-zero subspace. Thus the two coordinate equations have bounded solutions. The displayed martingale is correctly indexed: set F_k=sigma(D_1,...,D_{k+1}), with F_0=sigma(D_1). Then E[Z_k | F_{k-1}]=0.

The telescoping identity is exact:

    h(D_1)-h(D_{k+1}) + sum_{j=1}^k [h(D_{j+1})-Ph(D_j)]
      = sum_{j=1}^k [h(D_j)-Ph(D_j)] = S_k.

The endpoint correction has coordinatewise absolute value at most 2||h||_infinity. Bounded martingale differences have second moment O_a(n); Doob's L^2 inequality followed by a union bound over two coordinates gives the asserted maximal estimate. It controls every vertex, not merely S_n. The extra variable D_{n+1} is available from the infinite chain and presents no problem for the event determined by the first n directions.

With H=ceil(n^(2/3)), the exceptional probability is O_a(n^(-1/3)). Consequently a fixed positive fraction of the full exponential weighted mass stays in the square. This is enough; no local central limit theorem, endpoint return estimate, or nondegenerate covariance assumption is needed.

## 3. Endpoint and direction grouping

The number of endpoint/first-direction/last-direction classes is at most 16(2H+1)^2. Positive total mass and nonnegative weights justify the heavy-class bound. The endpoint parity need not be prescribed because P and Q are chosen from one common endpoint class. Empty or zero-weight classes do not cause difficulty.

The class may depend on n and on a. Only the bounds, not a fixed class across different lengths or parameters, are needed.

## 4. Mirror pairing and its seam

Reverse-negation sends NW to ES and ES to NW, and sends every uncounted adjacency to an uncounted adjacency. Therefore it preserves the weight exactly.

If P and Q have common endpoint z, then the second part of P revneg(Q), after k reverse steps, is at the vertex of Q at time n-k. It therefore retraces Q's vertex set, not a displaced second copy outside the square. This verifies both return to the origin and confinement.

The last direction of P is d and the first direction of revneg(Q) is -d. The possible seams are EW, WE, NS, SN. None is NW or ES. Hence the weight is exactly w(P)w(Q), not merely comparable to that product.

## 5. Padding and every additional seam

For f=W, the prefix ends in E and its entry seam is EW. For the remaining first directions f=E,N,S, the prefix ends in N and the entry seams are respectively NE, NN, NS. All have weight 1.

The departure seam is the reverse-negation of the entry seam and hence also has weight 1. The prefix has only straight adjacencies and one NE or EN adjacency. Its reversed-negated suffix has only straight adjacencies and one SW or WS adjacency. These all have weight 1.

The prefix ends at (H,H). The central closed path is translated into [0,2H]^2, and the suffix returns along the prefix in reverse, staying in the quadrant. No final/initial cyclic adjacency is counted. Thus padding works literally at a=0; it does not use division by a or any positive lower bound on a.

## 6. Injection, length, and exponent

For fixed n and the chosen class, H and A are fixed. From the constructed word one recovers P as the next n letters after the first 2H letters, then recovers revneg(Q) as the next n letters. Reverse-negation is invertible. Thus ordered pairs are counted injectively.

The output length is 2H+n+n+2H=2n+4H, so its half-length is exactly m_n=n+2H. There is no factor-of-two error. Summing the exact product weights gives B_n^2, and nonnegativity permits retaining this subfamily in Q_{m_n}.

Taking logarithms of the stated lower bound and dividing by m_n gives

    log Q_{m_n}/m_n
      >= [2n log lambda - 4 log(2H+1) + O_a(1)]/(n+2H)
      -> 2 log lambda.

Here H=o(n), log H=o(n), and m_n tends to infinity. A subsequence suffices for the lower limsup. The matching upper bound follows from the full weighted mass of all 2m-letter words. Both comparisons genuinely rely on a>=0.

## 7. Ordinary root limit

The optional root-limit strengthening is valid. A nonempty quadrant loop can start only with E or N and end only with W or S. Concatenation therefore has one of the seams WE, WN, SE, SN, none of which is counted. It is injective at specified component lengths and multiplicative in weight, so

    Q_{p+q}(a) >= Q_p(a)Q_q(a).

For every m, concatenating m independently chosen blocks EW or NS produces 2^m distinct loops with no counted corners. Thus Q_m(a)>=2^m, including a=0. Fekete's lemma applies to the finite real superadditive sequence log Q_m(a); the exponential upper bound keeps its limiting slope finite. The root limit exists and equals the proved limsup. No parity-zero subsequence remains because m denotes half-length.

## 8. Independent finite checks

As a non-probative implementation check, I exhaustively generated all n-letter words for n=1,...,6, retained those confined to the stated H-square, grouped by endpoint and first/last directions, and tested every ordered pair in every class. I checked reverse-negation invariance, exact corner-count addition, output length, return, quadrant confinement, and injectivity. All 85,208 constructed pairs passed. Counts by n were 4, 16, 64, 572, 6,304, and 78,248.

An independent integer dynamic program gave these coefficient lists for Q_m(a), in ascending powers of a:

    m=1: [2]
    m=2: [8, 2]
    m=3: [44, 24, 2]
    m=4: [288, 246, 52, 2]
    m=5: [2100, 2464, 882, 96, 2]
    m=6: [16480, 24756, 12724, 2502, 164, 2].

The first three agree with the source's model expansion. At a=1 the six values agree with the standard unweighted quadrant-loop enumeration. These checks support the encoding and seams but do not replace the asymptotic proof.

## 9. Optional exposition improvements and limits

1. State explicitly that at a=0 the zero-corner weight is 1, as evaluation of the polynomial dictates. The product definition already implements this convention.
2. In the root-limit addendum, identify the EW/NS blocks that prove Q_m(a)>=2^m. This makes the currently correct lower bound immediately transparent.

Neither point changes the proof. The crucial remaining obstruction for the full source question is signed cancellation: for a<0 the Markov representation is unavailable, and a positive squared weight of a constructed subfamily is not a lower bound for the total signed coefficient. The present argument must not be reported as settling that interval or the whole queue item.

