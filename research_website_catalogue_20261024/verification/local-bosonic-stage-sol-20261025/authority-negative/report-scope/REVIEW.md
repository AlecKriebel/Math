# Static source and scope intake — Zenodo 23203100

This is a completed source-acquisition and static-scope intake, not a mathematical pass, defect verdict, priority decision, repair, or publication clearance. Independent analytic and adversarial reviews and the root publication decision remain pending. No submitted code was executed, imported, compiled, or rebuilt. No external individual was contacted and no outreach was prepared.

The controlling queue entry is **row 78**, work **Z-23203099**, selected record **23203100**. Row 77 is not this assignment. The frozen queue binding and its SHA-256 are in `sources/record/queue_binding.json`.

## Edition and custody

Title: **Pure-loss bosonic dynamic capacities: EPnI consequences and consumed-key secrecy accounting**. Author: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X). DOI: [10.5281/zenodo.23203100](https://doi.org/10.5281/zenodo.23203100). Fresh API metadata identifies an open CC BY 4.0 preprint.

The exact version field is **Not supplied in Zenodo metadata**. Do not invent “v1” or “1.0” from the concept record's first-version relation. The declared publication date is **2026-10-06**; the record was created **2026-10-07T04:42:47.312983+00:00** and updated **2026-10-10T21:27:36.246172+00:00**. These are separate facts. The PDF's October 6 author date and production timestamp do not establish an earlier public deposit. The September date in the upstream EPnI directory/manuscript is not adopted as a public-priority date.

Fresh unauthenticated HTTPS API requests on 2026-10-25 UTC returned the record and both listed assets with HTTP 200. `sources/record/transport_receipts.json` preserves request URLs, retrieval times, response headers, sizes and hashes. No local candidate substituted for a fresh remote asset.

| Asset | Bytes | MD5 | SHA-256 |
|---|---:|---|---|
| `paper.pdf` | 88,566 | `91b808c56979206207f3246f5c73abfc` | `490c6d4d78eb4c2ae829d06f31df1ed1ace955174acec87279f5d5eb8dee8581` |
| `zenodo-upload-kit.zip` | 114,329 | `02e5c67a66da959846e0c154c23877d4` | `e9f9adb0dca6f7776b215672ab97b7f8922aae415d2d9f73afd631259ca40fab` |

Both match the fresh Zenodo checksums/sizes and the frozen queue. The unchanged PDF has seven searchable pages. All seven were read in extracted text, the entire archived `manuscript/main.tex` was read, and all seven rendered pages were viewed in a contact sheet. Mathematical interpretation uses the TeX as well as the extracted PDF; the contact sheet is a layout/identity check, not a proof check.

Safe extraction checked every archive path, rejected traversal/absolute paths and symlinks, and inventoried all members before source interpretation. There are **40 regular files**, all archived with mode `0644`; there are no directory entries, symlinks, hidden-path members, nested ZIP/tar archives, additional PDFs or alternate manuscripts. The embedded `SOURCE_INVENTORY.json` lists 39 files; all 39 sizes/hashes match the extracted bytes, and the inventory itself is the 40th file. The earlier progress count of 39 members was corrected at checkpoint 2. `all_archive_members.json` and `reader_support_map.json` preserve full member custody, archived/actual modes and read disposition.

## Reading disposition

The support map records 18 source/guide/proof/code/data files read in full as static text, 10 custody/reference metadata files parsed and compared, and 12 earlier internal review/route/priority/status bodies left opaque at filename/hash level. The separate published PDF was also read in full. Reader guides and mathematical proof supplements were used to locate the submitted arguments; their historical favorable-review assertions were not adopted. Opaque prior reports are not substitutes for current review.

Essential mathematical supplements read in full are `notes/capacity_proof/CONDITIONAL_DERIVATION.md`, `ACHIEVABILITY_AND_COST.md`, `PRIVATE_SECURITY_DEFECT_AND_REPAIR.md`, `notes/coding_repair/DIRECT_CODING.md`, and `notes/formal_scope/VACUUM_BRIDGE.md`. The current TeX has an embedded bibliography and no missing included chapter. The external `.bib` is bibliographic support rather than a required input to the printed bibliography.

All five archived Python files were read as text: the package builder, finite OTP/cone checker, symbolic chain-rule checker, exploratory interpolation sampler, and optional Lean-harness generator. They were not run or imported. The two archived result JSON files were read as submitted static data only. Their success flags and sampled values are not reproduced findings. The finite OTP/cone checker and entropy-coefficient checker do not certify the full capacity theorem; the interpolation sampler is explicitly exploratory floating-point evidence; the harness generator does not establish compilation or axiom closure.

## Exact model and claim map

The complete structured map is `CLAIM_MAP.json`. The channel is the one-mode pure-loss channel with independent vacuum environment, **1/2 ≤ η ≤ 1**, complement `L_(1−η)` up to phase, and arbitrary signal entanglement across finitely many uses. The finite photon budget is `Tr(G_n rho_bar_n) ≤ nN`, `G_n = sum_j a_j†a_j`, **0 ≤ N < ∞**, averaged over messages, key and encoder randomness; the quantum source is maximally mixed, equivalently half of a maximally entangled reference pair. There is no peak/per-codeword/occupation energy bound or strong converse claim. Entropies and rates use base two.

Rates are signed forward net resources, generation positive and consumption negative. Gross rates are finite with exponentially finite registers; finite required seeds are charged. Side resources are charged by rate rather than optical energy. There is no free feedback, two-way assistance or superlinear catalyst.

The relevant entropy premise, called VE in the supplements, is

`H(L_t^(tensor n)(rho))/n ≥ g(t g^(-1)(H(rho)/n))`

for every finite `n ≥ 1`, every finite-energy n-mode density operator, and `0 ≤ t ≤ 1`, with `g(u)=(u+1)log2(u+1)−u log2 u`. The other port is an independent n-mode vacuum; no product/Gaussian/full-rank restriction is imposed within the signal. The quantum reduction uses `t=η` and `(1−η)/η`; the private reduction uses the latter. The noiseless η=1 endpoint requires no nontrivial VE input.

| Printed claim | Classification for later review |
|---|---|
| Theorem 1, PDF p2 | Vacuum specialization of the external EPnI theorem; not an independent EPnI proof. |
| Lemma 2, PDF p2 | Elementary scalar convexity/concavity deduction, independent of EPnI. |
| Theorem 3, PDF p3 | Exact C/Q/E closed-union capacity consequence relying on VE, regularized quantum coding, the common λ argument and mean-cost approximation/closure. Gaussian inner coding does not itself require EPnI. |
| Proposition 4, PDF pp3–4 | Literal-model zero-energy obstruction claimed without EPnI: `1 ≤ 1/(d_M d_TA)+(ε_sec+ε_rel)/2`. This is the paper's claim to be independently tested, not a verdict issued here. |
| Theorem 5, PDF pp4–5 | Exact R/P/S closed-union consequence under explicitly changed generated-secret secrecy, relying on VE plus rewritten consumed-resource converse, direct key-assisted coding, composition and cost closure. |

Theorem 3's union over `0 ≤ λ ≤ 1` has the three bounds `C+2Q ≤ g(λN)+g(ηN)−g((1−η)λN)`, `Q+E ≤ g(ηλN)−g((1−η)λN)`, `C+Q+E ≤ g(ηN)−g((1−η)λN)`. Theorem 5's union has `R+P ≤ g(ηN)`, `P+S ≤ g(ηλN)−g((1−η)λN)`, `R+P+S ≤ g(ηN)−g((1−η)λN)`.

The original EPnI paper states a conjecture. The pinned OpenAI 2026 preprint's Theorem 1.1 asserts a proof for independent finite-energy ports with arbitrary internal entanglement. This intake reads the exact external statement and its vacuum consequence; it does not independently validate that proof or the Lean closure. Later wording must preserve both facts: the note relies on a cited unrefereed external theorem, and this review stage has not certified its soundness. Do not silently turn an external theorem into a new proof by Kriebel, or call the original conjecture currently open on the strength of a limited search.

## Consumed key, generation and catalysis

The exact 1005.3818v3 Section 5 body before Eq. (14) retains the consumed private register `J` and Bob's consumed key `S_B` in the private tuple `U=(M,T_A,J,S_B)`, with comparison `pi_U tensor sigma_(K,L,E^n)`. Eq. (13) supplies reliability. The related 0903.3920v1 Eq. (4) also retains `S_B`. These bodies were read directly rather than inferred from abstracts or prior audit reports.

The note's positive private theorem changes the promise explicitly. With generated `W=(M,T_A)`, public `X=(K,L)` and consumed `V=(J,S_B)`, it requires `||omega_(W X E^n)−pi_W tensor omega_(X E^n)||_1 → 0`; `V` is traced out and may become correlated with generated secrets and transcript. Eve is not additionally given the consumed key. Generated public/private messages are fresh, uniform and initially independent of preshared key. Unrestricted public common-randomness generation is not identified with communication. This is uniform-message trace secrecy, not semantic security or security after revealing consumed key.

The note charges the classical consumed registers by entropy/dimension in the revised converse. Finite gross rates are essential to the `o(n)` continuity terms: trace error tending to zero does not imply dimension-free absolute information leakage tending to zero. The composition claim discards consumed registers and charges finite seeds; its validity and the direct code construction remain tasks for the independent mathematical reviewers.

At N=0 the displayed quantum/GEN private regions are conversion cones; the literal-model proposition makes a separate claim about nontrivial generated private/key dimensions. At λ=0/1 the conditional thermal entropies vanish/take full values. At η=1/2, B/E entropies agree, so Q+E and P+S are at most zero. At η=1 the environment is vacuum. No theorem here covers η<1/2, infinite N, thermal-channel quantum capacity, amplifiers or confidential broadcast. Thermal/Gaussian attainment does not assert uniqueness or classify all equality cases.

## Primary sources, credit and honest limits

Sixteen primary PDFs were freshly acquired. `sources/primary/transport_receipts.json` records exact bytes/hashes, and `PRIMARY_BODY_READ_LEDGER.json` gives read line intervals, corresponding page spans, exact bodies and unread portions. Downloaded is not synonymous with read. Full third-party PDFs/texts remain local in ignored `sources/primary/.cache/`; only receipts, hashes and the reading ledger are publication material. The ignore rule was checked. There were no retrieval failures; the web tool could not open the Zenodo API/GitHub tree, but direct HTTPS acquisition obtained the actual record and pinned PDF. These successful alternate requests are receipted.

Central bodies read include OpenAI Theorem 1.1/Corollary 1.2 and Lemma 2.2 proof; WHG v1 displayed formulas, v2 conditional converses, and v4 Propositions 1–2/Theorems 3/7/Sections III.G–H; Wilde–Hsieh quantum Theorem 1/model and private Theorem 1/model/Section 5 converse; De Palma Theorem 11 and Corollary 12 with proof; CEF expected-input ρ-like propositions; Hsieh–Luo–Brun's consumed-key/message secrecy interface and covering statement; Devetak's direct coding portions; Hayashi–Nagaoka Lemma 2 with proof; and the joint erratum's correction/revised statements. The original Guha–Erkmen–Shapiro arXiv:0710.5666v2 was read in full, including the independent-port conjecture and consequences.

This supports source attribution, not a novelty adjudication: WHG's 2011 v1 already prints both formulas, v2 supplies the EPnI-conditional converse route, and De Palma Theorem 11/Corollary 12 provides the convex entropy-bound formulation. Coding mechanisms and the Hayashi–Nagaoka inequality belong to the cited predecessors. The joint erratum addresses generic optimization claims; it is not used as an operational secrecy correction.

Partial-read limits are material. The core OpenAI EPnI proof and formal closure were not re-audited, full QDC/CEF generic proofs were not read, and unrelated Gaussian/channel extensions were not examined. No current external priority search or worldwide-open-status conclusion was attempted. The extra 0801.0841 PDF was acquired during original-source lookup but not read substantively or used; the exact 0710.5666v2 conjecture source replaced it. No primary book was needed or represented as fully read.

## Handoff artifacts and remaining work

`ORIGINAL_ABSTRACT.txt` contains the complete published abstract, bound by `ABSTRACT_BINDING.json` to TeX content lines 19–34 and PDF p1. Only whitespace and the TeX typography in Wilde–Hsieh were normalized; the longer Zenodo description was not substituted. `PAGE_CONTENT_CANDIDATE.json` is a held, restrained candidate with exact dates/version status, original abstract, explicit dependency/operational limits, prior credit, AI/unrefereed disclosure, passive substantive-collaboration language and `follow_up: null`. It has no live canonical URL, no publication clearance and no prepared individual outreach.

Required next stages are independent analytic rederivation, an operational adversary addressing literal/GEN secrecy, zero-energy/catalysis/composition and constrained coding, appropriate independently authored reproducibility checks, and the root scientific decision. The strongest completed result of this intake is exact published-source custody and a source-bound scope/dependency map. No route is reopened or repaired by this assignment.

Scope-intake completion estimate: **100%**. This percentage measures this narrow intake deliverable, not mathematical correctness or inventory publication progress. The timestamped research log and sealed manifest accompany the report.
 