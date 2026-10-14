# Squared-kernel analytical target, not an established concentration estimate

This note proves a conditional spectral criterion and specifies its unproved enumerative hypothesis. The exact K, states C, F, lambda and rho are those in EXACT_GREEDY_TRANSFER.md. No new asymptotic bound on K is proved here. The hypothesis beta<lambda remains completely unestablished.

## Exact normalization and finite data

Define

    S_n = sum_{A,C in Av(213), |A|,|C|>=1, |A|+|C|=n} K(A,C)^2.

The square is an ordinary integer square: it counts ordered pairs of admissible interleavings with the SAME two normalized internal cell patterns. It is not the ordinary two-cell count sum K, nor the directed two-cycle count sum K(A,C)K(C,A).

Exact enumeration gives

    n:    2, 3,  4,   5,    6,     7,      8
    S_n:  0, 1, 15, 170, 1782, 18297, 187549.

These finite values do not prove a radius, a limiting ratio or an exponential growth bound.

On ell^2(C) define the size-symmetrized, still generally NON-SELF-ADJOINT matrix

    B(z)_{A,C} = z^((|A|+|C|)/2) K(A,C).

Its Hilbert-Schmidt norm squared, whenever finite, is exactly sum_n S_n z^n. Thus a certified beta = limsup S_n^(1/n) < lambda would put B(z) in the Hilbert-Schmidt (hence compact) class on an open neighborhood of the real critical point rho. A concrete way to prove this strict inequality would be to certify beta<=U and lambda>=L with U<L. Equality U=L gives no neighborhood and does not suffice for this route.

The crude bound K(A,C)<=binom(|A|+|C|,|A|), together with at most 4^m states of size m, gives S_n<=n*16^n, certifying |z|<1/16. The ordinary domino counts from the credited staircase paper can improve this crude certificate via K^2<=2^n K, but by themselves do not certify beta<lambda. No improved numerical bound is asserted here.

## Why compactness alone is not the conclusion

Put e(z)_A=z^(|A|/2). Formally the right and left path vectors are

    f(z)=sum_{r>=0}B(z)^r e(z),
    g(z)=sum_{r>=0}(B(z)^T)^r e(z).

Their coordinates are respectively z^(|A|/2)h_A and z^(|A|/2)ell_A. The exponentially marked-cell series is

    H(z,u)=sum_A u^|A| f_A(z)g_A(z).

Compactness at one z does not itself establish convergence of these Neumann series, an inverse I-B(z), control at nearby fugacities, or this weighted pairing. Those points must be checked.

A clean sufficient operator package is:

1. There are R>rho and u>1 with u*rho<R and R<1/4, and sum_n S_n R^n<infinity.
2. For every 0<z<rho, B(z) has spectral radius strictly below one on ell^2(C), so f and g above converge in ell^2 and are their minimal nonnegative path sums.

Under these two conditions the exact weighted-tail criterion (10) of the transfer note follows. Let D_u be diagonal with entries u^(|A|/2). Both D_u B(z) and D_u B(z)^T are Hilbert-Schmidt, because their squared entries are bounded by the summands defining sum_n S_n (uz)^n. Also D_u e(z) is in ell^2, since sum_A(uz)^|A| is the Catalan series minus one and uz<R<1/4. The equations f=e+Bf and g=e+B^Tg therefore show D_u f and D_u g are in ell^2. Cauchy-Schwarz gives

    H(z,u) <= ||D_u f||_2 ||D_u g||_2 < infinity.

The same u works for every z<rho. This supplies exponential largest-cell tails by the coefficient argument already proved in the transfer note. No boundedness of those weighted norms as z increases to rho, no finite critical expectation and no special critical eigenvector estimate are needed for that coefficient argument: each positive epsilon fixes a z strictly below rho, at which the finite constant is enough.

The strict squared-kernel margin is therefore valuable for more than compactness: it supplies exponential smoothing of BOTH left and right vectors. If only compactness exactly at rho were available, such smoothing would remain unproved.

## Conditional theorem and subcritical resolvent proof

**Conditional theorem.** If beta=limsup S_n^(1/n)<lambda, then the largest canonical greedy cell in a uniform1324-avoider has an exponentially small probability of exceeding epsilon*n, for every fixed epsilon>0. In particular, by the established deterministic staircase geometry, its permuton converges weakly to the anti-diagonal. The hypothesis beta<lambda has not been proved.

First beta>=4. Use just A=I_k,C=J_m in S_{k+m}; for k and m as equal as possible, the exact formula (8) in the transfer note is a central binomial coefficient minus one, whose square has nth-root limit4. Consequently beta<lambda implies rho<1/4. Choose

    rho<R<min(1/beta,1/4),  and  1<u<R/rho.

This proves condition1 of the smoothing package. We prove condition2 next; irreducibility and self-adjointness are unnecessary.

For positive bounded matrices on ell^2, entrywise T>=cU>=0 gives T^q>=c^qU^q. Also ||V||=sup_{x>=0,||x||=1}||Vx|| for a positive matrix V, since |Vx|<=V|x|. Operator norm is therefore monotone on positive matrices. Taking qth roots and applying the spectral-radius formula gives r(T)>=c*r(U).

Suppose at some 0<z<rho that r(B(z))>=1. Choose z<z'<rho. Since every cell is nonempty,

    B(z')_{A,C}=(z'/z)^((|A|+|C|)/2)B(z)_{A,C}
                >=(z'/z)B(z)_{A,C}.

Thus r(B(z'))>1. This operator is Hilbert-Schmidt. Enumerate the states by increasing size, and let P_N project onto the first N coordinates. For T=B(z'), the matrices T_N=P_N T P_N converge in Hilbert-Schmidt norm, hence operator norm, to T. This follows directly by deleting the tails of the convergent sum of squared matrix entries.

A nonzero compact spectral value of modulus greater than one persists in such truncations. Here is the precise argument. Choose an eigenvalue theta of T with |theta|>1, and a small closed contour around theta lying in {|w|>1} and in the resolvent except for its interior eigenvalue. Nonzero compact spectral points are isolated eigenvalues of finite algebraic multiplicity. The resolvent identity and Neumann series give uniform convergence of (wI-T_N)^(-1) to (wI-T)^(-1) on the contour. Their contour integrals, the Riesz projections, converge in operator norm. The limiting projection is nonzero; therefore the approximating projections are nonzero for all sufficiently large N. Some eigenvalue of T_N lies inside the contour, so r(T_N)>1. The cited compact-spectrum and Riesz-projection inputs are the only general spectral-theory facts in this step; the norm-approximation application is given explicitly here.

For completeness, the resulting finite matrix already contradicts the class count without any infinite-dimensional Perron theorem. Let e_N=P_N e(z'), whose N entries are strictly positive, with minimum d>0. Positivity gives, for every q,

    e_N^T T_N^q e_N >= d^2 * sum_{i,j}(T_N^q)_{i,j}
                     >= d^2 ||T_N^q||_2.

The last inequality follows from operator norm <= Frobenius norm <= sum of entries for a nonnegative finite matrix. Since r(T_N)>1, the spectral-radius formula shows that the sum over q of the right-hand side diverges. But every term e_N^T T_N^q e_N counts valid canonical state paths and is bounded, after summing q, by F(z')-1<infinity. Contradiction.

Therefore r(B(z))<1 for every z<rho. The Neumann series converge in operator norm by the spectral-radius formula. Applied to e(z), they give the ell^2 vectors f and g, with coordinates equal to the nonnegative path sums from the exact encoding. This proves condition2. The smoothing calculation in the preceding section proves H(z,u)<infinity for the same u>1 and every z<rho. Equation(11) of the transfer note then proves the conditional theorem.

## Primary spectral inputs and remaining problem

The standard compact-spectrum fact is stated in Stéphane Nonnenmacher, *Introduction to Spectral Theory*, Fall2022 notes, Theorem5.1.9, printed pp.67-68 (PDF pp.68-69):
https://www.imo.universite-paris-saclay.fr/~stephane.nonnenmacher/enseign/Spectral%20Theory%202022%20chap1-6.pdf#page=68

For the contour projection and isolated compact eigenvalue facts, see Leszek F. Demkowicz, *Lecture Notes on Non-Self Adjoint Operators and Related Topics*, dated4December2024, Theorem1.4 and Lemma1.12, PDF pp.12 and19:
https://oden.utexas.edu/media/pending_reports/book.pdf#page=12

These sources supply background spectral facts, not this staircase criterion or the unproved squared-kernel estimate. Source retrieval/inspection metadata is in SPECTRAL_SOURCE_PINS.json. No third-party source text is reproduced as a deliverable.

The only remaining hypothesis of the displayed conditional theorem is beta<lambda. Its truth is not asserted. A certified recurrence or shuffle-automaton bound for S_n is a concrete next task, but an empirical extrapolation of the finite coefficients is not a substitute. This conditional theorem does not close the original universal target or even its1324 case in this pass.
