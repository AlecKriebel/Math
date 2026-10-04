# Independent adversarial audit: KP-4.119 / 2995

Audit date: 2026-10-04 UTC. Scope: the frozen seven-payload candidate in `../bundle`, five failed approaches and seven partial statements. This is a mathematical and reproducibility audit, not a sixth proof-search attempt, an expert peer review, or a claim to settle the target.

## Verdict

**Mathematical verdict: pass as a carefully limited, unsolved partial investigation.** No blocking mathematical error was found in the seven statements or the scope of their applications. No arbitrary CW structure is constructed for a compact nonsmoothable 4-manifold, and no obstruction to all arbitrary CW structures is proved. The appropriate mathematical status remains **unsolved, five approaches used**. There is no candidate complete resolution and no verified novelty claim.

**Provenance qualification:** the supplied proof anchor agrees exactly, and the seven files satisfy the frozen manifest. The reviewer independently computed the manifest hash below. The coordinator confirmed that no independently supplied author manifest digest existed in the initial handoff; this is recorded in `AUDIT_RESULT.json`. The coordinator accepts the supplied proof anchor plus full current manifest/inventory verification for this scoped audit gate, with a separate author manifest check reserved for publication preflight. Mathematical acceptance does not invent historical manifest authentication.

## Frozen inputs and preservation

- Proof SHA-256: `9960b3632cd0e25986a4ac97f2a11e834663604adb1872d0fc0d1e510e9599cb`, matching the coordinator's supplied anchor.
- SHA256SUMS SHA-256: `72cc877fabada0d60ee5f88329f977e492f1c790dcd68c5350ad56ab1dbe553a`.
- All seven manifest entries verified before substantive review and again after the review.
- The original controls were inspected before execution; replay wrote only a separate audit output. The replay equals the frozen `CONTROL_RESULTS.json` byte for byte.
- No bundle file was edited. The audit and its independently written verifier are separate. Third-party PDFs and source-page screenshots are not part of the audit publication payload. No remote writes or external-person communications occurred.

## Exact target and source scope

The exact homeomorphism-to-CW question was independently read and visually checked at K3 Problem 4.119, printed pages 289-290. The statement is not a request for a homotopy model. The surrounding remarks distinguish smooth/noncompact positive cases from nonsmoothable nontriangulable examples. The candidate correctly asks about arbitrary, potentially nonregular CW structures and restricts its obstruction examples to closed manifolds. [K3](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf)

The 2024 v3 foundations source was checked at Questions 3.14-3.15, Proposition 3.11(b), and Theorems 3.5(2), 3.13, 3.16, 9.1 and 9.9. In particular, 3.16 supplies finite homotopy models, not homeomorphic cell structures. The question remains explicitly open in that source even for closed four-manifolds. Its separate high-dimensional boundary caveat must not be silently erased using a blanket handle-to-CW slogan. The candidate does not do so. [Foundations v3](https://arxiv.org/abs/1910.07372v3)

The 2025 algorithms source was read at Definition 3.5 and Theorem 3.6, including the scope of Theorem 3.6(3). The input link describes a smooth handle piece; the complementary contractible piece remains topological. Existence and uniqueness of that cap in the encoding are not a construction of a CW pair. Its closed, oriented, simply connected scope cannot resolve the unrestricted target. [Algorithms v2](https://arxiv.org/html/2411.08775v2)

## Statement-by-statement adversarial review

### 1. Compact subsets meet finitely many open cells: pass

The selection argument is valid. Closure-finiteness gives finitely many selected points in the image of each characteristic map. For every subset T of the selected set, its inverse image in every disk is closed because the relevant image points form a finite closed set in a Hausdorff space. Weak topology therefore makes every T closed in X. In particular, the selected set is closed in the compact A, and every one of its subsets is closed in the subspace. It is thus an infinite compact discrete space, the required contradiction.

No local finiteness hypothesis has been smuggled in. The stronger conclusion that the actual CW structure on a compact space has finitely many cells is justified. This is not merely existence of a different finite homotopy model.

The whiskered S^4 example is also valid: a point strictly inside the appended interval has an open interval neighborhood and local integral homology in degree 1, incompatible with a four-dimensional manifold point. It refutes promotion of that supplied homotopy model to a homeomorphism, not existence of another homeomorphic model for S^4.

### 2. Finite regular CW triangulation and E8: pass

The induction cones a triangulated cell boundary from a fresh vertex and uses the regular characteristic map to extend over a ball. Fresh vertices and the boundary subcomplex property prevent unintended identifications; common faces already have the same triangulation. Finiteness makes the resulting continuous bijection a homeomorphism. The standard regular-CW subdivision construction independently agrees with this argument. [Hatcher, Appendix on simplicial CW structures](https://pi.math.cornell.edu/~hatcher/AT/ATsimplicial.pdf)

For the closed examples at issue, the four-dimensional triangulation-to-PL implication and PL-to-smooth implication have the cited scope. The definite E8 form cannot be integrally congruent to a positive diagonal identity form because parity is invariant under an integral basis change. Freedman's existence theorem plus Donaldson's theorem therefore yields a nonsmoothable closed example, and Lemmas 1-2 exclude its regular CW structures.

This excludes only the regular target. There is no valid inference to arbitrary CW nonexistence. The standard two-cell CW structure on S^4 correctly illustrates that regularity of a chosen structure is a real additional condition, even for a manifold that also has regular structures.

### 3. Retaining the punctured decomposition: pass

A finite CW complex is compact; the punctured closed connected manifold is noncompact. Retaining an infinite family of its cells and adding a point would make a compact space into an infinite CW complex, contrary to Statement 1. This disposes precisely of the proposed fixed-cell compactification, not every reorganization of the cells.

The locally finite triangulation illustration is valid: its vertex set meets each compact subset of the punctured manifold finitely. An infinite sequence of distinct vertices has an accumulation subsequence in compact metrizable M, and the only possible limit is the missing point. Adding that point as a 0-cell would make the inherited 0-skeleton nondiscrete.

### 4. Smooth product end: pass

The cofinality, compact-complement and smooth-boundary assumptions are essential and are present. Truncation leaves a compact smooth manifold with standard smooth S^3 boundary; attaching a smooth ball produces a smoothing of the one-point compactification. A radial identification of the punctured ball with the product end verifies the underlying topology, and uniqueness of one-point compactification finishes the argument.

This does not deny the topological product end of a punctured topological manifold. It rules out the specified smooth product end for a nonsmoothable compactification. Nor does it claim an uncontrolled smooth end cannot support arbitrary CW data.

### 5. Compatible finite CW-pair gluing: pass

The hypotheses genuinely suffice. A boundary homeomorphism cellular in both directions sends each skeleton onto its counterpart. It therefore sends components of Y^(n) minus Y^(n-1), namely the open n-cells, bijectively to the corresponding components. Boundary cells can consequently be identified cellwise, as the proof requires. The remaining characteristic maps keep their interiors injective, and their boundaries lie in the required lower skeleta.

The finite disjoint union of characteristic disks is compact; its map onto the glued Hausdorff space is a continuous surjection and hence a quotient map. This supplies the weak topology, while closure-finiteness follows from finiteness. The condition is not known to follow from contractibility of the cap. No topological cap has been silently replaced by a homotopy equivalent point or cone.

### 6. Nontrivial-fundamental-group cone cap: pass

The conical neighborhoods form a neighborhood basis because Y is compact. If the cone vertex had a Euclidean chart, choose a sufficiently small chart ball inside one conical neighborhood and then a smaller conical neighborhood inside that ball. On puncturing, the inclusion between conical neighborhoods induces an isomorphism on pi_1, while its factorization through the punctured four-ball is trivial. A basepoint may be fixed in the smallest neighborhood, so the contradiction is legitimate.

If the convention allows boundary charts, the same argument works with a half-ball whose removed point is on the flat boundary; that punctured half-ball is also simply connected. Adding that phrase would make the boundary convention explicit, but the application to closed glued manifolds already uses an interior vertex. Correct homology of a homology-sphere link does not repair its nontrivial local fundamental group.

### 7. Vanishing KS and failed smooth/PL destabilization: pass

The connected sum E#E has the direct-sum form, signature 16, and even parity. Freedman's even-form formula gives Kirby-Siebenmann invariant zero, so the cited sum-stable smoothing theorem applies. Donaldson excludes a smooth structure before stabilization because the positive definite even form cannot equal the odd standard positive diagonal form. This application is also explicitly corroborated in Manolescu's Theorem 3.4 discussion. [Manolescu, Four-dimensional topology](https://web.stanford.edu/~cm5/4D.pdf)

Consequently no cancellation restricted to smooth or PL structures can recover the original F. This does not obstruct a descent process using arbitrary nonregular CW cells. The candidate also correctly notes that E itself retains nonzero KS after S^2 x S^2 stabilization. No dimension-five stable-smoothing claim is substituted for the dimension-four connected-sum theorem.

## Reproducibility and independent controls

1. Original command: `python3 ../bundle/controls.py`. The captured JSON is byte-identical to the frozen output; its hash is `16aaa5d26fec38b6c82f3b74e26eba723bd9f2f8a39610114043d78c5be2ebfa`.
2. Independently written `independent_controls.py` does not import or reuse the original implementation. It reconstructs the E8 graph, factors its matrix as L D L^T using exact fractions, explicitly multiplies the factors back, and checks its determinant by sparse Laplace expansion.
3. The exact D diagonal is 2, 3/2, 4/3, 5/4, 6/5, 7/6, 8/7, 1/8. Positivity proves positive definiteness. Cumulative products give leading minors 2,3,4,5,6,7,8,1. The direct-sum factorization repeats the diagonal, verifying determinant 1 and signature 16.
4. All 256 binary residue classes of E8 have even norm; symmetry and even diagonal independently give the universal parity formula. This is not an extrapolation from the author's 6,561 sampled vectors.
5. Fault controls detect deleted-branch determinant 16, an odd diagonal entry, a duplicate-row singular matrix, and hyperbolic determinant -1.

These are exact finite algebra checks only. They cannot establish the existence of manifolds, Freedman's classification, Donaldson's theorem, smoothability, CW characteristic maps, or cap compatibility. The candidate states that limitation correctly.

## Literature, novelty and operational scope

A fresh bounded web check found the same primary sources and no verified resolution. A 2026 paper with a superficially relevant simplicial-approximation title explicitly assumes an existing CW structure and constructs homotopy-equivalent models, so it is not a solution to the missing existence problem. [Tinarrage, SoCG 2026](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2026.93)

Automated-answer aggregators surfaced mutually incompatible claims; none was used as theorem evidence. Absence of a result from a bounded search is not a comprehensive priority certificate. The author makes no novel-theorem claim, and this audit approves no such claim.

The five mechanisms are genuinely different: finite homotopy models, regularization, punctured compactification, contractible-cap gluing, and stabilization/descent. This audit validates their written content and distinct scope; it cannot independently certify the wall-clock chronology of the author's earlier work. No new route was opened here.

The repository queue must preserve its existing exhaustion semantics. The mathematical display may say unsolved with 5/5 approaches; an automatic exhausted state must not be reset. Live duplicate/queue checks and authorized publication are the coordinator's separate responsibility. This audit did not revalidate the remote-head snapshot in SOURCE_STATUS.md and makes no claim that it is still current.

## Corrections and final gap

No blocking mathematical correction is required. `CORRECTIONS.md` records two optional proof clarifications and the manifest-receipt prerequisite. The unchanged final gap is an actual finite cellular construction on every compact nonsmoothable four-manifold, with valid characteristic maps and topology, or an obstruction to every possible arbitrary CW structure.

Discovery completion remains 0% of that missing general proof. Bounded mathematical audit completion is 100%. The separately recorded author manifest verification remains a publication-preflight action; these percentages are administrative, not probabilities.
