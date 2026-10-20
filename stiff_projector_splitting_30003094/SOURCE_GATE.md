# Source gate for low rank splitting on discretized PDEs

Checked 20 October 2026. Queue row 1829; ID 30003094; source key OWR-14226-001.

## Verdict

**Source recovered. Substantial later subclass results exist, but no verified general resolution of the original direct projector-splitting PDE question was found.** Do not mark the row solved from the bounded-matrix-ODE theorem, the 2019 modified stiff/nonstiff method, or a stability theorem alone. The original question does not specify a PDE class or a complete theorem statement; any research claim must first state those choices.

This is a source and literature gate, not a new proof or an independent audit of the cited proofs. No queue change or publication was made. The negative search finding is bounded by the sources inspected, not proof of universal nonexistence.

## Original source and scope

Emil Kieri, joint work with Christian Lubich and Hanna Walach, “Time-stepping of low-rank approximations with small singular values,” printed pp. 910–912 in *Geometric Numerical Integration*, Oberwolfach Reports 13 (2016), no. 1, 869–948, DOI 10.4171/OWR/2016/18. Workshop: 20–26 March 2016; publication: 11 October 2016. The queue source key matches EMS article 14226.

The final paragraph explains that dependence on the full vector field's Lipschitz constant prevents the existing estimate from explaining spatially discretized PDE behavior. Its precise request is: “Extending the error analysis to cover also this case remains an open problem.”

The target is the existing tangent-projector splitting, applied to matrix equations produced by spatial discretization; tensor-train extensions are also mentioned. No particular PDE, boundary conditions, spatial discretization, smoothness class, spatial rate, or second-order target is fixed. Treating it as a universal assertion over arbitrary PDEs would add unsupported scope.

Sources: [EMS report record](https://ems.press/journals/owr/articles/14226); [report PDF, pp. 910–912](https://ems.press/content/serial-article-files/46621). Printed pp. 911–912 were visually inspected.

## Exact numerical method

Let \(\dot X=F(t,X)\), \(\mathcal M_r=\{Y:\operatorname{rank}Y=r\}\), and \(Y=USV^*\), where \(U,V\) have orthonormal columns and \(S\) is nonsingular. The fixed-rank dynamical approximation solves
\[
\dot Y=P(Y)F(t,Y),\qquad
P(Y)Z=ZVV^*-UU^*ZVV^*+UU^*Z.
\]
For a step from \(t_0\) to \(t_1=t_0+\tau\), the K–S–L Lie projector-splitting algorithm is:

1. Solve \(\dot K=F(t,KV_0^*)V_0\), \(K(t_0)=U_0S_0\), and factor \(K(t_1)=U_1\widehat S_1\).
2. Solve \(\dot S=-U_1^*F(t,U_1SV_0^*)V_0\), \(S(t_0)=\widehat S_1\), obtaining \(\widetilde S_0=S(t_1)\).
3. Solve \(\dot L=F(t,U_1L^*)^*U_1\), \(L(t_0)=V_0\widetilde S_0^*\), and factor \(L(t_1)=V_1S_1^*\).
4. Return \(Y_1=U_1S_1V_1^*\).

The negative S-step matters. This is not a physical linear/nonlinear splitting. The Strang variant composes a half Lie step with its adjoint. OWR p. 911 accidentally omits the terminal \(V_0\) in its K equation; the dimensionally correct equation above agrees with the cited SIAM paper, §2.2. Its L equation uses an unindexed U; the fixed factor is \(U_1\).

## Already established bounded ODE result

Kieri–Lubich–Walach (2016), Theorem 2.1, uses the Frobenius norm. Assume bounded, Lipschitz \(F\), bounds \(B,L\); a decomposition \(F=M+R\) with \(M(t,Y)\in T_Y\mathcal M_r\), \(\|R\|_F\le\varepsilon\); rank-preserving existence; and initial error \(\delta\). Neighborhood versions suffice. Both Lie and Strang satisfy
\[
\|Y_n-X(t_n)\|_F\le c_0\delta+c_1\varepsilon+c_2\tau,
\qquad c_i=c_i(L,B,T).
\]
Thus the theorem is robust against small retained singular values, but gives only first order even for Strang. Tensor-train Theorem 3.1 additionally depends on tensor order \(d\), not explicitly on individual ranks. Uniform assumptions are essential: increasing rank or grid size can change \(B,L,\varepsilon\).

Section 2.6.2 improves propagation using a one-sided Lipschitz constant but still has full \(L\) in \(c_2\). Section 2.6.3 allows compatible substep defects \(\tau\eta\), adding \(c_3\eta\). Consequently, merely applying this theorem separately on every mesh does not establish stiffness-uniform convergence.

[Kieri–Lubich–Walach, SIAM JNA 54 (2016), 1020–1038](https://doi.org/10.1137/15M1026791); [institutional full published text](https://www.diva-portal.org/smash/get/diva2%3A874116/FULLTEXT01.pdf), §§2.2–2.6, 3.2.

## Closest established stiff convergence theorem

Ostermann–Piazzola–Walach, SIAM JNA 57 (2019), 1947–1966, Theorem 1, considers
\[
\dot X=AX+XA^*+G(t,X),\quad
\mathcal I_\tau=\Phi^A_\tau\circ\widetilde\Phi^G_\tau,
\quad\Phi^A_\tau(Z)=e^{\tau A}Ze^{\tau A^*}.
\]
Here only \(G\) receives projector splitting. In Frobenius norm its hypotheses include existence, initial error \(\delta\), a near-tangency remainder \(\varepsilon\) along the rank-r solution, locally \(C^1\) nonstiff \(G\), and semigroup estimates
\[
\|e^{tA}Ze^{tA^*}\|_F\le e^{\omega t}\|Z\|_F,\qquad
\|e^{tA}(AZ+ZA^*)e^{tA^*}\|_F\le C_s t^{-1}e^{\omega t}\|Z\|_F.
\]
The global estimate is
\[
\|X(t_n)-\mathcal I_\tau^n(Y^0)\|_F
\le c_0\tau(1+|\log\tau|)+c_1\delta+c_2\varepsilon.
\]
Constants depend on \(\omega,C_s,L_G,B_G,T\), not explicitly \(\|A\|\), mesh size, or small singular values; those hypothesis constants must be mesh-uniform. The step threshold depends on \(L_G\). Standard elliptic spatial discretizations motivate the semigroup assumptions.

**Scope boundary:** a modified method and a semidiscrete temporal bound, not the original full-F KSL theorem or a spatial-error theorem. Section 6.2 also sketches periodic transport with a contractive semigroup and uniformly bounded \(AG+GA^*\) from spatial smoothness; this is not arbitrary hyperbolic coverage. Section 6.1 supplies no robust second-order theorem.

[Published paper](https://doi.org/10.1137/18M1177901); [arXiv v2, §§3–6](https://arxiv.org/html/1803.10473v2). arXiv: submitted 28 March 2018, revised 31 May 2019; publisher: 13 August 2019. An experimental HTML rendering prints a 2026 date; the version history and publisher establish the actual chronology.

## Further relevant results and boundaries

- **Random parabolic stability:** Kazashi–Nobile–Vidličková (2021) proves singular-value-independent stability of related fully discrete variational/projector schemes. Explicit and generally semi-implicit variants have parabolic CFL conditions; the implicit version is unconditionally stable. This is meaningful PDE progress, not a general approximation-error bound for the original exact-subflow KSL scheme. [Published primary paper](https://doi.org/10.1007/s00211-021-01241-4).

- **Fully discrete error for a different stabilized scheme:** Nobile–Trigo Trindade, arXiv:2402.03586v1 (2024; conference publication listed 2025), Theorem 3.1, gives an error estimate for implicit SUPG-DLR on random advection–diffusion–reaction equations. Its hypotheses include homogeneous Dirichlet data, positive diffusion/reaction, divergence-free deterministic transport, a quasi-uniform degree-k finite-element mesh, collocation, solution regularity, a model residual, and stabilization restrictions. Section 3 also uses a local-basis inverse inequality in the proof. The error is measured in collocation-weighted \(L^2(D)\) and a time-summed SUPG norm; the bound includes \(h^{k+1}+\Delta t+\delta_s^{1/2}h^k+\delta_s^{-1/2}h^{k+1}\), initial error, and model residual. Here \(\delta_s\) is the stabilization parameter, not initial error. This is genuine space/time analysis, but not the unchanged orthogonal KSL method or unrestricted singular-value-uniform PDE theorem. [Full primary text](https://arxiv.org/html/2402.03586v1).

- **Current direct-PSI stability:** Zhang–Hu, arXiv:2507.15192v2, revised 12 April 2026, analyzes model linear hyperbolic/parabolic equations with specified finite differences and Lie/Strang projector splitting, comparing discretize-then-project with project-then-discretize. Stability depends on substep time discretization; Crank–Nicolson and hybrid choices can avoid the parabolic negative-step instability. This is a stability study, not a general robust global-error theorem. [Current primary version record](https://arxiv.org/abs/2507.15192), [v2 PDF](https://arxiv.org/pdf/2507.15192v2).

- **Separate second-order obstruction:** Zhang, arXiv:2608.12893v1, submitted 13 August 2026, claims a counterexample to singular-value-uniform second-order convergence of classical exact-subflow Strang PSI, already for a 3-by-3 smooth matrix ODE with rank-two data and uniform standard bounds. The public record shows a preprint, not a journal publication. Its theorem was identified, not independently proof-audited here. It does not settle the first-order stiff-PDE question, but prevents treating robust second order as automatic. [Primary preprint](https://arxiv.org/abs/2608.12893).

## Research acceptance boundary

A useful narrowed theorem must state the PDE/operator and boundary conditions, discretization and discrete norm, exact or numerical substeps, regularity and near-tangency assumptions, fixed or adaptive rank, and which constants remain uniform. The original issue is dependence on the increasingly large spatial operator, not merely algebraic existence of an error bound at each finite dimension.

For a mesh family, distinguish (a) temporal/rank error relative to the exact semidiscrete solution and (b) spatial error relative to the continuous PDE. A mesh-weighted Frobenius norm can represent discrete L2, but the weighting and uniform nonlinear estimates must be checked; unweighted Frobenius boundedness need not remain uniform as sample count grows. Small-singular-value robustness is not itself uniformity in rank, tensor order, or mesh. These are scope requirements for future research, not extra hypotheses asserted by the short OWR question.

## Provenance

Fresh hashes were taken of recovered local corpus files: exactly one matching problem record; no matching research record after scanning dictionary keys and values. This was not a fresh upstream corpus retrieval. Public verification metadata is in CORPUS_VERIFICATION.json and SOURCE_METADATA.json. Raw extracts, PDFs, extracted text, and inspection images are separate. Targeted later-literature checks covered stiff/semilinear, parabolic, hyperbolic, random-PDE, discretization-independent, SUPG, and 2025–2026 projector-splitting results. Broad general resolution remains unverified.
