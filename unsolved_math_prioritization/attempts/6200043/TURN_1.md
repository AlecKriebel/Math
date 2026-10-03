# Recovery proof turn 1: porous-image route and its precise obstruction

Date: 2026-10-03. Historical author count unknown; recovery author count 1/5. Original target unresolved. Completion estimate 10%, subjective coverage of approaches, not a probability of solution. This turn investigates whether one missing point can be amplified to holes at every scale.

## The credited obstruction

Let X be a compact metric space which attains its finite Ahlfors regular conformal dimension. If f:X→X is quasisymmetric, its image Y=f(X) cannot be uniformly porous in X. Indeed f is a quasisymmetric homeomorphism X→Y, so ARCdim(Y)=ARCdim(X). Carrasco–Mackay Proposition 8.3 rules out a porous subset with this equality when the ambient dimension is attained. This uses their full statement, which incorporates the regularization step for a subset that need not itself be Ahlfors regular. No unjustified regularity of Y is assumed.

For an Ahlfors Q-regular Q-Loewner X, the standard positive-modulus conformal-dimension theorem gives attained conformal dimension Q. Thus the obstruction applies in the source setting. It is an explicitly credited consequence, not a solution or novelty claim.

## A concrete hole-propagation criterion

Here is a separately proved, stronger-than-necessary hypothesis under which the route closes. Suppose X is compact, Y⊂X is closed and nonempty, and for every y∈Y and every sufficiently small r>0 there is a homeomorphism g:X→X with g(Y)=Y and a point z in a fixed open ball B(a,s)⊂X\Y such that:

1. g(B(a,s)) contains B(g(a),c r), for a constant c>0 independent of y,r;
2. g(B(a,s))⊂B(y,r).

Then Y is uniformly porous at all sufficiently small scales: the ball B(g(a),c r) lies in B(y,r)\Y because g preserves Y. Compactness upgrades small-scale porosity to all scales up to diam X: if the criterion holds for r≤r0, use radius r0/2 at y for r>r0 and reduce c by the positive factor r0/(2 diam X). Hence no proper QS image of an attained-dimension X can satisfy this criterion.

The formulation is deliberately explicit about g(Y)=Y. Ambient self-similarity of X alone supplies no such equality for an arbitrary embedding image. Conjugating a boundary group action by f only defines transformations on Y, not on all X; it does not provide images of an ambient complementary ball.

## Why a missing ball does not suffice

On X=[0,1]^n, f(x)=x/2 is a similarity onto Y=[0,1/2]^n. Y is proper, closed and has a missing ambient ball, but it contains a relatively open set. For y in the Euclidean interior of Y, all sufficiently small ambient balls B(y,r) lie inside Y; therefore Y is not porous. This elementary example falsifies the proposed implication 'proper QS image ⇒ porous' without group-boundary structure. It is not a source counterexample: the cube is not asserted to be the visual boundary of a hyperbolic group. Any use of its analytic regularity or Poincare properties is unnecessary for this countermodel.

## Exact remaining gap

We have not shown that an arbitrary proper QS image in a Loewner hyperbolic-group boundary satisfies hole propagation, nor that it is porous by another mechanism. The source conjecture cannot be deduced merely from attained conformal dimension and a missing open ball. Subsequent turns must investigate the additional group or dynamical structure rather than reassert this implication.
