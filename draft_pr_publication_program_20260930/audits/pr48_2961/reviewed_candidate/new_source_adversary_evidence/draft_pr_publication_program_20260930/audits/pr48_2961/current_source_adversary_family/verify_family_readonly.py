"""Separate ROOT readonly verification after this family's actual closer has exited."""
import argparse,hashlib,json,os,re,stat,sys
from pathlib import Path,PurePosixPath
F=Path(__file__).absolute().parent;R=F.parent.parents[2]
def need(v,n):
 if not v:raise ValueError(n)
def sha(b):return hashlib.sha256(b).hexdigest()
def regular(p):
 need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink');return p.read_bytes()
def load(b):
 def pairs(items):
  d={}
  for k,v in items:need(k not in d,'Duplicate JSON');d[k]=v
  return d
 def nonfinite(n):raise ValueError('Nonfinite')
 return json.loads(b,object_pairs_hook=pairs,parse_constant=nonfinite)
def safe(n):
 need(type(n) is str and n and '\\' not in n and '\0' not in n,'Path text');p=PurePosixPath(n);need(not p.is_absolute() and str(p)==n and not set(p.parts)&{'.','..','.git','__pycache__'},'Canonical path');return n
def main():
 p=argparse.ArgumentParser();p.add_argument('--expected-manifest-sha256',required=True);a=p.parse_args();need(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimized checks');need(F.name=='current_source_adversary_family' and F.parent.name=='pr48_2961' and R==Path('/Users/alec/Documents/Math') and not F.is_symlink(),'Exact owned anchor');bb=regular(F/'MANIFEST.json');need(sha(bb)==a.expected_manifest_sha256 and re.fullmatch('[0-9a-f]{64}',a.expected_manifest_sha256),'Actual externally supplied closure SHA');m=load(bb);need(m['schema']=='pr48-independent-current-source-adversary-self-only-closure/v1' and m['self_excluded']==['MANIFEST.json'] and type(m['files_count']) is int and len(m['files'])==m['files_count'] and type(m['actual_closing_pid']) is int and m['actual_closing_pid']!=os.getpid() and m['future_acceptance_approved'] is False and m['production_or_helper_import_compile_execution'] is False and m['new_whole_current_gate']=='PENDING','True scoped self-only closed schema')
 fs=set();ds={'.'}
 for pp in F.rglob('*'):
  need(not pp.is_symlink(),'No symlink');n=safe(pp.relative_to(F).as_posix())
  if stat.S_ISREG(pp.stat().st_mode):fs.add(n)
  else:need(stat.S_ISDIR(pp.stat().st_mode),'No special member');ds.add(n)
 need(ds=={'.'}|{q.as_posix() for n in fs for q in PurePosixPath(n).parents if str(q)!='.'},'No empty/extra directory');need(ds=={r['path'] for r in m['directories']} and fs=={r['path'] for r in m['files']}|{'MANIFEST.json'} and len(fs)==m['files_count']+1,'Exact closed topology')
 total=len(bb)
 for rr in m['files']:
  need(set(rr)=={'path','bytes','sha256','full_mode'} and type(rr['bytes']) is int and type(rr['full_mode']) is int and rr['full_mode']==0o444,'Typed full mode row');pp=F/safe(rr['path']);b=regular(pp);need(len(b)==rr['bytes'] and sha(b)==rr['sha256'] and stat.S_IMODE(pp.stat().st_mode)==0o444,'Full closed body/mode unchanged');total+=len(b)
 need(stat.S_IMODE((F/'MANIFEST.json').stat().st_mode)==0o444 and sha(regular(F/'REPORT.md'))==m['report_sha256'],'Manifest/report exact');
 for d in m['directories']:need(type(d['full_mode']) is int and stat.S_IMODE((F/d['path']).stat().st_mode)==d['full_mode'],'Full directory mode')
 b=load(regular(F/'AUDIT_BINDINGS.json'));need(b['source_manifest_sha256']==m['source_preparation_manifest_sha256'],'External closed source pin')
 for rr in b['whole_external_read_rows']:
  pp=R/safe(rr['path']);raw=regular(pp);need(len(raw)==rr['bytes'] and sha(raw)==rr['sha256'] and stat.S_IMODE(pp.stat().st_mode)==rr['full_mode'],'Full external body/mode unchanged')
 for entry in b['completed_private_controls']:
  d=F/safe(entry['directory']);c=load(regular(d/'CAPTURE.json'));need(c==entry['complete_capture'] and type(c['pid']) is int and c['pid']==entry['expected_actual_pid'] and type(c['exit_code']) is int and c['exit_code']==entry['expected_exit_code'] and c['actual_execution'] is True and c['completed'] is True and c['operator_unchanged'] is True and c['source_unchanged'] is True,'All failed and successful actual captures preserved')
  for k in ['stdout','stderr']:raw=regular(d/(k+'.bin'));need(len(raw)==c[k]['bytes'] and sha(raw)==c[k]['sha256'],'Complete actual stream')
 d=F/'final_binding_inspection_actual_capture';c=load(regular(d/'CAPTURE.json'));need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==79875 and type(c['exit_code']) is int and c['exit_code']==0 and c['source_unchanged'] is True and c['operator_unchanged'] is True and c['production_import_compile_or_execution'] is False,'Final actual inspection complete');need(sha(regular(d/'PRELAUNCH_SOURCE.py'))==c['source_sha256'] and sha(regular(d/'PRELAUNCH_OPERATOR.py'))==c['operator_sha256'] and regular(F/'final_binding_inspection.py')==regular(d/'PRELAUNCH_SOURCE.py'),'Final inspection source binding')
 for k in ['stdout','stderr']:raw=regular(d/(k+'.bin'));need(len(raw)==c[k]['bytes'] and sha(raw)==c[k]['sha256'],'Final complete streams')
 expected={x['directory'] for x in b['completed_private_controls']}|{'final_binding_inspection_actual_capture'};need({p.parent.relative_to(F).as_posix() for p in F.rglob('CAPTURE.json')}==expected and len(expected)==9,'All nine actual captures covered')
 for name in ['DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']:
  o=load(regular(F.parent/'current_preparation_family'/name));need(o['approved_by_root'] is False and o['created_utc'] is None and o['current_verdict'] is None,'Unapproved source drafts remain')
 need(not (F.parent/'reviewed_candidate').exists(),'No future freeze');print(json.dumps({'status':'PASS_READONLY_CLOSED_SOURCE_ADVERSARY_ONLY','actual_pid':os.getpid(),'closing_pid':m['actual_closing_pid'],'manifest_sha256':sha(bb),'payload_files':m['files_count'],'including_self':len(fs),'complete_owned_bytes':total,'whole_external_body_count':len(b['whole_external_read_rows']),'future_acceptance':False}))
if __name__=='__main__':main()
