# PR1262 workflow revision1

This is a narrow amendment to the immutable original proposal. Base manifest
SHA256: 202cf1602c1cfc9e9458e567fa97e0004a7a5c1f76380a07e10e83ff616ecd7d.
All nineteen base authored files authenticated before and after these tests.
No base file, sealed source-family artifact, deployed tool, shared kit, current
context, paper, metadata or external state was modified.

Deploy the original proposal exactly as previously documented, except replace
its verification_verify.py with this revision's verification_verify.py at
publication/verification/verify.py. This is the ONLY changed operative helper.
The other seven required helper scripts, actual coordinator and postmerge
verifier remain the unchanged base proposal versions. The existing base
workflow_regression.py does not need a source change; its complete suite passes
with this revised verifier copied alongside the unchanged helpers. The actual
final eight-script deployment hashes must be recorded from the deployed files
and presented to fresh whole-package reviewers. No deployment occurred here.

REVISION_DIFF.patch records three narrow changes:

1. The new explicit comparison enum json_ignore_start_end_utc ignores ONLY
   top-level run_started_utc and run_completed_utc. json_ignore_runtime,
   json_ignore_at_utc, json_exact and bytes_exact keep their previous semantics.
   For the actual source-family finite_checks.py, root should explicitly register
   normal mode, isolated layout, file output, no arguments, result
   reviews/source_question_family/finite_checks.json and this new comparison.
   The code runs from an immutable-byte copy in temporary scratch. Assertion-
   dependent diagnostics remain normal-only even when the surrounding verifier
   or test driver is run under -O/-OO. The result's mathematical payload and
   script_sha256 remain compared, and nested similarly named fields are never
   removed. This is a finite diagnostic replay, not proof of universal folding,
   critical/supercritical or other additional asymptotic claims.

2. The mandatory priority-family registration check accepts explicitly supplied
   reviews/priority_ family paths as well as legacy priority/ paths. The actual
   current families are reviews/priority_triangle and reviews/priority_modular.
   Root must register BOTH actual final sealed families using the exact schemas
   and outside SHA256 anchors once available. This amendment does not invent
   their schemas, supply pending manifests or authorize any clearance. It merely
   permits their known location convention. The registry still requires its
   explicit supported field triple, immutable outside anchor, safe member paths,
   declared base and all mandatory source/analytic registrations. Unrelated or
   nonpriority review families cannot replace the required priority evidence.

The original proposal's documented legacy-only priority-location paragraph and
comparison enum list are superseded only by these two changes. All other
contracts, identity/eight-thirteen scope, material-input fail-closed behavior,
strict metadata handling, review sequence, one-attempt intents and recovery,
public/tracker/PR/postmerge checks remain unchanged. No earlier mathematical or
priority conclusion is inherited from PR1261 or from synthetic fixture labels.

FOCUSED_TEST_RECEIPT.json reports identical PASS in normal/-O/-OO. Each mode
replays the actual immutable source-family code in normal-only temporary copies;
accepts changes to either or both named timestamps; rejects nine payload,
digest, other-runtime and nested-field changes; checks existing comparator
semantics; validates a complete current-context contract with the new enum;
accepts reviews/priority_triangle/MANIFEST.json; rejects unrelated/nonpriority,
missing-priority, wrong-anchor and guessed-schema substitutes; retains legacy
priority-family acceptance; and executes the entire unchanged base workflow
regression with this revised verifier. Every actual base/source input binding
is reauthenticated at the end. Compiler, service and Git I/O inside base fixtures
remain mocked, as documented in the immutable base proposal. No real release
clearance is produced.

The new authored manifest uses authored_files/path/bytes and excludes itself.
It explicitly binds the immutable base proposal's outside anchor. Register this
revision freeze alongside the base freeze if retaining both in the portable
package. Root must review the diff, supply complete actual material inputs,
deploy recorded exact bytes and obtain the requested fresh sequential whole-
package reviews before the already authorized release process.
