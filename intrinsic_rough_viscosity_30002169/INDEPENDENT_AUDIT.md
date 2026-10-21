# Independent scope audit: intrinsic viscosity for transport-noise HJB

Date: 2026-10-21. Target: row 1838, catalogue ID 30002169 / OWR12013-001.

## Verdict

**Qualified positive result, not a certified complete resolution of every regime in the original question.** Gubinelli–Tindel–Torrecilla (GTT, 2014) really does give intrinsic touching-test-function viscosity definitions for transport noise, proves that the tests are sufficiently rich, and identifies the definition with the rough-flow transformed deterministic definition. This is not merely convergence of smooth approximations renamed. But its explicit theorem does not match the full possible scope of the original p-variation control problem. In particular, one must not silently discard the vector-field regularity gap.

The original question concerns transport noise linear in the gradient. Unresolved comparison for general nonlinear-gradient noise cannot serve as evidence that this original transport question remains entirely unresolved. Conversely, a transport theorem cannot certify the catalogue's broader nonlinear formulation.

## Primary sources and locations

1. Joscha Diehl, joint work with P. Friz and P. Gassiat, “Controlled rough differential equations and applications to stochastic control,” Oberwolfach Report 41/2012, printed pp. 2505–2506. The original question is on p. 2505. Report PDF inspected: https://publications.mfo.de/bitstream/handle/mfo/3311/OWR_2012_41.pdf?sequence=1 .
2. M. Gubinelli, S. Tindel, I. Torrecilla, “Controlled viscosity solutions of fully nonlinear rough PDEs,” 2014 preprint, https://arxiv.org/abs/1403.2832 . The relevant PDF and locally extracted text were inspected; neither is redistributed here. Key items: Hypothesis 2.7; Propositions 2.19–2.20; Definitions 3.4, 3.6, 4.1; Propositions 4.3, 4.5; Theorem 4.7; Remarks 4.8 and 4.11.
3. J. Diehl, P. Friz, P. Gassiat, “Stochastic control with rough paths,” https://arxiv.org/abs/1303.7160 . The relevant PDF and locally extracted text were inspected; neither is redistributed here. Key items: Definition 1, Remark 2, Theorem 3, equation (3.3), Theorem 26(iv).
4. M. Caruana, P. Friz, H. Oberhauser (CFO), “A (rough) pathwise approach to a class of non-linear stochastic partial differential equations,” Ann. IHP AN 28 (2011), 27–46, https://www.numdam.org/item/AIHPC_2011__28_1_27_0.pdf . Independently downloaded and inspected. Key items: Theorem 1, Definition 1, Examples 3 and 5, Section 7 and footnote 19.

## What exactly was asked

The report starts with a controlled RDE driven by a geometric finite-p-variation rough path, with controls measurable into a set U. Its finite-horizon value function leads to a backward transport-noise HJB equation. The reported solution notion is locally uniform convergence of viscosity solutions with smooth approximating drivers. The question is whether an intrinsic characterization, for example by touching tests, is available.

The question paragraph does not explicitly fix p in (2,3), nor state precise smoothness, boundedness, or uniform-continuity hypotheses. A subsequent duality theorem on p. 2506 does impose p in (2,3) and vector fields Lip^gamma with gamma>p. That theorem is important context, but its hypotheses must not simply be pasted into the earlier question as an explicit scope restriction.

The later DFG formulation is precise: roughness alpha in (1/3,1/2], noise fields Lip^gamma with gamma>1/alpha, b continuous and uniformly Lip^1 in space over controls, terminal g bounded uniformly continuous, and f bounded continuous and locally uniformly continuous in (t,x), uniformly in the control. Its Hamiltonian is H(t,x,q)=sup_a{b(x,a)·q+f(t,x,a)}. The omission of t in some subsequent displays does not remove the permitted time dependence of f.

## GTT theorem matching

- **Driver:** Hypothesis 2.7 uses a Hölder path of exponent gamma>1/3 with a second-level area satisfying Chen's relation and the geometric symmetric identity. The development is level two. The introduction explicitly restricts the actual analysis to this regularity and only suggests higher-order expansions for rougher signals. Such a suggestion is not a proved all-p extension. A finite-p-variation path is not necessarily Hölder in the original clock. Reparameterization alone does not automatically transport their dt-drift and C1-time test definition without additional argument.
- **Fields:** Section 4 repeatedly assumes smooth bounded transport vector fields. Proposition 2.19 provides a C3 spatial flow; Proposition 2.20 its inverse. The manuscript does not give a sharp finite differentiability threshold in those statements. Taking bounded smooth fields with sufficiently many bounded derivatives is a safe sufficient specialization, not a proof for merely Lip^gamma, gamma>p.
- **Test definition:** Definition 4.1 prescribes the first and second controlled coefficients of a spatially C2 test by the first and iterated transport operators. The remaining time drift is continuous. Definition 3.6 tests continuous candidate solutions at local touching points and compares that drift with the deterministic Hamiltonian. Neither stochastic adaptedness nor selecting a smooth approximation of the candidate solution is part of this local definition.
- **Nonvacuity and equivalence:** Proposition 4.3 identifies the controlled test class with classical C1-in-time/C2-in-space tests by composing with the rough flow or its inverse. Proposition 4.5 then proves an if-and-only-if correspondence for subsolutions and supersolutions, using the transformed gradient and the same spatial diffeomorphism. This establishes an actual intrinsic characterization in the covered setting.
- **Existence/uniqueness:** Theorem 4.7 states existence and uniqueness for bounded Lipschitz F(t,x,q), with the smooth bounded fields. Its proof transfers deterministic comparison through Proposition 4.5. The theorem statement itself does not spell out an initial-data class, whereas the equation carries initial alpha; a clean application should specify an appropriate continuous, preferably BUC, initial datum rather than claim arbitrary initial functions.
- **Hamiltonian mismatch:** A control Hamiltonian is generally unbounded in q, even if b and f are bounded. Example: one control, b=1, f=0 gives H=q. It is also not generally globally Lipschitz jointly in (x,q), since spatial variation of b is multiplied by q. Thus GTT Theorem 4.7 alone does not literally cover general controlled HJB. Remark 4.8 points to CFO/DFG examples, supporting extension of the comparison-based argument but not elimination of hypotheses.
- **Jets:** The safer acceptance route is through the touching-test propositions, not an unrestricted appeal to equivalence of all rough jet definitions. Remark 3.9 calls the general jet argument heuristic; Remark 4.11 explicitly prefers the test-function definition.

## Broader smooth-field result and its limit

CFO Theorem 1 is stated for every p>=1 in geometric p-variation topology, with transport fields Lip^(gamma+2), gamma>p, and invariant deterministic comparison under the specified C3 diffeomorphism class. It assumes existence and a uniform bound for smooth-driver solutions and yields approximation-independent convergence, stability, and contraction. Its control examples allow Hamiltonians linear-growing in the gradient, with the required bounds/moduli uniform over controls. The invariant-comparison hypothesis is the operative condition; boundedness of F in the gradient is not necessary.

Thus, for sufficiently regular transport fields, an intrinsic definition can also be made directly by requiring the rough-flow pullback to solve the deterministic transformed PDE. That definition uses the given enhanced rough path rather than a chosen sequence of smooth drivers. Pulling classical tests back by the flow supplies touching tests, and comparison transfers. This is a valid conceptual answer to the original question in that regularity class. CFO Section 7 explicitly discusses the transformed viscosity meaning and its equivalence to localized Lions–Souganidis tests in the linear-noise case. The section is phrased for enhanced Brownian realizations; applying its mechanism for general rough drivers should be explained rather than quoted as a separate all-p controlled-expansion theorem.

This does **not** settle the minimal-regularity DFG setting. DFG Remark 2 expressly contrasts its Lip^gamma noise fields with the stronger Lip^(gamma+2) needed for its cited transformation approach, and says that approach is unavailable under Theorem 3's weaker hypothesis. DFG Theorem 26(iv) supplies a flow decomposition only after this higher regularity is imposed. A proof purporting to close the low-regularity case must supply the missing flow/test regularity and comparison, or use a genuinely different intrinsic argument. Neither a formal chain rule nor continuity of the value function suffices.

## Acceptance conditions for new claims

1. State driver topology and range, not just “rough path.”
2. State spatial field regularity and bounded derivative assumptions explicitly.
3. Use the control Hamiltonian's actual gradient growth and time dependence.
4. State the candidate-solution class, initial/terminal data, and comparison assumptions.
5. Distinguish definition, nonvacuity of tests, comparison/uniqueness, and equivalence with the approximation/value-function solution.
6. If smooth fields are assumed, label that a positive subclass result. Do not call the low-regularity or all-p gap closed without a separate argument.
7. Do not infer mathematical openness today merely from a mismatch in the sources audited here. The verdict is lack of a certified full-scope resolution from these sources, not a proof of unresolved status.




## Review of authored smooth-field extension (research draft, 00:39 UTC)

Inspected `RESEARCH.md`, Avenue 2. The cancellation sign is correct for the displayed backward equation: composing with the forward positive-sigma flow removes the negative transport differential. The transformed terminal condition g composed with the terminal flow is correct. The transformed control drift J inverse times b composed with the flow and its displayed global Lipschitz estimate are correct. The Hamiltonian spatial estimate gives the required squared-distance-over-epsilon comparison term; bounded drift permits localization at infinity.

No fatal mathematical defect was found in this restricted proposition. Before treating the deliverable as acceptance-ready, requested explicit C_b-infinity fields, explicit control-set hypotheses (compact metric U with appropriate joint continuity is a sufficient clean specialization), and a separate paragraph establishing equivalence to all smooth-driver approximations via rough-flow stability and transformed-control estimates. This review does not certify the original low-regularity regime or a general all-p controlled-test expansion theorem.

### Final research-draft acceptance (00:40 UTC)

Re-read the completed five-avenue research draft. It now supplies explicit C_b-infinity noise fields, a compact metric control set and joint continuity, the level-two Hölder range, and approximation equivalence by rough-flow stability, uniformly bounded transformed trajectories, uniform-in-control payoff convergence, and the elementary supremum inequality. These additions close the requested acceptance conditions for the **restricted smooth-field proposition**.

The pure-area calculation is correct with the declared iterated-integral convention: the area contribution is +a times the second-coordinate derivative, not twice that amount, and the terminal solution shifts by +a(T-t). The draft correctly labels the affine field as outside the bounded-field theorem and restricts geometric pure-area approximation to p>2. Its final statement does not claim the low-regularity or all-p original question solved. Accepted as a mathematically coherent restricted partial result with no novelty claim, not as an acceptance report for a complete original-problem resolution.
