# PR36 algebraic/descent family audit

**Assessment: the original mathematical counterexample is supported.** No central algebraicity, field-of-moduli or real-descent gap was found in the original degree-11 construction. This is independent verification of original turn 1 and adds **zero substantive research turns**. The conclusion answers the literal universal PCF question negatively; it does not establish historical novelty, a minimal degree, explicit coefficients, or the exact number field.

## Scope, independence and exact provenance

Audit head `35be7fe58a2832c4d7012cf69c973810fb4c42f8`, base `01358d66fc67d1c462bddf31c0d4ee5b120e6737`. All original16 file bytes equal the actual head Git blobs. The complete original17-path patch equals the actual base/head Git diff byte for byte, SHA-256 `cba891492c4ddb4b232f953b5753c2d48d289ca52450c048a4c00840c26e55ec`. The numeric attempt contributes 16 files; the seventeenth path is its QUEUE row changing queued0/5 to claimed_solved1/5. No shared queue, state, history, branch or remote was modified. Main remained the current branch.

The exact question is “Are all PCF maps defined over their field of moduli?” The imported odd-divisor condition is prior partial work and cannot be substituted as the target. A single algebraic PCF counterexample with even postcritical cardinality suffices to falsify the literal universal statement.

The literal target was sealed before reading CANDIDATE. The independently reconstructed universal proof was sealed at 2026-10-02T06:17:02.607357+00:00 before historical REVIEW/code/results or any parent/sibling mathematical proof/verdict. **Exposure limitation:** the initial full source_record read also displayed its embedded upstream_prior_report before the literal seal. Thus independence from that imported parity discussion is limited and is explicitly disclosed; there was no old candidate/reviewer verdict exposure before the universal proof seal. The audit does not falsely certify perfect source independence.

See `independent_universal_proof.md` for the full reconstructed argument and `READING_LEDGER.json` for exact reading order, source scope and original16 inventory.

## Main algebraic deductions and attacks

| Attack | Verified mechanism | Exact boundary |
|---|---|---|
| Graph-defined complex class might have transcendental coefficients | Fixed edge count gives finitely many graph classes; normalizing an ordered critical triple removes continuous Mobius freedom; finite constructible Q-locus forces algebraic coefficient coordinates | Only critically fixed fixed-degree classes are finite; arbitrary PCF/flexible-Lattes finiteness is not asserted |
| Critical-fixed equations might ignore multiplicities/infinity/degree | Homogeneous W=F_XG_Y-F_YG_X has degree20, H=YF-XG has degree12; support(W)subset support(H) iff W divides H^20 on nonzero-resultant char0 locus | Quotient degree220 with221 coefficients; 241 coefficient equations. Resultant nonvanishing and projective coefficient charts are essential |
| Elimination may only describe closure | Incidence polynomial equations and resultant inequation project to a constructible Q-locus; finite Galois-stable coordinate orbits imply algebraicity | No claim that an arbitrary elimination ideal alone equals the desired locus |
| Conjugacy over C might fail over Qbar | A conjugator sends three distinct algebraic critical points to three algebraic critical points; its unique Mobius coefficients are algebraic | Critical set has ten distinct points; this elementary proof applies directly |
| Arithmetic stabilizer may not yield a number field | It is a subgroup containing the open coefficient-field Galois subgroup, hence open and closed; fixed field is finite | Complex conjugation in the stabilizer puts K in the chosen real embedding, not necessarily all embeddings |
| Anti-involution might be mistaken for a reflection | Aut(f)=1 forces unique A and A^2=1; paired actual Tischler faces yield an actual connected A-invariant charge graph disjoint from fixed points; reflecting circle would disconnect it | Actual arcs, not solely an isotopy class, are necessary |
| Field of moduli could be conflated with field of definition | K is real in chosen embedding; a K-model would be an R-model; an R-model gives a reflecting antiholomorphic automorphism, already excluded | No explicit K or quaternion computation is necessary |
| Projective cocycle might be treated as linear/trivial | A^2=id gives a PGL2 cocycle, allowing the antipodal nonsplit conic; Hilbert90 does not trivialize PGL2 cohomology | No GL2 lift is assumed; nontrivial-aut gerbe difficulties do not arise since Aut(f)=1 |
| Odd-divisor result might contradict example | Reduced postcritical degree10, ramification degree20, fixed-point degree12 are all even | Imported parity criterion remains partial positive progress and is not the target assumption |

The symmetry part depends on [Hlushchanka's operative realization and inverse construction](https://arxiv.org/pdf/1904.04759v2), not on arbitrary correspondence equivariance. Immediate-basin (anti-)rotations carry all actual fixed internal rays and their faces to the corresponding rays/faces. Face incidence determines charge cyclic order, which makes the necessary symmetry action well defined. The later [Hlushchanka--Prochorov Section3.3](https://arxiv.org/pdf/2212.14759) explicitly corroborates charge-graph isotopy uniqueness. The needed real-model implication is the elementary proof in [Hidalgo--Quispe Lemma4](https://arxiv.org/pdf/1502.05306). The conic and known descent cases are consistent with [Silverman Theorem2.1/Corollary2.2/Theorem5.1](https://www.numdam.org/item/CM_1995__98_3_269_0/).

## Historical comparison and source limits

The frozen CANDIDATE algebraic steps match the independent reconstruction. Historical REVIEW Section6 already explicitly states the algebraic-conjugator lemma that is implicit in CANDIDATE Section9, so no repair route is required. Historical README/status/PR body claim full negative resolution while preserving absent coefficients/exact K, unestablished novelty and source-access limits. CANDIDATE's awaiting-review banner is a preserved historical freeze; the later review status is explicit elsewhere. The turn ledger records one original candidate turn, consistent with 1/5 metadata. Metadata references the historical author branch; this audit stayed on main.

Four recovered source PDFs match all four corresponding historical source-manifest hashes exactly: Silverman, Hlushchanka, Bresciani withdrawnv1, Bonifant--Buff--Milnor. The historical AIM workshop HTML hash could not be replayed because direct retrieval returned403, although the complete official workshop text was accessible through web and confirms rational-map/PGL2 context. The literal AIM problem page remains unavailable (timeout/certificate mismatch/403); the pinned source_record is the exact-statement evidence. These limitations were already disclosed in the original package and remain disclosed here.

[Bresciani's withdrawal notice](https://arxiv.org/abs/2405.03612) directly confirms the main-proof error about equal ramification degrees versus equal orders of vanishing. The candidate excludes that theorem. The [Bonifant--Buff--Milnor antipodal cubic paper](https://arxiv.org/pdf/1512.01850), Lemma2.3, has critically finite hyperbolic centers, so broad novelty/minimal-degree claims would require further prior-art work. This audit does not reopen discovery or certify historical novelty.

## Executable verification and preserved failures

Private unchanged copies of the original author and independent checker reproduce both historical JSON receipts **byte for byte** under normal Python. The original author exhausts1152 compatible permutations; the independent checker reports183 assertions. These programs verify finite graph data, not rational realization or descent.

`exact_algebra_controls.py` is a new standard-library exact equation checker. Its12 checks use a normalized degree-11 critically fixed Newton conjugate only as a positive control for the equations. It also checks a non-fixed critical point, infinity multiplicity, insufficient exponent and a degree-one translation padded to apparent degree11 by a degree10 common factor. The padded pair passes critical normalization/divisibility but has resultant0, showing why the original stated resultant guard is necessary. This is supplemental falsification of bookkeeping, not a new repair/construction of the candidate's coefficients.

| Actual executable variant | Result |
|---|---|
| Author graph changed to all pendants inside | Normal execution rejected |
| Reviewer one pendant coordinate changed | Rejected at exact derived rotation check |
| Reviewer antipodal matrix changed to reflection matrix | Rejected at projective matrix-sign check |
| Algebraic resultant guard removed | Rejected by spurious-base-point negative control |
| Algebraic exponent20 changed to1 | Rejected by genuine critically fixed positive control |
| Author only printed degree changed11to12 | Program prints pass=true; bytewise receipt comparison detects corruption |
| Corrupt author all-inside program run with Python -O | Assertions disabled; prints pass=true; receipt differs and is detected |

All variant source files, one-edit diffs, stdout, stderr and failure details are retained. The -O case is a real limitation of historical assert-based diagnostics: optimized Python must not be used to claim those checks ran. It is not a mathematical counterexample to the written proof, and original reproduction instructions use normal Python. The printed pass flag alone cannot certify arbitrary edited code/output; the exact Git/input/receipt binding supplies that boundary. No failure was discarded and no mutation was substituted for the historical originals.

Reproduce the read-only binding, private unchanged replays, and retained variants with:

    python3 replay_and_bind.py

## Completion and delivery boundary

Algebra/descent family audit completion:100%. Strongest verified result is the original graph-defined algebraic degree-11 PCF class with real embedded field of moduli and no model over that field. No unresolved central algebra/descent gap remains in the examined argument. Live literal-page provenance, historical novelty, exact coefficients/K, minimal degree and formal proof certification remain outside what is verified. No new preprint, acceptance claim, release or DOI is authorized or created. No individuals were contacted. Foreign source downloads are only in ignored `tmp/`.

`authored_manifest.json` strictly covers every deliverable file in this family except itself and ignored scratch/cache directories, with copied original inputs labeled as such. The proof/literal seals preserve the exact earlier exposure statements and were not rewritten after historical comparison.
