# Fresh adversarial review of corrected PR301 / problem30004365

## Verdict

**MATHEMATICAL PASS for v02, within the stated theoretical-algorithm scope.** No unresolved central mathematical gap or counterexample was found after independent derivation, targeted falsification, complete relevant primary-source inspection, and later comparison with the three earlier families. This is an audit conclusion, not priority, publication, peer-review, practical-runtime, or full-software certification.

The exact accepted audit target is `CURRENT_CORRECTED_PROOF_v02.md`, 15,956 bytes, SHA256 `d92a870709f5ce62440fa8a83313dd13790773f247e01cfb63c43c5ae8ea272a`. The unchanged v01 is 15,693 bytes, SHA256 `38f1a7d3893399c9e8821d445e4450c62b569dcb9fba8b8d2d46eac7fec60857`. The immutable submitted `TURN_1.md` has SHA256 `61130af734e4d1ad68d292b29546f562858fa6aafc6eb92f2e7d2e3d3c1c0a3a` at submitted head `125d90fa3f5a4f90b813fec7a7c0f1918914d885`. `INPUT_PINS.json` records all exact source pins.

## Mandatory repairs versus optional precision

**Mandatory, now resolved by v02:** define S0 by truncating original-boundary collars as well as punctures. APS §2 uses open surfaces with original boundary circles absent, so v01's literal closed puncture-only-truncated S0 did not lie inside the canonical line-field domain. An inward core embedding was compatible with the intended argument but had to be explicit before promoting the exact text. I read v02 in full and verified the sole diff supplies that repair. Core restriction, LP application, and collar extension are now well-defined, with end types and alternating marks retained as labels.

**Mandatory relative to the original submission, already resolved in both corrected versions:** replace standalone reliance on the literal puncture-deficient APS7.4 sufficient direction by full-end LP1.2.4 on the compact core, then APS6.1/7.2. A(3,5)/A(4,4) proves the literal printed truncation fails. The submitted numerical key already retained all puncture records; this is a proof/source correction, not a changed numerical criterion.

**Optional clarity:** when the core has been truncated, explain that the unique white occurrence used by the disk-side predicate is its retained pretruncation disk/end-collar label. The curves avoid those collars, so inward truncation cannot change which side contains it. It is also useful to state that a pure mapping-class representative may be chosen equal to the identity near the core boundaries before its cylinder extension. Neither is a remaining mathematical blocker for v02.

The corrected maximal-portion wording, canonical seam order, zero-category extension, explicit green=white convention, projective-detection factor argument, and honest finite-control limitations address the other earlier ambiguities.

## Strongest result and exact remaining gap

For every promised finite-dimensional gentle quadratic monomial bound quiver over the fixed field, the stated construction and exhaustive finite-predicate search compute a complete numerical bounded-derived-equivalence key and finite rational geometric handle certificates with exact canonical windings. Every individual stage is finite and decidable; the only unbounded searches have a guaranteed finite witness. Surface classification is used to prove handle existence, and LP classifies line-field orbits; neither is an unspecified effective surface/genus/homeomorphism oracle. Connected factors and the empty/isolated cases are covered.

No central mathematical gap remains in this v02 proof under the credited primary theorems. ROOT must still authenticate and replay this audit's evidence before relying on its conclusion. Historical priority remains entirely unassessed. A full curve enumerator, complement checker implementation, practical timings, independent peer review and preprint preparation remain absent and are explicitly outside this mathematical verdict.

## Independent mechanism and adversarial findings

`INDEPENDENT_OBLIGATIONS.md` and the complete `DERIVATIONS.md` were preserved before consulting any family report, with a timestamped hash checkpoint in `INDEPENDENT_CHECKPOINT.json`. The later family consultation is visible in the recorded commands and agrees with the independently obtained deductions. Initial derivation/control source versions are also preserved as `*.independent_checkpoint.gz`.

The fresh control program imports no submitted or family verifier. It constructs and tests lozenge edge/corner links, boundary cycles, occurrence-based fan triangulation and genuine flag subdivision. It independently supplies six named edge fixtures, including finite genus-one and genus-two inputs, and six bridge-cycle witnesses. It checks rational seam reversal, exact intersection signs, maximal-crosscut versus elementary-edge interpretations, once-crossing side occurrences, genus-one winding ideals, all 32 mod2 quadratic forms with one radical dimension, all 16 handle/radical lifts, both Arf values, and paired-record marginal traps.

The final authoritative run `captures/final_control_coverage` exits 0 with **46,068 actual mathematical check assertions** and **0 orbit-edge evaluations**. The controls are finite supplements to the proof; they are not a full implemented search or an experimental proof of universal halting.

Meaningful adversarial controls include:

| Attack | Exact outcome | Implication |
|---|---|---|
| Selfrelation quotient wrongly treated as a simplicial complex by vertex triples | Square-zero-loop fan has 2 duplicate vertex triples; occurrence-based flags give 144 genuine triangles | Preserve edge/face incidences; corrected triangulation survives |
| Ignore reversed seam order | Exact t=2/5 differs from 1-t | Shared canonical order is needed and supplied |
| Apply disk-separation test to every chart edge | A 3-edge proper crosscut has 2 interior intermediate nodes | Corrected maximal portions are essential |
| Merge two cut endpoints of one physical crossing | Their seam parameters coincide but left/right occurrence labels differ | Occurrence-preserving cutting is essential and supplied |
| Retain Arf on nonzero radical | q=x1*y1+x2*y2+z changes handle Arf under radical lifts; 120 changing finite examples | Corrected radical branch must omit Arf |
| Lose both Arf branches | For radical-zero g=2 forms, counts are 10 Arf0 and 6 Arf1 | Both bit values occur and are checked |
| Treat End(P_v) as necessarily k | Square-zero loop has a larger local endomorphism ring | Locality, used by the corrected factor proof, is enough |
| Drop puncture winds | A(3,5)/A(4,4) agree on outer data and differ at punctures | All-end sufficiency is necessary |

The End(P_v)=k overstatement occurred only in an intermediate paragraph of my own derivation and was corrected to the proper local-ring proof; its original bytes are preserved. It was not a defect in the candidate, which already uses indecomposable projectives. A stale fixture comment identified by ROOT was also corrected. The first control attempt failed only during JSON serialization of a Fraction after its checks; its source, actual PID and full traceback remain archived, and it is not a PASS run. The initial missing source-text path and a failed patch match are recorded transparently in the research log/chat; the missing-path failure is additionally reproduced with native captured PID/streams.

## Named source-range witness

Both A(3,5) and A(4,4) have 8 vertices, 9 arrows, permitted-path counts [8,9,2,1], dimension 20, g=0,b=1,p=2, 7 white boundary marks, and outer winding 6. Independent corner-cycle valences give puncture windings {-3,-5} and {-4,-4}; APS Euler identity then gives outer 6. Their paired keys and AG records differ:

| Algebra | Paired peripheral records (n,w) | AG records |
|---|---|---|
| A(3,5) | (7,6),(0,-3),(0,-5) | (7,1),(0,3),(0,5) |
| A(4,4) | (7,6),(0,-4),(0,-4) | (7,1),(0,4),(0,4) |

The split follows independently from APS6.1 preservation of all peripheral curves or APS6.2's AG interpretation. The original workshop Problem3.4 asks for the numerical algorithm without a complexity/software requirement; its total boundary mark count is twice the corrected white count. The stronger complete key includes peripheral information omitted from its abbreviated theorem summary.

## Primary-source inspection and custody

Read the full original Plamondon contribution printed pp161–164; PPP Definitions2.1/2.2 and §§4.1–4.2 through inverse construction; APS conventions, line-field/winding definitions, dual disks, signed-sum lemma, Theorem4.3, complete Theorem6.1 proof, Remarks6.2/7.2, Theorems7.3/7.4 and classification proof; and complete LP§1 including all definitions, Theorem1.2.4 proof and Corollary1.2.6. LP pp5–10, PPP pp10–11, APS pp6/12/13/19/23/24/25, and OWR printed p163 formulas were visually inspected. All relevant theorem hypotheses, end ranges and orientation signs were checked from the primary bodies, not abstracts.

| Primary PDF | SHA256 |
|---|---|
| PPP | 49026e4606c41d8729cfaad4395bb1ade989140aa44df99eedee6c9177b721ea |
| APS final | 42a3956f82fa7098dd37941c2d1bc5a767ad2a46afd6b3bb2b069c10db0c56f1 |
| OWR | b1be25a647257979a03e04e59a4c558b3d61e9dc6c9597de010eb9721ef66a6d |
| LP | d99c651200fc125ca2ad28ec4714b1efa8bf4145a86554991b04d656455215fb |

The first three match immutable SOURCE_HASHES; LP is the separately pinned supplementary primary source. No dependency installation occurred. For canonical reads/computations `record_run.py` archives exact argv/source, request, actual child PID, UTC start/end, exit, full compressed stdout/stderr and hashes. Initial lightweight tool reads had no exposed child PID and are not falsely assigned one. `CUSTODY_VALIDATION.json` checks the canonical archive. `ARTIFACT_MANIFEST.json` binds this packet. All work stays below the 15MiB evidence cap excluding primary PDFs.

All writes were confined to `corrected_math_adversary_02`. No Git/index/branch/shared-control/service/publication/PR-comment or external-individual communication action occurred. Internal agent messages were limited to reporting audit findings to ROOT.
