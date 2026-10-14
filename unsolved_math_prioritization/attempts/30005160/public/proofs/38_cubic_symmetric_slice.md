# Proof 38  Symmetric cubic coefficient boxes and explicit neighborhoods

Included dependencies: [Symmetric extreme bounds on zero two five](36_k5_symmetric_slice.md); [Explicit neighborhoods of the symmetric zero two five slice](37_k5_symmetric_neighborhood.md).

This authored proof is presented at its accepted scope. See the [source inventory](../CONTENT_AND_DEPENDENCIES.md) for its exact source and reading-edition hashes.

## Statement

Let 4<p<6 and q=p/2. For all A,B>=0, every real coefficient triple with |a|<=A, |b|<=B, and |c|<=A satisfies

    ||a+bz+cz^3||_p <= ||A+Bz+Az^3||_p.

The sign gap

    D(A,B,A)=E|A+Bz+Az^3|^p-E|A-Bz+Az^3|^p

is strictly positive for A,B>0 and obeys

    D(A,B,A) >= 2(q)_3 A^3 B^3(2A+B)^(p-6)>0,                  (1)

where (q)_3=q(q-1)(q-2)>0.

This covers the full prescribed coefficient boxes with equal extreme-frequency bounds, including their strict-triangle portion. It does not settle arbitrary unequal bounds.

## Proof by a three-root trace

Set z=e^(2is) and multiply by e^(-3is). The squared moduli are

    B^2+4A^2 cos^2(3s) +/- 4AB cos(3s)cos(s).

Put v=cos(3s). The three possible cos(s) values at this level are the three distinct roots x_i(v) in (-1,1) of

    T_3(x)=4x^3-3x=v.

They have equal conditional weights, by substituting t=3s modulo 2pi and then v=cos t. Thus for continuous H,

    E_s H(cos(3s),cos(s))
      =(1/(3pi)) integral_(-1)^1 sum_(i=1)^3 H(v,x_i(v))/sqrt(1-v^2) dv.

For fixed 0<v<1, define

    a_v=B^2+4A^2v^2,   c_v=4ABv,
    f_v(x)=(a_v+c_vx)^q,
    R_v(w)=sum_(i=1)^3 f_v(x_i(w)).

If A,B>0, then a_v>=c_v>0, so f_v is smooth on (-1,1) and

    f_v'''(x)=(q)_3 c_v^3(a_v+c_vx)^(q-3)>0.

As in the five-root case, implicit differentiation and the elementary divided-difference formula give

    R_v'(w)=sum_i f_v'(x_i(w))/T_3'(x_i(w))
           =(1/4)f_v'[x_1(w),x_2(w),x_3(w)]>0.

Indeed the divided difference is f_v'''(xi)/2! for some interior xi. Since T_3 is odd, the roots at -v are the negatives of those at v. Consequently the conditional positive-minus-negative gap is R_v(v)-R_v(-v)>0. Integrating with the even-in-v conditioning formula proves strict positivity of D.

For the quantitative bound, since q-3<0,

    R_v'(w)>=(q)_3 c_v^3(a_v+c_v)^(q-3)/8.

Integrating w from -v to v and then v from 0 to 1 gives

    D(A,B,A)>=[(q)_3(4AB)^3/(6pi)]
      * integral_0^1 v^4(B+2Av)^(p-6)/sqrt(1-v^2) dv.

Use B+2Av<=2A+B and integral_0^1 v^4/sqrt(1-v^2) dv=3pi/16 to obtain (1).

A global sign and z -> -z reduce all real sign vertices on {0,1,3} to the positive vertex and the middle-negative vertex used here. Convexity then proves the full box. Zero parameters give equality.

## Explicit neighborhood with unequal extreme bounds

For A,B,C>=0, put M=(A+C)/2 and S=A+B+C. If S>0 and

    |A-C| <= (q)_3 M^3 B^3/(p S^5),                             (2)

then the full real coefficient box bounded by (A,B,C) also has its maximum at the all-positive vertex.

Indeed interpolation from (M,B,M) to (A,B,C), with the two extreme coefficients changing oppositely, yields exactly as in the K5 neighborhood argument

    |D(A,B,C)-D(M,B,M)|<=2p|A-C|S^(p-1).

Equation (1) at M and condition (2) make the resulting lower bound nonnegative. For fixed p and positive M,B this gives a concrete open neighborhood of the symmetric line, including unequal-bound strict-triangle boxes. This remains a sufficient local criterion, not an unrestricted majorant theorem.

## Scope warning

The Chebyshev conditioning has a linear cos(s) term here and in the K5 support {0,2,5}. For {0,2,7} the centered middle term instead contributes cos(3s); the present proof does not apply. No positivity claim is made for that support or for arbitrary odd-frequency triples.
