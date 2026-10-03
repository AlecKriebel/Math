from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
root=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
subprocess.run([sys.executable,str(root/'verify_packet.py'),'--replay'],check=True)
projections=json.loads((root/'PUBLICATION_PROJECTION.json').read_text())
changed={e['file']:e for e in projections['changes']}
for manifest in ['AUTHOR_MANIFEST.json','AUDIT_INPUT_MANIFEST.json']:
    data=json.loads((root/manifest).read_text())
    entries=data.get('files',data)
    for name,record in entries.items():
        public=sha((root/name).read_bytes())
        if name in changed:
            assert record['sha256']==changed[name]['source_sha256'],name
            assert public==changed[name]['public_sha256'],name
        else:
            assert public==record['sha256'],name
compiler=shutil.which('c++') or shutil.which('g++')
assert compiler,'GNU or Clang C++17 compiler required'
with tempfile.TemporaryDirectory(prefix='audit-2609-') as t:
    executable=str(Path(t)/'direct')
    subprocess.run([compiler,'-O2','-std=c++17',str(root/'independent_direct.cpp'),'-o',executable],check=True)
    actual=subprocess.check_output([executable])
assert actual==(root/'independent_direct_results.json').read_bytes()
print('PASS: all public files, declared projections, unchanged mathematics/check programs, and three byte-identical exact replays.')
