# Turn 4: finite left-tail reduction and a unique continuous root for each pattern

**Scoped partial; original existence question unresolved after four new/recovered author turns.** This turn gives a general analytic reduction for each fixed outer span r, covering all n. It explains the isolated noninteger root in Turn2 and prepares an exact integer-root test without scanning larger binomial rows.

## 1. Setup

Use Turn2's nesting parameters: outer endpoints a,b=a+r, inner endpoints c=a+u,d=b-v, where u,v,s=r-u-v are positive integers. After reflection assume q=p/(1-p)<1. Put A=a, B=n-b, so0<=A<B. For P_j(x)=(x+1)...(x+j), define

 H_w(x)=s log P_r(x)-r log P_s(x+w),

where w is u or v. The two tie equations are equivalent to

 H_u(A)=H_v(B).                                                (1)

All arguments below use real x>=0, where the logarithms are defined.

## 2. The orientation of every biased collision

**Lemma 1.** If w>=r-s-w, then H_w is strictly increasing on[0,infinity), and tends to0 at infinity.

For the derivative, write f_x(j)=1/(x+j). Then

 H_w'(x)=rs[mean_{1<=j<=r} f_x(j)
                 -mean_{w+1<=j<=w+s} f_x(j)].                  (2)

The function f_x is strictly convex and strictly decreasing in j>0. Removing the two endpoints of a consecutive interval strictly decreases its average whenever an interior remains: every interior value lies strictly below the chord between the endpoints, and averaging those chord values gives the endpoint average. Remove r-s-w endpoints symmetrically from each side; then remove the remaining w-(r-s-w) left endpoints. The symmetric removals decrease the average by strict convexity, and the extra left removals decrease it by strict monotonicity. Both original side-removal counts are positive in our application. This proves the strict inequality in(2). The logarithmic leading terms in H_w cancel, so its limit is0.

If u>=v, Lemma1 makes H_u increasing. Since A<B,

 H_u(A)<H_u(B)<=H_v(B),

where the second inequality uses u>=v and the increase of P_s with its argument. This contradicts(1). Therefore every allowed collision with q<1 must satisfy

 u<v.                                                         (3)

Equivalently, the outer equal-height pair's midpoint lies strictly to the right of the inner pair's midpoint. The reverse orientation holds after reflecting to q>1. This is a global orientation theorem, stronger than merely excluding equal midpoints.

## 3. Exactly one possible continuous right-tail solution

Assume u<v. Then H_v is strictly increasing to0 by Lemma1. Also H_v(A)<H_u(A). Hence:

- If H_u(A)>=0, no finite B>A solves(1)
- If H_u(A)<0, there is exactly one real B>A solving(1), by continuity and strict monotonicity

The test H_u(A)<0 involves no numerical logarithm:

 P_r(A)^s<P_s(A+u)^r.                                         (4)

Once(4) holds, the remaining issue is whether that unique root B is an integer. Uniqueness of a real root is not a nonintegrality proof.

## 4. An explicit finite bound on A

Put delta=v-u>=1, t=A+1, mu=(r+1)/2 and nu=u+(s+1)/2=mu-delta/2. Jensen's inequality and the second-derivative Taylor bound for log give

 H_u(A)/(rs)
 >=log(A+mu)-log(A+nu)-(r^2-1)/(24t^2)
 >=delta/[2(A+mu)]-(r^2-1)/(24t^2).                            (5)

For the first bound, the variance of the uniform points1,...,r is(r^2-1)/12, their centered linear Taylor terms sum to zero, and log''(A+j)>=-1/t^2 throughout the interval. The inner mean of the logarithms is at most log(A+nu). The second bound uses log z>=1-1/z for z>=1.

If t>=r-1, then A+mu<=A+r<=2t. Thus(5) is at least

 [6delta t-(r^2-1)]/(24t^2).

Define the integer

 M(r,delta)=max(r-1, floor((r^2-1)/(6delta))+1).

For every A+1>=M(r,delta), the last numerator is strictly positive. Such an A cannot satisfy(4). Every genuine collision therefore has

 0<=A<=M(r,delta)-2.                                          (6)

This bound depends only on the outer span and offsets, not on n. It is sufficient, not asserted sharp.

## 5. Exact fixed-span decision procedure

For any specified r>=3, the following procedure decides all possible n and all real p for that outer span:

1. Enumerate positive u<v with s=r-u-v>=1
2. Enumerate the finitely many integers A in(6)
3. Discard A unless the exact integer comparison(4) holds
4. For each survivor define

 D(B)=P_r(A)^s P_s(B+v)^r-P_r(B)^s P_s(A+u)^r

At B=A this is positive. As B tends to infinity its sign is negative, because H_v(B) tends to0>H_u(A). The normalized logarithmic comparison has exactly one zero for B>A. Starting at the integer A, double an integer distance until an endpoint has D<=0. If D=0 an integer solution has been found. Otherwise use exact integer bisection to find adjacent integers L,U with D(L)>0>D(U). There can be no integer solution between them.

The doubling stage terminates mathematically for every survivor by the strict negative limiting comparison; no floating-point root approximation is needed. Positive denominators show that D(B)=0 is equivalent to(1). An integer solution produces n=A+B+r and q=(P_r(A)/P_r(B))^(1/r), with q in(0,1), and hence a genuine positive answer to the source's existence question. All four indices are distinct by u,v,s>0.

This is a finite procedure for each fixed r, not a uniform finite bound on r. The original question still ranges over unbounded outer span. The reduction does not itself decide whether some span eventually admits an integer root. One author turn remains; it will test this mechanism with explicit exact root certificates. The general convexity/Taylor tools are classical, and no historical novelty claim is made.
