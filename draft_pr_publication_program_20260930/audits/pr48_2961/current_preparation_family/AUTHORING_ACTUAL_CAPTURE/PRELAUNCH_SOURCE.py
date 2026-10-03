"""Author only this family's operative presentation and false/null drafts."""
import datetime as dt, hashlib, json, os
from pathlib import Path
F=Path(__file__).absolute().parent;A=F.parent
stamp=dt.datetime.now(dt.timezone.utc).isoformat()
def write(n,b):
    with (F/n).open('xb') as h:h.write(b if type(b) is bytes else b.encode())
def dump(o):return json.dumps(o,indent=2,allow_nan=False)+'\n'
qual='''# Operative qualifications for PR48 / KP-4.85

The exact original target remains UNSOLVED: a closed orientable smooth four-manifold with unbounded ordinary commutator length in its full Diff-infinity-0. The stabilized subgroup bound cl(f x id-S2)<=4 is valid in the ambient group; it supplies neither a bound for every ambient element nor an unbounded sequence. The Borel cocycle example in a fresh family diagnoses the averaging axioms; it is not a smooth geometric cocycle solving the target. No novelty, best-known-bound, paper, DOI or tracker row is claimed. This package is unrefereed and has not undergone human peer review. AI tools were used extensively in the original work and verification.

2961 / KP-4.85 and 30004403 / OWR-17471-009 are exactly the same target. They share two original substantive approaches out of five, not separate budgets. New substantive attempts0; audit turns0. The original two-entry JSONL ledger is literal. An absent duplicate queue row remains absent; only existing target rows may receive the local prospective Status/Turns/Findings changes. All other rows and columns, including Chat and DOI, remain byte-exact. Later native reconciliation needs a new ROOT plan and fresh13 authority.

For both plain integer-ID selected source records, the upstream research-results key is ABSENT. The in-place SQLite importer stores literal {} as its fallback. There is no original prior-report file. A missing key, present null, present empty object and local fallback are distinct cases. The original SOURCE_AUDIT null wording is preserved in original_archive as inaccurate dated provenance; the operative SOURCE_AUDIT corrects it. No raw, SQLite, PDF, OCR or pixel body is copied as a republication input.

The old review binds genuine Git mathematical note0036b78ba3164a52c15a7a24ea73fe4438a3db3c9a206f2882070c23e91cd3b2 from commit2c32c34e6ddfa52ce067805afd3e2157dc32a130. Final PARTIAL has hash196568d2029fd378dfa43919efbf49dcbd11244a2de8c525483f84484f00e5fa. Their sole changed sentence records completed review and adds the no-human-peer-review disclosure; mathematics and unresolved status are identical. Literal historical6570 receipts remain unchanged and bind the old note, not the final note. Genuine ROOT final-input replay11716 also passes6570; its receipt differs only in partial_sha256. The identical submitted author replay is a duplicate, not independent evidence. The historical independent checker reproduces228 exact assertions under actually installed SymPy1.14.0. Finite controls do not prove imported smooth perfectness or the full open problem.

Original runtime/model/effort/deadline, prior-attempt search, PDF hashes, pixels, review-pending/no-PR prose and PASS are attributed September30 history. The operative current review status is PENDING a new whole-current adversary. Fresh closed algebra and smooth families are distinct original-head partial reviews; their report/body/hash/render claims have their own stated scope. ROOT's current replay and raw audit supplement historical evidence but do not certify future package approval. SOURCE review, whole-current review, acceptance plan, integration and merge are separate events.

Classical Mather-Thurston perfectness and the BIP/Tsuboi/BHW imported theorems retain their published hypotheses and credit. The no-middle-handle bound four is conservative and is not claimed best known; later credited bounds do not resolve general dimension4. Compact-total-support isotopies, positive-genus surface hypotheses, finite connected-component reduction, integrability in the cocycle formula and centrality for descent remain essential. No exhaustive priority or literature-absence certificate is claimed.

A future actual builder only copies first-party evidence, unchanged original17 scientific files and explicit qualified presentation. It leaves all native inputs untouched. It copies a PREPUBLICATION prefix of its own evolving command record; ROOT must inspect the final entire original inner record and the genuine outer completion AFTER child exit at their actual paths. A frozen prefix or prelaunch cannot claim future completion. The whole-current gate stays PENDING; current model/reasoning/deadline/verdict are null. All ROOT prerequisites in this SOURCE folder are false/null drafts and confer no approval.
'''
write('SOURCE_PRECISION_QUALIFICATIONS.md',qual)
notice='''# Dated original evidence notice

The literal original17 files are preserved under original_archive. Original model/effort/deadline, source access/PDF hashes/pixels, PASS, pending/no-PR statements and prior-attempt search are historical attribution, not current runtime or approval. Read SOURCE_PRECISION_QUALIFICATIONS.md with every presentation. Literal receipts bind the historical note; the final-input replay is separately qualified. The full target is UNSOLVED and the NEW whole-current review is PENDING.

'''
write('HISTORICAL_ORIGINAL_NOTICE.md',notice)
source=(A/'source_snapshot/SOURCE_AUDIT.md').read_text()
assert source.count('its research-results entry is null')==1
source=source.replace('its research-results entry is null','for both exact targets the upstream research-results key is ABSENT, the local SQLite importer uses literal {} as its fallback, and no original prior-report file exists')
old='The actual model was gpt-6-astra at xhigh reasoning. Separate adversarial review is pending; no PR will be opened before that review. Shared queue/state files were not regenerated or edited here.'
assert source.count(old)==1
source=source.replace(old,'Dated September30 author attribution: model gpt-6-astra at xhigh reasoning. The pending-review/no-PR statement described pre-review authoring history; the archived final review subsequently reported PASS_PARTIAL. Fresh independent original-head reviews have their own closed reports. NEW whole-current acceptance review remains PENDING; no historical PASS or runtime assertion approves it. Shared native files are untouched by this SOURCE preparation.')
write('OPERATIVE_SOURCE_AUDIT.md',qual+'\n'+notice+source)
overview='''# KP-4.85: valid unresolved partial, PR48

The target remains UNSOLVED. For closed smooth M, every stabilized f x id-S2 has ambient commutator length at most four in Diff0(M x S2), by classical support displacement and two sphere cutoffs. This proves a transfer obstruction for the included surface subgroup. It gives no universal bound on the full ambient group and no required unbounded sequence. Direct cocycle averaging retains an extra signed pushforward term without measure invariance, and the full positive-dimensional identity group preserves no Borel probability. Other possible mechanisms remain open.

The exact duplicate30004403/OWR-17471-009 shares the same result and original2/5 attempt budget. New0; audit0. Published theorem hypotheses and credit remain explicit; no novelty or best-known claim is made. Operative SOURCE_AUDIT corrects missing-report-key provenance and dated pending-review prose. Literal historical helpers/results/plain sources/ledger and original17 archive are preserved. Historical6570 and independent228 receipts and the separate final-input6570 replay have precisely stated input hashes. Fresh algebra/cocycle and smooth-geometry reports support the partial mathematics; a new whole-current review remains PENDING.

This is an unrefereed source-qualified research record, with extensive AI assistance and no human peer review. No paper, DOI or tracker row is prepared. Exact remaining mathematical gap: an unbounded ordinary ambient commutator-length sequence in one full required closed smooth four-dimensional group, or a theorem excluding every such example. No native write, acceptance plan or merge is certified by this SOURCE package.
'''
write('CURRENT_OVERVIEW.md',overview)
for n in ['DRAFT_ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md']:
 write(n,'# DRAFT ROOT PR48 scope — NO APPROVAL\n\napproved_by_root: false\nreading_completed: false\ncurrent_verdict: null\nNEW whole-current review: PENDING\nOriginal shared2/5; new0; audit0; UNSOLVED.\n')
for n,schema in [('DRAFT_ROOT_PRIMARY_READ_LEDGER.json','pr48-root-primary-read-ledger/v1'),('DRAFT_ROOT_SCIENCE_CARD.json','pr48-root-science-card/v1'),('DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json','pr48-root-fresh13-input-preimages/v1'),('DRAFT_ROOT_EVIDENCE_BINDINGS.json','pr48-root-evidence-bindings/v1')]:
 write(n,dump({'schema':schema,'operative_preparation_directory':'current_preparation_family','draft':True,'approved_by_root':False,'reading_completed':False,'root_flags':None,'created_utc':None,'current_head':None,'files':None,'current_verdict':None,'future_acceptance_approved':False,'full_problem_solved':False,'status':'unsolved','duplicate_id':30004403,'duplicate_shared_budget':True,'original_substantive_attempts':2,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0}))
write('SOURCE_STATUS.json',dump({'schema':'pr48-source-only-status/v1','created_utc':stamp,'actual_authoring_pid':os.getpid(),'source_preparation_completion_estimate_percent':75,'target_discovery_completion_estimate_percent':0,'original_shared_turns':'2/5','new_substantive_attempts':0,'audit_turns':0,'production_builder_imported_compiled_or_executed':False,'ROOT_prerequisites_authored':False,'candidate_frozen':False,'future_acceptance_approved':False,'native_writes':False,'merge':False,'paper':False,'DOI':False,'tracker':False}))
write('SOURCE_PREPARATION_RESEARCH_LOG.md',stamp+' — Read complete original partial, two distinct helpers, old review, source/plain records, ROOT proof and both fresh reports. SOURCE preparation75%; full-target discovery0%. Mandatory absent/null provenance and dated review/hash qualifications prepared; full group remains unsolved. Original shared2/5; new0; audit0. Production builder/operator remain unexecuted.\n')
print(dump({'status':'PASS_SOURCE_DOCUMENT_AUTHORING','created_utc':stamp,'production_builder_executed':False,'ROOT_prerequisites_authored':False,'candidate_frozen':False}))
