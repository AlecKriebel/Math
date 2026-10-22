#!/usr/bin/env python3
"""Build explicit deterministic research/verification and portable upload archives."""
import hashlib,json,pathlib,subprocess,sys,zipfile
HERE=pathlib.Path(__file__).resolve().parent
AUDIT=HERE.parent
def sha(raw):return hashlib.sha256(raw).hexdigest()
def dump(value):return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
def stable_geometry(value):
 return {k:v for k,v in value.items() if k not in {'checked_at_utc','python_version','optimization_mode'}}
def stable_curvature(value):return {k:v for k,v in value.items() if k!='python'}
def archive(path,members):
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for name,raw in sorted(members.items()):
   info=zipfile.ZipInfo(name,date_time=(2026,10,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,raw)
def run(script,opt=False):
 p=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(HERE/'verification'/script)],capture_output=True,text=True)
 if p.returncode:raise SystemExit(p.stderr)
 return json.loads(p.stdout)
def main():
 ver=HERE/'verification';ver.mkdir(exist_ok=True)
 for src,name in [('reviews/geometry_01/check_geometry.py','check_geometry.py'),('reviews/curvature_01/curvature_reproduction.py','curvature_reproduction.py')]:
  (ver/name).write_bytes((AUDIT/src).read_bytes())
 geometry=stable_geometry(run('check_geometry.py'))
 if geometry!=stable_geometry(run('check_geometry.py',True)):raise SystemExit('Optimized geometry checks differ')
 curvature=stable_curvature(run('curvature_reproduction.py'))
 bad=subprocess.run([sys.executable,'-B','-O',str(ver/'curvature_reproduction.py')],capture_output=True,text=True)
 if bad.returncode==0 or 'requires enabled assertions' not in bad.stderr.lower():raise SystemExit('Curvature verifier optimization guard did not reject')
 expected={'geometry':geometry,'curvature':curvature,'geometry_optimized':'same checks PASS','curvature_optimized':'rejected at startup'}
 (ver/'expected_results.json').write_bytes(dump(expected))
 (HERE/'LICENSE.txt').write_text('Copyright 2026 Alec Kriebel. Original authored materials licensed under Creative Commons Attribution4.0 International: https://creativecommons.org/licenses/by/4.0/. Third-party works retain their licenses.\n')
 members={}
 for name in ['main.tex','README.md','LICENSE.txt','output/pdf/negative-curvature-cone.pdf','verification/check_geometry.py','verification/curvature_reproduction.py','verification/expected_results.json']:
  members[name]=(HERE/name).read_bytes()
 if not members['output/pdf/negative-curvature-cone.pdf'].startswith(b'%PDF-'):raise SystemExit('Final PDF missing')
 for src,dst in [
  ('ROOT_MATHEMATICAL_CHECK.md','audits/ROOT_MATHEMATICAL_CHECK.md'),
  ('ROOT_PRIORITY_CHECK.md','audits/ROOT_PRIORITY_CHECK.md'),
  ('reviews/geometry_01/REPORT.md','audits/geometry_01/REPORT.md'),
  ('reviews/geometry_01/SOURCES.json','audits/geometry_01/SOURCES.json'),
  ('reviews/geometry_01/results.json','audits/geometry_01/results.json'),
  ('reviews/geometry_01/results_optimized.json','audits/geometry_01/results_optimized.json'),
  ('reviews/curvature_01/ADVERSARIAL_REPORT.md','audits/curvature_01/ADVERSARIAL_REPORT.md'),
  ('reviews/curvature_01/results.json','audits/curvature_01/results.json'),
  ('reviews/curvature_01/execution.json','audits/curvature_01/execution.json'),
 ]:members[dst]=(AUDIT/src).read_bytes()
 priority=AUDIT/'reviews/priority_01'
 report=priority/'PRIORITY_AUDIT.md'
 if not report.exists():raise SystemExit('Final priority audit required')
 members['audits/priority_01/PRIORITY_AUDIT.md']=report.read_bytes()
 for name in ['QUERY_LEDGER.json','SEARCH_LEDGER.md','SOURCE_LEDGER.json','SOURCE_LEDGER.md','COMPARISON_MATRIX.md','retrieval_metadata.json','additional_retrieval_metadata.json','supplemental_retrieval_metadata.json','remainder_check.txt']:
  path=priority/name
  if path.exists():members['audits/priority_01/'+name]=path.read_bytes()
 members['PROVENANCE.json']=dump({'problem_id':30003439,'problem_alias':'OWR-15219-008','source_pr':'https://github.com/AlecKriebel/Math/pull/1108','source_head_sha':'148130ab93ab46a3459d7bc98a11a1ca79052d65','source_proof_sha256':'9577476ee2c0fd2e3d12ab1265201d8b99f6ef50a9060e245c46f872dd673302','analytic_proof':'main.tex','computation_role':'Exact displayed identities plus supplemental rational tests; universal proof in note.','review_status':'AI-assisted; unrefereed; no external human peer review or formal certification.'})
 source_manifest={name:{'bytes':len(raw),'sha256':sha(raw)} for name,raw in sorted(members.items())}
 members['SOURCE_MANIFEST.json']=dump(source_manifest)
 out=HERE/'output';out.mkdir(exist_ok=True)
 source=out/'negative-curvature-cone-source-and-verification.zip';archive(source,members)
 metadata=json.loads((HERE/'zenodo-metadata.json').read_text());manifest=json.loads((HERE/'zenodo-deposit.json').read_text())
 if manifest['metadata']!=metadata:raise SystemExit('Deposit metadata differs')
 portable=dict(manifest);portable['files']=[{'path':'negative-curvature-cone.pdf'},{'path':source.name}]
 kit={'negative-curvature-cone.pdf':members['output/pdf/negative-curvature-cone.pdf'],source.name:source.read_bytes(),'zenodo-metadata.json':(HERE/'zenodo-metadata.json').read_bytes(),'zenodo-deposit.json':dump(portable),'README.md':members['README.md']}
 archive(out/'zenodo-upload-kit.zip',kit)
 paths=[out/'pdf/negative-curvature-cone.pdf',source,out/'zenodo-upload-kit.zip',HERE/'main.tex',HERE/'zenodo-metadata.json',HERE/'zenodo-deposit.json']
 receipt={'files':{str(p.relative_to(HERE)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in paths},'source_members':source_manifest,'verifiers':'PASS','geometry_optimized':'PASS','curvature_optimized':'rejected at startup'}
 (HERE/'PACKAGE_RECEIPT.json').write_bytes(dump(receipt));print(json.dumps({k:v for k,v in receipt.items() if k!='source_members'},indent=2))
if __name__=='__main__':main()
