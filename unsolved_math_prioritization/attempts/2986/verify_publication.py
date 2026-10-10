#!/usr/bin/env python3
"""Check this publication against exact external pins, then replay in isolation.

Pin this wrapper and PUBLICATION_MANIFEST.json from an independent receipt first.
Integrity and finite algebra checks do not certify mathematical proofs.
"""
from pathlib import Path
import argparse, hashlib, json, stat, subprocess, sys, tempfile, zipfile

ROOT=Path(__file__).resolve().parent
PREFIX='WEINSTEIN_TWO_HANDLEBODIES_2986_'
PINS={
 'AUTHOR_SAFE_FREEZE.zip':(15453,'d322363aa52fb7f45110c3a66be3ed3381cba5cd23ce2dbe6ce20c283734b25b'),
 'AUTHOR_EXTERNAL_MANIFEST.json':(2111,'febab4c31b53b7d4a6f5844b22c808b1593f17e4006fa1c3260e5f0818a42cad'),
 'INDEPENDENT_AUDIT_SAFE.zip':(42665,'33db9f07a08be710bf6479b572d509b44bf9dd499b02f6d01d75b3047cc90e2d'),
 'INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(2963,'66439c8c32ea34cafb654e91186d73cc93f322a980791abd901ea0bcd9782476'),
 'INDEPENDENT_AUDIT_BOOTSTRAP.py':(3918,'8c31429aaedd9056951b3d0d3c2f13793aa0f5ebff851de18cb81f426d44cd5d'),
 'INDEPENDENT_AUDIT_RECEIPT.json':(15724,'5fb252bcfb6b0b4c90097d9d07101618ef817b1b31421bd22cebc261e4e7ea49'),
}
def need(c,m):
 if not c:raise ValueError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def pin(b,p,label):need((len(b),digest(b))==tuple(p),label+': size/hash mismatch')
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--corpus-dir',type=Path);p.add_argument('--source-dir',type=Path)
 a=p.parse_args();need(bool(a.corpus_dir)==bool(a.source_dir),'Supply both input directories or neither')
 corpus=a.corpus_dir.resolve() if a.corpus_dir else None
 sources=a.source_dir.resolve() if a.source_dir else None
 for name,expected in PINS.items():pin((ROOT/'releases'/(PREFIX+name)).read_bytes(),expected,name)
 manifest=json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_bytes())
 need(manifest['schema']=='weinstein-publication-manifest-v1','manifest schema')
 entries=manifest['files'];paths=[e['path'] for e in entries]
 need(len(paths)==len(set(paths)),'duplicate manifest paths')
 actual=[]
 for f in ROOT.rglob('*'):
  need(not f.is_symlink(),'symlink in publication')
  if f.is_file():actual.append(f.relative_to(ROOT).as_posix())
 need(set(actual)==set(paths)|{'PUBLICATION_MANIFEST.json'},'publication member set')
 for e in entries:
  f=Path(e['path']);need(not f.is_absolute() and '..' not in f.parts,'unsafe manifest path')
  pin((ROOT/f).read_bytes(),(e['bytes'],e['sha256']),e['path'])
 checked=0
 for stem,directory,count in [('AUTHOR','original',9),('INDEPENDENT_AUDIT','audit',12)]:
  an=PREFIX+stem+('_SAFE_FREEZE.zip' if stem=='AUTHOR' else '_SAFE.zip')
  ext=json.loads((ROOT/'releases'/(PREFIX+stem+'_EXTERNAL_MANIFEST.json')).read_bytes())
  expected={e['path']:e for e in ext['members']}
  with zipfile.ZipFile(ROOT/'releases'/an) as z:
   need(len(z.infolist())==len(expected)==count,'archive member count')
   need(set(z.namelist())==set(expected),'archive member set')
   need({f.name for f in (ROOT/directory).iterdir()}==set(expected),'extracted member set')
   for i in z.infolist():
    need(Path(i.filename).name==i.filename and not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16),'unsafe ZIP entry')
    e=expected[i.filename];b=z.read(i);pin(b,(e['bytes'],e['sha256']),i.filename)
    need((ROOT/directory/i.filename).read_bytes()==b,'extracted member differs: '+i.filename);checked+=1
 acceptance=json.loads((ROOT/'audit/ACCEPTANCE.json').read_bytes())
 need(acceptance['decision']=='accept_exact_original_author_archive_as_bounded_partial' and acceptance['author_repair_required'] is False,'acceptance mismatch')
 need(acceptance['turns_used']==4 and acceptance['turn_limit']==5 and acceptance['full_solution'] is False,'bounded status mismatch')
 outputs=[]
 for optimized in [False,True]:
  with tempfile.TemporaryDirectory(prefix='weinstein publication relocation ') as td:
   d=Path(td)/'trusted outer artifacts';d.mkdir()
   for name in PINS:(d/(PREFIX+name)).write_bytes((ROOT/'releases'/(PREFIX+name)).read_bytes())
   cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(d/(PREFIX+'INDEPENDENT_AUDIT_BOOTSTRAP.py'))]
   if corpus:cmd+=['--corpus-dir',str(corpus),'--source-dir',str(sources)]
   r=subprocess.run(cmd,cwd=td,capture_output=True,text=True,timeout=180)
   need(r.returncode==0 and not r.stderr,'sealed replay failed: '+r.stderr)
   result=json.loads(r.stdout);need(result['result']=='PASS' and result['formal_proof_certification'] is False,'unexpected result');outputs.append(r.stdout)
 need(outputs[0]==outputs[1],'normal and optimized outputs differ')
 print(json.dumps({'result':'PASS','problem_id':2986,'rank':922,'canonical_queue_status':'unsolved','turns':'4/5','archive_members_byte_identical':checked,'external_artifact_pins_verified':len(PINS),'isolated_relocated_normal_and_optimized':True,'byte_identical_stdout':True,'sealed_replay_stdout_sha256':digest(outputs[0].encode()),'full_external_inputs_supplied':bool(corpus),'formal_proof_certification':False,'audit_result':json.loads(outputs[0])},indent=2,sort_keys=True))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
