# Independent native transport review 1

Verdict: **CHANGES_REQUIRED — 3 mandatory findings and 1 optional durability finding.** Review completed on 2026-10-14 UTC. The supplied author PASS label was not treated as evidence. No production mutation, repair, Git mutation, or outside communication was performed.

The claim under review is that the PR623-only native adapter can continue the recovered initial draft 23356540, transmit only the two reviewed artifacts, preserve the kit's exact publication verification and receipt semantics, and avoid repeated uncertain writes. The success criterion includes binding the executed code and transmitted bytes to their pins, accepting the real service's legitimate published representation, and preserving fail-closed behavior on unsupported representations and ambiguous outcomes. Publication itself was excluded from this reviewer’s authorization.

## Mandatory F1 — the disk pin does not bind the loaded kit

**Priority P1.** `native_transport.py:22–26` imports `zenodo` before `pinned_inputs()` hashes `KIT_PATH` at lines 59–60. The module, superclass, functions, and globals already loaded in memory are the ones used afterward. Hashing the current pathname neither establishes which bytes were imported nor rejects an existing `sys.modules['zenodo']` entry. The hash function also comes from the module whose provenance has yet to be established.

`import_binding_probe.py` compiles an isolated stale kit snapshot with an altered `run` function, retaining the genuine reviewed digest and manifest-loading functions. Its `__file__` is the expected kit path, and the real shared file remains the genuine pinned bytes. The unchanged adapter then imports that loaded module and `pinned_inputs()` succeeds. Calling its kit function executes the unreviewed implementation. This models source read before a concurrent restoration to reviewed disk bytes, or a stale module cache; it does not edit the shared kit or make a network request.

`IMPORT_BINDING_PROBE.json` records the accepted disk hash `a91f961b…`, different loaded-source hash `e787a3ad…`, accepted two files, and execution of the altered function. All these checks are active independently of Python assertions.

**Required outcome:** execute the exact byte snapshot whose SHA-256 was checked, under an isolated module identity, while preserving the kit's intended absolute root/state paths. A pathname hash taken before or after an ordinary import remains a race. Verification must fail before imported unreviewed top-level code can run. The adapter's launch and the manifest reads need equally explicit byte provenance; no repair is supplied here.

## Mandatory F2 — a legitimate published OAI PID blocks readback and receipts

**Priority P1.** At `native_transport.py:336–340`, `get()` permits only an empty PID map or the `doi` key. The native publication service also creates an `oai` identifier. This is not an unexpected rich user metadata field.

The independently downloaded primary source establishes the chain: Zenodo's provider configuration copies Invenio's persistent identifier configuration; Invenio requires the enabled OAI scheme; the publish component creates missing required schemes; `OAIPIDProvider` emits `oai:{configured-prefix}:{record-id}`. Invenio’s primary test `test_oai_pid_default_created` starts with `pids={}` and explicitly checks `record.to_dict()['pids']['oai']` after publication. See [Zenodo providers](https://github.com/zenodo/zenodo-rdm/blob/master/site/zenodo_rdm/providers.py), [Invenio PID configuration](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/config.py), [publication PID component](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/components/pids.py), and [OAI provider](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/pids/providers/oai.py).

The parent’s separately obtained, filtered native published-record calibration confirms this deployed shape: its own earlier record 23331709 has both an exact DataCite DOI and `{'identifier': 'oai:zenodo.org:23331709', 'provider': 'oai'}`. This reviewer did not read that other record live. `PARENT_CALIBRATION_BINDING.json` binds the exact bytes supplied by the parent, SHA-256 `0cefe0f0…`, to the parsed evidence in one read.

The independent `legitimate_oai_postpublication` control adds only the exact expected OAI PID to a successful offline publication. One publish POST occurs and the model is published; the subsequent actual adapter/kit readback raises `Unsupported native persistent identifiers` and saves no publication receipt. The expected DOI is present and correct. Subsequent inspect would encounter the same rejection. The supplied mock backend hid this issue by generating only the DOI.

**Required outcome:** recognize and strictly validate the automatically generated OAI identifier/provider for this exact ID, alongside the version DOI. Preserve rejection of unrecognized PID schemes and incorrect IDs/providers/clients. Confirm normal and lost-response receipt recovery against the complete legitimate PID map.

## Mandatory F3 — upload rereads a mutable path after its byte check

**Priority P2.** `upload()` hashes `entry['path']` at lines 380–381, then performs multiple native reads and initialization/journal operations. At line 406 it hands the same mutable pathname to the kit. The kit stats it again and opens it later while sending content. No immutable checked byte snapshot or protected file descriptor binds that send to the earlier digest.

The independent `source_path_swap_after_validation` control copies the reviewed files into this review's ignored temporary area. After the early validation, immediately before the simulated PUT reads that path, it replaces one byte without changing file length. Its backend computes the committed MD5 from the actual transmitted bytes rather than pretending the original checksum still holds.

The adapter sends unpinned content with SHA-256 `f0fda75a…` instead of the reviewed PDF's `05c6bcae…`, then sends a commit POST. Only the commit acknowledgment detects the differing MD5. This is reproduced under normal Python and `-O`. No original input or production file was changed.

The final guards prevent publication of the changed file in this control. That does not satisfy the authorized upload boundary: the user authorized the exact reviewed PDF/ZIP, and different raced bytes have already been sent and committed to the draft. With no delete/reupload route, this also leaves an operationally blocked draft requiring new reconciliation.

**Required outcome:** capture the actual payload once, validate size, SHA-256 and required MD5 on those exact bytes, and send only that validated snapshot. A second pathname hash followed by another pathname open merely moves the race. Exercise both path replacement and modification during streaming; preserve bounds and no automatic retry semantics.

## Optional O1 — journal replacement is atomic, not power-loss durable

The journal delegates to the kit's `save_state`, which closes a temporary file and uses `os.replace`, without `fsync` of the temporary file or parent directory. The independent control observes zero `fsync` calls across six journaled mutations. The lock and journal both have mode 0600, and a second local lock is rejected.

The process-restart control creates a genuinely new client instance over the saved journal after a lost content response and confirms the write count remains two: no second PUT or initialize occurs. That supports ordinary process-interruption recovery when completed filesystem writes remain available. It does not establish survival across kernel crash, power loss, or storage rollback. An acknowledged rename may still be lost on such failures, allowing an attempted marker to disappear. No destructive power-loss test was conducted, and this report does not claim one.

The optional repair is to make pre-request intent persistence genuinely durable, or to state the narrower process-interruption guarantee explicitly. Registration and final local receipt persistence use the same kit storage primitive, so their stronger durability wording should remain consistent. The parent requested no waiver of this finding.

## DOI reservation question resolved independently

For this public initial record, a separate reserve-DOI endpoint is **not required** by the inspected primary publication implementation. Zenodo config enables DataCite and supplies prefix `10.5281` and format `{prefix}/zenodo.{id}`. Its provider list selects DataCite for DOI by default and retains Invenio's required DOI setting. The publish component computes missing required schemes from draft and record PID maps, creates them, reserves them, and schedules asynchronous registration. Thus `pids={}` on this public draft leads to version DOI `10.5281/zenodo.23356540` during publication under that configuration. See [Zenodo configuration](https://github.com/zenodo/zenodo-rdm/blob/master/invenio.cfg), [PID manager](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/pids/manager.py), and [DataCite provider/client](https://github.com/inveniosoftware/invenio-rdm-records/blob/master/invenio_rdm_records/services/pids/providers/datacite.py).

Assignment and queued registration are distinct from successful external DataCite registration and DOI resolution. The kit correctly records resolver status separately after confirming publication. Publication of this own draft was not attempted, so this report does not present a mock result as proof of actual registration. The documentation's reserve endpoint allows prepublication reservation; it does not override the required-scheme creation mechanism during publication. The generic documented example has a restricted record and empty PIDs, a different boundary case.

## Verified controls and unchanged publication binding

- All supplied 25 tests passed under normal Python and `-O`. Their temporary files were redirected into this assigned review, with no shared bytecode writes. The passing tests are evidence of their modeled lifecycle, not proof of undocumented production behavior.
- Six materially additional control families ran under normal and optimized Python: legitimate OAI postpublication failure, path swap, fresh-client restart, lock/sync behavior, 20 malformed mutation acknowledgments, and four hostile DOI/provider/client/extra-field cases. The hostile acknowledgments and PID cases were rejected without production writes.
- The endpoint allowlist limits writes to the exact draft/file paths and permits neither create, metadata PUT, deletion, edit, nor new version. Direct request mutations require active saved operation intent. Supplied controls substantiate no repeated mutation after uncertain initialize/content/commit/publish outcomes, exact metadata/rich-field rejection, size/MD5/downloaded SHA-256 verification, bounded HTTP-200 content reads, no redirect following, and truthful `receipt_saved=false` after local receipt failure.
- Independent live reads made **two GETs only** against own draft 23356540: native item and file collection. Metadata canonical SHA-256 remains `16618fd4…`; status is draft, unpublished, `pids={}`, and zero completed or pending files. `LIVE_READONLY_CHECK.json` contains only filtered evidence, without credentials or account/grant identities.
- All **45/45** final-publication-gate inputs match, both initially and at final recheck. All **29/29** native candidate files equal original PR commit `947442c091ae617804c6a0d07b98ff2c50368798` and their ZIP candidate entries. The ZIP has 88 unique members, its 87-item inventory passes the frozen integrity verifier, and its embedded PDF exactly matches the supplied reviewed 79,172-byte PDF. The 226,383-byte ZIP and PDF retain their full supplied SHA-256 pins.
- The transport is absent from the delivered ZIP/PDF. The working branch is `main`. The author runtime and full primary-source downloads are ignored; the only preexisting author runtime file is an empty mode-0600 lock. There was no upload/publish journal. No helper, proof, paper, metadata manifest, shared kit, index, branch, remote, or production draft was repaired or mutated.

One archive-check command was initially issued from the wrong working directory and created an empty root output file; the command failed before reading the archive verifier. The reviewer removed exactly that empty file and reran successfully inside the assigned review. No publication or existing repository file was changed.

## Exact remaining gap

The three mandatory issues must be repaired and reviewed by a fresh independent adversary before live execution. Optional O1 remains explicitly open. After code acceptance, deployed initialize/content/commit acknowledgments, pending-content readability after ambiguous PUT, this draft's exact final native representation, and actual DOI registration/resolution remain observable operational boundaries. The current implementation stops rather than retrying uncertain writes when pending content is unreadable; that safe behavior is verified in the model but its live availability is unknown.

The unchanged mathematical/publication packet remains byte-bound to the accepted prior review; this review neither reopens nor expands its mathematical conclusions. Review completion estimate: **100%**. Native execution authorization readiness: **blocked by findings**, with no live writes attempted.
