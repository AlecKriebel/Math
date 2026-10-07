# Approach 1: transfer standard Galerkin quasi-optimality

## Aim and disposition

Try to turn coercivity of convection-diffusion into best-mesh rate optimality. The ordinary Céa argument works at a fixed positive diffusion parameter; the explicit finite-element example below shows why its constants cannot simply be made uniform. This is a restricted obstruction to a proof route, not a counterexample to adaptive rate optimality.

## Proposition 1.1 (fixed-space transfer)

Let X be a real Hilbert space, b a bounded bilinear form with
b(v,v) >= alpha ||v||_X^2 and |b(w,v)| <= M ||w||_X ||v||_X,
where alpha>0. If u solves b(u,v)=F(v), and u_T in a finite-dimensional subspace X_T solves the same equation for v in X_T, then

||u-u_T||_X <= (M/alpha) inf_{w in X_T} ||u-w||_X.

Indeed, put e=u-u_T. Galerkin orthogonality gives b(e,u_T-w)=0, so alpha||e||^2 <= b(e,e)=b(e,u-w) <= M||e||||u-w||. Cancel ||e|| unless it is zero and take the infimum. Consequently, if a mesh selector already gives best-approximation error O(N^-s), its Galerkin solutions inherit the exponent. This does not construct such a selector.

## Proposition 1.2 (actual one-dimensional finite-element obstruction)

On (0,1), solve -epsilon u''+u'=f_epsilon with homogeneous Dirichlet boundary conditions and epsilon>0. Use the energy norm ||v||_epsilon^2=epsilon integral_0^1 |v'|^2 and the single-element conforming quadratic space X_T=P_2(0,1) intersect H_0^1(0,1). Define

phi=x(1-x), psi=x(1-x)(x-1/2), u=psi,
f_epsilon=-epsilon psi''+psi'.

Thus X_T=span{phi}; these are polynomial data and a genuine finite-element Galerkin problem. Integration by parts gives b(v,v)=||v||_epsilon^2. Exact polynomial integrations give

integral phi'^2=1/3,
integral psi'^2=1/20,
integral psi' phi'=0,
integral psi' phi=1/60,
integral phi' phi=0.

Writing u_T=c phi, the Galerkin equation is c epsilon/3=1/60, hence c=1/(20 epsilon). The energy-best approximation is zero because psi and phi are energy orthogonal. Pythagoras yields

||u-u_T||_epsilon^2 / inf_{w in X_T}||u-w||_epsilon^2
= 1 + 1/(60 epsilon^2).

Therefore there is no constant independent of epsilon bounding this unmodified Galerkin error by the same-space best energy error, even for this smooth family. This concerns one fixed coarse quadratic element in one dimension. It makes no assertion about two-dimensional SUPG, eventual fine meshes, the best-mesh exponent at fixed epsilon, or every adaptive algorithm. The forcing changes with epsilon, as allowed in a uniform-in-data quasi-optimality assertion.

## Remaining gap and credit

Céa's lemma and the use of coercivity are classical. The example is an elementary diagnostic, with no novelty claim. The missing step is a realizable best-mesh selector together with constants and an onset appropriate to the chosen robustness interpretation. The known stationary SUPG result is recorded separately in SOURCE_SCOPE.md; it already supplies a fixed-problem asymptotic rate theorem under its own hypotheses.
