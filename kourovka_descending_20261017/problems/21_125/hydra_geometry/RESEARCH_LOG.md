# Ordinary Hydra geometric research log

## 2026-10-24 21:39 UTC — scope and independent mechanisms

Target: Kourovka 21.125(b), ordinary Hydra groups G_m for m>=5. Exact source and priority contract read from ../priority/. Small ranks m<=4 are reported prior work and not original targets. The target is virtual specialness without a compactness hypothesis.

Independent mechanism families: (1) explicit canonical CAT(0) square-complex covers and hyperplane obstructions; (2) inductive cubical HNN combination along cyclic axes, distinguishing algebraic conjugacy from cubical local-isometry hypotheses; (3) wall/hierarchy extensions beyond the one-vertex tubular theorem. No conclusion from CAT(0), Ackermann subgroup distortion, or free cubulation alone.

Source inputs: Dison–Riley, Hydra groups, printed p.511 alternate square presentation; Wu–Ye arXiv:2504.14192v2, Theorems4.2/4.5 and scope of tubular hypotheses. These were read from primary cached texts in ../priority/sources/.

Discovery completion estimate: 2%. No candidate full resolution; no publication gate open.

## 2026-10-24 21:51 UTC — finite-cover mechanism checkpoint

Derived exact hyperplane transport and spanning-tree stabilizer L_m. Proved all abelian-monodromy covers retain first-square self-intersections for m>=3, plus an involution-quotient filter. Exhausted connected small permutation actions through degree8 for ranks3/5 (and degree6 for ranks2..6); no crossing-free cover found there. Constructed a regular24-sheeted wreath quotient for rank3 with **no self-intersections**, decisively rejecting any extrapolation from that bounded search. Full incidence check finds96 inter-osculating germ pairs, so it is not special. Rank2 reproduces an already-known special small-rank case. Higher ranks collapse under this shallow quotient.

Strongest proposed partial result: exact abelian-cover obstruction and regular-cover membership filter, together with exact finite examples. Independent review pending. Full m>=5 discovery estimate: 4%; no full candidate and publication gate closed.

## 2026-10-24 22:00–22:10 UTC — certified rank5 quotient and adversarial falsification

The exact F101 Lie quotient search found alpha2..alpha5 outside the hyperplane Lie image at class10, after classes<=9 failed for alpha2. Constructed and froze a1.1MB certificate: Rdimension226, relation ideal31, Wdimension88, quotient grouporder101^195. Standalone verifier checks every potentially nonzero R/W basis bracket, ideal condition, actual ring-unit relator, all L generators, and dual separating values1. This proves a canonical rank5 cover with no self-intersections, not specialness.

Rather than assume Lie-span membership implied group membership, independently collected actual truncated-ring units and extracted a192-node group word. A second verifier evaluates powers by binary squaring and proves an exact identity h*s=1, with h using L-generator seeds and ideal exponentials. Hence q(s) lies q(L5). Derived the corresponding explicit inter-osculation of alpha3+/alpha4+ germs. This **falsifies** the class10 cover as a specialness construction. The exact obstruction is now stronger than merely leaving other pathologies unchecked.

The old canonical-cover package independently passed review (root message). New finite Lie/group delta frozen for fresh independent review. The candidate general triangular threshold from ranks3,4,5 is only an unproved pattern; no extrapolation is used. Exploratory classes11 and12 agreed on existing alpha_j exclusions; class13 was intentionally interrupted as an unneeded extension, with no mathematical conclusion drawn from the interrupted computation.

Also recorded a fixed local link5-cycle excluding VH structures on every cover, and exact Britton-normal-form intersections for L_m. HNN/equitable-wall routes fail at unproved compatible finite-quotient and double-coset separation requirements. Author-family outcome: unsolved. Full Hydra discovery estimate6%, no publication gate open. No external communication, git action, or unrelated files changed.
