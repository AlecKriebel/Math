# Actual source-first adversarial hand controls — row184

2026-11-17 UTC. Derived after personally reading the actual257-line/four-page manuscript and fresh own four pixels, before new foreign proofs, support code, old opinions/results or current scope/root findings. The source itself necessarily gives its proof. The following checks are my own explicit reconstruction and attempts at falsification; they do not certify the unread printed-question/definition interfaces.

## 1. First variation, rank and all-center quantifiers

Let η_q(u) be the∇0-affine[0,1] path from a fixed p to q in a smooth convex geodesic branch. Set E(q)=1/2∫h0(T,T)du. In an endpoint variation F(s,u), the coordinate fields commute, so torsion-freeness gives∇_VT=∇_TV. Differentiating with metric compatibility and integrating gives

    dE_q(w) = ∫h0(∇_TV,T)du
            = [h0(V,T)]_0^1 − ∫h0(V,∇_TT)du
            = h0(w,T(1)).

The affine geodesic equation kills the integral; the initial endpoint fixes V(0)=0. Since q≠p, uniqueness of the geodesic ODE implies T(1)≠0. Positive definiteness then gives dE(T(1))=|T(1)|²>0. Consequently D=ker dE has constant rank n−1 off p. For X,Y in D, dE([X,Y])=X(dE(Y))−Y(dE(X))=0; equivalentlyα∧dα=0 forα=dE. Regular level sets supply local integral hypersurfaces at every q. The argument works for every fixed center and smooth convex branch; it never needs a globally minimizing distance function or a single global choice of geodesic outside the cut locus.

On a small normal product neighborhood, the additional explicit control is E=(r²+b²)/2, where r is the spherical geodesic distance and b is the Euclidean displacement norm in the relevant flat factor. These level sets are round in normal coordinates, not product coordinate slices. At p, dE=0, so one cannot assert the same rank distribution there. At a spherical antipode the connecting geodesic is nonunique, so extending the formula across that cut locus is outside the claim. Positive definiteness matters: a nonzero null terminal vector in an indefinite metric would not give this rank test. General statistical∇ is not silently substituted for the compatible∇0.

## 2. Curvature-change identity with a sign/potential check

For V=gradφ, put B(X,Y)=−h0(X,Y)V. Since∇0h0=0,

    (∇0_XB)(Y,Z) = −h0(Y,Z)∇0_XV,
    B(X,B(Y,Z)) = h0(Y,Z)h0(X,V)V.

Subtract the X/Y-swapped terms in the exact curvature difference law. It gives

    Rhat(X,Y)Z = R0(X,Y)Z − h0(Y,Z)A(X) + h0(X,Z)A(Y),
    A(X)=∇0_XV−dφ(X)V.

Thus Rhat=0 requires the printed arbitrary-endomorphism equation. No hidden Hessian symmetry assumption is necessary for the impossibility proof. As an independent sign check, for f=e^−φ>0,

    ∇0_Xgrad f = f[dφ(X)V−∇0_XV],
    A(X)=−f^−1∇0_Xgrad f.

Hence the sphere-plane equation would force the Hessian of f along e1 to be−f e1, while the mixed flat plane forces it to be0. Since f>0, these cannot agree. This excludes every possible smooth conformal factor, not just a guessed constant or radial φ. The metric exponent and the connection term have been kept together; changing the exponent while leaving the coefficient fixed could change the definition.

The proposed change remains statistical in this convention: directly,

    (∇hat_X hhat)(Y,Z)
      = e^φ[dφ(X)h0(Y,Z)+dφ(Y)h0(X,Z)+dφ(Z)h0(X,Y)],

which is fully symmetric, and B is symmetric in X,Y. Thus the obstruction tests genuine allowed statistical changes, rather than flat arbitrary affine connections unrelated to the statistical pair.

## 3. An independent arbitrary-A isotropy/trace attack

Assume at one point that a Levi–Civita curvature tensor has the asserted form for an **arbitrary** linear endomorphism A. For orthonormal ei,ej with i≠j,

    R(ei,ej)ej = A(ei).

Skew-adjointness of R(ei,ej) gives <Aei,ej>=0 for every j≠i. Thus A is diagonal in this basis, Aei=λi ei. Pair symmetry of sectional curvature gives λi=λj for every i≠j. Hence A=λId and all sectional curvatures at that point must agree. This argument imposes no gradient/PDE ansatz and no assumed self-adjointness of A.

The product S²(1)×R has sphere tangent plane curvature1 and mixed plane curvature0 at every point, so it fails this necessary algebraic isotropy condition. Every added Euclidean factor leaves one of each kind of plane. The original two evaluations are thereby corroborated by a full-A symmetry argument, not an incomplete diagonal guess.

A trace control also reconstructs the unique candidate from the linear system: tracing R(ei,Y)Z gives

    Ric(Y,Z)=tr(A)h0(Y,Z)−h0(A(Y),Z),
    scalar=(n−1)tr(A).

For the product, Ric has entries1,1,0,...,0 and scalar2. Thus the only possible A is[2/(n−1)]Id−Ric^sharp. In n=3 this is diag(0,0,1), contradicting the sphere equation A(e1)=e1. In general its e1 entry is2/(n−1)−1, which could equal1 only at n=2. This independently exposes the rank inconsistency without a computer solving a restricted subsystem.

In the stated curvature convention, the auxiliary projective-Weyl evaluation is also consistent: for n=3, W(e3,e1)e1=0−(1/2)e3. In the higher-dimensional product the analogous coefficient is−1/(n−1), not a dimension-independent−1/2. The manuscript uses the displayed1/2 calculation in its three-dimensional example and uses its separate A contradiction for the dimensional extension. Exact external projective/Ricci sign conventions remain to be compared later.

## 4. Dimension, scaling and ordinary-conformal controls

The mixed-plane contradiction needs at least three tangent directions. On a unit sphere alone, the pointwise condition is compatible with A=Id. On any open hemisphere let f be a positive height coordinate. The elementary embedded-sphere Hessian is Hess f=−f h; φ=−log f then gives A=Id and Rhat=0 by the transformation identity. Thus blindly applying the product obstruction to S² alone would be false. This is an actual limiting/domain control, not an asserted dimension-two counterexample. In one dimension every zero-rank radial distribution is integrable and curvature supplies no such contradiction.

For sphere radius r>0, the two plane curvatures are r^−2 and0; the same contradiction survives every finite r. It disappears in the flat r→∞ limit, as it should. In Euclidean space radial hyperplanes are ker d(|q−p|²/2) and the original flat connection is already1-conformally flat with constant factor. Integrability alone is therefore not a curvature detector.

In dimension3, ordinary conformal flatness is an especially useful falsifier of a wrong interpretation. The global map(x,t)↦e^t x from S²×R to R³\{0} pulls the Euclidean metric back to

    dr²+r²g_S² = e^(2t)(dt²+g_S²) = e^(2t)h0.

Thus the metric h0 **is** ordinarily conformally flat, while the statistical-connection obstruction above remains. The deformation metric e^t h0 is also in that ordinary conformal class. This does not contradict the note; it confirms why replacing statistical1-conformal flatness by ordinary metric conformal flatness would invalidate the target. This control is only for the3-dimensional product; no ordinary-conformal classification in higher dimensions is inferred.

## 5. Complete deformation and dual differentiation

Writeα=dt, D_XY=α(X)Y+α(Y)X and h1=e^t h0. The torsion is zero because D is symmetric. Since∇0_Xh1=α(X)h1, subtracting the two D terms gives

    (∇1_Xh1)(Y,Z)
      = −α(X)h1(Y,Z)−α(Y)h1(X,Z)−α(Z)h1(X,Y).

It is fully symmetric and its value on three∂t vectors is−3e^t, never0. This verifies statisticality and the nowhere-zero-cubic claim at all finite t, not merely at t=0 or in a frame with a hidden normalization.

In the defining dual identity the α(X)h1(Y,Z) from differentiating e^t cancels the corresponding D term. The remaining correction E satisfies h1(Y,E_XZ)=−α(Y)h1(X,Z), so

    (∇1)*_XZ = ∇0_XZ − h1(X,Z)α^sharp_h1
               = ∇0_XZ − h0(X,Z)∂t.

The conformal gradient scaling α^sharp_h1=e^−t∂t is essential. A useful coordinate consistency check is∇1_tt=2∂t, (∇1)*_tt=−∂t, whose average is(1/2)∂t, exactly the Levi–Civita value for h1. In a horizontal unit direction the corresponding average has vertical term−(1/2)∂t. Thus∇1 itself is not the Levi–Civita connection of its conformal metric, and the claimed non-self-duality is not just a terminology change.

## 6. Exact affine reparametrization and radial multiplier

Let η(u) be a∇0-affine geodesic from p to q, u∈[0,1], with t(u)=t_p+bu and b=t_q−t_p. For s=s(u), the∇1 geodesic equation is

    −s''/s' + 2t'(u)=0,
    s'(u)=C e^(2t(u)).

This checks the sign and exponent2 directly; its reciprocal would solve the wrong equation. Normalize s(0)=0,s(1)=1 by C=1/I, I=∫_0^1e^(2t(u))du. Both C and s' are finite positive on every compact segment, so endpoint velocities differ by a smooth nonzero scalar and the same trace lies in the same convex domain. No global affine completeness is required.

The actual radial one-form for(∇1,h1), rather than just its kernel, is

    h1(γ'_s(1),w)
       = e^(t_q) I e^(−2t_q) h0(η'_u(1),w)
       = [e^(t_p) sinh(b)/b] dE0_q(w).

The multiplier has positive smooth continuation e^(t_p) at b=0. Thus D1=D0 for every center and the whole allowed convex domain, with a checked zero-vertical-displacement limit. In particularα1=f dE0 andα1∧dα1=f²dE0∧d²E0=0. The stronger claim thatα1 is itself closed is generally false and not needed: locally E0=(r²+b²)/2, so dα1=f'(b)r db∧dr can be nonzero for b≠0,r>0. This separates Frobenius integrability from an unjustified new energy identity for the deformed connection.

Pure vertical paths give a second exact control: e^(2t(s))=(1−s)e^(2t_p)+s e^(2t_q), so t'_s(1)=(1−e^(−2b))/2. Hence h1(γ'_s(1),∂t)=e^(t_p)sinh b, agreeing with the multiplier times dE0(∂t)=b. At b=0, horizontal geodesics keep their affine parameter and h1 merely rescales orthogonality by e^(t_p).

As t→−∞ the metric h1 has a finite vertical length end, and some complete∇0 geodesics acquire a finite affine s endpoint. This does not refute the compact-segment/local-convex assertion, but forbids silently adding global completeness to the non-self-dual proposition.

## 7. Universal dual obstruction and scalar deformation controls

For any local ψ,

    h1(X,Y)grad_h1ψ = h0(X,Y)grad_h0ψ,
    (∇1)*_XY − h1(X,Y)grad_h1ψ
      = ∇0_XY − h0(X,Y)grad_h0(t+ψ).

The changed metric is also e^ψh1=e^(t+ψ)h0, so this is the entire same allowed1-conformal pair, not only a coincident connection formula. Flatness would contradict the arbitrary-A obstruction at each point. The tempting candidate ψ=−t just returns h0/∇0, which is still curved; ruling out that candidate alone would not suffice, whereas the composition identity rules out all candidates.

As a factor/sign/limit test, replace t everywhere by ct: h_c=e^(ct)h0 and∇c=∇0+c[α(X)Y+α(Y)X]. Direct differentiation yields cubic−c sym(α⊗h_c), dual∇c*=∇0−c h0⊗∂t, reparametrization s'=C e^(2ct), and combined potential ct+ψ. At c=0 the cubic vanishes and the original self-dual example is recovered; at c=1 these are precisely the printed formulas. This is a hand control of the actual example, not a substitute theorem, extended repair or proposed follow-up. The nonzero cubic is a genuine pointwise property, while the negative answer does not depend on insisting that all statistical structures have nonzero cubic.

## Exact remaining gate

All original internal formulas and their quantified local arguments have actual source-only checkable reconstruction. The manuscript's named-question interpretation, the exact1-conformal convention in the genuine primary, and the precise Matsuzoe attribution are not yet independently read. A changed convention or extra hypothesis in those actual interfaces could alter the full-original disposition even if these calculations remain valid. Those gates must be checked only after the requested INITIAL/checkpoint hold; no native finite system or old opinion can resolve them. No final verdict or priority certificate is issued here. Follow-up defaults null.
