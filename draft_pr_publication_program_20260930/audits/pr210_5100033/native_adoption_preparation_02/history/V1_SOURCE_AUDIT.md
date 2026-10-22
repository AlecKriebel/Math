# Independent adversarial audit of PR210 frozen native adoption sources

Final decision at 2026-10-17 03:38 UTC: **REQUIRES_REPAIR**. Exactly two mandatory contract defects remain in this frozen version. Neither finding establishes any change to an existing publication or native reference. This is a source-only report, not Root acceptance, scientific validation, an actual input manifest, or execution authority.

The audited source manifest is 3658 bytes / SHA256 `66cc2152310d29f7205f071956f35d88db57e7cee23d7b2912cf603dfd18aca9`, selecting 16 payloads totaling 160701 bytes. Model 34675 bytes / SHA256 `ff8d79fc245fcf55ac1d109ece1d3c5cd9c5f28bd51060e7efbc750ec41d2c4d`; executor 28745 bytes / SHA256 `c4de73154c88d21c7ef13ee36575d63505470c44904512d0883f2664aa547a39`; core 4719 bytes / SHA256 `c71575a580c43fea8d302c978e0b6c340a16474779ffeb4671e77b967cf6e2ce`.

The claim tested is a future single-parent adoption100 commit over fresh MAIN, with 52 completed / 36 published or adopted / last 210 / cursor 211 / goalFalse, preserving the already-merged original PR210. Success also requires the supplied exact Root gate and receipt chain; bounded one-use immutable effects; the original stable writer lock before candidate/local effects; full native scope and new-body verification; preservation of own 47 / shared audit / whole QUEUE and foreign tuples; and actual external Root CAS before local sync. A trusted invocation and externally supplied Root pins are assumptions. Peer PASS, preparer provenance, and self-tests supply no authority.

## M1 — Mandatory: GitHub CLI transport does not pin the host

Exact executor locations: line138 constructs the API argv; lines138-140 add input flags; lines188-189 call `subprocess.Popen` without an explicit environment. No `--hostname github.com` is present. The route firewall at lines120-128 constrains repository-relative paths but does not constrain the host chosen by `gh`.

Local `/opt/homebrew/Cellar/gh/2.85.0/bin/gh help environment` was read, without invoking `gh api`. Its GH_HOST description identifies it as the hostname selection when none is provided. Python `-E` changes Python's own environment interpretation and leaves `os.environ` available to subprocesses. An independent control executes the unchanged `run_bounded` with a harmless Python child and synthetic `GH_HOST=synthetic-audit.invalid`; that child observes the value even under `-E -S -B -P`.

Thus exact source/manifest/gate pins plus an allowed `git/blobs`/`git/trees`/`git/commits` route do not prevent a future POST from targeting a different configured GitHub host. This violates the requested host boundary. Root's separate native CAS remains a separate barrier.

Required fix: add `--hostname github.com` explicitly to every `gh api` dispatch, centrally in `API.__call__`. Verify actual argv through an ordinary synthetic transport fixture with an inherited hostile GH_HOST. Preserve the route firewall, expected OID, exact durable intent and one-use behavior. An external runtime-environment promise does not repair this source contract.

## M2 — Mandatory: candidate immutable effects do not check the pinned lock

Exact executor locations: `candidate` begins at line361; its complete per-effect guard is lines371-378. That guard reloads source/Root envelopes, checks local preimages, reads MAIN and refreshes PR identity, but never acquires `WriterLock` or checks its stable identity. The guard precedes object POSTs at392-393,398-399,401-402. `WriterLock` is defined at313; its sole caller is `sync` at439. Model line331 validates only the manifest's lock description against a constant.

The independent AST control verifies `sync` is the sole WriterLock caller. Under the frozen candidate path, an absent/replaced/unlocked real lock therefore does not stop candidate object creation. Existing local-five writes do acquire the lock. This finding concerns the additional candidate-effect requirement, which Root explicitly confirmed. README line19 says the pinned lock is checked before each effect, exceeding the implementation.

Required fix: acquire the original pinned WriterLock for candidate creation, retain it across candidate object effects, and include `lock.check()` in the candidate per-effect guard immediately before dispatch. Retain the fresh source/Root/preimage/PR/MAIN checks. Missing lock, wrong inode/device/mode/payload, replaced ancestor, or lock contention must cause zero immutable POSTs. Test via exact copied source and a synthetic transport boundary. Never replace or recreate the real lock inode.

## Strongest verified results

All 16 payload pins and readonly modes match the supplied frozen manifest. The 3 predecessor source pins match their provenance; both adaptation patches exactly equal recomputed full old-to-new diffs; all 12 declared unchanged executor AST blocks match; the core is byte-for-byte unchanged. These checks validate provenance without inheriting predecessor acceptance.

The full model/executor/core/schema/docs, patches, provenance/reference/exception JSON, preparation log and self-test source/result were inspected. Independently authored `AUDIT_TESTS.py` produced 141 passing assertions in `CONTROL_RESULTS.json`. Four assertions positively demonstrate M1/M2; control PASS does not mean the adoption contract passes.

The actual state and full verifier were exercised with an ordinary injected GET-only observer and independently constructed in-memory native objects. Checks cover the single fresh parent; full scope/selected bodies/foreign tuples; fixed author/parents/candidate; exact merged timestamp/ancestry; a valid-body intervening ascending checkpoint; selected-body forgery; a late MAIN move; after-ref readback; and no observer retry after uncertainty. Protected own 47 / shared / whole QUEUE remain opaque without unchanged-body fetches. Foreign executable/symlink/gitlink/empty-directory tuples are preserved.

Other controls cover malformed/duplicate/nonfinite JSON, integer/float distinctions, unsafe paths, canonical phase markers, exact 11 custody exceptions, all 127 paths of the pinned current public declaration, route refusal, bounded stdout/stderr and process reaping, readonly sources/symlink refusal, owned lock mode/inode replacement, journal/record reuse refusal, and exact pre/post local resume boundaries. Filesystem checks run exact source copies only in owned disposable synthetic trees; fixtures were removed. No target source/function/module or transport was monkeypatched.

Source inspection found no reference/PR/publication/tracker writer route, mutation retry loop, or current-five write before externally pinned actual Root CAS plus full native verification. Candidate reservation and exact request/expected-OID intents precede dispatch. Uncertainty stops mutation. Sync uses per-file atomic installs, exact pre/post resume boundaries, all-five postimage checks and actual-ref readback before its pointer. These are source deductions plus bounded synthetic evidence. Live transport failures, real CAS/sync, Root receipt truth/freshness/sequentiality, science and actual packet contents remain untested here and require Root checks.

No additional mandatory or optional defect is asserted. Distinct receipt paths alone are not accepted as fresh independent sequential review; Root must accept the exact evidence substantively. Public file extensions alone do not establish publication suitability: the finite allowlist remains a Root-reviewed content selection.

## Scope and remaining gap

Provider API calls: 0; local Git calls: 0; no outreach. No real MAIN/PR/native/service write, current view, stable lock, sync, pointer, or actual manifest/gate was created or modified. Only this owned audit folder was authored; no synthetic fixture is retained in `_private`. Sources were hashed again after controls. Git commit/push and any publication remain Root-owned under the delegated scope.

`PUBLIC_MANIFEST.json` selects exactly this report, reproducible script, result JSON and research log by bytes/SHA256. `EXTERNAL_SEAL.json` seals that manifest outside its selection. This V1 report grants no clearance to changed V2 source; renewed independent audits must bind the new exact version/packet. Source-audit completion estimate: 100%. Overall adoption remains gated by both repairs, actual exact-packet/native/scientific/priority/custody/publication/tracker and sequential whole-package evidence, actual Root acceptance and independent verifier, then external Root CAS.
