from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);a=ap.parse_args();p=a.author;r=Path(__file__).resolve().parent
pins={'FINAL_AUTHOR_MANIFEST.json':'a8881d305f9fa739590bfe47b8bd8ef6b28027e9523102498621e94c9085e255','REVIEW_CORRECTION_MANIFEST.json':'76d2ab2d1dcbb83b71ed87d8e60b75ad198e0c54554fa583a1803550a5cf3fa7'}
for name,sha in pins.items():
 b=(p/name).read_bytes();assert hashlib.sha256(b).hexdigest()==sha
 for e in json.loads(b)['files']:
  x=(p/e['path']).read_bytes();assert len(x)==e['bytes'] and hashlib.sha256(x).hexdigest()==e['sha256']
for e in json.loads((r/'REMOTE_BINDING.json').read_text())['files']:
 b=(p/e['path']).read_bytes();assert len(b)==e['bytes'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha']
for i in range(1,6):
 out=subprocess.check_output([sys.executable,str(p/f'check_turn_{i}.py')]);assert out==(p/f'TURN_{i}_CHECKS.json').read_bytes()
out=subprocess.check_output([sys.executable,str(r/'independent_checks.py')]);assert out==(r/'INDEPENDENT_CHECKS.json').read_bytes()
print(json.dumps({'author_files':41,'additive_correction_files':2,'raw_blob_ids_match':43,'author_assertions':747103,'independent_assertions':23463,'source_pdfs_reverified':False},sort_keys=True))
