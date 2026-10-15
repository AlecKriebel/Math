# Independent source consequence: universal PCF descent already fails in degree 3

Sealed before reading any sibling/root priority mechanism/report. This checks an explicit construction already present in Silverman (1995), Example on printed page 296, rather than undertaking a new proof search.

Let
\[
 f_d(z)=i\left(\frac{z-1}{z+1}\right)^d,\qquad d\ge3\text{ odd}.
\]
The exact formula was independently retrieved from the official Numdam PDF and visually inspected on printed page 296. Silverman states there that the absolute field of moduli is Q and there is no real field of definition (the latter continues on p.297 and is also stated for the cubic in the Introduction, p.271). Hidalgo–Quispe v4 (2021), Section 5.1, p.20, reproduces this same family as Silverman's examples. Neither occurrence explicitly labels this family PCF. The following elementary orbit check supplies that missing adjective.

## Exact PCF check

The map is the composition of the degree-one map m(z)=(z-1)/(z+1), the power map u^d and multiplication by i. Its only critical points are 1 and -1, each with local degree d. They are distinct, and the two homogeneous coordinates i(X-Y)^d and (X+Y)^d have no common zero, so the degree is exactly d. Equivalently the affine derivative is 2di(z-1)^(d-1)/(z+1)^(d+1); the pole at -1 has local degree d and infinity has local degree one.

For every odd d:
\[
 1\mapsto0\mapsto-i,\qquad -1\mapsto\infty\mapsto i.
\]
Because m(i)=i and m(-i)=-i,
\[
 f_d(i)=i^{d+1},\qquad f_d(-i)=i(-i)^d.
\]
For d=1 mod 4, these values are -1 and 1 respectively; for d=3 mod 4, they are 1 and -1. Thus the six-point set S={1,-1,0,infinity,i,-i} is forward invariant and both critical points are periodic. For d=3 mod 4 it is the six-cycle
\[
 1\to0\to-i\to-1\to\infty\to i\to1.
\]
For d=1 mod 4, it consists of the two cycles (1,0,-i) and (-1,infinity,i). The reduced postcritical set has exactly six points in both cases. Therefore all these maps are PCF.

## Complete elementary descent verification

Put T(z)=-1/z and c(z)=bar(z). A direct calculation for odd d gives bar(f_d)=T f_d T^(-1). Because coefficients belong to Q(i), every element of Gal(Qbar/Q) sends f_d to either f_d or bar(f_d). Both are conjugate, so the stabilizer is the entire absolute Galois group. The absolute field of moduli is exactly Q.

Any holomorphic dynamical automorphism H permutes the two critical points {1,-1} and, by commutation, their images {0,infinity}. If H fixes the two critical points individually, it fixes 0 and infinity individually, hence H(z)=a z and H(1)=1 forces a=1. If H swaps them, it swaps 0 and infinity, hence H(z)=a/z and H(1)=-1 forces a=-1. This candidate T does not commute: T f_d(infinity)=T(i)=i whereas f_d T(infinity)=f_d(0)=-i. Thus Aut(f_d)=1.

The antiholomorphic map A=T c=-1/bar(z) commutes with f_d because of the conjugacy identity. It is an involution with no fixed point: a finite nonzero fixed point would give |z|^2=-1, and 0 and infinity are swapped. Any other antiholomorphic automorphism differs from A by a holomorphic automorphism, so A is unique. A real representative M f_d M^(-1) would supply the antiholomorphic reflection M^(-1)cM commuting with f_d. Such a reflection has a fixed circle, whereas A has no fixed points. This is impossible. Hence there is no real model, in particular no Q-model.

This proves algebraicity, PCF, exact absolute field of moduli Q, and failure to descend. It settles the full literal AIM 2.6 question negatively, including all requirements for a prior-application classification. The d=3 instance suffices.

## Priority scope

This is a fully proved elementary consequence of Silverman's explicit 1995 example, not a claim that his printed theorem explicitly says “PCF,” and not a claim to have located the earliest historical recognition of its PCF property. The exact universal outcome cannot be credited as a novel discovery in PR36. The distinct degree-11 critically fixed graph realization may still be a different example or pedagogical contribution; its earliest exact appearance has not been established here. The orbit proof does not use Hlushchanka, graph classification, numerical centers, BBM, Bresciani, or sibling reports.
