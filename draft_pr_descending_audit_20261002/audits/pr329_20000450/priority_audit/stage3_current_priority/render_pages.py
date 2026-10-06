"""Render selected retrieved original pages with genuine native receipts."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,sys,re
N=Path(__file__).resolve().parent
name=sys.argv[1];assert re.fullmatch('[a-z0-9_]+',name)
pages=[int(x) for x in sys.argv[2].split(',')]
S=N/'private_evidence'/name/'source.bytes'
R=N/'private_evidence'/(name+'_visual');R.mkdir(exist_ok=False)
for page in pages:
 argv=['/opt/homebrew/bin/pdftoppm','-f',str(page),'-singlefile','-r','160','-png',str(S),str(R/('physical'+str(page)))]
 start=datetime.now(timezone.utc).isoformat();p=subprocess.run(argv,capture_output=True);end=datetime.now(timezone.utc).isoformat()
 (R/(str(page)+'.stdout')).write_bytes(p.stdout);(R/(str(page)+'.stderr')).write_bytes(p.stderr)
 sha=lambda b:hashlib.sha256(b).hexdigest()
 q=R/('physical'+str(page)+'.png')
 record={'kind':'genuine_native_original_page_render','argv':argv,'started_utc':start,'finished_utc':end,'actual_exit_code':p.returncode,'input_sha256':sha(S.read_bytes()),'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'image_sha256':sha(q.read_bytes()) if q.exists() else None,'image_bytes':q.stat().st_size if q.exists() else None,'inspection_limit':'Rendering alone is not agent visual inspection.'}
 (R/(str(page)+'.receipt.json')).write_text(json.dumps(record,indent=2)+'\n')
 print(json.dumps({'name':name,'page':page,'actual_exit_code':p.returncode,'finished_utc':end}))
 if p.returncode:raise SystemExit(p.returncode)
