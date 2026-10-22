# Arithmetic proofs and scope controls

These checks support the source-to-question deduction in README.md. The geometric theorem inputs are [Laface–Ugaglia, Theorem 2](https://arxiv.org/abs/2609.26521) and [Malara–Merta–Szpond–Zieliński, Theorem 1.2](https://arxiv.org/abs/2610.01783). This document does not substitute arithmetic tests for those theorems.

## One-point and multipoint thresholds

Let pi:Bl_x X -> X blow up a smooth point on a smooth projective surface. For an ample divisor L,

  epsilon(L;x) = sup{t >= 0 : pi*L - tE is nef}.

Since (pi*L-tE)^2=L^2-t^2, nefness implies t<=sqrt(L^2). To establish equality it suffices to prove the boundary class pi*L-sqrt(L^2)E nef. A square calculation by itself gives only the upper bound.

For r distinct plane centers with exceptional curves E_i, the analogous class is H-t sum E_i and its square is 1-rt^2. Under the degree inequality d>=sum m_i/sqrt(r) for every proper-transform prime curve, H-(sum E_i)/sqrt(r) has nonnegative intersection with those curves and with each E_i. It is therefore nef and the r-point constant is 1/sqrt(r). This argument is explicitly conditional on the inequality and does not compute the one-point constant of a chosen integral divisor on X_r. In particular, r=9 gives the rational value 1/3 in this multipoint calculation.

## Rank coverage and nonsquareness

The map r -> n=2r-13 is a bijection from integers r>=10 to odd integers n>=7. With k=(n-1)/2, the number k+7 is exactly r.

For all integer n>=5, put q=n(n-4). Then

  q-(n-3)^2 = 2n-9 > 0,
  (n-2)^2-q = 4 > 0.

Thus q lies strictly between consecutive integer squares. A rational square root of an integer is an integer: if sqrt(q)=a/b in lowest terms, b^2 divides a^2, hence b=1. It follows that sqrt(q), and also 2sqrt(q), are irrational.

## Divisor square and numerical ampleness hypotheses

Take n=2k+1>=7, d=3n-4, with multiplicities n once, n-2 four times, 4 k times and 2 twice. They are positive and nonincreasing. Their squared sum is

  Sigma = n^2 + 4(n-2)^2 + 16k + 8 = 5n^2-8n+16.

Consequently d^2-Sigma=4n(n-4). The three linear margins in Hanumanthu's ampleness criterion are

  d-(m1+m2)=n-2,
  2d-sum_(i=1)^5 m_i=n,
  3d-(2m1+sum_(i=2)^7 m_i)=3n-12.

All are positive. For s>=2, (s+3)/(s+2)<=5/4 and the first s squared multiplicities sum to at most Sigma. It suffices that 4d^2-5Sigma>0. Substituting n=7+z yields

  4d^2-5Sigma = 11n^2-56n-16 = 11z^2+98z+131 > 0

for z>=0. Thus every inequality in [Hanumanthu's Theorem 2.1](https://arxiv.org/abs/1507.06391v3) holds. This verifies the criterion application for all n>=7, not just the tested values.

For the exceptional r=9 formula, let X be the very general nine-point blowup and eta:X->S5 contract E6,...,E9. The unique plane cubic through the centers is smooth and irreducible for very general centers. Its transform B=-K_X has square zero. Every irreducible curve other than B has nonnegative intersection with B, and B^2=0, so B is nef. S5 is a degree-four del Pezzo surface. The identity

  9H-3 sum_(i=1)^5 E_i-2 sum_(i=6)^9 E_i
  = 2(-K_X)+eta*(-K_S5)

shows positivity on every curve not contracted by eta; the remaining four curves have intersection 2. The square is 20>0, so Nakai–Moishezon gives ampleness. This argument does not itself prove the Seshadri lower bound.

## Matrix checks and their logical boundary

Let Q be the matrix [[0,1,0],[1,0,0],[0,0,-2n]] and let

  T = [[0,1,0],[1,n,2n],[0,-1,-1]].

Set Delta=sqrt(n(n-4)), alpha=(n-Delta)/2, beta=(n+Delta)/2 and lambda=(n-2+Delta)/2. Direct multiplication proves T^tQT=Q. The vectors R=(alpha,beta,-1), Rbar=(beta,alpha,-1), K=(-2,-2,1) have eigenvalues lambda, lambda^(-1),1 respectively. Their exact decomposition is

  (0,1,0) = beta R/[n(n-4)] + alpha Rbar/[n(n-4)] + K/(n-4).

For gamma=(n-2,1,-1), gamma^t Q gamma=-4. The matrix

  S = I + gamma gamma^t Q/2

is an involutive Q-isometry. A direct substitution gives

  S R = c_n (n-4,1,-Delta/n),
  c_n = [n(n-3)+(n-1)Delta]/4 > 0.

All these identities are checked symbolically without numerical square-root approximations. They establish identities in a lattice with a quadratic form. To conclude nefness, one still needs actual isomorphisms, limiting nef classes and an allowed geometric deformation. Those are the cited theorem inputs.

## Universal recurrence and polynomial controls

For odd n>=5, w0=(n-1)/2 is invertible modulo n, with inverse n-2. Start (a,b)=(n-2,1). Alternate the maps

  (a,b) -> (-a-b,a),
  (a,b) -> ((n-4)a-b,a).

At an even stage suppose |a|>|b|>0 with equal signs. The first map gives opposite signs and new first magnitude |a|+|b|>|a|. At an odd stage, opposite signs imply that the second map gives equal signs and first magnitude (n-4)|a|+|b|>|a|. Induction proves the assertion at every stage. Both possible weights w have |w|>=2 and |w-n|>=2, so b is neither wa nor (w-n)a. This is an all-step arithmetic exclusion, supplemented in the program by exact iterations.

A second elementary check concerns polynomials with deg f<=2n-3 and deg g<=1. If U!=1 and

  f+(n-2)x^(n-2)g=(x^n-1)a,
  f-(n-2)x^(n-2)g=(x^n-U)b,

where deg a,deg b<=n-3, comparison in degrees n through 2n-3 gives a=b. Subtraction now gives

  2(n-2)x^(n-2)g=(U-1)a.

The left has degrees only n-2,n-1, while the right has degree at most n-3. Thus g=a=b=f=0. The program also constructs the exact coefficient matrices for n=5,7,9,11,13 and computes their nonzero determinants. The interpretation of this polynomial system as a normal-bundle section problem requires the geometric setup; that interpretation is not certified by a determinant alone.

## Controls against stronger or incorrectly normalized claims

1. **Arbitrary evaluation points fail.** For the r=9 divisor, a point x on E6 lies on a smooth curve of L-degree 2. Hence epsilon(L;x)<=2<sqrt(20). The known equality therefore cannot be extended to all x.
2. **Arbitrary center configurations fail.** If all nine centers are distinct points on a line, its strict transform C has L.C=9-5(3)-4(2)=-14. The displayed divisor is not nef, let alone ample, on that blowup.
3. **One extra center is essential in the nef class.** A one-point computation on a nine-center blowup involves ten total centers after blowing up the evaluation point. The assertion is not a computation on the original nine-center lattice alone.
4. **No real-scaling shortcut.** Multiplying a line bundle by an irrational scalar does not produce an integral line bundle. Every displayed polarization here is integral before epsilon is computed.
5. **A singular quotient is intermediate.** Nefness on a quotient or on its resolution is insufficient until the smooth plane-blowup polarization and its ampleness have been established.
6. **No conditional-to-unconditional shortcut.** Nagata's inequality yields a conditional multipoint statement. The unconditional one-point conclusion in this packet uses the two explicitly cited 2026 theorem statements, not a change in the logical status of Nagata.

## Reproducibility limits

The program checks the complete marked fiber intersection chains, contraction order, divisor orthogonality equations and Cremona arithmetic for ranks 9 through 64, in addition to the symbolic identities. The finite range is a control; the universal arguments above and cited geometric theorems carry the unbounded claim. There is no numerical extrapolation, novelty claim, or formal-geometric certificate.
