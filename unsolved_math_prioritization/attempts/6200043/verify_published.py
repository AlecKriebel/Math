"""Portable publication replay preserving strict frozen verifier semantics."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,shutil
p=Path(__file__).resolve().parent
m=json.loads((p/'PUBLICATION_MANIFEST.json').read_text())
for n,record in m['files'].items():
    b=(p/n).read_bytes()
    assert len(b)==record['bytes'],n
    assert hashlib.sha256(b).hexdigest()==record['sha256'],n
with tempfile.TemporaryDirectory(prefix='math-6200043-author-') as td:
    t=Path(td)
    for n in m['author_files']:
        shutil.copyfile(p/n,t/n)
    author=json.loads(subprocess.check_output([sys.executable,str(t/'verify_current_packet.py')],text=True))
    assert author=={'additive_files_bound':3,'exact_assertions':61033,'original_files_bound':32,'original_resolved':False,'public_files_including_manifest':36,'raw_sources_checked':0,'rereview_status':'pending'}
for script,expected in [('review/independent_controls.py','review/INDEPENDENT_CONTROLS_RESULT.json'),('review/rereview_3868261/check_repaired_scale.py','review/rereview_3868261/REPAIRED_SCALE_RESULT.json')]:
    actual=json.loads(subprocess.check_output([sys.executable,str(p/script)],text=True))
    assert actual==json.loads((p/expected).read_text()),script
print(json.dumps({'publication_hash_bindings':len(m['files']),'frozen_author_files':len(m['author_files']),'review_files':len(m['review_files']),'author_exact_assertions':61033,'independent_graph_assertions':5319784,'independent_series_assertions':540,'independent_holder_assertions':3645,'independent_scale_assertions':4320,'repaired_scale_assertions':22356,'raw_sources_checked':0,'original_resolved':False,'review_status':'scoped_pass_corrected_partial_packet'},sort_keys=True))
