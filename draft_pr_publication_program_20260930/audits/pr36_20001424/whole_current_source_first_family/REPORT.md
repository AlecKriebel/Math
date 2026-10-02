# NEW whole-current source-first adversarial report: PR36 / 20001424

**Verdict: PASS_WITH_EXPLICIT_LIMITS for the exact frozen packet below.** No proof-breaking error or mandatory correction to this packet was found. The universal question has a complete negative answer by an elementary verification of Silverman's printed 1995 cubic. Its classification as `PRIOR_APPLICATION / already_solved` is supported. The degree-11 graph construction remains mathematically supported as an existence argument under the established graph realization/classification theorems. This verdict is newly reconstructed and tested; no earlier clean verdict was transferred.

This audit closes my assigned adversarial review, adding zero substantive attempts. It does not perform publication, merge, canonical writes, a live queue update, a release, a paper, a DOI or a tracker update. Root must independently reproduce/check the sealed audit and perform the integration guard described below.

## 1. Exact reviewed inputs and preserved independence

Repository-relative packet: `draft_pr_publication_program_20260930/audits/pr36_20001424/reviewed_candidate/`.

| Frozen file | SHA256 |
|---|---|
| `MANIFEST.json` | `75d103fcfe2bce2322ff091fea73d0f03c7875b00c7c7af8f6e20ff741a2975c` |
| `CURRENT_PROOF_DEPENDENCIES.json` | `f6b0af0f11ee8aae60678cc37e7cb24373d99484918f893e1a94e9e703d43261` |
| `CURRENT_BUILD_RECEIPT.json` | `1c7b8ba0bd02d3c6945dde278fc4c0216140c8175acad577028536b462dd3ea5` |

All 60 packet members and all 480 dependencies passed fresh size/hash checks. Packet inventory is strict, with no missing or unlisted file. The dependency anchor is the exact repository-relative audit directory specified in `CURRENT_PROOF_DEPENDENCIES.json:3–4`; it does not change when the packet is copied to canonical attempts. The five first-party family closures bind 364 members; root retention binds 72 first-party members. Duplicate locations reduce to 257 unique content groups. Every unique JSON/JSONL parsed, every Python AST parsed, both SVGs parsed, and complete content inspection records were retained. Operative mathematical/admin files, historical reports and operative programs were read directly. AST/content inspection of other helpers is not presented as human line-by-line reading of every duplicate.

I read the repository instructions and **complete** `pinned_problem.json` before any candidate, historical review or prior report. The mandatory full JSON read unavoidably exposed its embedded research summary; this is disclosed, not hidden independence. I did not read `source_record.json`, whose nested prior report would have introduced an interpretation. The live official AIM HTML and embedded data were then read, with successful bytes pinned and failed web/HTTPS retrievals preserved. The exact official problem is the unrestricted ASCII question, “Are all PCF maps defined over their field of moduli?”, problem 2.6, revision `10-a40d7e595b8901daa191482b29f094cc`. No parity, automorphism, critically-fixed, polynomial or graph restriction occurs in its question field.

`literal_scope_seal.json` was sealed at 2026-10-02T07:30:14.918040+00:00 before dependent candidate review. Explicit pins were then received. I independently reconstructed the current cubic and graph mechanisms from operative current proofs and fresh primary sources; `independent_reconstruction_seal.md` was sealed at 2026-10-02T07:43:43.348443+00:00 before historical original review, `prior_report.json`, older family reports or root receipt/priority interpretation. Current operative proofs themselves imported earlier family reconstruction text, which is disclosed exposure. Only after my sealed mathematical assessment were historical interpretation and bookkeeping consulted. `READING_LEDGER.json` records actual source versions, reading scopes and limits.

## 2. Independently verified decisive mathematics and source consequence

For the cubic

`f(z) = i((z-1)/(z+1))^3`,

numerator and denominator are coprime and the degree is 3. The only critical points are ±1, each local degree 3; infinity is unramified. Projective evaluation gives the exact cycle

`1 → 0 → -i → -1 → infinity → i → 1`.

Consequently the reduced postcritical set has six points and `f` is PCF. Put `T(z)=-1/z`. Direct composition gives `T f T^-1 = conjugate(f)`. Since the coefficients lie in Q(i), the absolute arithmetic conjugacy stabilizer contains every automorphism of Qbar/Q; its fixed field is exactly Q.

A holomorphic centralizer must preserve or swap the critical pair {1,-1} and its value pair {0,infinity}. Preserving both critical points gives the identity. Swapping gives only T; T fails to commute, as evaluation at infinity shows `T f(infinity)=i` and `f T(infinity)=-i`. Thus the holomorphic centralizer is trivial. The antiholomorphic map `A(z)=-1/conjugate(z)` commutes, squares to the identity, and has no fixed points. Any other antiholomorphic centralizer differs from A by a holomorphic centralizer and is therefore A. A real representative would supply a commuting conjugate of ordinary complex conjugation, a reflection with a fixed circle. That cannot be A. There is no real model and hence no Q model.

This single exact Qbar rational-map class falsifies the literal universal assertion in the conventional P1 setting. It also falsifies any broader interpretation that includes these maps; no affirmative higher-dimensional statement is asserted. The odd-degree extension for every d≥3 is correct: d≡3 mod4 gives one six-cycle; d≡1 mod4 gives two three-cycles. Degree one and even degrees are excluded by the actual hypotheses and falsification controls.

I freshly retrieved the official Numdam PDF and visually inspected printed pages 271,296,297. The exact cubic and odd-degree formula, field of moduli Q and absence of real fields of definition are printed in Silverman's 1995 article. The source does not explicitly apply the adjective PCF to this family. The orbit deduction supplies that adjective, but does not turn a printed algebraic example with a printed descent obstruction into a new PR36 universal discovery. Hidalgo–Quispe v4 independently reproduces the odd-degree family. `CURRENT_UNIVERSAL_CERTIFICATE.md:9,23–35,41`, `CURRENT_SOURCE_SCOPE_CERTIFICATE.md:11–18`, `CURRENT_PRIORITY_DECISION.md` and `CURRENT_PRIOR_APPLICATION.md:133–137` correctly distinguish this deduction from an earliest historical recognition claim.

**Exact priority limit:** earliest worldwide recognition of the PCF consequence is unverified, as is narrower priority/minimality of the degree-11 decorated graph. This audit does not establish either. The current text preserves that limit and makes no new discovery claim.

## 3. Independent graph/algebraic argument

The graph has one four-cycle and attached path lengths 1,2,1,2, with the written rotation orders `[3,1,4]`, `[0,2,5]`, `[1,7,3]`, `[2,8,0]`. Its abstract automorphisms are identity, opposite translation and two reflections. Their local orientation signs are respectively `++++`, `----`, `-+-+`, `+-+-`. Hence only identity preserves the embedded rotation system, and only the fixed-vertex/fixed-edge-free opposite translation reverses it. Ten edges give degree 11; valence-plus-one critical local degrees are four 2s, two 3s and four 4s, with ramification sum 20. All ten critical points are fixed. A polynomial conjugate would require a critical local degree 11, which is absent.

The classification alone is not treated as an equivariant set-theoretic bijection. The operative proof uses intrinsic fixed internal rays, their union, Tischler faces, critical corner incidences and cyclic orders. Commuting holomorphic/antiholomorphic maps preserve this data. Face arcs are isotopic relative to the boundary/corner data. The reversing action yields an antiholomorphic centralizer A; trivial holomorphic centralizer forces uniqueness and A²=id. Actual faces pair under A. Choose one arc in a representative of each pair and its A-image in the partner face. This yields an actual connected invariant graph avoiding Fix(A). A reflection would exchange the two disks bounded by its fixed circle, contradicting connectivity of an invariant nonempty graph disjoint from that circle. Thus no real model exists. This checks the critical naturality/invariant-arc step at `CURRENT_GRAPH_DYNAMICS_PROOF.md:17–21` and `CURRENT_GRAPH_ALGEBRAIC_PROOF.md:15–21`.

Algebraicity is not inferred from the arbitrary drawn coordinates. Finite edge count gives finitely many critically-fixed plane graph classes. Normalizing an ordered critical triple to 0,1,infinity gives finitely many rational maps up to coefficient scaling. In degree 11 the ramification form W has degree 20 and the fixed-point form H degree 12. On the resultant-nonzero locus, “all critical points fixed” is equivalent to `W | H^20`, with quotient degree 220. The resulting incidence locus has polynomial Q equations and its coefficient image is constructible over Q. A finite Q-defined constructible complex locus consists of algebraic points. Critical triples then give algebraic conjugators. The arithmetic stabilizer contains an open coefficient-field subgroup, so its fixed field K is a number field. Conjugation stabilizes the class, hence K lies in the selected copy of R; no assertion of total reality is made. A K model would be real, already excluded. The precise argument is at `CURRENT_GRAPH_ALGEBRAIC_PROOF.md:23–46`.

I freshly read the complete operative Hlushchanka v2 inverse/realization proofs, the Cordwell injectivity proof, and Pilgrim–Tan blow-up/intersection/realization proofs. Initial Cordwell versioned retrieval406 and Pilgrim–Tan retrieval failure were preserved before successful retries. The latter PDF had extraction glyph defects, resolved by rendered printed pages28–30. For this simple connected graph the imported marked-graph hypotheses hold with M=id, multiplicity1, X=V and Gprime=G. Thurston characterization/rigidity and standard analytic/algebraic foundations remain established imports; graph code does not prove them. No new degree-11 explicit coefficients, exact field K or minimum-degree theorem is claimed.

## 4. Actual private executions and falsification

The latest retained run is `ACTUAL_REPLAY_20261002T081248401131Z.json`. It contains **27 actual program executions**, private exact source/spec copies, exit codes and actual stdout/stderr hashes, plus an additional actual false-prose execution. Both original verifier receipts reproduce byte for byte. Graph and arithmetic family mathematical structures reproduce in full apart from UTC timestamps; algebra stdout and the independent cubic checker reproduce exactly.

Positive odd degrees3,5,7,11 pass. Even degree, degree one, real-phase guard, wrong critical support, ramification, swap symmetry, orbit and optimized wrong-orbit controls reject. Executable derivative, pole and infinity corruptions reject. Algebra controls reject exponent1 and omitted resultant. A changed graph coordinate rejects. The all-inside rotation mutant rejects under normal execution. Five actual full packet metadata mutants—hidden attempt, wrong id, new deadline, novelty claim, narrowed literal target—fail the corresponding checks. Actual strict60-member missing/extra/corrupted-proof packet copies reject, as do separate toy closure controls.

Three **observed original-checker limits** must remain explicit:

- `verify_graph.py:21–94` and `review/independent_checks.py:15–16` use `assert`; with Python `-O`, the all-inside graph mutant actually exits0. Optimized output is not a valid mathematical check.
- A private change to printed `candidate_degree` at `verify_graph.py:96` actually exits0 and prints12, while its mathematical checks still use11. Output labels alone are not proof.
- A private CANDIDATE degree11→degree12 prose change with unchanged original verifier actually exits0 and returns its original saved bytes. The original script does not load that prose and cannot certify full prose or source/literature scope.

These are scope limits of preserved archival verifiers, not uncorrected false conclusions in the current packet. Current independent proofs and controls address the mathematical claims. Archival original programs are preserved rather than silently repaired. The report does not treat hashes, flags or PASS strings as proof.

An initial private adapter treated the recorded `-O` flag as a script path and failed setup. Both partial rounds, the error receipt and exact pre-fix helper were retained; the corrected helper parses the optional flag. A later revision added actual full60 packet integrity controls; its pre-revision helper is also retained. A final retention correction moved the three earlier full-packet first-party control copies unchanged out of excluded scratch into authored retention, and changed one helper output path so all future first-party control copies are included in the strict authored closure. `CONTROL_RETENTION_FIX.json` preserves the one-line change, exact pre-fix helper and every moved member hash. A fresh27-run replay after this output-path change passed. These are verification setup changes, adding0 research attempts.

## 5. Full preservation, receipts and bookkeeping

`verify_support_relations.py` produced `SUPPORT_RELATION_RESULTS.json`. It parses the complete97,918-byte original diff and verifies all17 path entries; every complete added payload for the16 original archival files equals the frozen archive. Original blobs were rederived using Git blob framing from frozen bytes without calling Git. Current source_record exactly embeds the complete frozen problem and complete upstream prior report. The full prior report was read after the independent mathematical seal, including the partial odd-divisor criterion and its hypotheses. The current full-target counterexample does not rely on treating that criterion as universal.

All28 root actual command records equal the retained command table; all56 actual stdout/stderr hashes were independently rederived. All13 full comparison original/fresh-retained bindings match. Root's three setup failures and three code versions remain bound. Historical arithmetic manifest controls used15 members, while the fresh comparison used18; exactly the two positive input count/hash fields change. Acceptance/rejection outcomes and all other fields match. This is an **actual dated-input comparison**, not identical-input reproduction. The current root qualification is accurate.

The current budget remains original1/5, new substantive0 and audit0. Historical xhigh/model/branch/deadline fields are preserved as historical rather than upgraded retroactively. Current deadline is null. Both current status and readiness withhold novelty, paper/newDOI/tracker/release claims. The current gate remains pending in the frozen reviewed inputs, which accurately records that this new review had not existed when the packet was frozen. The original `claimed_solved` archival state and custom readiness are not promoted into a claim of a native lifecycle acceptance.

The prospective queue patch preserves all12 columns. Only Status, Turns and Findings change; Chat and DOI remain byte-identical, as do all other named-row fields. The old row is queued0/5; the proposed row is already_solved1/5. `pr_body.md:10–26` matches the credited prior application, retained graph argument, budget and no paper/DOI/tracker disposition. No source-first family reports or root receipts are treated as new attempts.

## 6. Mandatory root conditions and exact unverified gaps

There is no mandatory frozen-packet correction. These conditions apply before publication/integration:

1. **Live integration guard** (`CURRENT_QUEUE_PATCH.json:20–36`): whole queue preimage/prospective bytes are not included in this packet. I independently checked the exact named row and unchanged columns, but cannot rederive the whole queue hash from absent bytes. Root must check the live whole-queue preimage or make a separately receipted exact named-row rebase that preserves every other byte. Do not replay the archival diff onto live queue state.
2. **Root reproduction and final state:** independently verify this authored closure and actual helper in a private copy before closing the NEW source-first gate. Match the frozen pins; do not transfer this PASS to changed proof/source/dependency bytes. Administrative acceptance/gate updates and canonical-copy integrity need a final root check. Dependency anchor resolution must remain explicit after canonical copies.
3. **Claim boundaries:** keep the current `already_solved / PRIOR_APPLICATION` attribution, original1/5/new0 accounting, no paper/newDOI/tracker/release scope, standard theorem imports and narrower priority limits. Do not replace them with a worldwide earliest-PCF or novel degree-11 claim.

This adversary did not execute live Git, shared history/inventory, full raw corpus score recomputation or live whole queue replay, as expressly excluded by the assignment. I audited frozen code/evidence, independently bound the actual root receipts and rederived frozen blob hashes. That is not a claim to duplicate root's live operations. The BBM/Milnor/Lodge–Mukherjee appendix is nonoperative attributed historical-family context; its bound reports/evidence were inspected, but I did not independently retrieve and reprove each supplementary paper. The decisive cubic proof and priority result do not import those assertions. No bounded literature audit proves worldwide priority.

## 7. Reproduction and authored closure

`replay_current_packet.py --run` performs the private actual replay and corruption controls using only the pinned packet and exact anchor dependencies. `verify_support_relations.py` independently checks diff/stream/comparison relations. To preserve this sealed audit, root should copy the audit and bound inputs into a private hierarchy retaining the anchor relationships before executing them. The replay helper writes only under its own directory; running it in this finalized live audit would correctly change the authored inventory and require a new seal.

`replay_current_packet.py --verify` checks this strict authored inventory. `--seal` is the explicit closure operation and is not a substitute for replay. `AUTHORED_MANIFEST.json` excludes only itself among authored members, plus ignored foreign scratch `tmp/` and generated `__pycache__/`. It includes reports, both successful and partial actual rounds, setup failure evidence, helper revisions, private first-party source/spec/output copies and all authored inspection receipts. Foreign PDFs/HTML/extractions/renders stay under ignored `tmp/` and are not redistributed. No outside person was contacted; all authored writes stayed inside this assigned audit directory.

Audit completion:100% of the assigned frozen-packet adversarial review. Root publication/integration remains outside this percentage. Substantive-attempt delta:0.
