# JC incorporated-article redirect implementation

Implementation preparation is **100% complete**. The new one-paper helper and final dry-run are ready for root code review. No redirect was applied or pushed.

Helper: `redirects/publish_jc_incorporated_article.py`.

Final reviewed candidate: `dry-run-final/plan.json`, based on fresh `origin/main` commit `1c46522fef00fcd3d1f05b38021b90c81b9c1ee3`.

The generic `publish_verified_article_redirects.py` is unchanged. This helper does not permit topic-based matching or weaken that helper's exact-edition rule. It handles only root's separately authorized incorporation decision for record 22089373.

## Exact proposed changes

Root authorized narrowing the three-path maximum scope to two changed paths after the fresh-origin index was found to contain no corresponding article href. The final candidate changes only:

1. `docs/papers/s-tc-jc-sharp-boundary/index.html`: a small HTML redirect with the exact canonical destination, immediate meta refresh, ordinary current-paper links, and a statement that the earlier result was incorporated into the later paper. The fallback retains the exact historical `href="./paper.pdf"`, labelled as the unchanged ten-page edition with narrower scope.
2. `docs/sitemap.xml`: removes exactly the old article URL. An XML comparison verifies that the ordered remaining entries are unchanged.

The actual diffs are `article.diff`, `sitemap.diff`, and the combined `dry-run-final/proposed.patch`. Complete proposed bytes and fresh-origin bytes are under `dry-run-final/after/` and `dry-run-final/before/`.

`docs/index.html` has zero corresponding article hrefs at this parent. It is unchanged, with SHA-256 `47e1007a933f2b3cd8d55c4a08379bf284698c751462759c5b812ebb3defe073`. No entry was invented. Historical PDF hrefs before/after are identical (empty for this article at this parent). Local and remote index bytes are captured separately; equality between those states is not required by the helper.

The remote docs tree contains 254 entries before and after. Its planned object map differs on exactly the two paths above. The historical PDF blob is unchanged, and its SHA-256 remains `65f5a54f6858b091546bc2221cb36d77bf5e24722bb79d6420b98f429dadc810`. Its existing `SHA256SUMS.txt` lists only that PDF and remains valid and unchanged.

## Gates and execution behavior

The helper requires all of the following before preparing or executing the change:

- Exact root lineage-disposition hash and status, record, source, destination, permitted paths and historical preservation conditions.
- Exact accepted lineage report/decision and unchanged original pending receipt.
- Existing root scientific clearance and target promotion/browser PASS, bound publication/promotion hashes, accepted browser receipt and its 33-page paper/7-page reader observations.
- Current target HTML and PDF matching root's accepted hashes; accepted live receipt entries for those exact URLs.
- Fresh direct HTTP 200 and exact-byte checks of the live target HTML and PDF.
- Fresh-origin old HTML SHA-256 `e6dadc68e6cecf64b2b9ac3d95c55a18d1a455c356b9d6da0797e17ff2faaedf`, historical PDF SHA-256 above, and identical local old article/PDF hashes.
- Shared branch `main`, expected repository and remote, no inherited Git directory/index overrides, and repeated evidence/origin race checks.

Execution additionally requires the root-reviewed dry-run plan. It refuses any changed script, parent, evidence, source bytes, output bytes or path set. It fetches fresh `origin/main`, constructs only the approved blobs in a temporary separate index, verifies the complete docs object map, creates a commit with that fresh parent and makes an ordinary **nonforce** push. A remote race after the final check is rejected by Git. It persists the prepared commit and push intent before sending, so an ambiguous transport result can be investigated without assuming failure or retrying automatically.

The helper never writes the shared working-tree docs files, the shared index, local `main` or HEAD—even during execution. This avoids overwriting the shared checkout's prior checkpoint state. Its preservation receipt compares all local docs hashes, the shared index hash, HEAD bytes and revision, and branch before and after.

The root lineage file itself is pinned. If root revises that existing file, the helper will deliberately stop until the new authorization is reviewed, the constant updated and a fresh dry-run produced. A separate narrowing disposition does not alter the pinned maximum-scope authorization.

## Verification completed

The final helper passed an AST syntax parse and a complete dry-run. An earlier dry-run was followed by two small audit improvements (sitemap XML comparison and pre-push intent receipt), so only `dry-run-final` is bound to the final helper hash. Both dry-runs performed no Git-object writes, commit, push, site edit, browser action, Sheet action or deployment.

The final dry-run fetched the live target at approximately 04:20:29 UTC on October 25:

| Payload | SHA-256 |
|---|---|
| Target HTML, 20,308 bytes | `ab60bf2313a43fcd0033fa1d450464f16dee03e6cc2ac9d37e3eeb1f1b8f5a1d` |
| Target PDF, 245,674 bytes | `ae01c6beba01da624bba7060e9f3adfce74a5e568e5808f4db168300d7873084` |

`dry-run-final/shared-state-preservation.json` confirms unchanged shared index, local HEAD, branch `main`, and every local docs file. `origin-docs-before.json` and `planned-docs-after.json` prove that all other remote docs objects and the historical PDF remain unchanged in the proposed commit.

The execute branch, commit creation and push have **not** been exercised. Post-push Pages build and live redirect/browser verification remain root work. No new scientific pass, priority or journal conclusion is made.

After reviewing the helper and exact diff, root can execute from the repository root:

```sh
python3 research_website_catalogue_20261024/redirects/publish_jc_incorporated_article.py --execute --approved-plan research_website_catalogue_20261024/redirects/jc-incorporated-article-implementation-20261025/dry-run-final/plan.json
```

If origin/main advances first, execution stops. Produce a new dry-run in a fresh owned output subdirectory and review its exact parent/diff before execution.

`READINESS.json` records the checks and scope. `SEAL.json` authenticates the helper, readiness files, final plan, exact diffs, snapshots and preservation receipts.
