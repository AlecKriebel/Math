# Post-INITIAL model-import checks and cutoff phase bridge

This file is written after the actual decisive primary passages were read but before archived candidate audit/mapping bodies are opened. It extends, and does not rewrite, the source-only INITIAL. No current other-family/root findings or scientific coordination have been used.

## Literal question and normalization

The actual OWR 7/2025 printed page 371, section 2.2, uses full-space dGamma(-Delta) plus the density-pair integral over Lambda×Lambda, coefficient one, without a fixed-density or energy restriction in that subsection. The fixed-high-density Hartree model is in a separate preceding bosonic subsection. Printed page 365 explicitly distinguishes pointwise norm continuity of each observable's orbit from the weaker strong operator topology. Thus the note's kappa=0 sector realization answers the literal density ordering, and kappa=1 independently treats the normal ordering used in much of the dynamics literature. This identification does not turn the construction into a thermodynamic-limit or CAR-invariance result.

The prior 2026 theorem is stated for a full-space difference potential with ordered off-diagonal pairs. The spatially cut off symmetric kernel is not literally another difference potential. Importing the theorem statement alone would therefore be invalid. Its bounded-kernel proof uses only the relevant multiplication bounds, commutation with smooth leakage observables and an approximately constant cross-interaction on separated regions. These survive for the present kernel. The construction below checks that bridge explicitly, rather than attributing a cutoff theorem to the prior paper.

## A fixed kernel, both orderings and the diagonal issue

Let K(x,y)=1_Lambda(x)1_Lambda(y)V(x-y)=1_Lambda(x)1_Lambda(y). Put delta=1-kappa. The n-particle Hamiltonian is

H_n=T_n+Σ_(i≠j)K(x_i,x_j)+delta Σ_i 1_Lambda(x_i).

When one particle is temporarily distinguished, the extra multiplication operator is

C_n(x;Y)=2Σ_(j=1)^n K(x,y_j)+delta 1_Lambda(x).

It is bounded by 2n+1. It is not necessary to absorb the discontinuous diagonal term into a one-particle Hamiltonian and then assume Sobolev propagation for that modified Hamiltonian. Keep h=-Delta for the distinguished propagation and keep the bounded extra term in C_n. Let A=B(0,1/2), B=B(2e_1,3/5), and B_0=B(2e_1,9/20). The closure of Q lies in B_0; A and B have disjoint closures, both inside Lambda. On A×B^n,

C_n=2n+delta=:c_n,

and everywhere |C_n-c_n|≤2n+1≤3n (n≥1). Symmetry of K gives the exact antisymmetrization intertwining with the full (n+1)-particle Hamiltonian. Bounded sector perturbations justify its Duhamel identity without differentiating 1_Lambda.

## Energy bootstrap in the interacting cluster

Choose a fixed smooth real eta, zero near Q, one on B complement, with eta-1 compactly supported in B. Define F_n(s)=<dGamma(eta^2)> in the interacting cluster e^(-isH_n)Psi_n. Then M_Lambda≤N_(B complement)≤dGamma(eta^2), and F_n(0)=0. All interaction terms commute with the smooth number multiplier. The commutator calculation for -Delta, with Cauchy–Schwarz summed over particles, gives

|F_n'(s)|≤C sqrt(F_n(s)) sqrt(<T_n>_s+n).

This is valid on the smooth initial vector and by its sector graph/form domain; no interacting Slater property is used. Since H_n is nonnegative and its interaction equals n(n-kappa) at the initial support, energy conservation and the exact identity from INITIAL give

<T_n>_s=<T_n>_0+n(n-kappa)-<L_n(L_n-kappa)>_s
≤C n^(5/3)+2n <M_Lambda>_s
≤C n^(5/3)+2n F_n(s).

With y_n=sqrt(F_n), regularizing the square root at zero and then passing to its limit yields an integral differential inequality

y_n'≤C n^(5/6)+C sqrt(n)y_n.

Gronwall gives y_n(s)≤C n^(5/6)|s| exp(C sqrt(n)|s|). For every fixed theta, |s|≤theta/n consequently gives y_n(s)=O(n^(-1/6)). This improves the crude O(n|s|) cluster leakage available from an undifferentiated O(n^2) energy bound. It verifies the specifically claimed cutoff energy-bootstrap consequence, rather than proposing a repair to the note's independent free-Slater proof.

## Localized antisymmetrization and phase error

For J_n=sqrt(n+1)P_-, the elementary occupation decomposition gives

||J_n xi||^2≤<xi,(1+N_A)xi>

when the distinguished variable is supported in A, and J_n is isometric when all cluster variables lie in disjoint B. Let P_B be the projection that every cluster particle lies in B and let chi_A be one near supp f, supported in A. Decompose u_s⊗Psi_n(s) into chi_A u_s⊗P_B Psi_n(s), chi_A u_s⊗(1-P_B)Psi_n(s), and (1-chi_A)u_s⊗Psi_n(s).

The phase residual C_n-c_n vanishes on the first term. On the second, the localized J bound and commutation of the bounded residual with N_A give a squared norm at most C n^2 F_n(s), since 1-P_B≤N_(B complement), N_A P_B=0 and N_A≤N_(B complement). On the third, global ||J_n||≤sqrt(n+1), ||C_n-c_n||≤3n and the free smooth-mode leakage ||(1-chi_A)u_s||≤C|s| give norm at most C n^(3/2)|s|. Thus exact Duhamel yields, on |t|≤theta/n,

||e^(-itH_(n+1))a*(f)Psi_n-e^(-ic_n t)a*(e^(-ith)f)e^(-itH_n)Psi_n||
≤C n^(11/6)t^2 exp(C sqrt(n)|t|)+C n^(3/2)t^2
=O(n^(-1/6)+n^(-1/2)).

Constants may depend on the fixed theta but not n. The prior lemma's convenient t≤1/n restriction is replaced by the same bounded-interval proof for any fixed theta; at the required pi/(2n+delta) times this is within a fixed theta/n and eventually within the one-body local-time bound. No singular cutoff derivative or translation invariance is needed. The qualitative discontinuity already follows with the prior cruder error by choosing theta sufficiently small. The improved bootstrap permits the maximal phase.

## The same maximal witness from this bridge

Use the original fixed f, Psi_n and Xi_n, not replacement modes. Since n_f≤N_A, ||a(f)Psi_n(t)||≤y_n(t). CAR then gives

<a*(u_t)Psi_n(t),a*(f)Psi_n(t)>=<u_t,f>+r_n(t), |r_n(t)|≤y_n(t),

using ||a(u_t)||=1; orthogonality at positive time is unnecessary. Also |<u_t,f>-1|≤|t| ||hf||. At t=pi/(2n+delta), exp(ic_n t)=-1, all errors vanish, and the creation matrix element tends to -1. Taking its adjoint and using the universal norm bound two yields all original maximal/vector/state limits, exactly as in INITIAL. This is a checked import/deduction from the earlier localized phase architecture, not a theorem literally stated there and not a claim of a new independent priority contribution.

## Time averages do not contradict the result

The actual 2025 accepted-version source separates continuity in every fixed-sector seminorm from full operator-norm continuity on the subalgebra generated by time averages. For A_g=integral g(s)alpha_s(A) ds with g smooth compactly supported, a time translation bounds ||alpha_t(A_g)-A_g|| by ||A|| ||g(.-t)-g||_1, which tends to zero. That continuity applies to a changed algebra/averaged observable. It does not say that the original fixed annihilation operator has a norm-continuous orbit in B(Fock), and density in all sector seminorms is not uniform full-Fock norm density.

No unproved fixed-state discontinuity, CAR non-invariance, all-kernel theorem or dimensional extension has been imported. The existing analytical proof and this import bridge do not require a numerical native replay; any later code inspection is to assess finite reproducibility, not to replace the universal argument.
