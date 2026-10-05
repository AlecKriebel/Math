# Proofs and exact scope

All geometric statements in Sections 1-7 are over C unless another field is explicitly named. An integral curve means reduced and irreducible. Standard background used below comprises intersection theory on the blowup of a smooth surface at distinct points, Bezout's theorem, adjunction for an integral Cartier curve on a smooth surface, and the explicitly cited weak bounded negativity theorem.

## 1. Intersection notation and the resolved pencil

Write H for the pullback of a projective line, and E_ab for the exceptional curve at [1:epsilon^a:epsilon^b]. Then H^2=1, H.E_ab=0, E_ab.E_cd=0 for distinct centers, and E_ab^2=-1. The canonical class is K=-3H+sum E_ab. Every integral curve is either exceptional or the strict transform of an integral plane curve Gamma, of degree d>=1, with multiplicities a_ab>=0 at the centers. Thus

C = dH - sum a_ab E_ab,
C^2 = d^2 - sum a_ab^2,
K.C = -3d + sum a_ab,
2p_a(C)-2 = d^2 - sum a_ab^2 - 3d + sum a_ab.

The two degree-m forms A=x_1^m-x_0^m and B=x_2^m-x_0^m have common zero set exactly Z_m. On x_0=1 their differentials m*x_1^(m-1) dx_1 and m*x_2^(m-1) dx_2 are independent at every common zero. Hence each base point is simple and transverse. Blowing up once resolves the pencil [A:B], with no infinitely near base points. Its fiber class is

F=mH-sum E_ab; F^2=0; F.E_ab=1.

The local map on each exceptional P^1 is the isomorphism given by the two independent linear terms, so every E_ab is a section, not a fiber component. Since F is the class of a fiber of a morphism to P^1, it is nef. Consequently every nonexceptional integral curve satisfies

h := F.C = md-sum a_ab >= 0.

The number h is the degree of the map from the normalization of a horizontal curve to P^1, and is positive for horizontal curves. Substituting in adjunction gives the exact identity

C^2 = 2p_a(C)-2 -(m-3)d + h.                         (1)

In particular the elementary lower bound C^2 >= (3-m)d+h-2 depends on d when m>3. It is not the requested bound depending only on m.

## 2. Vertical curves, line incidences, and order dependence

For m>=2 a member of the pencil has equation

u x_1^m + v x_2^m -(u+v)x_0^m = 0.

If u,v,u+v are nonzero, its three partial derivatives cannot vanish at a projective point. It is smooth; it is also irreducible, since distinct positive-degree components of a projective plane curve intersect and make the curve singular. Blowing up its smooth marked points preserves smoothness and irreducibility, and its strict transform has square 0.

If one of u,v,u+v vanishes, the member factors into m distinct lines. These are the three families

x_1=epsilon^a x_0,  x_2=epsilon^b x_0,  x_2=epsilon^c x_1.

Each such line contains exactly m centers, with multiplicity one, so its strict transform has square 1-m. Lines in one family meet at one coordinate vertex, which is not a center. Each exceptional divisor maps isomorphically to the base, so these are all fiber components. This proves the vertical classification.

An arbitrary projective line contains at most m points of Z_m when m>=2. Indeed, lines with a zero coefficient in their equation either belong to one of the three displayed families or contain no center. For a line with all three coefficients nonzero, in coordinates [1:z:w] its equation is alpha+beta*z+gamma*w=0. A center has |z|=|w|=1. The condition |alpha+beta*z|=|gamma| cuts the unit circle in at most two points: after squaring, it is a nonconstant real linear equation in Re(z),Im(z), because alpha and beta are nonzero. Each z determines at most one w. Thus every other line contains at most two centers. Its strict-transform square is at least -1. In particular the smallest line square is 1-m for m>=2.

It follows that any existing signed optimal lower bound satisfies b(X_m)<=1-m for m>=2. No bound independent of m is possible. This observation alone does not disprove boundedness on any fixed X_m.

## 3. Small orders and the anticanonical obstruction

For m=1, a nonexceptional curve has degree d and one multiplicity a<=d, so its square is d^2-a^2>=0. An exceptional curve has square -1; hence b(X_1)=-1.

For m=2, consider an integral nonexceptional curve of degree d>=2. It is distinct from every arrangement line. Bezout applied to the two lines in the first family gives sum a_ab<=2d. Adjunction therefore gives C^2>=-2+3d-sum a_ab>=d-2>=0. For d=1, the line-incidence argument above gives C^2>=-1. Exceptional curves attain -1. Therefore b(X_2)=-1.

For m=3, K=-F. Adjunction and nefness yield C^2=2p_a(C)-2+F.C>=-2 for every integral curve, including the exceptional ones. The arrangement lines attain -2. Therefore b(X_3)=-2. No assertion that the exceptional curves are the only (-1)-curves is used or needed.

For m>3 one has (-K).F=m(3-m)<0. Since F is nef, an effective divisor has nonnegative intersection with F. Thus no positive multiple of -K is effective; indeed -K is not pseudoeffective. This proves precisely why the effective-anticanonical argument cannot simply be extended to these orders.

## 4. Symmetry, averaging, and a misleading numerical cone

Suppose a nonexceptional integral curve has a_ab=r at every center. Nefness of F gives md-m^2*r>=0, hence d>=mr. Consequently C^2=d^2-m^2*r^2>=0. In particular this covers every nonexceptional curve invariant under the diagonal group mu_m x mu_m, since that group acts transitively on Z_m and preserves local multiplicities. The same conclusion holds whenever the multiplicity vector is constant, without an invariance assumption.

This does not reduce the target to symmetric curves. If S=sum a_ab and the class is averaged under that group, the averaged class has every multiplicity S/m^2 and square d^2-S^2/m^2. Its square minus the original square equals

sum (a_ab-S/m^2)^2 >=0.

Thus averaging can erase precisely the variance producing negativity. Likewise S<=md and Cauchy-Schwarz give the lower estimate sum a_ab^2>=S^2/m^2, not the upper estimate needed to conclude C^2>=0.

Here is an explicit stronger control on X_4. Index its centers by a,b in {0,1,2,3}. Let v be zero except

v_00=v_21=v_12=1, and v_10=v_01=v_22=-1.

Every row sum, column sum, and cyclic diagonal sum for b-a modulo 4 is zero; sum v=0 and sum v^2=6. For every integer k>=1 set

t=2k^2, d=8k^2+1, a_ab=t+2k*v_ab,
D_k=dH-sum a_ab E_ab.

All a_ab are nonnegative. Direct calculation gives

sum a_ab=32k^2,
sum a_ab^2=64k^4+24k^2,
F.D_k=4,
D_k^2=1-8k^2,
K.D_k=8k^2-3,
1+(D_k^2+K.D_k)/2=0.                              (2)

The sums on each of the 12 arrangement lines are 4t=8k^2<d. Every other line contains at most two centers, and its sum is at most 2(t+2k)=4k^2+4k<=8k^2+1=d. The last inequality is equivalent to (2k-1)^2>=0. Thus the family passes Bezout against **every line**, nonnegative multiplicities, nef-fiber testing, and the nonnegative arithmetic-genus requirement. Its squares nevertheless tend to minus infinity.

These are numerical divisor classes, not constructed curves. In fact none has an integral representative, as the next section establishes. Equations (2) are a counterexample only to the sufficiency of the listed numerical tests.

## 5. Exact nonrealizability controls and a known genus bound

We use Hao's weak bounded negativity result, in the following cited form: for a smooth complex projective surface X with h^0(-K_X)=0 and an integral curve of geometric genus g, its square is at least

min{K_X^2+chi(O_X)-3, K_X^2-3c_2(X)+2-2g}.

This is the combination of Lemma 2.2.1 and Theorem 2.2.7 in arXiv:1708.09463v1. The claim is a literature input, not a new proof of the logarithmic Miyaoka-Yau inequality. Later Misra-Ray work restates the genus-bounded theorem. For X_m with m>=4, Section 3 gives h^0(-K)=0, while K^2=9-m^2, chi(O)=1, and c_2=3+m^2. Substitution yields

C^2 >= 2-4m^2-2g.                                (3)

The other term in the minimum is 7-m^2 and is always larger for m>=4 and g>=0. In particular all rational integral curves on X_m have square at least 2-4m^2. Any sequence contradicting bounded negativity over C must have unbounded geometric genus.

If D_k on X_4 had an integral representative, its arithmetic genus would be zero by (2), hence its geometric genus would be zero. Formula (3) would give D_k^2>=-62. But 1-8k^2<-62 for k>=3. These k are therefore impossible.

For k=1 and k=2 the accompanying interpolation certificates prove something stronger: there is no nonzero plane form of degree d=8k^2+1 with the specified lower multiplicities. The construction and exact verification are as follows.

Let i be a square root of -1 and place the centers in the affine plane as (i^a,i^b). Use monomials x^u*y^v with u,v>=0, u+v<=d, ordered by increasing u, then increasing v. At a center, multiplicity at least e means that the Taylor coefficients for all (r,s) with r,s>=0 and r+s<e vanish. The corresponding matrix entry is

binom(u,r) binom(v,s) (i^a)^(u-r) (i^b)^(v-s)

when u>=r and v>=s, and is zero otherwise. All entries lie in Z[i]. A polynomial of total degree at most d corresponds exactly to a degree-d homogeneous form under homogenization, so this matrix detects every possible required form.

Reduce Z[i] to F_101 by i->10, which is valid since 10^2=-1 mod 101. The matrices have sizes 60 by 55 for k=1 and 624 by 595 for k=2. CERTIFICATES.json specifies 55 and 595 selected rows, respectively. The verifier regenerates the entire matrices from the formula and computes the corresponding square-minor determinants modulo 101; both are nonzero. Therefore the original minors in Z[i] are nonzero, and the matrices have full column rank over Q(i), hence also over C. Their kernels are zero. No floating-point rank or experimental dimension estimate is used.

Together with (3), this excludes an integral representative for every member of the entire numerical family. It does not exclude other multiplicity patterns.

## 6. Power-images of a line: the characteristic-zero calculation

Let L be x_0+x_1+x_2=0 and let Gamma_d be its image under the coordinatewise d-th power map on P^2, for an integer d>=1. The map from L to Gamma_d is generically one-to-one. To see this on x_2=1, write a point as (x,-1-x). If (x',-1-x') has the same d-th power image, then x'=zeta*x and -1-x'=eta*(-1-x) for d-th roots zeta,eta. Unless zeta=eta=1, this gives either no solution or one value of x. There are finitely many such pairs. Thus the map is birational onto its image. Pullback of a general line has degree d on L, so Gamma_d has degree d and L is its normalization. The map is an immersion over the torus, since the power map is etale there in characteristic zero.

A normalization point maps into Z_m exactly when x_0^(dm)=x_1^(dm)=x_2^(dm). No coordinate can then be zero. With x_2=1, put N=dm. We need x,y in mu_N satisfying x+y+1=0. The unit-circle condition gives |1+x|=1, so Re(x)=-1/2. Therefore the only possibilities are (x,y)=(omega,omega^2) and (omega^2,omega), where omega is a primitive cube root. Such points occur exactly when 3 divides N.

If 3 does not divide dm, Gamma_d misses Z_m. If 3 divides m but not d, the two points have distinct images in Z_m and each gives one smooth branch, so both image multiplicities are one. If 3 divides d, the two images coincide at [1:1:1]; there are two smooth branches there, and the multiplicity is two. They have distinct tangent slopes -omega and -omega^2 in an appropriate affine chart, since d-1 is congruent to 2 modulo 3. Thus the strict-transform square on X_m is exactly

d^2-4, if 3 divides d;
d^2-2, if 3 does not divide d and 3 divides m;
d^2, otherwise.                                  (4)

For d>=2 these values are nonnegative (the first case has d>=3). The only negative instance is d=1 with 3 dividing m, which has square -1. This family cannot yield unbounded negativity on a fixed complex X_m.

For comparison, Cheng-van Dobben de Bruyn construct these same power-image curves over algebraically closed characteristic p>0, with m prime to p and dm=p^e-1. Their strict transforms are smooth rational curves with square d(3-m)-1. For fixed m>3 there are infinitely many admissible e, because p has finite multiplicative order modulo m. Their squares tend to minus infinity. This theorem concerns the exact grid surface, but a different characteristic.

The incompatible mechanism is visible without extrapolation: on x+y+z=0, x^(p^e)+y^(p^e)+z^(p^e)=0 is a Frobenius identity in characteristic p. Over C it is not identically zero for p^e>1. The complex torus intersection above has at most two normalization points. For m=4,d=6, the complex square is 32, whereas p=5,e=2 gives -7. Formula (4) supplies an explicit control against transferring the positive-characteristic formula to C.

## 7. Divisibility maps and the missing direction

If m divides n, Z_m is a subset of Z_n. Blowing up the remaining centers gives a morphism X_n->X_m. For the strict transform C' of any integral curve C on X_m,

(C')^2=C^2-sum_q mult_q(C)^2<=C^2.

Thus a lower bound for all curves on X_n also bounds all curves on X_m, and a counterexample sequence on X_m would propagate to X_n. This implication is downward in order for positive results; it cannot prove all higher orders from m<=3.

There is also a different finite morphism g:X_(am)->X_m induced by [x_0:x_1:x_2]->[x_0^a:x_1^a:x_2^a], of degree a^2. The inverse image of the center set is exactly Z_(am); the power map is etale near these points. Blowup commutes with this flat base change, giving the stated finite map and no exceptional branch divisor. Its only branch curves are the strict transforms of coordinate lines, all disjoint from the centers. This construction is also described in Section 2.1 of Cheng-van Dobben de Bruyn.

For an integral curve C other than one of those coordinate lines, g^*C is reduced, say sum_(j=1)^r D_j, with r<=a^2. Distinct components have nonnegative intersection, so

a^2 C^2 = sum_j D_j^2 + 2 sum_(j<k) D_j.D_k.       (5)

If all integral curves on X_(am) satisfy D^2>=-B with B>=0, then (5) implies C^2>=-rB/a^2>=-B. Coordinate lines already have square 1. This recovers downward boundedness.

Conversely, knowledge that C^2 is bounded below on the target does not bound any individual D_j^2 from below: the nonnegative cross-intersections in (5) are subtracted when solving for a component's square. Replacing the total pullback with one component and dropping these terms is invalid. The finite map therefore does not supply the missing upward implication.

## Remaining gap

For each fixed m>=4, one must still control nonsymmetric horizontal integral curves of unbounded degree and unbounded geometric genus. The proven vertical classification, equal-multiplicity argument, line inequalities, genus-bounded estimate, power-image calculation, and divisibility implications do not do this. No upper bound on their multiplicity variance, no effective-cone classification, and no construction of a complex counterexample is established here.
