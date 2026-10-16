"""Read-only native Git provenance comparison for all 31 archived originals."""
from pathlib import Path
import subprocess,json,hashlib
from datetime import datetime,timezone
W=Path(__file__).absolute().parent;R=W.parent
U=R/'pr_update/30005244';m=json.loads((U/'ORIGINAL_SUBMISSION_MANIFEST.json').read_text());head=m['original_PR_head']
rows=[]
for row in m['files']:
    spec=head+':'+row['native_path']
    oid=subprocess.run(['git','rev-parse',spec],cwd=R,capture_output=True,check=True,text=True).stdout.strip()
    b=subprocess.run(['git','cat-file','blob',spec],cwd=R,capture_output=True,check=True).stdout
    assert oid==row['native_blob'] and b==(U/row['archive_path']).read_bytes()
    rows.append({'native_path':row['native_path'],'native_blob':oid,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'native_object_matches_archive':True})
result={'utc':datetime.now(timezone.utc).isoformat(),'native_head':head,'read_only_commands':['git rev-parse <head>:<path>','git cat-file blob <head>:<path>'],'all_31_match':len(rows)==31,'files':rows}
(W/'NATIVE_PROVENANCE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'all_31_match':len(rows)==31,'native_head':head}))
