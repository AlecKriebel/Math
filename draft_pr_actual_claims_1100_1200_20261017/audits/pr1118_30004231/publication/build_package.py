#!/usr/bin/env python3
"""Build frozen source/verification and portable Zenodo upload archives."""
import hashlib,json,pathlib,subprocess,sys,zipfile
HERE=pathlib.Path(__file__).resolve().parent
AUDIT=HERE.parent
def digest(raw):return hashlib.sha256(raw).hexdigest()
def dump(x):return (json.dumps(x,indent=2,sort_keys=True)+'\n').encode()
def run(name,opt=False):
 r=subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(HERE/'verification'/name)],capture_output=True,text=True)
 if r.returncode:raise SystemExit(r.stderr)
 return json.loads(r.stdout)
def archive(path,members):
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as z:
  for name,raw in sorted(members.items()):
   info=zipfile.ZipInfo(name,date_time=(2026,10,17,0,0,0))
   info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
   z.writestr(info,raw)
def main():
 for src,dst in [('reviews/geometry_01/verifier.py','check_geometry.py'),('reviews/topology_01/verify_poset.py','check_topology.py')]:
  (HERE/'verification'/dst).write_bytes((AUDIT/src).read_bytes())
 results={}
 for name,key in [('check_geometry.py','geometry'),('check_topology.py','topology')]:
  a,b=run(name),run(name,True)
  if a!=b:raise SystemExit('Optimized verification differs: '+name)
  results[key]=a
 results['ordinary_and_optimized']='identical; all explicit-exception checks execute'
 (HERE/'verification/expected_results.json').write_bytes(dump(results))
 (HERE/'LICENSE.txt').write_text('Copyright 2026 Alec Kriebel. Original authored materials: Creative Commons Attribution 4.0 International, https://creativecommons.org/licenses/by/4.0/. Third-party works retain their licenses.\n')
 pdf=HERE/'output/pdf/totally-mixed-face-posets.pdf'
 pdf.write_bytes((HERE/'output/pdf/main.pdf').read_bytes())
 members={}
 for name in ['main.tex','README.md','LICENSE.txt','zenodo-metadata.json','output/pdf/totally-mixed-face-posets.pdf','verification/check_geometry.py','verification/check_topology.py','verification/expected_results.json']:
  members[name]=(HERE/name).read_bytes()
 if not members['output/pdf/totally-mixed-face-posets.pdf'].startswith(b'%PDF-'):raise SystemExit('Missing PDF')
 for src,dst in [
  ('ROOT_MATHEMATICAL_CHECK.md','audits/ROOT_MATHEMATICAL_CHECK.md'),
  ('ROOT_RELATED_DEFINITIONS.md','audits/ROOT_RELATED_DEFINITIONS.md'),
  ('ROOT_PRIORITY_CHECK.md','audits/ROOT_PRIORITY_CHECK.md'),
  ('ROOT_PRIORITY_SEARCH.json','audits/ROOT_PRIORITY_SEARCH.json'),
  ('ROOT_REPRODUCTION.json','audits/ROOT_REPRODUCTION.json'),
  ('reviews/geometry_01/REPORT.md','audits/geometry_01/REPORT.md'),
  ('reviews/geometry_01/SOURCE_LEDGER.json','audits/geometry_01/SOURCE_LEDGER.json'),
  ('reviews/geometry_01/results.normal.json','audits/geometry_01/results.normal.json'),
  ('reviews/geometry_01/results.optimized.json','audits/geometry_01/results.optimized.json'),
  ('reviews/topology_01/REPORT.md','audits/topology_01/REPORT.md'),
  ('reviews/topology_01/SOURCE_LEDGER.json','audits/topology_01/SOURCE_LEDGER.json'),
  ('reviews/topology_01/RESULTS.json','audits/topology_01/RESULTS.json'),
 ]:members[dst]=(AUDIT/src).read_bytes()
 for name in ['PRIORITY_AUDIT.md','SOURCE_LEDGER.json','QUERY_LEDGER.json','COMPARISON_MATRIX.md','DIRECT_CONSEQUENCE_CHECK.md','RESEARCH_LOG.md']:
  members['audits/priority_01/'+name]=(AUDIT/'reviews/priority_01'/name).read_bytes()
 original=json.loads((AUDIT/'RETRIEVAL_RECEIPT.json').read_text())
 members['PROVENANCE.json']=dump({'problem_id':30004231,'alias':'OWR-17135-028','source_pr':'https://github.com/AlecKriebel/Math/pull/1118','source_head_sha':'8592fb7297d3c4973f2778c47cfa8972cba896a6','source_proof_sha256':'b6e32c893f45447951cf920777adaaf012b1eb5a9e5a8072a8822fc8fcf2ff28','pinned_original_inputs':original['files'],'operative_paper':'main.tex','historical_inputs_not_redistributed':'Original proof-only edition remains accessible at the pinned GitHub head; this package includes the new self-contained note and new verification.','computation_role':'Supplementary exact reproduction; exhaustive analytic proof in note.','review_status':'AI-assisted; unrefereed; no external human peer review or formal proof-assistant certification.'})
 manifest={name:{'bytes':len(raw),'sha256':digest(raw)} for name,raw in sorted(members.items())}
 members['SOURCE_MANIFEST.json']=dump(manifest)
 out=HERE/'output';source=out/'totally-mixed-face-posets-source-and-verification.zip'
 archive(source,members)
 metadata=json.loads((HERE/'zenodo-metadata.json').read_text())
 deposit=json.loads((HERE/'zenodo-deposit.json').read_text())
 if metadata!=deposit['metadata']:raise SystemExit('Deposit metadata differs')
 portable=dict(deposit);portable['files']=[{'path':'totally-mixed-face-posets.pdf'},{'path':source.name}]
 kit={'totally-mixed-face-posets.pdf':pdf.read_bytes(),source.name:source.read_bytes(),'zenodo-metadata.json':(HERE/'zenodo-metadata.json').read_bytes(),'zenodo-deposit.json':dump(portable),'README.md':members['README.md']}
 archive(out/'zenodo-upload-kit.zip',kit)
 paths=[pdf,source,out/'zenodo-upload-kit.zip',HERE/'main.tex',HERE/'zenodo-metadata.json',HERE/'zenodo-deposit.json']
 receipt={'files':{str(p.relative_to(HERE)):{'bytes':p.stat().st_size,'sha256':digest(p.read_bytes())} for p in paths},'source_members':manifest,'verifiers':'PASS in ordinary and optimized Python','source_members_including_manifest':len(members),'kit_members':len(kit)}
 (HERE/'PACKAGE_RECEIPT.json').write_bytes(dump(receipt))
 print(json.dumps({k:v for k,v in receipt.items() if k!='source_members'},indent=2))
if __name__=='__main__':main()
