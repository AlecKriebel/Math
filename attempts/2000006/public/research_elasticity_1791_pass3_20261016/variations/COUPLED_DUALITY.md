# Pass 3: coupled finite comparisons and exact inverse stress duality

E-6322, 2026-10-16. Status: rigorous structural identities and an identification of the remaining comparison gap; no unconditional regularity gain.

## 1. Established inverse baseline and notation

For an admitted y, write F=Dy, J=det F and Pi=DW(F). Put

T=Pi F^T,
E=W(F)I-F^T Pi.

The accepted pass-2 inverse theorem gives the actual a.e. inverse v on D=G(Omega), its full boundary trace, and

v in W^{1,9/5}(D),
H=Dv=F(v)^{-1} a.e.,
K=det H=J(v)^{-1}>0.

In particular the formulas below use a genuine weak inverse derivative. They do not invoke a topological inverse or full minimization of the inverse energy over an unconstrained Sobolev class.

The transformed energy is

V(H)=K W(H^{-1})
=a|cof H|^6/K^5+b|H|^3/K^2+c/K+dK^3.

## 2. Finite coupled comparisons are admissible

Let phi:Omega to Omega and Psi:D to D be orientation-preserving C^1 bi-Lipschitz diffeomorphisms fixing their entire respective boundaries pointwise. Lipschitz piecewise-C^1 versions with the same properties also work. Define

y_tilde=Psi composed with y composed with phi^{-1}.

The trace is g, the map is W^{1,6}, and its determinant is positive a.e. Uniform bounds on the two diffeomorphisms and their inverses give finite target energy, exactly as in the separate pass-1 comparisons. Thus this is a valid full-class competitor.

Write A(x)=Dphi(x), L(z)=DPsi(z), and k=det A. The exact energy formula is

I(y_tilde)=integral_Omega k(x) W(L(y(x))F(x)A(x)^{-1}) dx.

The exact a.e. inverse is

v_tilde=phi composed with v composed with Psi^{-1}.

Consequently inverse inner and outer diffeomorphism variations are precisely primal outer and inner diffeomorphism variations, with the roles exchanged. Considering these same composition maps in inverse coordinates does not enlarge the generated comparison class.

## 3. Exact inverse stresses

Let S(H)=DV(H), pointwise for det H>0. Matrix differentiation, using F=H^{-1}, gives

S=K[W(F)F^T-F^T Pi(F)F^T]=K E(F)F^T.

Therefore

S H^T=K E(F),
H^T S=K[W(F)I-T(F)],
V(H)I-H^T S=K T(F).

All primal fields in these expressions are evaluated at v(z). The two multiplicative inverse stresses are integrable: change of variables cancels K, so their L^1 integrals are bounded by the already established L^1 integrals of E and T on Omega.

Thus the inverse outer-variation identity is exactly the primal inner identity, and the inverse inner-variation identity is exactly the primal outer identity. There is no independent additional first-order equation merely from relabeling these variations as inverse variations.

## 4. What coupled second variations might still add

The preceding statement is restricted to the first-order identities. It does not assert that mixed second-variation stability follows from separate pure second-variation inequalities.

For phi_s=Id+s eta and Psi_t=Id+t psi, after the material change of variables the energy is

integral det(I+s Deta) W((I+t Dpsi(y))F(I+s Deta)^{-1}).

For fixed bounded test derivatives this expression is twice differentiable near (0,0), with derivatives dominated by a constant times W(F). This follows directly from the separate minor formulas; no unweighted bound on Pi is needed. The Hessian of the integrated energy at a minimizer is positive semidefinite.

The barrier part alone is exactly

B(F) det(I+s Deta)^3 det(I+t Dpsi(y))^{-2}.

Its mixed derivative is

-6B(F) tr(Deta) tr(Dpsi(y)).

The determinant-square part has mixed derivative

-2cJ^2 tr(Deta) tr(Dpsi(y)).

The other two contributions are bounded in absolute value by a constant times [a|F|^6+b|cof F|^3]|Deta||Dpsi(y)|. They cannot simply be discarded with a favorable sign.

Care is needed when expressing the mixed derivative as separate terms containing D^2W and Pi: individual terms involving F^{-1} can fail the available domination although their combined derivative is controlled. The finite minor expression is the safe object.

No coercive reverse-Holder or decay estimate for the positive energy has been extracted from this coupled Hessian in this pass.

## 5. The actual new step needed for inverse additive comparisons

An arbitrary inverse perturbation v+t zeta is not of the composition form above. Its admissibility as an inverse competitor requires more than its formal derivative and the finite V integral: one must establish the relevant injectivity/change-of-variables properties, the Sobolev regularity and trace of its inverse, and membership of that inverse in the original full class.

The pass-3 literature lane has now proved the restricted addition theorem in `../literature/ADDITIVE_INVERSE_ADMISSIBILITY.md`: every compactly supported W^{1,9/4} inverse addition, including every smooth or Lipschitz addition, is a genuine inverse competitor whenever its resulting V energy is finite. Its proof supplies the required compatibility rather than assuming it. This does not establish a finite-energy interval of nonzero amplitudes, nor does it transfer minimality to the unrestricted W^{1,9/5} class. In particular, the ordinary cutoff of v minus an affine map is initially only W^{1,9/5} and is not covered by that restricted theorem.

There is, however, a different route to ordinary primal or inverse equilibrium which does not require additive competitors at all: extra integrability can allow pulling additive test fields through the already established weak inverse and extending the safe multiplicative identities by duality. The precise thresholds are proved in `MOMENT_THRESHOLDS.md`.
