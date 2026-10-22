# Independent terminal07 lifecycle review

Disposition: **REPAIR_REQUIRED**. Frozen at 2026-10-15T08:19:52.470669+00:00.
Best-guess completion of this bounded operational review: **100%**.
This is no publication, merge, factual-completion or intake authorization.
The implementation still has the two concrete repair requirements below.

## Reviewed identity and independence

Case PR191/problem5000005; original HEAD
`a2791bdd3f7ecd5694aeeeb5dffb21964a5639fe`; supplied original QUEUE
`claimed_solved`, historical effort `2/5`.

The independent attack plan was sealed before implementation inspection.
Source inspection began only after explicit terminal07 dispatch. The initial
plan, pins, log and their seal remain unchanged. No author test harness,
author result/report contents, prior reviewer reports or judgments were read.
`FINAL_SEAL.json` was read as the authorized source/pin manifest; its embedded
author assertions were not used as an oracle.

Reviewed all nine runtime source files and the full gate contract in
`lifecycle_controls_preparation_07`; all runtime identities match the authorized
pins. Common module:92727 bytes,SHA256
`c5a15c7b1c4e05b11c60fef73bd0c791d4b0cc46537778f65e1fa58c6f085479`.
Contract:31552 bytes,SHA256
`6b3877f3bf7a6def1f9282223591fa52c581e22df23f9297ebefc908c7176833`.
Source seal:6906 bytes,SHA256
`090583034e01c89417b417e9b0fabc34317846f94955019ad4b81560741f2ca9`.
The exact19 proposal basenames and their0444 modes were independently checked.
Excluded author artifact contents were not inspected to verify their claims.

The inert8580-byte Root v6 handoff matches SHA256
`6cf4d701f7ddbc5c63ac76d4e25c20f069ed98439d108b93f76e3644636f36a2`;
it was read and never executed. The dated117421-byte operations06 seed matches
SHA256 `b596503f3793ab65ac7bf21c54081d2160c573db993b614211096a7256965dc4`.
Its supplied644-member historical status is not fresh MAIN, current service
fact or publication authority. Root semantic historical authorities remain
trusted. No cryptographic external attestation or rewrite of Root history is
required by this review. The two whole-science/package reviews are unchanged;
no novelty, priority, independence or mathematics is re-certified here.

## Required repair07-01 — exact current merge-receipt DOI

`lifecycle_common.py:556–560`, `validate_merge_acceptance_schema`, checks the
record's key set but does not check the DOI field's type or approved value.
`verify_merge_scope(..., accepted=True)` at562–574 binds selected other fields
but leaves DOI unchecked. This current dynamically generated record is later
selected by the factual producer.

Independent standalone validation accepted both an incorrect DOI string and
`DOI: {"unexpected_own_field": "SYNTHETIC_OWN_DIAGNOSTIC_ONLY"}` in an otherwise
honestly produced `ROOT_ACTUAL_MERGE_ACCEPTANCE.json`.

**Actual late-consumer reproduction:** run the valid synthetic lifecycle
through actual `integration_accept`; replace only the resulting own record's
DOI; call actual `factual_prepare`; simulate adoption of its produced commit
in the in-memory repository; call actual `factual_accept`. Both actual late
consumers accepted. The selected factual commit contained the changed DOI
field verbatim. The wrong scalar and unexpected nested object were exercised
separately, rather than relying on a combined malformed input. All producer
pins, candidate tree, selected map, full-tree delta and operative message were
generated normally by the actual implementation. No authority or gate was
changed and no check was monkeypatched away.

Implication: the declared exact nested public-record boundary does not cover
this allowed field; an otherwise allowed current public filename can carry
unapproved nested own data. Only synthetic own diagnostics were used. No real
private data was read or disclosed.

Required correction: at every relevant current-record consumption, require
DOI to be the exact approved published DOI string already available as
`z['doi']`. An unexpected type, wrong scalar or nested additional data must
reject before selection. Keep historical Root authority semantics unchanged.

## Required repair07-02 — exact current merge-receipt selected-file count

The same current-record schema requires `selected_files` to be a positive
integer but does not compare it with the already validated original merge
map's cardinality. `verify_merge_scope(..., accepted=True)` also omits this
comparison. Replacing only this count with999999 passed standalone verification
and, in a separate actual full factual preparation/acceptance reproduction,
reached the selected public receipt unchanged.

Required correction: compare `selected_files` with the exact number of entries
in the independently validated original accepted merge's selected map. The
actual count is available without any new external attestation or authority.
A different positive integer must reject before current-record publication.

## Results and positive workflow

435 independent reproducible cases executed:429 met their expected result;
6 unexpected acceptances establish the two requirements above. These are three
standalone current-record cases plus three separate actual late-consumer
reproductions. There were no unexpected rejections. All expected rejection
cases ended with explicit RuntimeError validation failures in the final run.

The actual complete positive workflow passed: check, stage, inspect, publication,
postpublication inspection, exactly one own tracker append, two fresh own/full
observations, native95, metadata request and accepted metadata, final scope,
two-parent merge preparation/acceptance, native100, factual preparation,
fresh-parent factual retry and factual acceptance. The retry retained the exact
same native100 pointer, timestamps and all50 native file bytes. All16 original
custody members and non-factual native/proof/support bytes stayed exact; protected
case science remained exact; historical case/programme facts remained preserved.
Prepared95/100 retained cursor191 and pending actual factual-acceptance semantics;
only the actual final receipt authorized the separate next status-only intake.

The403 field-validation cases injected ordinary unexpected fields at every
dictionary depth present in the tested public dynamic service/control/native
records, and checked representative wrong intended scalar values/types.
They exercise actual validators with independent own fixtures. Public Zenodo
projections dropped synthetic raw extra fields at top level and inside uploaded
files, normalizations and DOI-resolution objects. Tracker request/response and
own-only evidence remained canonical. The complete valid selected factual map
contained no synthetic raw-service diagnostic marker and omitted the private
baseline. Unrelated own synthetic tracker additions remained permissible;
fresh duplicate DOI, changed own row and changed publication ID rejected.

Nine coherent prepared-postimage cases regenerated selected hashes, trees,
map digests and operative messages while altering case/prog/log/QUEUE/native
science, true-parent tree, unrelated full-tree content or selected scope; all
rejected in actual integration acceptance. Twelve unknown-write cases exercised
stage/publication/append lost responses with and without durable effects and
safe recovery; the service model recorded no duplicate created objects or
successful append/publication writes. This is bounded evidence for that explicit
offline model, not certification of production service behavior.

## Reproduction and precise limits

Run `python3 -B reproduce_07.py` from this folder, or pass this script's absolute
path. It verifies the common-module SHA256, loads the authorized inert source,
sets all paths to its own disposable folder, injects an in-memory full-tree
repository and independent durable service stand-ins, and writes results only
under this folder. It never executes a production helper, subprocess, network
request, Git command or Root handoff. Source, contract and runtime pins are
separately recorded in `SOURCE_VERIFICATION_07.json`.

The repository model implements actual tree/blob bodies, parent ancestry,
complete changed-leaf comparisons and selected current identities in memory.
It does not call real Git or GitHub. The service model independently stores
publication/tracker durable state and reads; no real service or exact-kit
production code was executed. Its stage operation reuses a previously created
record; no claim is made that this review independently proved the production
kit's retry mechanism. An absent-record inspect is represented as an explicit
unsuccessful operation. External post-observation concurrency remains a stated
service boundary. No real private foreign rows or credentials were used.

The fixtures use synthetic approved package/proof identities and synthetic
16/50 native members, exercising the pin/inventory/derivation mechanics. They
do not validate the actual scientific payload or current Root MAIN, which were
outside this authorized operational test. Not every hypothetical parser/path
case in the broad sealed plan was exercised: the bounded review stopped on
the independently reproduced ordinary current-record defects. No unsupported
PASS is inferred from the successful cases, and no new attack family is needed
to establish this repair disposition.

## Safe deliverables

`PUBLIC_SAFE_ALLOWLIST.json` has an exact `files` key. Only those named files
are intended for publication. Raw disposable fixtures, copied runtime files,
private synthetic command output and the entire `offline_work/` tree are
excluded. The final seal hashes every allowlisted artifact except itself to
avoid a cycle. All files in this review folder are frozen0444. The historical
pre-inspection seal remains independently checkable.
