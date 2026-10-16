"""Additional independent exact-source controls; synthetic providers only."""
import probes as H
from pathlib import Path
import json,copy,io,contextlib,traceback,types,datetime,hashlib,subprocess,sys
import compact_fixtures
D,C,B,I,M,P,A,V=H.D,H.C,H.B,H.I,H.M,H.P,H.A,H.V
ROWS=[]
def check(name,fn,fixture=None):
 start=H.utc()
 try:result=fn();row=dict(name=name,start_utc=start,end_utc=H.utc(),PASS=True,result=result)
 except Exception as e:row=dict(name=name,start_utc=start,end_utc=H.utc(),PASS=False,error=repr(e),traceback=traceback.format_exc())
 ROWS.append(row);H.js(D/'FOLLOWUP_RESULTS.json',ROWS);print(json.dumps(row),flush=True)
 if fixture and (D/'fixtures'/fixture).exists():compact_fixtures.main([fixture])

class CheckedProvider(H.Provider):
 def ancestor(self,old,new):
  todo=[new];seen=set()
  while todo:
   x=todo.pop()
   if x==old:return True
   if x in seen:continue
   seen.add(x);todo.extend(y['sha'] for y in self.commits[x]['parents'])
  return False
 def api(self,method,path,payload=None):
  if method=='PATCH' and path.startswith('git/refs/heads/'):
   branch=path.removeprefix('git/refs/heads/')
   if branch=='main' and getattr(self,'race_at_patch',False):
    old=self.refs['main'];files=self.flat(self.commits[old]['tree']['sha']);files['foreign/patch-race.txt']=b'SYNTHETIC concurrent foreign main advance\n';self.refs['main']=self.commit(self.make_tree(files),[old]);self.race_at_patch=False
   if not self.ancestor(self.refs[branch],payload['sha']):
    self.calls.append(dict(provider='github',method='PATCH',path=path,nonforce_rejected=True,global_main_intent=(self.pub/'NATIVE_MERGE_REQUEST.json').exists()))
    raise RuntimeError('SYNTHETIC provider rejects non-fast-forward nonforce ref')
  if method=='GET' and path=='git/ref/heads/main':
   self.main_reads=getattr(self,'main_reads',0)+1
   if self.main_reads==getattr(self,'advance_on_read',None):
    old=self.refs['main'];files=self.flat(self.commits[old]['tree']['sha']);files[f'foreign/advance-{len(self.commits)}.txt']=b'SYNTHETIC before-main foreign advance\n';self.refs['main']=self.commit(self.make_tree(files),[old])
  return super().api(method,path,payload)

def checked_case(name):
 r,pub,p=H.make_case(name);p.__class__=CheckedProvider;p.install();return r,pub,p
def published_prepared(name):
 r,pub,p=checked_case(name);H.stage_and_append(r,pub,p)
 with contextlib.redirect_stdout(io.StringIO()):I.main([])
 return r,pub,p

def drift_completion():
 r,pub,p=published_prepared('completion_drift_final');p.main_unknown=True
 H.rejects(lambda:M.main([]),'unknown');p.main_unknown=False
 H.DRIFT=r,pub,p
 return H.drift_completion()

def safe_advances():
 r,pub,p=published_prepared('safe_advances')
 for args in [[],['--resume-before-main']]:
  p.main_reads=0;p.advance_on_read=3
  H.rejects(lambda:M.main(args),'terminally abandoned')
  assert not (pub/'NATIVE_MERGE_REQUEST.json').exists()
 p.main_reads=0;p.advance_on_read=None
 with contextlib.redirect_stdout(io.StringIO()):M.main(['--resume-before-main'])
 receipt=json.loads((pub/'PR_MERGED.json').read_bytes());assert receipt['merge_attempt_number']==3
 assert len(receipt['prior_abandoned_attempts'])==2
 assert sum(x.get('method')=='PATCH' and x.get('path')=='git/refs/heads/main' for x in p.calls)==1
 files=p.flat(p.commits[p.refs['main']]['tree']['sha']);assert len([x for x in files if x.startswith('foreign/advance-')])==2
 p.save('safe_advances');return dict(attempts=3,terminal_abandonments=2,main_writes=1,foreign_advances_preserved=2)

def nonforce_race():
 r,pub,p=published_prepared('nonforce_race');p.race_at_patch=True
 first=H.rejects(lambda:M.main([]),'unknown');assert not (pub/'PR_MERGED.json').exists() and (pub/'NATIVE_MERGE_REQUEST.json').exists()
 before=len([x for x in p.calls if x.get('method') in ['PATCH','POST']])
 second=H.rejects(lambda:M.main(['--resume-before-main']),'already created')
 after=len([x for x in p.calls if x.get('method') in ['PATCH','POST']]);assert before==after
 p.save('nonforce_race');return dict(first=first,second=second,second_write_calls=0)

def real_helper_chain():
 folder=D/'fixtures'/'actual_helper_chain';folder.mkdir(parents=True)
 freeze_utc=H.utc()
 for name in B.HELPERS:H.put(folder/name,(D/name).read_bytes())
 rows=[H.pin(folder/name,folder) for name in B.HELPERS]
 H.js(folder/'FROZEN_SOURCES.json',dict(frozen_utc=freeze_utc,rows=rows,SYNTHETIC_NO_AUTHORITY=True))
 H.put(folder/'REPORT.md',b'SYNTHETIC parser control only. No actual review or authority.\n')
 H.js(folder/'ASSESSMENT.json',dict(schema='pr209-release-helper-assessment-v1',reviewer='SYNTHETIC_FINAL_HELPER',completed_utc=H.utc(),frozen_sources=rows,mandatory_findings=[],optional_findings=[],verdict='PASS',SYNTHETIC_NO_AUTHORITY=True))
 H.js(folder/'AUTHORED_MANIFEST.json',dict(files=[H.pin(p,folder) for p in sorted(folder.iterdir())]))
 entries=[dict(assessment=H.pin(C/'release_helpers_adversary_01/ASSESSMENT.json',C),authored_manifest=H.pin(C/'release_helpers_adversary_01/AUTHORED_MANIFEST.json',C),source_freeze=H.pin(C/'release_helpers_adversary_01/FROZEN_SOURCES.json',C),resolution=H.pin(C/'initial_review_20261016/ROOT_RELEASE_HELPER_REVIEW01_RESOLUTION.json',C),supplements=[]),dict(assessment=H.pin(folder/'ASSESSMENT.json',C),authored_manifest=H.pin(folder/'AUTHORED_MANIFEST.json',C),source_freeze=H.pin(folder/'FROZEN_SOURCES.json',C),supplements=[])]
 result=B.review_chain(C,entries,'release-helper',rows);assert result==(2,1)
 H.js(D/'ACTUAL_HELPER_CHAIN_INPUTS.json',dict(entries=entries,result=result,SYNTHETIC_NO_AUTHORITY=True))
 return dict(actual_first_review_payloads_authenticated=True,all10_actual_dispositions_bound=True,synthetic_parser_only=result)

def review_resolution_checks():
 r,pub,p=checked_case('review_resolution_controls');ctx=B.context(r);entries=copy.deepcopy(ctx['clear']['release_helper_reviews']);first=pub.parent/entries[0]['assessment']['path'];folder=first.parent
 assess=json.loads(first.read_bytes());assess.update(mandatory_findings=[dict(id='SYNTHETIC_M')],optional_findings=[dict(id='SYNTHETIC_O')],verdict='REPAIRS_REQUIRED');H.js(first,assess)
 H.js(folder/'AUTHORED_MANIFEST.json',dict(files=[H.pin(q,folder) for q in sorted(folder.iterdir()) if q.name!='AUTHORED_MANIFEST.json']))
 entries[0].update(assessment=H.pin(first,pub.parent),authored_manifest=H.pin(folder/'AUTHORED_MANIFEST.json',pub.parent))
 out={};out['missing_resolution']=H.rejects(lambda:B.review_chain(pub.parent,entries,'release-helper',ctx['clear']['release_helpers']))
 resolution=dict(review_id=assess['reviewer'],review_assessment_sha256=entries[0]['assessment']['sha256'],review_manifest_sha256=entries[0]['authored_manifest']['sha256'],utc='2026-10-15T03:30:00+00:00',resolved_findings=[dict(id='SYNTHETIC_M',status='resolved'),dict(id='SYNTHETIC_O',status='resolved')],unresolved_mandatory_findings=[],unresolved_optional_findings=[],source_bindings=ctx['clear']['release_helpers'],SYNTHETIC_NO_AUTHORITY=True)
 rp=pub.parent/'SYNTHETIC_RESOLUTION.json';H.js(rp,resolution);entries[0]['resolution']=H.pin(rp,pub.parent)
 assert B.review_chain(pub.parent,entries,'release-helper',ctx['clear']['release_helpers'])==(2,1);out['complete_resolution_passed']=True
 for key,value in [('resolved_findings',[dict(id='SYNTHETIC_M',status='resolved')]),('utc','2026-10-15T05:30:00+00:00'),('source_bindings',[])]:
  changed=copy.deepcopy(resolution);changed[key]=value;H.js(rp,changed);entries[0]['resolution']=H.pin(rp,pub.parent);out[key]=H.rejects(lambda:B.review_chain(pub.parent,entries,'release-helper',ctx['clear']['release_helpers']))
 H.js(pub.parent/'RESOLUTION_CONTROL_RESULTS.json',out);return out

def receipt_and_public_corruption():
 r,pub,p=checked_case('receipt_corruption');z,t=H.stage_and_append(r,pub,p);ctx=B.context(r);out={}
 ap=pub/'STAGE_ATTEMPT.json';raw=ap.read_bytes();putaside=pub.parent/'saved_evidence/stage_intent_retained.bin';H.put(putaside,raw);ap.unlink()
 out['missing_stage_lineage']=H.rejects(lambda:B.publication(r,pub,ctx));H.put(ap,raw);putaside.unlink()
 tp=pub/'TRACKER_VERIFIED_APPEND.json';original=tp.read_bytes()
 for key,value in [('append_count',9),('updated_range',"'Wrong'!A2:D2"),('reconciled_existing_attempt',True),('values',t['values'][:-1]+['wrong notes'])]:
  changed=json.loads(original);changed[key]=value;H.js(tp,changed);out[key]=H.rejects(lambda:B.tracker(r,pub,ctx,z))
 H.put(tp,original)
 p.bad_download=True;out['wrong_public_bytes']=H.rejects(lambda:V.verify_publication_live(r,pub,ctx),'mismatch');p.bad_download=False
 live=V.verify_publication_live(r,pub,ctx);assert len(live['actual_public_file_downloads'])==2;out['public_readonly_recovered']=True
 H.js(pub.parent/'CORRUPTION_RESULTS.json',out);p.save('corruption');return out

def stale_prepared_and_modes():
 r,pub,p=published_prepared('stale_prepared_modes');ctx=B.context(r);z=B.publication(r,pub,ctx);t=B.tracker(r,pub,ctx,z);api=I.NativeAPI(pub,'SYNTHETIC_stale_prepared',readonly=True);trees=I.NativeTrees(api);out={}
 pp=pub/'PR_PREPARED.json';original=pp.read_bytes();changed=json.loads(original);changed['included_owned_pins']=[];H.js(pp,changed)
 out['forged_prepared']=H.rejects(lambda:M.prepared_authority(r,pub,ctx,z,t,api,trees),'differs');H.put(pp,original)
 head=json.loads(original)['prepared_head'];tree=p.commits[head]['tree']['sha'];flat=p.flat(tree);path=I.PREFIX+'PROOF.md';proof=flat[path]
 # Change the exact tree entry to a symlink mode while keeping blob bytes.
 parts=path.split('/');at=tree
 for part in parts[:-1]:at=next(x['sha'] for x in p.trees[at] if x['path']==part)
 entry=next(x for x in p.trees[at] if x['path']==parts[-1]);entry['mode']='120000'
 trees=I.NativeTrees(api);out['native_mode']=H.rejects(lambda:M.prepared_authority(r,pub,ctx,z,t,api,trees),'regular file')
 entry['mode']='100644';H.js(pub.parent/'STALE_MODE_RESULTS.json',out);p.save('stale_modes');return out

def process_and_import_controls():
 results=[]
 for name in B.HELPERS:
  code=(D/name).read_bytes();compile(code,str(D/name),'exec')
  child=H.REAL_RUN([H.PY,'-B','-O',str(D/name)],capture_output=True);assert child.returncode!=0 and b'optimized'in child.stderr.lower()
  H.put(D/(name+'.optimized.stdout'),child.stdout);H.put(D/(name+'.optimized.stderr'),child.stderr)
  results.append(dict(path=name,optimized_exit=child.returncode,parsed=True))
 script="import sys,subprocess,urllib.request;sys.path.insert(0,"+repr(str(D))+");subprocess.run=lambda *a,**k:(_ for _ in ()).throw(RuntimeError('FORBIDDEN PROVIDER'));urllib.request.urlopen=subprocess.run;import release_binding,append_verified_tracker,integrate_reviewed_pr,publish_preprint,verify_and_merge,verify_published_readonly;print('ALL SIX IMPORTS INERT')"
 child=H.REAL_RUN([H.PY,'-B','-c',script],capture_output=True);assert child.returncode==0,(child.stdout,child.stderr)
 H.put(D/'IMPORT_CONTROL.stdout',child.stdout);H.put(D/'IMPORT_CONTROL.stderr',child.stderr)
 return dict(all_six=results,normal_import_exit=child.returncode)

def log_record():
 H.js(D/'INITIAL_RUN_STORAGE_INTERRUPTION.json',dict(utc=H.utc(),last_complete_group='completion_drift_setup',last_complete_utc='2026-10-16T06:47:11.964263+00:00',recorded_complete_groups=11,initial_run_complete=False,initial_wrapper_exit_and_raw_streams_unavailable=True,observed_errors=['zsh heredoc creation ENOSPC before Python','apply_patch could not create compactor','own ZIP open raised OSError Errno28'],completion_drift_probe_incomplete=True,no_defect_inferred_from_incomplete_probe=True,all_owned_fixtures_subsequently_archived_exact_crc_and_every_body=True,case_completion_percent=65,audit_completion_percent=70))
 with (D/'RESEARCH_LOG.md').open('a') as f:f.write('- '+H.utc()+': Initial11 completed control groups preserved, including full419-pin release. ENOSPC interrupted next probe; no conclusion inferred. All own generated fixture trees were losslessly archived with exact membership/every-body/CRC checks before removal. Case65%; audit70%.\n')

if __name__=='__main__':
 log_record()
 check('completion_drift_after_long_public_reads',drift_completion,'completion_drift_final')
 check('actual_first_helper_seal_and_all10_resolution_compatibility',real_helper_chain,'actual_helper_chain')
 check('optional_mandatory_disposition_chronology_repair_pins',review_resolution_checks,'review_resolution_controls')
 check('publication_tracker_corruption_and_public_recovery',receipt_and_public_corruption,'receipt_corruption')
 check('prepared_pin_forgery_and_native_symlink_mode',stale_prepared_and_modes,'stale_prepared_modes')
 check('safe_repeated_foreign_main_advances_before_once_intent',safe_advances,'safe_advances')
 check('last_moment_nonforce_main_race_forbids_second_write',nonforce_race,'nonforce_race')
 check('inert_imports_and_all6_optimized_guards',process_and_import_controls)
 H.js(D/'FOLLOWUP_SUMMARY.json',dict(utc=H.utc(),groups=len(ROWS),passed=sum(x['PASS'] for x in ROWS),all_expected_outcomes=all(x['PASS'] for x in ROWS),synthetic_only=True,no_release_authority=True))
 sys.exit(0 if all(x['PASS'] for x in ROWS) else 1)
