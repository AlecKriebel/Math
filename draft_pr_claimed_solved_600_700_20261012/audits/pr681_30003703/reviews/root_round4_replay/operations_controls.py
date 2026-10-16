#!/usr/bin/env python3
"""Round4 new hostile selections; exact source; isolated toy repositories only."""
import contextlib, copy, datetime, hashlib, io, json, os, shutil, sys, types
from pathlib import Path
R=Path(__file__).absolute().parent;A=R.parent.parent
p=R/'fixture_plumbing.py';f=types.ModuleType('read_independently_captured_plumbing');f.__file__=str(p)
exec(compile(p.read_bytes(),str(p),'exec'),f.__dict__)
f.T=R/'tmp'/('new-ops-opt' if sys.flags.optimize else 'new-ops-normal')
if f.T.exists():shutil.rmtree(f.T)
f.T.mkdir(parents=True)
Fixture=f.Fixture;need=f.need;write=f.write;DOI=f.DOI
results=[]
def check(name,fn):fn();results.append({'name':name,'status':'PASS'})
def reject(name,fn):
 try:fn()
 except (ValueError,OSError,f.real_subprocess.CalledProcessError) as exc:results.append({'name':name,'status':'REJECTED','error':str(exc)});return
 raise RuntimeError('accepted hostile '+name)
q=Fixture();f.norm(q);v=q.inputs()['validation'];q.final_gate('tracker',v)
for label,mut in [('sheet_id_boolean',lambda d:d.update(sheet_id=True)),('sheet_title_case',lambda d:d.update(sheet_title='Math puzzles')),('publication_receipt_rebinding',lambda d:d.update(publication_receipt_sha256='0'*64)),('accepted_gate_rebinding',lambda d:d.update(accepted_input_gate_sha256='0'*64)),('wrong_doi',lambda d:d.update(doi='10.5281/zenodo.1')),('wrong_action_schema',lambda d:d.update(schema='pr681-final-integration-gate-v1'))]:
 q.final_gate('tracker',v);q.mutate_json('FINAL_TRACKER_GATE.json',mut)
 reject('tracker_gate_'+label,lambda:q.h.validate_live_write_gate('tracker',DOI,v))
for label,mut in [('cross_repository',lambda d:d.update(isCrossRepository=True)),('wrong_owner',lambda d:d.update(headRepositoryOwner={'login':'SomeoneElse'})),('wrong_base',lambda d:d.update(baseRefName='other')),('non_draft',lambda d:d.update(isDraft=False)),('merged',lambda d:d.update(state='MERGED'))]:
 old=copy.deepcopy(q.live);mut(q.live);q.final_gate('tracker',v)
 reject('fresh_live_identity_'+label,lambda:q.h.validate_live_write_gate('tracker',DOI,v));q.live=old
for label,path,data in [('duplicate_receipt_key','ZENODO_PUBLICATION_RECEIPT.json',b'{"environment":"production","environment":"production"}'),('receipt_NaN','ZENODO_PUBLICATION_RECEIPT.json',b'{"bad":NaN}'),('acceptance_duplicate_key','ACCEPTED_PUBLICATION_INPUTS.json',b'{"schema":1,"schema":1}')]:
 old=(q.a/path).read_bytes();(q.a/path).write_bytes(data);reject(label,q.inputs);(q.a/path).write_bytes(old)
for label,number,mut in [('bool_zero_optional',2,lambda d:d.update(optional_findings=False)),('one_optional',2,lambda d:d.update(optional_findings=1)),('finding_hidden_in_list',2,lambda d:d.update(findings=[{'mandatory':False}])),('second_start_future',2,lambda d:d.update(started_utc=(f.NOW+datetime.timedelta(days=1)).isoformat())),('empty_reviewer',2,lambda d:d.update(reviewer_id=''))]:
 x=Fixture();x.repin_report(number,mut);reject('review_'+label,x.inputs)
# Every source is captured and rechecked. A symlink cannot substitute identical bytes.
x=Fixture();v=x.inputs()['validation'];target=x.a/'publication/requirements.txt';b=target.read_bytes();target.unlink();target.symlink_to(A/'publication/requirements.txt')
reject('identical_byte_source_symlink_rejected',lambda:x.h.recheck_sources(v));target.unlink();target.write_bytes(b)
# Full current normalized and raw paths, including exact source diagnostic.
for normalized in [False,True]:
 x=Fixture()
 if normalized:f.norm(x)
 x.init_git();x.final_gate('integration');r=x.integration(True)
 check('full_push_captured_source_'+str(normalized),lambda:need(r['pushed'] and x.push_count==1 and x.git_snapshot()==x.git_initial,'push source isolation'))
 check('full_root_pushed_'+str(normalized),lambda:need(f.root_diagnostic(x)['all_23_native_bytes_blobs_modes_exact'],'pushed root'))
 check('full_root_merged_'+str(normalized),lambda:need(f.root_diagnostic(x,True)['status']=='PASS','merged root'))
 # New diagnostic hostile changes affect receipt, never packet code.
 rp=x.a/'INTEGRATION_PUSHED_RECEIPT.json';original=rp.read_bytes();d=json.loads(original);d['publication_sha256']['ghost.txt']='0'*64;write(rp,d)
 reject('root_publication_extra_receipt_member_'+str(normalized),lambda:f.root_diagnostic(x));rp.write_bytes(original)
 d=json.loads(original);d['tree']='0'*40;write(rp,d)
 reject('root_wrong_accepted_tree_'+str(normalized),lambda:f.root_diagnostic(x));rp.write_bytes(original)
 # Sticky intent blocks repeat before any second transport.
 reject('repeat_push_blocked_'+str(normalized),lambda:x.integration(True));need(x.push_count==1,'repeat dispatch')
# Remote main advances only at the last pre-push observation: no dispatch.
x=Fixture();x.init_git();x.final_gate('integration');old=x.h.remote_oid;count=[0]
def drift(ref):
 if ref=='refs/heads/main':
  count[0]+=1
  if count[0]>=3:return 'f'*40
 return old(ref)
x.h.remote_oid=drift
reject('fresh_remote_main_drift_before_push',lambda:x.integration(True));check('drift_sent_zero_pushes',lambda:need(x.push_count==0,'drift pushed'))
# Bad push URL is rejected after preparation and before any push intent/transport.
x=Fixture();x.init_git();x.final_gate('integration')
f.real_subprocess.check_output(['git','config','remote.origin.pushurl','https://evil.invalid/repo'],cwd=x.repo)
reject('unselected_push_URL_no_dispatch',lambda:x.integration(True));check('bad_push_URL_transport_count_zero',lambda:need(x.push_count==0,'wrong destination push'))
# Exact tracker source, normalized acceptance, target and global uniqueness rechecks.
x=Fixture();f.norm(x);dry=x.tracker_main();check('tracker_normalized_dry',lambda:need(not dry['applied'] and x.append_count==0,'dry'))
x.final_gate('tracker');done=x.tracker_main(True);check('tracker_normalized_apply',lambda:need(done['applied'] and x.append_count==1,'apply'))
x.tracker_main(True);check('tracker_existing_readonly',lambda:need(x.append_count==1,'duplicate'))
x.values[1][2]=' DOI: '+DOI.upper()+' /' # intentionally not a valid exact DOI match
need(x.tr.doi_matches(x.values,DOI)==[],'malformed spaced slash must not match')
# Accepted alternate DOI spellings must all trigger one exact row comparison.
for spelling in [DOI.upper(),'doi:'+DOI,'https://dx.doi.org/'+DOI+'/', 'https://doi.org/'+DOI]:
 values=[x.tr.HEADERS,['','',spelling,'']]
 check('exact_DOI_scan_'+spelling,lambda:need(x.tr.doi_matches(values,DOI)==[2],'DOI match'))
print(json.dumps({'schema':'pr681-round4-new-operations-controls-v1','status':'PASS','mode':'optimized'if sys.flags.optimize else'normal','count':len(results),'controls':results,'source_sha256':{n:hashlib.sha256((A/n).read_bytes()).hexdigest()for n in ['prepare_integration.py','record_tracker.py','root_check_integration.py']},'fixture_plumbing_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'transports_intercepted':True,'real_network_or_external_mutations':0,'mock_dispatches':f.DISPATCHES},indent=2,sort_keys=True))
