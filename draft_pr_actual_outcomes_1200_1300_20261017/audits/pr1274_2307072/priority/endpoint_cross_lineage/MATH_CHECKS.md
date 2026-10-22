# Self-contained convention and implication checks

These are present audit derivations. They verify what follows from the displayed operators; they are not claims that earlier papers printed the full annihilator question or the particular polynomial family.

Let B_- f(z)=-pi^(-1) pv integral f(w)/(z-w)^2 dA(w), with zero extension of disc inputs. Put B_+=-B_-. Write partial=(partial_x-i partial_y)/2 and dbar=(partial_x+i partial_y)/2.

## Ordinary radial sign check

For |z|>1, expand (z-w)^(-2)=sum_(n>=0)(n+1)w^n/z^(n+2), uniformly for w in the closed disc. Angular integration gives integral_D w^n dA=0 for n>0 and pi for n=0. Therefore

    B_- 1_D(z)=-1/z².                                      (A)

For f=1_(0,1) and Lambda f(t)=t^(-1) integral_0^t f(s)ds-f(t), Lambda f(t)=1/t for t>1. Consequently the printed rule +(bar z/z)Lambda f(|z|²) gives +1/z² outside. It is incompatible with B_- in (A). For the negative kernel the ordinary radial rule has a minus in front of (bar z/z)Lambda. The positive-angular rule below has a different form and is not changed by this check.

## Conjugated angular check

Let h(w)=(bar w/w)1_D(w). In the same outside expansion, only the n=2 angular moment survives; its value is integral_D |w|² dA=pi/2. Thus

    B_- h(z)=-3/(2z^4),  |z|>1.                            (B)

For f=1_(0,1), Lambda* f(t)=integral_t^infinity f(s)/s ds-f(t) vanishes for t>1. Hence F=(bar z/z)f(|z|²) followed by B_-F=-Lambda*f(|z|²) is false as printed. Replacing F by (z/bar z)f(|z|²) gives the correct target formula. A global sign flip does not fix the angular mismatch in (B).

## Positive angular formula and logarithmic pair

For bounded real or complex a on (0,1), extend it by zero and define

    Q(t)=-integral_t^1 a(s)/s ds,  0<t<1,
    u(z)=z Q(|z|²) in D, and u=0 outside.

The potential has zero trace at |z|=1, tends to zero at 0, and has square-integrable first derivatives. At 0, its size is O(r|log r|); the integration-by-parts boundary term on radius epsilon is O(epsilon²|log epsilon|), which tends to zero. There is no hidden point mass. Zero trace eliminates a boundary distribution at the unit circle. Almost everywhere,

    dbar u=(z/bar z)a(|z|²),
    partial u=Q(|z|²)+a(|z|²).

The L2 identity B_-(dbar u)=partial u therefore gives

    B_-[(z/bar z)a(|z|²)]
        =a(t)-integral_t^1 a(s)/s ds=-Lambda* a(t), t=|z|²,  (C)

and the output is zero outside D. For a=1, u=z log|z|² and the output is 1+log|z|². Its magnitude is essentially unbounded near zero. Under B_+ the output is the negative of this expression, proving the BJ2009 sign qualification. The origin's assigned value is immaterial.

## All analytic area-L1 tests

For v(re^(i theta))=e^(2i theta)a(r²) with bounded a and phi holomorphic in D, integral_D |v phi| is finite whenever phi is in area L1. Polar Fubini applies. For every r<1 the Taylor expansion of phi on that circle contains only nonnegative modes, so integral_0^(2pi) e^(2i theta)phi(re^(i theta))dtheta=0. Thus v annihilates every such phi bilinearly. This is stronger than checking finitely many moments and uses no endpoint density assertion.

The Hermitian pairing is different: for v=z/bar z and phi=z², integral_D v bar(phi)dA=integral_D |z|²dA=pi/2. No Hermitian-annihilator conclusion follows.

## Particular polynomials and the exact norm

For integer m>=1, choose a_m(t)=1-(1-t)^m on (0,1). Then

    v_m=z² sum_(j=0)^(m-1)(1-|z|²)^j,
    Q_m(t)=-sum_(k=1)^m (1-t)^k/k,
    u_m=z Q_m(|z|²).

These have zero boundary potential, v_m in the bilinear N, and essential input norm one. Formula (C) gives

    G_m(t)=1-(1-t)^m-sum_(k=1)^m (1-t)^k/k.

The polynomial output is strictly increasing on (0,1), since

    G'_m(t)=m(1-t)^(m-1)+sum_(j=0)^(m-1)(1-t)^j>0.

Its endpoint limits are -H_m and 1. Every neighborhood of either endpoint has positive area, so its essential norm on D is max(H_m,1)=H_m. This includes m=1, with G_1=2t-1. The outside output is zero. Since H_m diverges, no common polynomial norm constant exists.

This proof supports the mathematics while preserving the historical distinctions: the logarithmic pair is printed in 1986, the general positive-angular rule is printed in 2010, and the N-membership plus this exact specialization are calculations assembled here unless another exact earlier source is located.
