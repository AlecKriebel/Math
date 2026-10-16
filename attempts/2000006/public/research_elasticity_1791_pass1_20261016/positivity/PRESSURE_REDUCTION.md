# A global pressure estimate and a conditional whole-boundary positivity theorem

E-6322, mathematical pass 1, 2026-10-16.

**Status: a rigorous conditional reduction, not a proof of E-6322.** The initial W^{1,6} class does not supply the extra gradient integrability or regularity assumed below. This note shows exactly what those additional estimates would buy, including at the boundary.

## 1. The justified distributional equation

Let y be any full-class global minimizer from the frozen target. Write F=Dy, K=cof F and J=det F. The inner-variation calculation in `../variations/VARIATIONAL_AUDIT.md`, Sections 1–4, establishes

div E(Dy)=0,

where

E(F)=3dJ^{-2} I+Q(F),

Q(F)=[a|F|^6-2b|K|^3-cJ^2]I
     -6a|F|^4 F^T F+3b|K|K^T K.

Equivalently, for every vector field phi in C_c^infinity(Omega;R^3),

3d integral_Omega J^{-2} div phi
= -integral_Omega Q(Dy):Dphi.

All terms are initially in L^1. This identity is derived by material composition variations, which preserve the determinant constraint. It is not the unproved ordinary additive Euler-Lagrange equation.

The polynomial-minor inequalities |cof F|<=C|F|^2 and |det F|<=C|F|^3 give

|Q(F)| <= C(a+b+c)|F|^6.

In particular, any independently established bound Dy in L^{6q}(Omega) gives Q(Dy) in L^q(Omega).

## 2. A global negative-norm lemma, with no pressure boundary data

Let Omega be a bounded connected Lipschitz domain, let 1<q<infinity, and suppose p belongs to L^1(Omega) and Q belongs to L^q(Omega;R^{3x3}). If

integral p div phi = -integral Q:Dphi

for every compactly supported smooth vector test field, then p belongs to L^q(Omega) and

||p-p_Omega||_{L^q(Omega)} <= C(Omega,q)||Q||_{L^q(Omega)}.

Here p_Omega is the ordinary finite L^1 mean. No trace of p is prescribed or used.

One direct justification is the Nečas negative-norm theorem: the test identity bounds ||grad p||_{W^{-1,q}} by ||Q||_q, and that theorem controls the L^q norm modulo constants from this negative norm. Crucially, it applies with p initially only in L^1; one need not assume the conclusion to legitimize the argument.

For clarity, the standard divergence-right-inverse proof also identifies the noncircular duality step. For smooth compactly supported scalar f of mean zero, choose a Bogovskii test field Bf which is smooth and compactly supported, has div Bf=f, and satisfies

||D(Bf)||_{q'} <= C||f||_{q'},

where q'=q/(q-1). Then

|integral p f| <= C||Q||_q ||f||_{q'}.

Thus the distribution p restricted to mean-zero test functions extends to a bounded functional on the mean-zero subspace of L^{q'}. By duality it is represented by an L^q function modulo a constant distribution. The initial L^1 assumption identifies a finite constant and gives the asserted estimate after fixing the mean. No testing with the unproved L^q function |p|^{q-2}p is needed at the outset.

Primary theorem checks:

- D. Breit and A. Cianchi, *Negative Orlicz-Sobolev norms and strongly nonlinear systems in fluid mechanics*, arXiv:1401.4885v2. Equations (1.1)–(1.2), pp.1–2, explicitly state this negative-norm equivalence for every u in L^1 on a bounded Lipschitz domain and every exponent strictly between one and infinity. https://arxiv.org/pdf/1401.4885
- J. Wichmann, *Temporal Regularity of Symmetric Stochastic p-Stokes Systems*, Journal of Mathematical Fluid Mechanics (2024), Appendix A, Theorem 34, records the compact-support-preserving smooth Bogovskii mapping and its Sobolev bounds; the pressure reconstruction in Section 3.2 uses this duality approach. https://doi.org/10.1007/s00021-024-00852-9 . This second source was independently checked by the pass reviewer.

## 3. Exact consequence for E-6322

Apply the lemma with p=3dJ^{-2}. For every 1<q<infinity for which Dy belongs to L^{6q}(Omega),

||J^{-2}-(J^{-2})_Omega||_q
<= C(Omega,q)(a+b+c)/d * ||Dy||_{6q}^6.

The mean is already bounded by the finite energy:

(J^{-2})_Omega <= I(y)/(d|Omega|).

Consequently an independently bounded gradient, Dy in L^infinity(Omega), yields

J^{-2} in L^q(Omega) for every finite q,

or equivalently J^{-s} in L^1(Omega) for every finite s>0.

This is a whole-domain integrability conclusion. Merely solving a local scalar Poisson equation and retaining an unspecified harmonic remainder would obscure that point; the full first-order distributional pressure identity is what permits the global negative-norm estimate.

At the target's baseline Dy in L^6, Q is only in L^1. The q=1 endpoint does not furnish the asserted inverse estimate; the cited negative-norm equivalence fails at that endpoint. Thus substituting q=1 and then claiming a higher moment would be an invalid bootstrap. This is a concrete location of the remaining integrability gap.

## 4. Conditional positivity including the entire boundary

### Theorem

Let y be a global minimizer in the frozen target, and assume additionally that y belongs to C^{1,beta}(closure Omega;R^3) for some beta>0. Then

min_{closure Omega} det Dy > 0.

More generally the same conclusion follows if Dy is globally bounded and J has a beta-Hölder continuous representative on the closure, for any beta>0. An even more precise version needs only Dy in L^{6q} and J in C^{0,beta} on the closure for some q>1 satisfying 2q beta>=3.

Proof. The additional hypotheses give bounded Dy, hence every finite inverse-Jacobian moment by Section 3. The determinant is Hölder continuous on the closure and is nonnegative there, since it is positive almost everywhere inside.

Suppose J(x0)=0 at any point x0 of the closure. Hölder continuity gives

0<=J(x)<=C|x-x0|^beta.

Choose finite q>1 such that 2q beta>=3. The smooth domain has an interior cone at x0; if x0 is an interior point, take an ordinary ball. On the cone,

J(x)^{-2q} >= C^{-2q}|x-x0|^{-2q beta}.

Its three-dimensional integral diverges for 2q beta>=3, including logarithmically at equality. This contradicts J^{-2} in L^q(Omega). Thus no interior or boundary zero exists. Compactness yields the asserted positive lower bound. For the finite-q variant, apply exactly this last argument with the single given q. QED.

The theorem applies to every positive coefficient quadruple and every allowed smooth connected domain, including domains with holes. It assumes the same full-class minimizer; it does not replace that minimization problem by a smooth comparison class. Its sole extra hypothesis is regularity of that minimizer.

## 5. What this does and does not improve

The companion `REGULARITY_AND_BOUNDARY.md` gives finite-energy C^{2,alpha} examples, for all alpha<1, with a boundary Jacobian zero. They are not stationary. The theorem here does not conflict with them: stationarity supplies the additional inverse-Jacobian moments which those examples fail.

This conditional result is stronger than the energy-only C^{2,1} sufficient criterion, and it removes a possible separate boundary objection once global C^{1,beta} regularity is actually available. It also avoids an unverified invocation of the complete structural hypotheses of the Bauman–Owen–Phillips theorem.

It does not prove that every W^{1,6} minimizer is globally Lipschitz or C^{1,beta}. It does not derive an unconditional maximum principle for J. The finite-q pressure estimate cannot itself turn an L^1 coefficient tensor into L^q data, and all finite inverse moments alone still do not exclude essential infimum zero without some spatial regularity or a separate variational argument.

The resulting next target is precise: establish enough global regularity for the minimizer, without using a determinant lower bound in the proof, to invoke this theorem; or obtain a different argument eliminating low-Jacobian sets directly. Neither has been completed in this pass.
