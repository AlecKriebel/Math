# Partial browser verification of three new research pages

This checkpoint preserves completed public-browser presentation checks for the quadratic and bosonic articles, plus three actual Research-link returns to the 50-entry index. **The assignment is incomplete.** Completion estimate for this bounded browser task is **30%**. Full browser PASS, native tracker acceptance and overall goal completion are all false.

The deployment under review was site commit `16b7b547c7cf7f54e586f2a753fc861763807f33`, Firebase release `f3d003e1e8f50e45`. Scientific and public-copy acceptance belonged to the parent task. This checkpoint supplies browser evidence only.

## Completed checks

| Paper | Desktop article | Article at 390 pixels | Desktop Research return | Narrow Research return |
| --- | --- | --- | --- | --- |
| Nonunique nearest stable complex quadratics, Zenodo 23306332 | PASS | PASS | 50 links and three new titles | 50 links and three new titles |
| Pure-loss bosonic dynamic capacities, Zenodo 23203100 | PASS | Pending | 50 links and three new titles | Pending |
| Simultaneous amplifiers beyond relative fitness 3/2, Zenodo 22089807 | Pending | Pending | Pending | Pending |

The article checks covered the title and publication metadata, plain-language explanation, scope and limitations, actual embedded PDF first page, collaboration statement and citation. Raw DOM snapshots preserve the rendered article content; viewport screenshots establish the visible layout. The desktop article column remained 1000 pixels wide inside a 2056 × 1146 viewport. The completed narrow quadratic views used 390 × 844 with a 374-pixel content/iframe width and no document-width overflow.

The quadratic desktop top, scope, embedded manuscript, and collaboration/citation are in `quadratic-desktop-top.jpg`, `quadratic-desktop-scope.jpg`, `quadratic-desktop-embed-revisit.jpg` and `quadratic-desktop-collaboration-citation.jpg`. Its corresponding accepted narrow frames are `quadratic-narrow-top.jpg`, `quadratic-narrow-plain.jpg`, `quadratic-narrow-scope-actual390.jpg`, `quadratic-narrow-embed-actual390.jpg` and `quadratic-narrow-collaboration-citation.jpg`.

The bosonic desktop frames are `bosonic-desktop-top.jpg`, `bosonic-desktop-scope.jpg`, `bosonic-desktop-embed.jpg` and `bosonic-desktop-collaboration-citation.jpg`. The embedded viewers visibly show totals of 6 and 7 pages respectively. These embedded counts do not satisfy the still-pending separate full-window PDF gates.

Each completed index check clicked the actual article navigation link named **Research**. `index-observations.json` preserves exactly three returned index observations, each at `https://aleckriebel.com/research/`, each with 50 rendered paper-title links and all three new titles. The accepted images are `quadratic-desktop-index-return-new-titles-settled.jpg`, the two `quadratic-narrow-index-return` frames, and `bosonic-desktop-index-return-new-titles-settled.jpg`. No stale 47-entry index was observed in these completed routes. No cache clearing, cache-busting query, source patch, browser settings change or reload was used to obtain that result.

## Exact remaining gates

The bosonic article still requires the 390-pixel top/plain-language, scope, embedded first page, collaboration and citation views, followed by its actual narrow Research-link return. The amplifier article still requires all desktop and narrow article checks and both Research-link returns.

All three separate full-window PDF checks remain pending: actual visible **Open PDF in a full window** links, exact final URLs, first-page desktop and narrow-fit screenshots, and visible viewer totals of the expected 6, 7 and 21 pages. No source-PDF rendering is being counted as browser evidence. All three actual support downloads remain pending: 37,068-byte quadratic ZIP, 114,329-byte bosonic ZIP and 6,952,578-byte amplifier TAR.GZ, each obtained through its visible file link in a fresh owned tab and then compared with the unchanged deployed asset. No support archive was downloaded or executed in this partial session.

## Browser interruption and visual exclusions

The last successful saved browser frame was the settled bosonic desktop index at **05:31:18.849 UTC**. The subsequent browser call timed out after saving that frame; later intended click and narrow-view actions did not reach the persistent action log. Four 30-second CUA timeouts occurred in total: two before explicit disk exhaustion and two after disk recovery. A separate bootstrap attempt reported `No space left on device` while writing kernel assets. Disk recovery removed that error, but metadata and direct own-tab access remained unresponsive in this agent's browser-control context. `browser-failures.json` preserves the observed failure sequence without inventing precise timestamps that were not retained.

All **22** screenshot files retain their exact browser `Tab.screenshot({})` output bytes. `screenshot-manifest.json` records their hashes, byte counts, actual JPEG dimensions and per-frame adjudication. **17** frames support the bounded positive findings. Five remain preserved and excluded:

- `quadratic-desktop-embed.jpg`: transient embedded PDF redraw; the revisit shows the rendered page.
- `quadratic-desktop-index-return-new-titles.jpg` and `bosonic-desktop-index-return-new-titles.jpg`: blank paint immediately after a large scroll; settled frames replace them.
- `quadratic-narrow-scope.jpg` and `quadratic-narrow-embed.jpg`: incorrect narrow filenames; actual frames are 2056 × 1146. The `actual390` replacements are the accepted narrow evidence.

The raw CDP viewport override did not persist through the initial HTML capture cycle. The documented browser viewport capability then produced the accepted stable 390 × 844 article frames. Actual dimensions govern each adjudication. No physical mobile device was tested; no unrestricted tiny-PDF readability, human review or full-window PDF PASS is asserted.

## Preservation and authorized concurrent changes

Before browser actions, the session hashed **125,037** existing files, covering all **444** public site files, shared scripts and configuration, paper sources, prior sealed manifests and their bound files. The baseline remains unchanged in substance as `preservation-before.json.gz`: its original uncompressed 39,401,330-byte content has SHA-256 `6864c4916897f7aefddf1ba2fbbd91a52fd400daaed65f7a488a704fe4336eba`. The gzip is 6,266,780 bytes with SHA-256 `06e9ee867d182ed7dc3f0d50b961612e8a79b1787f89b244dbd857fb260847a9`. Compression was verified losslessly before removing only the redundant, owned, unsealed original and failed partial gzip, recovering 33,134,550 bytes. No prior evidence or source file was removed by this session.

The after-check found **30,675** unchanged files, **94,361** absent files confined to the parent's exact 17 authorized disposable runtime directories, and one concurrently completed editorial research log. The runtime cleanup is documented in the byte-identical local copy `root-runtime-cleanup-receipt.json`; the original receipt SHA-256 is `cce7a52d0cf86a19d38fcb39200f58185f98cc472a97f789b3156400532a2656`.

The parent explicitly confirmed that `papers/23430906/reviews/editorial/RESEARCH_LOG.md` changed as part of the concurrent Gaussian editorial completion. It changed from 615 bytes, SHA-256 `cd3d2b43e471f8db4c11b6006ac1a74c3135afab8498f63dd19bd065d4fbf5a1`, to 2,186 bytes, SHA-256 `11a389e8639fa9a2f1b0c0f51a70e32eb3034a8a312dc99b259d880cbf159c1a`. The before baseline was not rewritten to conceal this delta. `preservation-after-runtime-recovery.json` retains the raw comparison; `preservation-delta-adjudication.json` classifies the authorized concurrent changes. No unexplained delta remains.

A final focused check rehashed **461** site/script/configuration bindings, including all **444** public site files; every one remains identical to the before baseline (`core-files-final-preservation.json`). This report does not claim that all 125,037 baseline files remain present after the parent's runtime cleanup.

## UI custody and pending cleanup

The working browser in this agent's namespace was **Chrome 2**, profile **Person 1**, extension instance `f3bb8740-9481-4d2a-95f4-a2cfff40edc5`. The sole created tab was **963520718**, corresponding to provider `393e6cd7-b57d-471c-a9fc-dd9eaec9aeca`. No user tab was claimed. The initial inventory of 10 user tabs is local under `private/`, excluded through the dedicated `.gitignore` created before that inventory. It is excluded from the public evidence manifest.

The protected Sheet tab **963520539** was never claimed, navigated or edited by this session. User tabs are unchanged as far as observed; a final inventory could not be obtained after control failed. The browser viewport reset and raw CDP override clear had completed before the successful bosonic desktop checks. A final reset confirmation and closure of own tab **963520718** remain pending parent recovery. This checkpoint does **not** claim cleanup complete.

UI ownership was released to the parent before **05:37:26 UTC**, and this agent made no later browser attempts. The parent confirmed that its separate browser context was responsive and took responsibility for the remaining checks and own-tab cleanup. This session made no site, shared script, manuscript, configuration, Git, deployment, redirect or spreadsheet changes; no child agents or external individual communications were initiated.
