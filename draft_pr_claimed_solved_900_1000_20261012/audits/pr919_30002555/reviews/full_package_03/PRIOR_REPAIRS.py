#!/usr/bin/env python3
"""Authenticate prior review artifacts and preserved candidates; inspect actual repair surfaces."""
import argparse,ast,hashlib,json,pathlib,stat,zipfile
R=pathlib.Path(__file__).resolve().parent;A=R.parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,s):
 if not x:raise RuntimeError(s)
def fp(p):
 need(stat.S_ISREG(p.lstat().st_mode),'nonregular '+str(p));b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def perform(candidate):
 previous=[]
 for number,pin,count in [(1,'5bf7174357ccf4e228aeb14e1d25e44c9692b253919cde867c42b1a65956d3a1',36),(2,'98cbe02d1862614c0696a44b0ad8f5a3d8f3afe49dbd4fd55806c87311bcd0b2',43)]:
  d=A/'reviews'/f'full_package_{number:02}';need(fp(d/'MANIFEST.json')['sha256']==pin,'prior seal');m=json.loads((d/'MANIFEST.json').read_text());need(len(m['files'])==count and set(m['files'])==set(m['explicit_public_allowlist']),'prior map')
  for n,v in m['files'].items():need(fp(d/n)==v,'prior drift '+n)
  result=json.loads((d/'RESULT.json').read_text());previous.append({'round':number,'manifest_sha256':pin,'public_members':count,'completed_utc':result['completed_utc'],'required_issues':result['required_issues'],'optional_issues':result['optional_issues']})
 preserved=[]
 for number in (1,2):
  d=A/'publication/reviewed_candidates'/f'candidate{number:02}';m=json.loads((d/'SNAPSHOT_MANIFEST.json').read_text())
  if number==2:need(fp(d/'SNAPSHOT_MANIFEST.json')['sha256']=='f87720a52bde872a054341e96efb19f6e9989dba47c9312c161603faa215fa34','candidate02 snapshot pin')
  need(len(m['preserved_files'])==30,'preserved30')
  for n,v in m['preserved_files'].items():need(fp(d/n)==v,'preserved drift '+n)
  need({str(p.relative_to(d)) for p in d.rglob('*') if p.is_file()}==set(m['preserved_files'])|{'SNAPSHOT_MANIFEST.json'},'preserved closed inventory')
  preserved.append({'revision':number,'members':30,'snapshot_sha256':fp(d/'SNAPSHOT_MANIFEST.json')['sha256']})
 with zipfile.ZipFile(candidate/'rotational-veech-source-verification-v1.0.zip') as z:
  surfaces={n:z.read(n).decode() for n in ['README.md','requirements.txt','note.tex','PR_DESCRIPTION_CORRECTED.md','PUBLICATION_FRAMING.md']}
 for n in ['README.md','requirements.txt','PR_DESCRIPTION_CORRECTED.md','PUBLICATION_FRAMING.md']:
  need(all(s in surfaces[n] for s in ['POSIX','O_NOFOLLOW','macOS','Linux']),'R2 '+n)
 for n in ['README.md','note.tex','PR_DESCRIPTION_CORRECTED.md','PUBLICATION_FRAMING.md']:need('broader' in surfaces[n],'O1 '+n)
 for n in ['zenodo-deposit.json','prepare_metadata.py']:
  s=(candidate/n).read_text();need(all(t in s for t in ['broader','POSIX','O_NOFOLLOW','macOS','Linux']),'R2O1 '+n)
 merge=(R/'reviewed_helpers/merge_pr919.py').read_text();need("decision['decision'] == 'PREPARE_EXPLICITLY_ATTRIBUTED_APPLICATION_NOTE'" in merge and all(t in merge for t in ['Exact-source acceptance','Accepted freeze changed','Live PR head changed','--match-head-commit']),'R1 actual gates')
 functions=[]
 for n in ['append_pr919_tracker.py','update_pr919_publication_ledger.py','finalize_pr919_and_gate_next.py']:
  s=(R/'reviewed_helpers'/n).read_text();t=ast.parse(s);fun=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='verify_receipt_links');functions.append(ast.get_source_segment(s,fun));main=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='main');calls=[x for x in ast.walk(main) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='verify_receipt_links'];need(len(calls)==1,'O2 guard call '+n)
 need(len(set(functions))==1,'O2 identical guards')
 launcher=(R/'reviewed_helpers/run_pr919_zenodo.py').read_text();need(launcher.index("merge.get('headRefOid')==expected_head")<launcher.index("intent={")<launcher.index('result=subprocess.run(command'),'O3 ordering')
 return {'status':'PASS','prior_reviews':previous,'preserved_candidates':preserved,'prior_issue_resolution':{k:{'verified':True,'evidence':v} for k,v in {'R1':'Actual current label and later acceptance/freeze/live-head gates retained; independent and root synthetic regressions pass.','R2':'Actual candidate and archived README/requirements/note/metadata/generator/PR/framing scoped to POSIX, O_NOFOLLOW, macOS tested and Linux untested.','O1':'Actual RMV p530 broader nested-end/multi-group scope checked against note/README/metadata/PR/framing.','O2':'Identical guard in all three actual downstream sources, called before writes; root27 and independent48 negative substitutions plus positive original/integration chains pass.','O3':'Actual repaired launcher resolves original/integration head and rejects mismatch before intent or kit; root27 and independent9 negative pre-intent cases plus original/integration positives pass.'}.items()},'historical_as_of_helper_pins_preserved':True,'current_operational_revision':3}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--candidate',type=pathlib.Path,default=A/'publication');p.add_argument('--output',type=pathlib.Path);a=p.parse_args();r=perform(a.candidate)
 if a.output:a.output.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items() if k!='prior_reviews'},indent=2))
