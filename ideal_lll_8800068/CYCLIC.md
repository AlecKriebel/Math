# Cyclic and negacyclic obstructions for sharp LLL SVP factors

Date: 2026-10-20. Authored mathematical analysis; not a literature-status claim.
Conventions: full-rank coefficient lattices in Euclidean R^n, exact classical LLL parameters delta=3/4 and eta=1/2; the output measured is the first basis vector. Let D_i=||b_i^*||^2. Reduction implies D_{i+1} >= D_i/2.

## Main result: full shortest-vector rotational span halves the exponent

**Proposition.** Let L be a full-rank lattice invariant under an orthogonal linear map T. Suppose a shortest nonzero vector v has n linearly independent vectors among its T-orbit. Then every classical LLL-reduced basis B of L satisfies

    ||b_1|| / lambda_1(L) <= 2^((n-1)/4).

**Proof.** Choose independent orbit vectors v_1,...,v_n. Their integral span is a full-rank sublattice of L. Consequently

    det(L) <= det(span_Z(v_1,...,v_n)) <= product_i ||v_i|| = lambda_1(L)^n,

where the second inequality is Hadamard's inequality. The LLL inequalities yield

    det(L)^2 = product_i D_i >= D_1^n 2^(-n(n-1)/2).

Taking 2n-th roots gives ||b_1|| <= 2^((n-1)/4) det(L)^(1/n), and the assertion follows. This is a Hermite estimate converted to an SVP estimate by an additional, proved determinant inequality; the two measures are not being identified in general.

**Negacyclic corollary.** If n is a power of two and L is a full-rank coefficient ideal in Z[X]/(X^n+1), the proposition always applies. Multiplication by X is signed cyclic rotation and therefore orthogonal. The polynomial X^n+1 is irreducible over Q. For any nonzero v in this quotient, v,Xv,...,X^(n-1)v are Q-linearly independent: a dependence would make a nonzero polynomial of degree less than n annihilate the nonzero field element v. All these vectors lie in the ideal and have equal norm.

Thus the general classical LLL SVP exponent 1/2, specifically a target ratio >=2^((1/2-o(1))n), is IMPOSSIBLE for this power-of-two negacyclic specialization. No input convention, including adversarial already-reduced inputs, can evade the bound. This does not settle the historical question as recovered: its general coefficient-ideal formulation does not require this ring, and its phrase "worst-case approximation factor" does not specify the target exponent.

More generally, the same result applies to any cyclic or negacyclic lattice whenever at least one shortest vector has full rotational span. For q=X^n-1 this condition holds exactly when the shortest vector's representing polynomial is coprime to q over Q. For q=X^n+1 at arbitrary n the same coprimality test applies; irreducibility cannot be assumed at non-power-of-two n.

## Quantitative bound for partial rotational span

**Lemma.** If a lattice L contains d independent vectors, each of norm at most lambda_1(L), then every classical LLL-reduced basis satisfies

    ||b_1|| / lambda_1(L) <= 2^((2n-d-1)/4).

In particular this applies when the Q-span of a shortest vector's orthogonal rotational orbit has dimension d.

**Proof.** Express the d independent short vectors as rows of an integer coefficient matrix C relative to B. Write B=M G, where M is unit lower triangular and the rows of G are the orthogonal Gram-Schmidt vectors. In the exterior power, choose a lexicographically largest index set I of size d for which the corresponding minor of C is nonzero. Right multiplication by a unit lower triangular matrix leaves that minor unchanged: any other contributing index set is lexicographically larger, and its minor vanishes. The corresponding integer coefficient in the unnormalized orthogonal wedge basis has absolute value at least 1. Hence the length of this selected orthogonal wedge component is at least product_{i in I} sqrt(D_i). It follows that

    lambda_1(L)^d >= volume(v_1,...,v_d)
                      >= product_{i in I} sqrt(D_i)
                      >= ||b_1||^d 2^(-sum_{i in I}(i-1)/2)
                      >= ||b_1||^d 2^(-d(2n-d-1)/4).

Here the first inequality is Hadamard, and the last uses the largest possible sum of d distinct indices in {0,...,n-1}. Rearranging proves the lemma.

Consequently, a family matching exponent 1/2 under an orthogonal rotation must have shortest-vector orbit dimension d=o(n). Full-dimensional or positive-density orbit span quantitatively excludes that exponent.

## Scalar ideals cannot provide the sharp general SVP factor

For L=a Z^n, lambda_1(L)=a=det(L)^(1/n). Hence the same upper bound 2^((n-1)/4) holds, independently of which integer unimodular basis is supplied. Producing exponentially poor reduced unimodular bases, if possible, would prove only a weaker exponential-badness statement, not the requested exponent 1/2. This observation prevents spending a proof attempt on a target the scalar family cannot reach.

A small exploratory computation used SymPy exact rational LLL at delta=3/4, seed 8800068, dimensions 3,4,5,6,8,10, and 50 randomized unimodular inputs per dimension. Each input started at identity and applied 10n elementary row additions with coefficients from {-3,-2,-1,1,2,3}. All successful reductions had first-vector squared norm 1. This is only a negative toy experiment: no exhaustive classification, asymptotic obstruction to exponential reduced unimodular bases, or claim about arbitrary LLL implementations follows. The scalar upper bound above is analytic and does not depend on this experiment.

## Cyclic lattices genuinely need the span hypothesis

For n>=2 and an integer m>sqrt(2n), consider

    L = m Z^n + Z (1,...,1).

This is the coefficient ideal generated by m and 1+X+...+X^(n-1) in Z[X]/(X^n-1), and is invariant under cyclic rotation. It has determinant m^(n-1). Every vector in L has all coordinates congruent modulo m. If it is not constant, two coordinates differ by at least m, so its squared norm is at least m^2/2>n. A nonzero constant integer vector has squared norm at least n. Thus its only shortest vectors are plus or minus (1,...,1), with lambda_1=sqrt(n) and rotational span dimension 1.

In particular det(L)^(1/n)/lambda_1 = m^((n-1)/n)/sqrt(n) is unbounded with m. Therefore cyclic symmetry alone does NOT imply det(L)^(1/n)<=lambda_1, and the negacyclic argument cannot simply be transferred to all cyclic ideals. This example is not a construction of a poor LLL-reduced basis: the necessary basis/reduction assertions remain unproved.

## Outcome and remaining gap

The sharp general SVP-rate target is excluded for power-of-two negacyclic coefficient ideals, scalar ideals, and any orthogonally invariant family with positive-density shortest-vector orbit rank. General cyclic lattices with low-rank shortest-vector orbits, and general monic quotient rings with nonorthogonal multiplication by X, remain outside this obstruction. No sharp cyclic lower-bound family or general coefficient-ideal lower-bound family is established here. Nothing here establishes a worst-case output from HNF or any other canonical input.
