# PR104 / 600008 independent reproduction

Audit completed 2026-10-06 UTC. The stated analytic criterion survives this bounded independent audit. No counterexample or missing central implication was found for positive axes, the specified positively advancing equator map, and literal alternating full arcs with the stated even-parity requirement. This is acceptance of the precise analytic statement, not a novelty judgment or a finite algebraic Cayley criterion.

Original checkers have a real enforcement defect: Python optimization deletes their assert guards. The separate minimal RuntimeError repair is sufficient to fix that defect while preserving every other checker-source byte and all proof bytes.

## Claim and independent derivation

The target is rho=(1-M)/(2M), with M the mean of sqrt(f(t)^2/(c+f(t)^2)), f(t)^2=a sin(t)^2+b cos(t)^2. The specified lifted equator map closes after n steps and r positive turns iff M=n/(n+2r). Literal tropic-to-tropic chains also require n even. Least full-arc period for reduced rho=p/q is lcm(2,q).

Before reading archived result receipts, I derived the metric directly from the ambient embedding x=sqrt(a) cos(lambda) cos(phi), y=sqrt(b) cos(lambda) sin(phi), z=sqrt(c) sin(lambda). The five exact symbolic identities in ambient_diagnostics.py establish

E=cos(lambda)^2 f(phi)^2,

F=(a-b) sin(phi) cos(phi) sin(lambda) cos(lambda),

G=(a cos(phi)^2+b sin(phi)^2) sin(lambda)^2-c cos(lambda)^2,

F^2-EG=cos(lambda)^2[c f(phi)^2 cos(lambda)^2-ab sin(lambda)^2].

The ambient normal gives the same belt and tan(lambda)^2=c f(phi)^2/(ab) tropics. Thus ordinary latitude has strictly positive longitude coefficient inside the belt and supplies a separate null ODE dphi/dlambda=(-F +/- sqrt(F^2-EG))/E. Its trajectories do not use the proposed conformal metric or rotation formula.

The written global-coordinate argument is sound: the transverse root equation is strictly decreasing when x,y do not both vanish; its endpoints bracket precisely the closed belt. Signed equator gluing has a nonzero local ratio between Y and z. The boundary extension is a homeomorphism, while its v^(3/2) behavior correctly does not assert a nonsingular Lorentz metric at the tropics. The exact metric identities and positivity then give the conformal cylinder and its straight null paths. Null curves are unparameterized geodesics on a nonsingular Lorentzian surface because the null orthogonal complement is their tangent line. No extension of that argument beyond the belt is required.

I independently fixed the contour signs by continuing the four factors from positive infinity. On the upper bank their total argument is pi on (0,c) and 3pi on (-a,-b); the sign change of z makes z/R negative imaginary on both. Counterclockwise loops therefore contribute +2i times each positive period. The differential has coefficient 1/z at infinity, so I_u+I_v=pi. Integrable endpoint singularities add no contribution. This contour uses a>b; swapping axes and then continuity, or the direct rotational integral, handles a=b. With I_u=L/2 and equator advance 2H=I_v this yields the claimed rho. Positive density, strict decrease in c, the limits M->1 and M->0, and parity give the remaining uniqueness, bounds, winding and minimality conclusions.

## Actual reproduction and adversarial controls

The source was inspected before execution. Unmodified copies ran with /usr/bin/python3 -E -B, Python 3.9.6 and SymPy 1.14.0. Exact normal replay reproduced all 2,087 author checks and all 752 old-independent checks, including complete check dictionaries and analytic-artifact hashes. Normal and optimized original runs return PASS, but both forced-false helper calls exit 1 normally and exit 0 under -O. The optimized calls explicitly print FORCED_FALSE_ACCEPTED. Hence an optimized original PASS is not evidence of truth enforcement.

Independent inspection found the repair changes exactly one assert to an explicit RuntimeError guard per checker. Actual ck function ASTs compiled at optimize=0 and optimize=2 reject false inputs, do not increment their counts, and accept/count true controls. All other checker bytes are identical. Both repaired proof copies have the original SHA-256 608217a2ffc120a965b165f5b6065edd83f8cf94c5e77f0f95a0326640db2dae. Root's full repaired-count replays are consistent with this narrow independent semantic assessment; those shared replay files were not modified.

## Distinct numerical diagnostics and exact gap

The ambient-latitude ODE passed 11 axis cases and 17 initial trajectories at two tolerances. It traces equator-to-North-to-equator passages, complete North-to-South arcs, and complete South-to-North arcs, with explicit moving-boundary event corrections. Cases include rotational c=0.01,3,8,16/9,10000; swapped and unequal axes; horizontal ratios up to 10,000; small c; and common scaling by 1e-8. Maximum tight-run normalized shift error against the predicted rho is 6.257067729267415e-10. Maximum longitude difference between the two tolerance runs is about 1.49e-6. Fifty-digit quadrature independently checks the period identity in all 11 cases. These are numerical diagnostics, without interval error enclosures or a global proof claim.

Explicit rational boundary-state iteration checked 91 reduced fractions. Physical rotational trajectories first close after 2,2,6 full arcs for rho=1/2,1,1/3 respectively. In the rho=1 example a single arc has one winding but ends on the other tropic; in rho=1/3 three arcs have one winding but also end on the other tropic. This directly probes the parity/minimality distinction.

An early auxiliary chart q=tan(lambda) sqrt(ab/c)/f(phi) fixes the boundaries but is not a monotone global flow coordinate. Its constant-q levels can be timelike: at a=1/10000,b=1/10,c=1, sin(phi)^2=999/1000,q^2=1/36, the exact induced longitude coefficient is -60981564600753912/1754341758306005. The initial failed numerical route and its raw exit-1 record are preserved; the ordinary-latitude replacement avoids this unsupported chart assumption. This is a limitation of the auxiliary diagnostic, not the target conformal coordinates.

The source cache confirms GKT Section 5 defines the equator-to-North-to-equator map and Tabachnikov Section 7 describes full tropic-to-tropic chains. The source_record.json imported elliptic-torsion conclusion remains unsupported; a third-kind invariant differential does not itself identify an ordinary elliptic-group translation. The verified result remains analytic. Novelty and the stronger finite algebraic Cayley request are outside this bounded reproduction and unresolved here.

## Artifacts and accounting

EXECUTIONS.json contains exact argv, cwd, timestamps, exit codes and complete raw stdout/stderr for eight original replays/false controls, the failed auxiliary diagnostic, the successful latitude diagnostic, and the repair assessment. DIAGNOSTICS.json retains numerical cases, shifts, solver counts and events; REPRODUCTION_COMPARISON.json retains receipt comparisons; REPAIR_ASSESSMENT.json records the narrow repair and exact auxiliary-chart counterexample. MANIFEST.json is the single input/output hash manifest. Re-run reproduce.py to append fresh executions; original inputs remain read-only.

Assigned bounded reproduction is 100% complete. Original attempt accounting remains 1/5; extra central proof-search turns are 0. No shared inputs, Git state, services, publication state, or external contacts were changed.
