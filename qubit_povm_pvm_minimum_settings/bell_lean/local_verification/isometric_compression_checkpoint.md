# Isometric-compression helper checkpoint

Timestamp: 2026-09-21T14:23:19.694716+00:00. Assigned helper subgoal: 100% complete and kernel compiled. Overall arbitrary-Hilbert-space bridge remains under integration by the owning agent.

New production file: `Bell/IsometricCompression.lean`; only that production file was edited by this subtask. The actual target build passed with the pinned toolchain (`isometric_compression_build.log`). No sorry, admitted theorem, custom axiom, or changed existing endpoint was introduced.

The construction starts from a general finite rectangular complex matrix V with VᴴV=1. It proves positivity, trace and product preservation under A↦VAVᴴ, positivity/idempotence of K=1−VVᴴ, and annihilation between K and every embedded operator. Adding K to a selected declared outcome preserves total normalization and positivity, and preserves idempotence and pairwise orthogonality for projective measurements. Concrete `povm` and `pvm` constructors return the repository’s actual `Bell.POVM` and `Bell.PVM` types.

For independent local isometries V and W, the Kronecker matrix is an isometry. Joint density embedding constructs the actual repository `Bell.State`. The `born_padded` theorem states exact equality of the target `Bell.born` probability and the source joint trace against the source Kronecker effect. It uses no assumption about real-valued state entries, purity, rank, or additional ancillas.

`canonicalEmbedding hd` supplies the rectangular indicator isometry from Fin d to Fin 2 whenever d≤2. A supplementary audit verifies d=0,1,2 and that the complement vanishes in full dimension. A dimension-zero source still cannot supply a trace-one density matrix; the embedding lemma itself correctly remains valid on the empty carrier. Padding requires a selected label as an explicit local constructor input; callers must derive it from physical normalization rather than add a positive-output premise to the final theorem.

`IsometricCompressionAudit.lean` checked representative constructors and endpoints. All queried dependencies are exactly standard Lean axioms propext, Classical.choice and Quot.sound (`isometric_compression_audit.log`). The broader bridge’s source Hilbert-space basis, operator-coordinate correspondence and end-to-end statement remain outside this helper subgoal and require the owning agent’s integration checks.

## 2026-09-21T14:25:44.985269+00:00 — actual Hilbert isometry

Additional assigned helper subgoal: 100% complete. `Bell/HilbertIsometry.lean` compiled as an actual production module. For any complex inner-product space E, orthonormal basis b indexed by Fin d and proof d≤2, `Bell.Hilbert.linearIsometry b hd` is an actual `E →ₗᵢ[ℂ] EuclideanSpace ℂ (Fin 2)`. Its coordinate application is definitionally the canonical rectangular embedding applied to b.repr. The module proves exact inner-product preservation, norm preservation and injectivity, rather than using the phrase isometry solely for a matrix equation. It imports IsometricCompression and PiL2, independent of the source-coordinate bridge, to avoid a circular definition. The direct type contract and four targeted axiom queries pass in HilbertIsometryAudit.lean; dependencies are only standard Lean axioms.
