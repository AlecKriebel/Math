# Independent adversarial review of metadata editing

Final review checkpoint: 2026-10-10T18:42:29Z. Reviewer: independent subagent,
scoped to `metadata_updates.py`, its `zenodo.py` integration, and offline tests.
Best-guess completion of the scoped adversarial review: 100%. All concrete
defects identified in this review are repaired at the checked hashes below.
Live mutating API validation remains outside this review's authorized scope.

No live mutation, external communication, implementation edit, commit, push,
credential inspection, or unrelated-file change was performed by this reviewer.
The only created artifacts are this report and `adversarial_probes.py` in this
effort's folder. Official documentation and public source were read online.

## Exact claim under review

For a published, owned, specific Zenodo record version, an explicitly confirmed
partial metadata patch can be staged and then published or discarded. Omitted
metadata, the existing DOI, and files must be preserved. An uncertain mutation
response must not trigger an automatic duplicate mutation; an independently
verified remote result must survive a local receipt-write failure.

This is a software verification effort. Offline server models are empirical API
models, not proof of the behavior of Zenodo's currently deployed build.

## Checkable validation

Run from `zenodo_deposit_tool`:

```sh
python3 -W error::ResourceWarning -m unittest -v test_metadata_updates test_zenodo
python3 -W error::ResourceWarning metadata_updates_20261010/adversarial_probes.py
```

The initial existing test suite passed all 50 tests. Its checks cover exact ID and
confirmation, production/sandbox separation, preserving omitted legacy fields,
DOI/files checks, existing external edit rejection, explicit publish/discard,
saved state before mutation, no automatic duplicate mutation after lost
responses, changed-field/asset rejection, completed-session protection, and
the shared client's request and redaction behavior.

The independent probe script adds expected-behavior tests based on official
serializer/deserializer code. Its initial four probes all failed. The original
fifth probe demonstrated invisible native-author loss, and was then adapted to
require the repaired preflight refusal. Three further probes exposed native
session drift/recovery defects during the repairs. At this final checkpoint,
all 58 regression tests and all 8 independent probes pass, with ResourceWarnings
promoted to errors.

Reviewed implementation hashes at the final probe run:

| File | SHA-256 |
| --- | --- |
| `metadata_updates.py` | `43827440cd033abc453bffcb9dd3fbcbeccc1cd0fc27aab2d26255520f279263` |
| `zenodo.py` | `a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca` |
| `test_metadata_updates.py` | `2bbbaa0fe50532c26b93c4de13da8e5f4797113bd239010dc402f9a45bb3ac47` |
| `adversarial_probes.py` | `3bf8038417e9f63fdad094e3f749d4f6331a6f662329e9d6c76a123455a04c74` |

The shared workspace is actively edited by the primary agent. These hashes bind
this checkpoint rather than certifying later revisions.

## Findings repaired during review

1. **Explicit clearing of keywords and notes initially stranded a valid edit.**
   A `keywords: []` or `notes: ""` patch initially passed PUT in the probe, but
   the modeled official serializer omitted the empty field from GET. Exact
   metadata key equality rejected the resulting edit. Publish and discard also
   could not match the stored target. The existing fake's retention of empty
   values hid this mismatch. The revised verifier now permits narrow,
   explicitly-empty optional-field omissions. Both independent probes pass.

2. **A documented new related URL initially failed verification.**
   The probe adds an entry containing just `identifier` and `relation`; the
   modeled serializer adds `scheme: "url"`. Exact nested equality initially
   rejected the successfully staged edit. The revised verifier permits the exact
   addition of a matching inferred DOI/URL scheme, while retaining comparison of
   the supplied identifier, relation, and other attributes. The probe passes.

3. **An already-published retry initially lost confirmed status on receipt failure.**
   Stage and publish, then simulate `save_state` raising `OSError` on a repeated
   publish command. The initial implementation raised a generic persistence
   error although GET and metadata/files/DOI checks had confirmed the published
   result and no second publish POST occurred. The primary agent introduced a
   shared completion helper that returns `receipt_saved: false` with confirmed
   status. The independent probe now passes.

The first two server behaviors are supported by the current official legacy
[serializer](https://raw.githubusercontent.com/zenodo/zenodo-rdm/master/site/zenodo_rdm/legacy/serializers/schemas/common.py).
Its keyword and reference methods omit empty lists; its additional-description
method omits empty notes/method; related identifiers emit the detected scheme.
Identifier detection is implemented in the official legacy
[deserializer](https://raw.githubusercontent.com/zenodo/zenodo-rdm/master/site/zenodo_rdm/legacy/deserializers/metadata.py).

## Native preservation issue, repaired during review

Severity: high for native records with richer metadata; not reproduced by a live
mutation. This is a concrete source-derived model reproduction and a traced API
mechanism, rather than speculation about an arbitrary malicious server.

Reproduction: `test_omitted_native_author_details_survive_legacy_round_trip` in
the independent probe script starts with an organizational author and two native
affiliations. Its modeled legacy GET exposes only name and first affiliation.
The title-only patch resubmits the otherwise unchanged legacy creators. The
modeled official deserializer reconstructs a personal author and one affiliation.
Staging and publishing report success because every visible legacy field still
matches; the assertion comparing native author details fails.

The official serializer emits only the first affiliation and the supported
ORCID/GND author identifiers. The official deserializer reconstructs personal
author data. Both source links are above. The official legacy
[resource](https://raw.githubusercontent.com/zenodo/zenodo-rdm/master/site/zenodo_rdm/legacy/resources.py)
routes PUT to the inherited draft replacement method. The RDM
[metadata component](https://raw.githubusercontent.com/inveniosoftware/invenio-rdm-records/master/invenio_rdm_records/services/components/metadata.py)
assigns the parsed metadata to the draft, rather than merging omitted native
author details. A successful comparison solely through the legacy representation
therefore cannot establish preservation of all pre-existing native metadata.

The primary agent implemented an authenticated native reader, conservative
preflight shape checks, native snapshots, and exact comparisons of unpatched
native fields after staging and before publication. It rejects unsupported native
metadata such as organizational authors, multiple/structured affiliations,
unsupported author identifiers, controlled subjects, additional titles,
unsupported custom fields, and richer references. Patches are restricted to an
explicit field allowlist. Notes/method patches separately preserve unpatched
additional-description types. The adapted fifth probe now requires refusal
before edit/PUT for the original rich-author counterexample and passes. The
regression suite independently checks multiple unsafe native shapes and a
hidden author mutation after PUT.

## Native session drift and incomplete staging, repaired during review

Three new probes caught concrete gaps while the native protection was being
introduced. These are offline API models of source-supported hidden native
fields, rather than claims of live Zenodo behavior:

1. Stage a keywords patch, then add a native controlled subject which the legacy
   keyword serializer hides. Initially, a repeated staging command overwrote the
   saved native staged snapshot with this external change. Later publication
   could treat it as reviewed. Active-session restaging now rejects drift from
   the saved original/staged native snapshots; the independent probe passes.
2. With the same hidden native addition, discard initially ignored native
   differences in the patched subjects field and erased the external addition.
   Discard now rejects native drift from its saved snapshots before the action;
   the independent probe passes.
3. Simulate successful edit+PUT followed by a failed native draft GET. The saved
   session contains no `native_staged` snapshot. Initially, explicit publication
   could proceed and accept a hidden addition in patched native fields.
   Publication now requires completed native staging for an inprogress session
   and directs the user to resume the same update first; the probe passes.

The final snapshot checks also bind already-published recovery to the saved
native staged representation where one exists. A process-level file lock
prevents concurrent local mutators of the same record/environment from sharing
and overwriting a session; read-only inspection/preview remain available. The
regression suite checks this lock behavior and controlled errors for malformed
native responses.

## API state, recovery, and concurrency assessment

The official [Developer API documentation](https://developers.zenodo.org/)
supports editing an already-published deposition using edit, PUT, and publish,
and discarding changes using discard. A published editing session can have
`submitted: true` together with `state: inprogress`; the implementation's state
checks match this. The current official legacy serializer independently encodes
the same state semantics. Separate metadata publication preserves the specific
record version in this workflow rather than requiring a new version.

Mutation recovery is one attempted action followed by one authenticated GET.
The initial 50-test suite and independent receipt probe found no automatic second
mutation. Stale content that differs from both the saved original and saved
target is rejected; new files or a changed DOI are rejected. Completed local
sessions cannot publish or discard an already-open later editing session.

**Concurrency is a bounded limitation.** Content checks do not eliminate the
window between the last GET and a later PUT/publish/discard. A concurrent UI or
other-client edit in that window is not covered by the offline passing cases.
This reviewer has not reproduced that race on deployed Zenodo, and has not
claimed that local locking would eliminate remote-client races.

There is primary-source evidence for optional revision guards: legacy responses
use ETag headers, and the inherited
[draft resource](https://raw.githubusercontent.com/inveniosoftware/invenio-drafts-resources/master/invenio_drafts_resources/resources/records/resource.py)
passes parsed `If-Match` to draft update and deletion. Its edit and publication
methods do not pass that header. The
[draft service](https://raw.githubusercontent.com/inveniosoftware/invenio-drafts-resources/master/invenio_drafts_resources/services/records/service.py)
checks supplied revisions for draft update/deletion. This could reduce update
and discard races, but deployed support was not checked and it would not by
itself close publication races. Do not invent undocumented conditional semantics
or advertise total concurrency protection on this evidence alone.

## Strongest verified conclusion and remaining gap

No remaining actionable defect was identified in the checked, deliberately
bounded extension. Its supported-field workflow passes 58 regression tests and
8 independent adversarial probes. State semantics and action endpoints are
confirmed by official documentation/source. Rich native metadata is refused or
its unexpected loss is detected before publication; native staged snapshots
protect against detected later session drift.

The practical limits are material: this review did not execute edit, PUT,
publish, or discard against deployed Zenodo, including its sandbox. Actual API
canonicalization or transient deployment behavior can still cause a controlled
verification refusal and requires real-world validation before claiming full
integration coverage. External concurrent edits between the final read and
mutation remain a race window; local locking does not cover other clients.
No actual user's upload was changed by this review.
