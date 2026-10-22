# Turn 1: an exact dyadic obstruction for Du's quintic

Problem 30005278 / OWR-11695860-018. First substantive author turn. **The degree-five existence question remains unresolved.** This turn gives a complete square test for linear elements in the dyadic algebra of the prior candidate f(X)=X^5+2X+1. It yields an infinite class of general quadratic substitutions preserving irreducibility, and identifies exactly where this particular local test stops helping.

The candidate and its previously proved ax²+c case are credited to Lara Du, https://arxiv.org/abs/2409.16206v2 , Theorems 1.5 and 6.2. The Capelli composition criterion is credited through Bober–Du–Fretwell–Kopp–Wooley, Lemma 2.2, https://arxiv.org/abs/2309.15304 . No historical novelty assertion is made for the deductions below. The exact target uses integer substitutions of positive degree at most two and irreducibility in Q[x]; see SOURCE_GATE.md for the primary-source conventions.

## 1. The precise partial theorem

Let a,b,c be integers with a nonzero, and write v_2 for the usual 2-adic valuation, with v_2(0)=+infinity. Then

    v_2(a) <= 2 v_2(b)                                    (1)

implies that f(ax²+bx+c) is irreducible over Q.

In particular this covers every odd a, every b=0 (the credited prior theorem in degree five), and many substitutions with a nonzero linear term. It holds for all c, without a height bound. In the complementary case b nonzero and v_2(a)>2v_2(b), the discriminant of g(x)−theta is actually a square in the entire dyadic algebra Q_2[X]/(f). Thus this local obstruction is exactly exhausted there. Local squareness does not imply squareness in the global root field or reducibility over Q.

All nonconstant linear substitutions preserve the irreducibility of f automatically. No assertion is made that (1) covers every quadratic substitution or proves the source existence question.

## 2. The credited irreducibility and composition inputs

For completeness, the specialized Perron argument proving f irreducible can be written as follows. On the unit circle f has no zero: equality in 2=|z^5+1| would force z^5=1 and z=−1 simultaneously. For epsilon>0, z^5+(2+epsilon)z+1 has exactly one zero inside the unit circle by Rouche's theorem, comparing its linear term with z^5+1. Letting epsilon decrease to zero and using the absence of boundary zeros shows that f also has exactly one root inside and four outside. If monic f factored nontrivially in Z[X], both factors would have constant term of absolute value one, whereas the factor lacking the unique inside root would have constant term of absolute value greater than one. This contradiction proves irreducibility. This is a specialized verification of the prior Perron input, not a new polynomial candidate.

Put K=Q(theta), f(theta)=0. Capelli's criterion says f(g) is reducible over Q exactly when g(x)−theta is reducible over K. For a quadratic g=ax²+bx+c, this is equivalent to

    Delta=4a theta+b²−4ac                                 (2)

being a square in K. We will show nonsquareness by extending scalars to the algebra

    B=K tensor_Q Q_2 = Q_2[X]/(f),
    A=Z_2[X]/(f),

where A is free with basis 1,theta,...,theta^4. B is an algebra, not a degree-five field over Q_2. Its reduction is

    A/2A = F_2[X]/(X^5+1)
         = F_2 x F_16,                                   (3)

because X^5+1=(X+1)(X^4+X^3+X²+X+1), and the quartic is irreducible over F_2 (it has no root in F_2 and is not divisible by X²+X+1, the only irreducible quadratic). The two factors are distinct, so (3) is reduced. Everything below is proved directly in this power basis; no mistaken use of the full splitting field or an unverified integral-basis assertion is needed.

## 3. A complete linear-square criterion in B

**Lemma.** Let M,N be rational 2-adic numbers, not both zero. The element M theta+N is a square in B if and only if N is nonzero and

    v_2(N) is even,
    v_2(M) >= v_2(N)+3,
    2^(−v_2(N)) N == 1 (mod 8).                           (4)

The convention v_2(M)=+infinity is allowed when M=0. Congruences in (4) are in Z_2.

**Coefficient valuation.** For z=sum z_i theta^i in B, define w(z)=min_i v_2(z_i). If z is primitive in A, its nonzero reduction has nonzero square by (3). Therefore w(z²)=0. Scaling by a power of two gives

    w(z²)=2w(z)                                           (5)

for every nonzero z in B. In particular, if z²=M theta+N, then e=min(v_2(M),v_2(N)) is even. Dividing by the square 2^e reduces to M,N integral and primitive, with a primitive square root z in A.

**Primitive necessity modulo four.** Write z=A_0+A_1 theta+...+A_4 theta^4. Modulo two, theta^5=1, so comparison of the coefficients of theta², theta³ and theta^4 in z²=M theta+N gives A_1,A_2,A_4 even. The exact coefficient of theta², using theta^5=−2theta−1, is

    2A_0 A_2 + A_1² −4A_2 A_4 −2A_3² −2A_3 A_4 = 0.

Reducing modulo four forces A_3 even. Primitivity then forces A_0 odd. Consequently M is divisible by four and N is congruent to one modulo four.

**The extra factor of two.** Write z=1+2u in A. Then

    z² = 1+4(u+u²).

Let m=M/4 mod 2 and n=(N−1)/4 mod 2. The element n+m theta must belong to the image of u -> u²+u in (3). Its projection to F_2 must be zero, giving n+m=0. If omega is the image of theta in F_16, then

    Tr_F16/F2(omega)=omega+omega²+omega^4+omega^8=1,
    Tr_F16/F2(1)=0.

Every u²+u has trace zero. The F_16 trace condition therefore gives m=0, and then n=0. Thus in the primitive case M is divisible by eight and N is one modulo eight. Together with (5), this gives precisely the necessity in (4).

**Sufficiency.** After scaling off the square 2^v_2(N), condition (4) writes the element as 1+8h with h in A. The map u -> h−2u² is a strict contraction on the complete 2-adic module A: differences gain at least one factor of two. Its iterates from zero converge to u satisfying u+2u²=h. Then

    (1+4u)²=1+8h.

This supplies a square root in A and proves sufficiency. The criterion is exact, not merely a necessary congruence test. It also handles zero coordinates of B's product decomposition: (5) follows from reducedness, not from B being a field.

## 4. Applying the criterion to every integer quadratic

For b=0, (2) is 4a(theta−c). If c=0, the lemma immediately excludes a square because the constant coefficient is zero. If c is nonzero, (4) would require

    2+v_2(a) >= 2+v_2(a)+v_2(c)+3,

which is impossible for integer c. This recovers Du's degree-five ax²+c conclusion with full credit.

Suppose b is nonzero. Set s=v_2(a), t=v_2(b), and v_2(c)=r>=0, allowing r=+infinity. In (2) the theta coefficient has valuation s+2 and the constant coefficient is N=b²−4ac.

If (2) is a square, (4) gives v_2(N)<=s−1. But 4ac has valuation at least s+2. Hence no cancellation can lower its valuation below s+2, and necessarily v_2(N)=2t. Therefore 2t<=s−1, or s>=2t+1.

Conversely, if s>=2t+1, then

    N=2^(2t) [ (b/2^t)² − 4ac/2^(2t) ],

and the bracket is one modulo eight because its first term is an odd square and the second is divisible by eight. Also s+2>=2t+3. All three conditions in (4) hold. Thus

    Delta is a square in B  <=>  b != 0 and v_2(a)>2v_2(b). (6)

When (1) holds, nonsquareness in B implies nonsquareness in K, and the claimed global irreducibility follows from Capelli. The implication in the opposite direction is deliberately not asserted.

## 5. A concrete check that local squareness is not global reducibility

Take g=2x²+x. It lies in the complementary class of (6), so 1+8theta is a square in B. Nevertheless

    f(g)=32x^10+80x^9+80x^8+40x^7+10x^6+x^5+4x²+2x+1

is irreducible over Q. The accompanying exact checker certifies its degree-ten reduction modulo 11 is irreducible: x^(11^10)=x modulo that polynomial, and the gcd tests for x^(11^5)−x and x^(11²)−x both give one. These are the complete finite-field irreducibility criteria for degree ten; the script implements polynomial arithmetic over F_11 directly. Since the leading coefficient is nonzero modulo 11, the rational conclusion follows.

This individual example only illustrates the gap in the local method. It does not prove all complementary quadratics irreducible, and no claim of a counterexample to the original conjectured candidate is made.

## 6. Reproducibility and next gap

The checker exhausts all coefficient vectors in A/8A for the primitive linear-square implication, tests the trace calculation and coefficient identity, constructs dyadic square roots to stated finite precision in admissible cases, and checks the valuation classification on bounded integer quadratics. The single modulo-11 example has an exact irreducibility certificate. Universal conclusions rest on the preceding proofs, not the bounded counts.

The remaining class is b nonzero and v_2(a)>2v_2(b), with arbitrary integer c. The next turn will investigate global restrictions in this class rather than enlarging a coefficient scan as a substitute for proof.

Author turns completed: 1/5. Original degree-five existence target unresolved. Subjective completion estimate: 15%. Independent full source/proof review is required before any full-target disposition.
