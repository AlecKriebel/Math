from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent;r=p/'review'
assert hashlib.sha256((p/'FINAL_AUTHOR_MANIFEST.json').read_bytes()).hexdigest()=='db357e6334b49123b461dfd762f5fc05082997692ca33ce1ae4a898d16694ec8'
assert hashlib.sha256((r/'REVIEW_MANIFEST.json').read_bytes()).hexdigest()=='c636ff08daae7c5e76a03600ee0a09956f48e7d2c1d13d9b8d18f0b7f86aae90'
for e in json.loads((r/'REVIEW_MANIFEST.json').read_text())['files']:
 b=(r/e['path']).read_bytes();assert len(b)==e['bytes'];assert hashlib.sha256(b).hexdigest()==e['sha256']
a=json.loads(subprocess.check_output([sys.executable,str(p/'REPLAY_ALL.py')],cwd=p));assert a['assertions']==345888 and a['manifest_entries']==62 and a['all_receipts_byte_exact']
out=subprocess.check_output([sys.executable,str(r/'independent_check.py')]);assert out==(r/'INDEPENDENT_CHECKS.json').read_bytes();assert json.loads(out)['independent_assertions']==47964
print(json.dumps({'status':'PASS','author_assertions':345888,'independent_assertions':47964,'source_bindings_checked':a['source_bindings_checked'],'source_omission_explicit':a['source_bindings_checked']==0},sort_keys=True))
