#!/usr/bin/env python3
from pathlib import Path
import zipfile,hashlib,json,re,datetime
B=Path(__file__).resolve().parents[2];R=Path(__file__).resolve().parent
P=B/'publication';M=R/'tmp/mirror'
def pin(raw):return {'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
rec=json.loads((P/'PACKAGE_RECEIPT.json').read_text()); rows=[]
with zipfile.ZipFile(P/'output/random-lattice-counterexample-source-and-verification.zip') as z:
 names=z.namelist();require(len(names)==126 and len(set(names))==126,'source member inventory')
 data={n:z.read(n) for n in names}
 manifest=json.loads(data['SOURCE_MANIFEST.json'])
 require(set(manifest)==set(names)-{'SOURCE_MANIFEST.json'},'SOURCE_MANIFEST exact inventory')
 require(manifest==rec['source_members'],'package receipt vs source manifest')
 for n,expected in manifest.items():require(pin(data[n])==expected,'source fingerprint '+n)
 for n,raw in data.items():
  require(not(Path(n).is_absolute() or '..' in Path(n).parts),'unsafe path')
  require(not any(v in Path(n).parts for v in ('private','tmp','__pycache__','.git')),'private member '+n)
  require(not n.endswith(('.html','.xml','.png','.jpg','.pyc')),'unexpected body/cache '+n)
  require(n.endswith('.pdf')==(n=='output/pdf/random-lattice-counterexample.pdf'),'unexpected PDF '+n)
 for n in rec['files']:
  if n in data:require(pin(data[n])==rec['files'][n],'frozen shipped identity '+n)
 entries=0;families={}
 for name in names:
  if re.fullmatch(r'audit/reviews/[^/]+/ARTIFACT_RECEIPT.json',name):
   m=json.loads(data[name]);folder=Path(name).parent;families[str(folder)]={'entries':len(m['files']),'sha256':pin(data[name])['sha256']}
   for row in m['files']:
    path=str(folder/row['path']);require(pin(data[path])=={'bytes':row['bytes'],'sha256':row['sha256']},'review manifest '+path);entries+=1
 require(entries==73,'authored review inventory')
 # Shipped copies equal the corresponding live files, with unambiguous mapping.
 for n,raw in data.items():
  if n in ('SOURCE_MANIFEST.json','PROVENANCE.json'):continue
  src=B/n[6:] if n.startswith('audit/') else P/n
  require(src.read_bytes()==raw,'shipped/live mismatch '+n)
with zipfile.ZipFile(P/'output/zenodo-upload-kit.zip') as kit:
 require(len(kit.namelist())==5 and len(set(kit.namelist()))==5,'kit inventory')
 require(kit.read('random-lattice-counterexample.pdf')==(P/'output/pdf/random-lattice-counterexample.pdf').read_bytes(),'kit PDF')
 require(kit.read('random-lattice-counterexample-source-and-verification.zip')==(P/'output/random-lattice-counterexample-source-and-verification.zip').read_bytes(),'kit source')
 require(kit.read('zenodo-metadata.json')==(P/'zenodo-metadata.json').read_bytes(),'kit metadata')
 require(kit.read('README.md')==(P/'README.md').read_bytes(),'kit readme')
 portable=json.loads(kit.read('zenodo-deposit.json'));dep=json.loads((P/'zenodo-deposit.json').read_text());meta=json.loads((P/'zenodo-metadata.json').read_text())
 require(portable['metadata']==dep['metadata']==meta,'metadata equality')
 require([v['path'] for v in portable['files']]==['random-lattice-counterexample.pdf','random-lattice-counterexample-source-and-verification.zip'],'kit portable paths')
 require(all((P/x['path']).is_file() for x in dep['files']),'repository deposit paths')
 # Inspect links whose destination is visibly local. Historical absolute paths
 # are custody metadata and handled separately, not Markdown navigation.
 broken=[];checked=0
 for n,raw in data.items():
  if n.endswith('.md'):
   for dest in re.findall(rb'\]\(([^)]+)\)',raw):
    d=dest.decode()
    if '://' in d or d.startswith('#'):continue
    target=(M/Path(n).parent/d.split('#')[0]).resolve()
    checked+=1
    if not target.exists():broken.append({'file':n,'destination':d})
 require(not broken,'broken authored relative navigation: '+str(broken))
 report={'utc':datetime.datetime.now(datetime.UTC).isoformat(),'status':'PASS','source_members':len(names),'source_manifest_entries':len(manifest),'review_manifest_entries':entries,'review_manifests':families,'kit_members':5,'local_markdown_links_checked':checked,'broken_local_links':broken,'all_shipped_copies_equal_live':True,'authored_license':'CC BY4.0','third_party_full_bodies_found':False,'operative_frozen_files':rec['files'],'scope_note':'Out-of-package gates, logs and operational replay receipts are mutable and are not members of this frozen candidate.'}
(R/'PACKAGE_INVENTORY.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('review_manifests','operative_frozen_files')},indent=2))
