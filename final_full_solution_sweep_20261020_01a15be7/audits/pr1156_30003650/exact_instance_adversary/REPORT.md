# Independent finite-instance capsule review — changes required

The 19,284-byte capsule `reconcile_exact_instance.py`, SHA256 `3d2489fbae11fa92b92965b80c28e4d906df91db8be4c4aafa3e8bda11f5f9fa`, is **not ready for adoption**. One material gap remains: the idempotent path can accept additional, unreviewed ledger rows during its final read and issue a verified receipt. This escapes the finite corpus guarantee and restores reliance on a generic parser that this review does not approve. No live action or root clearance was performed.

The unchanged 4,337-byte plan SHA256 is `83df78463704c63ea3969a87325f18ab21c21893d6e1b8b49c5b16a6b4e3b2e1`. The review applies only to this v1 capsule and its pinned dependency closure, not a later repair.

## Claim and success criteria

The intended action is one exact four-cell RAW/INSERT_ROWS append to Math Puzzles, spreadsheet `1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20`, gid1254632077, or safe adoption of the already identical unique planned row. This records existing external Ferudun record23350364/concept23350363. It makes no new publication, authorship transfer, historical priority, or generic alias-normalization claim.

The independently adjudicated account consists of197 records, including positive23408971. Each record must retain all exact value types, dictionary keys, list positions and values except existing nonnegative integer leaves at the eight exact top-level stats counters. The initial ledger must be the exact181-row corpus or that corpus plus the one planned row. Unknown identity changes must halt without append or false successful verification. Operational safeguards inherited from v6 must remain effective.

Success required original197/181 and fresh152-counter-delta positives, exact182-row idempotence, deliberate failures covering the new finite profile and relevant inherited guards, ordinary/-O/-OO full main-entry executions, unchanged originals, no actual service/process use, and no unresolved material counterexample. The last condition fails.

## Material finding: final idempotent ledger leaves the finite profile

At capsule lines293–300, the final read checks only that the prior ledger is a prefix. Its final inventory length check is inside `if appended:`. When the initial read contains the approved181 rows plus the exact planned row, `appended` remains false. A new183rd row in the final read therefore survives whenever the generic lexical checks do not recognize it as a target or unresolved alias.

The minimal reproduction begins with all197 approved records and the exact approved182-row idempotent ledger. The first read is unchanged. During the final read, add one row whose notes cell is:

`<a href="https://doi.org/10.5281/zenodo.&#50;3350364">same result</a>`

The capsule returns without error and saves a receipt with `status: verified`, `read_back_exact: true`, `unique_target_and_DOI: true`, `ledger_rows_before: 182`, and `ledger_rows_after: 183`. Python's separate standard-library HTMLParser decodes the href to the literal exact target DOI `https://doi.org/10.5281/zenodo.23350364`. No HTTP resolution or URI-equivalence inference is needed: the simpler ordinary unreviewed-row control also violates the exact final corpus policy.

The same mechanism accepts new zero-width-separated identifiers, fullwidth digits and an unknown external alias. Five trailing-row families were tested in each of all four columns:20 unexpected verified receipts per Python mode,60 across the main matrices. A known literal target DOI and a known short resolver still reject, confirming the asymmetric idempotent gate rather than indiscriminate acceptance by a stub. Dedicated four-case reproductions in all three modes preserve complete receipts and independently decoded HTML evidence. Each dedicated case performs zero mock appends. This finding is false verification after a concurrent change, **not** an unsafe append reproduced in the missing-row path.

Required closure: enforce the exact final181-row corpus plus the exact planned row unconditionally, including the idempotent path, before issuing any verified receipt. A new helper version requires its own source binding and review. No original source was changed by this reviewer.

## Strongest verified result

The finite account recursion is sound for its stated parsed-JSON domain. By structural induction: the initial exact-type check rejects type substitutions; a dictionary branch requires equal keysets and recurses into every value; a list branch requires equal lengths and recurses at every position. At a scalar leaf, equality is required unless its record-relative path is exactly two components, `stats` followed by one of the eight names. At those exception leaves, the prior scalar is a nonnegative exact integer and the initial type check forces the current scalar to be the same exact integer type; the remaining check forces nonnegativity. Booleans, floats, strings, null, lists, nested objects, extra counter keys, removals and nested metadata stats cannot exploit the exception. No text or new identity-bearing object can be introduced through it.

`fixed_account` additionally requires query empty, exact integer total197,197 distinct positive integer record IDs and the exact baseline ID set. Account record order and transport page count may change; each ID's entire record is still compared. Within-record list order remains fixed. The service reader independently enforces exact totals, same-host HTTPS pagination, no repeated records and complete enumeration. It constructs the query/total/pages/records envelope itself.

The initial finite ledger comparison, combined with the strict all-string four-column schema, rejects any added, removed, reordered or changed row, including changes outside known generic patterns. Original197/181 and the independently captured fresh197/181 with precisely152 counter deltas both complete one simulated exact append. Exact182-row idempotence succeeds. In the append path, prefix preservation plus the unconditional initial profile, one-row final inventory check and exact final row ensure the final corpus is the approved181 rows plus the planned row. The identified gap is confined to the final idempotent branch.

The complete independent context audit was also replayed from a newly created private source copy, with no project imports or service access. Its5,928-byte summary and7,174,468-byte private context output are byte-identical to the independently adjudicated outputs. This supports the finite corpus evidence:43,495 strings/keys,5 explicitly adjudicated broad bare10 contexts,1,041 long DOI resolvers,7,551 native machine URLs,201 queries,13 fragments, and zero unresolved semantic/alias/known-payload-MD5 leads. It does not establish any generic parser correctness. The supplied fresh comparison source/report was independently inspected and its input pins checked.

## Coverage and custody

I read the whole capsule and plan before adapting the prior07 engine. I inspected all meaningful six-dependency code, the full authenticated reader, inherited identity/operational guards and finite adjudication source. The768,646-byte checkpoint dependency was copied and fully parsed/compiled unchanged. Its371 NAMES-construction blocks contain750,772 bytes of static data/list operations; the only calls there are293 NAMES.extend calls and2 string startswith calls. I did not abbreviate or edit it in an execution fixture. The v6-to-finite diff confirms that only account/ledger profile checks, acceptance filename and receipt scope changed.

All651 controls ran through the actual main entry in each of ordinary Python, -O and -OO:1,953 primary executions.631 expected guard behaviors pass per mode; the remaining20 reproduce the single finding. All371 inherited controls pass after intentionally changing previous unrelated-addition positive expectations to rejection under the finite policy. The280 additional controls cover pinned/missing corpus inputs, actual/fresh profiles, repagination/reordering, inventory changes, all eight integer exception fields and invalid types, every first-record top-level field removal/type change, metadata/files/links/pids/parent/DOI/raw keys, new encoded/HTML/Unicode/unknown aliases in all four columns and account fields, exact row changes, and the critical final idempotent branch.

The inherited families exercise source hashes, external acceptance and review pins, source shadows/pyc, all-six-dependency/plan snapshot replacement, destination/schema/gid, complete pagination, public record/family/metadata and three payload size/MD5/SHA256 checks, DOI outcome, PR initial and immediate fields, exact freshness endpoints, durable exclusive intent/file+directory fsync, uncertainty recovery, full append response and prefix/readback failures. All actual records are the197-record corpus; old clean3-record synthetic inventories are not treated as admissible positives.

A further12 dedicated and5 exploratory full-main executions supplement the primary matrix:1,970 executions total. The main matrices contain60 false verified receipts, the dedicated set6, and exploratory probes2. These are repeated reproductions of one mechanism, not68 distinct defects. There are no false successful mock appends among the newly identified finite-profile fault cases.

Only this review's new private source copies were executed. Each case used a short-lived private tree; dependency bytes were verified then compiled in the real helper load order. The private fixture acceptance is synthetic and grants no actual adoption. HTTP/subprocess seams were stubbed; a persistent audit hook blocks underlying socket/DNS/process attempts and a filesystem seam denies secret-file reads. A fixture token was installed before project execution. Actual service/process attempts:0. Original source pins remain unchanged. No case fixture trees were retained, no infrastructure ENOSPC result was accepted as a guard rejection, no original acceptance was created, and no Git/index/ref/provider state was changed.

## Limits and reproduction

Trust assumptions remain an uncompromised interpreter, standard library and initial import environment; truthful authenticated installed service/CLI observations; root actually reviewing and externally supplying its acceptance SHA; trusted local exclusive-create/fsync behavior; and no distributed transaction between account, provider, PR and sheet. Freshness and immediate checks narrow cross-service intervals without eliminating them.

`offline_exact_instance.py --output <local-name>.json` runs the full matrix; use Python3, Python3 -O and Python3 -OO separately. Expected guard violations are recorded, so a zero harness exit means custody/offline execution completed, not helper approval. `critical_reproduction.py` runs the four-case minimal reproduction and writes CRITICAL_MODE_0/1/2.json. `verify_review.py` verifies the manifest, every private copy and original pin, exact mode/case counts, expected failure family and critical false receipts. For independent reruns, use a new copied review directory so the sealed artifacts remain unchanged.

Verdict: changes required for v1; no generic alias approval, publication/priority claim, root write clearance or live execution. Completion estimate:100% of this independent review.
