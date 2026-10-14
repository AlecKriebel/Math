# Independent adjudication of the PR248 priority inference

## Verdict

**B1–B8 is a valid mathematical proof, but it does not establish that an earlier source resolved the particular wave question. Do not change this case to `already_solved` solely on this witness.** The witness proves that the core counterexample can now be proved concisely using old differentiability and familiar concentration ideas. Its decisive source-specific construction is supplied in the audit after reading the submitted example. This is compatible with an elementary, problem-specific contribution; it is not a novelty certificate.

This verdict neither requires an earlier identical example nor requires the submitted global uniqueness, target perturbation or optional L1 estimates. An earlier theorem could cover the core by a routine specialization. What is missing here is an earlier *constructive assertion* whose specialization supplies, simultaneously, a feasible wave-data choice, a genuine local optimizer, the ordinary strict-cone premise, and loss of L2 growth. The present bridge supplies those missing assertions itself.

The applicable historical claim is limited: the generic infinite-dimensional obstruction, sparse threshold geometry, and weak-null/non-degeneracy explanation are established prior theory and need explicit attribution. The source-specific example may be described as an elementary realization of that obstruction in the energy-critical wave problem. Claims of a new general obstruction or worldwide firstness would be unsupported.

## Independence and scope

I independently read the classical bridge and actual relevant primary theorem statements and proofs. I did not read the recent-priority family's report or conclusions. Inputs are pinned in INPUT_PINS.json. The exact target is the failure, at a genuine local optimizer, of the unchanged source ordinary-critical-cone strict-positivity implication to strong L2-squared growth after setting beta2=0. The stronger auxiliary assertions are unnecessary for this adjudication. No PR, queue, Git, publication, spreadsheet, or external-person action was performed.

## What the cited earlier results assert

Kunisch–Meinlschmidt's 2019 preprint Theorem 4.3 states C2 dependence of the state on L1-in-time, L2-in-space controls and supplies the second-state equation. At zero it gives S''(0)=0. The preprint explicitly leaves beta2=0 open before Theorem 4.17. On subsequently reading its full printed proof, I verified a codomain mismatch: at zero, e_y z=-xi_z cannot reach an arbitrary continuous energy pair such as F(t)=(0,w), w nonzero. The local differentiability assertion needed here is valid via a direct compatible-state residual, recorded in the mathematical ledger; the submitted contraction already avoids this issue. This qualifies what was historically *proved in the inspected formulation*, without changing the priority verdict. [Primary preprint and history](https://arxiv.org/abs/1907.02744), [pinned v1](https://arxiv.org/pdf/1907.02744v1).

Borchard–Wachsmuth's 2024 Theorem 2.18 says that norm-squared quadratic growth implies its weak-null non-degeneracy condition. Its proof divides the growth inequality by squared distance and uses the assumed Taylor expansion. The theorem applies to this reduced objective. It does not choose its wave data or assert that its NDC fails at a wave local optimizer. Its applications concern parabolic states and scalar boxes; the final discussion of failure without a Tikhonov term is in that setting. [Primary published article, Theorem 2.18 and pp. 34–35](https://jnsao.episciences.org/14959/pdf).

Casas–Herzog–Wachsmuth 2017 supplies the sparse-control distinction between exact cones and sufficient coercivity. Its state is parabolic, its constraints are scalar boxes, and its j3 groups time profiles by space. Exchanging norm-group variables does not exchange state equations or turn boxes into pointwise Hilbert balls. Its generic warning is relevant credit, without a verified covering negative-wave assertion. [Primary paper](https://www.numdam.org/item/10.1051/cocv/2015048.pdf).

Casas–Tröltzsch's 2015 survey reproduces a Dunn counterexample completely: coercivity on an exact cone can coexist with failure of even local optimality. That verifies a generic antecedent, while the reproduced objective is an explicit integral polynomial with scalar bounds. Dunn's original chapter was not inspected. Attribution must say that the example was verified through this reproduction. [Published survey in the society's archive](https://www.mathematik.de/images/DMV/Jahresberichte/Jahresberichte_Archiv/2015.117Heft1.pdf), DOI 10.1365/s13291-014-0109-3.

## Why the present bridge does not date the resolution to BW2024

BRIDGES.md B1–B7 already supplies the complete negative answer without BW's theorem. The proof uses the submitted unit-ball data, target pi*e, T=1 and centered shrinking pulses. The old C2 state theorem shortens the local-optimality argument: the remainder o(A2) is enough, so the submitted O(A5) and global comparison are unnecessary for the core. B8 repackages the resulting zero growth ratio as failure of NDC.

Thus the logical dependency is:

1. Old differentiability, norm calculus and concentration methods are available.
2. The particular wave data, threshold contact and concentrating sequence are selected.
3. An all-directions local-optimality argument proves that this selection meets the source premise.
4. The source critical cone and loss of growth are proved for that selection.
5. The old NDC theorem gives the same failure already obtained directly.

The affirmative historical assertion in item 1 is documented. Items 2–4 are documented as a submitted construction and a fresh audit derivation, not as an assertion in the older papers. Their mathematical shortness does not provide a date for their previous discovery or establish that the model-specific question was already resolved.

This is stronger than saying that the older articles do not mention waves. Their abstract theorem *does* apply to waves. The limitation is that it is conditional: it says nothing that supplies the source-specific existential counterexample until the data and simultaneous optimizer/cone/sequence properties have been constructed.

## Routine steps and the substantive historical gap

Once the example is specified, embedding the reduced problem into a separable Hilbert dual, defining G=j+indicator(Uad), checking its Taylor expansion, and substituting normalized pulses into NDC are routine. The sine integral, zero terminal linear velocity, Taylor coefficients and source subgradient are also elementary. Repairing the local state residual's codomain is a routine functional-analytic correction, not a new PDE mechanism; even accepting the old local C2 conclusion in full does not supply historical attribution for the counterexample.

The historical gap is the design and validation of an example satisfying all the source premises. The target must place the adjoint exactly at the sparsity threshold at a null time set while admitting near-threshold concentration. The construction must make zero an actual local optimizer despite that lack of uniform first-order separation. B3–B4 achieves the latter by retaining the terminal tracking square and using a monotone scalar projection estimate. That is a sound, short argument; it is a new argument written in the audit, not an assertion supplied by the cited theorem.

This is the central source-model bridge, even though it involves no new PDE estimate and no difficult global proof. A construction can be mathematically elementary and still be the missing contribution. Conversely, if an earlier constructive theorem is found asserting such counterexamples for a class encompassing these terminal-observation wave systems, a short assumptions map could establish coverage without requiring an earlier author to print pi*e or the same pulses. No such theorem was obtained in the inspected corpus.

The supplied old ingredients allow both outcomes. With the *same* wave equation, zero initial data, cap rho, gamma=beta1=1 and beta2=0, but target zero, the whole cost is nonnegative and J(u)>=||u||L1>=||u||L2^2/rho. Zero has the same trivial exact cone and positive global L2-squared growth. With target pi*e the construction instead loses growth. Therefore the general framework does not decide the wave instance until the threshold-tuned data and their consequences are supplied. This is a checkable quantifier test, not an argument that all specializations are novel.

## Defensible status recommendation

The evidence does **not** establish `already_solved` through an earlier complete covering result. Retaining `claimed_solved` for the narrowly stated negative implication is defensible if the complementary recent audit finds no actual covering assertion and the final note makes the prior mechanism and limited scope explicit. That recommendation is conditional on the parent's completed combined priority assessment; it is not independent publication clearance or a proof of historical novelty.

The note should lead with the concrete energy-critical wave counterexample, openly state that its cone is zero, identify the unchanged implication being refuted, and credit the old abstract/non-coercivity framework. It should call the proof an elementary realization using established state differentiability, rather than advertise a newly discovered general necessity for NDC. It may include stronger verified assertions, but those cannot be used to evade a genuine prior covering resolution of the core if one is later found.

The correct remaining priority gap is a bounded-search gap about earlier source-model coverage. It is not an unsupported mathematical gap in B1–B8. Bounded failure to locate a prior theorem is insufficient to certify worldwide absence. No outreach was initiated or prepared.
