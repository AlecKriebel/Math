# Fresh whole-package adversarial review, round 2

Verdict: **REQUEST_CHANGES for five publication/reproducibility safeguards.** No mathematical, attribution, current-artifact integrity, or visible-layout defect was found. The five findings concern what the workflow can accept on a later build or retry; they do not assert that the supplied PDF or ZIP already contains those corruptions.

The review was independent of previous whole-package review conclusions and `FIRST_REVIEW_FIXES.json`. Neither was read. Archived earlier math/source/priority reports were treated as candidate claims, not independent seals. No person was contacted, no outside application was mutated, and no Git/index/checkout operation was made. All authored work and control files stayed in this review folder. Primary scholarly HTTP GETs were read-only.

## Exact review boundary

`INPUT_BINDINGS.json` binds 17 inputs before execution. The PDF is 61,285 bytes, SHA-256 `f066f56ee442078163b85c858bf180f484954b0bda56d3c686aa0c6b13a34853`; the ZIP is 257,172 bytes, SHA-256 `17e8543dce0d41c829291c8840a749860159cff9fb48a8c6af8b3463dd4b895f`. TeX source is `f2d3b59d95c813d07f4792d1781b29a09c7284255d3141a0ef3f7842f07204c2`; deposit metadata is `56ac20fd2317df7b1e8e2831dd302ce4b4badf0c8a5a89e2fb976ad9ef2ad50f`.

The other exact inputs are BUILD/COMPILE/LAYOUT receipts, current simultaneous proof, all eight specified workflow/replay scripts, and the supplied workflow regression receipt. `FINAL_FREEZE.json` performs a second exact comparison after the report/verdict are finished and binds the authored evidence.

## Actionable findings

### R2-W1 — Bind the links actually published to the authenticated DOI and record (P2)

Locations: `publication/update_pr_publication.py:80–95`, `publication/check_public_downloads.py:25–39`, `publication/append_tracker.py:20–29`.

The public checker authenticates `id` and `doi`, but not the publication receipt's `doi_url` or `record_url`. The PR note and tracker use those unchecked strings. A receipt for record123 / DOI10.5281/zenodo.123 with links pointing to record999 passes the public identity logic; if the tracker agrees with the wrong DOI URL, the PR updater accepts it too. The `mismatched_doi_record_urls_resealed` main-entry control demonstrates acceptance. This is a missing consistency constraint in creating an initial intent as well as retrying one; it is not a claim that arbitrary modification of a previously sealed intent escapes its digest.

Fix: validate a positive record/deposit ID, the exact DOI assigned to that ID, `https://doi.org/<doi>`, and the canonical `https://zenodo.org/records/<id>` consistently before tracker append, public-verification receipt issuance, or PR publication. Bind both URLs in the public-verification identity and intended PR identity. If another canonical URL form is deliberately supported, enumerate it explicitly rather than trusting an arbitrary string.

### R2-W2 — Recompute and compare the complete four-cell tracker row (P2)

Location: `publication/update_pr_publication.py:83–84`.

The updater requires only that cell1 contain a numeric substring, cell2 be empty, and cell3 equal the publication DOI URL. It ignores the fourth cell entirely and does not require the exact original-problem label. A receipt with unrelated/false publication notes is accepted in `bad_tracker_notes_resealed`, despite the PR note asserting an exact tracker append/readback. An old tracker receipt for the same DOI can therefore certify stale notes on the first creation of a new intended PR commit. Existing saved intents correctly reject an unresealed receipt change; that working guard does not supply the missing semantic comparison.

Fix: share a single expected-row constructor between `append_tracker.py` and the updater, require exact equality of all four cells, and validate that `updatedRange` is a single four-cell row on the intended tracker tab. Continue binding the entire tracker receipt and exact range in saved intent/receipt checks.

### R2-W3 — Require the exact eight-script review coverage, rather than trusting an arbitrary dictionary (P2)

Location: `publication/update_pr_publication.py:92–93`.

The loop checks only the workflow entries that happen to be present. An empty `gate['workflow']` bypasses all current-script checks. `missing_workflow_gate_resealed` changes `append_tracker.py`, supplies an empty coverage map, and is accepted by the main entry point. This illustrates an incomplete gate accidentally produced by a coordinator; it does not purport to make a forged trusted review judgment cryptographically impossible.

Fix: require that the workflow map's key set be exactly the designated eight paths before checking any digest. Reject missing, extra, duplicate-equivalent, or unsafe names. Also give the final-review gate a defined schema that explicitly binds the current complete review set; a bare status string is not a substitute for that orchestration contract.

### R2-R1 — Require matching compile/layout receipts before freezing a build (P2)

Locations: `publication/build_package.py:9–22`.

The builder never reads COMPILE_RECEIPT or LAYOUT_VERIFICATION. It packages current TeX and simply copies whichever PDF is already at `output/pdf/main.pdf`. Editing TeX and rerunning the builder before recompiling can therefore produce an archive/source and PDF from different revisions while returning a new successful BUILD_RECEIPT. Missing compile/layout receipts also do not block this wrapper. The isolated control uses an old real PDF, changed source, and no compile/layout receipts; preparation and finite verification are stubbed only to isolate the wrapper, and the build is accepted.

The supplied artifacts themselves are consistent: their compile and layout receipts bind the exact reviewed source/PDF, the displayed pages match the source, and the current BUILD receipt is accurate. The finding concerns preventing an ordinary stale-output rebuild.

Fix: before creating/replacing release artifacts, require a successful compile receipt with source hash equal to current TeX and PDF hash equal to the actual compiler output. Require the current layout receipt to bind the same source/PDF and expected page count. Recheck those inputs after packaging to detect changes during the build. A stale or missing receipt must fail before replacing the public artifacts or issuing a new BUILD receipt.

### R2-R2 — Check the archived post-freeze cross-challenge manifest too (P2)

Locations: `publication/verification/verify.py:43–47`; omitted manifest: `priority/independent/cross_freeze_20261017T183513Z/MANIFEST.json`.

The verifier checks the independent family's first freeze, but never traverses its separate cross-challenge freeze manifest. A modified CROSS_FAMILY_CHALLENGE.md followed by the normal root-manifest rebuild passes every binding check even though that nested immutable manifest is stale. The isolated control stubs only the costly exact-driver outputs; all root/nested binding code executes. The README's broad nested-frozen-manifest replay description consequently overstates this coverage.

Every nested binding in the supplied archive, including this omitted cross freeze, was independently checked here and matches. There is no present corrupt cross report.

Fix: validate the cross-freeze manifest's three entries, or use a schema-aware traversal of all archived nested manifests. Add a regression that mutates a nested frozen member and rebuilds only the root manifest; the nested mismatch must still fail. Preserve the distinction between byte integrity and historical truth/independence authentication.

## Publication integration boundary

The updater writes `PR_BODY_FINAL.md` and a branch receipt, but does not itself edit/read back the PR body. A normal retry can therefore finish with the original body. On clarification, the coordinator stated that a separate final body edit/readback was already planned and that this script's receipt intentionally described only the branch update. Accordingly, absence of body mutation alone is **not an additional defect** in the reviewed branch-only contract. An explicit end-to-end wrapper or guarded idempotent body step would make completion easier to audit. The final publication must still actually perform that planned step before reporting completion.

## Mathematical attack and strongest verified result

The strongest verified written claim is the dense simultaneous theorem: a dense meagre subset B of HC(D) has `|(pf)^(n)(0)| -> infinity` for every nonconstant complex polynomial p, with f fixed first and the threshold allowed to depend on p. Universal polynomial preservers of all HC(D) are exactly nonzero constants. These statements follow under the stated standard complex-analysis and Baire assumptions.

The annular series mechanism survives the following attacks. Eventual jet upper bounds `log(n+e) <= n+1` imply normal convergence on every fixed disk. Derivative evaluations are continuous; X_M is nonempty, closed, and complete in the inherited complete metric. There is no need for D-invariance. Each hitting set is relatively open. Retaining the jets through L controls the original neighborhood by `2 sum_(n>L) u_n r^n/n!`. For an arbitrarily huge target, u_n tends to infinity, so a sufficiently remote finite target block is admissible. Small or zero target coefficients can be moved radially to the lower boundary with error at most ell_(N+k); nonreal phases create no restriction. All later shifted jets are baseline jets bounded by the decreasing ell_N, hence the **whole infinite shifted tail**, not just a finite block, is bounded by ell_N e^R. Countably many Gaussian-rational polynomials, integer disks, and reciprocal-integer tolerances then suffice for Baire and orbit density. This also works for M=0, where jet0 is constrained to the unit circle.

For the product estimate, `c_d(n)_d a_(n-d)` has lower size `|c_d| n^(d-1/2)` while all lower degrees together have upper size `C_p n^(d-1) log n`. The ratio tends to zero, including d=1. Reverse triangle is phase-independent. The hypotheses on f do not involve p, so the conclusion is deterministic for every p chosen afterward; there is no uncountable-intersection or quantifier-switch argument. An escaping tail misses the unit disk eventually, and a small subdisk can avoid the finite earlier values. Evaluation is continuous and onto, so scalar nondensity obstructs hypercyclicity. Appending a baseline after any polynomial and using relative density proves ambient density. Each closed X_M contains no polynomial and has empty ambient interior; the union B is meagre. This coexists with Costakis's residual positive-preservation family. Nonzero scalar multiplication is a homeomorphism commuting with D, while zero fails.

The original finer fixed-p result also remains valid for **each prescribed starting f in HC(D)** and each neighborhood. At a root alpha of multiplicity m>=1, the derivative order k+m contains a nonzero new coefficient `A_k=q_m(k+m)!/k!`; every cross-term correction index is smaller than k. Choosing c_k only when the current product jet is inside the eta disk locks that derivative outside it without changing earlier derivatives. The uniform bound `|c_k| <= 2 eta k!/(|q_m|(k+m)!)` gives a bounded null sequence and an entire null-orbit correction. All derivatives below m vanish at alpha. The excluded disk centered at eta/2 deals with both the zero prefix and later barrier values. The estimate `||h||_R <= 2 eta e^R/(|q_m|m!)` on disks about alpha gives arbitrary closeness as eta tends to zero, even though corrections depend on eta. Dense tails make null-orbit perturbations preserve HC. No arbitrary-input obstruction was found.

`independent_checks.py` adds 36 exact Gaussian-rational cases, 288 independently evaluated ordinary global-coordinate product identities, 36 corrected and252 retained recursive branches, shifted complex roots, multiplicities1/2/4, and eta=10^-8. These corroborate algebra only; they do not certify infinity or Baire arguments.

## Primary sources, probability, priority, and dates

Fresh primary bodies/version records were retrieved without relying on archived source seals; exact response bytes are bound in `SOURCE_RECEIPT.json`, and the bodies stay ignored. The inspected anchors were [Costakis printed330](https://ems.press/content/serial-article-files/46147), [Nikula v1 pp2–3 and Gaussian p10](https://arxiv.org/pdf/1209.6209v1), the [official Nikula version record](https://arxiv.org/abs/1209.6209v1), [Bayart–Matheron v1 settings/Proposition3.3 pp11–15](https://arxiv.org/pdf/1112.1289v1), its [official version record](https://arxiv.org/abs/1112.1289v1), and [Nikula's publisher metadata](https://link.springer.com/article/10.1007/s11785-013-0328-0). This authenticates the exact applicable hypotheses and bibliographic anchors; it does not independently reprove every source theorem.

Costakis's actual Question5 is universal pointwise multiplication, and Theorem6 is residual common preservation. Their quantifiers are correctly distinguished. Nikula Theorem1 assumes IID full-complex-support jets with the stated weak logarithmic-tail condition and concludes almost-sure entirety and frequent D-hypercyclicity. Standard circular Gaussian jets satisfy it. The inspected source uses independent real/imaginary variance1/2, giving density `pi^-1 exp(-|z|^2)`. Small-ball failure probabilities at exponent3/4 are summable, as are the upper log-tail probabilities. Borel–Cantelli1 supplies a single eventual-bound event independent of p; the leading-degree estimate then proves simultaneous escape. Polynomial additions preserve all sufficiently high derivatives and give an ambient dense translate of polynomials.

The raw square-root lower envelope would be false almost surely: independent failure probabilities `1-exp(-1/(n+1))` have divergent sum, so Borel–Cantelli2 gives infinitely many failures. The note avoids that mistake. It applies Nikula before clipping. Only finitely many upper clips occur; each lower correction is at most ell_n; the total correction jets tend to zero. The `e^R sup-tail` estimate proves the correction is an entire null-orbit. Visiting a smaller target neighborhood with positive lower density and discarding finitely many visits proves FHC stability. Each clipped coordinate has full relative support in its annulus, including angular support on the collapsed unit circle at n=0. Independence and uniform factorial tails identify finite-coordinate cylinders with a neighborhood basis in X_M. Thus exact-annulus FHC density follows too; no IID full-plane theorem is incorrectly applied after clipping.

For Bayart–Matheron, X=H(C) meets the separable complex Fréchet setting, D is continuous, normalized Haar on the circle is finite, and `E(lambda)=exp(lambda z)` is continuous and bounded in each seminorm. The integral operator is linear without a conjugation. For Fourier basis `lambda^k`, it sends k<=0 to `z^(-k)/(-k)!` and positive k to0. Thus its Gaussian law has **exact** independent standard complex Gaussian jets after reindexing; there is no covariance-only or normalization gap. Summing `R^n/n!` proves gamma-radonifying convergence in every seminorm. The range contains all polynomials, giving full support. Riemann–Lebesgue applies to every complex L1 density and checks the c0 mixing hypothesis. Proposition3.3 identifies the particular law. Strong mixing implies ergodicity; Birkhoff on a countable open basis gives almost-sure positive visit frequencies. No Banach-only hypothesis or inverse of D is required.

The served Nikula v1 PDF visibly has internal date August2,2018 while the official record dates v1 to September27,2012. The cause is not authenticated. Publisher metadata independently gives online October8,2013 and the2014 issue. The package qualifies this distinction and does not pretend to authenticate a byte-identical historical2012 PDF. The Bayart–Matheron v1 official record is December6,2011; the note does not backdate a later explicit remark. No source was shown here explicitly printing the multiplier corollary. The first explicit recording/earliest underpinning remains undetermined. The current publication appropriately avoids new-first-solution, new-existence, and still-open2026 claims. Bounded unsuccessful searches and independent-family receipts are not priority proofs.

## Reproducibility, provenance, layout, and metadata

A fresh safe extraction has104 unique ZIP members and exactly matches the supplied staging tree; the root manifest binds103 members. The portable verifier was actually run from the extraction under normal, -O, and -OO; each entry itself replays both exact drivers in all three modes. All passed with semantically identical expected results. The supplied workflow `--worker` was separately run under the same three modes without rewriting its reviewed receipt. Its stated scope is correct: validator/projection fixtures, not complete application integration.

An independent traversal checked134 manifest entries across all six archived MANIFEST files, plus current acceptance document bindings. The original eight submitted SHA256/size/Git-blob identities match; nested original/current/frozen bindings match. Byte corruption, missing member, extra member, and duplicate root-manifest entry are all rejected before finite executables run. The cross-freeze omission is separately reported above rather than conflating outer byte integrity with nested semantic consistency.

The root diagnostics genuinely execute three altered algorithms. The other driver's five controls are fixed-fixture false predicates; they are correctly disclosed as such throughout the current note/README/records. Historical omitted receipt bodies and third-party source bodies remain unavailable and are not authenticated by current hashes. The original research input-boundary/independence receipts are preserved authored assertions, not externally certified facts. The broader current/historical distinction is clearly stated, and archived historical claims are not silently rewritten as current acts. Finite code verifies identities, never the infinite theorem.

The PDF was freshly rendered with Poppler and all four pages visually inspected. Title, author, ORCID0009-0001-9320-500X, date17October2026, equations, citations, bibliography, page numbers, proof transitions, AI-use disclosure, and unrefereed status are legible and consistent with TeX/deposit metadata. No clipping, overlap, missing glyphs, or inappropriate split of the disclosure paragraph was found. No source body is redistributed in the ZIP. PDF technical metadata has no custom Title/Author fields, but the printed title/author are correct; no such technical-field assertion was made, so this is not a defect.

Deposit metadata has the requested title/creator/ORCID, open access/CCBY4.0, preprint/version/date, subject keywords, source DOIs/version links, and derivation link to the original PR. Its historical-answer and AI/unrefereed framing matches the manuscript. The public schema mapping uses resource_type.type/subtype for upload/publication type and license.id for license; all other supplied fields are compared exactly. Every one-field metadata corruption, record-ID/DOI mismatch, duplicate/missing file, and corrupted PDF/ZIP was rejected by mocked public-checker main-entry tests. No actual public record has yet been authenticated by this review; that later live gate remains required.

The offline GWS tests demonstrate one append followed by exact recovery, recovery after a simulated accepted append with a lost response, refusal of uncertain unmatched intent, header mismatch, duplicate/conflicting rows, and failed readback. All26 service cases pass in normal/O/OO. Mocked PR main-entry checks reject stale/missing intents, altered parent/path/blob bytes, bad public identity, missing public receipt, mismatched source snapshot, altered current source, workflow drift when covered, and DOI-cell mismatch. The three semantic-coverage omissions above reproduce in every optimization mode. All Git/gh/GWS/Zenodo mutating behavior was mocked; no public operation was attempted.

## Evidence and limits

Primary checkable evidence: `REPLAY_RECEIPT.json`, `OFFLINE_MODES_RECEIPT.json`, `OFFLINE_GUARD_RECEIPT.json`, `OFFLINE_SERVICE_RECEIPT.json`, `INDEPENDENT_CHECK_RECEIPT.json`, `SUPPLIED_WORKER_RECEIPT.json`, their authored drivers, input bindings, source receipt, and final freeze. Intermediate extracted/rendered/source/control directories are ignored.

This is an internal adversarial AI review, not human peer review, formal proof-assistant certification, exhaustive historical-priority clearance, or a live-service integration test. The supplied mathematics and artifacts are accepted within that scope; the five workflow safeguards should be repaired and the changed package reviewed afresh before publication completion.
