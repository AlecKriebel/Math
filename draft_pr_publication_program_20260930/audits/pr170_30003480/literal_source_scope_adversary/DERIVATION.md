# Independent derivation for the literal binary target

This derivation is a separate reconstruction from the permitted candidate claims and the primary source definitions. It supplies checkable proof steps; finite arithmetic checks are supplementary.

## Closed-ball necessity and exact three-factor image

Write s=||T||_F^2. A nonzero real tensor in the closed unit ball has0<s<=1. Every mode Gram matrix is positive semidefinite with trace s and determinant d_i, so d_i<=s^2/4 and its smaller eigenvalue is

    a_s(d_i)=(s-sqrt(s^2-4d_i))/2.

The HSS polygon theorem applied to T/sqrt(s) gives a_s(d_i)<=sum_(j!=i)a_s(d_j). Its necessity can also be seen directly: Schmidt-decompose the first factor with probabilities a<=1/2 and1-a and orthonormal remainder vectors u,v. Let N be the sum of the other factors' smaller-eigenvector projectors and w their product larger-eigenvector. Then N>=I-|w><w|. Bessel's inequality gives p+q<=1 for p=|<w,u>|^2, q=|<w,v>|^2, hence

    sum_(j>=2)lambda_j >= a(1-p)+(1-a)(1-q)
                              >= a(2-p-q) >= a=lambda_1.

Define lambda(d)=a_1(d). If lambda(d_i)>sum_(j!=i)lambda(d_j), then d_i>0 and d_i>d_j for all j!=i. For positive d_j<d_i and s>2sqrt(d_i), rationalization of a_s gives

    d/ds log a_s(d)=-1/sqrt(s^2-4d),
    d/ds log(a_s(d_j)/a_s(d_i))
        =1/sqrt(s^2-4d_i)-1/sqrt(s^2-4d_j)>0.

Thus each ratio is nondecreasing up to s=1; a zero d_j has constant zero ratio, and the minimum-s endpoint follows by continuity. The sum of ratios is<1 at s=1 and therefore at every allowed s<=1. That contradicts the HSS necessity at the tensor's actual s. The zero tensor has all d_i=0 and satisfies the condition. Consequently every closed-ball tensor obeys the s=1 polygon inequalities.

For n=3, given t_i=lambda(d_i) in[0,1/2] with t_i<=t_j+t_k, set

    w0=1-(t1+t2+t3)/2,
    w1=(t2+t3-t1)/2,
    w2=(t1+t3-t2)/2,
    w3=(t1+t2-t3)/2.

These weights are nonnegative, sum to1, and w0>=1/4. The real even-parity tensor with coefficients sqrt(w0),sqrt(w1),sqrt(w2),sqrt(w3) at000,011,101,110 has zero off-diagonal mode Gram entries: opposite rows cannot share a column on even-parity support. Its smaller diagonal entries are w2+w3=t1, w1+w3=t2, w1+w2=t3. It has norm1 and determinants t_i(1-t_i). This is the bit-flipped real construction in HSS equations13–20.

Therefore the exact G3 is the inverse image of the triangle region under the coordinate map d_i=t_i(1-t_i), including all boundary cases. For example, t=(0,0,0), (0,1/2,1/2), and(1/2,1/2,1/2) are realized by the same construction.

## Arbitrary-polynomial obstruction

Assume G3={d in C3:P(d)>=0} for a real polynomial P. On D=(0,1/2)^3 define

    F(t)=P(t1(1-t1),t2(1-t2),t3(1-t3)).

The coordinate map is a diffeomorphism from D to the open determinant cube. The polynomial F satisfies F(1-t1,t2,t3)=F(t1,t2,t3). It is nonzero because some open-cube points violate the triangle inequalities and must have F<0.

Let L=t1-t2-t3. On the open plane patch t2,t3>0 and t2+t3<1/2, the other two triangle inequalities are strict. One side L<0 is feasible, the other L>0 is infeasible. Continuity forces F=0 on that patch. In coordinates(L,t2,t3), the constant term of F in L vanishes on an open set in the two free variables, so it is the zero polynomial. Hence L divides F.

Let m>=1 be its exact multiplicity, F=L^m R, with R not divisible by L. The restriction R|_(L=0) is nonzero as a polynomial. It cannot vanish throughout the open patch. At a point where it is nonzero, R keeps its sign in a neighborhood. The required opposite signs of F on the two sides force m odd; the allowed feasible zeros do not alter this argument.

The affine involution t1->1-t1 carries L to-(t1+t2+t3-1). Since F is invariant, L'=t1+t2+t3-1 has the same exact multiplicity m. The plane L'=0 has an open patch near(1/3,1/3,1/3) in D, with all triangle inequalities strict: since sum t_i=1 and t_i<1/2, t_i<1-t_i. Thus F>=0 on a full neighborhood of that patch. Its exact residual factor after dividing by(L')^m is nonzero at some point in the patch, by the same polynomial restriction argument. If m were odd, F would change sign across this interior plane and be negative somewhere feasible. Hence m must be even, contradicting the earlier odd multiplicity.

This proof treats arbitrary real coefficients and arbitrary degree. It relies on exact polynomial divisibility and symmetry, not on sampled polynomials or a particular defining equation.

## Why the same contradiction applies inside H3

At the first plane patch put t1=b+c,t2=b,t3=c with b,c>0,b+c<1/2. For d_i=t_i(1-t_i), the determinant-polygon slacks are

    d2+d3-d1=2bc,
    d1+d3-d2=2c(1-b-c),
    d1+d2-d3=2b(1-b-c).

All are strictly positive and all coordinates lie strictly between0 and1/4. At the reflected plane sum t_i=1, the slack sum_(j!=i)d_j-d_i=2t_jt_k is strictly positive. Both patches have full neighborhoods inside H3. Consequently both local crossings used above remain available when the proposed definition is only required within H3.

## Exact zero-coordinate slice

For real tensors, det(M_i M_i^T)=0 implies rank(M_i)<=1 because the Gram matrix is positive semidefinite. A nonzero tensor therefore factors as S tensor u in that mode. Normalize u to length1 by absorbing its nonzero norm into S. The resulting S has the same Frobenius norm as T; for every remaining mode, the contracted unit factor leaves its Gram matrix unchanged. Repeating for zero modes4,...,n gives

    Gn intersect {d4=...=dn=0}=G3 x{0}^{n-3}.

The zero tensor is included; the converse follows by adjoining real unit vectors. Also

    Cn intersect this face=C3 x{0}^{n-3},
    Hn intersect this face=H3 x{0}^{n-3}.

If P_n defined Gn within either allowed domain, P_n(d1,d2,d3,0,...,0) would define G3 in the corresponding three-factor domain. A zero restriction would wrongly include the entire domain slice, so it cannot evade the contradiction. This proves the impossibility for every n>=3. For n=2, inside the source cube, the diagonal segment is defined by-(d1-d2)^2>=0; the source Definition1.2 begins at n=2. The candidate's n=1 remark is a harmless extension of the determinant convention.

## Exact positive n=4 counterexample

Take d=(2401/10000,81/625,81/625,1/10000). Its exact nonnegative roots are(49,36,36,1)/100. Its four determinant-polygon slacks are

    (12/625,1201/5000,1201/5000,312/625).

All are positive; every determinant is in(0,1/4). Thus

    Q1=(12/625)(1201/5000)^2(312/625)
      =168760917/305175781250.

In lexicographic sign order(-1 before+1), all16 signed-root factors are

    -61/50,-6/5,-1/2,-12/25,-1/2,-12/25,11/50,6/25,
    -6/25,-11/50,12/25,1/2,12/25,1/2,6/5,61/50.

Equivalently, pair global-sign partners to obtain

    Q2=(1/2)[(61/50)(6/5)(1/2)(12/25)(1/2)(12/25)(11/50)(6/25)]^2
      =23632249608/2384185791015625.

Hence Q1-Q2=2589624828909/4768371582031250>0. No factor was omitted and no radical approximation enters the calculation.

Nevertheless d1-(2/5)(3/5)=1/10000>0, while(1/6)(5/6)-d2=209/22500>0, the same holds for d3, and(1/100)(99/100)-d4=49/5000>0. Since t->t(1-t) is strictly increasing on[0,1/2],

    lambda(d1)>2/5,
    lambda(d2)+lambda(d3)+lambda(d4)<1/3+1/100=103/300<2/5.

The closed-ball necessity excludes the tuple. This is a strictly positive counterexample to the literal Conjecture1.5, separate from the all-polynomial impossibility.

## GHZ and the displayed Theorem1.4

For(|000>+|111>)/sqrt2, each Gram matrix is diag(1/2,1/2), hence each determinant1/4. Q1=1/64. The eight signed-root sums are-3/2, three copies of-1/2, three copies of1/2,3/2; their product times1/2 is9/512. The printed first region fails. Each secondary pair expression(di-dj)^2+(di+dj)/2=1/4 exceeds3/16, so the printed second region also fails. This check concerns the displayed theorem, which is unnecessary in the argument above.

## Reproduction and evidential limit

The private independent_checks.py uses only Python's fractions, itertools, math and json modules. Its assertions cover the exact n=4 product, threshold exclusions, parity-support diagonal entries, representative zero/maximal boundary cases and both required strict-H3 patches. The exact products and written proof here are sufficient for manual reproduction; the finite checker output is not substituted for the universal proof.
