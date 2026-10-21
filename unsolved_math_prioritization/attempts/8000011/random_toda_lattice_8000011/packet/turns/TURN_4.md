# Author turn 4: exact two-particle first-crossing mean

2026-10-03 06:24 UTC. Complete n=2 subproblem, original general-n problem unresolved. Completion estimate: 90% toward partial packet, 20% toward full source request.

This turn evaluates the all-coupling expectation for n=2 at every epsilon>0. Because there is one coupling, this is a special dimension, not a replacement of the target by endpoint deflation at general n.

## Exact trajectory and initial-direction law

Let d=lambda_2−lambda_1>0 and x=(a_1−a_2)/d. The chosen Lax equation gives x'=d(1−x²), and hence, for an initial parameter s=arctanh(x(0)),

 x(t)=tanh(dt+s),  b(t)=(d/2) sech(dt+s).

Under the unscaled two-by-two GOE, d has density f(d)=(d/4)exp(−d²/8). The vector ((a_1−a_2)/2,b_1) consists of an independent standard Gaussian and an absolute standard Gaussian. Its radial coordinate and angle are independent; the angle is uniform on a half-circle. Consequently s is independent of d and has density h(s)=sech(s)/pi on the real line.

If d<=2epsilon, T_all=0. If d>2epsilon, define A=arcosh(d/(2epsilon)). The FIRST crossing is

 T_all = (A−s)/d if −A<s<A,
         0 otherwise,                                      (11)

up to the zero-probability boundary. In particular s<−A means the initial coupling is already below epsilon, so T_all=0 even though the coupling later rises above epsilon. Using the later outgoing root there would compute a different stopping rule.

Symmetry of h removes the odd s term, and

 E[T_all | d]=(A/d) P(|s|<A)
             = (2A/(pi d)) arccos(2epsilon/d), d>2epsilon.

Thus the exact all-tolerance answer in dimension two is the convergent one-dimensional integral

 E[T_all(2,epsilon)]
 = (1/(2pi)) int_(2epsilon)^infinity exp(−d²/8)
        arcosh(d/(2epsilon)) arccos(2epsilon/d) dd.           (12)

There is no unknown Toda trajectory or implicit hitting-time functional in (12). It is a standard special-function quadrature. The n=1 answer is identically zero.

## Consistency checks

As epsilon decreases, (12) is consistent with Turn 3's constants C_2=sqrt(pi/8) and B_2=C_2(log2−EulerGamma)/2. Numerical quadrature below is diagnostic, not the proof of this expansion or of (12). The exact derivation is the independent radial/angular change of variables and the first-crossing partition (11).

A first-crossing negative control fixes d=4 and s=−3: for epsilon=1/2, A=arcosh4<3, so T_all=0 despite the positive later outgoing root (A+3)/4. The counterpart s=0 has T_all=A/4. A direct ODE check of x'=d(1−x²), b'=−db tanh(dt+s) verifies the Lax time normalization.

## Remaining gap

General n>=3 retains simultaneous-coupling interactions in its first-crossing condition. Equation (12) neither extends to n>=3 nor establishes full average-complexity universality. The next and final author turn will seek general-n finite-tolerance control rather than claiming this special dimension resolves the source.
