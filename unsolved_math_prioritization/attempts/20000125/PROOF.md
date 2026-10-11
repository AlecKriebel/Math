# Audited proof of the smooth prime field hypersurface theorem

## Result and attribution

For each prime p, each n ≥ 2, and each d ≥ n+1, there exists a geometrically smooth, geometrically integral degree-d hypersurface X in projective n-space over F_p such that |X(F_p)| is not 1 modulo p. A finite deterministic search in an explicitly given family finds a defining equation.

The construction, its case division, and the theorem are attributed to Alper Ferudun, *Smooth Hypersurfaces Beyond the Chevalley-Warning Range over Prime Fields*, dated 6 September 2026, DOI https://doi.org/10.5281/zenodo.22514087 and canonical record https://eulersolve.org/papers/aim-algebraic-geometry-0125/ . This document is an independently checked reconstruction, not a claim of a new theorem or of priority. The source is an unrefereed preprint and discloses AI assistance. Its displayed publication status and reported computations are not substitutes for the proof below. No author-supplied source code was executed in this audit.

The formulation in AIM Problem 9.5 at http://aimpl.org/ratsubvarpos/9/ omits a smoothness hypothesis and asks a disjunction: a degree-d hypersurface over the specified prime field, d ≥ n+1, with point count not 1 modulo p, or one that is not rationally connected. The theorem here proves its numerical alternative with the additional properties above. The distinct 2015 question https://mathoverflow.net/questions/220163 explicitly requests smooth hypersurfaces for each triple (d,p,n). No identification of rational connectedness with separable rational connectedness is needed.

Throughout, put m=n+1, use coordinates x_0,...,x_{m-1}, and work over the algebraic closure K of F_p when testing smoothness. Thus d ≥ m ≥ 3. The Jacobian criterion for a projective hypersurface says that a singular point is a nonzero coordinate vector at which both F and every partial derivative vanish. When p divides d, F must not be dropped from this condition.

## A finite field coefficient lemma

Take any positive integers v_i summing to d. Write Q=∏ x_i^{v_i}. Let H_0,...,H_{r-1} be degree-d monomials, each omitting at least one coordinate, and put

    F_A = Q + Σ_j A_j H_j,
    C(A) = (-1)^m Σ_{x∈F_p^m} F_A(x)^{p-1}.

The parameters A_j in this definition are indeterminates. The elementary power sum over F_p is zero if the exponent is zero, is -1 if the exponent is a positive multiple of p-1, and is zero otherwise. The zero-exponent assertion holds in F_p because the sum has p summands. Consequently the constant coefficient of C is 1: every exponent v_i(p-1) is positive and divisible by p-1. A power A_j^{p-1} can occur only by selecting H_j in all p-1 factors; its omitted coordinate makes its power sum zero. Thus deg_{A_j} C ≤ p-2.

Evaluation on (F_p^*)^r is injective for polynomials with individual degrees at most p-2. To prove this, induct on r. If a polynomial is zero at every grid point, fix all but the last coordinate. The resulting univariate polynomial, of degree below p-1, has p-1 roots and is identically zero. Its coefficient polynomials vanish on the smaller grid, so the induction makes them all zero. Since C has constant coefficient 1, there is a tuple A with every A_j nonzero and C(A)≠0. This includes p=2, where C is the constant polynomial 1.

For a positive-degree homogeneous equation F, let N_a and N_p count its affine and projective rational zeros. The origin is an affine zero, and every projective point has p-1 nonzero representatives, so N_a=1+(p-1)N_p. Also, the indicator of F(x)=0 is 1-F(x)^{p-1}. Summation modulo p gives N_a=-Σ_x F(x)^{p-1}. Therefore

    N_p ≡ 1 + (-1)^m C(A)  (mod p).

It remains to select a count-good tuple whose equation is geometrically smooth.

## Odd characteristic with p not dividing d

Set t=d-m+1 and use

    F_A = Σ_{i=0}^{m-1} A_i x_i^d + x_0^t x_1...x_{m-1},
    v=(t,1,...,1),   A_i∈F_p^*.

For this family the final individual degree improves to deg_{A_{m-1}} C ≤ p-3. Indeed, degree p-1 already vanishes by the lemma. A term of degree p-2 uses p-2 final pure powers and one other summand. If the remaining summand is a pure power, at most two coordinates occur, so m≥3 gives a missing-coordinate sum. If it is Q, coordinate x_1 (or any coordinate indexed from 1 to m-2) has exponent 1, whose power sum is zero for odd p. These are all possibilities.

First exclude critical points on the coordinate boundary. At least two zero coordinates make every derivative of Q vanish; a nonzero coordinate then has pure-power derivative dA_i x_i^{d-1}≠0. With exactly one zero coordinate x_j, if j≠0 the x_0 derivative is nonzero because its Q term still contains x_j. If j=0, the derivative in any nonzero coordinate is nonzero because its Q term contains x_0. Thus a common derivative zero must lie on the torus.

There the equations x_i F_{x_i}=0 give

    d A_i x_i^d = -v_i Q.

If p divides t, the i=0 equality is already impossible. Otherwise every v_i is nonzero modulo p. Raise equality i to the integer power v_i and multiply over i. Since Σ_i v_i=d and ∏_i x_i^{v_i}=Q, cancellation of Q^d yields the necessary condition

    d^d A_0^t A_1...A_{m-1} = (-1)^d t^t  in F_p.

Once the first m-1 nonzero coefficients are fixed, at most one nonzero value of A_{m-1} satisfies this equality. Choose a count-good tuple by the coefficient lemma and freeze its first m-1 entries. The resulting nonzero univariate polynomial has degree at most p-3, so at least two elements of F_p^* keep it nonzero. At most one is a singular candidate. Choosing another gives a smooth count-good equation. For p=3 the polynomial is constant, and the same two-value argument applies. If p divides t, every count-good tuple is already smooth.

## A chain lemma when p divides d

For a positive exponent vector v of sum d, put

    T_i = x_i^{d-1} x_{i+1}  (0≤i≤m-2),
    F_A = Σ_{i=0}^{m-2} A_i T_i + A_{m-1} x_{m-1}^d + Q,
    s_i = v_0+...+v_i,
    B = 1 + Σ_{i=0}^{m-2} s_i  in F_p.

Every monomial except Q omits a coordinate. All A_i below are nonzero. We prove that the whole family is smooth if any proper prefix s_i is zero modulo p or if B=0.

The torus derivative equations are triangular. Since d-1=-1 in F_p,

    A_0 T_0 = v_0 Q,
    A_i T_i = A_{i-1} T_{i-1}+v_i Q = s_i Q  (1≤i≤m-2).

The last equation is consistent because it becomes (Σ_i v_i)Q=dQ=0. If s_i=0, the equality A_iT_i=s_iQ is impossible on the torus. If all proper prefixes are nonzero, then at any torus critical point

    F_A = BQ + A_{m-1} x_{m-1}^d.

For B=0 the right side is nonzero, so the critical point is not on the hypersurface.

Here is a boundary proof requiring neither condition on the prefixes. If at least two coordinates vanish, all Q derivatives vanish. The final derivative is then A_{m-2}x_{m-2}^{d-1}=0, hence x_{m-2}=0. Descending through the derivative indexed by j gives x_{j-1}=0 whenever x_j=0, because d-2≥1. Thus x_0=...=x_{m-2}=0. The only remaining projective possibility has x_{m-1}≠0, at which F_A=A_{m-1}x_{m-1}^d≠0. If exactly x_j=0 and v_j≥2, every Q derivative is again zero, and the same conclusion holds.

Suppose instead that exactly x_j=0 with v_j=1. If j=m-1, the x_0 derivative is -A_0x_0^{d-2}x_1≠0; here m≥3 ensures x_1 is nonzero. If j≠m-1, the Q contribution to the last derivative vanishes, so that derivative forces x_{m-2}=0, hence j=m-2. For m≥4 the derivative indexed by m-3 is A_{m-4}x_{m-4}^{d-1}≠0, since its other chain term contains x_{m-2} and its Q term contains the same zero coordinate. For m=3, the exceptional possibility is x_1=0 with x_0,x_2≠0. Both T_0 and T_1 and Q vanish, while F_A=A_2x_2^d≠0. No boundary point is singular.

### Multiples strictly above p

If p divides d and d>p, then d≥2p. Choose an integer k with

    max(1,m-d+p) ≤ k ≤ min(p,m-1).

This interval is nonempty: each lower bound is at most p, and each is at most m-1, using m≤d, d-p≥1, and m≥3. We may choose k positive entries summing to p, followed by m-k positive entries summing to d-p. For example, use

    (p-k+1,1,...,1 ; d-p-(m-k)+1,1,...,1).

The two interval bounds make the first entries of both blocks positive. The prefix ending at index k-1 has sum p and is proper. The chain lemma makes every nonzero coefficient tuple smooth; the coefficient lemma supplies one with C≠0. This covers p=2 in every even degree allowed by d≥m≥3.

### Degree p with fewer than p variables

Here d=p and 3≤m<p, so p≥5. Write v_j=1+e_j with e_j≥0 and Σ_j e_j=L=p-m. Direct summation gives

    B = 1 + m(m-1)/2 + Σ_{j=0}^{m-1}(m-1-j)e_j  (mod p).

The final sum attains every integer from 0 to (m-1)L: it is the sum of L numbers in {0,...,m-1}, and the quotient/remainder algorithm represents every integer in that interval using at most L nonzero summands. When m=p-1, the first two terms reduce to 2 modulo p and L=1; choosing the available value p-2 makes B=0. When 3≤m≤p-2,

    (m-1)(p-m) - 2(p-3) = (m-3)(p-m-2) ≥ 0,
    2(p-3) ≥ p-1.

Hence the attainable interval contains representatives of every residue modulo p; choose the one making B=0. The chain lemma and coefficient lemma again supply smoothness and the desired count for the same tuple.

### Equal prime degree and variable count

The only remaining dividing-characteristic case is d=m=p. Since m≥3, p is odd. Fix a∈F_p^* with a≠1, for instance a=2, and define

    P=∏_{i=0}^{p-1} x_i,
    F=Σ_{i=0}^{p-2} x_i^{p-1}x_{i+1} + a x_{p-1}^p + P.

The boundary proof above applies. At a torus singularity the same triangular equalities read T_i=(i+1)P. Since 1+...+(p-1)=0 in F_p, the equation F=0 implies P=-a x_{p-1}^p. Multiplying the p-1 chain equalities and applying Wilson's theorem gives

    -P^{p-1} = ∏_{i=0}^{p-2} T_i
              = P^p / (x_0 x_{p-1}^{p-1}).

Combining these identities gives x_0=a x_{p-1}. Normalize x_{p-1}=1; thus x_0=a and P=-a. The recurrence

    x_{i+1} = -(i+1)a / x_i^{p-1}

now proves inductively that every coordinate is in F_p^*: the initial coordinate is, and the numerator is a nonzero element of F_p at every indicated index. Only after this induction is it legitimate to set every denominator to 1 by Fermat's theorem. The final recurrence says x_{p-1}=a, contradicting x_{p-1}=1 and a≠1. Thus smoothness has been proved over K, not merely over F_p.

For the count, every monomial of F^{p-1} has total degree p(p-1) in p variables. To survive all coordinate sums, every exponent must be a positive multiple of p-1; consequently every exponent must equal p-1. Suppose a contribution to P^{p-1} uses the first chain term e_0 times and P itself b times. Its x_0 exponent is (p-1)e_0+b=p-1, so either (e_0,b)=(0,p-1) or (1,0). The latter would force 1+(p-1)e_1=p-1 at x_1, impossible for an integer e_1 because p≥3. The former uses only P and has coefficient 1. Therefore C=1, and the count is 1+(-1)^p=0 modulo p.

## Characteristic two in odd degree

Now p=2 and d is odd. Set t=d-m+1 and define

    Q=x_0^t x_1...x_{m-1},
    F=Σ_{i=0}^{m-1}x_i^d + x_0^{d-1}x_1 + Q.

Every non-Q term omits a coordinate, so the coefficient sum with p-1=1 is 1. Hence the projective point count is even. Since d≡1 and d-1≡0 modulo two, the derivatives are

    F_{x_0}=x_0^{d-1}+t x_0^{t-1}x_1...x_{m-1},
    F_{x_1}=x_1^{d-1}+x_0^{d-1}+Q/x_1,
    F_{x_i}=x_i^{d-1}+Q/x_i   (i≥2).

The quotients here denote the monomials with the corresponding exponent lowered by one, so they are polynomial expressions valid on the boundary.

If t is even, the first derivative forces x_0=0. Since t≥2, every remaining Q derivative vanishes, and the remaining derivative equations force all coordinates to vanish. Suppose t is odd. At least two zero coordinates annihilate every Q derivative, again forcing all coordinates to vanish. With exactly one zero coordinate x_j, j≠0, the first derivative is nonzero. With only x_0=0, the first derivative is nonzero if t=1; if t≥3, the second derivative is nonzero. A projective critical point must therefore be on the torus.

Normalize x_0=1. The first derivative then yields Q=1. Multiplication of F_{x_i}=0 by x_i yields x_i^d=1 for i≥2. Since ∏_{i=1}^{m-1}x_i=Q=1, raising to the d-th power also gives x_1^d=1. But multiplying the second derivative by x_1 now gives

    x_1^d+x_1+Q = 1+x_1+1=x_1≠0,

a contradiction. This is an algebraic-closure calculation and makes no assumption that the coordinates are rational.

## Exhaustion and geometric integrality

The cases are exhaustive: odd p with p not dividing d; p dividing d with d>p, d=p>m, or d=p=m; and p=2 with d odd. Each displayed form is a nonzero homogeneous form of degree d. Each selected equation is smooth over K and has C≠0, hence the required point-count failure over the original prime field. All coefficient choices are finite: enumerate nonzero field tuples, compute C, and in the diagonal case exclude the one possible bad final coefficient.

For completeness, geometric integrality does not need a separate assumption. Factor F over K. A repeated positive-degree factor G makes F and all partials vanish at every projective point of G=0, contrary to smoothness. If F has two distinct positive-degree factors G and H, their homogeneous ideal in K[x_0,...,x_{m-1}] has height at most two. Its affine zero set has dimension at least m-2≥1, so it contains a nonzero point: otherwise its radical would be the maximal ideal of the origin, of height m≥3. At this point G=H=0 and the product rule makes F and every partial vanish, another contradiction. Thus F has one irreducible factor with multiplicity one. Its projective hypersurface over K is integral.

## Exact scope and the literal unsmoothed question

For the unsmoothed AIM wording there is a simpler witness. Choose an F_p-linear injection from F_p^{n+1} into the degree-d extension F_{p^d}; this is possible because n+1≤d. Restrict the degree-d norm polynomial to that subspace. Its coefficients are in F_p, it is homogeneous of degree d, and on rational vectors its only zero is the origin. It therefore defines a degree-d projective hypersurface with no F_p-points. It is a nonzero polynomial because it evaluates nontrivially on any nonzero rational vector. This argument does not supply a smooth or geometrically integral hypersurface; over the algebraic closure the norm decomposes into linear factors.

For n=1 and d≥2, homogenizing any irreducible degree-d polynomial over F_p gives a smooth finite étale hypersurface of projective one-space without rational points. Finite fields are perfect, so the polynomial is separable. Over the algebraic closure it consists of d distinct points and is not integral for d>1. The main theorem appropriately begins at n=2. There is no n=0 claim.

No assertion is made of point-freeness for the smooth constructions, an exact number of rational points, a polynomial-time search, simultaneous failure over all extension fields, a finite-field generalization modulo q, non-rational-connectedness proved from the canonical divisor, human peer review, or formal proof-assistant certification.
