#!/usr/bin/env python3
"""Revision1 focused tests; isolated copies, no release or source mutation."""
from pathlib import Path
import copy,datetime,hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'workflow_proposal'
AUDIT=ROOT.parents[1]
ANCHOR='202cf1602c1cfc9e9458e567fa97e0004a7a5c1f76380a07e10e83ff616ecd7d'
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 spec=importlib.util.spec_from_file_location('focused_'+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def reject(fn,label):
 try:fn()
 except (RuntimeError,ValueError,FileNotFoundError,KeyError):return label
 raise RuntimeError('Unexpected acceptance '+label)
def authenticate_base():
 need(sha(BASE/'FINAL_AUTHORED_FREEZE.json')==ANCHOR,'Outside base seal differs');f=json.loads((BASE/'FINAL_AUTHORED_FREEZE.json').read_text())
 for e in f['authored_files']:
  p=BASE/e['path'];need(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'Immutable base drift '+str(p))
 return len(f['authored_files'])
def source_replay(v,folder):
 source=AUDIT/'reviews/source_question_family';raw='reviews/source_question_family/finite_checks.py';result='reviews/source_question_family/finite_checks.json';folder.mkdir(parents=True);(folder/Path(raw).parent).mkdir(parents=True)
 before={n:sha(source/n) for n in ['manifest.json','finite_checks.py','finite_checks.json']}
 for n in ['finite_checks.py','finite_checks.json']:shutil.copyfile(source/n,folder/'reviews/source_question_family'/n)
 spec={'program':raw,'mode':'normal','result':result,'output_mode':'file','scope':'Actual source-family finite diagnostics only; not asymptotic proof.','layout':'isolated','arguments':[],'comparison':'json_ignore_start_end_utc'};context={'diagnostic_replays':[spec]};expected=folder/result;original=json.loads(expected.read_text());v.replay_diagnostics(folder,context)
 for fields in [['run_started_utc'],['run_completed_utc'],['run_started_utc','run_completed_utc']]:
  changed=copy.deepcopy(original)
  for field in fields:changed[field]='SYNTHETIC REPLACEMENT OF ALLOWED TOP-LEVEL RUNTIME ONLY'
  save(expected,changed);v.replay_diagnostics(folder,context)
 rejected=[]
 for label,mutate in [('non_time_count',lambda x:x['exact_enumeration'].update(graphs_enumerated_once_per_n=-1)),('script_digest',lambda x:x.update(script_sha256='0'*64)),('status',lambda x:x.update(status='changed')),('other_top_level_at_utc',lambda x:x.update(at_utc='MUST_REMAIN')),('other_top_level_run_utc',lambda x:x.update(run_utc='MUST_REMAIN')),('other_top_level_python',lambda x:x.update(python='MUST_REMAIN')),('other_top_level_optimization',lambda x:x.update(optimization=999)),('nested_start',lambda x:x['exact_enumeration'].update(run_started_utc='MUST_REMAIN')),('nested_end',lambda x:x['exact_enumeration'].update(run_completed_utc='MUST_REMAIN'))]:
  changed=copy.deepcopy(original);mutate(changed);save(expected,changed);rejected.append(reject(lambda:v.replay_diagnostics(folder,context),label))
 save(expected,original);need(before=={n:sha(source/n) for n in before},'Frozen source artifacts were edited');need(sha(folder/raw)==before['finite_checks.py'],'Scratch source copy bytes changed')
 return {'actual_immutable_source_copied_and_replayed_normal_only':True,'actual_code_sha256':before['finite_checks.py'],'actual_result_sha256':before['finite_checks.json'],'all_original_source_artifacts_unchanged':True,'accepted_timestamp_variations':['start_only','end_only','both'],'rejected_non_time_or_other_runtime_fields':rejected,'new_exclusion_scope':'Only top-level run_started_utc and run_completed_utc.'}
def semantics(v,folder):
 folder.mkdir(parents=True);p=folder/'program.py';base={'at_utc':'A','run_utc':'R','python':'P','optimization':0,'run_started_utc':'S','run_completed_utc':'E','payload':{'run_started_utc':'NS','run_completed_utc':'NE','value':1}}
 p.write_text('import json\nprint(json.dumps('+repr(base)+'))\n');expected=folder/'result.json';save(expected,base);spec={'program':'program.py','mode':'normal_O_OO','result':'result.json','output_mode':'stdout','scope':'Synthetic exact comparison semantics only.','layout':'isolated','arguments':[],'comparison':'json_exact'};accepted=[];rejected=[]
 for comparison,keys in [('json_ignore_runtime',['run_utc','python','optimization']),('json_ignore_at_utc',['at_utc']),('json_ignore_start_end_utc',['run_started_utc','run_completed_utc'])]:
  changed=copy.deepcopy(base)
  for key in keys:changed[key]='ALLOWED'
  save(expected,changed);spec['comparison']=comparison;v.replay_diagnostics(folder,{'diagnostic_replays':[spec]});accepted.append(comparison)
  changed=copy.deepcopy(base);changed['run_started_utc' if comparison!='json_ignore_start_end_utc' else 'run_utc']='REJECT';save(expected,changed);rejected.append(reject(lambda:v.replay_diagnostics(folder,{'diagnostic_replays':[spec]}),comparison+'_does_not_expand'))
 for comparison in ['json_exact','bytes_exact']:
  changed=copy.deepcopy(base);changed['run_started_utc']='REJECT';save(expected,changed);spec['comparison']=comparison;rejected.append(reject(lambda:v.replay_diagnostics(folder,{'diagnostic_replays':[spec]}),comparison+'_timestamp_change'))
 return {'established_comparison_semantics_retained':True,'accepted':accepted,'negative_controls':rejected}
def staged_base_tests(folder):
 stage=folder/'staged';stage.mkdir(parents=True)
 for name in ['prepare_package.py','build_package.py','compile_note.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py','deposit_coordinator.py']:shutil.copyfile(BASE/name,stage/name)
 shutil.copyfile(ROOT/'verification_verify.py',stage/'verification_verify.py');w=load(stage/'workflow_regression.py');w.ROOT=stage;w.COORDINATOR=stage/'deposit_coordinator.py';w.REPORT_ROOT=ROOT
 w.DEPLOY={name:('verification_verify.py' if name=='verification/verify.py' else name) for name in w.NAMES};f=w.fixture(folder/'fixture');v=f['v'];cp=f['audit']/'CURRENT_PR1262_CONTEXT.json';context=copy.deepcopy(f['context']);context['diagnostic_replays'][0]['comparison']='json_ignore_start_end_utc';save(cp,context);v.load_context(f['audit'],f['pub']);save(cp,f['context'])
 # Actual current family prefix registered explicitly; a nonpriority review must
 # not stand in even with a valid manifest and all its matching portable bytes.
 legacy=copy.deepcopy(f['context']);reg=next(x for x in legacy['authored_freezes'] if x['path'].startswith('priority/'));src=f['audit']/reg['base'];dest=f['audit']/'reviews/priority_triangle';dest.mkdir(parents=True)
 for q in src.iterdir():shutil.copyfile(q,dest/q.name)
 current=copy.deepcopy(legacy);currentreg=next(x for x in current['authored_freezes'] if x['path'].startswith('priority/'));oldbase=currentreg['base'];currentreg.update(path='reviews/priority_triangle/MANIFEST.json',base='reviews/priority_triangle');shutil.copyfile(dest/'FREEZE_MANIFEST.json',dest/'MANIFEST.json');currentreg['sha256']=sha(dest/'MANIFEST.json')
 current['portable_files']=[e for e in current['portable_files'] if not e['path'].startswith(oldbase+'/')]
 for q in sorted(dest.iterdir()):
  if q.name=='FREEZE_MANIFEST.json':continue
  current['portable_files'].append({'path':q.relative_to(f['audit']).as_posix(),'bytes':q.stat().st_size,'sha256':sha(q),'role':'authored_evidence'})
 save(cp,current);v.load_context(f['audit'],f['pub']);v.authenticate_nested_manifests(f['audit'],current['authored_freezes']);rejected=[]
 for name in ['ordinary_review','nonpriority_triangle']:
  substitute=copy.deepcopy(current);record=next(x for x in substitute['authored_freezes'] if x['path'].startswith('reviews/priority_'));target=f['audit']/'reviews'/name;shutil.copytree(dest,target);record.update(base='reviews/'+name,path='reviews/'+name+'/MANIFEST.json');record['sha256']=sha(target/'MANIFEST.json');rejected.append(reject(lambda:v.authenticate_nested_manifests(f['audit'],substitute['authored_freezes']),name+'_cannot_substitute'))
 absent=copy.deepcopy(current['authored_freezes']);absent=[e for e in absent if not e['path'].startswith('reviews/priority_')];rejected.append(reject(lambda:v.authenticate_nested_manifests(f['audit'],absent),'missing_priority_family'))
 wrong=copy.deepcopy(current['authored_freezes']);next(x for x in wrong if x['path'].startswith('reviews/priority_'))['sha256']='0'*64;rejected.append(reject(lambda:v.authenticate_nested_manifests(f['audit'],wrong),'priority_immutable_anchor'))
 wrong=copy.deepcopy(current['authored_freezes']);next(x for x in wrong if x['path'].startswith('reviews/priority_'))['entries_key']='guessed';rejected.append(reject(lambda:v.authenticate_nested_manifests(f['audit'],wrong),'priority_explicit_schema'))
 save(cp,legacy);v.authenticate_nested_manifests(f['audit'],legacy['authored_freezes'])
 # Run the actual complete base suite, with only the changed verifier copied.
 run=subprocess.run([sys.executable,'-B',str(stage/'workflow_regression.py'),'--worker'],capture_output=True,text=True);need(run.returncode==0,run.stderr);base=json.loads(run.stdout)
 return {'new_comparison_accepted_by_actual_complete_context_contract':True,'registered_reviews_priority_triangle_accepted':True,'legacy_priority_family_retained':True,'negative_controls':rejected,'complete_unchanged_base_regression_with_revised_verifier':base}
def worker():
 count=authenticate_base();bindings=json.loads((ROOT/'INPUT_BINDINGS.json').read_text())['inputs']
 for e in bindings:
  p=Path(e['path']);need(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'Read-only input drift')
 with tempfile.TemporaryDirectory(prefix='revision1-focused-',dir=ROOT/'_local') as tmp:
  folder=Path(tmp);v=load(ROOT/'verification_verify.py');source=source_replay(v,folder/'actual-source');sem=semantics(v,folder/'semantics');base=staged_base_tests(folder/'base')
 need(authenticate_base()==count,'Base changed')
 for e in bindings:
  p=Path(e['path']);need(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'Read-only input changed')
 return {'status':'PASS','base19members_authenticated_before_and_after':True,'source_replay':source,'comparison_semantics':sem,'base_and_priority_prefix':base,'scope':'Offline synthetic fixtures and actual source-family finite replay only; no mathematical acceptance or live service/Git mutation.'}
def main():
 if '--worker' in sys.argv:print(json.dumps(worker(),sort_keys=True));return
 runs=[]
 for flags in [[],['-O'],['-OO']]:
  r=subprocess.run([sys.executable,'-B',*flags,str(Path(__file__).resolve()),'--worker'],capture_output=True,text=True);need(r.returncode==0,r.stderr);runs.append({'flags':flags,'result':json.loads(r.stdout)})
 need(all(x['result']==runs[0]['result'] for x in runs),'Optimization-dependent revision behavior');result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','all_modes_identical':True,'base_proposal_manifest_sha256':ANCHOR,'changed_verifier_sha256':sha(ROOT/'verification_verify.py'),'runs':runs};save(ROOT/'FOCUSED_TEST_RECEIPT.json',result);print(json.dumps({'status':'PASS','all_modes_identical':True,'receipt_sha256':sha(ROOT/'FOCUSED_TEST_RECEIPT.json')},indent=2))
if __name__=='__main__':main()
