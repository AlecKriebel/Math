# Audit of prior results on vertex critical edge resilience

Audit date: 11 October 2026. Target: EP944 / problem 2398.

## Decisions

1. **Accept with explicit local corrections:** Skottová and Steiner, *Critical edge sets in vertex-critical graphs*, arXiv:2508.08703v1, proves existence for every fixed integer k >= 5 and every r >= 1. Its stronger all-sufficiently-large-orders cube-root lower bound and square-root subsequence lower bound also survive the audit. The full 24-page proof, including both appendices, was read. The corrections and dependency closure are supplied in PROOF.md and AUDIT.md. None changes the theorem's hypotheses or bounds. The lower-bound proof does not import Jensen's theorem.
2. **Accept the separate finite example at an independently checked computation boundary:** the Cayley graph published in Alex Chan's repository at commit 697307af42505b11490fdc74c04eda5c7ec76c51 has 60 vertices, 180 edges, chromatic number 4, and every vertex deletion has chromatic number 3. Every single-edge deletion still has chromatic number 4. Two independently authored exhaustive search formulations, with different branching rules and symmetry treatment, establish the needed non-colorability claims. No downloaded author code, certificate tree, package, or Lean project was executed.
3. **The finite example has exact three-color defect 2.** An independently checked two-edge deletion gives a proper three-coloring. The edge labels and coloring assignments are omitted from this prose edition. Thus this graph does not work for r = 2, and its one-edge result cannot establish the original every-r assertion at k = 4.
4. **Accept the upper-bound implication using the identified external theorem:** the proof of f_k(n) = O(n/(log n)^c), for fixed k >= 4 and an absolute c > 0, is correct conditional on Conlon and Fox's Lemma 8.1. Its exact statement and regularity convention were checked in the primary author-hosted PDF. That source expressly omits proofs of Lemmas 8.1 and 8.2. This audit does not claim a first-principles proof of that external regularity theorem. This dependency is wholly separate from the closed lower-bound proof.

The exact original question is whether, for every k >= 4 and r >= 1, there exists a finite simple k-vertex-critical graph G such that chi(G-R)=k for every edge set R with |R| <= r. The graph may depend on k and r. Erdős's printed page 113 was visually rechecked: it says k >= 4. The adjacent single-edge question and stronger order-dependent question are distinct.

**Residual within these audited results:** k = 4 and arbitrary r >= 2. This is a scope conclusion about the retained sources and verified example, not a claim to have exhaustively established the global current literature status. No attempt to solve that residual family was made. No claim of novelty or whole-problem resolution is made.

## Quantitative statements accepted

For integers k >= 5, r >= 1, put A = 8(k-1)(18r+3). Skottová-Steiner's Theorem 1.3 gives a (k,r)-graph at every order

    n >= A(6r+3)+1,   n = 1 mod A.

Their Theorem 2.3 gives a (k,r)-graph at every integer order

    n >= A[16(k-2)(k-1)(18r+3)(6r+3)+2].

Consequently, for each fixed k >= 5, f_k(n) = Omega_k(n^(1/3)) as n tends to infinity through all integers. At n_r = A(6r+3)+1, f_k(n_r) >= r = Omega_k(sqrt(n_r)). These are existing results of Skottová and Steiner.

## Independent finite verification

The first verifier reconstructs the graph from its published algebraic definition and six generators, checks its exact edge-list hash, verifies all 60 left-translation automorphisms and all 60 transported vertex-deletion witnesses, and exhaustively solves four single-edge deletion representatives. Their verified orbit sizes are 60, 60, 30, 30. Search node counts are 1230, 1464, 1207, 1219.

The second verifier uses forward checking and every color branch, with no color-symmetry or graph-orbit quotient. It directly solves G and each of the 180 single-edge deletions: all 181 are not three-colorable, with 1,651,066 total search nodes. It separately finds proper colorings of a vertex puncture and a two-edge deletion.

Both search routines were compared against direct enumeration of all color assignments on every labeled graph on one through five vertices, for both two and three colors: 2,198 cases per solver. The final independently authored verifiers were run in normal Python, -O, and -OO modes, producing the retained historical receipts. No correctness check depends on an assert statement. The historical verification used exact integer computation. This prose edition omits the code, graph data, coloring witnesses, and search certificates required for computational reproduction. It reports the authenticated historical outcomes rather than independently replayed Lean proof or kernel-only verification.

## Formal source boundary

Static inspection confirms that the structured Lean definitions express vertex-criticality and deletion of one undirected edge in the usual way. The source separates a generic balanced-puncture argument from finite data checks. Its reported final axiom list includes Lean.ofReduceBool as well as propext, Classical.choice, and Quot.sound. That list is an author-supplied log; it was not regenerated here.

Both UniversalDecoupling.lean files prove conditional logical glue over an abstract graph type. They retain the order-four construction, the every-k-at-least-five result named jensenGeFive, and the low-chromatic obstruction as explicit hypotheses. Jensen is not silently installed as an axiom, and the all-k theorem is not formalized end to end in those files. The compact certificate uses bv_decide for its negative Boolean statements and native_decide for positive finite checks, according to the inspected source. Neither route was built or replayed in this audit. The finite acceptance above rests instead on the independent verifier.

## Publication and review boundary

Exactly eight authored proof, audit, acceptance, source-provenance, and verification-metadata files are distributed. PROOF.md retains the complete conventional lower-bound argument and the separately conditional upper-bound argument. AUDIT.md retains every correctness-relevant printed correction, the focused independent review, and the finite-audit methods and limits.

This is not a computational reproduction package. Copied source documents and images, executable code, graph/generator/coordinate data, coloring and certificate contents are omitted. The finite claim is accepted at the disclosed historical independent exact-computation boundary; its omitted data and programs are necessary to reproduce that computation. They are not premises of the conventional k>=5 proof. Preparing this edition performed no new mathematical run, scholarly-source retrieval, visual source inspection, or literature search.

This AI-assisted work is unrefereed. Acceptance means internal independent AI audit, not external human peer review, journal acceptance, or formal proof-assistant certification. The focused review accepted the full repaired lower-bound proof and exact quantitative orders with no additional required mathematical correction. No novelty, priority, whole-problem resolution, or exhaustive global current-literature claim is made. The general residual k=4,r>=2 is unresolved by this work.

## Primary references

- P. Erdős, *On some aspects of my work with Gabriel Dirac*, Annals of Discrete Mathematics 41 (1989), 111-116, printed p. 113: https://users.renyi.hu/~p_erdos/1989-19.pdf
- E. Skottová and R. Steiner, *Critical edge sets in vertex-critical graphs*, arXiv:2508.08703v1, 12 August 2025: https://arxiv.org/abs/2508.08703v1
- Alex Chan, fixed public repository commit: https://github.com/alexgocardinal/dirac-critical-graph/tree/697307af42505b11490fdc74c04eda5c7ec76c51
- D. Conlon and J. Fox, *Bounds for graph regularity and removal lemmas*, Geometric and Functional Analysis 22 (2012), 1191-1256, primary author-hosted PDF, Lemma 8.1 on printed p. 56 and proof-omission notice on p. 57: https://www.its.caltech.edu/~dconlon/RegRem.pdf

No claim about the content or attribution of a separate NBER manuscript is used.
