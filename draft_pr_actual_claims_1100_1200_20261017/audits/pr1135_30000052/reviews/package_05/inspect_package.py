#!/usr/bin/env python3
"""Read-only live package custody; extracted reproduction only in ignored tmp."""
from pathlib import Path,PurePosixPath
import ast,datetime,hashlib,json,re,shutil,stat,subprocess,sys,zipfile
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];PUB=ROOT/'publication'
def require(v,label):
 if not v:raise RuntimeError(label)
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(name,obj):(HERE/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def pathfor(name):return ROOT/name[6:] if name.startswith('audit/') else PUB/name

def inspect():
 receipt=json.loads((PUB/'PACKAGE_RECEIPT.json').read_text());archive=PUB/'output/random-lattice-counterexample-source-and-verification.zip'
 with zipfile.ZipFile(archive) as z:
  names=z.namelist();members={n:z.read(n) for n in names}
  require(len(names)==len(set(names))==126,'source count/duplicates')
  require(z.testzip() is None,'source CRC')
  for i in z.infolist():
   p=PurePosixPath(i.filename)
   require(not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename,'unsafe name')
   require(not stat.S_ISLNK(i.external_attr>>16),'symlink')
   require(i.date_time==(2026,10,17,0,0,0),'nondeterministic timestamp')
  manifest=json.loads(members['SOURCE_MANIFEST.json'])
  require(set(manifest)==set(names)-{'SOURCE_MANIFEST.json'},'manifest coverage')
  require(manifest==receipt['source_members'],'receipt/manifest map')
  for n,b in members.items():
   if n in manifest:require(pin(b)==manifest[n],'source manifest mismatch '+n)
   if n not in ('SOURCE_MANIFEST.json','PROVENANCE.json'):require(b==pathfor(n).read_bytes(),'live/archive mismatch '+n)
  mirror=HERE/'tmp/extracted';require(not mirror.exists(),'mirror already exists')
  z.extractall(mirror)
 reviews={};entry_count=0
 for name in names:
  if not name.startswith('audit/reviews/') or not name.endswith('/ARTIFACT_RECEIPT.json'):continue
  rows=json.loads(members[name])['files'];reviews[name]=len(rows);entry_count+=len(rows)
  base=PurePosixPath(name).parent
  for row in rows:require(pin(members[str(base/row['path'])])=={'bytes':row['bytes'],'sha256':row['sha256']},'review artifact mismatch')
 require(entry_count==73,'authored review count')
 old_manifest=json.loads(members['audit/inputs/MANIFEST.json'])
 for row in old_manifest['entries']:require(pin(members['audit/inputs/'+row['file']])=={'bytes':row['bytes'],'sha256':row['sha256']},'original input manifest')
 remote=[]
 for name in old_manifest['members']:
  b=(HERE/'sources/private'/('remote_'+name)).read_bytes()
  require(b==members['audit/inputs/'+name],'remote original differs '+name);remote.append(name)
 all_source_hashes={row['sha256'] for row in json.loads((HERE/'SOURCE_FETCH.json').read_text()) if 'sha256' in row}
 leak=[]
 for n,b in members.items():
  if any(x in n.split('/') for x in ('private','tmp','__pycache__')):leak.append(n)
  if n.endswith(('.html','.xml','.png','.jpg','.pyc')):leak.append(n)
  if pin(b)['sha256'] in all_source_hashes and not n.startswith('audit/inputs/'):leak.append(n)
 require(not leak,'third-party/private body present')
 plan=json.loads(members['verification/CONTROL_PLAN.json'])
 for control in plan['controls']:
  require(pin(members['audit/'+control['file']])==control['pin'],'control pin')
  require(pin(members['audit/'+control['expected']])==control['expected_pin'],'expected pin')
  require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(members['audit/'+control['file']]))),'assert in pinned control')
  for n,p in control['auxiliary'].items():require(pin(members['audit/'+n])==p,'auxiliary pin')
 for n,p in plan['inputs'].items():require(pin(members['audit/inputs/'+n])==p,'runner input pin')
 kit=PUB/'output/zenodo-upload-kit.zip'
 with zipfile.ZipFile(kit) as z:
  require(len(z.namelist())==len(set(z.namelist()))==5 and z.testzip() is None,'upload kit count/CRC')
  require(z.read(archive.name)==archive.read_bytes(),'kit source bytes')
  require(z.read('random-lattice-counterexample.pdf')==members['output/pdf/random-lattice-counterexample.pdf'],'kit PDF')
  require(z.read('zenodo-metadata.json')==members['zenodo-metadata.json'],'kit metadata')
  require(z.read('README.md')==members['README.md'],'kit README')
  portable=json.loads(z.read('zenodo-deposit.json'));repo=json.loads(members['zenodo-deposit.json'])
  require(portable['metadata']==repo['metadata']==json.loads(members['zenodo-metadata.json']),'metadata copies')
  require(portable['files']==[{'path':'random-lattice-counterexample.pdf'},{'path':archive.name}],'flat upload paths')
  for row in repo['files']:require((mirror/row['path']).exists() or row['path']=='output/'+archive.name,'repo upload path')
 for n,p in receipt['files'].items():require(pin((PUB/n).read_bytes())==p,'six receipt pin')
 result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_members':len(names),'manifest_entries':len(manifest),'all_archive_manifest_and_live_pins_match':True,
         'review_manifests':reviews,'authored_review_entries':entry_count,'original_remote_head_files_byte_equal':remote,'upload_kit_members':5,'privacy_filename_and_body_hash_scan':'PASS','runner_controls':len(plan['controls']),'fixed_members':names,
         'license':'CC BY 4.0 applies to original authored material; primary full bodies excluded',
         'scope_note':'Out-of-package coordination gate/logs/operational receipts are not frozen source members.'}
 write('PACKAGE_INVENTORY.json',result)
 return mirror

def replay(mirror):
 before={n:pin((PUB/n).read_bytes()) for n in json.loads((HERE/'START_PINS.json').read_text())['frozen_six']}
 originals={p.relative_to(mirror).as_posix():p.read_bytes() for p in mirror.rglob('*') if p.is_file()}
 # Builder is run only against extracted mirror. All TMPDIR descendants ignored.
 process=subprocess.run([sys.executable,'-B',str(mirror/'build_package.py')],capture_output=True,text=True,env=__import__('os').environ|{'TMPDIR':str(HERE/'tmp')})
 (HERE/'tmp/build.stdout').write_text(process.stdout);(HERE/'tmp/build.stderr').write_text(process.stderr)
 require(process.returncode==0,'standalone builder failed '+process.stderr[-2000:])
 compare={}
 for n in before:
  current=(mirror/n).read_bytes();compare[n]={'byte_equal':current==(PUB/n).read_bytes(),**pin(current)};require(compare[n]['byte_equal'],'rebuilt six mismatch '+n)
 for n in ('PACKAGE_RECEIPT.json','verification/CONTROL_PLAN.json','verification/REPLAY_RECEIPT.json'):
  compare[n]={'byte_equal':(mirror/n).read_bytes()==(PUB/n).read_bytes(),**pin((mirror/n).read_bytes())};require(compare[n]['byte_equal'],'rebuilt receipt mismatch '+n)
 changed=[n for n,b in originals.items() if (mirror/n).read_bytes()!=b]
 require(not changed,'builder changed shipped authored inputs')
 require(before=={n:pin((PUB/n).read_bytes()) for n in before},'live six mutated')
 write('REBUILD_RECEIPT.json',{'status':'PASS','python':sys.version,'executable':sys.executable,'command':['python3','-B','tmp/extracted/build_package.py'],'builder_exit':process.returncode,'six_and_receipts':compare,'shipped_extracted_inputs_changed':changed,'frozen_PDF_was_input':True,'TeX_compilation_performed':False,'live_builder_executed':False,'replay':json.loads((mirror/'verification/REPLAY_RECEIPT.json').read_text())})
 print('Package inventory PASS: 126 members; 73 authored review artifacts; 10 remote originals identical. Standalone rebuild PASS: six frozen files and three receipts byte identical.')

if __name__=='__main__':replay(inspect())
