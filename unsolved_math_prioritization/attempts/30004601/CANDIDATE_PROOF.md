# A seven-hyperplane candidate counterexample to the generic-initial degree bound

**Status:** complete candidate found in recovered substantive turn 1; independent adversarial review pending. No correctness, novelty, priority, or publication claim is made before that review.

## 1. Exact target and example

Work over a field K of characteristic zero. The original conjecture uses degree-reverse-lexicographic generic initial ideals with the variables ordered x1 > x2 > x3 > x4. If B=rgin(J(A)) and

    p = min{d : x2^d belongs to B},

the proposed bound is that every minimal generator involving x3 has degree at least p. This is OWR Report 5/2021, printed p.234, Conjecture 7, and Bigatti-Palezzato-Torielli Conjecture 5.7 after shifting their reduction-number notation by one. The imported record's x1 in place of x2 is a transcription error; that easier literal statement is not the target settled here.

Consider the essential central arrangement in K^4 defined by

    Q = x y (x-y) (x-2y) z w (x+z+w).

Its seven factors are distinct, and the four coordinate hyperplanes make it essential. Put

    J = (Q_x, Q_y, Q_z, Q_w).

This is the arrangement Jacobian ideal: Euler's identity puts Q in J because 7 is invertible. The four displayed generators have degree 6.

**Candidate theorem.** For this arrangement, p=8 and B has a minimal generator of degree 7 divisible by x3. In fact one such generator uses only x1,x2,x3. Thus the corrected conjecture is false in four variables.

The proof below determines generic section dimensions algebraically. One exact rational flag is also checked for reproducibility, but genericity is not inferred from favorable numerical samples.

## 2. Linear polar syzygies after a generic section

Let C:K^r -> K^4 be an injective linear map, with r=2 or 3, and write X,Y,Z,W for the restrictions of x,y,z,w. Assume the following open conditions:

1. X,Y are linearly independent
2. the seven forms X,Y,X-Y,X-2Y,Z,W,X+Z+W are nonzero and pairwise nonproportional
3. when r=3, X,Z,W are linearly independent

These conditions define nonempty open sets. An explicit compatible flag is

    r=3: (x,y,z,w) = (s,t,u,s+2t+3u),
    r=2: u=2s+3t,

so the binary forms are X=s, Y=t, Z=2s+3t, W=7s+11t, and X+Z+W=10s+14t. They satisfy all the conditions.

Let f_x,f_y,f_z,f_w be the restrictions of the four *ambient* partial derivatives. They are not being identified with the three partial derivatives of Q restricted to a three-dimensional space.

For linear forms u_x,u_y,u_z,u_w in the r section variables, write

    U_i = a_ix u_x + a_iy u_y + a_iz u_z + a_iw u_w,

where a_i is the coefficient row of the i-th original factor and L_i is its restriction. Then

    u_x f_x + u_y f_y + u_z f_z + u_w f_w
      = sum_i U_i product_{j != i} L_j.

Reducing a zero relation modulo L_i shows that L_i divides U_i: the quotient by L_i is a domain and none of the other L_j vanishes there. Since U_i is linear, U_i=lambda_i L_i for a scalar lambda_i. Conversely, these proportionalities make the displayed sum equal to (sum_i lambda_i) product_j L_j. Therefore the linear syzygies are exactly the tuples satisfying

    U_i = lambda_i L_i for all i, and sum_i lambda_i=0.    (1)

The same reduction with constant u's shows that the four polars are linearly independent: all a_i dot u vanish, and the coordinate-factor rows force u=0. Thus they are four minimal degree-6 generators of each section ideal.

## 3. The three-dimensional section has no linear syzygies

The factors X,Y,X-Y already force their three scalars in (1) to coincide, because X,Y are independent. The factor X-2Y has the same scalar. Call it a. The factors Z,W and X+Z+W have scalars b,c,d, respectively. Consequently

    u_x=aX, u_y=aY, u_z=bZ, u_w=cW,
    (a-d)X+(b-d)Z+(c-d)W=0,
    4a+b+c+d=0.                                        (2)

For r=3, independence of X,Z,W forces a=b=c=d. The last equation is then 7a=0, so every scalar and every u is zero.

Write H3(k) for the quotient Hilbert function of a generic three-dimensional section of S/J. There are four independent generators in degree 6 and no relations with linear coefficients. Hence

    H3(5) = 21,
    H3(6) = binom(8,2)-4 = 24,
    H3(7) = binom(9,2)-3*4 = 24.                         (3)

These values hold on the stated nonempty open set, so they are the generic values.

## 4. The two-dimensional section has one linear syzygy

For r=2, the three nonproportional forms X,Z,W span a two-dimensional space and have a one-dimensional relation space. Let

    rho_x X + rho_z Z + rho_w W = 0

be a nonzero relation. All solutions of the middle equation in (2) have

    a=d+t rho_x, b=d+t rho_z, c=d+t rho_w.

The trace condition is

    7d+t(4rho_x+rho_z+rho_w)=0.

It cuts this two-parameter solution space down to dimension exactly one, since 7 is nonzero. The map from these parameters to the syzygy coefficients is injective: if u_x,u_y,u_z,u_w are all zero, then a=b=c=0, and the nonzero form X+Z+W also forces d=0.

Thus the binary ideal I2 has four minimal generators of degree 6 and exactly one independent linear syzygy. It has no nonconstant common factor. To see this after extending K to its algebraic closure, suppose that all four polars vanish at a projective binary point. The restricted Euler identity forces the product of the seven L_i to vanish. Pairwise nonproportionality means exactly one L_i vanishes there. At that point the vector of ambient polars is the nonzero product of the other six forms times the nonzero coefficient vector a_i, a contradiction.

The binary ideal consequently has height 2. By the graded Hilbert-Burch theorem its syzygy module is free of rank 3. Write the three positive coefficient degrees as a1,a2,a3. The Hilbert numerator is

    1 - 4 t^6 + t^(6+a1) + t^(6+a2) + t^(6+a3).

Because the quotient is Artinian, the numerator has a double zero at 1; differentiating gives a1+a2+a3=6. Exactly one independent linear syzygy means exactly one ai is 1 and the other two are at least 2. Therefore the degrees are exactly 1,2,3, and

    HS(K[s,t]/I2) = (1 - 4t^6 + t^7 + t^8 + t^9)/(1-t)^2.

In particular the generic binary Hilbert values are

    H2(6)=3, H2(7)=1, H2(8)=0.                          (4)

This proves the needed upper as well as lower rank bounds for generic flags; no semicontinuity direction is being reversed.

## 5. Translate the sectional ranks to the generic initial ideal

We use the classical generic-sectional-matrix identity for reverse lexicographic generic initial ideals:

    Hi(k) = dim_K (K[x1,...,xi]/(B intersect K[x1,...,xi]))_k.

This is Bigatti-Palezzato-Torielli Theorem 6.2, citing the standard generic-section result. In characteristic zero B is strongly stable.

First, a nonzero standard binary monomial of degree k exists if and only if x2^k is standard. Indeed if x2^k belonged to B, strong stability would put every degree-k binary monomial in B. Equation (4) therefore gives x2^7 not in B and x2^8 in B, so p=8.

Now put B3=B intersect K[x1,x2,x3] and A3=K[x1,x2,x3]/B3. The cokernel of multiplication by x3 from degree k-1 to degree k is the binary quotient in degree k. Thus

    dim ker(x3 : (A3)_(k-1) -> (A3)_k)
       = H3(k-1)-H3(k)+H2(k).

At k=6 this is 21-24+3=0. Since J and B have no elements below degree 6, there is no minimal generator involving x3 in degree at most 6. At k=7 it is 24-24+1=1.

Hence some standard monomial m of degree 6 has x3*m in B3. A minimal generator t dividing x3*m must involve x3; otherwise it would divide m. Such a generator cannot have degree at most 6 by the preceding paragraph, so it has degree exactly 7. It is also minimal in B, since divisors of a monomial using only x1,x2,x3 cannot involve x4.

We have obtained degree(t)=7 < 8=p, proving the candidate theorem.

## 6. Exact flag check

The supplementary program candidate_rank_check.py differentiates the seven-factor polynomial over Q *before* restriction and constructs homogeneous Macaulay matrices. It uses only the installed SymPy package and independently authored code. No downloaded external program is run.

For w=x+2y+3z and then z=2x+3y, the ranks are:

- three variables, degree6: 4 of28 columns; quotient dimension24
- three variables, degree7: 12 of36 columns; quotient dimension24
- binary, degree6: 4 of7 columns; quotient dimension3
- binary, degree7: 7 of8 columns; quotient dimension1
- binary, degree8: 9 of9 columns; quotient dimension0

The binary syzygy is explicitly

    11x f_x + 11y f_y - 73(2x+3y) f_z + 25(7x+11y) f_w = 0.

For this flag, X-11Z+3W=0 and the factor scalars are (a,b,c,d)=(11,-73,25,4), with4a+b+c+d=0. The numerical rank check is corroboration of the general proof, not its source of genericity.

## 7. Scope and attribution

The original three-variable arrangement case is already proved by Marchesi-Palezzato-Torielli, Theorem4.7. This counterexample is four-dimensional. Its generic three-variable section has four independent degree-6 ambient polars, so it is not the three-generated Jacobian ideal of the restricted plane arrangement. The result therefore does not contradict their theorem.

OWR Theorem10 also relates that known three-variable case to the3-WLP formulation in adjacent dataset record30004602. That related result is not a separate discovery of this attempt.

No claim of minimality of the seven-hyperplane example, historical priority, or novelty is made. The Hilbert-Burch theorem, Galligo strong stability, and generic-section/sectional-matrix identities are classical inputs and are credited. The new candidate contribution is this explicit arrangement and the scalar-syzygy obstruction to the proposed bound.

## Primary sources

- OWR Report5/2021, printed pp.233-235; Conjecture7 uses x2, not the imported x1: https://ems.press/content/serial-article-files/46883
- Bigatti-Palezzato-Torielli, *New characterizations of freeness for hyperplane arrangements*, Journal of Algebraic Combinatorics51(2020),297-315; Conjecture5.7 and Theorem6.2: https://arxiv.org/pdf/1801.09868
- Marchesi-Palezzato-Torielli, *Lefschetz properties and the Jacobian algebra of3-dimensional hyperplane arrangements*, DOI10.4171/PM/2155, Conjecture4.6, Corollary3.8, Theorem4.7: https://ems.press/content/serial-article-files/51900
