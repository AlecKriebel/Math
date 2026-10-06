# PR311 independent GWS append retry audit

Verdict: the pinned generic append route does not automatically retry an ordinary HTTP error, timeout, or ambiguous transport failure. The library-level `send_with_retry` helper is not on this route. A single CLI invocation is nevertheless not a proof of one HTTP transmission or unconditional exactly-once append processing: the default HTTP redirect layer can replay the POST on 307/308. This is a source-level conditional countermechanism, not evidence that Google Sheets emits such a redirect.

The coordinator's bounded decision is consistent with this audit: retain generic `values.append`, record one immutable invocation attempt, perform fresh complete read-only reconciliation, and accept success only when the whole observed poststate equals the prestate plus exactly one intended row. Do not infer “one transmission” from the invocation count or receipt. This audit does not approve or verify the coordinator's entire operator implementation, a sheet mutation, or the actual tracker state.

## Scope and independence

Criteria were frozen at 2026-10-04T20:49:07.707199+00:00 before reading candidate source. Frozen criteria SHA256: `74f7611786658cf01bf3ba1c7f05b4085fbcad08da8c9afba225abdae9f4419c`. The bounded operational research question was whether the installed CLI's generic `gws sheets spreadsheets values append` execution can semantically repeat a mutating POST after uncertain processing. No mathematical PR review was performed.

All writes were confined to this new dedicated private directory. No GWS command, sheet read/write, installation, credential/configuration read, Git mutation, mode change outside this directory, or communication outside the agent tree was performed. Public primary-source HTTP GETs retrieved source archives, an RFC, manifests, and tag metadata. Each controlled subprocess records actual argv, cwd, UTC start/end, exit code, full stdout/stderr, sizes, and hashes; tool display truncation does not truncate retained streams.

## Exact versions and provenance

The installed binary was read without execution at `/Users/alec/.nvm/versions/node/v22.16.0/lib/node_modules/@googleworkspace/cli/bin/gws`. Its independently measured size is 15,371,280 bytes and SHA256 is `0f27b8b0815bf09cdf95da48d3c604f05ceb8f16bf5c9f0ba355b1f957cdd47e`, matching the coordinator's pin. Its claimed installed version 0.22.5 was supplied by the coordinator; no version command was run in this subtask.

The [official tag reference](https://api.github.com/repos/googleworkspace/cli/git/ref/tags/v0.22.5) independently resolves v0.22.5 to commit `705fb0ecac6f4249679958f6325b809b63fdde17`. Both source package manifests declare 0.22.5. The coordinator's six primary-source captures were independently hashed against their supplied execution metadata, then copied into `imported_source` for the sealed evidence set. The lockfile pins reqwest 0.12.28, hyper 1.9.0, hyper-util 0.1.20, h2 0.4.13, tower 0.5.3, and tower-http 0.6.8. All six fetched crate archives exactly match their registry checksums in that lockfile.

This is a source audit tied to a separately measured installed binary identity. It is not a reproducible build or disassembly proof of source-to-binary equivalence. The published tag's normal feature configuration is distinguished below from a hypothetical build with additional dependency features.

## Reachable generic route

The installed `run.js` makes one `spawnSync` call for the existing binary (L26-29). It has a missing-binary auto-install branch (L13-24), which is excluded by the measured existing binary and was not exercised. It contains no retry of the spawned binary. A copy of this static source is included in the evidence.

CLI `main.rs` first offers dispatch to the Sheets helper (L203-208), then resolves the generic method and calls `executor::execute_method` once (L281-301). The helper only intercepts top-level `+append` and `+read`; the generic `spreadsheets values append` tree returns false (Sheets helper L97-195).

Executor request construction chooses POST for a POST Discovery method (L171-179), sets OAuth bearer authentication (L184-187), and serializes the supplied JSON body (L230-232). The generic executor creates its own client and executes `request.send().await` directly at L439-455. A failed send propagates an error immediately. Non-success status returns `handle_error_response` at L466-475. A response-body read failure propagates at L493-496. No application-level retry is entered in these cases.

The re-exported library client builder only adds default headers and a 10-second connect timeout before `.build()` (library client L28-43). It does not install the separate `send_with_retry` helper. That helper, if explicitly called elsewhere, would retry 429, `is_connect()`, and `is_timeout()` errors for three loop attempts plus a final attempt (L66-111). Its existence cannot be attributed to generic append's execution path.

## Pagination boundary

The executor's loop is pagination, not an error-retry loop. It continues only after a successful JSON response when `page_all` is true, `nextPageToken` is a string, and the page limit has not been reached (executor L314-325, L498-513). Otherwise it breaks (L526). The normal configuration sets `page_all` from the explicit `--page-all` flag, default false (main L313-319; default test L548-552).

With `--page-all` absent/false, even an unexpected `nextPageToken` cannot trigger a second generic send. The audit's single logical-request conclusion is scoped to that setting. With pagination enabled, source permits another POST after a success; subsequent pages omit the JSON body because body attachment is conditioned on `pages_fetched == 0` (L203-235). The audit does not declare pagination safe for append or assume a particular server response schema.

## HTTP-layer mechanisms

| Family | Exact mechanism and evidence | Result and boundary |
|---|---|---|
| Reqwest default classifier | Client defaults select `retry::Builder::default` (client L310-311); retry source L192-199 selects `ProtocolNacks`, no budget, maximum two retries in addition to the initial request. L424-429 and L453-461 classify only matching errors, not response statuses. | No default 429, 5xx, ordinary connection-loss, or ordinary timeout retry. A successful/failed final response does not enumerate transmissions. |
| HTTP/2 protocol NACKs | `retry.rs` L298-312 matches only remote GOAWAY with NO_ERROR or remote RST_STREAM with REFUSED_STREAM. JSON bodies are replayable (request L447-456; body L153-157, L196-200). | If HTTP/2 is enabled, up to two additional sends are possible under these protocol signals. They represent safe unprocessed requests for a conforming peer, not a retry after an arbitrary uncertain commit. |
| GOAWAY's processed-stream boundary | h2 streams source L724-737 applies the remote GOAWAY error to streams whose IDs exceed last_stream_id. [RFC 9113 §8.7](https://www.rfc-editor.org/rfc/rfc9113.html#section-8.7) permits retries for those streams and REFUSED_STREAM because processing is excluded by the peer's protocol guarantee. | Safety depends on truthful, conforming protocol signaling. This audit does not turn an arbitrary server's false NACK into an exactly-once guarantee. |
| Source build features | CLI and library manifests both set reqwest `default-features=false`; selected features are JSON, native-root Rustls, plus CLI stream/socks. Lockfile reverse references show these are the only reqwest users. Reqwest's HTTP/2 feature is separate; HTTP/3 is also unselected. TLS ALPN includes h2 only under reqwest's HTTP/2 cfg (client L823-842). | The normal pinned-tag build does not enable reqwest HTTP/2 or HTTP/3; its classifier branches for those protocols are compiled out. A binary build with additional features would require the conditional analysis above. Mere presence of h2 elsewhere in Cargo.lock does not enable reqwest's HTTP/2 cfg. |
| Hyper-util unstarted cancellation | Default `retry_canceled_requests=true` (legacy client L1033-1035). Send loop retries only a recoverable original request on a reused connection (L248-269, L324-338). Hyper HTTP/1 reports `message=None` once dispatched, and `Some(req)` only for an unstarted queued request (dispatch L658-674). | Recovery is restricted to an unstarted request; it does not retransmit a started ambiguous append. The generic executor constructs a fresh client per logical request, so it does not inherit the helper's shared pool. Connection checkout retries also occur before sending the application request. |
| Redirects | Reqwest's default redirect policy is limited(10) (redirect L160-164), wrapped outside its retry service (client L1020-1026). Tower-http changes POST to GET on 301/302, uses GET on 303, and preserves method/body on 307/308 (follow_redirect L272-327). Reqwest supplies body cloning for those redirects (redirect L349-352). | 307/308 can cause another actual append POST. If a server committed the original append before such a redirect, another processing append could occur. No application idempotency/deduplication guard is introduced by these sources. This conditional countermechanism is not evidence that Sheets issues a redirect after commit. |

TLS/TCP retransmission of bytes within one connection is not itself another application request; sequence/protocol handling must not be confused with POST processing. The evidence does not justify a universal numerical bound on all transport attempts from the application's one send call.

## Operational implication and exact remaining gap

The route “direct `.send()` therefore exactly one HTTP transmission” is refuted by the reachable redirect mechanism and, in feature-enabled builds, protocol retries. The route “no application retry therefore unconditional exactly-once append for any server” is also unsupported. Closing it would require an unsupported server-processing assumption or a server idempotency guarantee absent from the audited path. These routes should remain closed unless materially new evidence establishes such a mechanism.

The strongest verified finding is narrower: for the pinned tag's generic nonpaginated execution, ordinary uncertain errors are returned rather than automatically retried by the CLI/default classifier; automatic safe unstarted recovery and automatic redirects must still be distinguished. One invocation plus a complete exact pre/post sheet delta can establish one observed new tracker row at reconciliation time, with the scan's completeness and concurrent-writer assumptions stated. It does not prove all-time exactly-once semantics or absence of all additional transmissions.

The coordinator confirmed that its receipt will claim one CLI append invocation, use an immutable one-shot attempt marker, and stop unknown outcomes for fresh read-only reconciliation. It will require the exact old rows plus exactly one intended new row in a full postscan. Those are coordinator-reported controls, not controls implemented or reviewed in this source-only subtask.

If a future task requires duplicate-row prevention under arbitrary replay while retaining GWS, a deterministic `values.update` to a verified blank fixed row with the identical payload is a smaller conceptual alternative than append: replay changes the same cells. It requires an exclusive-writer/empty-row precondition and permission to use fixed-range update. It must not overwrite another writer's data. The coordinator explicitly retained append for this task; this audit neither changed that choice nor performed a write.

Audit completion is 100% for the bounded source question. The remaining gap is source-to-binary build attestation and actual server/tracker behavior; neither was in the authorized source-only scope. Full evidence integrity is recorded in `evidence_manifest.json` and its detached `seal.json`.
