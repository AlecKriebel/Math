#!/usr/bin/env python3
"""Replay artifact pins, the actual patch and algebra; optionally check complete corpora.
The external graph-girth theorem and mathematical reasoning are not machine-certified.
No files are downloaded, uploaded or published. No input corpus contents are printed.
"""
import argparse,hashlib,json,shutil,subprocess,tempfile,zipfile
from fractions import Fraction
from pathlib import Path
H=lambda b:hashlib.sha256(b).hexdigest()
B=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--catalog');p.add_argument('--problems');p.add_argument('--reports');p.add_argument('--sources-directory');p.add_argument('--output');a=p.parse_args()
result={'artifact_checks':{},'patch_replay':{},'arithmetic_checks':{},'corpus_checks':{'performed':False},'source_checks':{'performed':False},'limitations':['No machine certification of the LUW girth theorem or of manuscript proofs.','Arithmetic checks are consistency checks, not a substitute for an infinite-family proof.']}
archives={}
for stem in ['VERIFIED_PRIOR','CLARIFIED']:
 m=json.loads((B/('DENSE_CYCLES_2193_'+stem+'_EXTERNAL_MANIFEST.json')).read_text());z=B/m['archive']['name'];b=z.read_bytes();assert len(b)==m['archive']['bytes'] and H(b)==m['archive']['sha256'];members={}
 with zipfile.ZipFile(z) as f:
  assert len(f.namelist())==len(set(f.namelist()))==5;assert sorted(f.namelist())==sorted(x['path'] for x in m['members'])
  for x in m['members']:
   assert '/' not in x['path'] and x['path'] not in ['.','..'];v=f.read(x['path']);assert len(v)==x['bytes'] and H(v)==x['sha256'];members[x['path']]=v
 archives[stem]=members;result['artifact_checks'][stem]={'archive':m['archive'],'all_five_members_verified':True}
with tempfile.TemporaryDirectory() as d:
 d=Path(d)
 for n,b in archives['VERIFIED_PRIOR'].items():(d/n).write_bytes(b)
 r=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(B/'CLARIFICATIONS.patch')],cwd=d,text=True,capture_output=True)
 assert r.returncode==0,r.stderr;assert set(x.name for x in d.iterdir())==set(archives['CLARIFIED'])
 for n,b in archives['CLARIFIED'].items():assert (d/n).read_bytes()==b
 result['patch_replay']={'passed':True,'all_five_derivative_members_byte_equal':True,'changed_files':[n for n in sorted(archives['CLARIFIED']) if archives['CLARIFIED'][n]!=archives['VERIFIED_PRIOR'][n]],'patch_sha256':H((B/'CLARIFICATIONS.patch').read_bytes())}
for q in [2,3,5,7,11,101,1009]:
 n=2*q**5;m=q**6;delta=Fraction(m,n*n);assert 2*m==n*q;assert delta==Fraction(1,4*q**4);assert delta**2*n*n==Fraction(q*q,4);assert delta**3*n*n==Fraction(1,16*q*q)
result['arithmetic_checks']={'passed':True,'density_normalization':'m/n^2','symbolic_formula_review':'n=2q^5; m=q^6; delta=1/(4q^4); delta^2*n^2=q^2/4; delta^3*n^2=1/(16q^2)','finite_sanity_checks_q':[2,3,5,7,11,101,1009]}
if any([a.catalog,a.problems,a.reports]):
 assert all([a.catalog,a.problems,a.reports]),'Supply all three corpus files.'
 meta=json.loads((B/'INPUT_VERIFICATION.json').read_text());objs=[]
 for v,x in zip([a.catalog,a.problems,a.reports],meta['corpora']):
  b=Path(v).read_bytes();assert len(b)==x['bytes'] and H(b)==x['sha256'];objs.append(json.loads(b))
 c,ps,reports=objs;cs=[x for x in c if str(x.get('id'))=='2193'];rs=[x for x in ps if str(x.get('id'))=='2193'];assert len(cs)==len(rs)==1;r=rs[0];assert cs[0]['rank']==898 and r['problem_number']=='EP-584';assert H(r['statement'].encode())==meta['statement_sha256'];assert r['problem_number'] not in reports;assert H(json.dumps([r,reports.get(r['problem_number'],{})],sort_keys=True).encode())==meta['pair_sha256'];assert cs[0]['statement_hash']==meta['statement_sha256'] and cs[0]['review_hash']==meta['pair_sha256']
 result['corpus_checks']={'performed':True,'all_three_complete_files_verified':True,'unique_exact_record':True,'catalog_rank':898,'report_key_present':False,'effective_report_empty':True,'statement_hash_match':True,'complete_pair_hash_match':True,'dataset_contents_emitted':False}
if a.sources_directory:
 meta=json.loads((B/'SOURCE_AUDIT.json').read_text());files={H(f.read_bytes()):(f.stat().st_size,f) for f in Path(a.sources_directory).glob('*.pdf')}
 for r in meta['sources']:assert r['sha256'] in files and files[r['sha256']][0]==r['bytes']
 result['source_checks']={'performed':True,'all_five_source_pdf_pins_match':True,'source_contents_emitted':False}
result['passed']=True
s=json.dumps(result,indent=2,sort_keys=True)+'\n'
if a.output:Path(a.output).write_text(s)
print(s)
