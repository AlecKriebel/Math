# Research log: embedding-dimension gap, 30000439

Start: 30 September 2026, 03:55 UTC. Ceiling: 05:55 UTC. Model: gpt-6-astra, xhigh. Maximum five substantive proof responses. Only this problem folder and its dedicated branch may change.

## 03:56–04:05 UTC: source check and construction

The requested upstream page was tried first but inaccessible. Read the pinned full source record and original Brehm report, pp. 701–702 of OWR 12/2006. The exact target is a gap of at least two between the minimum PL and simplexwise-linear Euclidean embedding dimensions of one finite simplicial complex. No matching prior report exists; queue row was queued, 0/5, and matching all-state PR/branch searches were empty.

Read the relevant original Brehm–Sarkaria construction and current primary literature: Frick–Hu–Scheel–Simon (2023), Newman arXiv:2212.09576 and its 2026 journal metadata, and Lee–Nevo arXiv:2307.14195, including Lemma 3.1. Newman's current corrected version only asserts even-dimensional thresholds; an earlier odd-dimensional claim was withdrawn. No withdrawn claim is used.

A candidate combines a deletion-robust version of Newman's even-dimensional nonembedding mechanism with Lee–Nevo's inflation lemma. Sample triangles with probability n^(-3/2), delete at most n^(5/4) to remove shared-edge conflicts, and uniformly prohibit linear embedding in R4 through Janson's inequality, order types, and a union bound over all deletions. The resulting linear 3-uniform hypergraph PL embeds in R3 after adding a private fourth vertex per triangle and applying Lee–Nevo.

Checkpoint completion estimate: 75% toward a complete candidate; novelty unestablished. No solved claim.

## 04:09 UTC: substantive response 1/5

Saved the complete candidate proof. It supplies the exact dimensions 3 and 5, including a nonplanarity argument for the lower PL bound and a moment-curve upper linear bound. The explicit finite existence parameters n=2^256, p=2^-384, m=2^320 require only small exact integer calculations. No complex of this size was generated and no exhaustive search was run. All 16 exact bound checks passed.

Completion estimate: 90%, with independent adversarial review outstanding. The candidate credits all imported theorems and does not assert novelty or first resolution.

## 04:10 UTC: authorization and source precision

The initial checkpoint command was denied by the action reviewer for lacking visible authorization for research pushes. After exact user transcript evidence was supplied, the same branch push was retried once and succeeded. No workaround was attempted. The initial denied composite command had not committed the artifacts; a subsequent reviewed-scope checkpoint commits the saved files normally.

The Janson inequality was checked directly in the current author-hosted Frieze–Karoński text, Section 34.6, Theorem 34.13. The use of ordered distinct overlap pairs is conservative for the displayed denominator. Candidate snapshot frozen for review; hash is in provenance.json.

## 04:22 UTC: separate review passed

A separate agent independently audited the exact original target, every imported theorem, the uniform quantification over order types and adaptive deletions, the generic-perturbation step, PL inflation, and both exact embedding dimensions. No required mathematical correction was found. All 16 submitted checks and 396 independent exact assertions passed. The full review and its companion files are copied unchanged into `independent_review/`.

Completion estimate: 100% toward a complete independently AI-reviewed candidate for the exact existential target. Historical novelty remains unconfirmed and external peer review has not occurred. The candidate is retained byte-for-byte with its original pre-review header; README and provenance record the current review status. Preparing the one authorized draft PR; no shared queue files changed.

## 2026-10-01T15:29:12.909130+00:00 — full mathematical gates, direct subdivision supplement

Three independent families pass. Direct first-barycentric-subdivision proof and fresh child verification bypass the imported radial marked-vertex detail. Global current proof uses this supplement; original14files and historical reviews are preserved. Full two-family priority audit begins only after mathematical gates. Workflow **40%**; no paper/publication/acceptance.

## 2026-10-01T16:03:23.722848+00:00 — independent priority audits complete

Two families find no examined exact prior subsumption and prominently credit the known methods. Bounded literature clearance is not global priority proof. Current proof/source/provenance globally updated; preprint preparation follows, with fresh full-package reviews required. Workflow **50%**.

## 2026-10-01T16:23:53.443127+00:00 — paper draft and rendering checkpoint

Two independent deep priority families complete with bounded clearance and explicit access limits. The research-note draft at simplicial_embedding_gap_30000439/paper.tex compiles successfully in the native editor. All five exported PDF pages were visually inspected; the overfull local-fan equation was repaired. The proof distinguishes original affine simplices from subdivision and states the exact PL3/affine5 minima. Verification package and fresh complete publication rounds remain pending. Workflow **55%**.
