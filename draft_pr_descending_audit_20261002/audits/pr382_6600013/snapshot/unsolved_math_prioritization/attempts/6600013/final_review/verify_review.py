from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--sources',type=Path);a=ap.parse_args();r=Path(__file__).resolve().parent;p=a.author
assert hashlib.sha256((p/'FINAL_FROZEN_MANIFEST.json').read_bytes()).hexdigest()=='6051cac8bee10f0bdfa2bdadcb782ee3782855964cd2e10ee1a1fb0023c6f056'
for e in json.loads((r/'REMOTE_BINDING.json').read_text())['files']:
 b=(p/e['path']).read_bytes();assert len(b)==e['size'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['sha']
cmd=[sys.executable,str(p/'REPLAY_ALL.py')]
if a.sources:cmd+=['--sources',str(a.sources.resolve())]
v=json.loads(subprocess.check_output(cmd));assert v['author_assertions']==5367 and v['manifest_entries_verified']==173
out=subprocess.check_output([sys.executable,str(r/'independent_checks.py')]);assert out==(r/'INDEPENDENT_CHECKS.json').read_bytes();assert json.loads(out)['exact_assertions']==22728
print(json.dumps({'review':'PASS_SCOPED','author_assertions':5367,'independent_assertions':22728,'raw_author_blobs':44,'primary_source_pdfs_verified':v['primary_source_pdfs_verified']},sort_keys=True))
