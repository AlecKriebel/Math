# A lens-space counterexample to Ohtsuki Conjecture 7.5 for SU(5)

**Target:** 10400120 / AMR-103-0120. **Status:** complete counterexample candidate, independent review pending. **Substantive approaches:** 2/5. No novelty or human peer-review claim.

## Statement

For the standard SU(5) Witten–Reshetikhin–Turaev theory at WZW level k=5, hence shifted level r=k+5=10, use the normalization tau(S3)=1. Then

    |tau_10^SU(5)(L(5,1))|^2 = 3475 + 1550 sqrt(5),
    |tau_10^SU(5)(L(5,2))|^2 = 4025 + 1800 sqrt(5).             (1)

Both numbers are strictly positive and unequal. Both closed connected oriented three-dimensional lens spaces have fundamental group Z/5. Thus the universal claim that the absolute value of a nonzero quantum G invariant depends only on the fundamental group is false. Reversing an orientation conjugates the invariant and does not affect this comparison. A common nonzero normalization depending only on the fixed theory also cannot restore equality.

The source is Conjecture 7.5, printed p474 of [Ohtsuki's collection](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf); Section7.1 specifies closed oriented three-manifolds, the quantum G invariant and r=k+h-dual. SU(5) is compact, simple and simply connected, so it lies within that scope. This is the ordinary unrefined invariant, with no boundary, inserted link, spin choice or retained manifold framing. Signature/framing correction factors below have modulus one. The nonvanishing qualification is met for both examples. This does not contradict the original authors' SU(2) lens-space theorem or their finite SU(3) numerical checks.

## 1. Primary formulas used

[Guadagnini–Pilo, Three-manifold invariants and their relation with the fundamental group](https://arxiv.org/abs/hep-th/9612090), equations(13),(16),(19),(20), express the invariant of rational unknot surgery p/q through the vacuum entry of

    S T^(a1) S ... T^(ad) S,

where p/q=a1-1/(a2-...-1/ad), divided by S00, up to a unit-modulus signature factor. Their invariant is normalized to one on S3. For our two spaces the words are S T^5 S and S T^3 S T^2 S, since 5/2=3-1/2. Reversing the order of the second chain transposes the vacuum matrix entry and leaves it unchanged.

The unitary Lie-theoretic matrices are supplied by [Hansen–Takata](https://arxiv.org/abs/math/0209403), equation(12), with admissible root/shifted-weight conventions in Section4, pp26–27. In type A4 the rank is4, the number of positive roots is10, the dual Coxeter number is5 and the weight/root lattice volume ratio is1/5. The shifted level10 is permitted. Suppressing only a scalar phase in T, their formula becomes

    S_(lambda,mu) = -1/(100 sqrt(5))
        sum_(w in S5) sign(w) exp(-2 pi i <w(lambda+rho),mu+rho>/10),
    T_lambda = exp(pi i (|lambda+rho|^2-|rho|^2)/10).             (2)

The omitted scalar phase in T and the surgery signature phases multiply each answer by a phase and disappear from (1). We retain the normalization magnitude in S. The Weyl sum is exactly a determinant expansion; the minus sign is i^10. No semiclassical approximation is being used. These published modular/surgery formulas are imported mathematical inputs, rather than re-proved quantum-group construction theorems.

## 2. Complete finite index set and exact arithmetic

Index the 126 integrable highest weights by all four-tuples

    a=(a1,a2,a3,a4), ai>=0, sum ai<=5.

Lexicographic order places the vacuum a=0 first. Put

    l_i = sum_(j=i)^4 a_j + 5-i       (i=1,...,5),
    y_i(a) = 5 l_i - sum_(j=1)^5 l_j.

(The empty sum for i=5 is zero.) Then lambda+rho=y(a)/5 in the standard Euclidean realization of A4, and y(0)=(10,5,0,-5,-10). Let zeta=exp(2 pi i/100). Define the integer cyclotomic quantities

    D_ab = sum_(w in S5) sign(w) zeta^[-2 sum_i y_i(a)y_(w(i))(b)/5],
    t_a  = [sum_i y_i(a)^2 - 250]/5  (mod100).                 (3)

Every exponent is an integer: all y_i(a) have a common residue modulo5 and sum to zero, so their dot products are divisible by5; the squared-norm difference is likewise divisible by5. Equations(2) read S=-D/c and T_aa=zeta^(t_a), where c=100sqrt(5), c^2=50000.

Define the two finite sums

    A = sum_a D_0a D_a0 zeta^(5t_a),
    B = sum_(a,b) D_0a D_ab D_b0 zeta^(3t_a+2t_b).              (4)

The surgery formulas consequently give

    |tau(L(5,1))|^2 = A conjugate(A)/(50000 D_00 conjugate(D_00)),
    |tau(L(5,2))|^2 = B conjugate(B)/(50000^2 D_00 conjugate(D_00)). (5)

All sums in(3)–(4) are finite, with explicitly given ranges. They can be checked by the short accompanying program using exact integers in Z[zeta].

## 3. Exact finite-sum certificate

Use the irreducible cyclotomic polynomial

    Phi_100(X)=X^40-X^30+X^20-X^10+1.

Reducing the sums(3)–(4) in the power basis 1,zeta,...,zeta^39 gives

    D_00 = 5 - 10 zeta^20 + 10 zeta^30,
    A = 12500 - 20000 zeta^10 + 10000 zeta^20 - 20000 zeta^30,
    B = -3750000 - 2500000 zeta^20 + 2500000 zeta^30.           (6)

The verifier enumerates all126weights and all120Weyl permutations; it computes the entries and the two sums, then asserts each equality in(6). It also multiplies by the conjugate, with conjugation zeta->zeta^(-1), and verifies

    D_00 conjugate(D_00) = 125 - 200u,
    A conjugate(A) = 406250000 + 125000000u,
    B conjugate(B) = 20312500000000 + 12500000000000u,           (7)

where u=zeta^20-zeta^30=2cos(2pi/5)=(sqrt(5)-1)/2. Substitution in(5), followed by u^2+u=1, yields(1).

For an immediate nonzero/inequality check, 0<u<5/8, so 125-200u>0; all numerator expressions in(7) are positive. The difference between the second and first squared magnitudes is

    550+250sqrt(5)>0.

Equivalently the cross-multiplied cyclotomic difference is

    50000 A conjugate(A) - B conjugate(B)
       = -6250000000000 (zeta^20-zeta^30),

which is nonzero. Thus the conclusion does not depend on floating-point error or the decimal approximations that first suggested it.

## 4. Audit boundaries

A numerical modular-matrix search first located this pair; those floating-point results are discovery evidence only. The proof uses the exact finite certificate above and the cited surgery/modular formulas. No SU(2) counterexample, homotopy-equivalent pair, all-group classification, or optimality/minimality claim is made. The group equality follows from the elementary lens-space construction, not an unproved three-manifold rigidity assertion. The two spaces need not be homeomorphic or homotopy equivalent for the conjecture to apply.

Source and prior-attempt checks found no previous campaign attempt for this ID; the pinned imported report was open triage. A related keyword hit, Kirby3.5, concerns hyperbolic towers and is not a duplicate. Novelty of this particular counterexample has not been established. Independent review must verify source normalization, root/level admissibility, lens surgery words and the cyclotomic computation before a resolution status is adopted.

Actual work used the inherited native runtime without a model or reasoning-setting change; the exact runtime model identifier was not exposed to this worker.
