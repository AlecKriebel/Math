# Construction attempt: the rank-one-short-orbit cyclic family

Date: 2026-10-20. This is an authored partial obstruction and unsuccessful construction search, not a resolution of the historical question.

## Family and target

Let n>=2, m be a positive integer with m>sqrt(2n), and

    L(n,m) = m Z^n + Z u,   u=(1,...,1).

This is a full-rank cyclic coefficient ideal in Z[X]/(X^n-1). Its determinant is m^(n-1). Its only shortest vectors are +/-u and lambda_1=sqrt(n), as proved in CYCLIC.md. We seek an exact (3/4,1/2)-LLL-reduced basis whose first vector is much longer than sqrt(n), ideally approaching exponential rate 1/2. An already-reduced input would suffice for the existential stationary-input interpretation; HNF-start behavior is a separate question.

## A new exact obstruction at large modulus

**Theorem.** Set

    M_n = max(sqrt(2)*n, n^(n/(2(n-1))) * 2^(n/4)).

If m>M_n, every classical LLL-reduced basis B of L(n,m) starts with +/-u. More precisely, if u has largest nonzero basis coefficient at index k>=2, then

    m <= n^(k/(2(k-1))) * 2^(k/4).

**Proof.** Any k vectors in L have the form m z_i+a_i u with z_i integral. In the multilinear expansion of any k-by-k coordinate minor, terms containing two copies of u vanish. All remaining terms contain at least k-1 factors m. Consequently every such minor is divisible by m^(k-1). The first k rows of a lattice basis are independent, so some minor is nonzero. By Cauchy-Binet their Euclidean k-volume V_k satisfies

    V_k >= m^(k-1).

Write u=sum_i c_i b_i with integer c_i, and let k be the largest index with c_k nonzero. Orthogonal projection onto the complement of span(b_1,...,b_(k-1)) gives c_k b_k*. Therefore D_k=||b_k*||^2<=||u||^2=n. The LLL inequalities D_(i+1)>=D_i/2 imply D_i<=2^(k-i)n for i<=k. Thus

    V_k = product_(i=1)^k sqrt(D_i)
         <= n^(k/2) * 2^(k(k-1)/4).

For k>=2, combine these estimates and take the (k-1)-st root to obtain the stated necessary bound on m. To eliminate k, put

    f(x) = x log_2(n)/(2(x-1)) + x/4.

For x>1, f''(x)=log_2(n)/(x-1)^3>0. Hence on [2,n] its maximum occurs at an endpoint; their exponentials are sqrt(2)*n and n^(n/(2(n-1)))*2^(n/4). For n=2 the interval is a singleton and both expressions equal 2sqrt(2). Thus m>M_n excludes every k>=2. If k=1, then u=c_1 b_1; shortestness of u forces |c_1|=1, giving the assertion.

The threshold is strict. Equality in the displayed modulus bound is not ruled out by this proof, and no claim of optimality is made. The ambient assumption m>sqrt(2n) is already automatic when m>M_n, but is retained to identify the shortest vectors in the construction problem.

For large n, M_n is asymptotic to sqrt(n)*2^(n/4). Consequently simply sending m arbitrarily far above the short-vector scale cannot produce a bad basis: eventually every reduced basis must recover u. This improves the trivial recovery threshold of order sqrt(n)*2^(n/2) obtained from the generic SVP bound and the nonconstant-vector lower bound m/sqrt(2). It still leaves a broad intermediate-modulus window and does not exclude the desired exponent 1/2 within that window.

## Exact-reduction search

Reproduction (from this package directory):

    python computation/cyclic_search.py --trials 30

The script starts with rows m e_1,...,m e_(n-1),u. For each parameter pair, it runs 30 deterministic-seed trials alternating fresh scrambled inputs with mutations of the best previously reduced basis. Operations are row permutations and integer elementary row additions, so membership and lattice determinant are preserved. SymPy LLL runs at exact delta=3/4. The best basis receives an independent Fraction-based Gram-Schmidt audit of every size-reduction and Lovasz inequality, a determinant check, and congruence-membership checks.

The exact machine-readable basis, Gram-Schmidt values, parameters, seed, histogram, and audit are in computation/cyclic_results.json. Tested pairs were (6,4), (8,5), (8,8), (12,6), (12,12), (16,8), (16,16), (20,10), and (20,20). All 270 trials returned a shortest first vector; no reduction call failed. These results are not exhaustive and cannot establish a general impossibility theorem.

## Frozen-first feasibility optimization

A second experiment deliberately prevents LLL from replacing its prescribed long first vector. For c in {0,1,2,floor(m/2),m} and t in {-m,floor(-m/2),-1,0,1,floor(m/2),m}, it fixes

    b_1 = m e_1 + c m e_2 + t u.

These are genuine basis vectors obtained by elementary row additions to the initial basis. The suffix is scrambled in three deterministic ways. The routine then performs size reduction and Lovasz swaps everywhere except the forbidden swap of the first two rows. Thus it searches for a reduced completion with that particular long first vector rather than allowing ordinary LLL to discard it immediately. Its objective is the remaining first-boundary score

    (D_2 + mu_(2,1)^2 D_1)/D_1 = ||b_2||^2/||b_1||^2,

which must reach 3/4. Floating-point arithmetic chooses unimodular operations; reported best candidates undergo an independent exact Fraction-based audit. A floating candidate or an unverified failure is never treated as a proof.

Reproduction:

    python computation/frozen_search.py

Detailed candidates and exact audits are in computation/frozen_results.json. The five runs tested (n,m)=(6,4),(8,5),(10,6),(12,8),(16,12), with 105 trials each (525 total). Their best exact boundary scores were respectively 3/7, 8/23, 5/17, 16/71, and 2/17, all below 3/4. Each recorded best candidate is exactly size-reduced and fails only the first Lovasz boundary. No candidate found satisfies all classical LLL inequalities. The experiment is a restricted search over prescribed first vectors and local suffix reduction, not a feasibility solver over all unimodular bases. In particular it cannot exclude much more complicated first vectors or deliberately poorly reduced suffixes that ordinary suffix LLL does not reach.

## What remains

No poor reduced basis was constructed. The new rigorous outcome is the large-modulus recovery theorem, not the experimental failures. A next construction attempt should concentrate on m between sqrt(2n) and approximately sqrt(n)*2^(n/4), and on structured unimodular transformations that distribute the short relation across many basis positions. The determinant and rank-one orbit permit this region; neither establishes that the desired extremal reduced basis exists.
