# Attempt 2: the first nonlinear degree for every graph

Use the notation of Attempt 1. For a nonempty subset S of V, let cbar(S) be the number of connected components of the complement of the induced graph Gamma[S]. Define the integer polynomial

P_Gamma(Q)=sum over nonempty S with cbar(S)>=2 of
 (Q-1)^(|S|-1) sum_{j=1}^{cbar(S)-1} binom(cbar(S)-1,j) Q^(j-1).   (3)

## Theorem

For every odd prime power q,

N_1(Gamma;q)=P_Gamma(q),
ch(Gamma,1;q)=q^(n-2) P_Gamma(q) when n>=2.

For n<2 the latter count is zero. In particular the number of degree-p characters is a polynomial in p for every graph, with nonnegative integer coefficients after substitution p=t+1.

## Proof

Every rank-two alternating n by n matrix has a factorization A=X^T J X, where X is a rank-two 2 by n matrix and J=[[0,1],[-1,0]]. To see this, quotient F_q^n by the radical of the form and choose a symplectic basis of its two-dimensional quotient. Conversely any such X gives rank two.

The fibres of X -> X^T J X have size |SL_2(F_q)|=q(q^2-1). Indeed equal alternating matrices have the same radical, so the two quotient maps differ by a unique invertible 2 by 2 matrix g; equality of forms says g^T J g=J, equivalently det(g)=1. The cardinality follows by choosing a nonzero first column (q^2-1 options), then a second column with determinant one (q options).

Let S be the indices of the nonzero columns of X. For two nonzero columns, their determinant vanishes precisely when they determine the same point of the projective line P^1(F_q), which has q+1 points. Every nonedge of Gamma[S] therefore forces equality of projective directions, and all such conditions together say exactly that the direction is constant on each component of the complement graph. There is no inequality requirement on graph edges: allowed entries may also be zero.

If c=cbar(S), the number of direction assignments using at least two directions is (q+1)^c-(q+1). This condition is exactly rank(X)=2. Once directions are fixed, every column has q-1 independent nonzero scalar choices, giving

(q-1)^|S| ((q+1)^c-(q+1))

matrices X. The case S=empty contributes zero and is excluded; a component count of zero must not be inserted into this expression. Dividing by q(q^2-1) gives

(q-1)^(|S|-1) ((q+1)^(c-1)-1)/q.

Expanding the numerator by the binomial theorem proves (3), without any division in the resulting polynomial. All coefficients in (3) as a polynomial in q-1 are nonnegative, because every power q^(j-1)=(1+(q-1))^(j-1) has that property. Attempt 1 finishes the character-count assertion.

## Boundary checks and limitation

An edgeless graph has connected complement on each nonempty S and gives zero. A single edge gives P=q-1. A complete graph on three vertices gives P=q^3-1, as every nonzero alternating 3 by 3 matrix has rank two.

The argument uses the fact that in dimension two symplectic orthogonality of nonzero vectors is equality of projective directions. In dimension four and above, orthogonality no longer reduces to equality. Replacing these projective directions by higher-dimensional points does not give the same component-count formula. Thus this attempt establishes i=1 for arbitrary Gamma, but not higher degrees. Historical novelty is not asserted.
