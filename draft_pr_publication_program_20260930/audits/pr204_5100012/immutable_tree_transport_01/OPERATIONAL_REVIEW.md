# Optional immutable-tree transport: offline adversarial review

The bounded operational design is ready for Root review. **No API call, live adapter installation, helper phase, native mutation, ref move or production-cache seed was performed.** Every existing sealed helper remains unchanged. Actual public PR204 authority remains priority60; this transport supplies no mathematical, priority or publication clearance.

The adapter caches only `GET git/trees/<exact40lowercasehex>` with no body, in the fixed AlecKriebel/Math repository namespace. Every other request goes to the original transport exactly once: refs, commits, comparisons, PR metadata, blobs, contents/body requests, recursive/query trees, non-SHA trees, POST and other methods. Transport exceptions propagate. No request, including a mutation, is retried automatically. The adapter does not change credentials, quota headers or the original API implementation.

## Why patching h.api alone is insufficient

Offline reflection found six distinct module objects with aliases to one original API callable:

1. `h`: PR190 final scoped-merge helper.
2. `h.m`: PR179 final scoped-merge helper.
3. `h.m.m`: PR179 progress checkpoint.
4. `h.m.m.h`: PR177 final scoped-merge helper.
5. `h.m.m.h.m`: PR177 progress checkpoint.
6. `h.m.m.h.m.m`: PR152 scoped-merge base.

`h.lookup`, `h.changed_leaves` and `directory` are function objects whose global namespace is the PR152 base module. Its `directory` calls that base namespace's `api`. The PR177 `warm_selected_directories` submits `m.m.directory`, reaching the same base function through another module alias. `h.body_at` also uses base-global `api`, but its contents requests pass through uncached. Merely replacing the top module's h.api leaves the directory crawl unchanged.

`install_loaded` checks this exact six-module graph, shared original API binding, repository namespace, lookup/directory/diff function globals, warm-selected directory target, and native-cache dictionary identity. It checks all already-loaded native tree rows with the unchanged verifier. It then substitutes the same cache callable into all six module `api` attributes, which also replaces the base-global API lookup. It changes no directory, lookup, warm, changed-leaf, selected-current, byte-pin or validator function. An explicit restorer verifies and restores every original alias.

`c.selected_current` still fetches fresh commit metadata, warms the relevant directories and checks every selected path. `v.validate_caches` still invokes `h.m.verify_tree_object` over the exact same in-memory native-tree dictionary. The full repository changed-leaf comparison, original PR checks, foreign QUEUE byte reconciliation, actual selected-map verification and local-five guards remain unchanged.

`CALL_GRAPH_AND_SOURCE_PINS.json` records the observed binding graph and10 source-file byte pins. The optional runner patches only `v.load` in its own process: the existing loader first returns c,h,rv,n and disables its old monolithic cache writer; only then does the reviewed adapter install. This has not been run on a live helper.

## Cache identity and filesystem contract

Every fresh response and every cache hit is checked against the exact requested SHA. Validation requires nonrecursive `truncated:false`, exact API schema and repository URLs, canonical mode/type pairs, safe single-component UTF-8 names, unique names, canonical Git byte ordering, exact40hex OIDs and regular blob-size metadata. It reconstructs the complete raw Git tree record stream and recomputes the native SHA1. Full API JSON is retained, including entry URLs and sizes; cache hits return an independent parsed object rather than a stripped directory map. A SHA256 of canonical full API JSON additionally detects accidental corruption of metadata not included in the Git tree object.

The cache root must be a direct `private_...` child of this transport folder, owned by the current user, nonsymlink and0700. Directory descriptors with O_NOFOLLOW anchor file operations. Each per-SHA gzip file and lock must be owned regular0600 with one link when read. Symlinks, world-readable files, wrong owner/path, malformed envelopes, corrupt gzip, duplicate JSON keys, nonfinite JSON, wrong SHA or tree content fail closed. Existing invalid files do not cause a network fallback.

Each cache object is bounded to4MiB canonical JSON and1MiB compressed data. New cache data is capped at4,096 objects and24MiB compressed in total; no automatic eviction or relaxation occurs. Lock/inode metadata adds filesystem overhead, and failed requests can leave small lock files. This is a per-object cache, not another monolithic tree dump. Per-SHA threading and advisory file locks provide single flight across threads/process instances. A complete verified gzip is written to an exclusive0600 temporary file, flushed and atomically published by exclusive hardlink, then the temporary link is removed and the directory synchronized. Adapter readers hold the same SHA lock and cannot observe the transient two-link publication state. Existing final objects are never overwritten.

The fixture caches were temporary private directories inside this folder and were removed. The default production `private_tree_cache` directory does not exist as an artifact of this audit. Private cache contents must never be included in a public checkpoint allowlist.

## Checkable offline evidence

The tests use the eight authenticated original-custody nonrecursive tree API JSON objects. They extract the real directory/lookup/changed-leaf, warm-selected and native-validator function ASTs from the pinned existing sources into synthetic modules with a fake transport. They do not run a live helper or install the adapter into a live loaded graph.

Across four simulated separate processes/phases, the original transport receives32 tree calls without the adapter and8 with it: **24 saved,75% reduction in this fixture**. Every simulated phase still verifies the complete21-leaf original delta and all20 submitted native identities. Full cached API JSON equals the original objects. This is observed fixture savings, not a benchmark or guarantee for the current3,837-selected candidate.

The latest `OFFLINE_TEST_RESULTS_03.json` and `OFFLINE_EXTRA_RESULTS_03.json` record27 passed controls. They cover all six aliases and restoration, native OID tampering despite a forged envelope checksum, malformed mode/path/order/URL/request identities, truncated responses, gzip corruption/expansion, private permissions, symlink files/root, outside cache paths, full JSON checksum/duplicate/nonfinite controls, exact noncache passthrough,16-way concurrency, two cache instances sharing a single fetch, exclusive publication races, file-count budget failure, invalid fresh responses, closed-cache rejection and failed GET/POST propagation without retry. Earlier first-pass receipts are retained as history.

## Limits and remaining Root decision

The cache cannot replenish shared quota. A cold verified tree still needs one original authenticated GET, and every mutable/body/commit request stays uncached. New immutable trees require fresh misses; strict future schema changes, unsupported path encoding or bounds exhaustion stop the phase for review. A stale expected MAIN lease remains stale: the original fresh ref/ancestry/parent checks still decide whether the unreferenced prepared package commit can be used or requires a new generation. No cache hit is current-MAIN authority.

Native SHA1 is the existing Git identity protocol, not a newly strengthened cryptographic premise. The canonical JSON checksum is corruption detection, not a signature. A user with the same UID can rewrite cache metadata and recompute that checksum; critical Git tree fields still require the requested native content hash. Blob `size` metadata is not part of Git's tree hash and remains informational; existing blob/body identity verification stays fresh and unchanged. The cache is not a source of scientific conclusions or body bytes.

The installer is deliberately restricted to the observed graph. Already wrapped/divergent APIs, another repository, changed global bindings or future unreviewed loader architecture are rejected rather than guessed. Current helper phases use one loader call. Future lifecycle/helper changes require another binding review. Advisory locks, dirfd/O_NOFOLLOW and atomic hardlinks require the tested POSIX filesystem behavior; no Windows adaptation is claimed.

After Root reviews and accepts these exact files, an optional invocation is:

`python3 -B <absolute-run_with_tree_cache.py> --root-reviewed <absolute-existing-helper.py> verify package75_01 execute`

The runner accepts only the three sealed existing PR204 science/priority/package helpers and explicit prepare/verify/accept/sync phases. It creates no ref update capability; prepare retains its existing authorized native-object operations, which are forwarded without caching or retries. The runner restores all API aliases afterward and prints only compact transport counts. Root must perform normal fresh verification and the separate expectedSHA/forcefalse CAS; this audit has executed neither the runner nor any helper phase.

**Operational verdict:** ready for Root review as an optional transport optimization. Production efficacy and the actual package75 acceptance remain unverified here. No mathematical/publication promotion follows from these offline checks.
