# Turn 5: character and finite-orbit rigidity on the double-exponential test

## Final substantive outcome

Consider the source-admissible surface

    V_2={z in C^3:exp(exp z_1)+exp(exp z_2)+exp(exp z_3)=0}.

The full source question is not settled for arbitrary entire F by this attempt, even on this test surface. This fifth turn rules out a large family of candidate bounded functions without presenting a failed proof route as a counterexample.

**Theorem A.** Suppose a bounded holomorphic function F on V_2 satisfies

    F(z+2 pi i k)=chi(k)F(z),   k in Z^3,                   (1)

for a multiplicative character chi:Z^3->C*. If chi is nontrivial, F is identically zero. If chi is trivial, F is constant.

**Theorem B.** If F is bounded holomorphic on V_2 and the vector space spanned by all its deck translates is finite-dimensional, then F is constant. In particular every ambient exponential polynomial

    F(z)=sum over finitely many nu of P_nu(z) exp(lambda_nu dot z),

with polynomial coefficients P_nu and arbitrary complex exponent vectors lambda_nu, is constant on V_2 whenever bounded there.

These are scoped obstructions to counterexample constructions. An arbitrary ambient entire function need not have the stated automorphy or finite-dimensional orbit. The original arbitrary-triple problem remains unresolved after five substantive turns. No sixth author search is proposed.

## 1. The quotient surface and its coordinate divisors

Let

    Y={u in C^3:exp u_1+exp u_2+exp u_3=0},
    Y^*=Y intersect (C*)^3.

The coordinate exponential map E:V_2->Y^* is a surjective unramified holomorphic cover, with Z^3 acting by the translations in (1), transitively on every fiber. The surface Y is smooth since each exp u_j is nonzero.

There is a biholomorphism Y=S x C, where S={exp a+exp b=1}, given by

    u_1=a+t+pi i,  u_2=b+t+pi i,  u_3=t.                    (2)

The equality follows from exp(pi i)=-1. The inverse is a=u_1-u_3-pi i, b=u_2-u_3-pi i, t=u_3. The credited Demailly–Wakabayashi theorem says S is Liouville. Consequently Y is Liouville: a bounded holomorphic function is first constant along each entire t-line, then constant on S.

The coordinate divisors D_j={u_j=0} in Y are smooth. At a point of D_j, one of the other coordinates can be eliminated holomorphically using its nonzero exponential derivative. At an intersection of two D_j, their two coordinate functions are local coordinates on Y, since the derivative in the third coordinate remains nonzero. No triple intersection exists: exp 0+exp 0+exp 0=3. Thus their union has only simple normal crossings.

For completeness the connectedness of this particular covering can be checked without the general separated-sum irreducibility input. The surface S is connected: it is the exponential pullback of C minus {0,1}, whose two basic puncture loops have independent winding vectors, so its logarithmic cover has one component. Hence Y and its complement Y^* of analytic divisors are connected. For each j, D_j has a point on neither other divisor, for example by permuting (0,log 2,log 3+pi i). A small transverse meridian there has winding vector e_j in (C*)^3. Thus pi_1(Y^*) surjects onto Z^3, and the exponential pullback V_2 is connected. The proof of Theorem A below in fact uses transitivity on each fiber directly, not an unproved connectedness assertion.

## 2. A bounded eigenfunction has a unitary character

If F is not identically zero, choose z with F(z)!=0. For each coordinate generator e_j and every integer n, boundedness and (1) imply

    |chi(e_j)|^n |F(z)| <= ||F||_infinity.

Using both positive and negative n gives |chi(e_j)|=1. Thus there are uniquely chosen real numbers

    0<=alpha_j<1,   chi(e_j)=exp(2 pi i alpha_j).             (3)

No nonunitary character supports a nonzero bounded F. This step does not assume that the entire deck representation decomposes into such characters; it concerns only a function satisfying (1).

## 3. Descent and subunit removable singularities

For u in Y^*, choose any logarithms z with exp z_j=u_j and define

    H(u)=exp(-sum_j alpha_j z_j) F(z).                       (4)

Equations (1) and (3) make (4) independent of the logarithm choices. Local inverse branches show that H is holomorphic on Y^*. If ||F||_infinity<=M, then

    |H(u)| <= M product_j |u_j|^(-alpha_j).                 (5)

The exponents are strictly less than one. This implies that H extends holomorphically across all D_j, including their pairwise intersections.

Here are the local details. Near a point on just one divisor, take a local coordinate s=u_j transverse to it; all other |u_i| are bounded away from zero. Then |H|<=C|s|^(-alpha_j). The Laurent coefficient of s^{-m}, m>=1, is bounded by C r^{m-alpha_j} on a circle of radius r. As r tends to zero this tends to zero, so all negative coefficients vanish. The same estimate uniformly on smaller parameter discs supplies joint holomorphic extension. At a crossing, use coordinates s=u_i, t=u_j. The bound is C|s|^(-alpha_i)|t|^(-alpha_j). The two-variable Laurent expansion has no negative s or t coefficients, by integrating successively and using m-alpha_i>0 and n-alpha_j>0. This yields extension across the crossing. Local uniqueness makes all extensions agree.

The resulting H is holomorphic on the whole smooth surface Y. We do not assert it is bounded near the divisors merely from the original inequality; removability was proved with the precise subunit exponents. When every alpha_j=0 it is bounded there by continuity, as used below.

## 4. Entire common-translation lines force the character to disappear

Fix (a,b) in S and use (2). The function

    h_{a,b}(t)=H(a+t+pi i,b+t+pi i,t)

is entire on C, including the finitely many t for which one of the coordinates is zero. Away from those points, (5) gives

    |h_{a,b}(t)| <= M |t+a+pi i|^(-alpha_1)
                          |t+b+pi i|^(-alpha_2)|t|^(-alpha_3).   (6)

Put A=alpha_1+alpha_2+alpha_3. For sufficiently large |t|, each translated factor has magnitude at least |t|/2. Hence

    |h_{a,b}(t)| <= M 2^A |t|^(-A).                         (7)

If the character is nontrivial, at least one alpha_j is positive and A>0. The entire function h_{a,b} is bounded on the outside of a disc and tends to zero there. It is also bounded on the closed disc, so Liouville gives h_{a,b}=0. This holds for every (a,b), hence H=0 on Y and F=0 on V_2.

If the character is trivial, all alpha_j=0. Then H is bounded by M on dense Y^* and therefore on all of Y. The Liouville property of Y=S x C established in Section 1 makes H constant, so F is constant. This proves Theorem A.

The whole argument treats irrational unitary characters as well as finite-order ones. It does not rely on passing to a finite cover to clear the alpha_j.

## 5. Finite-dimensional translation orbits

Let E be the finite-dimensional vector space generated by the deck translates of a bounded F. Every element of E is bounded holomorphic on V_2, and the supremum norm is a norm on E. The three deck generators induce commuting invertible isometries T_1,T_2,T_3 of E, since each translation is a bijection of V_2.

For a finite-dimensional invertible isometry, every eigenvalue has modulus one, using bounded positive and negative powers. No nontrivial Jordan block can occur: its positive powers contain nonconstant polynomial-in-n entries and cannot remain uniformly bounded. Thus each T_j is diagonalizable. Commuting diagonalizable complex linear operators are simultaneously diagonalizable; one obtains this by decomposing into the eigenspaces of the first operator, all preserved by the others, and continuing.

Every vector in a simultaneous eigenbasis is therefore a bounded holomorphic function satisfying (1) for a unitary character. Theorem A makes it constant, and excludes all nontrivial characters. Consequently E consists of constant functions and F is constant. This proves Theorem B.

For an ambient exponential polynomial, every translation preserves the finite span of the functions z^beta exp(lambda_nu dot z) with beta bounded coordinatewise by the finitely many polynomial degrees. Restriction to V_2 preserves finite-dimensionality. Therefore Theorem B applies exactly as stated, including polynomial prefactors and repeated exponent vectors.

## 6. Why this is not a full Liouville proof

An infinite-dimensional isometric action of an abelian group need not be spanned by character eigenvectors. A simple abstract obstruction is the bilateral shift on c_0(Z). It is an invertible isometry and has no nonzero eigenvector with a unit-modulus eigenvalue: such an eigenvector would have constant nonzero modulus along all integer indices and could not tend to zero. Nevertheless the representation is nonzero, and the translates of delta_0 have pairwise supremum distance one.

This sequence-space example is not a bounded holomorphic function on V_2 and is not a counterexample to the original question. It shows the precise missing functional-analytic implication. Normal-family compactness in the compact-open topology does not supply precompactness in the global supremum norm, nor a finite-dimensional deck orbit. No such implication is used or claimed.

The final attempt therefore leaves two explicit gaps: a general source triple need not have any of the finite/abelian/virtually-nilpotent structures proved in earlier turns; and even on the natural triple-double-exponential test, arbitrary bounded entire restrictions may have an infinite-dimensional deck orbit outside Theorem B. No actual bounded nonconstant ambient entire F has been constructed.

## Final status

Five genuine author turns are complete. The original arbitrary-entire question is **unresolved, 5/5**. The packet preserves the exact polynomial-pullback equivalence, the one-input positive theorem, the monodromy criterion, and the double-exponential character/finite-orbit rigidity. Classical results are credited, including Demailly–Wakabayashi, Lin and Rubel–Squires–Taylor. The latter's theorem statement was checked in primary sources, but its original full Annals proof remains unretrieved and that dependency qualification is retained. No novelty certification is made.

The exact controls verify the translation parametrization, the subunit exponent inequalities, finite-dimensional Jordan-power identities and algebraic finite-orbit assertions on representative families. They are finite algebra checks, not a proof of the analytic source question.
