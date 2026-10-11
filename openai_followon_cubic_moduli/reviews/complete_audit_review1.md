# Complete audit review 1 — frozen local research package

Review completed 2026-10-06, America/Los_Angeles (2026-10-07 UTC).
Reviewer: fresh independent internal AI subagent `complete_audit_review1`.
Original target: `ORIGINAL_REQUEST.txt`; exact review version: `receipts/review_snapshot_v1.json`, timestamp 2026-10-07T05:20:04.260265+00:00.
This is a review of the research audit package, not a novelty-cleared publication candidate. No external individual was contacted. No Git operation or manuscript edit was performed.

## Verdict

No substantive mathematical defect was found in the **conditional** cubic consequence stated in the frozen manuscript. Its precise hypothesis remains the unrestricted algebraic gap in every dimension 2 through n. The manuscript does not claim this audit independently reproves or formalizes the upstream gap. Favorable scoped reviews are evidence about their inspected mechanisms, not an independent full proof certificate.

The publication goal is not achieved. A public KSZZ manuscript discloses the stronger all-dimensional target, and the proposed route combines the existing Spotti–Sun conditional reduction with an external upstream gap and established Li–Liu minimization. A different proof is not prohibited merely because the theorem was already disclosed; nevertheless this package identifies no genuinely new cubic theorem or proof mechanism. Withholding a **new-solution** Zenodo deposit is a supported recommendation. No statement that KSZZ contain the identical gap-based proof is warranted or made in the main manuscript.

Two documentary repairs should precede a fresh review. An independent clean source build also remains unverified because storage exhaustion interrupted output writing, as distinguished from a mathematical or TeX-source failure.

## Findings and exact evidence

1. **Clarify public-repository audit status.** `main.tex` PDF subject calls the note an “Internal mathematical and priority audit”; the abstract opens “This internal research note”. `CURRENT_THEOREM.md` says “Retain the consequence audit locally”, and other notes recommend retaining an “internal” note. But the original protocol authorizes and requires public repository checkpoints; `RESEARCH_LOG.md` records the already pushed owned checkpoint `091e36ff17ff1fc196bb4cc7d0aebc244566d85b`. The appropriate distinction is a research audit available in public repository checkpoints, not a submitted new-solution preprint. These labels must not imply that nothing has been publicly released. This is a documentary consistency finding, not a change to the conditional theorem.

2. **Distinguish competing disclosure from independent proof certification.** Checkpoint 02 of `RESEARCH_LOG.md` describes KSZZ Theorem 1.1 as “proving a stronger all-dimensional cubic K/GIT comparison”, then states that this project has not independently certified every proof in that paper. The precise verified priority fact is that the accessible manuscript **states** the theorem and supplies its claimed proof. Replace the first phrasing accordingly. `main.tex` itself already uses the more defensible “states” and “publicly claimed”. This repair prevents a priority audit from being presented as validation of the competitor's entire proof.

3. **Independent clean rebuild interrupted by storage.** I copied the exact frozen `main.tex` into a clean review scratch directory and ran Tectonic. TeX ran twice and reached `xdvipdfmx`; only minor bibliography underfull-box warnings occurred. The process then returned exit code 1 with `No space left on device (os error 28)` while writing output. I therefore do not claim independent clean-build success. The existing PDF was separately rendered and visually inspected on all five pages and is readable. This transient storage limitation must be cleared before any future production package operation. Only my own render/failed-build scratch files were deleted after inspection, not third-party evidence or peers' files.

No additional known substantive concern with the conditional consequence remains from my inspected scope. A later edited version requires a new complete-package review; this verdict applies only to the hashes below.

## Independent attacks on the proof and boundaries

- **Infimum versus Reeb:** Direct inspection of [Li–Liu](https://arxiv.org/html/1602.05094v3), Theorem 1.9, Section 6 setup, Theorem 6.2 and its limiting proof confirms the required global inequality over all centered valuations. The manuscript uses equality with the infimum before applying the algebraic upper bound. A Reeb-only variational minimum would not suffice.
- **Irregularity and normalization:** Lemmas 6.3 and 6.8 and the proof of 6.2 support the limit; approximating Sasaki metrics are not asserted to remain Einstein. The contact-volume sphere ratio gives the displayed k^k density normalization. Flat space and the ODP degree valuation provide compatible boundary checks.
- **Canonical form and algebraic eligibility:** I checked [van Coevering](https://arxiv.org/html/0806.3728v3), Sections 2–3, and [Collins–Székelyhidi](https://msp.org/gt/2019/23-3/gt-v23-n3-p05-p.pdf), Lemmas 6.1–6.2. The manuscript does not use rational plus Q-Gorenstein as a false klt criterion. Its finite-cover/Bishop case avoids extending Li–Liu's genuine top-form setup to arbitrary pluricanonical data. The simply connected punctured Ricci-flat cone has trivial canonical holonomy, and normal reflexive extension supplies the stated top form.
- **Singular links and dimensions:** Direct inspection of [Spotti–Sun](https://arxiv.org/html/1705.00377), Theorem 1.3(2), Section 5.1, Theorem 5.2, Lemma 5.3 and Section 5.2 supports use of smooth isolated transverse factors through iteration. The package requires every k=2,...,n, not only k>=5. It makes no direct smooth-link Li–Liu application to singular links.
- **Cartier root and Fujita:** The exact source conclusion retains -K=(n-1)L with L Cartier, not only canonical singularities. The strict volume threshold is valid. Fujita's official preview and the package's vanishing/duality ranges establish the necessary all-integer intermediate cohomology; n>=5 is well inside the valid range n>=3. No terminality hypothesis is inserted into the canonical Gorenstein version. The full 1990 classification proof remains a cited external theorem, not reproduced here.
- **CM sign:** Expanding the universal-family expression independently gives 2(n+2)(n-1)^n times the parameter hyperplane class, with positive sign. A positive rescaling leaves its role unchanged.
- **Complex GH and smoothing scope:** The saved OSS primary text explicitly distinguishes complex-structure-preserving GH topology from the bare metric quotient. The manuscript retains biholomorphic isometry and analytic GIT topology. LWX Theorem 1.1/1.3 support the corresponding smoothable closed-polystable interpretation. Equal dimension and anticanonical volume are not used to select a deformation component. No scheme, stack, functor or every-nonclosed-semistable upgrade is inferred.
- **Priority:** I directly checked the live [primary author page](https://sites.google.com/uic.edu/jzhao/research), which still links “K-moduli of cubic hypersurfaces”, and the saved PDF's exact main statements/component/proof sketch. Present disclosure is verified; earliest posting is not. The source route differs from ours. The main paper's existing no-new-contribution conclusion is consistent with the original requested scope, without asserting that every alternative proof is banned.
- **Upstream dependence:** I read the full geometric/semigroup scoped audit reports and inspected the pinned introduction's unrestricted theorem and the actual bootstrap upper-bound proof. I did not personally reread every line of the 57-page upstream proof or rebuild its original cited external theorems. This complete package review verifies the package's honest external-input status and conditional deduction; it is not a new comprehensive independent certification of all upstream arguments.

The total summary of each browsed primary source above is deliberately limited; theorem/section labels are stable evidence locators.

## Inspected scope and reproducibility evidence

I read the entire original request, workspace `AGENTS.md`, entire `main.tex`, all five rendered `paper.pdf` pages, `README.md`, `CURRENT_THEOREM.md`, `DEPENDENCY_LEDGER.md`, `APPROACH_TABLE.md`, complete `RESEARCH_LOG.md`, every frozen `agent_notes/*.md` report, and the complete priority adversarial review. I inspected source manifests, build receipts, arithmetic code and the owned isolated-index publication script without running its mutation operations. Primary source inspections are listed above; competitor central theorem/scope were checked directly, not its full proof. All rendered PDF pages showed legible formulas/references and no clipped/overlapping content. PDF metadata, page count and dimensions were checked. No successful compilation is mistaken for proof.

An independent arithmetic child checked all 18 frozen snapshot entries; all 21 pinned-manifest entries against the read-only clone and the project-local copies; the seven transfer-source PDF hashes; both rebuilt-upstream PDF receipt hashes; source/code arithmetic agreement; and absence of a relevant family037 Lean verification claim. Both exact rational arithmetic scripts pass. It independently checked the exponential-tail certificate and the fourfold constants, including positive contradiction margins, and the CM coefficient. Its report is `reviews/complete_audit_review1_arithmetic.md` if storage permits saving; its result is incorporated here. No inconsistency was found. The review artifact itself is additional evidence created after the frozen snapshot and is not part of that snapshot.

## Exact frozen reviewed hashes (SHA-256)

| File | SHA-256 |
|---|---|
| main.tex | cca7f77f3e225990b46d9f62284513471aa8f02cd0d00c8dcc99cc46149f9030 |
| paper.pdf | 2acab134d1b1ad0308fc3f15c817c5f94690d0f3e379b039b6ab53fc28e4f7aa |
| README.md | e66131ae2b4c70de8acc26fe209c74b1ecd57d4a9f89ada9fcf0007bf7410ef4 |
| ORIGINAL_REQUEST.txt | e6c5d41d0c799d59521c4e055da76b96b9947130e3107ae959b74ea303f75b6c |
| CURRENT_THEOREM.md | 6f89a6f991546ae152142ba3a36ac105c914fbec45f4d4c739b16b2e58ad8f0a |
| DEPENDENCY_LEDGER.md | f24b13bb493d238115d1afa61133d6a310cd2955691ba39a26ca4e5e0ca57ecf |
| APPROACH_TABLE.md | afb016388dbcfb5960d664062b4cd8dbdbf730954e7fff2872d8c83de249c88a |
| RESEARCH_LOG.md | 18ae045212c93a5c740b06aaf865bd0713930b2d59ce83e0f24e701277d4e4c3 |
| sources/PINNED_MANIFEST.json | 876e3db29cae7bb566c5557247c6db1e18bc97a1a051f7b179906adea325876c |
| reproducibility/verify_constants.py | 177b9e48f8cbc7e4b948978e86f0ad73a92241a29a8e29d1e29caf5e94a4c079 |
| agent_notes/fourfold_constants_check.py | 4033f4f671710ec3b3ff35b92770ab289a017be7f8e81baf29273a7b5b8cb764 |
| agent_notes/priority_audit.md | cd6286a55ea506d310668d922ebbde4cfc07a0db0a92e146814974ce7fa368af |
| agent_notes/reeb_bridge_audit.md | bd38f4b478aeeeb58daa5a80f5ff6ad634002b21dc85f142289c8cdefb83a312 |
| agent_notes/spotti_sun_source_hashes.json | d3940de2f9676e138d92f2593710ada8deed3ad1d4022320b604e69babbfc46e |
| agent_notes/spotti_sun_transfer.md | e32fb4ed16462e25f8c9768165fb94cdda053efb52345a4209b0096b5cd26d5a |
| agent_notes/upstream_geometric_audit.md | e8b6eb07096f36f7d25c867bbfd43c305938e713a8e748a7680c91ea2ff6e59c |
| agent_notes/upstream_semigroup_audit.md | b2566e1045f2ac902aadb7dcea84aac0745b5c14225035da8062b0d410cf4e61 |
| reviews/priority_adversary.md | bd6c88085b03c16bd79e80fbae897b224cf51d8f054b10d90dd016c303566302 |

Upstream commit: `adc7f1241b42e322a6451854ab7e4b4c146bf78a`; original all-dimensional PDF hash `5e2cdac4857afef7065967c49c6f4f9a1aec01b0b776ce324220707545e8e114`; original fourfold PDF hash `6d58101115e4bf4f963ea2bc4e301f041eaff601e3b325ec475200e43e3031a4`; public KSZZ PDF hash `6813e3d3be36c087e60b696f40652f8a837da7fcd9e3bdbd7af7df030c3ad65e`.

No Zenodo/DOI/tracker operation was reviewed or performed because none is appropriate at this stage. The original publication objective remains unachieved, and this review does not decide the persistent-goal tool's repeated-blocking threshold.
