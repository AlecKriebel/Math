# Coefficients, projection, and multiplication

All coefficients are prime to the characteristic. For positive characteristic, invert the exponential characteristic as in Kahn–Levine §6.9 and Kahn §1. A division representative of degree d is fixed when d occurs. For a matrix algebra, using another degree changes the displayed finite bounds and varieties; Morita invariance of SK_i alone does not identify these presentations.

## Integral versus torsion coefficients

For i=1,2 put j=i+2. The usual connecting isomorphism for a field identifies

    B_i(F)=H^(j+1)(F,Q/Z(j)) ≅ H_et^(j+2)(F,Z(j)).

Thus i=1 means H^4(Q/Z(3)) and H_et^5(Z(3)); i=2 means H^5(Q/Z(4)) and H_et^6(Z(4)). The Brauer class has torsion-coefficient degree two and integral-motivic degree three. Cup-product with K_(i+1)^M has precisely the displayed degree and twist. Connecting maps must not be treated as unsigned degree-zero maps when changing product order; approach 5 explains the resulting limitation.

For N invertible in F, write Z/N(j) for the standard Tate-twisted coefficient sheaf, also denoted mu_N^(tensor j). Under the norm-residue theorem, the coefficient homomorphism

    H^(j+1)(F,Z/N(j)) → B_i(F)

is injective with image B_i(F)[N]. Indeed its kernel is the cokernel of multiplication by N on H^j(F,Q/Z(j)), which is divisible because it identifies with K_j^M(F) tensor Q/Z. This is the finite-to-infinite coefficient injection used in Kahn Corollary 7.4. The norm-residue theorem is now a theorem; the older papers label its applications by their required Bloch–Kato degrees.

For r|d set N=d/r. Then r[A] has order dividing N, and the finite geometric target is

    H^(i+3)(F,Z/N(i+2)) /
       (r[A] cup H^(i+1)(F,Z/N(i+1))).

The denominator identifies with D_(i,r)=r[A] cup K_(i+1)^M(F), and this finite quotient injects into Q_(i,r)=B_i/D_(i,r). This is the finite refinement of sigma_r^i. When r=d, N=1 and the finite target is zero, in agreement with SB(d,A) being a point. It does not make the separate SL_1 invariant c_A zero.

No finite refinement of beta with this particular N is inferred merely from torsion of its source. In general (B/D)[N] need not equal B[N]/D, even when ND=0. For example, B=Q/Z, D=B[2], N=4 gives orders four and two respectively. Torsion in a quotient can require representatives of higher order.

## The arrows are different

For s|r there is a quotient map Q_(i,r)→Q_(i,s), since D_(i,r)⊆D_(i,s). The maps q_r:B_i→Q_(i,r) are also quotient maps.

If eD_(i,r)=0, the reverse-direction map

    mu_e:Q_(i,r)→B_i,       b+D_(i,r)↦eb

is well-defined. It satisfies mu_e q_r=e and q_r mu_e=e, and its kernel is B_i[e]/D_(i,r). It is not a projection or a canonical inverse to q_r.

At finite level, coefficient reduction Z/4(3)→Z/2(3), followed by the standard inclusion Z/2(3)→Z/4(3), composes to multiplication by 2. These are Tate-twist coefficient maps, not a tensor product of three unrelated inclusions of roots of unity. They must not be replaced by an identity on B_i followed by a quotient projection.

## The explicit example in all three presentations

For F=Q_5((x))((y)) and A=(2,x)_2 tensor (5,y)_2, fix the iterated residue and local invariant identification B_1≅Q/Z. It identifies D_(1,1) with B_1[2]={0,1/2}.

Let s be the nonzero element of SK_1(A)≅Z/2. The established geometric values are

    sigma_1^1(s)=1/4+D_(1,1),
    sigma_2^1(s)=c_A(s)=1/2.

The first formula uses Suslin's injectivity, identified with sigma_1 in Kahn §7.C. The second uses Rost's injectivity and Kahn Theorem E. The sign of 1/4 is immaterial modulo D, and the sign of 1/2 is immaterial in B.

Therefore q_1(c_A(s))=0, while mu_2(sigma_1^1(s))=c_A(s). The map mu_2:B/D→B is an isomorphism in this particular infinite group. At finite level B[4]≅Z/4, D≅2Z/4, and sigma_1(s) is the nonzero coset in (Z/4)/(2Z/4). The quotient Z/4→Z/2 kills every image of a homomorphism Z/2→Z/4. Conversely the multiplier sends the nonzero quotient coset to 2∈Z/4. This exactly distinguishes Wouters's projection obstruction from his multiplier comparison.

The value beta_1(s) has not been computed here. Naming both potential values in the order-two quotient does not select one.
