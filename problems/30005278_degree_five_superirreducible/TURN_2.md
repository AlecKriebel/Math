# Turn 2: global sparsity obstructions for a possible square root

Problem 30005278. Second substantive author turn. **The source existence problem remains unresolved.** The global discriminant-square route is now constrained beyond the dyadic test: every nonconstant linear square in the root field of Du's quintic must have a square root using all five power-basis coordinates. We also derive an exact affine plane equation for the remaining witnesses, with all divisions and exceptional cases checked.

The polynomial f(X)=X^5+2X+1 and the ax²+c theorem remain credited to Du, https://arxiv.org/abs/2409.16206v2 . The composition reduction is the credited Capelli criterion. The restrictions and explicit elimination below are supplied without a historical novelty claim.

## 1. Exact coefficient equations

Let theta be a root of f, K=Q(theta), and suppose

    z=A_0+A_1 theta+A_2 theta²+A_3 theta³+A_4 theta^4,
    z²=M theta+N,             M,N in Q, M nonzero.          (1)

Reducing with theta^5=−2theta−1 gives the three necessary and sufficient equations

    Q_2=2A_0 A_2+A_1²−4A_2 A_4−2A_3²−2A_3 A_4=0,
    Q_3=2A_0 A_3+2A_1 A_2−4A_3 A_4−A_4²=0,
    Q_4=2A_0 A_4+2A_1 A_3+A_2²−2A_4²=0.                 (2)

When they hold, the remaining coefficients are exactly

    N=A_0²−2A_1 A_4−2A_2 A_3,
    M=2A_0 A_1−4A_1 A_4−4A_2 A_3−2A_2 A_4−A_3².        (3)

These equations live in the degree-five root field, not its full splitting field.

## 2. Every coordinate of a nonconstant witness is nonzero

**Theorem.** Under (1), all A_i are nonzero. In particular no square root supported on at most four of the five power-basis monomials can witness reducibility of f(ax²+bx+c).

### 2.1 The constant coordinate

Scale all A_i by a common rational number to make them integral with at least one odd coefficient. The primitive necessity in Turn 1 shows A_0 odd and all other coefficients even. Thus A_0 cannot be zero. This application does not require M,N to be integers before scaling; their scaled values are integers because the basis relation is integral.

### 2.2 A zero quartic coordinate

If A_4=A_3=0, equations Q_4=Q_2=0 successively give A_2=A_1=0, so z is rational and M=0, excluded in (1).

Otherwise with A_4=0, scale A_3 to one and put t=A_2. Equations Q_4=Q_3=0 give

    A_1=−t²/2,       A_0=t³/2.

Then Q_2=0 becomes 5t^4=8. No rational t satisfies this: the 5-adic valuation of t^4 would have to be −1. Hence A_4 is nonzero in every witness.

### 2.3 Normalize A_4=1

Write s=A_3 and t=A_2 after dividing z by A_4. Equations Q_4=Q_3=0 imply

    2A_1(t−s²)=s t²+2s+1.                                (4)

The denominator D=t−s² cannot vanish at a rational solution, because (4) would then imply s^5+2s+1=0, contradicting the irreducibility of f. We may therefore solve

    A_1=(s t²+2s+1)/(2D),
    A_0=(−t³+2t−4s²−s)/(2D).                             (5)

After this substitution the last equation Q_2=0 is equivalent to

    R(s,t)=−8s^6−8s^5+16s^4t+20s³t+5s²t^4+4s²t²
           +4s²−10st²+4s−4t^5−8t³+1=0.                 (6)

Specifically R=4D² Q_2, while Q_3 and Q_4 vanish identically under (5).

### 2.4 A zero cubic coordinate

If A_3=s=0, then D=t is nonzero and (6) becomes

    4t^5+8t³−1=0.

The rational-root theorem leaves only t=±1,±1/2,±1/4, and direct exact substitution excludes all six. Therefore A_3 is nonzero.

### 2.5 A zero quadratic coordinate

If A_2=t=0, (6) becomes

    −8s^6−8s^5+4s²+4s+1=0.

The rational-root theorem leaves only s=±1,±1/2,±1/4,±1/8, and direct exact substitution excludes all eight. Therefore A_2 is nonzero.

### 2.6 A zero linear coordinate

If A_1=0 and A_4=1, equation Q_4 gives A_0=1−t²/2, and Q_3 gives

    s=−1/(t²+2).

The denominator is positive for rational t, so this division has no exceptional case. The remaining equation Q_2=0 gives

    t(t²+2)^3−2(t²+1)=0.                                 (7)

This is a monic degree-seven integer polynomial with constant term −2. The only possible rational roots are t=±1,±2, and all four are excluded by exact substitution. Thus A_1 is nonzero, completing the theorem.

The constant rational square roots are excluded by M nonzero, as they must be: constant vectors are genuine solutions to the homogeneous equations (2), but cannot make a quadratic composition reducible since its theta coefficient is 4a nonzero.

## 3. Exact remaining curve and the additional integral-substitution condition

Every nonconstant linear square in K, modulo rational scaling of its square root, corresponds to a rational point (s,t) satisfying (6), with (5) and A_4=1. Conversely any rational point of (6) gives a solution to (2) by (5): D cannot vanish, since substitution t=s² into R gives

    R(s,s²)=(s^5+2s+1)²,

which is nonzero for rational s. The resulting vector has A_4=1, so it is not a constant vector. It cannot have M=0: if z²=N were rational with z nonrational, Q(z) would be a quadratic subfield of the odd degree field K, contrary to the tower law. Thus (6) is an exact global parameterization of all nonconstant linear-square witnesses up to scaling, without discarded rational exceptional points.

This reformulation alone does not solve the problem. In particular, a rational witness to z²=M theta+N does not automatically supply an integer quadratic substitution. Multiplying z by q in Q gives M'=q²M and N'=q²N. To correspond to a valid integer g=ax²+bx+c one needs

    a=M'/4 in Z nonzero,       N' in Z,
    b in Z,       b² == N' (mod 4a),
    c=(b²−N')/(4a) in Z.                                 (8)

Here q may be chosen to clear denominators first, but the square congruence in (8) remains an additional condition. Conversely (8), when satisfied, gives an integer quadratic with discriminant exactly (qz)², so Capelli proves reducibility. We do not drop that integrality condition or replace the source question by its stronger rational-substitution analogue.

The sparsity theorem excludes all five coordinate-hyperplane approaches. It does not determine the rational points of R or show there are none. The remaining global curve is therefore an explicitly identified unresolved step, not an asserted solution hidden in a change of variables.

## 4. Exact controls and next direction

The checker independently derives all five reduced coefficients, verifies the elimination identities, exhausts all rational-root candidates in the three excluded coordinate cases, and enumerates a modest box of projective integer vectors solely as a diagnostic. The rational proofs, not the diagnostic box, exclude sparse witnesses. No genus, rank, completeness of a rational-point list, or computer-algebra number-field black box is claimed.

Author turns completed: 2/5. Original target unresolved. Subjective completion estimate: 18%. The next turn will assess norm and finite-prime approaches against this global gap, rather than assuming a necessary norm-square condition is sufficient.
