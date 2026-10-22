# Exact sequences for logarithmic lattice sheaves

**Status: UNSOLVED. Five new shared mathematical passes completed; independently audited partial results.**

The total number of earlier lifetime attempts is unknown. The five-pass count describes this investigation only. The [independent reader-edition review](PACKAGING_ACCEPTANCE.md) is complete.

This reader addresses Mücksch's constructive Problem 6.3 in [arXiv:2008.13700v3, p. 18](https://arxiv.org/abs/2008.13700v3), also posed in the [2021 Oberwolfach report, printed p. 288](https://ems.press/content/serial-article-files/46883). The question asks for natural short exact sequences relating the logarithmic **lattice sheaves** of an arrangement, deletion, and ordinary or Ziegler restriction. It does not prescribe all the terms, maps, or comparison spaces. The results below therefore establish positive constructions and precisely scoped obstructions; they do not settle the entire question.

Read this overview first. Complete authored proofs and their independent mathematical audits are linked below. The [bounded checks](CHECKS.md) are reproducible supplements, not proofs of untested cases or claims of novelty.

## 1. What is proved

Let A be central and essential in V over a field K, with dimension ℓ≥2, and mark H=ker α. Put S=Sym(V*), R=S/(α), A′=A\{H}, and B=A^H. The base P is the poset of **all nonzero flats** of A, ordered by geometric inclusion. On its upper Alexandrov topology, a sheaf is a covariant functor. The target-bearing subposet Q consists of the flats contained in H, with closed inclusion i:Q→P.

Write D_X=D(A_X), F_X=D(A′_X), and E_X={θ∈D(A_X):θ(α)=0}. The sheaf F is a canonical exact direct-image transport of the geometric deletion functor. Let Z denote the derivation lattice sheaf of the genuine Ziegler multiarrangement (B,m^H). The coefficient ideal I has stalk αS on Q and S off Q, with the actual inclusion transitions. In particular, I is **not a uniform grading shift**.

### Genuine short exact sequences in substantial classes

The canonical multiplication and reduction maps always give independently identified kernels:

- 0 → I⊗F → D → i_*D_B
- 0 → I⊗E → E → i_*Z
- 0 → E → D → I → 0

The first two become short exact sequences over every field in each of these cases:

- ℓ≤3
- H is a coloop
- H contains no nonzero deletion flat (the “flat-transverse” condition)

The third condition holds for a nonempty Zariski-open set of newly added marked hyperplanes over an infinite field. Over finite fields, existence is not asserted. An explicit rank-five example proves that it includes arrangements whose marked original and deletion localizations are nonfree.

There are additional sufficient conditions: freeness of each relevant deletion localization for ordinary restriction, and freeness of each relevant original localization for Ziegler restriction. These conditions are distinct. The ordinary Euler multiplicity and the Ziegler multiplicity are not interchangeable.

The proofs also establish canonical reflexive-hull descriptions of both restriction images and a natural **pointwise module Ext** formula for the ordinary defect. This Ext is not internal sheaf Ext or lattice-sheaf cohomology.

See [common-poset construction](proofs/01_common_poset_sequences.md), [restriction defects](proofs/01b_restriction_defects.md), and [generic hyperplanes and transport](proofs/05_alternative_lattice_transports.md).

### Corrected constructions in every rank

Explicit two-term tangency complexes give unconditional short exact sequences of complexes. Their degree-zero cohomology sheaves are the actual named derivation sheaves. Taking cohomology sheaves yields

0 → I⊗F → D → i_*D_B → I⊗T′ → T_A → i_*T_rep → 0,

0 → I⊗E → E → i_*Z → I⊗U → U → i_*T_Z → 0.

Here T′, T_A, T_rep, U, and T_Z have independently specified finite matrix presentations. The ordinary repeated rows are different from the multiplicity powers in the Ziegler complex. The local Ziegler defect is Tor₁^S(U_X,R), with its grading retained.

These complexes yield long exact **hypercohomology** sequences and two-row spectral sequences retaining their extension data. A six-term exact sequence of sheaves does not itself become a long exact sequence of ordinary sheaf cohomology by concatenation.

The normal sequence splits as a sheaf sequence exactly when H is a coloop. Nevertheless I is acyclic, and H^k(P,E)≅H^k(P,D) for k≥1. Both restriction defects are supported on nonzero flats X⊆H with dim X≤ℓ−3; their cohomology vanishes above degree ℓ−4. For ℓ≥4, the restriction-image cohomology agrees with that of the named target from degree ℓ−2 onward. The lower-degree correction is retained.

See [all-rank complexes](proofs/02_tangency_complex_sequences.md) and [cohomological corrections](proofs/03_cohomological_corrections.md).

### Fixed-term and transport obstructions

For ℓ≥3, on the specified common poset, all coefficient-degree-zero S-linear maps to the ordinary target and from E to the Ziegler target are classified. A degree-zero epimorphism exists exactly when the corresponding canonical restriction is onto. This covers reducible ordinary restrictions and requires no extra naturality across different arrangements.

The credited four-plane and seven-plane examples, promoted to essential rank four, have nonzero defects at retained line flats. Hilbert-series discrepancies also obstruct exact sequences with the specified graded endpoint modules, including arbitrary rank-one grading twists. A separate transport result shows that an exact change of poset preserving the compatible derived-global-sections construction cannot erase a defect visible to those derived global sections.

The tempting open-complement direct image does identify the deletion functor in degree zero, but can have an explicit nonzero higher direct image. Standard open/closed recollement supplies different terms; it does not identify the named restriction or the desired deletion cohomology.

The final audited result removes the grading restriction for the two fixed-poset source/target pairs. **All S-linear sheaf maps**, with arbitrary polynomial degrees and no across-arrangement naturality assumption, are classified. An epimorphism D→i_*D_B exists exactly when canonical ordinary restriction is onto; an epimorphism E→i_*Z exists exactly when canonical Ziegler restriction is onto. Thus changing ungraded arrows cannot remove these fixed-poset defects, whatever kernel is proposed. This theorem assumes ℓ≥3 and works over every field; its seven-plane application retains characteristic ≠2.

There is an important distinction at isolated stalks. The promoted four-plane E/Z stalk has no ungraded epimorphism at all. The seven-plane D/D_B stalk **does** admit an ungraded epimorphism, but its kernel cannot be the actual deletion module, even after a rank-one twist free at the tested prime: the relevant Ext lengths are 2 and 4. Sheaf compatibility is essential to the ordinary rigidity theorem. Separately, rank-two direct D/F/Z exact stalk sequences do exist after forgetting grading, so the earlier graded obstruction is not extended to that ungraded case. No gluing of those isolated stalk sequences is claimed.

See [graded classification](proofs/04_graded_sequence_rigidity.md), [ungraded classification and epimorphism rigidity](proofs/06_ungraded_restriction_rigidity.md), [ungraded local distinctions](proofs/07_ungraded_local_obstructions.md), and [transport proofs](proofs/05_alternative_lattice_transports.md).

## 2. A separately scoped source-version counterexample

For A in K⁴ defined by xyz(x+y+z)w=0, the complete geometric-inclusion functor on all nonzero flats satisfies H^n(P,D)=0 for every n>0, while D(A) is nonfree. Its explicit minimal resolution and a local-cohomology calculation also distinguish the punctured-affine H² from lattice H².

The [complete authored proof](appendix_v3/coloop_consistency_calculation.md) and [independent adversarial audit](appendix_v3/audit_coloop_consistency.md) establish counterexamples to the literal **Corollary 1.6 and Theorem 1.1 at n=2 in arXiv:2008.13700v3**, dated 12 October 2021. They identify a concrete quotient/Tor error in that version's argument.

This conclusion is limited to those inspected statements in that version. The later [published version](https://doi.org/10.1007/s00208-022-02499-1) has not been inspected here. No claim is made that all statements in the paper are wrong, that its published version contains the same error, or that the source has been fully repaired. The counterexample does not solve Problem 6.3. None of this reader's positive results imports the affected unrestricted freeness-from-cohomology inference.

## 3. Boundaries that matter

- **The whole constructive problem remains unresolved by the results currently included.** Other terms, maps, categories, or comparison spaces are not excluded merely by failure of a prescribed sequence.
- For nonessential deletion, the geometric deletion poset retains its nonzero center. It is not the source's center-deleted poset. The coloop case has a separate proved product formula for the latter's actual cohomology.
- At ℓ=2 the restriction is one-dimensional. Its punctured-poset global sections need not be its full logarithmic derivation module. The stated sheaf sequences still make sense, but that module identification cannot be imported.
- The four-plane example xyz(x+y+z) and the seven-plane example are credited to Abe–Kawanoue, [Example 4.3(2)–(3), arXiv:2406.00305v2](https://arxiv.org/abs/2406.00305v2). Their all-field calculations, promotion to retained stalks, and refined defects are carefully distinguished from discovery of those examples. The seven-plane simple-arrangement argument requires characteristic different from 2; in characteristic 2, two original planes coincide.
- The source search was bounded. There is no exhaustive openness, literature-completeness, or novelty certificate.

## 4. Proof and audit reading order

1. [Common-poset construction](proofs/01_common_poset_sequences.md) and [restriction defects](proofs/01b_restriction_defects.md); [joint audit](audits/01_common_poset_sequences.md)
2. [Tangency complexes](proofs/02_tangency_complex_sequences.md); [audit](audits/02_tangency_complex_sequences.md)
3. [Cohomological corrections](proofs/03_cohomological_corrections.md); [audit](audits/03_cohomological_corrections.md)
4. [Graded rigidity](proofs/04_graded_sequence_rigidity.md) and [alternative transports](proofs/05_alternative_lattice_transports.md); [joint audit](audits/04_graded_rigidity_transports.md)
5. [Ungraded rigidity](proofs/06_ungraded_restriction_rigidity.md) and [local obstructions](proofs/07_ungraded_local_obstructions.md); [joint audit](audits/05_ungraded_sequence_results.md)
6. [Version-scoped counterexample](appendix_v3/coloop_consistency_calculation.md); [audit](appendix_v3/audit_coloop_consistency.md)

The reports retain their complete accepted mathematical content, original notation, and historical artifact names. Process-only editorial changes are recorded against the exact accepted input hashes. Use [CHECKS.md](CHECKS.md), rather than historical run commands in those reports, for the safe stdout-only reader checkers. [EDITIONS.json](EDITIONS.json) identifies accepted input hashes and every reader-edition change. All mathematical components and the reader-edition packaging have independent acceptance.

## 5. Sources and evidence

[SOURCES.json](SOURCES.json) contains public source URLs, exact PDF byte hashes/sizes, inspection records, and version/access limits. It contains no source PDF or extracted source text. Relevant primary sources include Mücksch; Abe–Denham's derivation/form restriction results with their precise hypotheses; Abe–Kawanoue's Euler/Ziegler cokernels; Everitt–Turner's separately scoped homological framework; and Denham–Schenck–Schulze–Wakefield–Walther's generic/good-characteristic special cases. The original reports state exactly which results are used.
