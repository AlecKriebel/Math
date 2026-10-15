from pathlib import Path, PurePosixPath
import hashlib,json,zipfile,stat,datetime
HERE=Path(__file__).resolve().parent; AUDIT=HERE.parent.parent; PUB=AUDIT/'publication'
def h(b): return hashlib.sha256(b).hexdigest()
def put(n,d): (HERE/n).write_text(json.dumps(d,indent=2)+'\n')
(HERE/'.gitignore').write_text('tmp/\nprivate_sources/\n__pycache__/\n')
freeze_raw=(PUB/'PREPUBLICATION_FREEZE.json').read_bytes(); freeze=json.loads(freeze_raw)
checks={}
for n,r in freeze['files'].items():
 b=(PUB/n).read_bytes(); checks[n]={'bytes':len(b),'sha256':h(b),'matches_freeze':len(b)==r['bytes'] and h(b)==r['sha256']}
 if not checks[n]['matches_freeze']: raise RuntimeError(n)
expected={'output/pdf/note.pdf':'eac73f8c53ece8ef5825258327b98fb9e5eda161a0cc9ad18afdd0d3cd61d05c','robinson-tangency-source-verification-v1.0.zip':'549d708e0e58a5ec453a1432db309ffa72ec86a636d3cbc7a6dd99d46b78b01d','zenodo-deposit.json':'5d3bffaa92ff0fdf717f172bebd648f162f33a9c8080403cc6264964f1441353'}
for n,a in expected.items():
 if checks[n]['sha256']!=a: raise RuntimeError('External anchor '+n)
original=json.loads((AUDIT/'ORIGINAL_SNAPSHOT.json').read_text())['files']; original_checks={}
for n,a in original.items():
 b=(AUDIT/'original'/n).read_bytes(); original_checks[n]={'sha256':h(b),'bytes':len(b),'matches_original_snapshot':h(b)==a}
 if h(b)!=a: raise RuntimeError('Original mutated '+n)
put('evidence/frozen_before.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'freeze_sha256':h(freeze_raw),'files':checks,'original':original_checks})
archive=PUB/'robinson-tangency-source-verification-v1.0.zip'; out=HERE/'tmp/extracted'; out.mkdir()
with zipfile.ZipFile(archive) as z:
 names=z.namelist()
 if len(names)!=len(set(names)): raise RuntimeError('Duplicate ZIP members')
 records={}
 for zi in z.infolist():
  p=PurePosixPath(zi.filename)
  if p.is_absolute() or '..' in p.parts or '\\' in zi.filename or zi.filename!=p.as_posix() or stat.S_IFMT(zi.external_attr>>16)!=stat.S_IFREG: raise RuntimeError('Unsafe ZIP member '+zi.filename)
  b=z.read(zi); q=out.joinpath(*p.parts); q.parent.mkdir(parents=True,exist_ok=True); q.write_bytes(b)
  records[zi.filename]={'bytes':len(b),'sha256':h(b)}
manifest_raw=(out/'PACKAGE_MANIFEST.json').read_bytes(); manifest=json.loads(manifest_raw)
if h(manifest_raw)!='a50792f1c2d55ba4b4d0085369ca08b0d47296d1a3963ea0c2fe820433093832':raise RuntimeError('Trusted manifest mismatch')
if set(names)!=set(manifest['files'])|{'PACKAGE_MANIFEST.json'}: raise RuntimeError('ZIP membership')
for n,r in manifest['files'].items():
 if records[n]!=r: raise RuntimeError('ZIP payload '+n)
orig_archive={}
for n,a in original.items():
 rel=n.removeprefix('unsolved_math_prioritization/attempts/30000717/'); r=records['original_packet/'+rel]
 if r['sha256']!=a: raise RuntimeError('ZIP original '+n)
 orig_archive[rel]=r
for n in ['note.tex','README.md','requirements.txt','verify_package.py']:
 if (out/n).read_bytes()!=(PUB/n).read_bytes(): raise RuntimeError('Active/archive mismatch '+n)
put('evidence/archive_inventory.json',{'status':'PASS','zip_members':len(names),'payloads':len(manifest['files']),'trusted_manifest_sha256':h(manifest_raw),'all_members':records,'unchanged_original_count':len(orig_archive),'unchanged_original_members':orig_archive,'active_archive_agreement':True,'special_entries':False})
(HERE/'RESEARCH_LOG.md').write_text('# Fresh full-package review 02\n\n- '+datetime.datetime.now(datetime.timezone.utc).isoformat()+': Started independent adversarial review of revision 2. All eight frozen active file digests and all 30 original snapshot files match; all 85 ZIP members are safe regular files and the 84 payloads match the externally pinned manifest. Mathematical/source/visual/tool review remains open. Completion estimate: 15%.\n')
print(json.dumps({'status':'PASS','zip_members':len(names),'payloads':len(manifest['files']),'unchanged_original':len(orig_archive)}))
