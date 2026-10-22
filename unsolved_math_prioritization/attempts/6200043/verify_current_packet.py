"""Check all frozen and corrected public bindings, plus the historical replay."""
from pathlib import Path
import hashlib,json,subprocess,sys
p=Path(__file__).resolve().parent
m=json.loads((p/'CURRENT_PACKET_MANIFEST.json').read_text())
for group in ('original_files','additive_files'):
    for name,record in m[group].items():
        b=(p/name).read_bytes()
        assert len(b)==record['bytes'],name
        assert hashlib.sha256(b).hexdigest()==record['sha256'],name
for f in sorted(p.glob('TURN_*_MANIFEST.json'))+[p/'CORRECTION_MANIFEST.json']:
    for name,sha in json.loads(f.read_text()).items():
        assert hashlib.sha256((p/name).read_bytes()).hexdigest()==sha,(f.name,name)
expected_names=set(m['original_files'])|set(m['additive_files'])|{'CURRENT_PACKET_MANIFEST.json'}
actual_names={f.name for f in p.iterdir() if f.is_file()}
assert actual_names==expected_names,(actual_names-expected_names,expected_names-actual_names)
replay=json.loads(subprocess.check_output([sys.executable,str(p/'verify_publication.py')],text=True))
assert replay=={'public_bindings':29,'exact_assertions':61033,'raw_sources_checked':0,'original_resolved':False}
print(json.dumps({'original_files_bound':len(m['original_files']),'additive_files_bound':len(m['additive_files']),'public_files_including_manifest':len(expected_names),'exact_assertions':61033,'raw_sources_checked':0,'rereview_status':'pending','original_resolved':False},sort_keys=True))
