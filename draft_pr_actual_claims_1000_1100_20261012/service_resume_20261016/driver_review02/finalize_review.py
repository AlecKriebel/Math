"""Record bounded administrative review evidence without touching candidates."""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
H=Path(__file__).resolve().parent;R=H.parent;T=datetime.datetime.now(datetime.timezone.utc).isoformat()
def load(p):return json.loads(p.read_text())
def identity(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
# Preserve an exact rerun of the first incomplete-fixture failure. It remains
# incomplete, so this is an expected failing probe, not a driver finding.
argv=[sys.executable,'-B',str(H/'preflight_fixture'/'service'/'prepare_service_configs.py')]
p=subprocess.run(argv,capture_output=True,text=True,timeout=30)
save(H/'PREFLIGHT_INITIAL_FIXTURE_FAILURE_REPRODUCED.json',{'utc':T,'argv':argv,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'scope':'Reproduced initial probe-setup omission: PR1098 auxiliary review JSON absent only from this fixture.'})
assert p.returncode==1 and 'ROOT_WHOLE_PACKAGE_REVIEW_02.json' in p.stderr
pins={name:identity(R/name)for name in ['run_service.py','prepare_service_configs.py']}
for name,v in pins.items():assert v==identity(H/('REVIEWED_'+name+'.txt'))
parsed=[];invalid=[]
for i,line in enumerate((H/'COMMAND_RECEIPTS.jsonl').read_text().splitlines(),1):
 try:parsed.append(json.loads(line))
 except json.JSONDecodeError:invalid.append(i)
assert not invalid,invalid
probes=load(H/'PROBE_RESULTS.json');preflight=load(H/'PREFLIGHT_REPLAY.json')
assert probes['status']=='PASS' and len(probes['results'])==25
assert preflight['exit']==0 and all(preflight['generated_configs_match_current_canonical'].values())
report={'utc':T,'status':'ZERO_ACTIONABLE_ISSUES_IN_BOUNDED_ADMINISTRATIVE_REVIEW',
        'assigned_review_completion_percent':100,'P0':0,'P1':0,'P2':0,'P3':0,'findings':[],
        'reviewed_source_identities':pins,'frozen_sources_equal_current_at_end':True,
        'scope':'Full administrative driver and config-generation source review with bounded offline subprocess/failure probes. Not a mathematical review, preprint review, native uploader audit, or service authorization.',
        'independence':'Fresh analysis of both source files and native uploader first; previous driver_review01 report/harness read only after that independent analysis. No further agents.',
        'fixed_findings_verified':{
          'D01':'Durable completion event, atomic owned writes and idempotent registry/log/README before cursor save; failure/retry checks before and after five write targets pass; shared completion lock serializes completed-old retry and current PR.',
          'D02':'Stable first-write acceptance payload; PATCH/ready readback and durable intents; an existing merge intent prevents all additional PR mutations; no recursive nesting on retry.',
          'D03':'Fresh exact unique DOI and full-row verification blocks both merge and completion after remote-row deletion.',
          'D04':'Same-head wrong base branch, wrong repository and wrong PR number are rejected before staging; live target checks also surround merge.'},
        'evidence':{'offline_driver_probes':25,'driver_child_command_receipts':len(parsed),
                    'config_generation_replay':'13 exact canonical config matches; 26 reviewed asset byte identities rehashed; all input source byte identities unchanged.',
                    'native_source_read':'zenodo_deposit_tool/zenodo.py: load_manifest/state_path/local_state/verify/run/published_summary inspected for exact metadata/file and recovery contract.'},
        'failures_disclosed':[
          'First offline harness run failed at plan because the harness parsed native argv without accounting for -B; corrected only the harness. Raw child receipt is preserved as first line of COMMAND_RECEIPTS.jsonl.',
          'Next suite attempt suffered real OSError ENOSPC while controller saved a timeout-probe receipt. That entire partial attempt is not counted as a successful suite; its already-written command receipts remain. The individual invocation whose receipt write failed is not asserted to have a known persisted outcome. Disposable unsealed fixtures were reset by suite setup during final rerun; no prior/canonical/frozen source was removed. Final entire 25-probe rerun passed.',
          'Initial config replay omitted PR1098 ROOT_WHOLE_PACKAGE_REVIEW_02.json from its isolated fixture. Canonical generator correctly failed with missing file. Original incomplete fixture is preserved; exact failure is reproduced and recorded separately. Second fixture includes that input and passes all13 configs.'
        ],
        'limits':['Service subprocesses are faked and sockets blocked in driver children; no real API, credential, authorization or external service behavior was tested.',
                  'Config replay uses 26 read-only fixture hardlinks to reviewed PDF/archive inputs and copies JSON inputs. No linked path is written. Content identities were rechecked unchanged; hardlink creation changes link metadata.',
                  'Injected local errors cover process-level write interruption/retry. Power-loss durability and arbitrary concurrent writers that ignore the shared lock are outside this bounded review.',
                  'PR1032 config is outside the thirteen-package prepare script and was not generated by this review. All driver cases use synthetic PR1033/1034 fixtures.',
                  'No candidate contents, canonical scripts, real service records, Git state or release were changed. No external communication or further subagents.'],
        'uncompleted_required_checks':[]}
save(H/'REPORT.json',report)
(H/'REPORT.md').write_text(f'''# Administrative driver review 02

{T} — **ZERO actionable P0/P1/P2/P3 issues** in this bounded administrative review. Assigned administrative review completion: **100%**. This is not a mathematical or preprint whole-package review.

Current sources equal the frozen reviewed copies at end. `run_service.py`: `{pins['run_service.py']['sha256']}`; `prepare_service_configs.py`: `{pins['prepare_service_configs.py']['sha256']}`.

Fresh source analysis preceded reading review01. The four previous findings are fixed in these bytes. Twenty-five offline subprocess probes pass: full staged flow; ten before/after local completion-write failures with idempotent retry; failed merge retry without body nesting or repeated mutation; successful-but-timeout publication/PATCH/ready/merge/append reconciliation; uncertain stage without saved ID; four identity/target drift checks; stale tracker rejection at merge/completion; and a two-process shared-completion-lock test. See `PROBE_RESULTS.json`, `offline_probe.py`, and `COMMAND_RECEIPTS.jsonl`.

The unmodified frozen config generator also ran in an isolated fixture: all thirteen generated configs equal the current canonical configs, twenty-six reviewed assets were rehashed, and every source byte identity remained unchanged. See `PREFLIGHT_REPLAY.json` and `replay_preflight.py`. The PDF/archive fixture uses read-only hardlinks; link metadata changes, but no linked path is opened for writing.

Failures are preserved and excluded from successful-run claims. The initial driver harness had an argv-index mistake at plan, corrected only in the harness. A partial later run hit real ENOSPC while saving a receipt; its completed receipts remain, and the unsaved invocation outcome is not certified. Only newly created unsealed mock fixtures were reset by final suite setup. A first config fixture omitted PR1098's auxiliary review JSON; that original fixture remains and its expected failure is reproduced in `PREFLIGHT_INITIAL_FIXTURE_FAILURE_REPRODUCED.json`. The corrected second fixture passes.

No real service calls, credentials, external communications, Git operations, candidate content edits, or further agents. PR1032 config preparation, actual API behavior, power-loss durability and writers ignoring the shared completion lock are outside scope. No required assigned checks remain uncompleted. `REPORT.json` contains precise scope and limitations.
''')
(H/'RESEARCH_LOG.md').write_text(f'''# Review log

- 2026-10-17T03:57Z — Independent fresh read of both administrative scripts and applicable root AGENTS completed before reading review01. Administrative review estimate 25%; mathematical/preprint review not undertaken.
- 2026-10-17T03:59Z — Frozen current driver with shared completion lock; source SHA f0a12d61a88adfe8a76349534741402914ac95caa129ccde1deb5b64e6ba218d. Administrative estimate 50%.
- 2026-10-17T04:01Z — Harness-only argv-index failure corrected. Partial suite then hit real ENOSPC in controller receipt write; preserved existing receipts, claimed no full-suite success. Administrative estimate 75%.
- 2026-10-17T04:01:50.555873+00:00 — Complete final 25-probe offline subprocess/failure run PASS. Administrative estimate 90%.
- {T} — Corrected isolated thirteen-config replay PASS after preserving initial missing-fixture-input failure. Current source hashes equal frozen copies. Final administrative estimate 100%; ZERO actionable P0/P1/P2/P3 in bounded scope. No math/preprint review credit.
''')
outputs=[]
for q in sorted(H.rglob('*')):
 if q.is_file() and q.name!='OUTPUT_PINS.json':outputs.append({'path':str(q.relative_to(H)),**identity(q)})
save(H/'OUTPUT_PINS.json',{'utc':T,'files':outputs,'scope':'End-of-review identities; includes own mocked fixtures and copies/read-only links. No candidate writes.'})
print(json.dumps({'status':report['status'],'administrative_completion_percent':100,'probes':25,'configs':13,'outputs_pinned':len(outputs),'sources_unchanged':True}))
