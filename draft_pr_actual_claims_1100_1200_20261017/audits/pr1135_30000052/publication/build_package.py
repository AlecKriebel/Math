#!/usr/bin/env python3
"""Deterministically rebuild the authored source package and Zenodo upload kit.

The operative PDF is frozen and never silently recompiled. Python3.10+ stdlib.
Explicit member lists and frozen review manifests exclude later release receipts.
"""
import hashlib,json
from pathlib import Path
import subprocess,sys,zipfile

HERE=Path(__file__).resolve().parent
AUDIT=HERE/'audit' if (HERE/'audit').is_dir() else HERE.parent
PDF='random-lattice-counterexample.pdf'
SOURCE='random-lattice-counterexample-source-and-verification.zip'
INPUTS=['ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md',
        'README.md','SOURCE_METADATA.json','SOURCE_REVIEW.md','STATUS.json','VERIFICATION.md']
REVIEWS={
 'probability_01':'4f65617dc88cbb53e52475d1d46ed5dc4f1055ee136abe6ae4e2146a95287d3d',
 'exact_01':'9a2cde68433eefb9a828faf8570afa9fc8b3a0c9fde7b85d01a9e643d441b754',
 'tail_01':'aaf58efd70cff1ae0f07c9cfedb9779e7b3788365752e7ec7e2c5266604ee36f',
 'priority_01':'09678b2d4a6c835a21aecdf8d212a685f83c53947685d1bb8708a67e625e2bbb',
 'priority_rotations_01':'5ac8b78d68991527a2e5c80054f424c9f63b44e3274278cae44d96d12eabe712',
 'priority_classification_01':'f02d201b107eb037a4217fbcf26c40d06e78264a075b62a86cfe81b2095bcd5d',
}
DOCUMENTS=[
 'PR_BODY.md','PR_SNAPSHOT.json','RETRIEVAL_RECEIPT.json','ROOT_MATHEMATICAL_CHECK.md',
 'ROOT_FOURIER_PRIORITY_BRIDGE.md','ROOT_PRIORITY_DECISION.md','ROOT_PRIORITY_QUERY_LEDGER.json','ROOT_PDF_QA.json',
 'sources/ROOT_FETCH_RECEIPT.json','sources/ROOT_RECENT_PAPER_FETCH.json',
 'sources/ROOT_PR_CHRONOLOGY.json','sources/ROOT_CLASSICAL_FETCH.json','sources/ROOT_BOOK_FETCH.json',
 'root_reproduction/INPUT_PIN_CHECK.json','root_reproduction/ROOT_MOMENT_REPLAY.json',
 'root_reproduction/check_root_moments.py','root_reproduction/ROOT_FOURIER_REPLAY.json',
 'root_reproduction/check_fourier_bridge.py','root_reproduction/PROBABILITY_01_REPLAY.json',
 'root_reproduction/EXACT_01_REPLAY.json','root_reproduction/TAIL_01_REPLAY.json',
 'root_reproduction/PRIORITY_01_REPLAY.json','root_reproduction/PRIORITY_ROTATIONS_01_REPLAY.json',
 'root_reproduction/PRIORITY_FINGERPRINT_CHECK.json',
]

def digest(raw):return hashlib.sha256(raw).hexdigest()
def pin(path):
 raw=path.read_bytes();return {'bytes':len(raw),'sha256':digest(raw)}
def encoded(value):return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()
def archive(path,members):
 path.parent.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED) as out:
  for name,raw in sorted(members.items()):
   info=zipfile.ZipInfo(name,date_time=(2026,10,17,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
   out.writestr(info,raw)

def main():
 verification=HERE/'verification';verification.mkdir(exist_ok=True)
 controls=[]
 for file,expected,key,guard in [
  ('reviews/probability_01/check_inclusions.py','reviews/probability_01/CHECK_RESULTS.normal.json',None,'--negative-guard'),
  ('reviews/exact_01/check_cells.py','reviews/exact_01/RESULTS.normal.json',None,'--negative-guard'),
  ('reviews/tail_01/verify_tail.py','reviews/tail_01/CHECK_RESULTS.normal.json',None,'--force-failure'),
  ('reviews/priority_01/check_priority_bridge.py','reviews/priority_01/BRIDGE_CHECKS_NORMAL.json',None,None),
  ('reviews/priority_rotations_01/verify_fourier_bridge.py','reviews/priority_rotations_01/CHECK_RESULTS.normal.json',None,'--fail-guard'),
  ('root_reproduction/check_root_moments.py','root_reproduction/ROOT_MOMENT_REPLAY.json','result',None),
  ('root_reproduction/check_fourier_bridge.py','root_reproduction/ROOT_FOURIER_REPLAY.json','result',None),
 ]:
  aux={};aux_path=Path(file).parent/'INPUT_PINS.json'
  if (AUDIT/aux_path).is_file():aux[str(aux_path)]=pin(AUDIT/aux_path)
  controls.append({'file':file,'pin':pin(AUDIT/file),'expected':expected,'expected_pin':pin(AUDIT/expected),
                   'expected_key':key,'guard':guard,'auxiliary':aux})
 plan={'schema_version':1,'inputs':{name:pin(AUDIT/'inputs'/name) for name in INPUTS},'controls':controls}
 if plan['inputs']['PROOF.md']['sha256']!='1b37d4296730dfcc7a22e3f5b8d149687357e926058a7ed6de844814da404e58':
  raise RuntimeError('Frozen source proof changed')
 (verification/'CONTROL_PLAN.json').write_bytes(encoded(plan))
 checked=subprocess.run([sys.executable,'-B',str(verification/'verify_all.py')],capture_output=True,text=True)
 if checked.returncode:raise RuntimeError(checked.stderr[-5000:])
 (verification/'REPLAY_RECEIPT.json').write_bytes(encoded(json.loads(checked.stdout)))
 members={}
 def add(name,file):
  if name in members or Path(name).is_absolute() or '..' in Path(name).parts:
   raise RuntimeError('Unsafe/duplicate archive member: '+name)
  if file.is_symlink():raise RuntimeError('Symlink excluded: '+str(file))
  members[name]=file.read_bytes()
 for name in ['main.tex','README.md','LICENSE.txt','zenodo-metadata.json','zenodo-deposit.json','build_package.py',
              'output/pdf/'+PDF,'verification/verify_all.py','verification/CONTROL_PLAN.json','verification/REPLAY_RECEIPT.json']:
  add(name,HERE/name)
 for name in INPUTS:add('audit/inputs/'+name,AUDIT/'inputs'/name)
 for name in DOCUMENTS:add('audit/'+name,AUDIT/name)
 for family,sha in REVIEWS.items():
  folder=AUDIT/'reviews'/family;m=folder/'ARTIFACT_RECEIPT.json'
  if digest(m.read_bytes())!=sha:raise RuntimeError('Review manifest changed: '+family)
  add('audit/reviews/'+family+'/ARTIFACT_RECEIPT.json',m)
  for row in json.loads(m.read_text())['files']:
   rel=Path(row['path'])
   if len(rel.parts)!=1 or rel.suffix in ('.pdf','.html','.xml','.png','.zip'):
    raise RuntimeError('Unsafe/non-authored review entry: '+str(rel))
   f=folder/rel
   if pin(f)!={'bytes':row['bytes'],'sha256':row['sha256']}:raise RuntimeError('Review entry changed: '+str(f))
   add('audit/reviews/'+family+'/'+str(rel),f)
 qa=json.loads((AUDIT/'ROOT_PDF_QA.json').read_text());pdf=HERE/'output/pdf'/PDF
 if pin(HERE/'main.tex')!=qa['source'] or pin(pdf)!=qa['pdf'] or qa['pages']!=4:
  raise RuntimeError('PDF/source QA pin changed')
 if not pdf.read_bytes().startswith(b'%PDF-'):raise RuntimeError('Missing operative PDF')
 metadata=json.loads((HERE/'zenodo-metadata.json').read_text());deposit=json.loads((HERE/'zenodo-deposit.json').read_text())
 if metadata!=deposit['metadata']:raise RuntimeError('Deposit metadata mismatch')
 members['PROVENANCE.json']=encoded({
  'problem_id':30000052,'alias':'OWR-723-005','source_pr':'https://github.com/AlecKriebel/Math/pull/1135',
  'source_head_sha':'e809a9c40f4ccdaced6f45f10b1dc8b7725a2119',
  'source_proof_sha256':'1b37d4296730dfcc7a22e3f5b8d149687357e926058a7ed6de844814da404e58',
  'operative_paper':'main.tex','source_proof':'audit/inputs/PROOF.md',
  'historical_inputs':'All ten source PR files unchanged; retain historical10October scope, superseded by current release audit/priority descriptions.',
  'claim':'Full negative answer to universal expected p-th-power comparison; n3,d1,p4 exact19/1620>4/405; minimal point count; independent all-n>=4 tail argument.',
  'later_full_overlap':{'author':'Alper Ferudun','date':'2026-10-14','doi':'10.5281/zenodo.23372668','scope':'Same exact counterexample and broader dimension/exponent results, prominently credited.'},
  'chronology':'Source PR GitHub creation record2026-10-10; related preprint2026-10-14; this note2026-10-17. Historical public visibility/first discovery/publication not certified; no causal attribution.',
  'priority':'No pre-PR full answer identified in bounded audit; exhaustive priority uncertified. Inaccessible full/final bodies and incomplete citation coverage documented. New classical Fourier application is not mislabeled an earlier recorded solution.',
  'verification':'Seven unchanged stdlib programs ordinary/optimized; exact results and guards supplement universal analytic proofs.',
  'review_status':'Extensive AI assistance; unrefereed; no external human peer review, journal acceptance or formal proof-assistant certification.',
  'source_bodies':'Third-party full bodies, extracts, images, raw API responses and private caches excluded.',
 })
 manifest={name:{'bytes':len(raw),'sha256':digest(raw)} for name,raw in sorted(members.items())}
 members['SOURCE_MANIFEST.json']=encoded(manifest)
 out=HERE/'output';source=out/SOURCE;archive(source,members)
 portable=dict(deposit);portable['files']=[{'path':PDF},{'path':SOURCE}]
 archive(out/'zenodo-upload-kit.zip',{PDF:pdf.read_bytes(),SOURCE:source.read_bytes(),
  'zenodo-metadata.json':(HERE/'zenodo-metadata.json').read_bytes(),'zenodo-deposit.json':encoded(portable),'README.md':members['README.md']})
 files=[pdf,source,out/'zenodo-upload-kit.zip',HERE/'main.tex',HERE/'zenodo-metadata.json',HERE/'zenodo-deposit.json']
 receipt={'files':{str(f.relative_to(HERE)):pin(f) for f in files},'source_members':manifest,
          'source_members_including_manifest':len(members),'kit_members':5,'operative_paper_pages':4,
          'verifiers':'Seven unchanged standard-library programs PASS ordinary/optimized; complete outputs compared'}
 (HERE/'PACKAGE_RECEIPT.json').write_bytes(encoded(receipt))
 print(json.dumps({k:v for k,v in receipt.items() if k!='source_members'},indent=2))

if __name__=='__main__':main()
