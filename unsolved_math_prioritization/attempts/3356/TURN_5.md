# Turn 5: Frobenius algebra route and final obstruction

2026-10-02. Fifth and final substantive author turn. The original conjecture is **unresolved**. This turn attempted to force irreducibility of a binomial using its special Frobenius action, discriminant and norm invariants. The resulting exact structure theorem explains why the elementary invariants do not close the missing q-primary step. No sixth author search is implied.

## 1. The exact finite algebra

Assume the original hypotheses: q>3 and p=16q^4+1 are both primes. In the reduced finite F_p-algebra

    A=F_p[T]/(T^q-3),

put beta=3^(16q^3) modulo p. Fermat gives beta^q=1. Because p=1 modq,

    T^p=T^(1+16q^4)=T*(T^q)^(16q^3)=beta*T.

Hence Frobenius on the standard basis1,T,...,T^(q-1) is diagonal with eigenvalues1,beta,...,beta^(q-1). As q is prime, exactly two cases occur:

1. beta=1: Frobenius is the identity. Every finite-field factor of the reduced algebra is F_p, so T^q-3 splits completely into q distinct linear factors.
2. beta!=1: beta has exact orderq, so the Frobenius-fixed subspace has dimension1. A reduced finite algebra is a product of finite fields and its fixed subspace has dimension equal to the number of factors. Thus A is a field, and T^q-3 is irreducible over F_p.

Reducedness holds because gcd(T^q-3,qT^(q-1))=1: neither p=q nor p=3. Therefore the original primitive-root conjecture is precisely the assertion that the second case always holds.

This is a complete dichotomy, but it is not a proof selecting the second case. Computing the decisive Frobenius coefficient beta is exactly the prior modular-exponent test; claiming irreducibility from this calculation without excluding beta=1 would be circular.

## 2. Discriminant and determinant do not select a case

The binomial discriminant is

    Disc(T^q-3)=(-1)^(q(q-1)/2)*q^q*3^(q-1).

It is a nonzero square modulo p in every original case. Indeed -1 is a square because p=1 mod4; q-1 is even; and quadratic reciprocity gives

    (q/p)=(p/q)=(1/q)=1.

Thus the discriminant cannot distinguish the irreducible and completely split outcomes. In permutation terms, both an odd-length q-cycle and the identity are even permutations.

Likewise, the determinant of the Frobenius operator is always

    beta^(q(q-1)/2)=1.

The trace is0 in the irreducible case andq in the split case, but this only rewrites the unresolved test: it is the geometric sum1+beta+...+beta^(q-1). The trace of multiplication by T^j is0 for1<=j<q in both cases, and its norm information comes from the same binomial constant term. These elementary norm, discriminant and determinant calculations therefore give identities compatible with both branches; none supplies a missing exclusion.

## 3. An exact control showing the distinction is real

Take the certified original prime case q=17, p=1,336,337. For b=3, the coefficient beta=3^((p-1)/17)=1,267,487 has exact order17. Thus T^17-3 is irreducible. For the neighboring base h=3^17 modulo p, h^((p-1)/17)=1, and T^17-h splits completely; its roots are3*beta^j for0<=j<17.

The two bases3 andh have identical characters of every order dividing16, since17=1 mod16. Both binomials have square discriminant and Frobenius determinant1. The distinction is entirely in the17-primary Frobenius coefficient. verify_turn5.py independently computes powers in the quotient polynomial algebra, checks the17-step Frobenius orbit and explicit split roots, and checks the numerical certificates with exact arithmetic. It is an algebraic falsification control, not a counterexample with base3.

## 4. Exact final remaining statement

A counterexample, if one exists, must have q>100,000,000 by the exact finite certificates. It would be a prime q with p=16q^4+1 prime and

    3^(16q^3)=1 mod p,

or equivalently T^q-3 split completely over F_p. The precise equivalent quartic-phase form is

    3^(4q^3)=-4q^2 mod p if q=1 mod4,
    3^(4q^3)= 4q^2 mod p if q=3 mod4.

Then ord_p(3) is16q,16q^2 or16q^3. All smaller original instances are certified positive. Fixed-q Chebotarev theorems produce compatible bad primes in a larger progression but do not select the single diagonal value16q^4+1. The exact quartic identity controls only the2-part. The neighboring exponent42 counterexample disproves only a broader shortcut. No uniform argument excludes the splitting case at this diagonal prime, and no original counterexample was found.

Final disposition: original unsolved,5/5 substantive author turns consumed. Completion estimate15% of the universal proof goal, uncalibrated and not a probability. The proof collection, finite certificates and failed-route diagnostics require independent scoped review before a final unresolved draft. No full solution, novelty or historical-priority claim is made.
