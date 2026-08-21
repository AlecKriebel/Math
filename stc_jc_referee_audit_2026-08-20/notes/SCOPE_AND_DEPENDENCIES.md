# Exact claim reconstruction

## Positive theorem scope

- Objects: two leaf-labelled, binary, level-2, already-simple mixed graphs on the same taxon set that arise by the single root suppression `sd_0` of an LSA-valid rooted binary network (manuscript Definition 2.1, PDF pp. 3-4; TeX lines 235-268).
- Class: `S_TC`, meaning at least one admissible rooting exists and **every** admissible rooting of the fixed mixed graph is tree-child (PDF p. 4; TeX lines 280-340). This is narrower than weak tree-childness and tied to the manuscript's fixed-mixed-graph convention.
- Stochastic domain: every JC Fourier edge multiplier and inheritance probability is strictly between zero and one; the root distribution is uniform (PDF p. 5; TeX lines 362-401).
- Directed observation relation: `N <=_JC N'` requires a source-regular common distribution and a relatively open neighborhood in the regular source image contained in the target open stochastic image; the target dimension may be larger (Definition 2.4, PDF p. 6; TeX lines 403-418).
- Symmetric observation relation: `N bowtie_JC N'` requires a common full-local-dimensional regular germ in both model images (same location).
- Theorem 1.1 conclusion: directed containment occurs iff the labelled reduced bridge trees agree and every corresponding nontrivial blob is labelled-isomorphic or differs by an ordinary triangle redirection that changes only the triangle reticulation vertex/arrowheads. The same condition characterizes the symmetric relation; hence no proper one-sided containment exists within this class (PDF pp. 2-3; TeX lines 180-195).
- Corollary 1.2: outside a topology-dependent proper algebraic subset of the complex model closure, a distribution in the open source image determines the labelled standard semi-directed topology modulo ordinary triangle redirection (PDF p. 3; TeX lines 197-202).

## Sharpness scope

- Theorem 1.3 concerns the larger weak-but-not-strong class. For every `n >= 4`, two triangle-free level-2 networks have nonisomorphic/non-triangle-related topology and share a regular relatively open germ of common image dimension `2n+1` (PDF p. 3; TeX lines 204-215).
- The separate Theta family is triangle-containing and has common dimension `2n`; it is not asserted as a move or ambiguity inside the strong class (Theorem 9.3, PDF pp. 25-27; TeX lines 1688-1802).

## Dependency graph reconstructed from the proofs

1. Definition 2.1 + Lemma 2.2 (no-omnian criterion) -> locked class convention and strong repairs.
2. Lemmas 3.1-3.2 + Proposition 3.3 -> cycle/four-theta primitive-core exhaustiveness; Proposition 3.4 -> at most one triangle per strong blob.
3. Lemmas 4.1-4.2 + exact Lemma 4.4 -> Theorem 4.3 pointwise cut ranks -> Corollary 4.5 bridge-tree/decorations.
4. Theorem 5.1 exact positive incidence fibre -> Lemma 5.3 local product chart; Lemma 5.4 finite-cover fact -> Proposition 5.5 projective localization/no cross-blob compensation.
5. Lemma 6.2 marginal open image + rigid-support/completion grammar + Theorem 6.3 finite decorated relation -> restoration; Lemma 6.4 coherent probes -> necessity in Theorem 6.1.
6. Lemma 6.5 ordinary triangle common germ -> local converse; Lemma 6.6 simultaneous physical gluing -> global converse.
7. Corollary 4.5 + Proposition 5.5 + Theorem 6.1 -> Theorem 1.1 necessity; Lemma 6.6 -> sufficiency and symmetric germ.
8. Theorem 1.1 + semialgebraic dimension/Zariski-closure argument -> Corollary 1.2.
9. Identical-cherry analytic inverse + Omega topology/equality/rank certificates -> Theorem 1.3; analogous Theta algebra/rank calculation -> Theorem 9.3.

## Initial proof checks completed before archive-code inspection

- All 31 manuscript pages and all 7 supplement pages were rendered and visually inspected; both extracted TeX sources were read completely.
- The combinatorial crossing-quartet split reduction, the displayed two-endpoint determinant identities, the finite-cover lemma, the cherry inverse, and the dimension logic of the localized Theta equations are internally consistent on direct algebraic checking.
- The load-bearing unresolved obligations are exactly the claimed endpoint/open-cube sign universe, marginal descriptor surjectivity for every permitted restriction, bounded directed-relation exhaustiveness, restoration/probe coherence, and the exact Omega/Theta graph-to-Fourier and Jacobian computations. These now require archive-to-primitive code tracing rather than acceptance of manuscript assertions.

