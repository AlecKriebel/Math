#!/usr/bin/env python3
import datetime,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
TARGET=ROOT/'AUTHORED_SEAL.json'
def inventory():
 return {p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(ROOT.iterdir()) if p.is_file() and p!=TARGET and (p.suffix in {'.md','.json','.py','.txt'} or p.name=='.gitignore')}
if '--verify' in sys.argv:
 sealed=json.loads(TARGET.read_text());assert sealed['files']==inventory();print(json.dumps({'status':'PASS','authored_files':len(sealed['files']),'sealed_scope':'Top-level authored review artifacts only; scratch, runtime, raw media and third-party payloads excluded.'}))
else:
 rec={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'algorithm':'sha256','scope':'All top-level authored review artifacts except this seal; ignored runtime/extract/producer/mutation/render/media/wheel excluded.','files':inventory()}
 TARGET.write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps({'status':'SEALED','authored_files':len(rec['files'])}))
