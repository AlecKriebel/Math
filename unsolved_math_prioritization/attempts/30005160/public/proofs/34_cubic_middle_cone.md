# Proof 34  Cubic middle frequency dominant coefficient boxes

Included dependencies: [A dominant constant region on the cubic support](22_cubic_dominant_constant.md); [Cubic high frequency dominant coefficient boxes](26_cubic_high_cone.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## Claim

For 2<q<3, a,b,c>=0, and b>=a+c, let

D_q(a,b,c)=E|a+bz+cz^3|^(2q)-E|a+bz-cz^3|^(2q),

where z is uniform on the unit circle. Then

D_q(a,b,c) >= (1/6) q(q-1)(q-2) b^(2q-3) a^2 c >= 0.       (1)

The zero triple is interpreted separately. The inequality is strict whenever a,b,c>0. All real sign vertices reduce to this comparison by a global sign and z -> -z; convexity therefore proves the entire prescribed real coefficient-box majorant property on this cone.

## Absolutely convergent exact series

If b>0, divide amplitudes by b, then factor z from the polynomial. Write a,c for the normalized amplitudes, so a+c<=1. Expand (1+a z^(-1)+c z^2)^q. The binomial expansion is absolutely uniformly convergent even when a+c=1, since sum_j |binom(q,j)| is finite. Multiplication and termwise integration are therefore valid, including boundary zeros.

An oriented sign-changing resonance has exponent pairs (r+2k,s+k) and (r,s), where r,s>=0 and k>=1 is odd. Both orientations give

D_q = 4 sum_(k>=1 odd) sum_(r,s>=0)
 (q)_(r+s+3k)(q)_(r+s)
 a^(2r+2k)c^(2s+k) /[(r+2k)!(s+k)!r!s!].             (2)

Here (q)_j is a falling factorial. For odd k, a term is positive if n=r+s is 0 or 2, and negative if n=1 or n>=3. Put

L=2(q)_3 a^2 c.

For positive a,c this is the k=1,n=0 term. Coordinate-zero cases follow by continuity and have D_q=0.

## The retained low blocks have a uniform one-third margin

Retain the entire k=1,n=0,1,2 blocks. Divide by L and write x=a^2,y=c^2 and t=q(3-q). Their sum is

P = 1-t(x/3+y/2)
 +t(q-1)(4-q)(x^2/24+xy/6+y^2/12).

Since 0<t<2 and (q-1)(4-q)>=2,

P >= 1-t H,
H=x/3+y/2-x^2/12-xy/3-y^2/6.

Now x+y<=1. For F=2H,

partial F/partial x = (2-x-2y)/3 >= (1-y)/3 >=0.

Consequently F(x,y)<=F(1-y,y)=1/2+y^2/6<=2/3. Thus tH<=2/3 (immediate also when H<0), and

P>=1/3.                                                    (3)

In particular the positive n=2 block is not discarded.

## The remaining negative terms

Write k=2h+1, R=r+2h, S=s+h, N=R+S, and n=N-3h. Let

B=(R+2h+2)!(R-2h)!(S+h+1)!(S-h)!.

The contribution divided by L has coefficient

2 (q)_(N+3h+3)(q)_(N-3h) /[(q)_3 B]

multiplying a^(2R)c^(2S). The allowable h satisfy 0<=h<=min(floor(R/2),S).

For n>=3, use rising factorials (u)^[m] and 0<3-q<1:

|(q)_(N+3h+3)|/(q)_3 = (3-q)^[N+3h]
 <=(3-q)(N+3h)!,

|(q)_n| = (q)_3 (3-q)^[n-3] <= (q)_3 (n-3)!.

Also (q)_3(3-q)=q(q-1)(q-2)(3-q)<=3/2. Define

C_N(R,S) = sum_(h allowable, N-3h>=3)
 2 (N+3h)!(N-3h-3)! / B,

M_N = max_(R+S=N) C_N(R,S)/binom(2N,2R).

The total magnitude of every negative n>=3 term is at most

(3/2) sum_(N>=3) M_N (a+c)^(2N) <= (3/2) sum_(N>=3) M_N.   (4)

For the negative n=1 terms with h>=1, necessarily N=3h+1. There are exactly two possibilities: r=1,s=0 or r=0,s=1. Their normalized factorial coefficients after the same binomial comparison are respectively

2/[(4h+3)(2h+1)(6h+2)],
2/[(4h+2)(4h+1)(6h+2)].

The first is larger for h>=1. Both are <=1/(24h^3). Their common exponent-dependent multiplier is q(3-q)<=2: this follows by bounding (3-q)^[6h+1] <=(3-q)(6h+1)!. Taking the maximum binomial coefficient ratio, rather than adding the two, is valid because they occupy distinct monomials in the full binomial sum. Hence all these negative terms total at most

2 sum_(h>=1) 1/(24h^3)
 <= (1/12)(1+integral_1^infinity u^(-3)du)=1/8.             (5)

All remaining terms (n=0 or 2, h>=1) are positive and may be discarded.

## A uniform analytic coefficient bound

For every N>=8,

M_N <= 472/N^3.                                             (6)

To prove it, put j=N+3h+3 and l=N-3h. Vandermonde gives

binom(2R+2,R+2h+2) binom(2S+1,S+h+1)
 <= binom(2N+3,j).

First remove the factor N+3h from the numerator factorial, replacing (N+3h)! by (N+3h-1)!. Let the resulting auxiliary summand be T_h. Vandermonde bounds T_h by

2(2N+3)(2N+2)(2N+1) /
 [(2R+2)(2R+1)(2S+1) j(j-1)(j-2)(j-3) l(l-1)(l-2)].       (7)

Always j(j-1)(j-2)(j-3)>=N^4, and the numerator is <=54N^3.

For h<=N/6, l>=N/2. Since N>=8,
l(l-1)(l-2)>=N^3/32.
Also (2R+2)(2R+1)(2S+1)>=2(2N+1)>=4N. Each such summand is <=432/N^5. There are at most N/6+1<=N/3 such h, so this part is <=144/N^4.

For h>N/6, R>=2h>N/3 and S>=h>N/6, so
(2R+2)(2R+1)(2S+1)>=4N^3/27.
Equation (7) is then <=(729/2)/[N^4 l(l-1)(l-2)]. Distinct h give distinct l>=3, and

sum_(l>=3) 1/[l(l-1)(l-2)]=1/4.

This part is <=729/(8N^4). Adding gives sum_h T_h<236/N^4. Restoring the omitted factor uses N+3h<=2N, because n=N-3h>=3. Thus C_N(R,S)/binom(2N,2R)<=472/N^3, proving (6). The restored factor is essential.

## Exact small coefficients and conclusion

The accompanying exact-arithmetic certificate evaluates every defining rational coefficient for 3<=N<=99, every R+S=N, and every allowable h. It verifies

sum_(N=3)^99 M_N < 7/125.                                  (8)

No floating-point calculation is used by this certificate. The full coefficient ratios and exact maxima are recorded in [check_middle_exact.json](../certificates/check_middle_exact.json). The infinite range follows analytically from (6):

sum_(N>=100) M_N <=472 sum_(N>=100) N^(-3)
 <=472 integral_99^infinity u^(-3)du=236/99^2.

Combining (4) and (5), all discarded negative terms have total magnitude at most

(3/2)(7/125+236/99^2)+1/8 =800803/3267000 <1/4.

Combining this with (3) gives D_q/L>=1/3-800803/3267000>1/12. In particular D_q>=L/12. Restoring b yields (1). Boundary a+c=b was already included by absolute uniform convergence; coordinate-zero cases follow by continuity. The zero triple is trivial.

## Scope left open

Together with the separately accepted constant-dominant and frequency-3-dominant cones, this covers every nonnegative amplitude triple with at least one amplitude >=the sum of the other two. The unrestricted strict-triangle region a<b+c, b<a+c, c<a+b remains open. [Proof 38](38_cubic_symmetric_slice.md) covers its symmetric-extreme and explicit nearby boxes. No unrestricted theorem about that region or the support {0,2,5} follows from the dominant-cone argument.
