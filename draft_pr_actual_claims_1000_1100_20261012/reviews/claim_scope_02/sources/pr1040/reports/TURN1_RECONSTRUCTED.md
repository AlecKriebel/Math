# Reconstruction of accepted turn 1 findings

Historical status: accepted before interruption, as reported in the surviving assignment. The exact original text and audit bytes were not recovered. This file provides rechecked derivations and does not claim a new independent acceptance.

## 1 Recovering the part supported on squarefree n

Let n be positive and squarefree, and let m be any positive integer. Set u_0=m. Repeatedly compute

    g_k = gcd(n,u_{k-1}),
    u_k = u_{k-1}/g_k,

as long as g_k>1. If there are t nontrivial layers, put

    A = product_{k=1}^t g_k,
    R = product_{1<=k<=t, k even} g_k,
    S = A/R^2,
    u = u_t = m/A.

Empty products are 1. All displayed divisions are exact.

For any prime p dividing n, let e=v_p(m). Since n is squarefree, p divides g_k exactly when k<=e, and then with exponent one. Consequently

    v_p(A)=e,
    v_p(R)=floor(e/2),
    v_p(S)=e mod 2,
    v_p(u)=0.

No prime outside n divides any g_k. Hence A is the entire n-supported part of m, S is squarefree, and gcd(u,n)=1. No coprimality between R and S is asserted or required.

The algorithm uses at most floor(log_2 m) nontrivial layers because every such division reduces u by a factor of at least two. All intermediates A,R,S,u are at most m. Gcd, multiplication, and exact division of integers of polynomial bit length give a deterministic polynomial bit algorithm in the combined input lengths of n and m. The prime factorization of n is used only in this proof, never by the algorithm.

## 2 Coprime query normal form

If C7(u)=(r_u,s_u), then

    C7(m)=(R r_u, S s_u).

Indeed, m=(R r_u)^2(S s_u). The prime support of S is contained in n, while that of s_u is disjoint from n, so S s_u is squarefree. Uniqueness of the positive squarefree decomposition proves the formula.

Given any bounded classical C7 computation on a squarefree n, replace each virtual oracle query m by this preprocessing, one actual query u coprime to n, and the displayed answer reconstruction. Queries u=1 can instead be answered directly. The simulated computation receives the identical answer to its identical virtual query. Induction over successive queries therefore preserves its complete virtual transcript, output, and success or failure on each fixed random tape, including adaptive choices. The actual oracle query transcript changes from m to u; it is the simulated transcript that is identical.

Query lengths do not increase, and polynomial overhead is added. The transformation works with every correct C7 oracle. It is a normalization of access, not an oracle-free simulation.

For example, n=35 and m=72 are coprime. C7(72)=(6,2), and

    gcd(35,6-1)=5.

Thus an answer to a query coprime to n can still be useful after subtraction. One cannot infer that coprime queries contain no usable factoring information.

## 3 Valuation tags and exact recoverable blocks

Let z_1,...,z_t be positive integer tags. Partition the primes p dividing squarefree n by the joint vectors

    (v_p(z_1),...,v_p(z_t)).

The product of the primes in every nonempty block can be obtained without factoring n. For one tag, its gcd layers h_k are the products of primes having valuation at least k. The layer quotient h_e/h_{e+1} is the product with valuation exactly e, while n/h_1 is the valuation-zero product. Refining these partitions across tags uses intersections by gcd and complementary pieces by exact division. The number of nonempty blocks is at most the number of primes dividing n, itself at most log_2 n. Layer counts and all bit lengths are polynomial in the explicit input size.

A useful limitation follows. Suppose p and q have equal valuations in every initialized integer available to a computation. The following operations preserve that equality:

- multiplication, because valuations add;
- exact division, because valuations subtract;
- gcd and lcm, because valuations take minimum and maximum;
- common nonnegative integer powers, because valuations are multiplied by the exponent;
- exact integer kth roots, when defined, because valuations are divided by k;
- C7, because its two output valuations are floor(e/2) and e mod 2.

This is an induction on the generated integers. Any initialized constants or extra inputs must be included among the tags. Selecting an existing integer according to a bit computation preserves equality, but constructing a new integer by arbitrary bit decoding is a new tag and is outside this closure argument.

In particular, this closure cannot manufacture a proper divisor of pq if its initialized integers all have equal p- and q-valuations. It is not a theorem about arbitrary classical algorithms. Addition, subtraction, modular reduction, or freshly bit-constructed integers can break the invariant. The n=35 example does so immediately.

## 4 Normalized fresh polynomial tags

The following estimate applies to a restricted experiment, not to every C7 algorithm. Let n=pq with distinct primes. At a stage, a polynomial F in Z[X] is selected from past information, before a fresh uniform ell-bit integer X is sampled. Put M=2^ell, so X is uniform on {0,...,M-1} and independent of that past.

Before evaluating F, normalize its coefficients:

1. If F is identically zero, discard it as uninformative for this bound.
2. Compute g=gcd(n, all coefficients of F).
3. If 1<g<n, record a coefficient-split event. This already gives a proper factor and is not a root-probability event.
4. If g=n, divide all coefficients by n and repeat.
5. If g=1, use the resulting polynomial G.

The normalization terminates in polynomial bit time on an explicit polynomial, since each division reduces nonzero coefficient lengths. It ensures that G is nonzero modulo both p and q. Retaining the stripped power n^k in the original tag affects both valuations equally, so it does not itself separate p and q.

If deg(G)=d, then G has at most d roots over each prime field. Each residue class modulo p occurs at most ceil(M/p) times in the sampling interval, so

    Pr[p divides G(X) | past] <= d(1/p + 1/M).

The same argument gives the q bound, and hence

    Pr[gcd(G(X),n)>1 | past]
        <= d(1/p + 1/q + 2/M).

A degree-zero polynomial with normalized coefficient gcd one has no such hit. The bound remains true when its right side exceeds one, although then it is uninformative.

## 5 Adaptive degree budget and correct event statement

Allow adaptively chosen stages, with each G selected before its fresh independent X. Stop the relevant experiment at a coefficient split. Let d_t be the degree of the normalized polynomial at active stage t, and suppose that on every possible execution path

    sum_t d_t <= D.

Multiplying each conditional root estimate by the indicator that its stage is active, then summing expectations, proves

    Pr[some hit before the first coefficient split]
        <= D(1/p + 1/q + 2/2^ell).

The budget must be pathwise. A mere bound along one observed run is insufficient. Polynomial-time use also requires polynomially bounded numbers of zero-degree operations and explicit coefficient lengths; the degree budget alone is not a bit-complexity bound.

If, within a separately specified restricted factoring scheme, every success without a coefficient split requires such a hit, then

    Pr[success AND no coefficient split]
        <= D(1/p + 1/q + 2/2^ell).

It is incorrect to condition the fresh-variable law on the future event that no coefficient split will ever occur. That event may depend on later observations and bias the samples. The valid argument uses conditioning only on the past at each stage, then the joint-event bound above. It is also incorrect to drop coefficient-split successes from the total success probability without an additional bound for them.

For an explicit balanced range p,q >= 2^(ell/2-2), the right side is at most

    10 D 2^(-ell/2).

This conservative constant follows from 1/p+1/q<=8*2^(-ell/2) and 2*2^(-ell)<=2*2^(-ell/2). Other conventions for balanced primes can sharpen the constant; they do not broaden the model. Low-degree root bounds, gcd layers, and valuation invariance are standard techniques; no novelty is asserted.

## 6 Existing distinct exponent result

The classical black-box reduction for integers whose distinct prime factors have pairwise distinct positive exponents is already established in Section 5, Theorem 5.3, of Kahanamoku-Meyer, Ragavan, Vaikuntanathan, and Van Kirk, *The Jacobi Factoring Circuit: Quantum Factoring with Near-Linear Gates and Sublinear Space and Depth*, arXiv:2412.12558v4. The postprocessing outside the squarefree-decomposition subroutine is classical. This prior result is credited rather than claimed as new.

A squarefree composite has at least two exponents equal to one, so it does not meet that theorem's distinct-exponent hypothesis. The theorem therefore does not settle the central squarefree case here. See the [versioned source](https://arxiv.org/html/2412.12558v4#S5).

## 7 Remaining gap

The unrestricted algorithm may exploit addition, modular arithmetic, oracle-derived bit patterns, and adaptive constructions outside these restricted models. No general classical polynomial-time reduction or impossibility theorem has been obtained.
