# Author approach 1: test the connection-replacement argument at the cusp

Problem 30004711. 7 October 2026. First substantive mathematical approach; no novelty is claimed for Chern–Weil theory or the split super-symplectic construction.

## Goal and result

Attempt to derive the literal torsion/Euler representative comparison by replacing the torsion super-symplectic form with one built from Norbury's canonical Chern connection. The local algebra permits this replacement at the level of ordinary cohomology. The global integral step requires a boundary-transgression estimate that the local algebra does not supply.

We derive the exact missing functional and give an explicit finite-volume counterexample to the unrestricted invariance principle. The example has identical underlying bundle, fibre metric, body symplectic form, and cohomology throughout a nondegenerate deformation. Nevertheless its volume varies by an arbitrary prescribed real amount. This is a counterexample to a proposed general lemma, not to the OWR problem.

## 1. The source step being tested

[Stanford–Witten, 1907.03363v5](https://arxiv.org/abs/1907.03363v5), Appendix A.2, printed p.111 / PDF p.112, writes a split super-symplectic form as omega_hat=pi^*omega+d lambda and replaces lambda by an expression using any SO(m) connection. Formulae (A.14)–(A.17) then compute the resulting split-model integral using its Euler form.

The algebraic computation for a fixed connection can be checked locally. Invariance of the total integral under the replacement is a separate statement. Nondegeneracy and finiteness alone do not imply it on a noncompact space.

## 2. Exact reduction to a boundary functional

Let S be an oriented manifold or smooth orbifold of dimension 2d and F an oriented real rank-2r bundle. Assume d>=r>=1 for the factorial and boundary formulas below. If r>d, the Euler form already exceeds the body dimension and its volume contribution is zero. Fix a closed two-form omega. Let A_0,A_1 be metric connections on the same oriented bundle and define A_t=A_0+t(A_1-A_0), a=A_1-A_0. Use the polarized degree-r Pfaffian P, normalized so P(X,...,X)=Pf(X). Define

CS_e(A_0,A_1)=r/(2 pi)^r integral_0^1 P(a,F_(A_t),...,F_(A_t)) dt.

The derivative of the curvature is d_(A_t)a. Invariance of P and the Bianchi identity d_(A_t)F_(A_t)=0 give

d/dt Pf(F_(A_t))=r d P(a,F_(A_t),...,F_(A_t)).

Integrating in t proves

e(A_1)-e(A_0)=d CS_e(A_0,A_1).

For any relatively compact smooth exhaustion domain S_R, Stokes' theorem therefore gives the exact identity

integral_(S_R) (e(A_1)-e(A_0)) omega^(d-r)/(d-r)!
 = integral_(boundary S_R) CS_e(A_0,A_1) omega^(d-r)/(d-r)!.

The same calculation applies in orbifold charts with their usual stabilizer weights and hence descends to stack integration. It requires no compactification. If both improper integrals on the left converge, their difference is the limit of the displayed boundary integral. Convergence does not set its value to zero.

For the stable all-NS problem with g>=1, d=3g-3+n and r=2g-2+n, so d-r=g-1. In stable genus zero r=n-2>d=n-3, and the volume vanishes by degree; the factorial formula is not applied there. The precise condition needed to identify the two volumes is

B(A_0,A_1;L):=lim_R integral_(boundary S_R)
 CS_e(A_0,A_1) omega(L)^(g-1)/(g-1)! = 0,

or the appropriate nonzero value if the target uses a different normalization. This formula is conditional on having first identified the actual two connections on the same oriented bundle. It does not invent a torsion connection that has not been constructed.

## 3. Explicit finite-volume counterexample to the generic shortcut

Take S=C^*=R times S^1, with coordinates t=log|z| and theta modulo 2 pi. Put

q(t)=e^(2t)/(1+e^(2t)),
q'(t)=2e^(2t)/(1+e^(2t))^2,
omega=q'(t) dt wedge dtheta.

Then omega is symplectic and integral_S omega=2 pi. Let F be the trivial oriented real rank-two bundle with its fixed Euclidean metric. Choose J in so(2) with Pf(J)=1. For any c in R define metric connections

A_0=0,
A_1=c q(t) J dtheta,
A_s=s A_1, 0<=s<=1.

Because so(2) is abelian,

F_(A_s)=s c q'(t) J dt wedge dtheta,
e(A_s)=s c/(2 pi) q'(t) dt wedge dtheta.

Consequently

integral_S e(A_s)=s c,
integral_S |e(A_s)|=|s c|.

The Euler forms are all exact, since e(A_s)=d[s c q(t)dtheta/(2 pi)]. They represent the same ordinary class on S and use the same bundle, metric, and orientation. The Chern–Simons form from A_0 to A_s is s c q(t)dtheta/(2 pi). On the exhaustion S_R=[-R,R] times S^1,

integral_(boundary S_R) CS_e = s c(q(R)-q(-R))
 = s c (e^(2R)-1)/(e^(2R)+1) -> s c.

All integrals converge absolutely. The failure of exact-form invariance is exactly the nonzero cusp boundary term.

This is not merely an unrelated ordinary two-form example. On the split supermanifold Pi F of dimension 2|2, use the fixed negative Euclidean odd metric and form

Omega_s=pi^*omega+d lambda_(A_s),

where lambda_(A_s) is the connection expression in SW (A.10). The body and odd blocks are omega and the fixed nondegenerate negative metric, so every Omega_s is nondegenerate. The forms differ by exact terms and have the same body restriction. With the same split retraction and consistent Berezin orientation, the local Gaussian/Berezin calculation (A.14)–(A.17) gives

Vol_s=integral_S e(A_s) exp(omega)=s c,

since e(A_s) already has the body's top degree. Hence exact deformation, nondegeneracy, fixed odd metric, and finite total integral still do not guarantee invariant total super-volume.

The qualification “same split retraction” matters. For noncompact superintegration, a nilpotent change of even coordinates can itself introduce boundary contributions; unrestricted retraction-independence is not an alternative proof of invariance. Compact support, compactness, or suitable uniform boundary control would remove this particular obstruction. None is inferred here solely from finite volume.

This construction uses arbitrary metric connections, as allowed in the generic replacement argument. It does not assert that they are all the Chern connection for one fixed holomorphic structure; uniqueness of that Chern connection is fully respected.

## 4. What would be needed for the actual genus-one target

In genus (1,1), r=d=1, so the Weil–Petersson exponential contributes only its constant term. Suppose an actual comparison has put the torsion representative and the canonical one on the same oriented spin bundle, with no additional parity weights or stack normalization. Let epsilon=+1 for the dual complex orientation and epsilon=-1 for the original F orientation, and write

V_tau=epsilon W+B_tau,

where B_tau is the limiting transgression integral in those fixed conventions. The independently established algebraic values are W=1/16 and V^Theta=1/8. Thus the coefficient-one target would require

B_tau=1/8-epsilon/16.

It requires B_tau=1/16 in the dual convention, or B_tau=3/16 in the original F convention. If a valid comparison instead proves B_tau=0, it disproves that strengthened coefficient-one statement under those conventions. The bundle extension alone proves neither value.

For an exhaustion removing disks around the compactification cusps, rank-one B_tau becomes a weighted sum of boundary integrals of the connection-difference one-form divided by 2 pi. The boundary orientation and orbifold stabilizer weights must be retained. Explicit asymptotics of the actual torsion-induced retraction/connection at every cusp would therefore suffice to decide the genus-one comparison. We have not obtained these asymptotics from the inspected sources.

## 5. Comparison with the available hyperbolic construction

[Norbury, 2608.25237v2](https://arxiv.org/abs/2608.25237v2), section 4.1.3, pp.27–28, defines a connection by harmonic projection. Its Exercise 7 asks for a comparison with the holomorphic Euler measure; p.29 proposes the bordered analogue. This provides a concrete prospective connection to analyze. It does not identify it with the torsion-induced supermeasure, nor supply the necessary cusp estimates.

Once both are well-defined metric connections on one oriented bundle, the ordinary exactness portion is given by section 2 above. The integrated conclusion still needs B=0. If their bundles, metric compatibility, or orientation identification differ, those must be checked before even applying the transgression formula.

## 6. Outcome

The proposed proof by arbitrary connection replacement does not close the literal OWR identity. We have proved why the generic invariance premise is insufficient and reduced the remaining step to a precise boundary functional, with explicit numerical requirements in genus one. No actual value of B_tau has been inferred from the toy example or from matching recursions.

Supported status: one genuine mathematical approach completed, canonical normalized identity already known, original convention/representative comparison still pending. This is not a final unsolved disposition and not a claim that the comparison is absent from all literature.
