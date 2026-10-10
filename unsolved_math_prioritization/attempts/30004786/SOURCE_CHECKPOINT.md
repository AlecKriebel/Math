# Exact source and formulation gate

**Source checkpoint only; zero substantive author proof turns used.**

The target is Jiang's contribution with Luo in OWR39/2021, printed pp2113–2115, [DOI10.4171/owr/2021/39](https://doi.org/10.4171/owr/2021/39). The full report was recovered from the institutional TIB mirror, and the exact conjecture/expectation pages were rendered and inspected. The workshop is2021; the imported citation's2022 is publication context.

Let k be a number field, A its adeles, G a k-split reductive group, rho any finite-dimensional representation of the complex dual group, and sigma an irreducible cuspidal automorphic representation of G(A). Local transfer through rho is needed to define the local data at general ramified places; no unproved global automorphic transfer is assumed. The target L-function includes its local factors, with contragredient sigma on the reflected side. The paper's general convergence theorem uses unitary sigma; nonunitary twists require tracking normalization rather than being silently included.

The crucial source distinction is between two formulations:

1. OWR Conjecture1.3 asks only for nontrivial k×-invariant linear functionals E_sigma,rho and E_dual,rho on their Schwartz spaces, intertwined by the Fourier operator. It does not state that they are actual theta sums, does not specify their boundary terms, and does not state an asymptotic expansion or Mellin-transform bound. The adjacent sentence says the formula is expected to be responsible for continuation and functional equation; it does not give a theorem proving that implication.
2. The later published Jiang–Luo paper, Pacific J.Math.326(2023),301–372, [DOI10.2140/pjm.2023.326.301](https://doi.org/10.2140/pjm.2023.326.301), calls the weak formulation Conjecture1.5 and gives a refinement in Conjecture7.4, pp363–364. The refinement identifies the functionals with actual theta sums on a restricted space S-double-circle. That space is spanned by pure tensors with some compactly supported local factor and with a compactly supported local factor after Fourier transformation, possibly at different places. The refinement must not be silently substituted for the weaker OWR premise.

The source's expected direct construction for split classical groups and the standard representation is a proposed route to prove the conjecture. It is not a restriction of the preceding arbitrary-(G,rho) conditional target. The imported literature assessment conflates those scopes if read as a full hypothesis list.

## Definitions and normalization recovered from the published primary paper

- Assumption6.1 and equations(6-3)–(6-8): transfer each local sigma_v through rho to an admissible GL_n representation pi_v, using the local reciprocity map. Define S_sigma_v,rho=S_pi_v and F_sigma_v,rho,psi_v=F_pi_v,psi_v. The global space/operator are restricted tensor products using the unramified basic functions. The global pi is not assumed automorphic.
- Equation(3-9): Z(s,phi,chi)=integral phi(x)chi(x)|x|^(s-1/2) d×x. The half shift is essential. Theorem3.4 identifies the local zeta ideals and basic-function Mellin transforms with local L-factors. The basic function is normalized to have value1 at1.
- Theorem3.10: Fourier sends S_pi to S_dual and has inverse F_dual,psi^-1. It intertwines the local zeta integrals through the local gamma factor. Exact Haar/additive-character conventions are inherited from the paper and must be retained in any proof.
- Theorem5.4 gives absolute and locally uniform theta convergence under a uniform unramified Satake bound; Theorem6.2 verifies the required bound for unitary sigma under the local-transfer setup. Mere theta convergence is weaker than rapid decay at both norm ends.
- Theorem1.1/4.7 gives actual theta inversion for cuspidal automorphic GL_n, proved using Godement–Jacquet and classical Poisson summation. Theorem7.3 treats square-integrable automorphic pi on the restricted two-place space. These known cases are credited, not new resolutions of the general conditional program.

## Prior and current-source gate

Exact-ID all-state PR and branch searches were empty; default-branch attempt-path commit history was empty; related-target groups had no entry. The maintained queue is rank241, queued0/5. The pinned dataset record was read completely; its exact-key prior imported report is null. Dataset revision37e53eabe540fb458758e198be61634bd02ee008.

The author's current publication page was checked. The2023 paper and2024 symplectic harmonic-analysis memoir are relevant primary literature; the checked page did not identify a complete general implication theorem. This is a limited search, not a universal novelty claim. The public problem website remained inaccessible, so the user-approved pinned dataset and primary papers are used.

Next substantive step: determine whether the weak invariant-functional identity actually provides Mellin information, then isolate precisely which strengthened theta/boundary hypotheses yield continuation and the global functional equation without importing global functoriality. No completed proof or counterexample is claimed at this source-only checkpoint.
