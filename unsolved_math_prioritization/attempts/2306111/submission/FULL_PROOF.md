# Partial results for the Janowski coefficient-neighbourhood problem

Author: Alec Kriebel. ORCID: https://orcid.org/0009-0001-9320-500X

Problem: 2306111 / AMR-022-6111, Hayman–Lingham Problem 6.111.
Date: 2026-10-04 (UTC).
Status: **UNSOLVED.** This document does not prove the requested starlikeness assertion. The results below are partial deductions and exact reductions; no novelty claim is made for them.

## 1. Exact target and remaining parameter set

Write D={z:|z|<1}. Let A be the analytic functions normalized by f(0)=0 and f'(0)=1. For f=z+sum_{n>=2} a_n z^n, put

    N_eta(f) = {g=z+sum b_n z^n in A: sum_{n>=2} n|b_n-a_n| <= eta}.

For real -1<=B<A<=1, K[A,B] consists of the normalized univalent functions satisfying

    1+zf''(z)/f'(z) = (1+A omega(z))/(1+B omega(z)),
    omega(0)=0, |omega(z)|<1.

Define

    delta(A,B)=(1-B)^((A-B)/B)  if B!=0,
    delta(A,0)=exp(-A).

The question asks whether N_delta(f) consists entirely of starlike univalent functions for EVERY f in K[A,B], and whether delta is the largest uniform constant. The recorded theorem covers B>=-c0 or A+B>=0, where c0=(2+sqrt(3))/4. Its uncovered parameter set is exactly

    -1<=B<-c0,  B<A<-B.                                      (1)

Thus B=0 is not a missing case. The B=0 formula is nevertheless included in the checks and deductions below. No inference about current literature status is made solely from the 2018 open-problem update.

## 2. Sharp universal univalence at the proposed radius

**Proposition 1.** For every permitted A,B and every f in K[A,B], all g in N_delta(f) are univalent in D. More precisely, Re(g'/f')>0. The constant delta is the largest one that can hold uniformly even for local univalence.

**Proof of the lower assertion.** Let p=1+zf''/f'. The Möbius map h(w)=(1+Aw)/(1+Bw) takes D into the right half-plane. For example, on |w|<=t<1,

    Re h(w) >= (1-At)/(1-Bt)>0.

The minimum occurs at w=-t: for |w|=t this follows by differentiating the real part as a function of cos(arg w), whose derivative has positive sign (A-B)(1-B^2 t^2). The interior follows by the minimum principle. Thus f is convex, by the usual analytic characterization Re(1+zf''/f')>0.

Schwarz's lemma gives |omega(z)|<=|z|. For z=r exp(i theta), integrating along the radius gives

    d/dt log|f'(t exp(i theta))|
        = Re((p(t exp(i theta))-1)/t)
        >= -(A-B)/(1-Bt).

Consequently

    |f'(z)| >= m(r),
    m(r)=(1-Br)^((A-B)/B)  (B!=0),
    m(r)=exp(-Ar)           (B=0).                            (2)

The function m is strictly decreasing, m(0)=1, and m(1)=delta. Hence |f'(z)|>=m(r)>delta whenever r<1.

If g=f+h and sum n|[z^n]h|<=delta, then

    |h'(z)| <= sum n|[z^n]h| r^(n-1) <= r delta < m(r).

It follows that Re(g'/f')>0. For a direct global-univalence proof, put G=g o f^{-1} on the convex domain Omega=f(D). Then Re G'(w)>0. For distinct w1,w2 in Omega,

    (G(w2)-G(w1))/(w2-w1) = integral_0^1 G'(w1+t(w2-w1)) dt

has strictly positive real part, so it is nonzero. Thus G and g are injective. This also proves the usual close-to-convex conclusion. It does not prove starlikeness. QED for this part.

**Proof of sharpness.** Define f0 by f0(0)=0 and

    f0'(z)=(1+Bz)^((A-B)/B)  (B!=0),
    f0'(z)=exp(Az)           (B=0),                           (3)

using the analytic logarithm on Re(1+Bz)>0. Then 1+zf0''/f0'=(1+Az)/(1+Bz), so f0 is in K[A,B]. Given any eta>delta, let

    g_eta(z)=f0(z)+(eta/2)z^2.

The coefficient distance is exactly eta. On the negative radius,

    g_eta'(-r)=m(r)-eta r.

This is positive at r=0 and tends to delta-eta<0 as r increases to 1. By continuity it has a zero for some r in (0,1). An analytic injective function has nonzero derivative, so g_eta is not locally univalent and cannot be starlike. This proves the claimed optimality for univalence. It also establishes the upper-bound/sharpness half of the original proposed starlikeness radius for every parameter pair. QED.

The proof deliberately keeps local/global univalence separate from starlikeness. Inferring the latter from Re(g'/f')>0 would be an unsupported strengthening.

## 3. Exact reduction to quadratic perturbations

This reduction is useful independently of the Janowski hypotheses.

For f in St, z!=0, r=|z|, set d=f'(z) and q=f(z)/z. Regard the real-linear map

    M_f(z):(u,v) -> u d - 2i v q,   (u,v) in R^2

as a 2 by 2 real matrix, and let sigma_f(z) be its smaller singular value. Explicitly,

    sigma_f(z)^2 = (a+b-sqrt((a-b)^2+16 Im(d conjugate(q))^2))/2,
    a=|d|^2, b=4|q|^2.                                      (4)

**Proposition 2 (exact criterion).** For eta>=0,

    N_eta(f) subset St
        iff sigma_f(z)>eta |z| for every 0<|z|<1.             (5)

If the inequality fails at one point, a perturbation f+c z^2 of coefficient distance at most eta already witnesses failure. Thus allowing arbitrary high-degree or infinite perturbations does not create a smaller obstruction at any point than a single quadratic coefficient.

**Proof.** For real theta define

    L_theta(h;z)=cos(theta) h'(z)-2i sin(theta) h(z)/z.

For h=sum_{n>=2} c_n z^n,

    |L_theta(h;z)|
      <= sum n|c_n| r^(n-1) sqrt(cos(theta)^2+4sin(theta)^2/n^2)
      <= r sum n|c_n|.                                      (6)

Equality in the operator norm is attained by a suitable c z^2: its value is 2c z exp(-i theta). Therefore the norm in (6) is exactly r, not just an upper bound.

Suppose (5) holds and g in N_eta(f). For every z!=0 and theta,

    |L_theta(g;z)| >= |L_theta(f;z)|-eta r
                        >= sigma_f(z)-eta r >0.

At theta=pi/2 this implies g(z)/z!=0. Hence W=zg'/g extends analytically to D, with W(0)=1. For cos(theta)!=0, L_theta(g;z)=0 is equivalent to W(z)=2i tan(theta). Since all imaginary values are excluded, connectedness of D implies Re W>0 everywhere. The standard analytic starlikeness criterion now gives g in St.

Conversely, if sigma_f(z)<=eta r, choose a real theta attaining the minimum on the unit circle and set

    c=-L_theta(f;z)/(2z exp(-i theta)).                       (7)

Then 2|c|=sigma_f(z)/r<=eta, and g=f+c z^2 satisfies L_theta(g;z)=0. If cos(theta)=0 then g(z)=0 at a nonzero z and g is not injective. Otherwise, if g(z)!=0 then zg'(z)/g(z) is purely imaginary, violating starlikeness; if g(z)=0 then injectivity again fails. Thus g is not starlike. QED.

For the original target, all f in K[A,B] are convex and hence starlike, so Proposition 2 applies without extra assumptions. In particular, the ENTIRE missing assertion is equivalent to

    sigma_f(z)>delta(A,B)|z|
    for all (A,B) in (1), f in K[A,B], 0<|z|<1.              (8)

The first Gram diagonal in (4) exceeds delta^2 by Proposition 1. The missing control is its coupling with q, not simply a derivative lower bound. For any s>=0, the Gram matrix minus s^2 I is positive definite precisely when

    |d|^2>s^2,
    (|d|^2-s^2)(4|q|^2-s^2)>4 Im(d conjugate(q))^2.          (9)

At s=delta|z|, (9) is another exact form of the remaining gap. We have not proved it uniformly.

## 4. Explicit models and sharpness stress tests

The extremal derivative (3) has

    f0(z)=((1+Bz)^((A-B)/B+1)-1)/(A)  if B!=0 and A!=0,

with the removable exceptional cases interpreted by integration, rather than division by zero. In particular:

- B=-1,A=0: f0(z)=-log(1-z).
- B=-1,A=1: f0(z)=z/(1-z).
- B=0: f0(z)=(exp(Az)-1)/A.

For B=-b and beta=(A-B)/b, the formula is f0'(z)=(1-bz)^(-beta). At z=-r, d=m(r)>0 and q=integral_0^1(1+brt)^(-beta) dt>=m(r). Consequently M has orthogonal columns and

    sigma_f0(-r)=m(r)>delta r.

As r tends to 1, this becomes the sharp boundary equality sigma_f0(-1)=delta. Therefore the natural extremal has no obstruction along the negative radius, while every larger neighbourhood fails by Proposition 1. This boundary equality alone does not establish (8) at other points or for other functions.

An elementary exact control family is f=z+a z^2 with |a|<=1/4. Its sharp coefficient-neighbourhood radius for starlikeness is 1-2|a|. Indeed, the triangle inequality puts N_{1-2|a|}(f) in N_1(z). To verify N_1(z) subset St directly, write g=z+sum b_n z^n. For r<1,

    sum n|b_n|r^(n-1)<1,
    |zg'-g| < |g|,

where the second inequality follows by bounding the numerator by sum(n-1)|b_n|r^n and |g| below by r-sum|b_n|r^n. Thus |zg'/g-1|<1 and g is starlike. Perturbing the quadratic coefficient in the direction of a until its modulus exceeds 1/2 proves the upper bound by a derivative zero; when a=0 any phase works. This checks the exact quadratic obstruction mechanism but is not a replacement for the Janowski class.

## 5. Herglotz / atomic-measure route and its exact limitation

For B=-1 write beta=A+1 in (0,2]. The condition for K[A,-1] is equivalent to

    p(z)=1+zf''/f'=1-beta/2+(beta/2)P(z),  Re P>0, P(0)=1.

By Herglotz's representation, there is a probability measure mu on the unit circle with

    P(z)=integral (1+u z)/(1-u z) dmu(u).

Integrating the logarithmic derivative yields

    f'(z)=exp(-beta integral log(1-u z) dmu(u)),
    f(z)/z=integral_0^1 exp(-beta integral log(1-u tz) dmu(u)) dt.       (10)

All logarithms are the analytic branches equal to zero at z=0; the formulas are valid locally uniformly in D. Conversely, (10) defines a function in K[beta-1,-1]. Thus the unresolved B=-1 slice really is an optimization over ALL probability measures, not just a heuristic parametrization.

For b in (0,1], a finite probability vector w_j and unit complex u_j, put

    f'(z)=product_j(1-b u_j z)^(-beta w_j).

Then

    1+zf''/f'=sum_j w_j (1+A u_j z)/(1+B u_j z),
    B=-b, A=b(beta-1).

The Janowski image is convex and contains these averages; its inverse gives the required Schwarz function fixing 0. Hence this is a certified subclass of K[A,B]. For b<1 we do NOT claim that this measure representation exhausts K[A,B].

The finite experiments search three-atom measures for b=0.94,0.97,1 and beta=0.1,0.5,1,1.5,1.9. They examine the boundary ratio sigma_f(1)/delta. All evaluated angles stay at least 0.001 away from the singular phase. A STRICT value below one would, by continuity, produce an interior violation of (8); none was found. The numerical minima approach a point mass at u=-1, the equality model above.

This is floating-point, finite-dimensional, non-exhaustive evidence only. Positive results for 15 optimizations, or even all three-atom measures, do not prove (8). The outstanding assertion involves arbitrary measures and the full disk; for b<1 it also includes functions outside this atomic subclass. The accompanying code gives exact search limits and software versions.

## 6. A rigorous smaller-disk starlikeness conclusion

Here we use the positive parameter-range theorem reported in Problem 6.111, rather than claiming to re-prove it.

**Proposition 3 (conditional on the recorded known theorem).** If (A,B) is in (1), f in K[A,B], and g in N_delta(f), then g is starlike on

    |z|<R,  R=c0/|B|,  c0=(2+sqrt(3))/4.                     (11)

In particular, R>=0.9330127018922193.

**Proof.** For 0<r<1 define f_r(z)=f(rz)/r and g_r(z)=g(rz)/r. If p_f=h_{A,B} o omega, Schwarz's lemma shows that omega(rz)/r is a Schwarz function. Therefore

    f_r in K[rA,rB].

Also

    sum n|[z^n](g_r-f_r)| <= r delta(A,B).

The proposed radius for the scaled parameters is

    delta(rA,rB)=(1-rB)^((A-B)/B)=m(r)>delta(A,B)>=r delta(A,B).

At r=R we have rB=-c0 and r<1, so hypothesis (a) of the recorded theorem applies. It follows that g_R is starlike throughout D, which is exactly (11). QED.

The general g is already globally univalent by Proposition 1. Nevertheless, starlikeness on the disk of radius R and univalence on D do not establish starlikeness on the remaining annulus. That annulus is the geometric gap left by this route.

## 7. Final mathematical disposition

The full answer to Problem 6.111 has not been obtained or verified from literature. We have proved the sharp univalence analogue and sharp upper bound, reduced every starlikeness obstruction to a quadratic perturbation with the exact singular-value criterion, derived a complete Herglotz formulation for B=-1, and transferred the recorded theorem to a concrete subdisk. The remaining task is the strict inequality (8), or a certified violation within its exact quantifiers.

The five approach families were exhausted without a complete candidate. This package must retain status `unsolved`, with five turns used; neither the finite computations nor the partial theorems justify `claimed_solved` or `already_solved`.
