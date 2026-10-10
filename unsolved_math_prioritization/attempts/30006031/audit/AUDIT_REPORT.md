# Independent audit: operadic homotopy centers

Problem 30006031; OWR-14298590-001; catalog rank 792. Audited 2026-10-05.

## Verdict

**ACCEPT the five scoped arguments and the UNRESOLVED disposition, with one packaging-verifier correction.** This is an independent adversarial AI-assisted audit, not human peer review or formal proof verification. It does not turn the packet into a solution or a counterexample to the target.

The author ZIP has 25,495 bytes and SHA-256 `80e41bf9af68cbd1197495c188ba3ea956b541238ea33ab0ea4cbadfeabecb60`. Its manifest SHA-256 is `64feb895b04279f97b88a9f624d5d75d9937b14d3b10981badf790e5dc2bb619`. The `author/` directory reproduces all ten frozen public files without modification. The original ZIP and author manifest remain unchanged.

The actual author archive contains no source PDFs, extracts, images, dataset records or private coordination material. The original verifier does have an exact-file-set blind spot: it accepts an additional dangling symlink. The separate `verify_audit.py` guard rejects every symlink and special entry, including that regression. Read `CORRECTIONS.md` before relying on the original packaging claims.

## 1. Target and definition gate

The exact contribution in [OWR 39/2024](https://ems.press/content/serial-article-files/50048), printed pp. 2255-2256, announces the center definition and a proposed little-three-disks action but does not print the construction or its model hypotheses. The source does not license replacing the intended derived center by the strict unary center or a convenient Hochschild object. The audit independently downloaded the primary PDF and confirmed its byte identity. The [publisher record](https://ems.press/journals/owr/articles/14298590) dates publication to 14 February 2025 while retaining volume/report year 2024; these are compatible dates.

Therefore the packet's distinction among unary operadic units, nullary operations, and a multiplicative map from Ass is essential. Likewise, an E3 algebra need not have group-like components. These distinctions are preserved in all five approaches. No target-specific action, comparison theorem, general counterexample, or exhaustive literature-status certificate has been established.

## 2. Strict unary center and all-arity coherence

Proposition 1 is correct for the specified set-valued nonsymmetric operad. For central unary x and y, substitution associativity rewrites (xy)p as p(xy,...,xy). At arity zero both sides are p. Applying x's centrality equation to the unary operation y gives xy=yx; the unary operadic identity is central.

The resulting Com action is genuinely all-arity: its operation on k inputs is their monoid product, including the empty product. Flattening a tree of products proves substitution compatibility, the empty product gives the nullary operation, the singleton product gives the unary identity, and commutativity gives every symmetric-group axiom. Precomposing with the terminal map D_n -> Com supplies a continuous symmetric D_n action; no hidden symmetric structure on P was assumed. Discreteness makes continuity automatic.

For U(M), only unary arity is nonempty, so its strict center is the monoid center and a map Ass -> U(M) cannot exist. For End(X), constants are nullaries and force z(x)=x for every x. These controls do not identify a homotopy equalizer, derived center, or higher coherent center.

## 3. Conditional triple delooping

The conditional construction on based maps I^3/boundary I^3 -> Y is valid: affine insertion in disjoint cubes, with the basepoint elsewhere, is compatible with substitution, coordinate relabeling, the full unit cube and the empty configuration. Boundaries match because the input maps are based there. In compactly generated mapping spaces this is the usual continuous little-cubes action. Transport across an equivalence in the infinity-category of spaces asserts existence of the algebra structure on that homotopy type; it does not promise a literal point-set action on an arbitrary representative.

The extra group-like restriction is correctly conditional on a specified product. pi_0(Omega^3 Y) is the abelian group pi_3(Y), so a multiplication-preserving equivalence with a space whose component monoid is (N,+) is impossible. This does not obstruct E3 structures on nongroup-like spaces: discrete N already has a Com action.

The audit checked Definition 5.13 and Corollary 5.22 of [Triple delooping for multiplicative hyperoperads, v1](https://arxiv.org/pdf/2309.15055v1). Contractibility on the free edge and every corolla and coherent trunk-insertion retractions are real hypotheses. No application to all target centers has been supplied. The [published article record](https://link.springer.com/article/10.1007/s10485-025-09832-0) confirms the 2025 publication; the subscription-preview page does not verify the final proof or its numbering.

## 4. Binary topology, indexing, and the failed fiber

Proposition 3 gives the correct integral statement. The order complex with two incomparable vertices at each of q totally ordered levels is the join of q copies of S^0. Its simplices are exactly the proper faces of the q-dimensional cross-polytope, so its realization is S^(q-1). This is a geometric proof over Z; finite-field ranks alone would not exclude torsion.

The square cycle and its cone have the stated signs. The extra cone vertex in the third level fills the nonzero two-level 1-cycle. An independent ternary-coordinate implementation checks face counts, integral boundary identities and F2 Betti numbers through seven levels.

Fresh PDF rendering and pixel inspection independently confirm that [Condensation of the operad for multiplicative hyperoperads, v1](https://arxiv.org/pdf/2507.10192v1), page 4, allows labels 0 through m, while page 8 calls B(K_2) an E2 operad. Literally, the first convention gives three binary levels for K_2 and hence S^2, incompatible with D_2(2) having type S^1. This is an internal printed-indexing discrepancy, not an OCR claim. Normalizing the number of levels does not produce an E3 theorem.

For binary circled-tree operations of complexity at most zero, horizontal separation is required. A linear tree has only one branch, so the relevant category is empty. Its nerve is not contractible. This invalidates the proposed fiberwise argument at that specific hypothesis. Neither emptiness of this fiber nor the printed indexing defect determines the whole condensation's homotopy type or forbids other constructions. The paper announces an E2 result, which the packet correctly keeps distinct from the target E3 claim.

## 5. Free E2 algebra: genuine obstruction, correct scope

Proposition 4 is correct. For X={a,b}, the mixed-label weight-two component of the free unital D_2 algebra is D_2(2), not the unordered quotient. Distinct labels have trivial stabilizer under Sigma_2. Sorting the labels to (a,b) gives the claimed homeomorphism; evaluation at the two unary generators is precisely that map. This component is open and closed, so its H_1 injects into the homology of the coproduct.

For fixed distinct centers c_1,c_2 in the open unit n-ball, admissible radii form a nonempty convex set. For example, giving both disks radius one quarter of min(1-|c_1|,1-|c_2|,|c_1-c_2|) provides a continuous section. Linear interpolation of radii stays admissible. Thus forgetting radii is a homotopy equivalence. Configuration of two ordered centers has type S^(n-1), by a homeomorphism from the open ball to R^n and then midpoint/difference coordinates.

Consequently the mixed binary evaluation has nonzero integral H_1, while any factorization through D_3(2) induces zero H_1. Agreement up to homotopy is already impossible. No full calculation of the free algebra's homology is needed. The two-label choice avoids the stabilizer issue that a one-label example would introduce.

This obstructs extension of the **specified** D_2 action along D_2 -> D_3. It is not a statement that its underlying space admits no unrelated E3 action, and it is not a counterexample to an unidentified homotopy-center construction. [Additivity](https://arxiv.org/pdf/2205.12875v2) cannot supply the missing coherently commuting action: an algebra over the relevant derived tensor product is additional data.

## 6. Naturality and newer sources

Proposition 5 is valid: the nontrivial element of C2 is central, but its image under the transposition subgroup inclusion in S3 fails to commute with another transposition. Therefore the evident map on elements cannot define center covariance for all monoid maps. Surjective monoid homomorphisms preserve centers by lifting target elements; the same all-arity lifting argument works for levelwise-surjective maps of the specified set-valued operads. Isomorphisms induce center isomorphisms. This does not preclude appropriate bimodule or correspondence variance.

The audit independently downloaded and inspected the object/action scope of [the Swiss-cheese preprint](https://arxiv.org/pdf/2512.20167v1), including its introduction, Definition 2.12, Theorem 3.9 and Corollary 3.10. Applying its E3 consequence requires the relevant E2/complete-graph algebra input and its Hochschild object. A nonsymmetric operad's collection and substitutions do not by themselves supply that input or the required comparison to the OWR center. The preprint's universal property remains separately conjectural.

The qualifications in [Batanin-Markl v1](https://arxiv.org/pdf/1109.4084v1), Definitions 43-44 and 47, Remark 48, Theorem 103, Corollary 104 and Theorem 105, support the packet's caution about enrichment and derived hypotheses. The [lattice-path source](https://arxiv.org/pdf/0902.0556v2), Theorems 3.8 and 3.12, concerns the corresponding conditional E_n condensation and E2 Hochschild action. The [polynomial-2-monad preprint](https://arxiv.org/pdf/2605.25222v1), Section 1.5, explicitly assumes certain extensions of model-categorical results and defers their proofs. No missing target comparison was found in the passages inspected. None of these imported theorems has been independently re-proved here.

## 7. Reproduction and provenance

- Frozen-author default output: 900 assertions, byte-identical to its recorded RESULTS.json.
- Frozen-author external-corpus output: 916 assertions, byte-identical to its EXTERNAL_REPLAY.json.
- Frozen-author manifest output: 930 assertions, matching the recorded author replay.
- New independent default suite: 19,322 assertions. It includes seven cross-polytope dimensions, every identity-fixed labeled monoid of size at most four (counts 1,2,11,156), 1,038 surjective maps to monoids of size at most three, Com-action controls, label stabilizers, and strict-manifest regressions.
- New independent suite with author, all three full corpora, and eight scholarly-PDF hash checks: 19,359 assertions.

These numbers count individual checks, not independent theorems or confidence percentages. The homotopy-center target is not an input to the finite suite.

The complete catalog, problems corpus and research corpus were independently hashed. The selected statement, DOI, rank and unique numeric identity match. The audit also recomputed the review hash from the **entire** selected problem record and its research record, using the pinned repository's serializer and absent-record default. It matches `5576c84aff240284caeb8d3ea655c4be9c82ed64d9a7c4737888242b70cb9487`; four mutation controls distinguish changes to nonstatement data, prior research, statement-only hashing and compact serialization. This closes the original packet's explicitly disclosed retained-only review-hash limitation.

All eight scholarly PDFs and the primary mirror were independently downloaded from their public URLs and byte-matched; no source bytes are redistributed.

Read-only GitHub checks independently confirm the pinned dataset manifest, catalog blob and review-hash formula, the complete 63-entry attempts tree with no target directory, no exact-ID PR/commit/branch/code result, and the target directory's 404 at the pinned commit. A combined exact-ID/alias/title PR search also returned no result. These are bounded observations, not proof that no unpublished or unindexed attempt exists. Current web searches did not locate a target resolution; no exhaustive priority or openness claim is made.

## 8. Acceptance boundary

All five author propositions are accepted **in their stated scope**. The general E3 center question remains unresolved after five approach families. The exact definition, universal hypotheses, operadic action/coherences and model comparisons remain missing. The safe delivery consists only of the unchanged authored packet, this audit, the explicit packaging correction, independent code/results, public verification metadata and the audit manifest.
