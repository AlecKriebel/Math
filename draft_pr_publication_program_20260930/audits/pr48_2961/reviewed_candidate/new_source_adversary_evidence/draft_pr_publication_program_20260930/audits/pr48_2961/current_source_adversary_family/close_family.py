"""ROOT-only self-only SOURCE-adversary closer. Never run by the reviewer."""
import argparse,datetime as dt,hashlib,json,os,re,stat,sys
from pathlib import Path,PurePosixPath
F=Path(__file__).absolute().parent;R=F.parent.parents[2]
def need(v,n):
 if not v:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def regular(p):
 need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink');return p.read_bytes()
def relative(n):
 need(type(n) is str and n and '\\' not in n and '\0' not in n,'Typed path');p=PurePosixPath(n);need(not p.is_absolute() and p.as_posix()==n and not set(p.parts)&{'.','..','.git','__pycache__'},'Safe path');return n
def load(b):
 def pairs(items):
  d={}
  for k,v in items:need(k not in d,'Duplicate JSON');d[k]=v
  return d
 def nonfinite(n):raise ValueError('Nonfinite')
 return json.loads(b,object_pairs_hook=pairs,parse_constant=nonfinite)
def inventory():
 need(F.name=='current_source_adversary_family' and F.parent.name=='pr48_2961' and R==Path('/Users/alec/Documents/Math') and not F.is_symlink(),'Exact owned anchor');fs=set();ds={'.'}
 for p in F.rglob('*'):
  need(not p.is_symlink(),'No symlink member');n=relative(p.relative_to(F).as_posix())
  if stat.S_ISREG(p.stat().st_mode):fs.add(n)
  else:need(stat.S_ISDIR(p.stat().st_mode),'No special member');ds.add(n)
 need(ds=={'.'}|{q.as_posix() for n in fs for q in PurePosixPath(n).parents if str(q)!='.'},'No extra empty directory');return fs,ds
def check_bindings():
 b=load(regular(F/'AUDIT_BINDINGS.json'));need(b['production_or_helper_import_compile_execution'] is False and b['future_acceptance_approved'] is False,'SOURCE-only binding');owned=F.relative_to(R).as_posix()+'/'
 for r in b['whole_external_read_rows']:
  need(type(r['bytes']) is int and type(r['full_mode']) is int and type(r['sha256']) is str and re.fullmatch('[0-9a-f]{64}',r['sha256']) and not r['path'].startswith(owned),'Typed external row only');p=R/relative(r['path']);bb=regular(p);need(len(bb)==r['bytes'] and sha(bb)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode'],'Complete external body/full mode unchanged')
 for name in ['DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']:
  o=load(regular(F.parent/'current_preparation_family'/name));need(o['approved_by_root'] is False and o['created_utc'] is None and o['current_verdict'] is None and o['future_acceptance_approved'] is False,'SOURCE drafts remain false/null')
 need(not (F.parent/'reviewed_candidate').exists(),'No production freeze happened')
 for entry in b['completed_private_controls']:
  d=F/relative(entry['directory']);c=load(regular(d/'CAPTURE.json'));need(c==entry['complete_capture'] and type(c['pid']) is int and c['pid']==entry['expected_actual_pid'] and type(c['exit_code']) is int and c['exit_code']==entry['expected_exit_code'] and c['actual_execution'] is True and c['completed'] is True and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['stdin_supplied'] is False and c['production_import_compile_or_execution'] is False,'Complete successful/failed private actual preserved');pre=load(regular(d/'PRELAUNCH.json'));need(pre['argv']==c['argv'] and pre['source_sha256']==sha(regular(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and pre['operator_sha256']==sha(regular(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'True prelaunch bytes');need(regular(Path(c['argv'][-1]))==regular(d/'PRELAUNCH_SOURCE.py'),'Own original executed source unchanged')
  for k in ['stdout','stderr']:bb=regular(d/(k+'.bin'));need(len(bb)==c[k]['bytes'] and sha(bb)==c[k]['sha256'],'Entire actual private stream')
 d=F/'final_binding_inspection_actual_capture';c=load(regular(d/'CAPTURE.json'));pre=load(regular(d/'PRELAUNCH.json'));need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==79875 and type(c['exit_code']) is int and c['exit_code']==0 and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['stdin_supplied'] is False and c['production_import_compile_or_execution'] is False,'Actual final inspection completed before closure');need(pre['source_sha256']==sha(regular(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and pre['operator_sha256']==sha(regular(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'],'Final inspection exact prelaunch');need(regular(F/'final_binding_inspection.py')==regular(d/'PRELAUNCH_SOURCE.py'),'Final actual executed source unchanged')
 for k in ['stdout','stderr']:bb=regular(d/(k+'.bin'));need(len(bb)==c[k]['bytes'] and sha(bb)==c[k]['sha256'],'Complete final actual inspection stream')
 need(c['stderr']['bytes']==0,'Final actual inspection empty stderr');expected={x['directory'] for x in b['completed_private_controls']}|{'final_binding_inspection_actual_capture'};actual={p.parent.relative_to(F).as_posix() for p in F.rglob('CAPTURE.json')};need(actual==expected and len(actual)==9,'All nine complete actual captures accounted, no bypass')
 return b

def main():
 p=argparse.ArgumentParser();p.add_argument('--expected-report-sha256',required=True);a=p.parse_args();need(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimized checks');need(re.fullmatch('[0-9a-f]{64}',a.expected_report_sha256) and sha(regular(F/'REPORT.md'))==a.expected_report_sha256,'Exact full report');need(not (F/'MANIFEST.json').exists(),'No overwrite');fs,ds=inventory();b=check_bindings();v=load(regular(F/'VERDICT.json'));need(v['mandatory_mathematical_corrections']==[] and v['mandatory_source_corrections']==[] and v['full_target_resolved'] is False and v['future_acceptance_approved'] is False and v['new_whole_current_gate']=='PENDING' and v['report_sha256']==a.expected_report_sha256,'Scoped verdict')
 rows=[]
 for n in sorted(fs):p=F/n;bb=regular(p);p.chmod(0o444);need(regular(p)==bb and stat.S_IMODE(p.stat().st_mode)==0o444,'Own body preserved/full0444');rows.append({'path':n,'bytes':len(bb),'sha256':sha(bb),'full_mode':0o444})
 need(inventory()==(fs,ds),'Exact unchanged owned topology');m={'schema':'pr48-independent-current-source-adversary-self-only-closure/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closing_pid':os.getpid(),'self_excluded':['MANIFEST.json'],'files_count':len(rows),'files':rows,'directories':[{'path':n,'full_mode':stat.S_IMODE((F/n).stat().st_mode)} for n in sorted(ds)],'report_sha256':a.expected_report_sha256,'source_preparation_manifest_sha256':b['source_manifest_sha256'],'verdict':'PASS_STATED_UNSOLVED_PARTIAL_AND_CLOSED_SOURCE_CONTRACT','full_target_resolved':False,'inherited_context_disclosed':True,'prepared_PR48_SOURCE':False,'production_or_helper_import_compile_execution':False,'native_index_remote_changes':False,'future_acceptance_approved':False,'new_whole_current_gate':'PENDING','original_shared_attempts':'2/5','new_substantive_attempts':0,'audit_turns':0,'assigned_SOURCE_audit_completion_estimate_percent':100,'target_discovery_completion_estimate_percent':0,'complete_closing_capture_required_outside_owned_family_after_child_exit':True,'ROOT_separate_readonly_postexit_verification_required':True}
 bb=(json.dumps(m,indent=2,allow_nan=False)+'\n').encode()
 with (F/'MANIFEST.json').open('xb') as h:h.write(bb);h.flush();os.fsync(h.fileno())
 (F/'MANIFEST.json').chmod(0o444);need(inventory()[0]==fs|{'MANIFEST.json'},'Self-only exact closure');print(json.dumps({'status':'CLOSED_SOURCE_ADVERSARY_ONLY_NO_FUTURE_APPROVAL','actual_pid':os.getpid(),'manifest_sha256':sha(bb),'payload_files':len(rows),'including_self':len(rows)+1,'directories_including_root':len(ds),'full_mode':'0444','source_manifest_sha256':b['source_manifest_sha256'],'future_acceptance':False}))
if __name__=='__main__':main()
