#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys

def require(c,m):
    if not c:raise RuntimeError(m)

base=Path(__file__).resolve().parent
manifest=json.loads((base/'MANIFEST.json').read_text())
expected={row['path']:row for row in manifest['authored_files']}
actual={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
require(actual==set(expected),'Closed file membership differs')
for name,row in expected.items():
    path=base/name
    require(not path.is_symlink(),'Symlink is forbidden')
    data=path.read_bytes()
    require(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'Integrity failed: '+name)
verdict=json.loads((base/'VERDICT.json').read_text())
require(verdict['math_issue_count']==0 and verdict['completion_estimate_percent']==100,'Final verdict is not closed PASS')
if '--replay' in sys.argv:
    for flags in [[],['-O']]:
        result=subprocess.run([sys.executable,*flags,str(base/'independent_controls.py')],capture_output=True,text=True)
        require(result.returncode==0,result.stderr)
        require(json.loads(result.stdout)['result']=='PASS','Controls did not pass')
print(json.dumps({'result':'PASS','authored_file_count':len(expected),'review_manifest_sha256':hashlib.sha256((base/'MANIFEST.json').read_bytes()).hexdigest(),'replayed':'--replay' in sys.argv}))
