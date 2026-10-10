# Turn 4: complete reconstruction for prime-cyclic 3-cocycle inputs

Timestamp: 2026-10-03T09:36:00Z. Outcome: declared twisted subcase resolved; general target unresolved.
Completion estimate toward the general converse: 25% (subjective).

## Attempt and precise subcase

Let p be prime, let zeta=exp(2*pi*i/p), and identify C_p with residues 0,...,p-1. Consider the unitary pointed categories C_u=Vec_(C_p)^(omega_u), where u is a residue modulo p and

    omega_u(a,b,c)=zeta^[u a floor((b+c)/p)].

These normalized cocycles represent all of H^3(C_p,U(1))=C_p. Carry associativity proves the cocycle identity: the two ways of adding b,c,d give equal total carries, and replacing a+b by its residue changes the exponent only by a multiple of p.

Claim: within this declared family, ordinary TQFT isomorphism forces tensor equivalence of the inputs. In fact S^3 fixes p, and one lens-space value distinguishes the cocycle classes up to group automorphism.

## Derive the lens value, including the square

Use the standard orientation and generator for L(p,1). Its classifying map to BC_p takes the fundamental class to the generator of H_3(BC_p,Z)=Z/p. In the normalized bar complex, a representative is

    gamma_1 = sum_(j=0)^(p-1) [1|j|1].

For completeness this is the degree-three comparison map from the standard periodic cyclic-group resolution: the degree-one image is [1], the degree-two image is sum_j [j|1], and the degree-three image is gamma_1. The bar boundaries satisfy d(f_2)=N[1] and d(gamma_1)=(g-1)f_2 before tensoring with the trivial module, where N=1+g+...+g^(p-1). The standard lens-space CW model has the same resolution through dimension three; the infinite lens space is BC_p. After trivial coefficients, gamma_1 generates the Z/p homology group, with the stated orientation.

A homomorphism taking 1 to x sends this cycle to gamma_x=sum_j[x|[jx]_p|x]. Its weight is therefore

    product_j omega_u(x,[jx]_p,x)
      = zeta^[u x sum_j floor(([jx]_p+x)/p)]
      = zeta^(u x^2).

The last equality follows by telescoping [jx]_p+x-[(j+1)x]_p over j: the total is p*x. This also holds for x=0. Every homomorphism has centralizer C_p, so the normalized partition function is

    Z_u(L(p,1)) = (1/p) sum_(x=0)^(p-1) zeta^(u x^2).              (1)

Reversing the common orientation complex-conjugates every value and does not alter the equality criterion below. Equation (1) also agrees with the established cyclic-group/lens-space Gauss-sum formula; the calculation here makes its normalization and exponent explicit.

## Exact separation without approximate Gauss sums

Put c_u(k)=#{x:u*x^2=k mod p}, so p*Z_u=sum_k c_u(k)zeta^k. If Z_u=Z_v, the degree-at-most-p-1 integer polynomial

    P(X)=sum_k (c_u(k)-c_v(k)) X^k

vanishes at zeta. Since its minimal polynomial is Phi_p(X)=1+...+X^(p-1), P is a constant multiple of Phi_p. But P(1)=p-p=0, so that constant is zero. Thus equality holds exactly when the entire counting distributions c_u and c_v agree.

For u=0, c_u(0)=p; for u!=0, c_u(0)=1. For odd p and nonzero u, the nonzero support is u times the nonzero squares, with count two at each supported residue. Hence nonzero u,v give the same value exactly when u/v is a square. For p=2 the two possibilities u=0,1 give values 1 and 0 and are distinct.

The automorphism a of C_p acts on H^3(C_p,U(1)) by multiplication by a^2: pulling omega_u back and evaluating on gamma_1 gives zeta^(u*a^2), and evaluation on this homology generator identifies H^3 with the p-th roots of unity. Therefore the just-derived equality criterion is exactly membership in a common automorphism orbit. An appropriate relabeling makes the cocycle classes equal; their difference is a coboundary, which is precisely a scalar trivalent-basis/tensorator gauge change. Thus C_u and C_v are tensor equivalent. QED.

## Checks and limits

The standard-library verifier checks 20,207 cocycle pentagons for p=2,3,5,7, the lens exponent identity on 2,397 (p,u,x) cases for primes through 29, and all 2,397 pairs (p,u,v) for the exact cyclotomic-value/orbit equivalence. No floating-point comparison is used. These controls supplement the arbitrary-prime proof above; they are not the proof of the theorem.

This rules out counterexamples within the prime-cyclic family, including nontrivial associators. It does not cover arbitrary cyclic order, nonabelian groups, or arbitrary fusion categories. The general reconstruction route remains open. The finite-gauge and group-cohomology ingredients are classical, and no historical-priority claim is made for this subcase.
