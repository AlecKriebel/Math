# Turn 3: a verified analytic-space bridge for a Gaussian return model

**Substantive author turn 3 of 5. The original Helmholtz-density question remains unresolved.** This turn proves, rather than assumes, a same-space small-operator estimate for one explicit analytic local model. It also identifies its leading-multiplier correction. The model is not identified with the source's boundary operator. Analyticity and an interior complex neighborhood are genuine extra hypotheses, absent for general smooth convex obstacles.

## 1. The exact operator and Banach space

Let D_R={z in C:|z|<R}, R>0. Let F be holomorphic on D_R, F(0)=0, and |F(z)|≤theta R for all z, where 0≤theta<1. Let a be holomorphic and nonzero on an open neighborhood of the closed disc, with lambda=a(0)>0. Fix a complex number v with |v|=1 and a real r satisfying

    0<r<(1−theta)R,       delta=(1−theta)R−r>0.

For 0<h≤r²/2 put

    Z_h=integral_(-r)^r exp(−t²/(2h)) dt,
    (T_h f)(z)=a(z)/Z_h integral_(-r)^r
                   exp(−t²/(2h)) f(F(z)+v t) dt.            (1)

This defines a bounded holomorphic function on D_R: the integration points stay at least delta from its boundary, and locally uniform domination justifies holomorphic integration. The choice v=exp(i pi/4) has the direction of a rotated quadratic stationary-phase contour, but (1) is the definition; no contour deformation of a physical scattering kernel is asserted.

Use B=H-infinity(D_R) with the equivalent norm

    ||f||_B=|f(0)|+sup_(D_R)|f−f(0)|.

Thus ||f||_infinity≤||f||_B≤3||f||_infinity. Constants plus B_0={f:f(0)=0} is an exact l1 direct sum. Schwarz's lemma gives |F(z)|≤theta|z| and, for y in B_0,

    ||y composed with F||_infinity≤theta ||y||_infinity.

Consequently C_F acts as 1 on constants and has norm at most theta on B_0. This uses holomorphic interior contraction, not a derivative estimate on an unrestricted smooth space.

Define Wf=a(f composed with F), A=sup|a|. Because a is nonvanishing on a simply connected neighborhood of the closed disc, a/lambda has a holomorphic logarithm ell with ell(0)=0 and bounded derivative on the closed disc (restrict to a slightly smaller disc-shaped neighborhood if needed). The series

    g(z)=exp(sum_(j≥0) ell(F^j z))

converges uniformly on D_R: |ell(F^j z)|≤R sup|ell'| theta^j. Both g and 1/g are bounded holomorphic, g(0)=1, and

    g=(a/lambda)(g composed with F),   M_g^(-1) W M_g=lambda C_F. (2)

Multiplication satisfies ||M_b||_B≤3||b||_infinity, so
K=||M_g||_B ||M_g^(-1)||_B is finite (for example at most
9||g||_infinity||1/g||_infinity).

## 2. A same-space O(h) estimate without derivative loss

Let E_h denote integration against the normalized density in (1). Its odd moments vanish. Integration by parts gives

    m_2=E_h t²=h−2rh exp(−r²/(2h))/Z_h≤h,
    m_4=E_h t⁴=3h m_2−2r³h exp(−r²/(2h))/Z_h≤3h².          (3)

Both moments are nonnegative. Along every segment F(z)+svt, 0≤s≤1, the Cauchy derivative bound is

    |f^(j)(F(z)+svt)|≤j! delta^(−j)||f||_infinity.

Taylor's integral remainder, with the odd linear term canceled by symmetry, therefore proves

    sup|T_h f−Wf|≤A m_2 delta^(−2)||f||_infinity
                    ≤A h delta^(−2)||f||_infinity,
    ||T_h−W||_(B→B)≤C h,       C=3A/delta².                 (4)

In particular (4) controls every bounded holomorphic amplitude in the same norm, including h-dependent amplitudes. It is qualitatively stronger than a fixed-amplitude stationary-phase expansion. No bound on a derivative of the input in a larger norm is substituted for (4).

## 3. Uniform iterate quotients in this model

The block proof in Turn 2, Sections 3–4, uses only an l1 splitting into constants and B_0, contraction by theta on B_0, bounded point evaluation dominated by the norm, and invertible multiplication by g. All hold here. Apply that proof with k=1/h, phase xi=1 and C from (4). For clarity set

    Delta=1−theta,     epsilon=K C h/lambda,
    q=epsilon/(Delta−3epsilon).

If epsilon≤Delta/16, the normalized operator
S_h=lambda^(−1)M_g^(−1)T_h M_g has a rank-one commuting projection Pi_h and a multiplier zeta_h such that

    |zeta_h−1|≤2epsilon,
    ||S_h^j−zeta_h^j Pi_h||≤2(theta+2epsilon)^j.

For any nonzero f_h in B with a uniform a_0 in (0,1] satisfying

    |(f_h/g)(0)|≥a_0 ||f_h/g||_B,

if h≤min(1,a_0 lambda Delta/(32KC)) and

    j≥[log(1/h)+log(32/a_0)]/|log(1−3Delta/4)|,

all denominators below are nonzero on D_R and

    sup_(D_R) |(T_h^(j+1)f_h)/(T_h^j f_h)−lambda|
                    ≤(2KC+3lambda)h.                       (5)

The data f_h=g satisfy the excitation condition with a_0=1. Thus (5) is not an empty conditional statement for this exact operator. A physical incident field is not claimed to equal g or to satisfy this bound. Multiplying T_h by any scalar unit phase xi_h simply multiplies the limiting rate by xi_h.

## 4. The first correction to the leading multiplier

A more precise statement follows from the same analytic buffer. Write

    (E f)(z)=(v²/2) a(z) f''(F(z)).

For 0<h≤r²/2, Z_h≥2 exp(−1/2)sqrt(h). With t_0=r²/(2h)≥1, (3) gives

    0≤h−m_2≤r sqrt(h) exp(1/2−r²/(2h))≤3h²/r².             (6)

For the last bound, the ratio to h² is
r^(−2)(2t_0)^(3/2)exp(1/2−t_0), whose maximum for t_0≥1 is
3 sqrt(3)/(e r²)<3/r². Taylor expansion through degree three, symmetry, the fourth derivative Cauchy bound and (3) now give

    ||T_h−W−h E||_(B→B)≤C_2 h²,
    C_2=9A[1/(r² delta²)+1/delta⁴].                          (7)

Indeed the variance-replacement error in the supremum norm is at most
3A h²/(r² delta²), and the fourth-order remainder is at most
3A h²/delta⁴; the B norm costs at most three.

Set V=lambda^(−1)M_g^(−1) E M_g. The constant-to-constant entry of V is

    gamma=(V1)(0)=(v²/2) g''(0),                            (8)

using g(0)=1 and a(0)=lambda. The scalar Schur fixed-point equation in Turn 2 gives a quantitative second-order remainder without assuming a convergent perturbation series. If epsilon≤Delta/16, then

    |zeta_h−1−h gamma|
       ≤[KC_2/lambda+(KC/lambda)²/(Delta−3epsilon)]h².        (9)

The first term comes from (7) in the constant block; the off-diagonal Schur term is bounded by epsilon²/(Delta−3epsilon). Thus the actual leading multiplier of this exact model is lambda[1+h gamma+O(h²)], with constants stated above. For v=exp(i pi/4), v²=i; even real analytic positive transport weights can acquire an imaginary first correction. An optical positive magnitude by itself does not specify this correction or the optical travel phase.

As an explicit nonconstant weight, take F(z)=theta z and

    a(z)=lambda exp(c z+d z²),
    g(z)=exp(c z/(1−theta)+d z²/(1−theta²)).

Then

    gamma=(v²/2)[c²/(1−theta)²+2d/(1−theta²)].                (10)

This example meets the analytic nonvanishing hypotheses for any complex c,d and the indicated disc. The controls verify its formal coefficients and exact low-degree moment identities. They do not identify it with a boundary-integral kernel.

## 5. Relation to established scattering analysis and the remaining obstruction

An additional primary source was checked: A. Iantchenko, *Scattering poles near the real axis for two strictly convex obstacles*, [arXiv:math/0702022](https://arxiv.org/abs/math/0702022). Its initial sections define the physical quantum billiard operator and discuss the earlier Ikawa–Gérard resonance strings; its stronger normal-form analysis assumes analytic boundaries and nonresonant Poincare multipliers. These are pre-existing microlocal methods and results, not claimed as a contribution here. A resonance-location result is not automatically a uniform pointwise quotient estimate for the physical iteration and incident density.

The exact model above isolates a viable analytic mechanism for the same-space estimate that Turn 2 needed. To apply it to the source question one would still need a proved, uniformly bounded conjugation of the physical return operator into a controlled analytic integral form, including the single-obstacle solution operator, amplitudes, remote contour pieces and all remainders. General C-infinity boundaries need not permit this analytic continuation. A local model would additionally require control of all other modes, uniform excitation by the given incidence, and a return from the analytic norm to the desired actual-density statement. Shadow boundaries and possible zeros are separate global difficulties.

No such identification has been proved here. Equations (4), (5) and (9) are a complete theorem for (1), not a proof for arbitrary source obstacles. They show that a genuine smoothing/interior mechanism can remove the derivative-loss obstruction, while making its extra assumptions visible.

**Original unresolved, author count 3/5.** The next attempt should test whether established physical monodromy results provide the missing global mode control, rather than repeat this analytic model. Uncalibrated completion estimate: 30%.
