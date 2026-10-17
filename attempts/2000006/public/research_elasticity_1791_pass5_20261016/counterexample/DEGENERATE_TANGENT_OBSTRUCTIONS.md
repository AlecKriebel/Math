# Final-pass obstruction for nonnegative-Jacobian weighted tangents

16 October 2026. Frozen target: E-6322, unchanged coefficients, density, full comparison class and full smooth diffeomorphic boundary data. This is a conditional interior tangent theorem. It neither establishes tangent existence nor resolves the benchmark.

## 1. Statement

Let y be a full-class global minimizer of the frozen energy, or a local minimizer allowing sufficiently small compactly supported W^{1,6} variations. Let x0 be an interior point. Put A={z:1/2<|z|<2}. Suppose there are radii r_k down to zero and positive weights

    0 < m=alpha_1 <= alpha_2 <= alpha_3,
    s=alpha_1+alpha_2+alpha_3 > 3,
    gamma=s-3,

such that the componentwise rescalings

    Y_{k,i}(z)=r_k^{-alpha_i}(y_i(x0+r_k z)-y_i(x0))

converge strongly in W^{1,infinity}(A) to

    U_i(z)=|z|^{alpha_i} phi_i(z/|z|).

Assume the limiting determinant J_U=det DU is not identically zero.

Then neither of the following alternatives is possible:

1. **Barrier-dominated energy:** s+3m>6 and phi is C^1 on S^2.
2. **Balanced energy:** s+3m=6 and phi is C^2 on S^2.

No strictly positive lower bound on the limiting angular determinant is assumed in either alternative. In fact J_U>=0 follows from the convergence and the original determinant constraint. The theorem allows angular zeros initially and rules them out or obtains a contradiction locally.

The determinant-identically-zero limiting profile is not covered. Neither is a general subcritical profile with s+3m<6. The balanced statement retains its C^2 profile hypothesis.

## 2. Whole-density normalization

Write

    H(F)=a|F|^6+b|cof F|^3+c(det F)^2,
    D_r=diag(r^{alpha_i-1}),
    L_r=diag(r^{alpha_i-m}).

Every summand of H has matrix homogeneity six, and D_r=r^{m-1}L_r. Consequently, for det P>0,

    r^{2 gamma} W(D_r P)
      = r^{2(s+3m-6)} H(L_r P) + d(det P)^{-2}.       (2.1)

This identity is exact. Also L_r converges to the orthogonal row projection Pi onto the indices with alpha_i=m. The map H is C^2 on all matrices: in particular |v|^3 is C^2 at v=0. Thus H(L_r P) converges in C^1 on bounded matrix sets to

    H_0(P)=H(Pi P).                                  (2.2)

Since s>3, the balanced relation implies m<1. All three weights cannot equal m in the balanced case, because that would give m=1 and s=3. Hence Pi kills at least one row, including row 3, and H_0 is independent of row 3. More explicitly, with the weights ordered:

- if alpha_1<alpha_2, H_0(P)=a|p_1|^6;
- if alpha_1=alpha_2<alpha_3,
  H_0(P)=a(|p_1|^2+|p_2|^2)^3+b|p_1 cross p_2|^3.

Here p_i denotes row i of P. The determinant-square term vanishes in H_0.

## 3. Localized variational passage

Strong W^{1,infinity} convergence implies det DY_k converges essentially uniformly to the continuous function J_U. Because det Dy>0 almost everywhere, J_U>=0 everywhere on A. Its nontriviality therefore supplies a nonempty open positive set O={J_U>0}.

Fix a smooth compact test vector field Phi supported in O. On a compact neighborhood of its support, J_U has a positive minimum and DY_k is essentially uniformly bounded. For every sufficiently large fixed k, the physical gradients D_{r_k}DY_k lie almost everywhere in a compact subset of GL^+(3). The physical variation corresponding to Y_k+t Phi is

    y_i(x0+r_k z) + t r_k^{alpha_i} Phi_i(z).

It is compactly supported and admissible for all sufficiently small positive and negative t, where the permissible size can depend on k and Phi. Differentiation of the energy is dominated there. Multiplication by the positive scalar in (2.1), and omission of the common volume factor r_k^3, do not change stationarity.

On this fixed support, normalized stresses converge uniformly in the essential sense. Thus:

- if s+3m>6, U satisfies the full weak Euler system of d J_U^{-2} on O;
- if s+3m=6, U satisfies the full weak Euler system of H_0(DU)+d J_U^{-2} on O.

No derivative of the convergence error is taken. The actual minimizer need not be C^1 on these annuli.

For context, the original finite energy also forces m>1/2 and s<9/2 whenever such a nontrivial positive-determinant patch exists. On a fixed smaller positive patch, the first limiting row is nonzero and J_U is bounded above and below, giving positive lower bounds times r_k^{6m-3} and r_k^{9-2s} for shrinking-annulus strain and barrier energies. Absolute continuity makes both integrals tend to zero, excluding equality as well as negative exponents. These restrictions are not substitutes for the Euler equations.

## 4. Barrier-dominated case: no positive patch

The limiting weak system is

    div[J_U^{-3}(cof DU)_i]=0,   i=1,2,3.             (4.1)

On any sufficiently small positive-J patch, U is a C^1 local diffeomorphism. Set X=U(z). For a test chi in its target chart, use psi(z)=chi(U(z)); compact C^1 tests are justified by approximation. The cofactor identity and change of variables give

    integral J_U(U^{-1}(X))^{-3} partial_{X_i}chi(X) dX=0.

All three target derivatives of the continuous pressure vanish. Therefore J_U is constant on each such local chart. But every positive-J point z lies on a short radial segment contained in O, and

    J_U(tz)=t^{gamma} J_U(z),    gamma>0.

This is not locally constant. The contradiction proves alternative 1 impossible. Neither an axis preimage nor any global degree argument enters this case.

## 5. Balanced case: bounded pressure excludes angular zeros

Here U is C^2 and H_0 is C^2 globally. On O the full reduced weak Euler equation is classical:

    div DH_0(DU) + 6d J_U^{-4}(cof DU) grad J_U=0.

Piola's identity is used only on this smooth positive set. Multiplying by DU^T and using DU^T(cof DU)=J_U I yields

    grad(J_U^{-2})=(1/(3d)) DU^T div DH_0(DU).        (5.1)

The right side is bounded on every compact subset of A, including across the potential zero set of J_U: this follows from U being C^2 on A and H_0 being C^2 on all matrices.

Suppose O is nonempty but a point of A has J_U=0. Join a point of O to that zero by a finite-length polygonal path lying in A, and stop at its first zero. The image of the path is compactly contained in A. On its portion before that first zero, (5.1) bounds the variation of J_U^{-2} by a constant times the path length. Continuity instead forces J_U^{-2} to tend to infinity at the first zero. This contradiction proves J_U>0 throughout A.

Homogeneity then gives a positive angular minimum, so J_U>0 on the whole punctured space and uniformly on each compact annulus.

## 6. Balanced case: the pressure-only row is impossible

Because H_0 is independent of row 3, the third limiting Euler equation is

    div[J_U^{-3}(cof DU)_3]=0.                       (6.1)

The target-coordinate argument from Section 4, now using only row 3, says that J_U is constant along sufficiently short fibers of (U_1,U_2), parametrized by vertical target segments.

For completeness, a regular preimage of the third target axis exists in the now everywhere-positive situation. Extend U by U(0)=0. The weighted radial derivative identity shows that U(z)=0 at a nonzero point would imply DU(z)z=0 and hence det DU(z)=0. Thus zero is isolated. In a fixed ball B, its boundary image stays away from zero. Values U(z_n) approaching zero from z_n approaching zero are regular, have finitely many preimages in B, and every such preimage has positive Jacobian. Their degree is therefore positive. Degree is constant for small target values, so a sufficiently small nonzero third-axis value has a preimage. At its angle theta_0,

    phi_1(theta_0)=phi_2(theta_0)=0,
    phi_3(theta_0) != 0,
    j(theta_0)>0.

The radial curve r theta_0 maps to a nonconstant local vertical target segment, while

    J_U(r theta_0)=r^{gamma} j(theta_0),  gamma>0,

is strictly nonconstant. This contradicts (6.1) and proves alternative 2 impossible.

## 7. What remains

These conclusions concern only an assumed strong annular weighted tangent. They supply no reason that every singular minimizer has one, and no boundary tangent theorem. Among such tangents, determinant-identically-zero profiles remain outside the argument. Nontrivial angularly degenerate profiles in the subcritical range s+3m<6 remain open in general; the separate critical-axis family report rejects one explicit family in that range as well. Balanced C^1 profiles without the C^2 pressure bound are also not settled here.

There is no actual full-class minimizing counterexample in this report, and no positive resolution of E-6322. The benchmark and the distinction from broader sufficient-condition programmes are unchanged.

## Dependencies and independent checks

The local target-coordinate pressure argument is proved above and agrees with the sealed pass-4 audit addendum `research_elasticity_1791_pass4_20261016/audit/WEAK_ANNULAR_REFINEMENT.md`. The bounded-pressure identity is the reduced-density version of the pass-2 conditional C^2 argument. This proof needs no new external regularity theorem and does not use the scalar p-Laplacian regularity input from pass 3.
