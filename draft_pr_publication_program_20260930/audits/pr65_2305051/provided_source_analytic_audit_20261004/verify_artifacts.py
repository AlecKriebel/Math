"""Verify hashes/receipts and preserve historical runner bodies by exact hash."""
import hashlib, json, pathlib

root=pathlib.Path(__file__).resolve().parent
def sha_bytes(data):return hashlib.sha256(data).hexdigest()
def sha(path):return sha_bytes(path.read_bytes())
manifest=json.loads((root/'MANIFEST.json').read_text())
for e in manifest['files']:
    p=root/e['path']
    assert sha(p)==e['sha256'] and p.stat().st_size==e['bytes'],str(p)

current=(root/'run_receipted.py').read_text()
v2=current.replace("p.add_argument('--final-manifest', action='store_true')\n",'')
v2=v2.replace("    'argv_body_sha256': hashlib.sha256(json.dumps(command, ensure_ascii=False, separators=(',',':')).encode()).hexdigest(),\n",'')
v2=v2.replace("if '-c' in command:\n    receipt['inline_code_sha256'] = hashlib.sha256(command[command.index('-c')+1].encode()).hexdigest()\n",'')
start=v2.index('if a.final_manifest:\n')
end=v2.index('sys.stdout.buffer.write(out)',start)
v2=v2[:start]+v2[end:]
v1=v2.replace("p.add_argument('--streams-dir')\n",'')
new="stream_prefix = (pathlib.Path(a.streams_dir) / a.name) if a.streams_dir else prefix\nstream_prefix.parent.mkdir(parents=True, exist_ok=True)\nout_path, err_path = pathlib.Path(str(stream_prefix)+'.stdout'), pathlib.Path(str(stream_prefix)+'.stderr')\n"
old="out_path, err_path = pathlib.Path(str(prefix)+'.stdout'), pathlib.Path(str(prefix)+'.stderr')\n"
assert new in v1
v1=v1.replace(new,old)
versions={sha_bytes(s.encode()):s for s in (v1,v2,current)}
rows=[]
for p in sorted((root/'receipts').glob('*.json')):
    d=json.loads(p.read_text())
    assert isinstance(d['pid'],int) and d['pid']>0 and d['exit_code']==0
    assert d['runner']['sha256'] in versions,(p,d['runner']['sha256'])
    assert sha_bytes(json.dumps(d['argv'],ensure_ascii=False,separators=(',',':')).encode())==d['argv_body_sha256']
    for k in ('stdout','stderr'):
        stream=pathlib.Path(d[k]['path'])
        assert sha(stream)==d[k]['sha256'] and stream.stat().st_size==d[k]['bytes']
    for pin in d['source_pins']:
        assert sha(pathlib.Path(pin['path']))==pin['sha256'],pin
    rows.append({'name':d['name'],'pid':d['pid'],'exit_code':d['exit_code'],'runner_sha256':d['runner']['sha256']})
vdir=root/'runner_versions'
vdir.mkdir(exist_ok=True)
for digest,body in versions.items():
    (vdir/(digest+'.py')).write_text(body)
(root/'runner_versions.json').write_text(json.dumps({'method':'Exact earlier bodies reconstructed from this audit own edits and required to match original execution-time hashes',
   'versions':{digest:str((vdir/(digest+'.py')).relative_to(root)) for digest in versions}},indent=2)+'\n')
for p in root.rglob('*'):
    if p.is_file():
        assert p.suffix not in ('.pdf','.png'),str(p)
print(json.dumps({'prior_manifest_files_verified':len(manifest['files']),
                  'historical_runner_bodies_matched':len(versions),
                  'receipts_verified':rows,
                  'public_full_primary_pdfs_or_rendered_images':0},indent=2))
