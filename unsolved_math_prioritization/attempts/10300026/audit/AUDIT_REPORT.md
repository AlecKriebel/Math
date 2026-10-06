# Independent audit: Calegari Question 8.3

Date: 2026-10-06. Problem 10300026 / AMR-102-0026; catalog rank 844.

## Verdict and acceptance boundary

**ACCEPTED AS A SCOPED AUDIT AND ELEMENTARY REDUCTION REPORT.** The reviewed v2 report does not solve the original problem. Its four elementary lemmas are correct under their stated hypotheses; its uses of the cited theorems preserve the relevant restrictions. No mathematical patch is required. Neither a new theorem answering the problem nor a verified counterexample is established. The original unqualified question's current global status remains **not established by this audit**.

Only the v2 candidate is accepted. Its archive is 19,002 bytes, SHA-256 `7f36eececb5ddcbdfd17e34a7dd015d081641b2d5aa555f093576ae9713df454`. The original v2 archive and its four members were not modified. Its frozen `independent_audit_status: PENDING` describes the author-stage snapshot; `ACCEPTANCE.json` is the independent disposition and must accompany any later presentation as independently reviewed. It must not be interpreted as approval of a general solution.

## Input binding and privacy

The entire supplied catalog, entire problems file, and entire research-results file were parsed independently. Their byte counts and SHA-256 hashes match the author metadata. Their record counts are respectively 15,458, 15,458, and 6,701. Selection by identifier finds one catalog row and one complete problem record, at rank 844. The catalog stores the identifier as text, whereas the problem record stores it as an integer; the independent comparison explicitly handles that difference.

The statement digest is `df1623ec850b43d288ee3b733ef4c0108852280687e2cd09c89c79a18659b6df`. The complete review digest is `d539a48fb43e8d346651b0e11607b0e6315c856cdaec3d0d156d348c4d77aca2`. It was recomputed from the complete 21-key problem object and complete 8-key research report, using default Python `json.dumps` separators and ASCII escaping, with `sort_keys=True`, on the two-element pair. It was not recomputed from a shortened summary or canonicalized substitute. `CORPUS_BINDINGS.json` and `verify_corpus_bindings.py` make these checks reproducible without publishing the data.

The public candidate contains authored exposition, authored elementary proofs, public citations, executable verification code, and bounded verification metadata. No source PDFs, extracted source text, dataset records, private sources, or private coordination materials are included. The superseded candidate and the exact redaction diff are excluded. Comparison of the two freezes confirmed that only the report member changed, at the passage replacing the copied question with an authored logical restatement. The replacement did not alter the mathematical argument or the executable validator.

## Exact mathematical target

The target is an existence implication about a manifold. The existence of one branching taut foliation does not preclude a different foliation with line leaf space. A negative answer requires the same manifold to satisfy the original geometric and tautness assumptions and to exclude every candidate of the required type. A classification of all such manifolds is unnecessary.

The original question adds no co-orientability clause. Moreover, [C] Definition 1.2 introduces R-covered foliations within the class of taut foliations. This convention matters when applying the line-action lemma: its explicit tautness hypothesis is retained, rather than extending the statement to all usages of the term R-covered in other literature. The report's extra closedness, connectedness, and nonsingularity assumptions govern its elementary partial statements; they are not silently inserted into the original question.

## Proof audit of the four lemmas

### 1. Covering invariance

For a connected covering of manifolds, composing it with the universal cover produces a simply connected covering of the base. Pullback foliations compose, so the universal lifted foliations agree as partitions on the same space. Quotient topology is determined by that partition, giving the asserted leaf-space identification. This proof concerns the pullback of a specified downstairs foliation. It correctly does not claim that an arbitrary foliation upstairs descends.

### 2. Descent through a finite regular cover

For a descended foliation, every deck transformation necessarily preserves the entire plaque structure. Conversely, regularity makes the deck group transitive on each fiber, and an evenly covered neighborhood permits one to transport a foliation box between sheets. Invariance makes the quotient charts independent of the chosen sheet and compatible on overlaps. Deck transformations may permute leaves; pointwise leaf fixation is not required. Co-orientation descends only when the chosen transverse orientation is also preserved. The R-covered conclusion follows from Lemma 1. The stated tautness observation uses projected closed transversals in the leafwise sense. A projection may be immersed; this does not invalidate the usual closed-transversal criterion, and a small transverse perturbation in dimension three yields an embedded representative when that convention is desired.

### 3. Surface bundles

The infinite cyclic cover of a surface bundle is a product with the line, and its universal cover is the product of the universal cover of the connected surface with the line. The fiber leaves become the slices, and product projection is an open quotient map with exactly those fibers. The circle direction supplies co-orientation. With the mapping-torus convention identifying the top using the monodromy, the specified path ends at the inverse image of its starting point; its graph therefore closes correctly. Its base coordinate traverses the entire circle, establishing transversality and intersection with every fiber. Stationary endpoint choices yield the stated smooth version.

[A] Theorem 9.2 supplies the finite fibered cover for closed hyperbolic manifolds. Taking the normal core yields a further finite regular cover; it does not prove that the pulled-back fiber foliation is invariant under the full deck group over the original manifold. The report correctly leaves this descent condition open.

### 4. Absence of a global fixed point

Deck transformations act on the lifted leaf space by homeomorphisms. If they all fixed one leaf-space point, lifting a closed transversal through that leaf would give a transverse arc whose endpoints lie in that same lifted leaf. In the line leaf space, the transverse parameter is locally strictly monotone. Its direction is locally constant and hence constant on the connected interval. It cannot return to its starting leaf-space value. This proves the claimed contradiction.

The conclusion is **no common fixed point for the group**, not a free action or absence of fixed points for every nonidentity element. No faithfulness claim is needed: for a bundle, the natural action can have the fiber subgroup in its kernel. Co-orientability implies orientation preservation; without it the action may include orientation reversals. An obstruction restricted to orientation-preserving actions alone therefore does not establish the unqualified negative certificate described in the report. The report preserves this distinction.

## Literature and status audit

The six source PDFs were individually checked against their stated byte counts and SHA-256 digests. Fresh `pdftotext -layout` extraction matched all six retained text extractions exactly. Relevant definitions, theorem statements, conventions, and question locations were then inspected; this is verification of cited scope, not an independent reproof of those papers.

- [C] confirms the manifold-level question and the potentially conflicting historical remark. The remark is not accepted as a stand-alone counterexample proof.
- [Z1] Theorem 1.1 has the connected, closed, orientable, irreducible, co-orientable-taut, one-sided-branching hypotheses recorded by the report. Left-orderability is not a realization theorem for an R-covered foliation on a prescribed manifold.
- [Z2] v2 is dated June 15, 2026. Its introductory global co-orientability convention governs Question 2. Its positive filling theorem is restricted by the monodromy, stable-foliation, and slope hypotheses. The report's projective interval uses the correct numerator and the denominators with plus/minus the boundary-orbit length, excludes the degeneracy slope, and does not replace the projective interval with an ordinary real interval. The theorem is not a general answer.
- [B] supplies graph-manifold examples containing incompressible tori. These do not satisfy the atoroidal requirement. Its hyperbolic question is not a 2026 status certificate.
- [R] announces a hyperbolic family, but the short conference abstract provides no construction or full proof and does not settle conventions. It remains an important unverified lead.

An additional primary source [S], inspected in this independent audit, describes the Roberts–Shareshian–Stein work as producing hyperbolic manifolds without Reebless foliations. Such examples cannot themselves satisfy the taut-foliation premise. This reinforces the need to reconcile the older citation instead of inferring a counterexample from it. It does not independently establish the announced 2004 family's properties or settle the original problem. The publisher and indexed-mirror attempts to open the full Roberts–Shareshian–Stein paper did not return a usable full document in this audit. No full proof from that paper is claimed to have been checked.

## Approach accounting

The actual report contains four substantive routes: covering and descent; the universal line-action obstruction; one-sided branching; and the restricted Dehn-filling construction. The first route includes three elementary lemmas, the second includes the fourth, and the latter two evaluate consequences of existing work. Four lemmas are not four separate attempted general proofs. The approach count of four is supported by the report itself.

The inherited data's suggested negative conclusion and classification-oriented stopping point are not accepted as mathematical evidence. The report corrects their quantifier error and stops at an honest scoped conclusion. No further general attempt, novelty claim, or current literature consensus is inferred from bounded searching.

The author's prior repository-search and public-problem-page access history is retained as author-stage provenance. Those repository queries and that page-access attempt were not independently repeated here. No novelty or completeness claim depends on them.

## Executable review and replay

All executable input code was read before execution. The independent harness pins the exact external archive, bootstrap, manifest, and author receipt before extracting or running anything. It verifies the four-member ZIP inventory and each member's hash and size. All archive members are regular, unencrypted, top-level files. The author gate checks canonical absolute roots, exact root inventory, non-symlink regular members, external manifest entrypoint, archive agreement, and isolated startup before executing the already-verified entrypoint bytes.

All **45 independent replay cases passed**. Clean execution, relocation, and hostile current-directory/environment cases passed under both normal and optimized Python. Added or missing entries, caches, import shadows, report/status/metadata/entrypoint tampering, member and root symlinks, wrong or relative roots, manifest confusion, archive tampering, and external-input symlinks were rejected under both modes. Omitting each required isolation/startup flag was also rejected. The shadow-execution marker remained absent.

The gate is a bounded byte-integrity and metadata check, not a mathematical proof checker. Its trust boundary includes the externally pinned bootstrap and manifest, the Python interpreter and standard library, and a quiescent filesystem during checking. The author validator rereads two verified metadata files after the gate; this audit does not certify resistance to an actively racing filesystem writer. Direct execution of `validate.py` bypasses the inventory gate and is not an accepted verification procedure.

To replay from the unpacked audit directory, invoke `python -I -S -B replay_author.py` with the canonical absolute path to that directory. Corpus replay separately takes the three authorized local corpus paths as arguments to `verify_corpus_bindings.py`. Neither command needs to publish those inputs. The external independent bootstrap validates the complete audit package before running its metadata validator; it likewise does not prove the mathematics.

## Sources

[C] Danny Calegari, *Problems in foliations and laminations of 3-manifolds*, Definitions 1.1–1.2 and Question 8.3 with remarks. https://arxiv.org/abs/math/0209081v1

[Z1] Bojun Zhao, *Left orderability and taut foliations with one-sided branching*, Theorem 1.1. https://arxiv.org/abs/2209.04752v2

[Z2] Bojun Zhao, *Left-orderability in Dehn fillings of pseudo-Anosov mapping tori*, Question 2, Conventions 1.1–1.2, Theorems 1.3–1.4. https://arxiv.org/abs/2604.04629v2

[A] Ian Agol, *The virtual Haken conjecture*, Theorem 9.2. https://arxiv.org/abs/1204.2810

[B] Mark Brittenham, *Tautly foliated 3-manifolds with no R-covered foliations*, introduction and Question 6. https://arxiv.org/abs/math/0011130

[R] Rachel Roberts, *Foliated hyperbolic 3-manifolds containing no R-covered foliation*, *Knots in Vancouver* abstract, July 19–23, 2004, page 5. https://media.pims.math.ca/pdf/science/2004/KT3Mwksp/knotabs.pdf

[S] John Shareshian, joint work with Rachel Roberts and Melanie Stein, *Hyperbolic 3-manifolds with no Reebless foliation*, Oberwolfach report 16/2003, page 14. https://publications.mfo.de/bitstream/handle/mfo/2763/Report_03_16.pdf?isAllowed=y&sequence=1
