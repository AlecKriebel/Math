# PR1064 credited-corollary preprint preparation report

Prepared 2026-10-14T04:31:27.195103+00:00. Assigned local preparation complete (100%). Whole-package publication readiness remains false; no issue/service update, publication, upload, merge, Git mutation, or external contact was performed. Work confined to newly created preprint_v1_0.

## Eligible mathematical and scholarly scope

The five-page paper is titled **An explicit Frobenius corollary of established marginal entropy bounds for permanents** and credits Alec Kriebel (ORCID 0009-0001-9320-500X), CC BY 4.0. Its title, abstract, main statement, source section, README, status and three normalized metadata records characterize a credited corollary. The random Gibbs-marginal exposure mechanism is Anari-Rezaei 1811.02933v2 section4 Eq6. Conditional Jensen gives scalar q(b)=-b^2 log(b)/(1-b) with q(0)=0 and q(1)=1. The explicit scalar threshold estimate is supplied here without certified novelty. Anari2608.28031v2 Lemma7 expands to the same precursor with a distinct nonnegative sequential permutation KL. Dong-Jain2609.02017v1 Theorem3.1 at g4 yields the entropy lemma via row/column expansion and Jensen.

The result applies to every nonnegative row-stochastic n-by-n A, n>=1. With unnormalized S=sum a_ij^2, per(A)<=exp(-n+e^4 sum a_ij^2 log(e/a_ij))<=exp(-n+e^4 S(1+log n)). Fixed S<=gamma gives all-n exp(e^4 gamma)n^(e^4 gamma)e^-n; the pure n^(3e^4 gamma)e^-n consequence is only n>=2. The exact Barvinok-Samorodnitsky OWR44/2008 problem9 pp2549-2550 norm hypothesis is retained and its already-known van der Waerden lower bound credited. Strong entrywise gamma/n is not substituted. Fixed k uniform blocks with k<=gamma show polynomial loss is necessary; the stated exponent is not sharp.

The proof is self-contained: positive histories only; support-normalizer positivity; independent priorities; finite-support logarithm integrability; conditional Jensen integral with both factors of b; per=0 before Gibbs; B need not equal A; matrix KL is not sequential KL; all-entry mass cancellation retains d(0,a)=a; h monotonicity used only on [0,1]; normalized p=a^2/S has entropy at most 2log n and S>=1. All scalar zero/unit/switch cases and n1 are included.

## Custody, evidence and archive

Before the first write, all 170 pre-existing audit files were frozen by byte count/SHA256, including ignored raw source bytes, without modifying them. All 72 selected authored inputs are byte-exact copies, including all nine root submission snapshots and full root, entropy, scalar/source and priority reports/derivations. Complete required reports and locators were read; current family seals were freshly rehashed (32,30,31 records). Full original custody is local INPUT_PINS.json; safe distributed custody is COPY_MAP.json/SAFE_INPUT_PINS.json. This worker made no fresh source fetch or new actual-Git claim. Historical inspection/identity claims retain their original dates and scopes.

The exact 97-member archive has a safe explicit allowlist, authored UTF8 text/code plus the authored PDF, sorted paths, fixed timestamp 2026-10-14 00:00:00, Unix regular-file mode0644 and deflate9. Full third-party PDFs/text/images/raw search captures, full 28MB recursive Git tree and other unnecessary raw Git/service captures are excluded. EXCLUSION_LEDGER.json states exclusions; old seals may point to omitted local evidence, while the new SUPPORT_MANIFEST defines distributed coverage. No old snapshot/report was edited.

The external publication/DEPOSIT_BINDING.json binds PDF and ZIP and is excluded from ZIP to avoid a hash cycle. A present descriptor is always checked strictly; clean extraction works without a descriptor, with a separate optional required mode. Bare metadata.json and both wrappers normalize exactly to the same bibliographic object.

PDF SHA256: 67f07f64a5b06c9a4372c285ed438e735fb780d8477b25652bea4f7f6c72e072 (74898 bytes).

ZIP SHA256: 46101b4ccb180bb99996e02ebceb1b23e616da23f54c291ddf1688f3976ceb63 (263179 bytes).

## Reproducibility and QA

The unchanged entropy reviewer checker runs only in normal -I -B mode with assertions active; current replay matches the root baseline after declared runtime-only completed_utc/python/platform projection. The new disclosed derivative uses explicit raising guards and adds direct suffix, Anari expanded KL and Dong-Jain g4 model checks. It agrees in normal and optimized modes. Seven faulty variants (scalar divergence deletion, wrong unit endpoint, zero-mass term deletion, n1 purepower misuse, KL confusion, sequential KL deletion, wrong Dong-Jain half coefficient) are rejected in both modes. A diagnostic-record bug at per=0 was found and repaired before sealing; final controls passed. These are 11 matrices, 2 arbitrary laws, 1573 positive histories and 201 scalar pairs with 120-digit Decimal logs, finite corroboration rather than universal/interval/formal proof.

All positive README commands succeeded from a clean ZIP extraction: verification, checker replay, deterministic archive rebuild/verify and Tectonic compilation to ignored temporary outputs. Rebuilt ZIP is byte-identical in the documented Python/zlib environment. Fourteen normal/optimized integrity/binding controls confirm required-absent and present-malformed descriptor rejection, correct external binding acceptance, extra-member/hash corruption rejection and unsafe-archive rejection. Builtin final compiler succeeded. Every one of five final PDF pages was individually rendered and viewed; no clipping, overlap, lost glyphs, margins or equation defects. No overfull boxes remain; a harmless bibliography underfull warning was visually cleared. No cross-environment PDF byte-identity claim.

## Remaining gates and limits

STATUS.json is a dated preparation snapshot with publication_ready=false and issues_updated=false; it requires at least two NEW whole-package adversarial reviews and records zero completed. Ascending publication/service action remains held after PR1032. Earlier math/priority reviews concern historical inputs and do not certify this new package. FINAL_VERIFICATION.json gives the full final preparation scope, and OUTPUT_PINS.json is frozen only after this report and final verification.

Historical novelty and priority of scalar/final norm statements remain UNKNOWN. Full Soules2000/2003/2005 bodies were inaccessible403; broader admissible Orlicz functions, Roos hierarchy and optimized lp consequences are not exhausted. No first/new-method/independent-discovery/worldwide-open/exhaustive-literature/optimal-exponent claim. Extensive AI assistance; unrefereed; no external human peer review or proof-assistant certification. Source bodies and omitted historical programs are not distributed or newly replayed.
