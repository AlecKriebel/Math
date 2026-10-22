# Attempt 4: Ricci-flat Bochner vanishing for twisted jets

## Objective
Assume the negation c1(T_X)_R=0 and derive an algebraic vanishing obstruction. Then determine whether jet curvature forces the forbidden object.

## External standard input, stated precisely
The Calabi–Yau existence theorem says: for a compact Kähler manifold with c1(T_X)_R=0, every Kähler class contains a Ricci-flat Kähler form. We invoke this established theorem; we do not reprove the nonlinear PDE existence theorem. Yau's 1977 announcement and 1978 paper are identified in SOURCES.md, with the actual level of inspection disclosed there.

## Retained theorem
Let X be smooth projective with c1(T_X)_R=0 and let A be ample. For all k>=1 and all m>=0,

H^0(X,E^GG_{k,m}T_X^* tensor A^-1)=0.

The same holds with the invariant subbundle E_{k,m} in place of E^GG_{k,m}.

## Proof of the tensor vanishing step
Choose a Ricci-flat Kähler form omega in c1(A), absorbing positive normalization constants consistently. By the dd^c lemma a smooth Hermitian metric on A can be adjusted to have curvature omega. The induced Chern connection on Omega_X^1 has contracted curvature i Lambda_omega F_{Omega}=0 because the metric is Kähler and Ricci flat. Contraction commutes with tensor products, and their curvature is the sum of the curvature on each factor. Thus E=(Omega_X^1)^{tensor q} has i Lambda F_E=0 for every q>=0. For F=E tensor A^-1,

i Lambda F_F=-n Id_F,

with the chosen normalization (any convention changes n to a positive constant).

For a holomorphic section s of F, the integrated Bochner identity for sections is

0=||D's||^2 - integral_X <i Lambda F_F s,s> dV_omega
 =||D's||^2+n||s||^2.

Both terms are nonnegative, hence s=0. This identity follows by applying the metric connection to |s|^2 in a unitary frame, using D''s=0, tracing, and integrating the scalar Laplacian over compact X. The curvature sign is also checked by the elementary case A^-1, which cannot have nonzero holomorphic sections.

Every tensor product Sym^{ell_1}Omega_X^1 tensor ... tensor Sym^{ell_k}Omega_X^1 embeds holomorphically into (Omega_X^1)^{tensor q}, q=sum ell_j: use the averaging symmetrization map on each block in characteristic zero. After twisting by A^-1 it consequently has no sections.

## Passing through the jet filtration
Under a holomorphic coordinate change z→Psi(z), the j-th derivative of a curve transforms as dPsi(f)f^(j) plus terms in derivatives of smaller order. Filtering polynomial jet functions successively by degree in the highest derivative therefore makes each associated-graded block transform linearly. For weighted degree m, the resulting blocks are

Sym^{ell_1}Omega_X^1 tensor ... tensor Sym^{ell_k}Omega_X^1,
where ell_j>=0 and sum j ell_j=m.

This is the Green–Griffiths jet filtration (Demailly, formula (6.5)). There are finitely many blocks. Tensoring the filtration by A^-1 is exact. If both H^0(F_{i-1}) and H^0(F_i/F_{i-1}) vanish, the long exact sequence gives H^0(F_i)=0. Induction over the filtration proves the displayed vanishing for E^GG_{k,m}. The invariant jet sheaf is a subsheaf of this polynomial jet bundle, so its section space injects and vanishes as well. This completes the proof of the retained theorem, relative only to the explicitly stated Calabi–Yau existence theorem and standard differential identities.

## Consequence and exact gap
Under c1(T_X)_R=0, no ample-negatively-twisted invariant jet section can occur. By Attempt 3, bigness of O_{X_k}(1) would produce one. Thus this route excludes total-curvature/big-tautological cases.

The original hypothesis only gives positivity along V_k. It supplies neither such a section nor a global positive curvature current on the entire tower. A direct image positivity theorem requiring total semipositivity cannot be applied with only a restricted inequality. The missing step is an actual construction of a nonzero ample-negatively-twisted jet section from the exact directed metric. The vanishing theorem alone does not provide that step.

The code enumerates weighted multiindices and verifies the elementary tensor/weighted-degree arithmetic, but does not prove Yau's theorem, the Bochner identity, or the sheaf-filtration argument.
