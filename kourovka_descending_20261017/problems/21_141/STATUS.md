# Kourovka 21.141 — unsolved in this effort

Checkpoint: 2026-10-17 UTC. Discovery completion estimate **12%**;
this is a subjective research-progress estimate, not a correctness probability.

The exact target is coherence of a free pro-p amalgam of coherent pro-p
vertices over a polycyclic pro-p edge. The current official 6 October
edition, p.198, leaves the entry unanswered. Primary proposer-authored
sources identify polycyclic with a finite closed subnormal series having
procyclic factors. Closed subgroups, continuous maps, topological generation
and pro-p presentations are essential. Properness is the main research
convention; the official wording itself does not expressly specify it.

No unrestricted proof or counterexample was found after independent
homological, tree, algebraic and explicit-counterexample investigations.
No partial result has been promoted to a solution.

## Reviewed positive mechanisms

- Finite presentations pass through pro-p extensions. Coherent quotients
  by topologically finitely generated normal kernels are coherent.
  A normal kernel whose every closed subgroup is finitely generated and
  finitely presented preserves coherence of a coherent quotient.
- These prove normal-edge and malnormal-modulo-normal-kernel cases.
  The malnormal analytic-edge theorem itself is prior work, explicitly
  credited to Castellano–Zalesskii. Finite and procyclic edges are also
  already covered by known structural results.
- Commensuration by every element of each compact vertex yields a common
  subgroup open in H and normal in G, reducing to the finite-edge case.
  Berdugo–Zalesskii's stronger finite-generating-commensurator lemma is
  prior work (published 27 February 2026), not a new discovery here.
- If a finitely generated closed subgroup has finitely many edge orbits
  on the standard tree, continuous Mayer–Vietoris and Shapiro first force
  finite generation of vertex stabilizers, then finite presentation of the
  subgroup. The finite-orbit assumption is not automatic.
- Every finitely generated kernel of an epimorphism onto a finitely
  generated abelian pro-p group is finitely presented under the hypotheses.
  This excludes the standard abelian-fiber counterexample family while
  leaving arbitrary subgroups untouched.

## Failed shortcuts and useful diagnostics

- A proper reduced rank-two path family P_n has d(P_n)=2 and
  r(P_n)=dim H2(P_n,Fp)=n+1. A faithful modification Q_n=P_n coproduct Zp
  has d=3 and arbitrarily many edges with fixed nontrivial edge type Zp^2.
  Thus uniform graph-size or relation-rank bounds in these few parameters
  are unavailable. This is not fixed-group inaccessibility or noncoherence.
- The compatible inverse limit of the P_n is free pro-p of rank two:
  their defining relations eventually vanish in every finite p quotient.
  Unbounded finite-stage relation ranks therefore do not produce a
  non-finitely-presented inverse limit in this attempt.
- Commensurability cylinders need not be closed in a proper pro-p amalgam
  without further hypotheses. The diagnostic factors are not asserted
  coherent, so this is a topology obstruction to the proposed argument,
  not a counterexample to the original problem.
- An explicit nonproper shear pushout collapses its entire analytic edge
  and becomes free pro-p of rank two. Nonproperness by itself supplies no
  counterexample. Replacing arbitrary coherent vertices by quotient images
  need not preserve coherence. A finitely normally generated kernel is
  not necessarily topologically finitely generated as a subgroup.

## Verification and exact remaining gap

A fresh adversary checked the new partial arguments, source hypotheses,
category conventions and finite-orbit sequences. Root reproduced 96
finite-field/lattice cases, 343,400 inverse-system interval cases, and the
shear checks for eight primes. The added relation-rank/inverse-limit
deductions passed a followup audit. These computations supplement exact
proofs; they do not test the full coherence question.

See approach_homology.md, approach_tree.md, approach_counterexamples.md,
counterexample_raag/FIBER_OBSTRUCTION.md, priority_20261017.md and
reviews/partial_adversary01.md for precise claims and source limitations.
No novelty certification, formal verification or independent human peer
review is claimed for these notes.

The unrestricted obstacle is control of infinite profinite orbit families
and the associated completed homology, or a different argument for every
finitely generated closed subgroup. Pointwise finite generation of edge
stabilizers does not supply this control. Tree contraction, rank induction
and a generic finite-core lemma remain unsupported at exactly this step.
Further searches concerning general normal kernels and nonproper
pushouts are exploratory only. No preprint, Zenodo upload, DOI or tracker
row is associated with 21.141.
