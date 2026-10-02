# Turn 2: exact arithmetic limits of the four-parameter wheel

Substantive author turn **2/5**, 2026-10-02. The attempt to extend turn 1 to arbitrary determinants produces an exact obstruction for this construction. **No nonexistence result for knots outside this construction is claimed.**

## 1. A four-parameter family and its determinant

In the plane wheel and duality of turn 1, replace each spoke s_i by x_i parallel edges and its paired rim edge r_{−i} by a path of x_i edges. Let (x_0,x_1,x_2,x_3)=(a,b,c,d) be arbitrary positive integers. The four ribbons can be chosen disjoint. Each replacement is exchanged with its dual, so the resulting graph G(a,b,c,d) remains plane self-dual, loopless, bridgeless and without cut vertices, by the same ribbon and vertex-removal arguments as in turn 1. Whenever its spanning-tree number is odd, it gives a prime alternating achiral knot by the credited checkerboard facts.

Define

    F = abcd + ab + ac − bd + cd,
    H = abd + bcd + a+b+c+d = (a+c)(bd+1)+b+d.

Both are positive: F=(ac−1)bd+ab+ac+cd>0. Then

    τ(G(a,b,c,d)) = F²+H².                         (1)

For a direct derivation, give the wheel spokes weights a,b,c,d and its rim edges weights 1/a,1/d,1/c,1/b. The tree-subdivision factors contribute abcd. Thus its reduced weighted Laplacian is

    [a+1/a+1/b   −1/a          0        −1/b]
    [ −1/a      b+1/a+1/d    −1/d         0 ]
    [   0         −1/d       c+1/c+1/d   −1/c]
    [ −1/b          0         −1/c      d+1/b+1/c].

Expanding its determinant and multiplying by abcd gives (1). Equivalently, each of the 45 base trees contributes the monomial ∏ x_i^{1+1_{s_i∈T}−1_{r_{−i}∈T}}; the sum of these monomials is the expansion of F²+H². The supplied exact checker verifies both descriptions independently for a finite grid, while the displayed determinant expansion is an algebraic identity for arbitrary parameters.

## 2. Complete classification on the prime ray 5p²

Let p≡3 mod4 be prime. There exist positive integers a,b,c,d with

    F²+H² = 5p²

if and only if either p=3, p=163, or p is a value at an integer b≥1 of one of

    Q_1(b)=5b²+14b+9,
    Q_2(b)=10b²+18b+8,
    Q_4(b)=20b²+26b+9.                           (2)

The statement is restricted to primes p≡3 mod4; (2) does not assert that any quadratic has infinitely many prime values. In fact Q_1=(b+1)(5b+9) and Q_2=2(b+1)(5b+4) are composite for every b≥1, so only Q_4 can contribute a prime.

**Reduction.** Since −1 is not a square modulo such a prime p, p divides F and H. This follows from Fermat's little theorem if one of F,H were invertible modulo p. Dividing by p² gives two positive squares summing to 5, so (F,H)=(p,2p) or (2p,p). The polynomial pair is unchanged by (a,b,c,d)↦(c,d,a,b), so assume a≤c.

**Case 2F=H.** Its equation is

    (2ac−a−c−2)bd + (2a−1)b + (2c−1)d + (2ac−a−c)=0.       (3)

If a≥2, all terms are nonnegative and some are positive, so there is no solution. For a=1 and c≥3 the same holds. For a=c=1, equation (3) is 2bd=b+d, equivalently (2b−1)(2d−1)=1, giving b=d=1 and p=3. For a=1,c=2 it becomes

    (b−3)(d−1)=4.

The positive solutions are (b,d)=(7,2),(5,3),(4,5), yielding F=27,28,36 respectively. None is prime. This completes the first case.

**Case F=2H.** Its equation is

    (ac−2a−2c−1)bd + (a−2)b + (c−2)d + (ac−2a−2c)=0.       (4)

If a=1 the left side is

    −(c+3)bd−b+(c−2)d−c−2 < 0,

since b≥1. If a=2, equation (4) becomes

    d(c−2−5b)=4.

Hence d is 1,2 or4 and c=5b+2+4/d. Substitution into H gives exactly Q_d(b) in (2). Conversely these positive parameters realize F=2H for every b≥1. Whenever H is prime and 3 modulo4, they supply precisely the corresponding case in the theorem.

It remains to take a≥3. Put A=a−2 and C=c−2, so 1≤A≤C, and q=AC. Equation (4) is

    (q−5)bd + Ab + Cd + q−4=0.                  (5)

For q≥5 it is strictly positive. The possible pairs for q≤4 are therefore (A,C)=(1,1),(1,2),(1,3),(1,4),(2,2). For the first pair the left side is −4bd+b+d−3<0. For the second it is −3bd+b+2d−2≤−d−1<0. The remaining possibilities are:

- (A,C)=(1,3): (2b−3)(2d−1)=1, so (b,d)=(2,1), with H=27
- (A,C)=(1,4): (b−4)(d−1)=4, so (b,d)=(8,2),(6,3),(5,5), with H=163,180,244
- (A,C)=(2,2): (b−2)(d−2)=4, so (b,d)=(3,6),(4,4),(6,3), with H=161,144,161

The only prime among these is 163, which is 3 modulo4 and is realized, for example, by (a,b,c,d)=(3,8,6,2). This proves necessity and sufficiency.

## 3. An infinite missing class for this construction

If p is prime and p≡11 mod12, then p≡3 mod4 and p≡2 mod3. The polynomials Q_1 and Q_2 are composite as observed above. The polynomial Q_4 takes only residues 0 and1 modulo3, since Q_4(b)≡2b(b+1) mod3. Consequently p is in none of (2), and p is neither3 nor163. The complete classification proves

    5p² is not τ(G(a,b,c,d)) for any positive integers a,b,c,d.   (6)

Since gcd(11,12)=1, the classical Dirichlet theorem supplies infinitely many such primes. Credit for that infinitude theorem is Dirichlet's; an English translation of his 1837 paper is [arXiv:0808.1408](https://arxiv.org/abs/0808.1408). No new prime-distribution theorem is claimed. The single example p=11, n=605 already gives a fully elementary obstruction to universal coverage by this construction, without using Dirichlet's theorem. The source explicitly reports that determinants5p² for p≤11 are realizable by other diagrams, so this smallest example particularly clearly cannot be called an original-question counterexample. The further elementary example p=59 gives n=17405.

These n are valid inputs of the original problem: they are odd, exceed49, and equal p²+(2p)². **Equation (6) is not a counterexample to the knot problem.** It excludes only the explicitly defined integer parallel/series wheel family. More general rational tangle replacements, other self-dual graphs, and other prime alternating achiral diagrams remain possible. The original Problem12.25 remains unresolved2/5.

## 4. Relation to prior work

Stoimenow's Claim4.25 already proves failure of a different three-arborescent-tangle pattern on values5p². That result motivated this test and is not claimed as our result. Here the family is specified independently as four paired integer replacements in a wheel, with its own polynomial and a complete prime-ray classification. Whether this particular parametrization and classification have appeared previously has not been certified. The general checkerboard method remains credited prior work.
