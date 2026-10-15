# Checkable routine-specialization bridge for the core negative implication

## Audit criterion

An earlier counterexample at a genuine local optimizer is enough to resolve the core negative implication. It need not establish the submitted stronger global uniqueness or target perturbation results. An earlier abstract theorem can cover a case through a genuinely routine specialization. This bridge records such a specialization and isolates exactly which inputs predate the submitted construction. It is an audit derivation, not a claim that an earlier article printed the final unit-ball example verbatim.

## Prior inputs, a local codomain repair, and local-optimality bridge

Use the actual KM model with zero energy initial data, Dirichlet unit ball, T=1, beta1=gamma=1, beta2=0, target pi*e, and any fixed positive pointwise Hilbert norm cap rho. Let e be the normalized first radial mode with eigenvalue pi². Allow every fixed nu>=0 in the report's extra terminal-velocity cost.

KMv1 Theorem4.3 (printed19-21) states C² from L1(0,1;H) to the continuous-energy/Strichartz state space Y+ and displays a second-state forcing -20*ybar³*z1*z2. Its printed residual proof has a codomain defect: it claims its y derivative is onto every continuous energy pair. At zero that derivative is -(z,z_t), while F(t)=(0,t*g), g nonzero in H, is a continuous zero-initial energy pair with incompatible components and no preimage. This audit does not endorse that surjectivity assertion.

The local conclusion needed here is valid with an elementary compatible-space repair. Let Y+_0 be the Banach space of compatible position/velocity trajectories in Y+ with zero initial data. KM Lemma2.9 gives the bounded linear zero-data forcing map L:L1H->Y+_0. Interpolation gives Y+_0->L5L10, so N(y)=y^5 maps Y+_0 to L1H as a continuous polynomial. Use Phi(y,u)=y-L(u-N(y)) with codomain Y+_0. Its y derivative at(0,0) is the identity; the implicit-function theorem yields a local C² solution map with S(0)=0, S'(0)=L and S''(0)=0, since N'(0)=N''(0)=0. Small-data contraction or source uniqueness identifies it with the actual mild controlled state. This repair uses classical estimates and IFT; it is supplied here rather than falsely represented as the printed proof. Therefore Banach-space Taylor, with A=||u||L1H, gives

    y_u = z_u + R(u),   ||R(u)||Y = o(A²)   as A -> 0.                 (B1)

The little-o is uniform in direction, since the repaired local S is Fréchet C². This is weaker than the submitted independently verified O(A^5) bound and requires no global-existence construction beyond identifying the local mild solution. Endpoint position H and velocity H^-1 traces are continuous in Y+, so their remainder bounds follow. Also ||y_u||Y+=O(A). Every use of Y in(B1) can be read as Y+; the energy part alone also suffices for the endpoint bounds.

The elementary linear-wave eigenmode identity is

    <e,z_u(1)> = (1/pi) integral_0^1 sin(pi*t)<e,u(t)>dt <= A/pi.     (B2)

This follows by projecting the zero-data linear wave onto the first eigenmode; no assertion that the nonlinear state remains in that mode is used.

Write x=<e,y_u(1)>. Equations(B1)-(B2) imply
x <= A/pi + d(A)*A² with a nonnegative d(A)->0. Increasing d if necessary gives a bound uniform over all controls of mass at most A. The full terminal tracking square, the group-L1 cost, and nonnegative additional terms give

    J(u)-J(0) >= A - pi*x + x²/2.                                   (B3)

For small A, b(A)=A/pi+d(A)A² < pi. The scalar function A-pi*x+x²/2 is decreasing for every x<=b(A), so

    J(u)-J(0)
      >= A-pi*b(A)+b(A)²/2
      = A²/(2pi²) - pi*d(A)A² + d(A)A³/pi + d(A)²A^4/2
      >= A²/(4pi²)                                                 (B4)

once pi*d(A)<=1/(4pi²). This holds for every sufficiently small nonzero control, without a cap-density/bathtub estimate. For A=0, u=0 as an equivalence class. Thus zero is a genuine strict local optimizer in L1, and also in L2 (A<=||u||2 on T=1) and L-infinity (A<=||u||infinity). It satisfies the exact source's local premise. The positive cap can be arbitrary here; small fixed rho is required only for the stronger global assertion.

This local-optimality calculation is scalar algebra after the locally repaired C² statement. It does not transfer an unresolved central PDE/global-optimality claim into an assumption. Whether finding these data and this local-minimum certificate is a genuinely routine specialization or a modest new counterexample construction is a priority judgment, not settled by its short length.

## Exact critical cone and concentrating directions

The first derivative at zero is

    J'(0;v)= integral (||v(t)||H - sin(pi*t)<e,v(t)>)dt
            >= integral (1-sin(pi*t))||v(t)||H dt.                  (B5)

The lower bound is strictly positive for every nonzero L1 or L2 equivalence class: the only zero coefficient occurs at t=1/2, a null set. The pointwise-ball tangent is full by bounded truncation. Hence the ordinary source cone is {0}; its substitute second-order condition is vacuously positive, with exactly its convention j''(0;v²)=0. The subgradient lambda(t)=sin(pi*t)e and p=-lambda satisfy stationarity; the constraint multiplier is zero. The group-norm subgradient/threshold recipe is standard (HSW2012 Lemma2.2 and KM's first-order calculus).

For 0<h<min(rho,1/2), set u_h=h*e*1_{|t-1/2|<h}. Direct integration gives

    A_h=2h²,   r_h²=||u_h||2²=2h³,   ||u_h||infinity=h,
    z_h(1)=2h*sin(pi*h)/pi² * e,   (z_h)_t(1)=0.                    (B6)

The linear-plus-sparse loss is
L_h=2h²-2h*sin(pi*h)/pi=(pi²/3)h^4+O(h^6).
The terminal quadratic cost is (2/pi²)h^4+O(h^6).
Equation(B1) gives R(u_h)=o(A_h²)=o(h^4); its tracking-linear contribution is o(h^4). The quartic state cost is O(A_h^4)=O(h^8). The velocity term is o(A_h^4)=o(h^8) since its linear terminal velocity vanishes. Thus

    J(u_h)-J(0)=(pi²/3+2/pi²)h^4+o(h^4),
    [J(u_h)-J(0)]/r_h² ->0.                                       (B7)

This is a full counterexample to the core implication at the genuine local optimizer proved in(B4). It works in the source's L-infinity localization and the report's L2 localization. It uses the prior target-paper C² result and classical mode/norm calculations, not the stronger submitted nonlinear/global machinery.

## Abstract necessary-condition covering witness

BW2024 Theorem2.18 says positive norm-squared quadratic growth requires NDC in its general F+G setting. For this specialization:

- X=L2(0,1;H) is a separable Hilbert dual; take Y=X with its canonical duality.
- G=j+indicator(Uad) is proper, convex and norm-lower-semicontinuous; j is continuous in L2, and Uad is closed convex there.
- F is the terminal tracking plus nonnegative smooth state/velocity costs. KM Lemma4.6's stated calculus and the repaired local(B1) give a second-order Taylor expansion at zero in L1, hence in L2 since A<=||u||2. The extra velocity composition has the same expansion by its continuous trace.
- F'(0)v=-integral sin(pi*t)<e,v(t)>dt is a bounded L2 form.
- F''(0)[v]^2=||z_v(1)||H²+nu*||(z_v)_t(1)||H^-1². The quartic state cost and S''(0) contribute zero.

Set v_h=u_h/r_h. Then ||v_h||2=1 and v_h converges weakly to zero: for any L2 test w, Cauchy-Schwarz bounds |<v_h,w>| by the L2 norm of w restricted to the shrinking interval, which tends to zero. Feasibility holds and r_h->0. The expression in NDC equals

    [G(u_h)-G(0)+F'(0)u_h]/r_h² + F''(0)[v_h]^2/2
       = 1/h - sin(pi*h)/(pi*h²) + sin²(pi*h)/(pi^4*h)
       = (pi²/6+1/pi²)h + O(h³) ->0.                              (B8)

Therefore that prior abstract theorem excludes L2-squared growth in an L2 neighborhood at zero. It is applicable and not dismissed because its concrete applications are parabolic. The L-infinity localization is covered directly by(B7), not automatically by a theorem formulated in L2. Alternatively, apply BW to G restricted to the closed cap ||u(t)||H<=min(rho,sigma), for an arbitrary fixed sigma>0: if a positive growth estimate held within an L-infinity radius epsilon, taking sigma<epsilon would imply L2 growth on this smaller set, contradicting the same NDC pulses. The local optimizer/cone(B1)-(B5) supplies a complete CURRENT application, but it does not by itself prove that an earlier source resolved the existential model-specific question.

CW2018 Theorem4.4/Lemma5.1 and CT2012's A2/(2.5) are earlier explanations of the same weak-null obstruction. The submitted Hessian is not Legendre: v_h is normalized and weakly null while F''(0)[v_h]^2 ->0. At zero, inactive Hilbert caps have zero multiplier and cannot supply active-boundary curvature. CW's Example5.13 ball curvature term does not rescue this example.

## Sparse-threshold and weaker-norm credit boundary

For q(t)=1-sin(pi*t), the exact size of its small-level set is

    |{q<=delta}| = (2/pi) arccos(1-delta)
                 ~ (2sqrt(2)/pi) sqrt(delta).                     (B9)

The O(delta) condition in WW2011 Theorem3.7 and the transversal-threshold hypotheses in WW2022 Assumption4.12 fail at this quadratic contact. Those specialized theorems are not directly covering proofs for this example.

This does not make the L1-squared estimate(B4) a new abstract principle: it is an elementary tracking-square consequence of established local state differentiability. The norm cap always gives ||u||2²<=rho*||u||1. Quadratic growth versus a linear datum perturbation and this interpolation explain the optional basepoint L1/L2 upper rates through established stability reasoning. No pairwise Lipschitz selection or sharp optimizer asymptotic is certified here.

## Source boundary: no universal inference from the final unregularized note

BW2024's final §4 sentence saying NDC cannot be satisfied for nu=0 cannot be used as a universal theorem for all sparse admissible data. For instance, zero initial data and zero target with scalar box |u|<=M and unregularized mu*||u||1 yield J(u)>=mu*||u||1>=(mu/M)||u||2². For j3, ||u(x)||L2time<=M*sqrt(T) similarly gives j3(u)>=||u||2²/(M*sqrt(T)); group temporal L1 with a norm cap has the analogous bound1/rho. These strict-margin examples can satisfy NDC. The quoted note is overbroad if read universally; the present obstruction uses the explicit threshold calculation(B8), not that sentence.

## Priority conclusion under the clarified gate

The mathematical bridge is complete for the narrow obstruction at a genuine local optimizer, subject to the explicit local source-proof repair above. The earlier NDC theorem genuinely encompasses its functional setting once the construction is supplied. The inspected sources do not themselves supply the chosen eigenmode target, the zero-cone construction and genuine local-optimum certificate as an existential wave result. A new proof using old theorems is not automatically prior resolution, and elementary length alone does not certify “routine specialization.” No earlier complete or automatic covering witness has been authenticated. The generic mechanism requires full classical credit; any model-specific contribution is correspondingly modest and precisely scoped. Stronger global/perturbation auxiliary claims cannot be required of earlier coverage or used to redefine the core question.
