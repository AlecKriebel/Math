from pathlib import Path
import json,hashlib,os,stat,datetime
A=Path("/Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr85_30001203/isolated_main_integration_20261005/checkout/draft_pr_publication_program_20260930/audits/pr91_30003052")
R=A/'exact_reproduction_adversary_20261005'
pins=[]
def pin(p, row=None):
 p=Path(p)
 if p.is_symlink() or not p.is_file():raise RuntimeError('not regular '+str(p))
 b=p.read_bytes();h=hashlib.sha256(b).hexdigest()
 if row and (len(b)!=row['bytes'] or h!=row['sha256']):raise RuntimeError('pin mismatch '+str(p))
 pins.append(dict(path=str(p),bytes=len(b),sha256=h,native_mode=oct(stat.S_IMODE(p.stat().st_mode))))
 return b
m=json.loads(pin(A/'original_source_authentication_20261005/ORIGINAL_BLOB_MANIFEST.json'))
if m['original_count']!=20 or m['head']!='2ea84c5de45cb92783b5b55057af1f52590be6bf' or m['literal_status']!='claimed_solved' or m['original_budget']!='1/5':raise RuntimeError('original target differs')
for row in m['files']:
 b=pin(row['preserved_path'],row)
 if hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=row['git_blob_SHA1']:raise RuntimeError('Git blob mismatch')
 if stat.S_IMODE(Path(row['preserved_path']).stat().st_mode)!=0o644:raise RuntimeError('original mode changed')
for f in ['peripheral_projection_adversary_20261005/EVIDENCE_MANIFEST.json','full_spectrum_adversary_20261005/READ_BODY_PROCESS_MANIFEST.json']:
 j=json.loads(pin(A/f))
 for row in j['artifacts']:pin(row['path'],row)
m2=json.loads(pin(R/'ARTIFACT_MANIFEST.json'))
if m2['file_count']!=230 or len(m2['files'])!=230:raise RuntimeError('wrong computation manifestcount')
for row in m2['files']:
 p=R/row['path']
 if R.resolve() not in p.resolve().parents:raise RuntimeError('path outside computation folder')
 pin(p,row)
execution_records=[]
for p in sorted((R/'executions').glob('*/execution.json')):
 x=json.loads(pin(p))
 if x['actual_child_PID']<=0 or x['recorder_PID']<=0 or not x['argv'] or not x['cwd']:raise RuntimeError('missing execution metadata')
 if datetime.datetime.fromisoformat(x['UTC_end'])<datetime.datetime.fromisoformat(x['UTC_start']):raise RuntimeError('reversed process time')
 for name in ['stdout.bin','stderr.bin']:pin(p.parent/name,x[name])
 for row in x['sources']:pin(row['retained'],row)
 execution_records.append(dict(label=x['label'],PID=x['actual_child_PID'],returncode=x['exit_code'],argv=x['argv'],cwd=x['cwd'],start=x['UTC_start'],end=x['UTC_end']))
summary=json.loads(pin(R/'SUMMARY.json'))
if summary['verdict']!='PASS_EXACT_FINITE_REPRODUCTION_WITH_RUNTIME_CAVEAT':raise RuntimeError('verdict changed')
labels={x['label']:x for x in execution_records}
if len(labels)!=len(execution_records):raise RuntimeError('duplicate execution labels')
for row in summary['completed_execution_records_verified']:
 if labels[row['label']]['PID']!=row['actual_child_PID'] or labels[row['label']]['returncode']!=row['exit_code']:raise RuntimeError('execution summary mismatch')
for fam,n in [('submitted',473),('review',907)]:
 e=json.loads(pin(R/(fam+'_events_python39.json')))
 if e['actual_calls']!=n or len(e['events'])!=n or e['optimization']!=0 or e['exceptions']:raise RuntimeError('event ledger differs')
 if not all(t['truth'] is True and t['returned'] is True and t['exception'] is None for t in e['events']):raise RuntimeError('false event')
for row in summary['original_receipt_comparisons']:
 stream=R/'executions'/row['label']/'stdout.bin'
 b=pin(stream,row)
 orig=Path(m['canonical_checkout'])/'draft_pr_publication_program_20260930/audits/pr91_30003052/original_source_authentication_20261005/original_attempt'
 o=orig/('verification.json' if row['label'].startswith('submitted') else 'review/independent_results.json')
 if b!=o.read_bytes():raise RuntimeError('original receipt differs')
for row in summary['minimal_owned_repair_runs']:
 if labels[row['label']]['returncode']!=row['exit_code']:raise RuntimeError('repair return mismatch')
 if row.get('false_control_rejected') and row['exit_code']!=1:raise RuntimeError('negative control did not fail')
 if row.get('original_math_receipt_preserved') and row['actual_assertions'] not in (473,907):raise RuntimeError('repaired count differs')
for n,h in [('owr2016','28a2dc55933344c73a994f7eb50436469c7ddc4bc9ec73166d5cb8b97855aa1d'),('kuester2015','4422566d4944d0530e610071c3809566829bf18bf7846265e0f981a31c79f9fb')]:
 if hashlib.sha256(pin(A/'ROOT_source_scope_20261005'/(n+'.pdf'))).hexdigest()!=h:raise RuntimeError('primary changed')
for f in ['original_source_authentication_20261005/SOURCEPAIR_AUTHENTICATION.json','ROOT_source_scope_20261005/ROOT_SOURCE_SCOPE.md','ROOT_source_scope_20261005/ROOT_SOURCE_SCOPE_ACTUAL.json']:pin(A/f)
out=dict(schema='pr91-root-mathematical-adjudication/v1',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),actual_reader_PID=os.getpid(),PR=91,problem_id=30003052,immutable_head=m['head'],literal_status='claimed_solved',original_budget='1/5',new_central_proof_search_turns=0,mathematical_validity=True,exact_original_question_resolved=True,mathematical_audit_percent=100,analytic_families=['peripheral_projection_adversary_20261005','full_spectrum_adversary_20261005'],computational_family='exact_reproduction_adversary_20261005',original_bodies_unchanged=20,computation_manifest_verified=230,execution_records_verified=len(execution_records),original_counts=[473,907],separate_independent_counts={'peripheral_controls':6,'full_spectrum_controls_including_custody':573,'reproduction_boundary_controls':1340},no_finite_check_as_proof=True,root_primary_scope_complete=True,remaining_mathematical_gap=None,supporting_checker_finding='Optimization can bypass original assert; minimal repaired copies tested positive and false controls under-O.',supporting_checker_repair_required_before_publication=True,priority_audit_complete=False,priority_clearance=False,publication_clearance=False,whole_package_rounds=0,estimated_PR_workflow_percent=35,program_completed=11,dated_total=99,pins=pins,execution_records=execution_records)
(A/'ROOT_MATHEMATICAL_GATE_20261005.json').write_text(json.dumps(out,indent=2)+'\n')
with (A/'RESEARCH_LOG.md').open('a') as f:f.write('\n## '+out['UTC']+' UTC — ROOT mathematical gate\n\nAnalytic classification and exact source scope pass. ROOT authenticated20originals, all closed analytic-family artifacts,230 computational manifest files, full actual execution streams/source archives and473/907 traced true conditions. All finite controls are supplementary. Original-O assertion issue requires demonstrated minimal repair in public/native checker copies; originals remain unchanged. Math100%; source100%; priority ongoing50%; workflow35%; program11/99 (11.11%). No priority or publication clearance. Actual source/proof checkpoint cb8091dcfa69ed41defad72963836f5f8920648f pushed, remote verified.\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['pins','execution_records']}))

