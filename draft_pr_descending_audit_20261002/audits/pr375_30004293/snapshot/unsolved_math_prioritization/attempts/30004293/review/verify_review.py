from pathlib import Path
import argparse,hashlib,json,subprocess,sys
ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);a=ap.parse_args();p=a.author;r=Path(__file__).resolve().parent
m=p/'FINAL_AUTHOR_MANIFEST.json';assert hashlib.sha256(m.read_bytes()).hexdigest()=='ab2d9369a444b49e913abf32420b1c08f701149dc2df631278ad03e69feb5218'
for e in json.loads(m.read_text())['files']:
 b=(p/e['path']).read_bytes();assert len(b)==e['bytes'];assert hashlib.sha256(b).hexdigest()==e['sha256']
for e in json.loads((r/'REMOTE_BINDING.json').read_text())['files']:
 b=(p/e['path']).read_bytes();assert len(b)==e['size'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['sha']
out=subprocess.check_output([sys.executable,str(r/'independent_checks.py')]);assert out==(r/'INDEPENDENT_CHECKS.json').read_bytes()
for i in range(1,6):assert subprocess.check_output([sys.executable,str(p/f'verify_turn{i}.py')])==(p/f'TURN_{i}_CHECKS.json').read_bytes()
print(json.dumps({'frozen_author_files':42,'raw_blobs':42,'independent_assertions':json.loads(out)['exact_assertions'],'author_receipts_byte_exact':True,'source_pdfs_checked_by_this_portable_wrapper':False},sort_keys=True))
