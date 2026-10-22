"""New actual06 live-gate and complete review-contract sensitivity tests, all transport fake."""
import sys
if not sys.flags.isolated or sys.flags.optimize:raise RuntimeError('Use -I -B')
from pathlib import Path
import json,copy,hashlib,contextlib,io
from datetime import datetime,timezone
O=Path(__file__).resolve().parent
source=(O/'closure07_controls.py').read_text();setup=source[:source.index('\ntargets=')];ns={'__file__':str(O/'closure07_controls.py'),'__name__':'_contract_setup_'};exec(compile(setup,str(O/'closure07_controls.py'),'exec'),ns);N=ns['N'];a=ns['a'];d=ns['d'];w=ns['w'];F=ns['F'];FP=ns['FP'];ctx=ns['ctx'];accepted=ns['accepted'];specs=ns['specs'];originals=ns['originals'];results=[];baseblob=N['blob'];baserun=N['run'];baseview=N['pr_view'];catalog=json.loads(ns['catalog']);queue=ns['queue']
def reject(label,fn):
 try:
  with contextlib.redirect_stdout(io.StringIO()):fn()
 except (RuntimeError,OSError,ValueError,KeyError,TypeError) as e:
  assert 'Unexpected fake' not in str(e);results.append({'case':label,'rejected':True,'reason':str(e)[:400]});return
 raise RuntimeError('INVALID ACCEPTED '+label)
for key,value in [('number',True),('headRefOid','0'*40),('baseRefName','other'),('state','CLOSED'),('isDraft',False),('body','changed')]:
 changed=copy.deepcopy(baseview());changed[key]=value;N['pr_view']=lambda:changed;reject('premerge_live_'+key,lambda:N['premerge_gate'](F,require_draft=True))
N['pr_view']=baseview
for key,value in [('present',False),('holds',['SYNTHETIC_HOLD']),('statement_hash','0'*64),('review_hash','0'*64)]:
 data=copy.deepcopy(catalog);data[0][key]=value;N['blob']=lambda ref,name:json.dumps(data).encode() if name==N['CATALOG'] else baseblob(ref,name);reject('fresh_source_'+key,lambda:N['premerge_gate'](F,require_draft=True))
N['blob']=lambda ref,name:b'{"groups":[{"ids":["6000001"],"reason":"new"}]}' if name==N['RELATED'] else baseblob(ref,name);reject('fresh_source_new_related_membership',lambda:N['premerge_gate'](F,require_draft=True));N['blob']=baseblob
for text in ['claimed_solved_but_unchecked','preprint_published','partially_solved']:
 badq=queue.replace(b'claimed_solved',text.encode());N['blob']=lambda ref,name:badq if name==N['QUEUE'] else baseblob(ref,name);reject('exact_HEAD_status_'+text,lambda:N['premerge_gate'](F,require_draft=True))
N['blob']=baseblob
N['run']=lambda argv,**kw:'unrelated/path\n' if argv[:2]==['gh','api'] else baserun(argv,**kw);reject('unrelated_changed_PR_path',lambda:N['premerge_gate'](F,require_draft=True));N['run']=baserun
N['blob']=lambda ref,name:(b'other queue bytes\n'+queue) if name==N['QUEUE'] and ref=='a'*40 else baseblob(ref,name);reject('other_original_queue_bytes_changed',lambda:N['premerge_gate'](F,require_draft=True));N['blob']=baseblob
# Review mutations are deliberately re-sealed only in private synthetic terminal07.
_,exp=N['original_check']();saved={name:(w/name).read_bytes() for name in ['RESULT.json','AUTHENTICATION_START.json','AUTHENTICATION_END.json','COLD_REPLAY.json','MANIFEST.json']}
def reseal():
 fs={q.name:N['fingerprint'](q.read_bytes()) for q in w.iterdir() if q.name!='MANIFEST.json'};b=(json.dumps({'files':fs,'explicit_public_allowlist':sorted(fs)},indent=2)+'\n').encode();(w/'MANIFEST.json').write_bytes(b);return specs[:-1]+['07:'+hashlib.sha256(b).hexdigest()]
def restore():
 for name,b in saved.items():(w/name).write_bytes(b)
mutations=[('RESULT.json','revision999',lambda j:j.update(candidate_revision=999)),('RESULT.json','revision_bool',lambda j:j.update(candidate_revision=True)),('RESULT.json','same_reviewer',lambda j:j.update(reviewer_agent_id='/root/pr946_full_package_05')),('RESULT.json','nonsequential_time',lambda j:j.update(started_utc='2026-01-01T00:00:00+00:00')),('RESULT.json','missing_prior_resolution',lambda j:j['prior_issue_resolution'].pop('FP05-OPS-001')),('RESULT.json','unverified_broad_prior',lambda j:j['prior_issue_resolution']['FP02-OPS-001'].update(verified=False)),('RESULT.json','nonempty_math_gap',lambda j:j.update(mathematical_remaining_gap_for_stated_theorem='SYNTHETIC GAP')),('RESULT.json','optional_unresolved',lambda j:j['optional_issues'].append({'id':'SYNTHETIC_OPTIONAL'})),('RESULT.json','required_unresolved',lambda j:j['required_issues'].append({'id':'SYNTHETIC_REQUIRED'})),('AUTHENTICATION_START.json','missing_original',lambda j:j['originals'].pop(next(iter(j['originals'])))),('AUTHENTICATION_END.json','bad_candidate_file_map',lambda j:j['candidate_files'].pop('research_note.tex')),('COLD_REPLAY.json','normalization_nonempty',lambda j:j.update(normalized_fields_ignored=['SYNTHETIC'])),('COLD_REPLAY.json','wrong_env2_observed',lambda j:j['modes'][3].update(observed_outer_optimization=0)),('COLD_REPLAY.json','bool_mode_observed',lambda j:j['modes'][0].update(observed_outer_optimization=False)),('COLD_REPLAY.json','whole_receipt_changed',lambda j:j['modes'][0]['receipt'].update(proof_search_turns_added=1))]
for name,label,mutate in mutations:
 j=json.loads(saved[name]);mutate(j);(w/name).write_text(json.dumps(j,indent=2)+'\n');temporary=reseal();reject('complete_review_'+label,lambda:N['review_check'](temporary,F,FP,ctx,exp));restore()
N['review_check'](specs,F,FP,ctx,exp);results.append({'case':'restored_full_seven_round_current_and_historical_contract','pass':True})
(O/'CONTRACT07_CONTROLS.json').write_text(json.dumps({'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'actual_current07_context':True,'actual_gate_and_review_functions_unstubbed':True,'terminal07_explicitly_synthetic':True,'all_services_and_Git_transport_fake':True,'actual_external_mutations':0,'cases':results,'case_count':len(results)},indent=2)+'\n');print(json.dumps({'status':'PASS','cases':len(results)}))
