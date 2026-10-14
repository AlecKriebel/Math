# Proof 26  Cubic high frequency dominant coefficient boxes

Included dependencies: [A dominant constant region on the cubic support](22_cubic_dominant_constant.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

Let q=p/2 be in (2,3), let a,b,c be nonnegative, and define

D_q(a,b,c) = E |a+bz+cz^3|^(2q) - E |a+bz-cz^3|^(2q),

where z is uniform on the unit circle. If c >= a+b, then

D_q(a,b,c) >= 4 binom(q,3) binom(q,2) c^(2q-5) a^2 b^3
  * [1-(3/5)(q-2)(3-q)] >= 0.                  (1)

At c=0 the right side is defined to be zero; the cone condition then forces a=b=0. When a,b,c are positive the right side is positive. The square bracket is at least 17/20 because (q-2)(3-q)<=1/4. Consequently the real coefficient box bounded by (a,b,c) has its maximum norm at its all-positive vertex whenever c>=a+b.

## Exact expansion

The c=0 case is trivial. Reflection of frequencies sends the positive polynomial to c+bz^2+az^3. An overall sign and z -> -z send the negative polynomial to c-bz^2+az^3. By homogeneity assume c=1, and put x=a/c, y=b/c; thus x+y<=1. The binomial expansion of (1+yz^2+xz^3)^q is absolutely uniformly convergent, including at x+y=1, because sum_j |binom(q,j)|<infinity.

An oriented sign-sensitive resonance has exponents

  (r+3k,s) and (r,s+2k), with r,s>=0 and k a positive odd integer,

where the coordinates count y and x respectively. Its contribution to D_q is

  4 (q)_(r+s+3k) (q)_(r+s+2k)
    x^(2s+2k) y^(2r+3k)
    / [(r+3k)! s! r! (s+2k)!],                       (2)

where (q)_j denotes the falling factorial. Both orientations are included by the factor 4. The unique positive contribution is r=s=0,k=1:

  L = 4 binom(q,3) binom(q,2) x^2 y^3.

Every other contribution in (2) is negative: its two block indices have opposite parity and are both at least 3. For j>=3, sign((q)_j)=(-1)^(j-3).

Write k=2h+1, R=r+3h, S=s+2h, and N=R+S. After dividing by L, a negative term has monomial x^(2S)y^(2R) and absolute coefficient

  12 |(q)_(N+h+3)(q)_(N-h+2)|
  / [(q)_3(q)_2 (R+3h+3)! (R-3h)! (S-2h)! (S+2h+2)!].                 (3)

Here 0<=h<=H=min(floor(R/3),floor(S/2)) and N>=1. Put beta=q-2. The elementary bounds

  (1-beta)_m <= m! for m>=0,
  (1-beta)_m <= (1-beta)m! for m>=1

for rising factorials give

  |(q)_(N+h+3)(q)_(N-h+2)| / [(q)_3(q)_2]
  <= beta(1-beta) (N+h)! (N-h-1)!.                (4)

The second factorial has a nonnegative index since h<=N/5 and N>=1. Explicitly, the two rising factors before bounding are (1-beta)_(N+h) and beta(1-beta)_(N-h-1).

## Combinatorial coefficient bound

For R,S>=0 with N=R+S>=1, define

  T_h = (N+h-1)! (N-h-1)!
    / [(R+3h+3)! (R-3h)! (S-2h)! (S+2h+2)!].

We claim

  12 sum_(h=0)^H T_h <= [2/(N^2(N+1)(N+2))] binom(2N,2R).             (5)

First T_h is nonincreasing in h. When h+1<=H, its consecutive ratio is

  (N+h)/(N-h-1)
  * [(R-3h)(R-3h-1)(R-3h-2)]
      /[(R+3h+4)(R+3h+5)(R+3h+6)]
  * [(S-2h)(S-2h-1)]/[(S+2h+3)(S+2h+4)].

The first factor is canceled by the first factor of the R quotient, because

  (R-3h)/(R+3h+4) <= (N-h-1)/(N+h).

Indeed, the cross-product difference is

  (6h+4)N-(2h+1)R-(7h+4)
  >= (4h+3)N-(7h+4) > 0,

using R<=N and N>=5h+5. Every remaining factor is at most 1. Therefore sum T_h <= (H+1)T_0.

By Vandermonde,

  binom(N,R)^2 <= binom(2N,2R).

Thus 12T_0 divided by the right side of (5) is at most

  P = 6(N+1)(N+2)/[(R+1)(R+2)(R+3)(S+1)(S+2)].

If R=0, then H=0 and P=1. If S=0, then H=0 and P=3/(N+3)<=1. If R,S>=1, then H+1 <= (R+3)/3, and hence

  P(H+1) <= 2(N+1)(N+2)
             /[(R+1)(R+2)(S+1)(S+2)] <= 1.

For the last inequality, RS>=N-1 implies

  (R+1)(R+2)(S+1)(S+2)
    = (RS+N+1)(RS+2N+4)
    >= 6N(N+1) >= 2(N+1)(N+2),

where N>=2. This proves (5).

## Summing the tail

Combining (3)--(5) uses the extra factor N+h in (4). Since h<=N/5, this factor is at most 6N/5. Bounding the even terms by the full binomial expansion therefore gives

  (L-D_q)/L
  <= beta(1-beta) sum_(N>=1) [12/(5N(N+1)(N+2))]
       sum_(R+S=N) binom(2N,2R) x^(2S)y^(2R)
`<= beta(1-beta) sum_(N>=1) [12/(5N(N+1)(N+2))](x+y)^(2N)`
  <= (3/5)beta(1-beta).

The last equality uses the elementary telescoping sum

  sum_(N>=1) 1/[N(N+1)(N+2)] = 1/4.

This proves (1) when x,y>0. Coordinate-zero cases follow by continuity (and have equality). Restore c by homogeneity.

## Full real coefficient box and remaining scope

For {0,1,3}, a global sign and z -> -z reduce all real sign vertices to the two norms defining D_q. Convexity of the Lp norm then establishes the full prescribed real coefficient-box result on c>=a+b.

Together with the constant-dominant theorem and [Proof 34](34_cubic_middle_cone.md), all three dominant coefficient cones are positive. The unrestricted strict-triangle region is not classified.
